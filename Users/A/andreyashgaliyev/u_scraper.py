# -*- encoding: utf-8 -*-
import scraperwiki

#category name> /html/body/div/div[2]/div/div/center/h1/text()
#hrefs on category page> /html/body/div/div[2]/div/div/div[num or none]/div[2]/a
#title of message> /html/body/div/div[2]/div/div/div[2]/h1/text()
#description> /html/body/div/div[2]/div/div/index/text()
#price> /html/body/div/div[2]/div/div/span/text()
#phones> /html/body/div/div[2]/div/div/text()
#images> /html/body/div/div[2]/div/div/div[6]/a/img
#date> /html/body/div/div[2]/div/div/div[3]/text()

import lxml.html, urllib, string, datetime
from lxml import etree


base_url = "http://doska.uralsk.info/"

total_deleted = 0
total_new = 0


categories_lst = [("http://doska.uralsk.info/c188.html", "FLAT1")]
""",
                   ("http://doska.uralsk.info/c189.html", "FLAT2"),
                   ("http://doska.uralsk.info/c190.html", "FLAT3"),
                   ("http://doska.uralsk.info/c191.html", "FLAT45"),
                   ("http://doska.uralsk.info/c98.html", "GARAGE"),
                   ("http://doska.uralsk.info/c94.html", "HOUSE"),
                   ("http://doska.uralsk.info/c95.html", "FLATS"),
                   ("http://doska.uralsk.info/c99.html", "COMMERCIAL"),
                   ("http://doska.uralsk.info/c96.html", "ROOMS"),
                   ("http://doska.uralsk.info/c97.html", "COUNTRY"),
                   ("http://doska.uralsk.info/c113-ts.html","COMP"),
                   ("http://doska.uralsk.info/c92.html","JOB"),
                   ("http://doska.uralsk.info/c254.html","AUTOSERVICE"),
                   ("http://doska.uralsk.info/c185.html","COMPSERVICE"),
                   ("http://doska.uralsk.info/c181.html","STROISERVICE")] """


def start_parsing(limit):
    res = []
    for cat in categories_lst:
        res = res + parse_category(cat[0],cat[1],limit)
    print "Total deleted {0}".format(total_deleted)
    print "New total {0}".format(total_new)
    print "Saving results to DB."
    save_results(res)
    print "Done."
    print "Exit."


def load_page(url):
    for at in range(5):
        try:
            str_page = scraperwiki.scrape(url)
            return str_page
        except:
            print " -> Reload url {0}".format(url)
            pass
    raise Exception("Failed to load url {0}".format(url))

#Вводится ссылка на категорию, вытаскиваются все объявления из неё.
def parse_category(category_url,category_name,limit):
    print "Parsing category '{0}'".format(category_name)
    print "Getting full href list"
    
    desc_urls = get_full_href_list(get_pages_urls(category_url))
    
    if len(desc_urls)==0:
        print "No hrefs loaded."
        return []

    print "Urls count: {0}".format(len(desc_urls))
    print "Done."
    print "Cleaning urls."
    c_urls = clean_urls(desc_urls,category_name)
    print "Done."
    print "Getting info from urls."
    mdata = get_info_list(c_urls,limit)
    print "Done."
    print "Adding category name: '{0}'".format(category_name)
    dd = add_category(mdata,category_name)
    print "Done."
    print "Parsing done."
    return dd
    
    

# - DB ----------------------------------------------------------------------------------
def save_results(mdata):
    scraperwiki.sqlite.save(unique_keys=["url"], data=mdata)

#END - DB -------------------------------------------------------------------------------


#   -HREFS- -----------------------------------------------------------------------------
#Вытаскиваются все ссылки на страницы и передаются в get_full_href_list
def get_pages_urls(category_url):
    urls = []

    str_page = ""
    try:
        str_page = load_page(category_url)
    except:
        print "Failed to load pages urls for category {0}".format(category_url)
        return urls
        
    urls = [category_url]
    doc = lxml.html.fromstring(str_page)
    doc.make_links_absolute(base_url)
    for el in doc.cssselect("div.pagination a"):
        urls.append(el.attrib['href'])
    return urls


#Получить полный список ссылок с указанных адресов страниц
def get_full_href_list(page_urls):
    lst = []
    p = 1
    for page_url in page_urls:
        print "Page "+str(p)+"/"+str(len(page_urls))

        try:
            pg = load_page(page_url)
        except:
            print "Failed to load page {0}".format(page_url)
            continue

        lst += get_href_list(scraperwiki.scrape(page_url))
        p = p + 1
        #print lst
    return lst




#Удаляет старые объявления, возвращает список новых объявлений
def clean_urls(desc_urls,category_name):
    global total_deleted
    global total_new

    lst = []
    db_urls = []
    if "swdata" in scraperwiki.sqlite.show_tables():
        for row in scraperwiki.sqlite.select("* from swdata where category_name='{0}'".format(category_name)):
            db_urls.append(row["url"])

    #delete out of date ads
    deleted = 0
    for url in db_urls:
        if url not in desc_urls:
            scraperwiki.sqlite.execute("delete from swdata where url='{0}'".format(url))
            deleted = deleted + 1
            total_deleted = total_deleted + 1
    print " - Deleted {0} ads.".format(deleted)    

    #return only new urls
    newurls = 0
    for url in desc_urls:
        if url not in db_urls:
            lst.append(url)
            newurls = newurls + 1
            total_new = total_new + 1
    print " - New urls: {0}.".format(newurls)    

    return lst
    

#Получить список ссылок с загруженной страницы
def get_href_list(page):
    doc = lxml.html.fromstring(page)
    doc.make_links_absolute(base_url)
    hrefs = doc.xpath('/html/body/div/div[2]/div/div/div/div[2]/a')
    lst = []
    for href in hrefs:
        lst.append(str(href.get('href')))
    return lst

def add_category(mdata,cat_name):
    lst = []
    for row in mdata:
        if type(row)==str:
            continue
        row["category_name"] = cat_name
        lst.append(row)
    return lst


#END -HREFS- ----------------------------------------------------------------------------





# -DESC- --------------------------------------------------------------------------------
#Получить окончательный список данных с указанных адресов
def get_info_list(desc_page_urls,limit):
    lst = []
    counter = 0
    for purl in desc_page_urls:
            ff =  get_data_row(purl)
            if ff == 'breake':
                print 'stopped'
                return lst 
            else:
                lst.append(ff)
                counter += 1
                if counter == limit and counter !=0:
                    break
                print '{0} fetched {1}/{2}'.format(counter,len(desc_page_urls),purl)
    return lst 

#Возвращает данные в виде ключ-значение для указанной страницы описаний
def get_data_row(desc_page_url):

    doc = None
    try:
        doc = lxml.html.fromstring(load_page(desc_page_url))
    except:
        return 'breake'


    try:
        row = {
        "url":desc_page_url.replace('\n',''),
        "title":get_title(doc).encode('utf-8').decode('utf-8').replace('\n',''),
         "desc":get_desc(doc).encode('utf-8').decode('utf-8').replace('\n',''),
        "price":get_price(doc).encode('utf-8').decode('utf-8').replace('\n',''),
        "phones":get_phones(doc).encode('utf-8').replace('Цена:','').replace(',',' ').decode('utf-8').replace('\n',''),
        "img":get_images_url(doc).replace('\n',''),
        "date":str(get_date(doc)),
        "error":''
            }
    except Exception as e1:
        print ' ^^^Exception'
        row = {
        "url":desc_page_url.replace('\n',''),
        "title":'',
         "desc":'',
        "price":'',
        "phones":'',
        "img":'',
        "date":'',
        "error":''
        }
        print e1.message.encode('utf-8')
        return row
    return row
     
#END -DESC- -----------------------------------------------------------------------------




# -DETAILS- -----------------------------------------------------------------------------
#Возвращает название категории
def get_category_name(doc):
    try:
        s= doc.xpath('/html/body/div/div[2]/div/div/center/h1/text()')[0]
        return s.strip()
    except Exception as e:
        raise Exception('Category name: '+e.message)

#Возвращает название объявления
def get_title(doc):
    try:
        s = doc.xpath('/html/body/div/div[2]/div/div/div[2]/h1/text()')[0]
        return s.lstrip().rstrip()
    except Exception as e:
        raise Exception('Title: '+e.message)

#Описание в объявлении
def get_desc(doc):
    try:
        outstr = doc.xpath('/html/body/div/div[2]/div/div/index/text()')[0]
        s = doc.xpath('/html/body/div/div[2]/div/div/index',smart_strings=False)[0]
        for child in s.iterdescendants():
            outstr  = outstr + lxml.html.tostring(child,encoding=unicode).strip().replace('<br>&#13;','')
        return outstr
    except Exception as e:
        raise Exception('Desc: '+e.message)

#Цену
def get_price(doc):
    try:
        s = doc.xpath('/html/body/div/div[2]/div/div/span/text()')
        if(len(s)>0):
            return s[0].lstrip().rstrip()
        else:
            return "no price"
    except Exception as e:
        raise Exception('Price: '+e.message)

#Телефоны
def get_phones(doc):
    try:
        lst = doc.xpath('/html/body/div/div[2]/div/div/text()',smart_strings=False)
        return ''.join(lst).replace('\n',',')
    except Exception as e:
        raise Exception('Phones: '+e.message)

#Ссылки на картинки
def get_images_url(doc):
    try:
        newlist = []
        lst = doc.xpath('/html/body/div/div[2]/div/div/div[6]/a/img')
        for el in lst:
            newlist.append(el.get('src'))
        return ''.join(newlist)
    except Exception as e:
        raise Exception('Images: '+e.message)

#Дата публикации объявления
def get_date(doc):
    try:
        s = doc.xpath('/html/body/div/div[2]/div/div/div[3]/text()')[0][6:].encode('utf-8')
        dateStr = s[:string.find(s,'г.')].strip()
        return datetime.datetime.strptime(dateStr, '%d.%m.%Y')
    except Exception as e:
        raise Exception('Date: '+e.message)

#END -DETAILS- --------------------------------------------------------------------------





      
start_parsing(5)

#doc = lxml.html.fromstring(load_page('http://doska.uralsk.info/c92-127214.html'))
#get_desc(doc)
#print type(get_date(doc))
#print scraperwiki.sqlite.table_info("swdata")

