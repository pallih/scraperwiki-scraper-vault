import scraperwiki,lxml.html

# Blank Python

url = 'http://www.rbwm.gov.uk/pam/view.jsp?ID=12%2F01432%2FAGDET'

html= scraperwiki.scrape(url)
root=lxml.html.fromstring(html)
plan5=root.cssselect("table[summary='Planning Application Details'] tr")[5]
print lxml.html.tostring(plan5)
for td in plan5:
    print lxml.html.tostring(td)

#doc.search('table[@summary="Planning Application Details"] tr')[5].search('td')[1].to_s
import scraperwiki,lxml.html

# Blank Python

url = 'http://www.rbwm.gov.uk/pam/view.jsp?ID=12%2F01432%2FAGDET'

html= scraperwiki.scrape(url)
root=lxml.html.fromstring(html)
plan5=root.cssselect("table[summary='Planning Application Details'] tr")[5]
print lxml.html.tostring(plan5)
for td in plan5:
    print lxml.html.tostring(td)

#doc.search('table[@summary="Planning Application Details"] tr')[5].search('td')[1].to_s
