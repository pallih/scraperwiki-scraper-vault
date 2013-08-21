import scraperwiki
import lxml.html
global Rank #Scoreboard rank-- to be incremented with each DB commit.
globals()["Rank"]=1
firstpage = lxml.html.fromstring(scraperwiki.scrape("http://c3l6.org/honours/combinedhonoursboard"))
headers=["Name", "City", "Country", "Age 1st July 2012", "Feb", "March", "April", "May", "June", "Total"]
#Collect data for the first page:
def collectdata(root):
    for row in root.cssselect("tr+tr+tr+tr"):#I don't know, it just werks.
        r = dict(
            zip(
                headers,
                [x.text for x in row.cssselect("td")]
            )
        )
        r["Rank"]=globals()["Rank"]
        scraperwiki.sqlite.save(unique_keys=["Rank"], data=r)
        globals()["Rank"] += 1
collectdata(firstpage)
#How many pages are there?
for n in [n for n in range(int(firstpage.cssselect("div.paging>span:nth-last-child(1)>a")[0].attrib["href"][-1])+1) if not n==1 and not n==0]:
    collectdata(lxml.html.fromstring(scraperwiki.scrape("http://c3l6.org/honours/combinedhonoursboard/page:%s"%(n))))

