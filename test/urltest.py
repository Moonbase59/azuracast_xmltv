#!/usr/bin/env python3
# encoding: utf-8

# (?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))

import re

def linkify_urls(text):
    """
    (Try to) replace any URLs in text with anchor links, for HTML conversion.
    Based on John Gruber’s article: https://daringfireball.net/2010/07/improved_regex_for_matching_urls
    and Gist: https://gist.github.com/gruber/249502
    "Liberal Regex Pattern for Any URLs"
    """
    urls = re.compile(r"(?i)\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", re.MULTILINE|re.UNICODE)
    text = urls.sub(r'<a href="\1" target="_blank">\1</a>', text)
    return text

text = """Besuche uns auf https://radio.niteradio.net/public/niteradio.
Oder mail an mailto:moonbase@quantentunnel.de!
wie wär’s mit www.example.com? Oder so …
Know what?  A domain like http://موقع.وزارة-الاتصالات.مصر/ is actually legal nowadays!

A blog link: Does it crap out? (It DOES!)

John Gruber’s test data:

Test data for the URL-matching regex pattern presented here:

http://daringfireball.net/2010/07/improved_regex_for_matching_urls


Matches the right thing in the following lines:

	http://foo.com/blah_blah
	http://foo.com/blah_blah/
	(Something like http://foo.com/blah_blah)
	http://foo.com/blah_blah_(wikipedia)
	http://foo.com/more_(than)_one_(parens)
	(Something like http://foo.com/blah_blah_(wikipedia))
	http://foo.com/blah_(wikipedia)#cite-1
	http://foo.com/blah_(wikipedia)_blah#cite-1
	http://foo.com/unicode_(✪)_in_parens
	http://foo.com/(something)?after=parens
	http://foo.com/blah_blah.
	http://foo.com/blah_blah/.
	<http://foo.com/blah_blah>
	<http://foo.com/blah_blah/>
	http://foo.com/blah_blah,
	http://www.extinguishedscholar.com/wpglob/?p=364.
	http://✪df.ws/1234
	rdar://1234
	rdar:/1234
	x-yojimbo-item://6303E4C1-6A6E-45A6-AB9D-3A908F59AE0E
	message://%3c330e7f840905021726r6a4ba78dkf1fd71420c1bf6ff@mail.gmail.com%3e
	http://➡.ws/䨹
	www.c.ws/䨹
	<tag>http://example.com</tag>
	Just a www.example.com link.
	http://example.com/something?with,commas,in,url, but not at end
	What about <mailto:gruber@daringfireball.net?subject=TEST> (including brokets).
	mailto:name@example.com
	bit.ly/foo
	“is.gd/foo/”
	WWW.EXAMPLE.COM
	http://www.asianewsphoto.com/(S(neugxif4twuizg551ywh3f55))/Web_ENG/View_DetailPhoto.aspx?PicId=752
	http://www.asianewsphoto.com/(S(neugxif4twuizg551ywh3f55))
	http://lcweb2.loc.gov/cgi-bin/query/h?pp/horyd:@field(NUMBER+@band(thc+5a46634))

	
Should fail against:
	6:00p
	filename.txt

	
Known to fail against:
	http://example.com/quotes-are-“part”
	✪df.ws/1234
	example.com
	example.com/


"""

print(linkify_urls(text))
