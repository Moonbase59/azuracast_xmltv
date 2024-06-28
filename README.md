# azuracast_xmltv

## Create rich XMLTV Tuner, EPG and RSS feeds from an [AzuraCast](https://www.azuracast.com/) Web Radio.

**If you like what you got, please consider to [![Donate with Paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif)](https://www.paypal.com/donate/?hosted_button_id=PBPR63362LDEU). Thank you! ❤️**

> _Don’t miss the [Discussions](https://github.com/Moonbase59/azuracast_xmltv/discussions)! New versions are announced there, and useful hints._

> _**Did you know? You can follow my [commits](https://github.com/Moonbase59/azuracast_xmltv/commits.atom), the [discussions](https://github.com/Moonbase59/azuracast_xmltv/discussions.atom) or just the [announcements](https://github.com/Moonbase59/azuracast_xmltv/discussions/categories/announcements.atom) using your RSS/Atom feed reader!** Just copy-paste the links into your reader as a new subscription and you’ll never miss anything again._

The big picture behind this is to create **standards-compliant files** to
- **easily access your station(s)** from almost any media player or server
- get **better distribution** by providing interested listeners with
  - an easy access to your stations and streams
  - an electronic program guide (EPG) so they can actively tune in to your shows
  - RSS Feeds with show info and direct links to the web player & streams

Therefore I recommend regenerating the files periodically and **linking to them on your website**, so your listeners can point their media centers/players directly at these links and stay up-to-date with your station(s) automatically.

Unfortunately, there isn’t a "standard" location for this yet. Maybe we should all start using `https://domain.tld/xmltv` for that, and
- put an `index.html` (or other) file there that lists the available links in human-readable form,
- use this as a base location for the `m3u` and `xml` files (i.e., get your station data by pointing to `https://domain.tld/xmltv/station.m3u` and get the EPG by pointing to `https://domain.tld/xmltv/domain.tld.xml`).
- from version 0.10.0 on, a gzip-compressed version can be made available at `https://domain.tld/xmltv/domain.tld.xml.gz`.

It would make things so much easier for server operators and listeners alike.

You’ll get **one M3U file per station** (containing that station’s streams), **one RSS file per station** (containing that station’s scheduled programs, web player and stream links), and **one XML EPG file per AzuraCast instance** (containing the scheduled programs for all your stations). Since v0.14.0, you also get an **additional M3U file per AzuraCast instance** (containing ALL station’s streams).

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

![News (1324) - cloud syvi net – Mozilla Firefox_001](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/20cb0cbe-7f38-4fc9-9b8a-07747207e29c)  
_Station RSS 2.0 Feed, as seen by Nextcloud (v0.12.0 and up)_


Note all this _may_ work on Windows machines, but I don’t know. I’m a Linux guy. You’ll run it on your AzuraCast server anyway, right?


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

### Install on a real AzuraCast server (Ubuntu 22.04)

Probably after trying out the above on a local machine, you might want to install `azuracast_xmltv` on your real AzuraCast server. Let’s assume you run AzuraCast on a remote Ubuntu 22.04 server in a Docker container (standard install) and you wish the output files to be available under `https://yourdomain.com/xmltv` as I suggested.

1. Log into your AzuraCast and create an API key for use with `azuracast_xmltv`. You’ll find the function under _My Account_. **Copy the key to a safe place and _keep it secret_!** After creating, **you will not be able to view the key again!**

   ![Auswahl_285](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/79d6c031-d9d7-47d5-bcd4-eb3888d2df93)

2. `ssh` into your AzuraCast server instance and become `root` (`sudo su`).

3. Install `azuracast_xmltv` as shown above. Put it in `/usr/local/bin`.

4. Change into the `/var/azuracast` folder and create a subfolder `xmltv`. This will later hold the files for your AzuraCast website.

   ```bash
    cd /var/azuracast
    mkdir xmltv
    ```

5. Modify the `docker-compose.override.yml` file and add an entry for the `xmltv` folder in the `volumes` section:

   ```bash
   nano docker-compose.override.yml
   ```

   ```yaml
   services:
     web:
       volumes:
         - /var/azuracast/xmltv:/var/azuracast/www/web/xmltv
   ```

6. Restart your AzuraCast so it can pick up the new settings:

   ```bash
   docker-compose down
   docker-compose up -d
   ```

7. Create a _crontab_ entry to run `azuracast_xmltv` periodically, let’s say twice a day, at 2 minutes past the hour:

   ```bash
   crontab -e
   ```

   ```crontab
   2 */12 * * * /usr/local/bin/azuracast_xmltv -o /var/azuracast/xmltv -u https://yourdomain.com -a 'your_api_key_here' -f -m -t > /dev/null
   ```

   Save the file.

   I left the `-m` option in here (will create M3U files), since my mounts might change, but you can also leave it out and create the M3U manually once. I also set the `-f` option to create _filler_ program entries. Use any options you want here.

   _Note:_ I also use the new `-t`/`--tvgurl` option here, since your files can now be found under your server’s `/xmltv/` path. This allows more modern software (like KODI) to automatically find the EPG data file (XML) belonging to the M3U.

8. Now change into the `xmltv` folder and run `azuracast_xmltv` once to check there are no errors, and get the initial set of files. You don’t want to wait for the next automatic update—it might be almost 12 hours away… Use _the exact same command you put into the crontab_ for this, just to be sure everything works.

   ```bash
   /usr/local/bin/azuracast_xmltv -o /var/azuracast/xmltv -u https://yourdomain.com -a 'your_api_key_here' -f -m -t -g
   ```
   Don’t forget to include the `-m` option, so it’ll create M3U files.

9. You should now be able to access the XMLTV data on your public AzuraCast website:

   ```
   https://yourdomain.com/xmltv/yourstation.m3u
   https://yourdomain.com/xmltv/yourdomain.com.xml
   https://yourdomain.com/xmltv/yourdomain.com.xml.gz
   ```

   Instead of `yourstation`, use the _station shortcode_ you have used when setting up your station. This is the "URL Stub" you might have changed under _Edit Station Profile → Profile_. You can see this field only in Advanced Mode:

   ![Auswahl_284](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/08b51d0b-0a3b-4e88-a340-4abe3afc6193)

   _Hint:_ Even if underscores `_` are shown in the example, **only use alphanumeric** characters and digits, and the hyphen `-` to comply with [RFC2838](https://www.rfc-editor.org/rfc/rfc2838.html). Underscores are not allowed in a domain name.


11. **Congratulations!** You can now **publish the above links on your website so your listeners will know where to point their media players and where to get the EPG!**

    Try it out using any media center or player I mentioned, or just do a quick test with an audio player like _Audacious_ or _VLC_.

    If your client supports the compressed gzip-format (.gz) for the EPG, you should use it. It reduces transmission time and bandwidth.

    And don’t forget to **log out** from your AzuraCast `ssh` session.

12. Optional fine-tuning:

    a) If your M3U shows some non-public streams and you don’t want that, use the `-p` option to only include streams that are marked _public_ in AzuraCast.

    b) You might want to edit the programme _text_ that `azuracast_xmltv` generates for the EPG listings and adapt these for your stations. The code is very well documented, just `ssh` into your server and edit it: `sudo nano /usr/local/bin/azuracast_xmltv`. The template texts near the beginning of the file are highly configurable (they use `{moustache}`-type variables) so you should be able to adapt to your needs easily.


## Usage

From the help screen:
```
usage: azuracast_xmltv [-h] [-v] [-u URL] [-i URL] [-c URL] [-d DAYS] [-f]
                       [-o FOLDER] [-a APIKEY] [-p] [-m] [--group GROUP] [-r]
                       [-t] [-g] [--rss]

Create XMLTV Tuner, EPG and RSS Feed files from an AzuraCast Web Radio.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -u URL, --url URL     base URL to an AzuraCast instance (default:
                        https://demo.azuracast.com)
  -i URL, --icon URL    URL to a channel icon; will use station's default
                        album art if omitted (default: None)
  -c URL, --customplayer URL
                        URL to a custom web player; modifies {player_url} and
                        {request_url} variables (default: None)
  -d DAYS, --days DAYS  number of days in the future [1-30] to include in the
                        EPG (default: 7)
  -f, --fillgaps        fill gaps between programmes with a 'General Rotation'
                        entry (default: False)
  -o FOLDER, --output FOLDER
                        output folder for XMLTV files (default: )
  -a APIKEY, --apikey APIKEY
                        AzuraCast API key; allows creating much better EPG
                        data, see below (default: None)
  -p, --public          include only public stations & streams (default:
                        False)
  -m, --m3u             create M3U XMLTV Tuner file(s); only needed on first
                        run or after changes in AzuraCast (default: False)
  --group GROUP         set M3U 'group-title' to something other than station
                        name (see below) (default: )
  -r, --radio           add 'radio="true"' tags to M3U #EXTINF; allows
                        distinction between radio and TV channels (see below)
                        (default: True)
  -t, --tvgurl          add 'tvg-url' tags to M3U file; allows software to
                        find the corresponding EPG automatically (see below)
                        (default: False)
  -g, --gzip            additionally output a gzip-compressed (.gz) version of
                        the EPG XML file; many clients can use this format,
                        and it reduces transmission time and bandwidth
                        (default: True)
  --rss                 create/update RSS 2.0 Feed(s); one feed per station
                        (default: False)

azuracast_xmltv can create XMLTV M3U Tuner, XML EPG and RSS 2.0 Feed files for
both your own and other AzuraCast stations.

For much better programme data to be generated, create an AzuraCast API key
and use the -a/--apikey option, which allows:
  - using otherwise invisible mounts, like an added video stream,
  - showing listener request info if a playlist has requests enabled
  - adding a presenter image on live shows, and (mis-)using the streamer
comment field as a description
  - showing extra info for syndicated content (remote playlists)

--group GROUP modifies the 'group-title' in M3U Tuner files. It normally
contains the station name. Using this, you can group all stations of an
AzuraCast server under a common name, or use something like 'Radio-DE' to
merge with larger, existing lists. A very few clients, like KODI, support
multiple groups. Separate these with a semicolon ';'. Empty values will be
replaced by the station name: ';Radio-DE' --> 'Your Station;Radio-DE',
'Radio;;Radio-DE' --> 'Radio;Your Station;Radio-DE'.

-r/--radio adds a 'radio="true"' tag to the M3U #EXTINF lines, if a stream’s
display name doesn’t contain any of the words 'Video', 'TV', 'Testbild',
'mpeg', 'mpg', 'm2t', 'm2ts', 'ts' (you can customize this list).
This is for software like KODI, which can distinguish between Radio and TV
channels and displays these in separate menus.

-t/--tvgurl adds 'url-tvg' and 'x-tvg-url' tags to the M3U Tuner files. This
helps media center software like KODI to automatically locate the
corresponding EPG data file, but only works if the generated M3U and XML files
are available under the '/xmltv' path of your AzuraCast server.
See installation instructions at
https://github.com/Moonbase59/azuracast_xmltv.

Output files are named after the (sanitized) station shortcode ("URL Stub" in
AzuraCast), and the server base URL.

Edit './azuracast_xmltv' using a text editor to change some defaults near the
top of the file. No worries, everything is well documented.

Please report any issues to
https://github.com/Moonbase59/azuracast_xmltv/issues.
```

## Sample output from the AzuraCast demo station

```bash
azuracast_xmltv -u https://demo.azuracast.com -m
```

### XMLTV Tuner file (one per station)
XMLTV/IPTV "Tuner" files are M3U files, in a special `#EXTM3U` format.

`azuracast_xmltv` names its output file after your station’s **shortcode** (called _URL Stub_ in the UI). Ideally, this should only contain alphanumeric characters and the '-' (minus or hyphen).

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

Beginning with `azuracast_xmltv` version 0.7.0, the M3U file entries (mount points) will be _sorted_ by their display name, and the _default mount_ put at the top.

Beginning with `azuracast_xmltv` version 0.18.0 and AzuraCast Rolling Release
\#c8bcee0 (2023-12-20 1:55), HLS streams set as default will "trump" Icecast/Shoutcast
default streams and be put at the top.

This is mainly intended for players that immediately start playing when opening an M3U file (they should play the default mount first), but also helpful for humans. We just like sorted lists. ;-) Putting HLS first provides easier use for "road warriors", on smartphones and car stereos, due to automatic bandwidth adjustment in areas with varying reception conditions.

More modern playout/media center software like KODI can automatically find the EPG file that corresponds to a M3U, thus reducing manual intervention and setup.

Beginning with version 0.7.0, you can use the `-t`/`--tvgurl` option to enable this feature. It _requires_ that your generated M3U and XML are reachable from the Internet under your AzuraCast server’s `/xmltv/` path. See the Installation instructions on how to achieve this.

### XMLTV Electronic Program Guide (EPG) file (one per server)
XMLTV/IPTV EPG data files are XML files containing channel and program information. They must be compliant with the [XMLTV DTD](https://github.com/XMLTV/xmltv/blob/master/xmltv.dtd) and can be validated using the `tv_validate_file` tool, which can be installed on Debian-like systems with `sudo apt install xmltv-util`.

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

## RSS 2.0 Feeds (one per station)

From version 0.12.0, `azuracast_xmltv` can optionally generate **RSS 2.0 Feeds**, too. Using the `--rss` option, these can be created/updated together with the EPG in one go. We produce one file per station, which can easily be cached for great performance.

The RSS feeds build on the already existing, flexible customization logic and can even use HTML code (although some readers strip some HTML elements). You get a chronological feed with all your shows, image, description, web player and stream links. My generator uses modern technologies, `<media:…>` elements and all.

### Here are some screenshots

![Auswahl_296](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/07b69b8c-9dbe-444d-9bb9-a48f39682bdb)  
_Station RSS Feed as seen by Nextcloud._

Scheduled programmes are presented in a chronological list, click on a list entry for more information, or click the globe icon to directly jump to the station’s web player to make a request.

![News (1324) - cloud syvi net – Mozilla Firefox_001](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/c0bc9a8e-3cb2-4fdf-8571-c5bea147f7e4)  
_Single programme as seen by Nextcloud_

The description is highly configurable, as with the EPG, but you can even use HTML here.

A click on the image opens the web player.

![Nite Radio – Mozilla Firefox_032](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/3ff33950-cde5-4bf1-b821-89d6a824795a)  
_Station RSS Feed as seen by the Firefox "Livemarks" extension_

The RSS feed looks good even in the most basic feed reader. A click on the title opens the web player, but here you also have _direct links to all the station’s streams_. Listeners enjoy the information, and your station is always only one click away.

![Liferea_001](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/fff3ad14-da01-4104-b94a-4bb66eaa80c8)  
_Station RSS Feed as seen by Liferea (a famous Linux feed reader)_

![Liferea_002](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/e05bd58d-a684-470d-ad37-0228eabfc951)  
_You can even use the web player within some feed readers_

The RSS 2.0 Feeds we generate are _standards-compliant_ and usually _validate_ just fine. Some validators have problems with feed items lying in the future, that can safely be ignored.

We use the most _modern technologies_ and the _most compatible_ set of features, so chances are good that a feature _is already there_ when feed readers finally catch up. Currently, not every feed reader supports all features.


## A note on mount point display names

It makes no sense for an EPG to have a zillion entries called `/radio.mp3 (128kbps MP3)`. Seriously. A station might not even have a logo, so how would you distinguish all these in a large EPG?

The above will happen when you leave the mount point _Display Name_ empty, it’s just AzuraCast’s default.

My suggestion: Change the _Display Name_ of your station’s mount points to something meaningful that everyone can easily find and distinguish in the EPG. `azuracast_xmltv` will _automatically pick up the change_ when you run it with the `-m`/`--m3u` option next time.

As an example, I used
- Nite Radio (128kbps AAC)
- Nite Radio (128kbps MP3)
- Nite Radio Testbild
- Nite Radio Video-Stream

The HLS stream (if you have one), will automatically be named `<Your Station Name> (HLS)`.

### Distinguishing audio and video streams

Some media center software (like _KODI_) can distinguish between "Radio" and "TV" and puts streams under "Radio" and "TV" menus, respectively. The distinction is made by a flag `radio="true"`on the M3U `#EXTINF` lines.

From version 0.11.0, `azuracast_xmltv` fully supports this feature if the `-r`/`--radio` option is used (default).

`azuracast_xmltv` will look for a list of keywords in your stream name, and flag it a video stream if any of the following keywords are found in the stream display name: `Video`, `TV`, `Testbild`, `mpeg`, `mpg`, `m2t`, `m2ts`, `ts`. The comparison is case-insensitive, also expanding some language-specific characters, like the German "ß" to "ss".

You can edit the default keyword list near the beginning of the file. It is called `videostream_keywords`.

In _KODI_ this will later look like this:

![screenshot00010](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/32f4657e-9b8c-413a-8a25-fb07e4053ecb)  
_Radio: audio streams only_

![screenshot00009](https://github.com/Moonbase59/azuracast_xmltv/assets/3706922/6cf1fe7b-4342-45af-870b-2738f543fdc4)  
_TV: video streams only_

### Grouping streams and stations

_To be supplied._

Read the built-in help in the meantime: `azuracast_xmltv --help`.


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
- _syndicated content_ (remote playlists),
- playlists that have _listener requests_ enabled,
- _gap filler_ programmes, and
- _RSS Feeds_ (HTML allowed here).

You can also set defaults for most options here. These will be shown when `--help` is invoked.

### `azuracast_xmltv` as a Python module

`azuracast_xmltv` can be used and imported as a Python module. Just rename (or symlink) it to have a `.py` file extension.

All usual module functions should work, like `import`, help and documentation with tools like `pdoc`.

### `{moustache}`-type variables that can be used in customization

Using this type of marking a _variable_ part of text is commonly used. While executing, `azuracast_xmltv` will replace these with the actual content, for example replace `{year}` with `2023` (if the programme starts in 2023). `azuracast_xmltv` will also automatically remove any leftover extra whitespace after replacing the variables.

"Extra whitespace" is, for instance, multiple blanks in succession or extra linefeeds at the end of the text. This can happen when a variable to be replaced is actually empty.

**An example:**

You might have specified `The best {playlists} in {year}.` in the `gap_filler_description`, which would normally expand to `The best Classic Rock, Folk Rock & Hard Rock in 2023.`

But you haven’t used an _API key_, which is needed to use `{playlists}`, so we would get `The best  in 2023.` The double space looks awful, right?

`azuracast_xmltv` will automatically detect this and correct to `The best in 2023.` Much better!

#### Always available

- `{station_name}`
- `{station_description}`
- `{station_website}` — the station website URL (this is _not_ the AzuraCast URL)
- `{player_url}`\*\* — station’s web player URL
- `{year}` — start year of the programme
- `{category}` — global category, usually "Music"

#### In `requests_enabled`

- `{playlist}` — playlist name
- `{request_url}`\*\* — station’s web player URL

#### In `remote`\*

- `{playlist}` — playlist name
- `{remote_url}` — remote URL used in the playlist

#### In `live`

- `{presenter}` — streamer/DJ name
- `{image_url}`\* — streamer’s image URL
- `{comments}`\* — AzuraCast’s Streamer Comments field content.  
  _Note:_ Comments should be used with care: This field was originally meant for _internal_ remarks only, **you could leak data!**

#### In `gap_filler`

- `{playlists}`\* — comma-separated list of playlist names that make up the general rotation (enabled, type default, not on schedule).  
  So if your general rotation was made up of the playlists `Classic Rock`, `Folk Rock` and `Hard Rock`, it would show `Classic Rock, Folk Rock & Hard Rock`.

#### In `rss_feed_description`

- `{title}` — programme title
- `{subtitle}` — programme sub-title
- `{airdate}` — date of programme start "YYYY-MM-DD"
- `{airtime}` — programme start & end time "HH:MM–HH:MM"
- `{airtime_length}` — programme length "HH:MM"
- `{desc}` — original programme description, generated from above elements. Newlines in `{desc}` will automatically be converted to `<br/>`.

\* = This can only be used with an API key, i.e., on your own station.

\*\* = URL to AzuraCast’s web player, or a custom player specified using the `-c`/`--customplayer` option. Use the latter to point listeners to a customized player on your station’s website instead of the default one.

## FAQ: Frequently Asked Questions

### I get `Check URLs! – 'http://…/api/status' redirected to 'https://…/api/status' [301, 200]`

This can happen in the initial server verification phase and is actually a _warning_. `azuracast_xmltv` will try to continue if it can find a live AzuraCast server.

In the case shown, your request was redirected from a `http://` to a `https://` URL.
Since HTTP status 301 means "moved permanently", you should re-invoke the command,
this time using the `https://` URL. The URL you give on the commandline is used
to construct the URLs in the various M3U, XML and RSS files, and you wouldn’t want
to publicize "wrong" URLs. Even if they work, it looks unprofessional and generates
unnecessary traffic.

There _are_ situations where you want to _keep_ the un-redirected URLs, though.
Let’s assume your server is in maintenenace and you have a _temporary_ redirect
to a backup server for the time being (307 Temporary Redirect). In this case,
you want to keep the "old" URLs and just let `azuracast_xmltv` continue.

### I get `HTTPError – 403 Client Error: Forbidden for url: …`

In almost all cases, this means the API key given didn’t work. `azuracast_xmltv` will continue as if no API key had been given.

The user who generated the API key in AzuraCast must have appropriate rights to access the station’s …
- mounts,
- playlists, and
- streamers/DJs.

Or maybe there was a typo or a character left out while copying the API key.

### I get `HTTPError – 500 Server Error: Internal Server Error for url: https://…/api/station/STATION_ID/mounts`

This means the station with ID `STATION_ID` has no mounts. Maybe they aren’t set up yet, or the station is HLS-only and doesn’t use Icecast or Shoutcast.

`azuracast_xmltv` will continue normally.

### How do you handle different timezones?

Timezones should be handled correctly: Linux servers, AzuraCast, `azuracast_xmltv`, the XMLTV EPG file standard, and the clients know about timezones.

You can set your station’s timezone in AzuraCast, and `azuracast_xmltv` will simply use the timezone of the machine it runs on. Since `azuracast_xmltv` normally runs on your AzuraCast server (which should be set up correctly, ask your system administrator), all should be well.

If you experience any problems (like EPG hours being offset), it is usually the client software’s fault (the EPG reading application). The files `azuracast_xmltv` generates contain the correct timezone UTC offsets as specified in the protocol.

### What about daylight savings time?

Both AzuraCast and `azuracast_xmltv` handle this correctly, if the server has been set up correctly.

Here is an example of a programme that runs on 2023-10-29 00:00–06:00 in Germany. Now that night at 03:00 clocks in Germany will be reset to 02:00 since daylight savings time ends. The generated EPG code looks like this:

```xml
<programme start="20231029000000 +0200" stop="20231029060000 +0100" channel="niteradio.example.com">
  <title lang="en">Nuit électronique</title>
  <desc lang="en">Playliste: Nuit électronique</desc>
  <credits/>
  <category lang="en">Music</category>
</programme>
```

As you can see, the UTC time offset at the start of the programme is `+0200`, and `+0100` at its end. A standards-compliant EPG client should be able to handle this correctly. The programme starts at 00:00 daylight savings time and ends at 06:00 normal time, making for an actual duration of 7 hours.

### What about the gzip-compressed `.gz` file?

#### Should I use it?

Absolutely. Many clients like _KODI_ and _xTeVe_ support reading this format. Since files are _much_ smaller, it decreases transmission time and bandwidth drastically.

#### Why provide _both_ `.xml` and `.xml.gz`?

Some clients don’t yet support the modern, compressed version of the EPG. Offer both and let the client decide which to use.

This is also the reason why the `url-tvg` and `x-tvg-url` entries in the M3U file (if you use the `-t`/`--tvgurl` option) point to the `.xml` version of the file, _not_ to the gzipped version.


## But wait… What do I _do_ with these files now?

I can’t give support for the many applications that use this format, but here’s a short list of apps I have tested or know they work fine with `azuracast_xmltv`:

- [Jellyfin](https://jellyfin.org/)\* – The Free Software Media System
- [KODI](https://kodi.tv/)\* – Entertainment Center
- [Plex](https://www.plex.tv) – (non-free)
- [Emby](https://emby.media/) – (non-free)
- [TVHeadend](https://tvheadend.org/)\* – TV Streaming Server and Recorder
- [Hypnotix](https://github.com/linuxmint/hypnotix)\* – The Linux Mint IPTV player (no EPG yet)
- [Celluloid](https://github.com/celluloid-player/celluloid)\* – A simple GTK+ frontend for mpv (no EPG); default video player in Linux Mint
- [VLC](https://www.videolan.org/vlc/)\* – The VLC media player (no EPG)
- xTeVe\* ([GitHub](https://github.com/xteve-project/xTeVe)) ([Documentation](https://github.com/xteve-project/xTeVe-Documentation/blob/master/en/configuration.md)) – M3U Proxy, recommended
- [Liferea](https://lzone.de/liferea/)\*, [Thunderbird](https://www.thunderbird.net/)\*, [Nextcloud](https://nextcloud.com/)\* – are/have good RSS feed readers (just a random selection, because I use all of these)

Many others are out there in the wild. Consult their documentation to find how to set up "XMLTV" or "IPTV". In KODI, some are under "PVR …" (Personal Video Recorder).

### Further reading

Here are some links for looking up related items:

- The [XMLTV DTD](https://github.com/XMLTV/xmltv/blob/master/xmltv.dtd)\*
- [XMLTV.org](https://xmltv.org)
- [Kodi: IPTV einrichten](https://www.heise.de/tipps-tricks/Kodi-IPTV-einrichten-4676549.html) – (heise online; German)
- [What is Live TV, PVR and Radio?](https://kodi.wiki/view/PVR) – (KODI FAQ)
- [PVR IPTV Simple Client](https://kodi.wiki/view/Add-on:PVR_IPTV_Simple_Client)\* – IPTV client for KODI
- [Kodinerds](https://www.kodinerds.net/) – KODI-related German Forum
- [Kodinerds IPTV - Freie und legale Streams für Kodi](https://github.com/jnk22/kodinerds-iptv) – Free and legal streams for IPTV; German, but has international channels.
- [ErsatzTV](https://ersatztv.org/)\* – Your Personal IPTV Server
- The [RSS 2.0 Specification](https://www.rssboard.org/rss-specification)\* – RSS Advisory Board

\* Free and Open Source Software I personally use and recommend.
