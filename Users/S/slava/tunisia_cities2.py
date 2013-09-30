import scraperwiki
import lxml.html

# Blank Python
user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"

scraperwiki.sqlite.execute("delete from data")
html=scraperwiki.scrape("http://www.ins.nat.tn/fr/rgph2.1_gouv_derolant.php?Code_indicateur=0301007", None, user_agent )
#html=html.replace("<html ", '<html xmlns="http://www.w3.org/1999/xhtml" ')
#html=html.replace('<meta charset="UTF-8" />', '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
root=lxml.html.document_fromstring(html)

def get_towns(code):
    result = []
    if code== "" or code == None: 
        result.append({'town': '', 'district': ''})
        return 

    try:
        html=scraperwiki.scrape("http://www.ins.nat.tn/fr/rgph2.1.commune.php?code_modalite="+code+"&Code_indicateur=0301007&Submit3=Envoyer", None, user_agent)

    except:
        result.append({'town': '', 'district': ''})
        return result
        pass

    root=lxml.html.document_fromstring(html)

    cities = root.xpath("//div[@id='divmain']/table/tr[3]/td/table/tr/td/table[2]/tr/td[1]/div/table/tr/td")

    if cities != []:
        for c in cities:
            if c.xpath('em') == []:
                town = c.text_content()
                district = ''
            else:
                district = c.text_content()

            result.append({'town': town.strip(), 'district': district.strip() })
    else:
        result.append({'town': '', 'district': ''})
        

    return result
    

lst = root.xpath("//select[@id='code_modalite']/option")
i=1
#print lst
for l in lst:
    print l.text_content()
    try:
        a = l.attrib['value']
        if l.attrib['value'] == '': continue
    except:
        continue
        
    print l.attrib['value']
    deleg = l.text_content()
    deleg_code = l.attrib['value']

    towns = get_towns(deleg_code)

    for t in towns:
        data={ 'id': i, \
            'guvernorate': deleg, \
            'guvernorate_code': deleg_code, \
            'town': t['town'], \
            'district': t['district'] }
    
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='data')
        i+=1
                
                


import scraperwiki
import lxml.html

# Blank Python
user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"

scraperwiki.sqlite.execute("delete from data")
html=scraperwiki.scrape("http://www.ins.nat.tn/fr/rgph2.1_gouv_derolant.php?Code_indicateur=0301007", None, user_agent )
#html=html.replace("<html ", '<html xmlns="http://www.w3.org/1999/xhtml" ')
#html=html.replace('<meta charset="UTF-8" />', '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />')
root=lxml.html.document_fromstring(html)

def get_towns(code):
    result = []
    if code== "" or code == None: 
        result.append({'town': '', 'district': ''})
        return 

    try:
        html=scraperwiki.scrape("http://www.ins.nat.tn/fr/rgph2.1.commune.php?code_modalite="+code+"&Code_indicateur=0301007&Submit3=Envoyer", None, user_agent)

    except:
        result.append({'town': '', 'district': ''})
        return result
        pass

    root=lxml.html.document_fromstring(html)

    cities = root.xpath("//div[@id='divmain']/table/tr[3]/td/table/tr/td/table[2]/tr/td[1]/div/table/tr/td")

    if cities != []:
        for c in cities:
            if c.xpath('em') == []:
                town = c.text_content()
                district = ''
            else:
                district = c.text_content()

            result.append({'town': town.strip(), 'district': district.strip() })
    else:
        result.append({'town': '', 'district': ''})
        

    return result
    

lst = root.xpath("//select[@id='code_modalite']/option")
i=1
#print lst
for l in lst:
    print l.text_content()
    try:
        a = l.attrib['value']
        if l.attrib['value'] == '': continue
    except:
        continue
        
    print l.attrib['value']
    deleg = l.text_content()
    deleg_code = l.attrib['value']

    towns = get_towns(deleg_code)

    for t in towns:
        data={ 'id': i, \
            'guvernorate': deleg, \
            'guvernorate_code': deleg_code, \
            'town': t['town'], \
            'district': t['district'] }
    
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='data')
        i+=1
                
                


