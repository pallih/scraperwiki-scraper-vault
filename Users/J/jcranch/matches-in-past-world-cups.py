"""
All FIFA World Cup match scores, 1930--2006
"""


from scraperwiki import datastore
from html5lib import HTMLParser, treebuilders, sanitizer
from lxml import etree
import urllib2
import datetime



def main():
    world_cups = [(2006,"http://www.fifa.com/worldcup/archive/germany2006/results/index.html"),
                  (2002,"http://www.fifa.com/worldcup/archive/edition=4395/results/index.html"),
                  (1998,"http://www.fifa.com/worldcup/archive/edition=1013/results/index.html"),
                  (1994,"http://www.fifa.com/worldcup/archive/edition=84/results/index.html"),
                  (1990,"http://www.fifa.com/worldcup/archive/edition=76/results/index.html"),
                  (1986,"http://www.fifa.com/worldcup/archive/edition=68/results/index.html"),
                  (1982,"http://www.fifa.com/worldcup/archive/edition=59/results/index.html"),
                  (1978,"http://www.fifa.com/worldcup/archive/edition=50/results/index.html"),
                  (1974,"http://www.fifa.com/worldcup/archive/edition=39/results/index.html"),
                  (1970,"http://www.fifa.com/worldcup/archive/edition=32/results/index.html"),
                  (1966,"http://www.fifa.com/worldcup/archive/edition=26/results/index.html"),
                  (1962,"http://www.fifa.com/worldcup/archive/edition=21/results/index.html"),
                  (1958,"http://www.fifa.com/worldcup/archive/edition=15/results/index.html"),
                  (1954,"http://www.fifa.com/worldcup/archive/edition=9/results/index.html"),
                  (1950,"http://www.fifa.com/worldcup/archive/edition=7/results/index.html"),
                  (1938,"http://www.fifa.com/worldcup/archive/edition=5/results/index.html"),
                  (1934,"http://www.fifa.com/worldcup/archive/edition=3/results/index.html"),
                  (1930,"http://www.fifa.com/worldcup/archive/edition=1/results/index.html")]
    for (y,url) in world_cups:
        do_year(y,url)


def do_year(y,url):
    pagetext = urllib2.urlopen(url)
    parser = HTMLParser(tree=treebuilders.getTreeBuilder("lxml"), tokenizer=sanitizer.HTMLSanitizer)
    page = parser.parse(pagetext)

    for section in page.findall("body/div/div/div/div/div/div/div/div/table[@class='fixture']"):

        matchtype = section.find("caption").text

        for match in section.findall("tbody/tr"):

            l = list(match.getchildren())
            d = {}
            d["Match type"] = matchtype
            d["Match number"] = l[0].text
            d["Date"] = make_date(l[1].text, y)
            d["Team 1"] = flatten_refs(l[3])
            d["Team 2"] = flatten_refs(l[5])
            a = l[4].find("a")
            d["Score"] = a.text
            d["Report"] = "http://www.fifa.com" + a.get("href")
            print "%d (%s) %s - %s"%(y,d["Match type"],d["Team 1"],d["Team 2"])
            datastore.save(unique_keys = ["Date","Team 1","Team 2"], data=d)

            
def make_date(rdm, y):
    (rd, rm) = rdm.split(" ")
    m = 1 + ["January","February","March","April","May","June","July","August","September","October","November","December"].index(rm)
    return datetime.date(y,m,int(rd))


def flatten_refs(t):
    return (t.text or "") + "".join((a.text or "") for a in t.findall("a"))


main()
