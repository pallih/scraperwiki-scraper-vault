import scraperwiki
import lxml.html 

base_url = 'http://www.autoevolution.com'
#base_url = 'http://64.225.158.193'

def scrape_series(brand_page):
    """ Get serie names and URLs
        returns list of tuples (serie_name, lxml) """

    serie_pages = brand_page.cssselect('.serie_title h2 a')
    return map(lambda page: (page.text, lxml.html.fromstring(scraperwiki.scrape(base_url + page.attrib['href']))), serie_pages)

def get_tab_data(tabbar):
    try:
        return map(lambda tab: (tab.attrib['id'][:3] + 'content'+ tab.attrib['id'][3:], tab.cssselect('a')[0].text), tabbar)
    except IndexError:
        pass

def get_table_contents(model, table_id):
    """ Parse data from table by tab """
    table_data =  {}
    table = model.cssselect('#%s' % table_id)
    try:
        rows = table[0].cssselect("tr")
        for row in rows:
            cells = row.cssselect('td')
            try:
                table_data[cells[0].text.strip()[:-1]] = cells[1].text.strip()

            except IndexError:
                pass

        return table_data
    except IndexError:
        pass


def car_scraper():
    
    # get car list from here
    url = base_url + '/cars/'

    html = scraperwiki.scrape(url)
    
    root = lxml.html.fromstring(html)

    tech_groups = {}
    feature_groups = {}
    tech_data = {}
    
    model_data = None
    
    # database 
    result = []
    
    for brand in root.cssselect("#brands .brand a"):
        # print brand.text.lower() + ' ' + brand.attrib['href']
        # go to brand page
        brand_page = lxml.html.fromstring(scraperwiki.scrape(base_url + brand.attrib['href']))
        
        series = scrape_series(brand_page)
        
        # individual serie of current brand
        for (serie_name, serie) in series:
            for s in serie.cssselect(".model_by_year_tbl .elisting a"):
                try:
                    model = lxml.html.fromstring(scraperwiki.scrape(base_url + s.attrib['href']))
                    
                    # Group techincal data by tabs
                    tabbar1 =  get_tab_data(model.cssselect("#tabbar1 div"))
                    try:
                        for (table_id, tab_name) in tabbar1:
                             tech_groups[tab_name] = get_table_contents(model, table_id)
                    except TypeError:
                        pass
    
                    # Features
                    tabbar2 = get_tab_data(model.cssselect("#tabbar2 div"))
                    try:
                        for (table_id, tab_name) in tabbar2:

                            if feature_groups[tab_name] is None:
                                feature_groups[tab_name] = {}
                            
                            table = model.cssselect('#%s table' % table_id)
                            for tr in table[0].cssselect('tr'):
                                feature_name = tr.cssselect('td')[0].text
                                feature_val = ''

                                try: 
                                    feature_val = tr.cssselect('td')[1].cssselect('img')[0].attrib['alt']
                                except:
                                    pass

                                #feature_groups[tab_name][feature_name] = feature_val
                                print  (feature_name, feature_val)

                    except TypeError:
                        pass
    
                    model_data = { 'title': s.attrib['title'].strip(), 'engine': s.text.strip(), 'tech_groups': tech_groups, 'feature_groups': feature_groups }
                    # scraperwiki.sqlite.save(unique_keys=['title'], data=model_data)
                    print model_data
                    tech_groups = {}
                    feature_groups = {}
                    result.append(model_data)
                except:
                    # read error (IncompleteRead)
                    pass

                
car_scraper()
