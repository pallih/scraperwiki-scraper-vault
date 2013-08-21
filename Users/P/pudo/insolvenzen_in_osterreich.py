import scraperwiki
import lxml.html

URL = "http://www.edikte.justiz.gv.at/edikte/id/idedi8.nsf/suchedi?SearchView&subf=v&SearchOrder=4&FT=wien&SDatArt1=DATAF&SDatWert3=13.6.2012&SDatWert4=&SDatWert1=&SDatWert2=&ftquery=wien&query=%28%28wien%29%29_%26_DATAF%3E%3D%5B13.6.2012%5D"

web_page = lxml.html.parse(URL)

table_of_insolvencies = web_page.find('//table/tbody')

for row in table_of_insolvencies.findall('tr'):
    cells = row.findall('td')
    nr, reference_number, debtor = cells
    
    data = {}

    details_link = reference_number.find('a')
    data['reference'] = details_link.text
    data['link'] = details_link.get('href')

    data['debtor_name'] = debtor.text

    remaining_lines = [d.tail for d in debtor.findall('br')]
    if len(remaining_lines) == 2:
        data['debtor_profession'] = remaining_lines[0]
        data['debtor_town'] = remaining_lines[1]
    else:
        data['debtor_town'] = remaining_lines[0] 

    data['debtor_postcode'], data['debtor_town'] = data['debtor_town'].split(" ", 1)
    
    scraperwiki.sqlite.save(unique_keys=['reference'], data=data)

