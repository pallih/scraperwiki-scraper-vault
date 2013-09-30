# -*- coding: UTF-8 -*-
import scraperwiki
#k2k=scraperwiki.swimport('postliste-python-lib-k2000')
#utl=scraperwiki.swimport('hildenae_utils')
#parser = k2k.K2000JournalParser("https://sametime.hemne.kommune.no/k2000/k2post.nsf", "Hemne kommune",debug=True, limit=2)
#parser = k2k.K2000JournalParser("https://sametime.hemne.kommune.no/k2000/k2post.nsf", "Hemne kommune",debug=True, limit=2)
#parser = k2k.K2000JournalParser("http://mobil.iktin.no/Grong/K2000/k2post.nsf", "Grong kommune",debug=True, limit=2)

#parser.scrapeAll()

#parser = k2k.K2000JournalParser("http://lkpub01.lunner.kommune.no:8080/k2000/k2post.nsf", "Hemne kommune",debug=True, limit=2)

records = (
    "C1257181002DEE6DC1257A2F004CE484", 
    "C1257181002DEE6DC1257A40003B3D71", 
    "C1257181002DEE6DC1257A3F002C4017", # gradering + dobbel til
    "C1257181002DEE6DC1257A40003B3DB5", # dobbel Til ????
    "C1257181002DEE6DC1257A40003B3D83", # notat
    "C1257181002DEE6DC1257A3000456603", # "Svar på lnr"
    "C1257181002DEE6D'C1257A36004B98DC" # "Navn"
)
records = {}
records['a'] = "A"
records['b'] = "B"
records['c'] = "C"
#for record in records:
#    utl.pretty(parser.scrapeRecord(record))
#parser.report_errors()

data= {}
data["url"] = "http://www.gmail.com"
data["summary"] = "online email etc"
data["populaity"] = 10
data["records"] = records

scraperwiki.sqlite.save(unique_keys=["url"], data=data)           
print scraperwiki.sqlite.table_info("swdata")# -*- coding: UTF-8 -*-
import scraperwiki
#k2k=scraperwiki.swimport('postliste-python-lib-k2000')
#utl=scraperwiki.swimport('hildenae_utils')
#parser = k2k.K2000JournalParser("https://sametime.hemne.kommune.no/k2000/k2post.nsf", "Hemne kommune",debug=True, limit=2)
#parser = k2k.K2000JournalParser("https://sametime.hemne.kommune.no/k2000/k2post.nsf", "Hemne kommune",debug=True, limit=2)
#parser = k2k.K2000JournalParser("http://mobil.iktin.no/Grong/K2000/k2post.nsf", "Grong kommune",debug=True, limit=2)

#parser.scrapeAll()

#parser = k2k.K2000JournalParser("http://lkpub01.lunner.kommune.no:8080/k2000/k2post.nsf", "Hemne kommune",debug=True, limit=2)

records = (
    "C1257181002DEE6DC1257A2F004CE484", 
    "C1257181002DEE6DC1257A40003B3D71", 
    "C1257181002DEE6DC1257A3F002C4017", # gradering + dobbel til
    "C1257181002DEE6DC1257A40003B3DB5", # dobbel Til ????
    "C1257181002DEE6DC1257A40003B3D83", # notat
    "C1257181002DEE6DC1257A3000456603", # "Svar på lnr"
    "C1257181002DEE6D'C1257A36004B98DC" # "Navn"
)
records = {}
records['a'] = "A"
records['b'] = "B"
records['c'] = "C"
#for record in records:
#    utl.pretty(parser.scrapeRecord(record))
#parser.report_errors()

data= {}
data["url"] = "http://www.gmail.com"
data["summary"] = "online email etc"
data["populaity"] = 10
data["records"] = records

scraperwiki.sqlite.save(unique_keys=["url"], data=data)           
print scraperwiki.sqlite.table_info("swdata")