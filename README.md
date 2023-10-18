# azuracast_xmltv
Create rich XMLTV Tuner and EPG files from an AzuraCast Web Radio.

More info will follow soon…

## Installation

- Download `azuracast_xmltv`, put it in a location that’s in your path (on Linux servers, you can use `/usr/local/bin`, on desktop systems `~/.local/bin` or `~/bin` is usually also good).
- On a remote server, you can use _wget_ or _curl_ to download it:
  ```bash
  wget azuracast_xmltv https://raw.githubusercontent.com/Moonbase59/azuracast_xmltv/master/azuracast_xmltv
  ```
  ```bash
  curl -o azuracast_xmltv https://raw.githubusercontent.com/Moonbase59/azuracast_xmltv/master/azuracast_xmltv
  ```
- Make it executable (`chmod +x azuracast_xmltv`).
- Optionally, open in a text editor and modify defaults near the beginning of the file.

For every new station, use the `-m`/`--m3u` option on the first run, to generate its M3U file. On further runs, this can be omitted and `azuracast_xmltv` will only generate fresh EPG XML files.

On servers, just set up a _cron job_ for the software to update the EPG periodically.
Let’s assume you have saved the program as `/usr/local/bin/azuracast_xmltv`.

Use `crontab -e` to edit your crontab file, and add an entry like this:
```crontab
# get new EPG data for Jellyfin every 12 hours
0 */12 * * * /usr/local/bin/azuracast_xmltv -u https://demo.azuracast.com
```
Add any command line options you want, of course.

If you don’t want the success/failure mails, simply send its output to `/dev/null`:
```crontab
# get new EPG data for Jellyfin every 12 hours
0 */12 * * * /usr/local/bin/azuracast_xmltv -u https://demo.azuracast.com > /dev/null
```

## Usage

From the help screen:
```bash
usage: azuracast_xmltv [-h] [-v] [-u URL] [-i URL] [-d DAYS] [-o FOLDER]
                       [-a APIKEY] [-p] [-m]

Create XMLTV Tuner and EPG files from an AzuraCast Web Radio.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -u URL, --url URL     base URL to an AzuraCast instance
  -i URL, --icon URL    URL to a channel icon; will use station's default
                        album art if omitted
  -d DAYS, --days DAYS  number of days to include in the EPG
  -o FOLDER, --output FOLDER
                        output folder for XMLTV files
  -a APIKEY, --apikey APIKEY
                        AzuraCast API key; allows creating much better EPG
                        data, see below
  -p, --public          include only public stations & streams
  -m, --m3u             create M3U XMLTV Tuner file(s); only needed on first
                        run or after changes in AzuraCast

azuracast_xmltv can create XMLTV M3U Tuner files and XML EPG files for both
your own and other AzuraCast stations.

For much better programme data to be generated, create an AzuraCast API key
and use the -a/--apikey option, which allows:
  - using otherwise invisible mounts, like an added video stream,
  - showing listener request info if a playlist has requests enabled
  - adding a presenter image on live shows, and (mis-)using the
    streamer comment field as a description
  - showing extra info for syndicated content (remote playlists)

Edit './azuracast_xmltv' using a text editor to change
some defaults near the top of the file.

Please report any issues to https://github.com/Moonbase59/azuracast_xmltv/issues.
```

## Sample output from the AzuraCast demo station

```bash
azuracast_xmltv -u https://demo.azuracast.com -m
```

### XMLTV Tuner file (one per station)
XMLTV/IPTV "Tuner" files are M3U files, in a special `#EXTM3U` format.

`azuracast_xmltv` names its output file after your station’s **shortname**. Ideally, this should only contain alphanumeric characters and the '-' (minus or hyphen).

**Sample XMLTV Tuner file `azuratest_radio.m3u`**

```m3u
#EXTM3U
#EXTINF:-1 tvg-name="/radio.mp3 (128kbps MP3)" tvg-id="azuratest_radio.demo.azuracast.com" group-title="AzuraTest Radio" tvg-logo="https://demo.azuracast.com/api/station/1/art/0",/radio.mp3 (128kbps MP3)
https://demo.azuracast.com/listen/azuratest_radio/radio.mp3
#EXTINF:-1 tvg-name="/mobile.mp3 (64kbps MP3)" tvg-id="azuratest_radio.demo.azuracast.com" group-title="AzuraTest Radio" tvg-logo="https://demo.azuracast.com/api/station/1/art/0",/mobile.mp3 (64kbps MP3)
https://demo.azuracast.com/listen/azuratest_radio/mobile.mp3
#EXTINF:-1 tvg-name="AzuraTest Radio (HLS)" tvg-id="azuratest_radio.demo.azuracast.com" group-title="AzuraTest Radio" tvg-logo="https://demo.azuracast.com/api/station/1/art/0",AzuraTest Radio (HLS)
https://demo.azuracast.com/hls/azuratest_radio/live.m3u8
```

### XMLTV Electronic Program Guide (EPG) file (one per server)
XMLTV/IPTV EPG data files are XML data files containg channel and program information. They must be compliant with the [XMLTV DTD](https://github.com/XMLTV/xmltv/blob/master/xmltv.dtd) and can be validated using the `tv_validate_file` tool, which can be installed on Debian-like systems with `sudo apt install xmltv-util`.

This package brings some other nice utilities, just try `tv_to_text <yourstation>.xml`.

The XML files `azuracast_xmltv` produces are roughly named after [RFC2838 - Uniform Resource Identifiers for Television Broadcasts](https://www.rfc-editor.org/rfc/rfc2838.html). They _look_ like DNS names, but _aren’t_, really. We use these names as TV Guide "channel IDs", to hold the M3U and XML data together, so that automated tools like [xTeVe](https://github.com/xteve-project/xTeVe), and media servers like [Jellyfin](https://jellyfin.org/) or [KODI](https://kodi.tv/) can auto-assign channels and you have less work.

There are some dumber media servers (like Plex, for an example) that don’t handle many M3U/XML files well. This is the reason why we create only _one_ EPG data file per AzuraCast instance (including all its stations).


**Sample XMLTV EPG file `demo.azuracast.com.xml`**

```xml
<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE tv SYSTEM "xmltv.dtd">
<tv date="20231018210640 +0200" source-info-url="https://demo.azuracast.com" source-info-name="demo.azuracast.com" generator-info-name="azuracast_xmltv 0.5.0" generator-info-url="https://github.com/Moonbase59/azuracast_xmltv">
  <channel id="azuratest_radio.demo.azuracast.com">
    <display-name>AzuraTest Radio</display-name>
    <icon src="https://demo.azuracast.com/api/station/1/art/0"/>
  </channel>
</tv>
```

Too sad, the AzuraCast demo instance has nothing on schedule right now… Let me show you part of an EPG file from my evaluation station (URLs modified):

```xml
<?xml version='1.0' encoding='UTF-8'?>
<!DOCTYPE tv SYSTEM "xmltv.dtd">
<tv date="20231018214854 +0200" source-info-url="https://example.com" source-info-name="example.com" generator-info-name="azuracast_xmltv 0.5.0" generator-info-url="https://github.com/Moonbase59/azuracast_xmltv">
  <channel id="niteradio.example.com">
    <display-name>Nite Radio</display-name>
    <icon src="https://example.com/api/station/1/art/0"/>
  </channel>
  <programme start="20231018060000 +0200" stop="20231018120000 +0200" channel="niteradio.example.com">
    <title lang="en">Pop (requests enabled)</title>
    <sub-title lang="en">Your favorite station, YOUR music!</sub-title>
    <desc lang="en">Playlist: Pop

The request lines are open! Make this program YOURS by adding a request.

Go to https://example.com/public/niteradio, click on ›Request Song‹ and select your favorite.
</desc>
    <credits/>
    <category lang="en">Music</category>
  </programme>
  <programme start="20231018120000 +0200" stop="20231018160000 +0200" channel="niteradio.example.com">
    <title lang="en">Live: Moonbase</title>
    <desc lang="en">Streamer: Moonbase

Live Show, hosted by Moonbase.

In his unmistakable way, Moonbase presents highlights of music history: Kraut and progressive rock, classic, glam and hard rock. Some metal, too. Some of his shows are centered around the finest electronic music in existence, most notably the Berlin School.

You CAN be excited. Or just have fun!
</desc>
    <credits>
      <presenter>Moonbase<image type="person">https://example.com/api/station/1/streamer/1%7C1678618644/art</image></presenter>
    </credits>
    <category lang="en">Music</category>
  </programme>

  ...
  
  <programme start="20231021180000 +0200" stop="20231022000000 +0200" channel="niteradio.example.com">
    <title lang="en">Heart Dance from London, UK</title>
    <desc lang="en">Playlist: Heart Dance from London, UK

(Syndicated content.)
</desc>
    <credits/>
    <category lang="en">Music</category>
  </programme>
  <programme start="20231022000000 +0200" stop="20231022060000 +0200" channel="niteradio.example.com">
    <title lang="en">Nuit électronique (requests enabled)</title>
    <sub-title lang="en">Your favorite station, YOUR music!</sub-title>
    <desc lang="en">Playlist: Nuit électronique

The request lines are open! Make this program YOURS by adding a request.

Go to https://example.com/public/niteradio, click on ›Request Song‹ and select your favorite.
</desc>
    <credits/>
    <category lang="en">Music</category>
  </programme>
</tv>
```

Now _this_ looks like some program, right?

## API Key

`azuracast_xmltv` _will_ work with any AzuraCast instance that uses scheduled programming, even stations that might not be your own. Please don’t overuse this—polling for a fresh EPG every 12, 24, or 48 hours is usually enough!

When using _your own station_, I recommend setting up an API key in your AzuraCast and use the `-a`/`--apikey` option, which will enable enhanced functionality and provide a much richer EPG.

## Making `azuracast_xmltv` your own

This is just a Python script, so you can open it using a text editor. (Windows users: No editors that produce a BOM, please! Use something like [Notepad++](https://notepad-plus-plus.org/).)

Near the beginning of the file, you’ll find many user-customizable options, most notably the program title/sub-title and description text to go with a) _live shows_ (streamer/DJ), b) _syndicated content_ (remote playlists), and c) playlists that have _listener requests_ enabled.

You can also set defaults for most options here. These will be shown when `--help` is invoked.
