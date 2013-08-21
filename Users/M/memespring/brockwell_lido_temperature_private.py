import scraperwiki
import lxml.html, lxml.cssselect
import re
import dateutil.parser

def extract_temperature(text):

    result = None
    regex = r'(?P<temperature>\d+\.?\d?)\s?[degrees|Degrees|deg|Deg|c|C]'
    RE = re.compile(regex, re.DOTALL)
    match = RE.search(text)
    if match:
        result = float(match.group('temperature'))
    return result


root = lxml.html.parse('http://search.twitter.com/search.atom?q=brockwelllido').getroot()
for item in root.cssselect('feed > entry'):
    tweet_id = item.cssselect('id')[0].text
    tweet = item.cssselect('title')[0].text
    date_time = dateutil.parser.parse(item.cssselect('published')[0].text) #2011-05-27T10:15:02Z
    temperature = extract_temperature(tweet)
    if temperature:
        print "Saving"
        scraperwiki.sqlite.save(unique_keys=["tweet_id"], data={"tweet_id":tweet_id, "tweet":tweet, "temperature": temperature, "date_time": date_time})           