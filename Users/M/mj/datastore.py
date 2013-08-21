import scraperwiki

# Blank Python


#scraperwiki.sqlite.attach("PL2012")
 
#print scraperwiki.sqlite.table_info("gazeta.swdata")

scraperwiki.sqlite.attach("pl2012")
scraperwiki.sqlite.attach("gazetawaweuro2")
news = scraperwiki.sqlite.select("* from pl2012.swdata order by iDate desc limit 30")
scraperwiki.sqlite.save(['iDate', 'title', 'datePub', 'content'], news)

news1 = scraperwiki.sqlite.select("* from gazetawaweuro2.swdata order by iDate desc limit 30")
scraperwiki.sqlite.save(['iDate', 'title', 'datePub', 'content'], news1)



print news
print news1