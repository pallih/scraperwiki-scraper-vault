import scraperwiki
    
scraperwiki.sqlite.attach("test3")

print scraperwiki.sqlite.show_tables("test3")

scraperwiki.sqlite.attach("test4")