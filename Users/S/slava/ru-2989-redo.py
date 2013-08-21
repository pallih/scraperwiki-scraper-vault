import scraperwiki
import lxml.html
import re

# Blank Python

# return text content of a given xpath on a parent node
def get_xpath_el(parent, xpath, default='text',index=0):
    el=parent.xpath(xpath)
    if el!=[]:
        if default=='text' or default=='':
            return el[index].text_content()
        else:
            return el[index].attrib[default]
    else:
        return ''
scraperwiki.sqlite.execute('delete from data')
html=scraperwiki.scrape("http://www.fundservice.ru/o_banke/filialy_i_dopolnitelnye_ofisy")
root=lxml.html.document_fromstring(html)
i=1
for r in root.xpath("//div[@class='main_submenu']/div[@class='submenu_over'][position()>8 and position()<=16]/div[@class='left_submenu']/a"):
    region_url=r.attrib['href']
    region_name=r.text_content()

    html=scraperwiki.scrape("http://www.fundservice.ru"+region_url)
    root=lxml.html.document_fromstring(html)
    data=[]
    for b in root.xpath("//table[@class='offices']/tr/td[1]"):
        branch_name1 = get_xpath_el(b,"div")
        branch_url = get_xpath_el(b,"div/a","href")
        address1 = get_xpath_el(b, "b")
        ll={'lat':'','lon':''}
        branch_name2 = ''
        address2 =''
        
        if branch_url != '':
            branch_html=scraperwiki.scrape("http://www.fundservice.ru" + branch_url )
            root1=lxml.html.document_fromstring(branch_html)
            branch_name2 = get_xpath_el(root1,"//div[@class='inner_block']/*[@class='head1']")
            address2 = get_xpath_el(root1,"//*[@id='center_part']/div/table/tr[2]/td[1]/div[1]")
            latlon=re.findall(r"new YMaps\.Placemark\(new YMaps\.GeoPoint\(([\d\.]+?),([\d\.]+?)\)", branch_html, re.I|re.U)
    
            if latlon!=[]:
                ll['lat']=latlon[0][1]
                ll['lon']=latlon[0][0]

        data.append({'id':i,'region':region_name, 'branch_name1':branch_name1, 'branch_url':branch_url, 'address1':address1,'branch_name2':branch_name2, 'address2': address2, 'lat':ll['lat'], 'lon':ll['lon']})
        i+=1

    if data!=[]:
        scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name='data') 
    