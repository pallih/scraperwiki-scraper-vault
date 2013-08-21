import scraperwiki
from lxml import etree

#base_url = "http://www.uk-postcodes.com/distance.php?lat=[latitude]&lng=[longitude]&distance=[distance in miles]&format=[xml|csv|json]"
#http://www.uk-postcodes.com/distance.php?lat=51.375801&lng=-2.359904&distance=50&format=xml
url_comp1 ="http://www.uk-postcodes.com/distance.php?lat="
url_comp2 ="&lng="
url_comp3 = "&distance=15"
url_comp4 ="&format=xml"


#cities = {)}

places = {
          'Bath' : (51.375801, -2.359904, "BA2"),
          'Bristol': (51.457392, -2.58948, "BS1"),
          'Cornwall': (50.263664, -5.054564, "TR1"),
          'Croydon': (51.376165, -0.098234, "CR0"),
          'Derbyshire': (52.922695, -1.476910, "DE1"),
          'Devon': (50.777214, -3.999461, "EX20"),
          'Dorset':(50.741670, -2.381287, "DT2"),
          'Essex': (51.723172, 0.512238, "CM2"),
          'Exeter': (50.718412, -3.533899, "EX2"),
          'Grimsby': (53.563451, -0.073814, "DN32"),
          'Gloucestershire': (51.867347, -2.247131, "GL1"),
          'Hull': (53.74364,-0.3405, "HU1"),
          'Kent': (51.206883, 0.694885, "TN27"),
          'Leicestershire': (52.653894, -1.132691, "LE4"),
          'Lincolnshire': (53.230688, -0.540579, "LN2"),
          'North Devon': (51.07816, -4.058338, "EX32"),
          'Nottingham': (52.953059, -1.148736, "NG1"),
          'Plymouth': (50.371917, -4.13602, "PL1"),
          'Scunthorpe': (53.614, -0.650, "DN15"),
          'Somerset': (51.051754, -2.702637, "TA11"),
          'South Devon': (50.468795, -3.532125, "TQ1"),
          
          'Staffordshire': (53.023098, -2.197793, "ST1"),
          'Surrey': (54.455, -3.9, "GU20"),
          'Sussex': (50.928014, -0.461707, "RH20"),
          'Tamworth': (52.633584, -1.691032, "B79")}


for city in places.keys():
    latitude, longitude, postcode = places.get(city)
    print city
    city_url = url_comp1+str(latitude)+url_comp2+str(longitude)+url_comp3+url_comp4
    print city_url
    xml = scraperwiki.scrape(city_url)
    root = etree.fromstring(xml)
    
    postal = root.xpath("//postcode")
    print len(postal)
    for address in postal:
        record = {}
        latitude = address.xpath("lat")
        #print latitude[0].text
        record['latitude'] = latitude[0].text
        longitude = address.xpath("lng")
        record['longitude'] = longitude[0].text
        uri = address.xpath("uri")
        uri = uri[0].text
        uri = uri.replace("http://www.uk-postcodes.com/postcode/", "")
        record['postcode'] = uri
        record['place'] = city
        scraperwiki.sqlite.save(['postcode'], record)



