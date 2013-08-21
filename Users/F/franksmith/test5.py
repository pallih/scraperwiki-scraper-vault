# Blank Python

import scraperwiki

tempItemStartPrice = {}
temp1 = {}

scraperwiki.sqlite.attach("test4")
print scraperwiki.sqlite.show_tables("test4")


ItemNumber = "280712217861"

#tempItemStartPrice = scraperwiki.sqlite.select("auctionNumber from test4.auction where auctionNumber = ?", ItemNumber)
tempItemStartPrice = scraperwiki.sqlite.select("* from test4.auction")

print tempItemStartPrice[0]["auctionNumber"]
print tempItemStartPrice[1]["auctionNumber"]
print tempItemStartPrice[2]["auctionNumber"]
print tempItemStartPrice[200]["auctionNumber"]

print len(tempItemStartPrice)

temp1 = tempItemStartPrice[0]
print temp1

temp1["auctionStatusCode"] = "Active"
print temp1
print temp1["auctionStatusCode"]

#scraperwiki.sqlite.save(["auctionNumber"], temp1, table_name="auctionStatus")

ItemNumber = "120752111311"
tempItemStartPrice = scraperwiki.sqlite.select("* from auctionStatus where auctionNumber = ?", ItemNumber)

print tempItemStartPrice[0]["auctionNumber"]
print tempItemStartPrice[0]["auctionStatusCode"]
print tempItemStartPrice[0]


