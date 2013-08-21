import scraperwiki
import urllib2, lxml.etree

def gettext_with_bi_tags(el):
    res = [ ]
    if el.text:
        res.append(el.text)
    for lel in el:
        res.append("<%s>" % lel.tag)
        res.append(gettext_with_bi_tags(lel))
        res.append("</%s>" % lel.tag)
        if el.tail:
            res.append(el.tail)
    return "".join(res).strip()

for year in range (2006, 2013):
    for week in range (1, 85):
        week_str = str(week)

        if (week<10):
            week_str = "0" + week_str

        year_str = str(year)

        url='http://www.joradp.dz/FTP/jo-francais/'+ year_str +'/F'+ year_str +'0'+ week_str +'.pdf'
        
        try:
            pdfdata = urllib2.urlopen(url).read()
        
            xmldata = scraperwiki.pdftoxml(pdfdata)
            
            root = lxml.etree.fromstring(xmldata)
            pages = list(root)
            
            data={}
            text = ""
            for page in pages:
                for el in page:
                    if el.tag == "text":
                        if el.attrib['top']=='1220': pass
                        else:
                            text += " " + gettext_with_bi_tags(el)
            data["text"] = text
            data["date"] = year_str + "-" + week_str
            scraperwiki.sqlite.save(unique_keys=['date'], data=data)

        except:
            pass
