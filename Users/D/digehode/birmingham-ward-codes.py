import scraperwiki
from BeautifulSoup import BeautifulSoup
data=scraperwiki.scrape("http://posterous.com/getfile/files.posterous.com/james-nsqsp/zxGkmSD6eV465OY6UyIrBisQwJ1WrsoJ2uoTblOwUlv03RdHbLp9t7BkaGBf/code_to_name.csv")

for l in data.split("\n"):
    parts=l.split(",")
    if len(parts)!=2: continue
    parta=parts[0][1:-1]
    partb=parts[1][1:-1].upper()
    data={"ONS":parta, "ward":partb}
    scraperwiki.datastore.save(["ONS"], data) 
