import scraperwiki
import lxml.html
import re
import datetime

domaine = 'http://www.americasfoodandbeverage.com/'
s_url = 'http://www.americasfoodandbeverage.com/2012exhibitor_list.cfm?xemail&xprint'

scraperwiki.sqlite.save_var("source", "americasfoodandbeverage.com")
scraperwiki.sqlite.save_var("author", "Ajay Singh Rathour")
def scrape_site(start_url, domaine):
    html_content = scraperwiki.scrape(start_url)
    p_num=1
    r_num=0
    while True:
        root = lxml.html.fromstring(html_content)
        data_list = root.cssselect('td[class="lightbg exhlist_company"]')
        
        if len(data_list)==0:
            print 'SPIDER-STOP'
            break
        for i in range(len(data_list)):
            temp_link = data_list[i].attrib.get('onclick')
           
            rel_link = temp_link.split('(')[1].split(',')[0].replace("'","")
            abs_link = domaine+rel_link
            
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
    for attempt in range(5):
        try:
            html_content = scraperwiki.scrape(comp_link)
            break
        except:
            pass
    root = lxml.html.fromstring(html_content)
    div = root.cssselect('div[id="eshowDiv"]')[0]
    data_list = div.text_content().split('\t\n')
    

    adress = data_list[10].replace('\n','').replace('\u','').replace('\t','').strip()
    if adress:
        adress= " ".join(adress.split())
        if "@" in adress:
            adress= adress.replace("@",'').strip()
            my_data.append(('address', adress))
        else:
            my_data.append(('address', adress))
    else:
        my_data.append(('address', ''))

    temp_state = data_list[10].split('   ')
    state_list = []
    for temp in temp_state:
        if temp.strip():
            state_list.append(temp.replace('\n','').replace('\u','').replace('\t','').strip())

    if (len(state_list[-1].split(' ')))==3:
            country = state_list[-1].split(' ',1)[1].strip()
            if "," in state_list[-2]:
                state = state_list[-2].split(',')[1].strip()
                city = state_list[-2].split(',')[0].strip()
                my_data.append(('state', state ))
                my_data.append(('city', city ))
            pin_code = state_list[-1].split(' ',1)[0].strip()
            if '-' in pin_code:
                temp_code = pin_code.split('-')[0].strip()
                if temp_code.isdigit():
                    zip = pin_code
                    my_data.append(('zip', zip))

    else:
        country = state_list[-1].strip()
        try:
            state = state_list[-3].split(',')[1].strip()
            city = state_list[-3].split(',')[0].strip()
            my_data.append(('state', state ))
            my_data.append(('city', city ))
        except:
            if "," in state_list[-1]:
                state = state_list[-1].split(',')[1].strip()
                city = state_list[-1].split(',')[0].strip()
                my_data.append(('state', state ))
                my_data.append(('city', city ))
        pin_code = state_list[-2].strip()
        if pin_code.isdigit():
            zip =  pin_code
            my_data.append(('zip', zip))
        else:
            zip = ''
    
    my_data.append(('companyname', data_list[1].replace('\n','').replace('\u','').replace('\t','').strip()))

    temp_desc = div.cssselect('table')[3]
    temp_desc = temp_desc.text_content().split('\t\n')   
    desc = ""
    for temp in temp_desc:
        desc = " ".join([desc,temp.replace('\n','').replace('\u','').replace('\t','').strip()])
    desc = " ".join(desc.split())
    my_data.append(('description', desc))

    try:
        web_site = div.cssselect('input[value="Website"]')[0].attrib.get('onclick')
        web_site = web_site.split('(')[1].split(',')[0].replace("'",'').strip()
        my_data.append(('website', web_site))        
    except:
        pass


    try:
        sale_m = div.cssselect('tr[id="ROW16E53E063-05FE-46C3-A47F-3CAE0FAAD401"]')[0]
        sale_m= sale_m.text_content().split('\t\n')
        main_sale = ""
        for temp in sale_m[2:]:
            if temp.strip():
                main_sale = " , ".join([main_sale,temp.strip()])
            main_sale = " ".join(main_sale.split())
            main_sale = main_sale.split(',',1)[1].strip()
            my_data.append(('salesmethod', main_sale)) 
    except:
            pass

    cat1 = div.cssselect('tr[id="ROW1756B1710-233C-47EA-BE00-832B9A1E9307"]')[0]
    temp_cat = cat1.cssselect('b[style="font-size: larger;"]')
    categ = ""
    for temp in temp_cat:
        categ = " , ".join([categ,temp.text_content().strip()])
    categ = " ".join(categ.split())
    categ = categ.split(',',1)[1].strip()

    temp_main = cat1.cssselect('a')
    main_categ = ""
    for temp in temp_main:
        main_categ= " , ".join([main_categ,temp.text_content().strip()])
    main_categ = " ".join(main_categ.split())
    main_categ= main_categ.split(',',1)[1].strip()
            
    my_data.append(('categories',categ))

    my_data.append(('maincategory',main_categ))

    my_data.append(('country', country))
        
    now = datetime.datetime.now()
    now_text = now.strftime("%Y-%m-%d")
    my_data.append(('datescraped', str(now_text)))

    my_data.append(('sourceurl',comp_link))

    try:
        contact_link = div.cssselect('input[value="Email"]')[0].attrib.get('onclick')
        contact_link = contact_link.split('(')[1].split(',')[0].replace("'",'').strip()
        link = 'http://www.americasfoodandbeverage.com/' + contact_link
        my_data.append(('contactlink', link ))        
    except:
        pass

    boothnum = div.cssselect('td[class = "bgcolor2"]')[1]
    booth = boothnum.text_content().replace('Booth','').strip()
    my_data.append(('boothnum', booth))   
    
    print my_data

    scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

scrape_site(s_url, domaine)
