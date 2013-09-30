import scraperwiki
import lxml.html
import re, cgi, os, csv, sys, json
import string
import stdnum.isbn


qdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
url = qdict.get("url", 'http://www.wellcome.ac.uk/stellent/groups/corporatesite/@msh_peda/documents/web_document/wtd003419.pdf')

try:
    sdata = scraperwiki.sqlite.select("url, pages, isbns, final_isbn from swdata where url=? limit 1", (url,))
except scraperwiki.sqlite.SqliteError:
    sdata = [ ]

if sdata:
    data = sdata[0]
    data = { "url":sdata[0]["url"], "pages":sdata[0]["pages"], 
             "isbns":json.loads(sdata[0]["isbns"]), "final_isbn":sdata[0]["final_isbn"] }

else:
    lazycache=scraperwiki.swimport('lazycache')
    pdfdata=lazycache.lazycache(url)
    xmldata = scraperwiki.pdftoxml(pdfdata)
    root=lxml.html.fromstring(xmldata)
    pages = list(root)
    isbns = [ ]
    fisbn = ""
    for i, page in enumerate(pages):
        pagetext = " ".join(t.text_content()  for t in page)
        for isbn_org, isbn in re.findall("(ISBN[\s:]*([\d\s\-]+))(?i)", pagetext):
            isbn = re.sub("[^\d]", "", isbn)
            if not stdnum.isbn.is_valid(isbn):
                isbn = ""
            else:
                fisbn = isbn
            isbns.append({"isbn_org":isbn_org, "isbn":isbn})
    
    data = { "url":url, "pages":len(pages), "isbns":isbns, "final_isbn":fisbn }
    scraperwiki.sqlite.save(["url"], {"url":data["url"], "pages":data["pages"], 
                            "isbns":json.dumps(data["isbns"]), "final_isbn":data["final_isbn"]})


jdata = json.dumps(data)
if qdict.get("callback"):
    jdata = "%s(%s)" % (qdict.get("callback"), jdata)

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print jdata
import scraperwiki
import lxml.html
import re, cgi, os, csv, sys, json
import string
import stdnum.isbn


qdict = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
url = qdict.get("url", 'http://www.wellcome.ac.uk/stellent/groups/corporatesite/@msh_peda/documents/web_document/wtd003419.pdf')

try:
    sdata = scraperwiki.sqlite.select("url, pages, isbns, final_isbn from swdata where url=? limit 1", (url,))
except scraperwiki.sqlite.SqliteError:
    sdata = [ ]

if sdata:
    data = sdata[0]
    data = { "url":sdata[0]["url"], "pages":sdata[0]["pages"], 
             "isbns":json.loads(sdata[0]["isbns"]), "final_isbn":sdata[0]["final_isbn"] }

else:
    lazycache=scraperwiki.swimport('lazycache')
    pdfdata=lazycache.lazycache(url)
    xmldata = scraperwiki.pdftoxml(pdfdata)
    root=lxml.html.fromstring(xmldata)
    pages = list(root)
    isbns = [ ]
    fisbn = ""
    for i, page in enumerate(pages):
        pagetext = " ".join(t.text_content()  for t in page)
        for isbn_org, isbn in re.findall("(ISBN[\s:]*([\d\s\-]+))(?i)", pagetext):
            isbn = re.sub("[^\d]", "", isbn)
            if not stdnum.isbn.is_valid(isbn):
                isbn = ""
            else:
                fisbn = isbn
            isbns.append({"isbn_org":isbn_org, "isbn":isbn})
    
    data = { "url":url, "pages":len(pages), "isbns":isbns, "final_isbn":fisbn }
    scraperwiki.sqlite.save(["url"], {"url":data["url"], "pages":data["pages"], 
                            "isbns":json.dumps(data["isbns"]), "final_isbn":data["final_isbn"]})


jdata = json.dumps(data)
if qdict.get("callback"):
    jdata = "%s(%s)" % (qdict.get("callback"), jdata)

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print jdata
