import itertools
import scraperwiki
import lxml.html
import dateutil.parser

html_str = scraperwiki.scrape("http://www.gaithersburgmd.gov/poi/default.asp?POI_ID=1283&TOC=107;85;1283")
html_tree = lxml.html.fromstring(html_str)

texts = html_tree.xpath(".//text()")

keywords = ("avenue", "ave", "drive", "dr", "road", "rd", "street", "st", "court", "ct", "way", "lane", "ln", "terrace", "tr")

def strip_trailing_punct(s):
    return "".join(itertools.takewhile(lambda y: y.isalnum(), s))

i = 0
for text in texts:
    low = text.lower()
    start = low.find("block of")
    if start > -1:
        # put everything after "block of" in tail, split by space
        tail = low[start + len("block of"):].split()

        # put in words everything before the first keyword we encounter
        words = list(itertools.takewhile(lambda x: strip_trailing_punct(x) not in keywords, tail))

        # len(words) == len(tail) is possible... otherwise if the word after the last one in words
        # is a keyword, add it to words
        if len(words) < len(tail) and strip_trailing_punct(tail[len(words)]) in keywords:
            words.append(strip_trailing_punct(tail[len(words)]))
        
        record = {
            'id': i,
            'address': " ".join(words)
        }
        scraperwiki.sqlite.save(unique_keys=["id"], data=record)
        i += 1
import itertools
import scraperwiki
import lxml.html
import dateutil.parser

html_str = scraperwiki.scrape("http://www.gaithersburgmd.gov/poi/default.asp?POI_ID=1283&TOC=107;85;1283")
html_tree = lxml.html.fromstring(html_str)

texts = html_tree.xpath(".//text()")

keywords = ("avenue", "ave", "drive", "dr", "road", "rd", "street", "st", "court", "ct", "way", "lane", "ln", "terrace", "tr")

def strip_trailing_punct(s):
    return "".join(itertools.takewhile(lambda y: y.isalnum(), s))

i = 0
for text in texts:
    low = text.lower()
    start = low.find("block of")
    if start > -1:
        # put everything after "block of" in tail, split by space
        tail = low[start + len("block of"):].split()

        # put in words everything before the first keyword we encounter
        words = list(itertools.takewhile(lambda x: strip_trailing_punct(x) not in keywords, tail))

        # len(words) == len(tail) is possible... otherwise if the word after the last one in words
        # is a keyword, add it to words
        if len(words) < len(tail) and strip_trailing_punct(tail[len(words)]) in keywords:
            words.append(strip_trailing_punct(tail[len(words)]))
        
        record = {
            'id': i,
            'address': " ".join(words)
        }
        scraperwiki.sqlite.save(unique_keys=["id"], data=record)
        i += 1
