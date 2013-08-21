import scraperwiki
import lxml.html
import re
import datetime
import urllib2
import sys

domaine = 'http://www.theorganicpages.com/topo/'
scraperwiki.sqlite.save_var("source", "theorganicpages.com")
scraperwiki.sqlite.save_var("author", "Ajay Singh Rathour")
    
def scrape_site(start_url, domaine):
    html_content = scraperwiki.scrape(start_url)
    p_num=1
    r_num=0
    while True:
        print html_content
        root = lxml.html.fromstring(html_content)
        data_list = root.cssselect('a[class="linksbig"]')
        if len(data_list)==0:
            print 'SPIDER-STOP'
            break
        else:
            for i in range(len(data_list)):
                temp_link = data_list[i].attrib.get('href')
                t_link = 'http://www.theorganicpages.com/topo/'+temp_link
                try:
                    inner_html_content = scraperwiki.scrape(t_link)
                except:
                    continue
                inner_root = lxml.html.fromstring(inner_html_content)
                inner_data_list = inner_root.cssselect('a[class="links"]')
                if len(inner_data_list)==0:
                    break
                else:
                    for i in range(len(inner_data_list)):
                        rel_link = inner_data_list[i].attrib.get('href')
                        abs_link = domaine+rel_link
                        abs_link = abs_link.replace("'s ","%27s%20").strip()
                        abs_link = abs_link.replace(" ","%20").strip()
                        scrape_info(abs_link, r_num)
                        r_num+=1

        for attempt in range(5):
            try:
                html_content = scraperwiki.scrape(s_url+'?Page='+str(p_num+1))
                p_num+=1
                break
            except:
                pass

def scrape_info(comp_link, num):
    my_data = []
    my_data.append(('id', num))
    my_data.append(('sourceurl', comp_link))
    html_content = None
    for attempt in range(5):
        try:
            html_content = scraperwiki.scrape(comp_link)
            break
        except:
            pass
            break
    if not html_content:
        return None
    root = lxml.html.fromstring(html_content,comp_link)
    root.make_links_absolute()
    div = root.xpath('//td[@class="body"]')
    
    div = lxml.html.fromstring(html_content)
    comp_name = div.xpath('//span[@class="subtitles"]/text()')
    if comp_name:
        comp_name = comp_name[0].replace('\r','').replace('\n','').replace('\t','').strip()
        my_data.append(('companyname', comp_name))    

    temp_add = div.xpath("//tr[td[span[contains(text(),'Address:')]]]//text()|//tr[td[span[contains(text(),'Address:')]]]/following::tr[1]//text()") 
    if temp_add:
        add = ""
        for temp in temp_add:
            add = " ".join([add,temp.strip()])
        add = " ".join(add.split())
        
        temp_add1 = div.xpath("//tr[td[span[contains(text(),'Address:')]]]//text()") 
        add1 = ""
        for temp in temp_add1:
            add1 = " ".join([add1,temp.strip()])
        add1 = " ".join(add1.split())
        add1 = add1.split(":")[1].strip()
            
        add = add.split(':')[1].strip()
        my_data.append(('address', add1))
        my_data.append(('address2', add1))
    
        count = add.split(' ')[-1].strip()
        my_data.append(('country', count))
        
        state = add.split(',')[-2].strip()
        my_data.append(('state', state))
        
        temp_data = add.split(',')[-1].strip().split(' ')[0]
        if "-" in temp_data:
            p_code = temp_data.split('-')[0].strip()
            if p_code.isdigit():
                p_code = temp_data.strip()
                my_data.append(('zip', p_code))
        else:
            p_code = temp_data
            if p_code.isdigit():
                p_code = temp_data.strip()
                my_data.append(('zip', p_code))

    certifications = div.xpath("//td[span[contains(text(),'Certifier:')]]/following::td[1]/text()")
    if certifications:
        my_data.append(('certifications', certifications[0].strip()))

    dba = div.xpath("//td[span[contains(text(),'DBA:')]]/following::td[1]/text()")
    if dba:
        dba = " ".join(dba)
        dba = " ".join(dba.split())
        my_data.append(('dba', dba.strip()))


    contact1first = div.xpath("//td[span[contains(text(),'Contact:')]]/following::td[1]//text()")
    if contact1first:
        my_data.append(('contact1first', contact1first[0].strip()))
    
    contact1title = div.xpath("//td[span[contains(text(),'Contact:')]]/following::td[1]//text()")
    if contact1title:
        if "," in contact1title[-1].strip():
            contact1title = contact1title[-1].replace(',','').strip()
            my_data.append(('contact1title', contact1title))
        else:
            my_data.append(('contact1title', contact1title[-1].strip()))
    
    l_name = div.xpath("//td[span[contains(text(),'Contact:')]]/following::td[1]//text()")
    if l_name:
        l_name.pop(0)
        l_name.pop(-1)
        contact1last = "".join(l_name)
        my_data.append(('contact1last', contact1last))

    email = div.xpath("//td[span[contains(text(),'e-mail:')]]/following::td[1]/a/text()")
    if email:
        email = " , ".join(email)
        my_data.append(('email', email))

    phonenumber = div.xpath("//td[span[contains(text(),'Phone:')]]/following::td[1]/text()")
    if phonenumber:
        my_data.append(('phonenumber', phonenumber[0].strip() ))

    faxnumber = div.xpath("//td[span[contains(text(),'Fax:')]]/following::td[1]/text()")
    if faxnumber:
        my_data.append(('faxnumber', faxnumber[0].strip()))

    website = div.xpath("//td[span[contains(text(),'site:')]]/following::td[1]/a/text()")
    if website:
        my_data.append(('website', website[0].strip()))

    yearfounded = div.xpath("//td[span[contains(text(),'Founded:')]]/following::td[1]/text()")
    if yearfounded:
        yearfounded = yearfounded[0].strip()
        my_data.append(('yearfounded', yearfounded))

    description = div.xpath("//td[span[contains(text(),'Description:')]]/following::td[1]/text()")
    if description:
        description = " ".join(description[0].split())
        my_data.append(('description', description))

    categories = div.xpath("//tr[td[contains(text(),'Services:')]]//td[2]//text()")
    if categories:
        cat = ""
        for data in categories:
            cat = " ".join([cat,data.strip()])
        cat = " ".join(cat.split( )).replace('\n',' ').replace('\r',' ').replace('\t',' ').strip()
        my_data.append(('categories', cat ))

    main_cat = div.xpath("//span[@class = 'index']//a/text()")
    if main_cat:
        temp_cat = []
        for temp in main_cat:
            temp_cat.append(temp.strip())
        category = " > ".join(temp_cat)
        my_data.append(('maincategory', category))
               
    now = datetime.datetime.now()
    now_text = now.strftime("%Y-%m-%d")
    my_data.append(('datescraped', str(now_text)))

    print "in round:" + str(curr_idx) + "saving:" + dict(my_data).get('companyname', "No companyname")

    scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

url_list=['certificationservices','brokerservices','childrensproducts','consultingservices','farmingsupplies','farmgrownproducts','fibertextiles','foodservice','distribution',
                'ingredients','internationaltrade','manufacturing','mailorder','packaging','personalcareproducts','petcareproducts','privatelabel','retailstores','supportservices']

last_scraped = scraperwiki.sqlite.get_var('last_scraped')
if last_scraped == len(url_list):
    print "DONE"
    sys.exit()

for i, name in enumerate(url_list[last_scraped:]):
    curr_idx = i + last_scraped
    print str(curr_idx) + " of " + str(len(url_list))+str(name)
    scraperwiki.sqlite.save_var('last_scraped', curr_idx)
    s_url = 'http://www.theorganicpages.com/topo/commercialactivity.html?ca=s'+name
    scrape_site(s_url, domaine)

