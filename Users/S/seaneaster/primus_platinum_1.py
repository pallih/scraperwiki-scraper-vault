import scraperwiki
import lxml.html

companies = ['AgrIcola+Daniella',
'Agricola+El+Consuelo',
'Agricola+El+Rosal',
'Agricola+Pony',
'Andrew+&+Williamson',
'Andrew+Smith+Company',
'Babe+Farms',
'Baja+Premium+Fresh',
'BeachSide+Produce',
'Better+Produce',
'BJ+Brothers+Produce',
'Boggiatto+Produce',
'BoniPak+Produce+Company',
'Brooks+Tropicals',
'Cal-Cel+Marketing',
'California+Giant',
'CC+Tropicales',
'Central+West+Produce',
'Channel+Islands+Farms',
'Chieftain+Harvesting',
'Christopher+Ranch',
'Church+Brothers',
'Circle+Produce',
'Classic+Salads',
'Coastline+Produce',
'Combs+Produce',
'Custom+Produce+Sales',
'First+Choice+Distributing',
'Divine+Flavor',
'Driscoll+Strawberry+Associates',
'Duda+Farm+Fresh+Foods',
'Eclipse+Berry+Farms',
'Expo+Fresh+San+Vicente+Camalu',
"Farmer's+Best+International",
'Five+Crowns+Marketing',
"Frank's+Distributing+of+Produce",
'Fresh+Farms',
'Fresh+Kist+Produce',
'Fresh+Quest+Produce',
'Freshway+Foods',
'Frutas+Selectas+de+Tijuana',
'MJ+International+Marketing',
'Gargiulo',
'General+Produce',
'George+Amaral+Ranches',
'GR+Produce',
'Harris+Farms',
'HC+Produce',
'Heller+Bros.+Packing+Corp',
'Hugh+H.+Branch',
'J-C+Distributing',
'Kaliroy+Produce',
'Kingdom+Fresh+Produce',
'Limoneira+Company',
'Harris+Fresh',
'Mann+Packing+Company',
'MAS+Melons+&+Grapes',
'Metz+Fresh',
'Meyer+Tomatoes',
'Misionero+Vegetables',
'Naturipe+Farms',
'New+Lime+Co.',
'NewStar+Fresh+Foods',
'Ocean+Mist+Farms',
'Pacific+International+Marketing',
'Pacific+Tomato+Growers',
'Pappas+Produce+Company',
'Pinos+Produce',
'Pismo+Oceano+Vegetable+Exchange',
'Prime+Time+International',
'Red+Blossom+Farms',
'Righetti+Farms',
'Rio+Queen+Citrus',
'River+Ranch+Fresh+Foods',
'RM+Produce+Corporation',
'Royal+Flavor',
'S&H+Packing+&+Sales',
'Salad+Savoy+Corporation',
'San+Miguel+Produce',
'Sanbon',
'Santa+Barbara+Farms',
'Santa+Sweets',
'Shuman+Produce',
'Sigma+Sales',
'Simonian+Fruit',
"Six+L's",
'Sun+Coast+Farms+Sales',
'Sun+World+International',
'SunFed',
'Sunnyside+Packing+Company',
'Sunrise+Growers-Frozsun+Foods',
'Taylor+Farms',
'United+Greenhouse',
'Valores+Horticolas+del+Pacifico',
'Watsonville+Produce',
'Well+Pict',
'West+Lake+Fresh',
'Wiers+Farms',
'Custom+Pak']

# WARNING LETTERS: http://google2.fda.gov/search?client=FDAgov&site=FDAgov-WarningLetters-ICECI&output=xml_no_dtd&proxystylesheet=FDAgov&ie=UTF-8&oe=UTF-8&as_q=&num=100&btnG=Search&as_epq=COMPANY+NAME&as_oq=&as_eq=&restrictBox=FDAgov-WarningLetters-ICECI&lr=&as_ft=i&as_filetype=&as_occt=any&as_dt=i&as_sitesearch=&sort=
# ENFORCEMENT REPORTS http://google2.fda.gov/search?client=FDAgov&site=FDAgov-EnforcementReports-Safety&output=xml_no_dtd&proxystylesheet=FDAgov&ie=UTF-8&oe=UTF-8&as_q=++&num=100&btnG=Search&as_epq=COMPANY+NAME&as_oq=&as_eq=&restrictBox=FDAgov-EnforcementReports-Safety&lr=&as_ft=i&as_filetype=&as_occt=any&as_dt=i&as_sitesearch=&sort=

SearchURL1First = "http://google2.fda.gov/search?client=FDAgov&site=FDAgov-WarningLetters-ICECI&output=xml_no_dtd&proxystylesheet=FDAgov&ie=UTF-8&oe=UTF-8&as_q=&num=100&btnG=Search&as_epq="
SearchURL1Second = "&as_oq=&as_eq=&restrictBox=FDAgov-WarningLetters-ICECI&lr=&as_ft=i&as_filetype=&as_occt=any&as_dt=i&as_sitesearch=&sort="

SearchURL2First = "http://google2.fda.gov/search?client=FDAgov&site=FDAgov-EnforcementReports-Safety&output=xml_no_dtd&proxystylesheet=FDAgov&ie=UTF-8&oe=UTF-8&as_q=++&num=100&btnG=Search&as_epq="
SearchURL2Second = "&as_oq=&as_eq=&restrictBox=FDAgov-EnforcementReports-Safety&lr=&as_ft=i&as_filetype=&as_occt=any&as_dt=i&as_sitesearch=&sort="

html = []
root = []

for z in companies:
    html.append(scraperwiki.scrape(SearchURL1First + z + SearchURL1Second))
    html.append(scraperwiki.scrape(SearchURL2First + z + SearchURL2Second))

for x in html:
    root.append(lxml.html.fromstring(x))

for y in root:
    for el in y.cssselect("p.g a"):
        data = {
            'URL' : el.attrib['href']
        }
        scraperwiki.sqlite.save(unique_keys=['URL'], data=data)


