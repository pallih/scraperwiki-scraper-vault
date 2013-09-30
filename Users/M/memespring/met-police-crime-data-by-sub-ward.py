import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

def extract_areas(page):
    
    result = []
    table = page.find('table', {'id': 'areas-table'})    
    for row in table.findAll('td', {'class': 'area'})[1:]:
        area_name = row.a.string.replace('&amp;', '&')
        area_link = 'http://maps.met.police.uk/php/dataview.php' + row.a['href']
        area_id = row.a['href'].split('&')[0].replace('?area=', '')
        result.append({'area_name': area_name, 'area_link': area_link, 'area_id': area_id})
        
    return result

def extract_crime(url):

    result = []

    html = scraperwiki.scrape(url)
    page = BeautifulSoup.BeautifulSoup(html)
    month = page.find('h2', {'class': 'textviewtitleblock'}).span.string.replace('Total notifiable offences, ', '')
    
    crime_table = page.find('table', {'class': 'crime-table'})
    for row in crime_table.findAll('tr')[1:]:
        crime_type = row.find('td', {'class': 'type'}).string
        crime_count = row.find('td', {'class': 'count'}).string
        crime_rate = row.find('td', {'class': 'rate'}).string
        result.append({'month': month, 'crime_type': crime_type, 'crime_count': crime_count, 'crime_rate': crime_rate})        
    
    return result


def main():
    #scrape page
    borough_html = scraperwiki.scrape('http://maps.met.police.uk/php/dataview.php?area=MPS&ct=8')
    borough_page = BeautifulSoup.BeautifulSoup(borough_html)
    boroughs = extract_areas(borough_page)

    for borough in boroughs:
        ward_html = scraperwiki.scrape(borough['area_link'])
        ward_page = BeautifulSoup.BeautifulSoup(ward_html)
        wards = extract_areas(ward_page)
        for ward in wards:
            sub_ward_html = scraperwiki.scrape(ward['area_link'])
            sub_ward_page = BeautifulSoup.BeautifulSoup(sub_ward_html)
            sub_wards = extract_areas(sub_ward_page) 

            for sub_ward in sub_wards:
                crimes = extract_crime(sub_ward['area_link'])
                for crime in crimes:
                    
                    data = {
                        'borough' : borough['area_name'],
                        'ward' : ward['area_name'],
                        'sub_ward' : sub_ward['area_name'],
                        'super_output_area_code' : sub_ward['area_id'],                            
                        'month': crime['month'],
                        'crime_type': crime['crime_type'],
                        'crime_rate': crime['crime_rate'],
                        'crime_count': crime['crime_count'],                            
                        }

                    datastore.save(unique_keys=['super_output_area_code', 'month', 'crime_type'], data=data)

main()
import scraperwiki
import BeautifulSoup

from scraperwiki import datastore

def extract_areas(page):
    
    result = []
    table = page.find('table', {'id': 'areas-table'})    
    for row in table.findAll('td', {'class': 'area'})[1:]:
        area_name = row.a.string.replace('&amp;', '&')
        area_link = 'http://maps.met.police.uk/php/dataview.php' + row.a['href']
        area_id = row.a['href'].split('&')[0].replace('?area=', '')
        result.append({'area_name': area_name, 'area_link': area_link, 'area_id': area_id})
        
    return result

def extract_crime(url):

    result = []

    html = scraperwiki.scrape(url)
    page = BeautifulSoup.BeautifulSoup(html)
    month = page.find('h2', {'class': 'textviewtitleblock'}).span.string.replace('Total notifiable offences, ', '')
    
    crime_table = page.find('table', {'class': 'crime-table'})
    for row in crime_table.findAll('tr')[1:]:
        crime_type = row.find('td', {'class': 'type'}).string
        crime_count = row.find('td', {'class': 'count'}).string
        crime_rate = row.find('td', {'class': 'rate'}).string
        result.append({'month': month, 'crime_type': crime_type, 'crime_count': crime_count, 'crime_rate': crime_rate})        
    
    return result


def main():
    #scrape page
    borough_html = scraperwiki.scrape('http://maps.met.police.uk/php/dataview.php?area=MPS&ct=8')
    borough_page = BeautifulSoup.BeautifulSoup(borough_html)
    boroughs = extract_areas(borough_page)

    for borough in boroughs:
        ward_html = scraperwiki.scrape(borough['area_link'])
        ward_page = BeautifulSoup.BeautifulSoup(ward_html)
        wards = extract_areas(ward_page)
        for ward in wards:
            sub_ward_html = scraperwiki.scrape(ward['area_link'])
            sub_ward_page = BeautifulSoup.BeautifulSoup(sub_ward_html)
            sub_wards = extract_areas(sub_ward_page) 

            for sub_ward in sub_wards:
                crimes = extract_crime(sub_ward['area_link'])
                for crime in crimes:
                    
                    data = {
                        'borough' : borough['area_name'],
                        'ward' : ward['area_name'],
                        'sub_ward' : sub_ward['area_name'],
                        'super_output_area_code' : sub_ward['area_id'],                            
                        'month': crime['month'],
                        'crime_type': crime['crime_type'],
                        'crime_rate': crime['crime_rate'],
                        'crime_count': crime['crime_count'],                            
                        }

                    datastore.save(unique_keys=['super_output_area_code', 'month', 'crime_type'], data=data)

main()
