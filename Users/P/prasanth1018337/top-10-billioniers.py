import urllib
import csv

# fill in the input file here
url = "http://en.wikipedia.org/wiki/Forbes_list_of_billionaires_(2009)"

fin = urllib.urlopen(url)
lines = fin.readlines()
for line in lines:
    print line

def dataset():
    import scraperwiki
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"1","name":"bill gates","networth":"$40.0 billion", "age":"53","citizenship":"united states","residence":"united states","sources wealth":"microsoft"})
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"2","name":"warren buffet","networth":"$37.0 billion", "age":"78","citizenship":"united states","residence":"united states","sources wealth":"berkshire hathaway"})
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"3","name":"carlos slim helu","networth":"$35.0 billion", "age":"69","citizenship":"mexico","residence":"mexico","sources wealth":"telmex, america movil"})
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"4","name":"lawrence ellison","networth":"$22.5 billion", "age":"64","citizenship":"united states","residence":"united states","sources wealth":"oracle corporation"})
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"5","name":"ingvar kamprad and family","networth":"$22.0 billion", "age":"83","citizenship":"sweden","residence":"switzerland","sources wealth":"ikea"})
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"6","name":"karl albrecht","networth":"$21.5 billion", "age":"89","citizenship":"germany","residence":"germany","sources wealth":"aldi sud"})
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"7","name":"mukesh ambani","networth":"$19.5 billion", "age":"51","citizenship":"india","residence":"india","sources wealth":"reliance industries"})
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"8","name":"lakshmi mittal","networth":"$19.3 billion", "age":"58","citizenship":"india","residence":"united kingdom","sources wealth":"arcelor mittal"})
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"9","name":"theo albrecht","networth":"$18.8 billion", "age":"87","citizenship":"germany","residence":"germany","sources wealth":"aldi nord,trader joes"})
    scraperwiki.datastore.save(unique_keys=["number"], data={"number":"10","name":"amancio ortega","networth":"$18.3 billion", "age":"73","citizenship":"spain","residence":"spain","sources wealth":"inditex group"})

dataset()



