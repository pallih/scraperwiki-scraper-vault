# Blank Python

print "Starting the run"
import scraperwiki
html = scraperwiki.scrape("http://www.education.gov.uk/edubase/establishment/summary.xhtml?urn=100000")
print html


##def ctext(el):           
##    result = [ ]
##    if el.text:
##        result.append(el.text)
##    for sel in el:
##        assert sel.tag in ["b", "i"]
##        result.append("<"+sel.tag+">")
##        result.append(ctext(sel))
##        result.append("</"+sel.tag+">")
##        if sel.tail:
##            result.append(sel.tail)
##    return "".join(result)# Blank Python

print "Starting the run"
import scraperwiki
html = scraperwiki.scrape("http://www.education.gov.uk/edubase/establishment/summary.xhtml?urn=100000")
print html


##def ctext(el):           
##    result = [ ]
##    if el.text:
##        result.append(el.text)
##    for sel in el:
##        assert sel.tag in ["b", "i"]
##        result.append("<"+sel.tag+">")
##        result.append(ctext(sel))
##        result.append("</"+sel.tag+">")
##        if sel.tail:
##            result.append(sel.tail)
##    return "".join(result)