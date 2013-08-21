# Blank Python
sourcescraper = 'lse_podcast_feed'
import scraperwiki
import datetime

scraperwiki.utils.httpresponseheader('Content-Type', 'application/rss+xml')

scraperwiki.sqlite.attach("lse_podcast_feed")
episodes = scraperwiki.sqlite.select("* from lse_podcast_feed.swdata")

PODCAST_TEMPLATE = """\
<rss version="2.0">
    <channel>
        <title>%(title)s</title>
        <description>%(description)s</description>
        <link>%(link)s</link>
        <lastBuildDate>%(builddate)s</lastBuildDate>
        <pubDate>%(pubdate)s</pubDate>
        <generator>%(generator)s</generator>
        %(items)s
    </channel>
</rss>
"""

ITEM_TEMPLATE = """\
    <item>
        <title>%(title)s</title>
        <description>%(description)s</description>
        <link>%(link)s</link>
        <enclosure url="%(mp3)s" length="%(mp3_bytes)s" type="audio/mpeg"/>
        <guid isPermaLink="true">%(link)s</guid>
        <pubDate>%(pubdate)s</pubDate>
    </item>
"""

#Time format:
#Mon, 24 Jul 2006 17:59:28 -0400

podcast_data = {
    'title': 'LSE Podcast',
    'description': "A collection of audio from LSE's programme of public lectures and events.",
    'link': 'http://www2.lse.ac.uk/newsAndMedia/videoAndAudio/channels/publicLecturesAndEvents/latest100.aspx',
    'builddate': datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S -0000'),
    'pubdate': max(datetime.datetime.strptime(ep['pubdate'], '%a, %d %b %Y %H:%M:%S -0000') for ep in episodes).strftime('%a, %d %b %Y %H:%M:%S -0000'),
    'generator': 'https://scraperwiki.com/scrapers/lse_podcast_feed/',
    'items': '\n'.join(ITEM_TEMPLATE % episode for episode in episodes),
}

print PODCAST_TEMPLATE % podcast_data