import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

html = scraperwiki.scrape("http://www.nomos.ru/branches/offices/moscow/")
root = lxml.html.document_fromstring(html)
options = root.xpath("//select[@name='change_city']/option")
#scraperwiki.sqlite.execute("delete from branch")
i=71
go=0
for option in options:
    if option.text_content().encode('utf-8') == 'Омск':
        go=1
        continue

    if go==0:continue

    if option.attrib['value']!= '' and option.attrib['value']!= '0':
        html = scraperwiki.scrape("http://www.nomos.ru/branches/offices/" + option.attrib['value'])
        coords = re.findall(r'var coords = {(.+?)}', html, re.I|re.U|re.S|re.M)
        #print coords

        if coords !=[]:
            coords = coords[0].replace(', , ,', ',0,0,')
            branches = eval('{' + coords + '}')
            #print branches
            for branch_id in branches:
                b=branches[branch_id]
                scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':b[3], 'address': b[4], 'lat':b[1], 'lng':b[2], 'city': option.text_content()}, table_name='branch')
                i+=1
        #exit()

        
import scraperwiki
import lxml.html
import simplejson
import re
# Blank Python

html = scraperwiki.scrape("http://www.nomos.ru/branches/offices/moscow/")
root = lxml.html.document_fromstring(html)
options = root.xpath("//select[@name='change_city']/option")
#scraperwiki.sqlite.execute("delete from branch")
i=71
go=0
for option in options:
    if option.text_content().encode('utf-8') == 'Омск':
        go=1
        continue

    if go==0:continue

    if option.attrib['value']!= '' and option.attrib['value']!= '0':
        html = scraperwiki.scrape("http://www.nomos.ru/branches/offices/" + option.attrib['value'])
        coords = re.findall(r'var coords = {(.+?)}', html, re.I|re.U|re.S|re.M)
        #print coords

        if coords !=[]:
            coords = coords[0].replace(', , ,', ',0,0,')
            branches = eval('{' + coords + '}')
            #print branches
            for branch_id in branches:
                b=branches[branch_id]
                scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, 'name':b[3], 'address': b[4], 'lat':b[1], 'lng':b[2], 'city': option.text_content()}, table_name='branch')
                i+=1
        #exit()

        
