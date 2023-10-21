# azuracast_xmltv

**Create rich XMLTV Tuner and EPG files from an [AzuraCast](https://www.azuracast.com/) Web Radio.**

The big picture behind this is to create **standards-compliant files** to
- **easily access your station(s)** from almost any media player or server
- get **better distribution** by providing interested listeners with
  - an easy access to your stations and streams
  - an electronic program guide (EPG) so they can actively tune in to your shows
 
Therefore I recommend regenerating the files periodically and **linking to them on your website**, so your listeners can point their media centers/players directly at these links and stay up-to-date with your station(s) automatically.

Unfortunately, there isn’t a "standard" location for this yet. Maybe we should all start using `https://domain.tld/xmltv` for that, and
- put an `index.html` (or other) file there that lists the available links in human-readable form,
- use this as a base location for the `m3u` and `xml` files (i.e., get your station data by pointing to `https://domain.tld/xmltv/station.m3u` and get the EPG by pointing to `https://domain.tld/xmltv/domain.tld.xml`).

It would make things so much easier for server operators and listeners alike.

You’ll get **one M3U file per station** (containing that station's streams) and **one XML EPG file per AzuraCast instance** (containing the scheduled programs for all your stations).

### Some screenshots: This is what it looks like

When validated, you can import your M3U "tuner" and the XML EPG into your media center and **enjoy a beautiful LiveTV EPG** (and playout, of course):

![Live-TV – Mozilla Firefox_004](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/81ad9ccb-6d37-45e5-bc00-cb9ba5eff678)  
_EPG in Jellyfin_

![screenshot00001](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/765941a4-a4be-4bfd-8e22-f8fbf8f2559d)  
_EPG in KODI_

Some applications have no EPG support (yet), but are still nice to use. **You can use the M3U tuner file `azuracast_xmltv` generates** with these:

![Moonbase_001](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/4a5f84a0-64e9-4360-87dd-58e836fd1610)  
_Hypnotix, the Linux Mint IPTV player (no EPG yet)_

![Robert Long - Komisch_001](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/aa22201a-0c37-47ae-8f03-11c54f6c3b72)  
_Celluloid, a GTK+ frontend for mpv (no EPG)_

Note all this _may_ work on Windows machines, but I don’t know. I’m a Linux guy.


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

Perform a trial run, just executing `azuracast_xmltv`. Depending on your operating system, chances are that not all required Python modules are installed, and `azuracast_xmltv` will complain about that.

On Debian-like systems, you can easily install the missing modules using `pip3`. So let’s assume `azuracast_xmltv` complains: `ModuleNotFoundError: No module named 'lxml'`. Just go and install it:
```bash
pip3 install lxml
```

Then try again until all required modules are there. You have to do this only once. (On my Ubuntu 22.04 AzuraCast server, only the modules `lxml` and `tzlocal` were missing.)

_Hint:_ If you don’t even have `pip3`, a `sudo apt install python3-pip` helps. ;-)

For every new (or modified) station, use the `-m`/`--m3u` option on the first run, to generate its M3U file. On further runs, this can be omitted and `azuracast_xmltv` will only generate fresh EPG XML files.

On servers, just set up a _cron job_ for the software to update the EPG periodically.
Let’s assume you have saved the program as `/usr/local/bin/azuracast_xmltv`.

Use `crontab -e` to edit your crontab file, and add an entry like this:
```crontab
# get new EPG data for Jellyfin every 12 hours, 2 minutes past the hour
# avoiding clashes with the AzuraCast demo instance just being reset.
2 */12 * * * /usr/local/bin/azuracast_xmltv -u https://demo.azuracast.com
```
Add any command line options you want, of course.

If you don’t want the success/failure mails, simply send its output to `/dev/null`:
```crontab
# get new EPG data for Jellyfin every 12 hours, 2 minutes past the hour
# avoiding clashes with the AzuraCast demo instance just being reset.
2 */12 * * * /usr/local/bin/azuracast_xmltv -u https://demo.azuracast.com > /dev/null
```

## Usage

From the help screen:
```
usage: azuracast_xmltv [-h] [-v] [-u URL] [-i URL] [-d DAYS] [-f] [-o FOLDER]
                       [-a APIKEY] [-p] [-m]

Create XMLTV Tuner and EPG files from an AzuraCast Web Radio.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -u URL, --url URL     base URL to an AzuraCast instance
  -i URL, --icon URL    URL to a channel icon; will use station's default
                        album art if omitted
  -d DAYS, --days DAYS  number of days to include in the EPG
  -f, --fillgaps        fill gaps between programmes with a 'General Rotation'
                        entry
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

Edit './azuracast_xmltv' using a text editor
to change some defaults near the top of the file.

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
XMLTV/IPTV EPG data files are XML data files containing channel and program information. They must be compliant with the [XMLTV DTD](https://github.com/XMLTV/xmltv/blob/master/xmltv.dtd) and can be validated using the `tv_validate_file` tool, which can be installed on Debian-like systems with `sudo apt install xmltv-util`.

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

**Sample XMLTV EPG file `niteradio.example.com.xml`**

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

## A note on mount point display names

It makes no sense for an EPG to have a zillion entries called `/radio.mp3 (128kbps MP3)`. Seriously. A station might not even have a logo, so how would you distinguish all these in a large EPG?

The above will happen when you leave the mount point _Display Name_ empty, it’s just AzuraCast’s default.

My suggestion: Change the _Display Name_ of your station’s mount points to something meaningful that everyone can easily find and distinguish in the EPG. `azuracast_xmltv` will _automatically pick up the change_ when you run it with the `-m`/`--m3u` option next time.

As an example, I used
- Nite Radio (128kbps MP3)
- Nite Radio (128kbps AAC)
- Nite Radio Video-Stream
- Nite Radio Testbild

The HLS stream (if you have one), will automatically be named `<Your Station Name> (HLS)`.

## Fill the gaps between scheduled shows

You don’t have many scheduled shows but a 24/7 station and **want to show that something is playing** in the EPG?

`azuracast_xmltv` has the concept of _fillers_. Just use the `-f`/`--fillgaps` option and it will create nice programme entries for the times in between shows, and your listeners will know something is playing on the station.

The filler logic takes the playlist names that constitute your general rotation (enabled, type default, not on schedule), so **name your playlists wisely**. Let’s say you had a general rotation built of the 'Classic Rock', 'Folk Rock' and 'Hard Rock' playlist. `azuracast_xmltv` then generates a `{playlists}` variable for you that looks like `Classic Rock, Folk Rock & Hard Rock` and can be used in the configuration.

The default filler **can be configured in the options** near the start of the script file:

```python
# "Gap Filler" text to be shown when a programme is actually a gap filler.
# After parsing, the gap_filler_title will be used as playlist name and the result
# RE-PARSED by the requests_enabled parser, if ANY of the involved playlists has
# requests enabled. Descriptions from here and the requests enabled parsing will
# be APPENDED to each other (the request text coming beneath).

# this will be used as a programme's title
gap_filler_title = "24/7 Rock"
# this will be used as a programme's subtitle
gap_filler_subtitle = "{playlists}"
# this will be the programme's description
# Your text should make sense even if {playlists} is empty!
# Multiple successive blanks will be automatically replaced by a single blank.
gap_filler_description = """Your favorite sound, 24 hours a day, 7 days a week.
The best {playlists} in {year} — just here, on {station_name}."""
```

With our example, the generated EPG playlist entry would then look like this:

```xml
<programme start="20231020170000 +0200" stop="20231020180000 +0200" channel="niteradio.example.com">
  <title lang="en">24/7 Rock</title>
  <sub-title lang="en">Classic Rock, Folk Rock &amp; Hard Rock</sub-title>
  <desc lang="en">Your favorite sound, 24 hours a day, 7 days a week.
The best Classic Rock, Folk Rock &amp; Hard Rock in 2023 — just here, on Nite Radio.

Program Copyright © 2023 Nite Radio — Non-public test &amp; evaluation server only
Visit us on https://example.com</desc>
  <credits/>
  <category lang="en">Music</category>
</programme>
```

(The copyright part coming from another element, namely the `append_to_description` text.)


## Validation and other nice tools

Before going public, you should always check if your setup _validates_ as correct XMLTV data.

On Debian-like systems, install the `xmltv-util` package:
```bash
sudo apt install xmltv-util
```
then _validate_ your EPG file using:
```bash
tv_validate_file niteradio.example.com.xml
Validated ok.
```

Here is another nice trick: Output the EPG as text in your terminal!

```
tv_to_text niteradio.example.com.xml
10-18 (Wednesday)

06:00--12:00	Pop (requests enabled) // Your favorite station, YOUR music!	Nite Radio
12:00--16:00	Live: Moonbase	Nite Radio

10-21 (Saturday)

18:00--00:00	Heart Dance from London, UK	Nite Radio

10-22 (Sunday)

00:00--06:00	Nuit électronique (requests enabled) // Your favorite station, YOUR music!	Nite Radio

Generated from example.com by azuracast_xmltv 0.5.0.
```

Or even with long descriptions:

```
tv_to_text --with-desc radio.niteradio.net.xml 
10-18 (Wednesday)

06:00--12:00	Pop (requests enabled) // Your favorite station, YOUR music!	Nite Radio	Playlist: Pop  The request lines are open! Make this program YOURS by adding a request.  Go to https://example.com/public/niteradio, click on ›Request Song‹ and select your favorite.
12:00--16:00	Live: Moonbase	Nite Radio	Streamer: Moonbase  Live Show, hosted by Moonbase.  In his unmistakable way, Moonbase presents highlights of music history: Kraut and progressive rock, classic, glam and hard rock. Some metal, too. Some of his shows are centered around the finest electronic music in existence, most notably the Berlin School.  You CAN be excited. Or just have fun!

10-21 (Saturday)

18:00--00:00	Heart Dance from London, UK	Nite Radio	Playlist: Heart Dance from London, UK  (Syndicated content.)

10-22 (Sunday)

00:00--06:00	Nuit électronique (requests enabled) // Your favorite station, YOUR music!	Nite Radio	Playlist: Nuit électronique  The request lines are open! Make this program YOURS by adding a request.  Go to https://example.com/public/niteradio, click on ›Request Song‹ and select your favorite.

Generated from example.com by azuracast_xmltv 0.5.0.
```

## API Key

`azuracast_xmltv` _will_ work with any AzuraCast instance that uses scheduled programming, even stations that might not be your own. Please don’t overuse this—polling for a fresh EPG every 12, 24, or 48 hours is usually enough!

When using _your own station_, I recommend setting up an API key in your AzuraCast and use the `-a`/`--apikey` option, which will enable enhanced functionality and provide a much richer EPG.

If you use an API key, it will allow:
- using otherwise invisible mounts, like an added video stream
- customizable Live Show title/sub-title/description (streamer/DJ info)*
- customizable Live Show DJ info (mis-using Streamer Comment field)
- Live Show DJ image (if provided in AzuraCast); this is added as an
  image of type "person" in the programme's `<presenter>` info.
  Not all clients may support this (they'll just ignore it).
- customizable listener requests info (for playlists that have requests enabled)
- customizable syndication info (for playlists that are remote streams)
- gap filler `{playlists}` info

\* This also works without an API key.

## Making `azuracast_xmltv` your own

This is just a Python script, so you can open it using a text editor. (Windows users: No editors that produce a BOM, please! Use something like [Notepad++](https://notepad-plus-plus.org/).)

Near the beginning of the file, you’ll find many user-customizable options, most notably the program title/sub-title and description text to go with…
- _live shows_ (streamer/DJ),
- _syndicated content_ (remote playlists), and
- playlists that have _listener requests_ enabled.

You can also set defaults for most options here. These will be shown when `--help` is invoked.

## But wait… What do I _do_ with these files now?

I can’t give support for the many applications that use this format, but here’s a short list of apps I have tested or know they work fine with `azuracast_xmltv`:

- [Jellyfin](https://jellyfin.org/)\* - The Free Software Media System
- [KODI](https://kodi.tv/)\* - Entertainment Center
- [Plex](https://www.plex.tv) - (non-free)
- [Emby](https://emby.media/) - (non-free)
- [TVHeadend](https://tvheadend.org/)\* - TV Streaming Server and Recorder
- [Hypnotix](https://github.com/linuxmint/hypnotix)\* - The Linux Mint IPTV player (no EPG yet)
- [Celluloid](https://github.com/celluloid-player/celluloid)\* - A simple GTK+ frontend for mpv (no EPG); default video player in Linux Mint
- [VLC](https://www.videolan.org/vlc/)\* - The VLC media player (no EPG)
- xTeVe\* ([GitHub](https://github.com/xteve-project/xTeVe)) ([Documentation](https://github.com/xteve-project/xTeVe-Documentation/blob/master/en/configuration.md)) - M3U Proxy, recommended

Many others are out there in the wild. Consult their documentation to find how to set up "XMLTV" or "IPTV". In KODI, some are under "PVR …" (Personal Video Recorder).

### Further reading

Here are some links for looking up related items:

- The [XMLTV DTD](https://github.com/XMLTV/xmltv/blob/master/xmltv.dtd)\*
- [XMLTV.org](https://xmltv.org)
- [Kodi: IPTV einrichten](https://www.heise.de/tipps-tricks/Kodi-IPTV-einrichten-4676549.html) - (heise online; German)
- [What is Live TV, PVR and Radio?](https://kodi.wiki/view/PVR) - (KODI FAQ)
- [PVR IPTV Simple Client](https://kodi.wiki/view/Add-on:PVR_IPTV_Simple_Client)\* - IPTV client for KODI
- [Kodinerds](https://www.kodinerds.net/) - KODI-related German Forum
- [Kodinerds IPTV - Freie und legale Streams für Kodi](https://github.com/jnk22/kodinerds-iptv) - Free and legal streams for IPTV; German, but has international channels.
- [ErsatzTV](https://ersatztv.org/)\* - Your Personal IPTV Server

\* Free and Open Source Software I personally use and recommend.
