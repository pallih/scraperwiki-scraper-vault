import urllib, urllib2
from lxml import etree
import scraperwiki

#scraperwiki.cache(True)

neighbourhoods = dict([
('A1', 'East Wallasey'),
('A2', 'Moreton and West Wallasey'),
('A3', 'Hoylake'),
('A4', 'Upton, Prenton and Egerton'),
('A5', 'Bidston and St. James, Oxton and Claughton'),
('A6', 'Birkenhead'),
('A7', 'Bromborough'),
('A8', 'Heswall'),
('B1', 'Bootle'),
('B2', 'Crosby'),
('B3', 'Litherland and Netherton'),
('B4', 'Maghull'),
('B5', 'Formby, Ainsdale and Birkdale'),
('B6', 'Southport North East'),
('B7', 'Southport Town Centre'),
('C1', 'Kirkby'),
('C2', 'Huyton'),
('C3', 'Prescot, Whiston and Halewood'),
('D1', 'St Helens Town Centre'),
('D2', 'Parr, Sutton and Bold'),
('D3', 'Rainhill, Thatto Heath, Eccleston and West Park'),
('D4', 'Windle, Rainford, Moss Bank, Billinge and Seneley Green'),
('D5', 'Newton, Haydock, Blackbrook and Earlestown'),
('E1', 'City'),
('E3', 'Kirkdale'),
('E2', 'Everton, Anfield and County'),
('E5', 'Kensington, Fairfield and Tuebrook'),
('E4', 'Old Swan, West Derby, Yew Tree and Knotty Ash'),
('E6', 'Croxteth, Norris Green and Clubmoor'),
('E7', 'Warbreck and Fazakerley'),
('F1', 'Riverside, St Michaels, Greenbank and Dingle'),
('F2', 'Princes, Picton, Granby and Wavertree'),
('F3', 'Childwall, Church and Mossley Hill'),
('F4', 'Allerton, Belle Vale, Netherley and Woolton'),
('F5', 'Cressington, Garston and Speke')])

areas = {
  'A': 'Wirral',
  'B': 'Sefton',
  'C': 'Knowsley',
  'D': 'St Helens',
  'E': 'Liverpool North',
  'F': 'Liverpool South',
}

def get_td_following(doc, text, tag='td'):
    return doc.xpath("//%s[text()='%s']/following-sibling::*[1]" % (tag, text))[0].text

def scrape_area(area, neighb, year, html):
    data = {'area': areas[area], 'neighbourhood': neighbourhoods[neighb], 'year': year}
    doc = etree.HTML(html)
    data['violent_crime'] = get_td_following(doc, 'Violent Crime')
    data['burglary'] = get_td_following(doc, 'Burglary')
    data['vehicle_crime'] = get_td_following(doc, 'Vehicle Crime')
    data['non_vehicle_theft'] = get_td_following(doc, 'Non Vehicle Theft')
    data['fraud_and_forgery'] = get_td_following(doc, 'Fraud and Forgery')
    data['drug_offences'] = get_td_following(doc, 'Drug Offences')
    data['criminal_damage'] = get_td_following(doc, 'Criminal Damage')
    data['other_crime'] = get_td_following(doc, 'Other Crime')
    #data['total_crime'] = get_td_following(doc, ' Total Crime ', 'th')
    scraperwiki.datastore.save(['area', 'neighbourhood', 'year'], data)

for year in range(2004, 2011):
    for area in areas.keys():
        for neighb in [x for x in neighbourhoods.keys() if x.startswith(area)]:
            print area, neighb, year
            data = urllib.urlencode({'p_beat': 'ALL', 'p_area': area,'p_neighbourhood': neighb, 'p_category': 'ALL_CRIME', 'p_year': year})
            f = urllib2.urlopen('http://www.merseysidepolice.info/webfigures/Index.htm', data)
            scrape_area(area, neighb, year, f.read())
