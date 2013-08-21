import scraperwiki
import bs4
import string, unicodedata

ph_baseurl = 'https://resources.parenthelp123.org/'

ph_index = scraperwiki.scrape(ph_baseurl)

soup_index = bs4.BeautifulSoup(ph_index)

def strip_string_to_lowercase(s):
    return ''.join(c for c in s if c in string.ascii_lowercase + string.ascii_uppercase)

def getSectionData(cat_name,cat_url,section_name):
    page_add = '?page='
    page = 1
    while True:
        url = ph_baseurl + cat_url[1:] + page_add + str(page)
        ph_section = scraperwiki.scrape(url)
        soup_section = bs4.BeautifulSoup(ph_section)
        r_table = soup_section.find(id = "results_table")
        if not r_table:
            break
        else:
            page = page + 1
            for service in r_table.find_all('tr')[1:]:
                row = {}
                cells = service('td')
                row['resource_id'] = service.get('id').replace('resource_','')
                row['name'] = cells[0].find('a').get_text()
                if cells[0].find('p'):
                    row['info'] = unicodedata.normalize('NFKD', cells[0].find('p').get_text())
                if len(cells[1].contents) > 1: 
                    row['address1'] = str(cells[1].contents[-3]).replace('\n','')
                    row['address2'] = str(cells[1].contents[-1]).replace('\n','')
                if cells[2].find('li'):
                    row['phone'] = cells[2].find('li').get_text()
                if cells[2].find('a'):
                    row['website'] = cells[2].find('a').get('href')
                row['key'] = section_name + row['resource_id']
                row['section_name'] = section_name
                row['category_names'] = cat_name
                scraperwiki.sqlite.save(unique_keys=['key'], data=row)
                
            
            
        

for section in soup_index.find(id = "drilldown").find_all('li'):
    section_name = strip_string_to_lowercase(section.h3.get_text())
    for cat in section.find_all("div")[1:]:
        cat_url = str(cat.a.get('href'))
        cat_name = strip_string_to_lowercase(cat.get_text().split('(', 1)[0])
        getSectionData(cat_name,cat_url,section_name)
        
        