import feedparser
import scrapemark
import scraperwiki

def get_challenges_from_challengedotgov():
    feed = feedparser.parse("http://challenge.gov/search.rss")
    entries = []
    entries.extend(feed["items"])
    for entry in entries:
        # remove spaces from links
        entry["link"] = entry["link"].replace(" ", "")
        data = (
            {
                "title" : entry["title"],
                "identifier" : entry["link"],
                "modified" : entry["updated"],
                "abstract" : entry["description"],
                "source" : "http://www.challenge.gov"
            }
        )
        scraperwiki.sqlite.save(unique_keys=['identifier'], data = data)

def get_challenges_from_innocentive():
    feed = feedparser.parse("http://www.innocentive.com/rss/challenges.xml")
    entries = []
    entries.extend(feed["items"])
    for entry in entries:
        description = scrapemark.scrape("""
            <td valign='top'>
                <p>
                    {{ text }}
                </p>
            </td>
            """,
            entry["description"]
        )
        data = (
            {
                "title" : entry["title"],
                "identifier" : entry["link"],
                "modified" : entry["updated"],
                "abstract" : description["text"],
                "source" : "http://www.innocentive.com"
            }
        )
        scraperwiki.sqlite.save(unique_keys=['identifier'], data = data)

def get_challenges_from_openideo(feed_list = []):
    if not feed_list:
        feed_list = scrapemark.scrape("""
            <table class="challenge-list" cellspacing="0">
            <tr />
            {*
                <tr>
                <td>
                    <h4>
                        <a href='{{ [].url }}'/>
                    </h4>
                    <div>{{ [].description }}</div>
                </td>
                </tr>
            *}
            </table>
            """,
            url = "http://www.openideo.com/open"
        )
        if feed_list:
            for item in feed_list:
                item["url"] = item["url"].replace("brief.html", "feed.rss")
            get_challenges_from_openideo(feed_list)
    else:
        for item in feed_list:
            feed = feedparser.parse(item["url"])
            if not feed["bozo"]:
                data = (
                    {
                        "title" : feed["channel"]["title"],
                        "identifier" : feed["channel"]["link"],
                        "modified" : feed["channel"]["updated"],
                        "abstract" : item["description"],
                        "source" : "http://www.openideo.com"
                    }
                )
                scraperwiki.sqlite.save(unique_keys=['identifier'], data = data)

token_dict = {
    "challengedotgov" : get_challenges_from_challengedotgov,
    "innocentive" : get_challenges_from_innocentive,
    "openideo" : get_challenges_from_openideo
}

def Main():
    for key in token_dict.iterkeys():
        token_dict[key]()

Main()