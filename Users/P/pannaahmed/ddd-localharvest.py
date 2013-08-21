import re;

def remove_html(string):
    return re.sub("<.*?>", "", string)

def clean(string):
    return safestr(final_clean(strip_non_text(remove_html(string.strip()))))

def strip_non_text(string):
    return re.sub("\n|\r|&\w{3};|<.*?>",",",string)

def final_clean(string):
    return re.sub("[, ]{2,10}", ",", string)

def split_and_clean(string, delim):
    return ",".join(re.sub("[^a-zA-Z ]", "", rec, re.I) for rec in [clean(rec) for rec in string.split(delim) if rec.strip() != ""])

SAFESTR_RX = re.compile("^u\'(.+)\'$")
def safestr(string):
    try:
        return english_string(string).encode('utf-8', 'replace')
    except:
        return re.sub(SAFESTR_RX, '\1', repr(string))

import scraperwiki

import lxml.html
import re
domaine = 'http://www.localharvest.org'
s_url = 'http://www.localharvest.org/store'

scraperwiki.sqlite.save_var("source", "localharvest.org")
scraperwiki.sqlite.save_var("author", "Panna Ahmed")

def scrape_site(start_url, domaine):
    print start_url
    html_content = scraperwiki.scrape(domaine, None, 'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20100101 Firefox/15.0.1')
    p_num=1
    r_num=0
    #while True:
    root = lxml.html.fromstring(html_content)
    print root
    #data_list = root.cssselect('div[id="col1_content"] div')

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
    div = root.cssselect('div[id="col1_content"] ')[0]
    data_list = div.text_content().split('\r\n')
    print data_list
    adress = data_list[4]+data_list[5]+data_list[6]
    my_data.append(('companyname', data_list[3]))
    my_data.append(('address', adress))
    for data in data_list[6:]:
        if re.search('Phone:',data):
            #print data
            contacts = data.split(':')
            try:
                my_data.append(('country', contacts[0][:-5]))
                my_data.append(('phonenumber', contacts[1][:-3]))
                my_data.append(('faxnumber', contacts[2][:-7]))
                if contacts[3].split()[0] != 'Products':
                    if '@' in contacts[3].split()[0]:
                        my_data.append(('emails', contacts[3].split()[1][:-8]))
                    else:
                        my_data.append(('contact1first', contacts[3].split()[0]))
                        my_data.append(('contact1last', contacts[3].split()[1][:-8]))
            except:
                pass
    m_cats=''
    m_categories = div.cssselect('li span.toplevelcategory')
    for m_cat in m_categories:
        m_cats=m_cats+', '+m_cat.text
    my_data.append(('maincategory', m_cats[2:]))
    categories = div.cssselect('li span')
    
    cats=''
    for cat in categories:
        cats=cats+', '+cat.text
    print cats
    my_data.append(('categories', cats[2:]))
    print my_data
    scraperwiki.sqlite.save(unique_keys=['companyname'], data=dict(my_data))

scrape_site(s_url, domaine)

