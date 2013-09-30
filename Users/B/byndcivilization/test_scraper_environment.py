import scraperwiki
import urllib2, urlparse
import lxml.html, lxml.etree
import re
import calendar
from datetime import datetime


url = "http://www.un.org/en/peacekeeping/contributors/2013/jul13_3.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

mlnk = re.search("contributors/(\d\d\d\d)/(.*?_3.pdf)", url)
urlEnd = mlnk.group(2)
mnz = re.match("(...).*?(?:\d\d)?(\d\d)?_3.pdf", urlEnd)
m3 = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
iso3Alpha = {"Aruba":"ABW","Afghanistan":"AFG","Angola":"AGO","Anguilla":"AIA","Aland Islands":"ALA","Albania":"ALB","Andorra":"AND","United Arab Emirates":"ARE","Argentina":"ARG","Armenia":"ARM","American Samoa":"ASM","Antarctica":"ATA","French Southern Territories":"ATF","Antigua and Barbuda":"ATG","Australia":"AUS","Austria":"AUT","Azerbaijan":"AZE","Burundi":"BDI","Belgium":"BEL","Benin":"BEN","Bonaire Sint Eustatius and Saba":"BES","Burkina Faso":"BFA","Bangladesh":"BGD","Bulgaria":"BGR","Bahrain":"BHR","Bahamas":"BHS","Bosnia and Herzegovina":"BIH","Saint Barthelemy":"BLM","Belarus":"BLR","Belize":"BLZ","Bermuda":"BMU","Bolivia":"BOL","Brazil":"BRA","Barbados":"BRB","Brunei":"BRN","Bhutan":"BTN","Bouvet Island":"BVT","Botswana":"BWA","Central African Republic":"CAF","Canada":"CAN","Cocos (Keeling) Islands":"CCK","Switzerland":"CHE","Chile":"CHL","China":"CHN","Cote d Ivoire":"CIV","Cameroon":"CMR","DR Congo":"COD","Congo":"COG","Cook Islands":"COK","Colombia":"COL","Comoros":"COM","Cape Verde":"CPV","Costa Rica":"CRI","Cuba":"CUB","Curacao":"CUW","Christmas Island":"CXR","Cayman Islands":"CYM","Cyprus":"CYP","Czech Republic":"CZE","Germany":"DEU","Djibouti":"DJI","Dominica":"DMA","Denmark":"DNK","Dominican Republic":"DOM","Algeria":"DZA","Ecuador":"ECU","Egypt":"EGY","Eritrea":"ERI","Western Sahara":"ESH","Spain":"ESP","Estonia":"EST","Ethiopia":"ETH","Finland":"FIN","Fiji":"FJI","Falkland Islands (Malvinas)":"FLK","France":"FRA","Faroe Islands":"FRO","Micronesia Federated States of":"FSM","Gabon":"GAB","United Kingdom":"GBR","Georgia":"GEO","Guernsey":"GGY","Ghana":"GHA","Gibraltar":"GIB","Guinea":"GIN","Guadeloupe":"GLP","Gambia":"GMB","Guinea-Bissau":"GNB","Equatorial Guinea":"GNQ","Greece":"GRC","Grenada":"GRD","Greenland":"GRL","Guatemala":"GTM","French Guiana":"GUF","Guam":"GUM","Guyana":"GUY","Hong Kong":"HKG","Heard Island and McDonald Islands":"HMD","Honduras":"HND","Croatia":"HRV","Haiti":"HTI","Hungary":"HUN","Indonesia":"IDN","Isle of Man":"IMN","India":"IND","British Indian Ocean Territory":"IOT","Ireland":"IRL","Iran":"IRN","Iraq":"IRQ","Iceland":"ISL","Israel":"ISR","Italy":"ITA","Jamaica":"JAM","Jersey":"JEY","Jordan":"JOR","Japan":"JPN","Kazakhstan":"KAZ","Kenya":"KEN","Kyrgyzstan":"KGZ","Cambodia":"KHM","Kiribati":"KIR","Saint Kitts and Nevis":"KNA","Republic of Korea":"KOR","Kuwait":"KWT","Lao People's Democratic Republic":"LAO","Lebanon":"LBN","Liberia":"LBR","Libya":"LBY","Saint Lucia":"LCA","Liechtenstein":"LIE","Sri Lanka":"LKA","Lesotho":"LSO","Lithuania":"LTU","Luxembourg":"LUX","Latvia":"LVA","The former Yugoslav Republic of Macedoniaao":"MAC","Saint Martin (French part)":"MAF","Morocco":"MAR","Monaco":"MCO","Moldova, Republic of":"MDA","Madagascar":"MDG","Maldives":"MDV","Mexico":"MEX","Marshall Islands":"MHL","The former Yugoslav Republic of Macedonia":"MKD","Macedonia, FYROM":"MKD","Mali":"MLI","Malta":"MLT","Myanmar":"MMR","Montenegro":"MNE","Mongolia":"MNG","Northern Mariana Islands":"MNP","Mozambique":"MOZ","Mauritania":"MRT","Montserrat":"MSR","Martinique":"MTQ","Mauritius":"MUS","Malawi":"MWI","Malaysia":"MYS","Mayotte":"MYT","Namibia":"NAM","New Caledonia":"NCL","Niger":"NER","Norfolk Island":"NFK","Nigeria":"NGA","Nicaragua":"NIC","Niue":"NIU","Netherlands":"NLD","Norway":"NOR","Nepal":"NPL","Nauru":"NRU","New Zealand":"NZL","Oman":"OMN","Pakistan":"PAK","Panama":"PAN","Pitcairn":"PCN","Peru":"PER","Philippines":"PHL","Palau":"PLW","Papua New Guinea":"PNG","Poland":"POL","Puerto Rico":"PRI","Korea Democratic People's Republic of":"PRK","Portugal":"PRT","Paraguay":"PRY","Palestine State of":"PSE","French Polynesia":"PYF","Qatar":"QAT","Reunion":"REU","Romania":"ROU","Russian Federation":"RUS","Rwanda":"RWA","Saudi Arabia":"SAU","Sudan":"SDN","Senegal":"SEN","Singapore":"SGP","South Georgia and the South Sandwich Islands":"SGS","Saint Helena Ascension and Tristan da Cunha":"SHN","Svalbard and Jan Mayen":"SJM","Solomon Islands":"SLB","Sierra Leone":"SLE","El Salvador":"SLV","San Marino":"SMR","Somalia":"SOM","Saint Pierre and Miquelon":"SPM","Serbia":"SRB","South Sudan":"SSD","Sao Tome and Principe":"STP","Suriname":"SUR","Slovakia":"SVK","Slovenia":"SVN","Sweden":"SWE","Swaziland":"SWZ","Sint Maarten (Dutch part)":"SXM","Seychelles":"SYC","Syrian Arab Republic":"SYR","Turks and Caicos Islands":"TCA","Chad":"TCD","Togo":"TGO","Thailand":"THA","Tajikistan":"TJK","Tokelau":"TKL","Turkmenistan":"TKM","Timor-Leste":"TLS","Tonga":"TON","Trinidad and Tobago":"TTO","Tunisia":"TUN","Turkey":"TUR","Tuvalu":"TUV","Taiwan Province of China":"TWN","Tanzania, United Republic of":"TZA","Uganda":"UGA","Ukraine":"UKR","United States Minor Outlying Islands":"UMI","Uruguay":"URY","United States of America":"USA","Uzbekistan":"UZB","Holy See (Vatican City State)":"VAT","Saint Vincent and the Grenadines":"VCT","Venezuela Bolivarian Republic of":"VEN","Virgin Islands British":"VGB","Virgin Islands U.S.":"VIR","Viet Nam":"VNM","Vanuatu":"VUT","Wallis and Futuna":"WLF","Samoa":"WSM","Yemen":"YEM","South Africa":"ZAF","Zambia":"ZMB","Zimbabwe":"ZWE"}
iso3Num = {"Afghanistan":"004","Albania":"008","Antarctica":"010","Algeria":"012","American Samoa":"016","Andorra":"020","Angola":"024","Antigua and Barbuda":"028","Azerbaijan":"031","Argentina":"032","Australia":"036","Austria":"040","Bahamas":"044","Bahrain":"048","Bangladesh":"050","Armenia":"051","Barbados":"052","Belgium":"056","Bermuda":"060","Bhutan":"064","Bolivia":"068","Bosnia and Herzegovina":"070","Botswana":"072","Bouvet Island":"074","Brazil":"076","Belize":"084","British Indian Ocean Territory":"086","Solomon Islands":"090","Virgin Islands British":"092","Brunei":"096","Bulgaria":"100","Myanmar":"104","Burundi":"108","Belarus":"112","Cambodia":"116","Cameroon":"120","Canada":"124","Cape Verde":"132","Cayman Islands":"136","Central African Republic":"140","Sri Lanka":"144","Chad":"148","Chile":"152","China":"156","Taiwan Province of China":"158","Christmas Island":"162","Cocos (Keeling) Islands":"166","Colombia":"170","Comoros":"174","Mayotte":"175","Congo":"178","DR Congo":"180","Cook Islands":"184","Costa Rica":"188","Croatia":"191","Cuba":"192","Cyprus":"196","Czech Republic":"203","Benin":"204","Denmark":"208","Dominica":"212","Dominican Republic":"214","Ecuador":"218","El Salvador":"222","Equatorial Guinea":"226","Ethiopia":"231","Eritrea":"232","Estonia":"233","Faroe Islands":"234","Falkland Islands (Malvinas)":"238","South Georgia and the South Sandwich Islands":"239","Fiji":"242","Finland":"246","Aland Islands":"248","France":"250","French Guiana":"254","French Polynesia":"258","French Southern Territories":"260","Djibouti":"262","Gabon":"266","Georgia":"268","Gambia":"270","Palestine":"275","Germany":"276","Ghana":"288","Gibraltar":"292","Kiribati":"296","Greece":"300","Greenland":"304","Grenada":"308","Guadeloupe":"312","Guam":"316","Guatemala":"320","Guinea":"324","Guyana":"328","Haiti":"332","Heard Island and McDonald Islands":"334","Holy See":"336","Honduras":"340","Hong Kong":"344","Hungary":"348","Iceland":"352","India":"356","Indonesia":"360","Iran":"364","Iraq":"368","Ireland":"372","Israel":"376","Italy":"380","Cote d Ivoire":"384","Jamaica":"388","Japan":"392","Kazakhstan":"398","Jordan":"400","Kenya":"404","Korea Democratic People's Republic of":"408","Republic of Korea":"410","Kuwait":"414","Kyrgyzstan":"417","Lao People's Democratic Republic":"418","Lebanon":"422","Lesotho":"426","Latvia":"428","Liberia":"430","Libya":"434","Liechtenstein":"438","Lithuania":"440","Luxembourg":"442","Macao":"446","Madagascar":"450","Malawi":"454","Malaysia":"458","Maldives":"462","Mali":"466","Malta":"470","Martinique":"474","Mauritania":"478","Mauritius":"480","Mexico":"484","Monaco":"492","Mongolia":"496","Moldova, Republic of":"498","Montenegro":"499","Montserrat":"500","Morocco":"504","Mozambique":"508","Oman":"512","Namibia":"516","Nauru":"520","Nepal":"524","Netherlands":"528","Curacao":"531","Aruba":"533","Sint Maarten":"534","Bonaire Sint Eustatius and Saba":"535","New Caledonia":"540","Vanuatu":"548","New Zealand":"554","Nicaragua":"558","Niger":"562","Nigeria":"566","Niue":"570","Norfolk Island":"574","Norway":"578","Northern Mariana Islands":"580","United States Minor Outlying Islands":"581","Micronesia Federated States of":"583","Marshall Islands":"584","Palau":"585","Pakistan":"586","Panama":"591","Papua New Guinea":"598","Paraguay":"600","Peru":"604","Philippines":"608","Pitcairn":"612","Poland":"616","Portugal":"620","Guinea-Bissaua":"624","Timor-Leste":"626","Puerto Rico":"630","Qatar":"634","Reunion":"638","Romania":"642","Russian Federation":"643","Rwanda":"646","Saint Barthalemy":"652","Saint Helena Ascension and Tristan da Cunha":"654","Saint Kitts and Nevis":"659","Anguilla":"660","Saint Lucia":"662","Saint Martin":"663","Saint Pierre and Miquelon":"666","Saint Vincent and the Grenadines":"670","San Marino":"674","Sao Tome and Principe":"678","Saudi Arabia":"682","Senegal":"686","Serbia":"688","Seychelles":"690","Sierra Leone":"694","Singapore":"702","Slovakia":"703","Viet Nam":"704","Slovenia":"705","Somalia":"706","South Africa":"710","Zimbabwe":"716","Spain":"724","South Sudan":"728","Sudan":"729","Western Sahara":"732","Suriname":"740","Svalbard and Jan Mayen":"744","Swaziland":"748","Sweden":"752","Switzerland":"756","Syrian Arab Republic":"760","Tajikistan":"762","Thailand":"764","Togo":"768","Tokelau":"772","Tonga":"776","Trinidad and Tobago":"780","United Arab Emirates":"784","Tunisia":"788","Turkey":"792","Turkmenistan":"795","Turks and Caicos Islands":"796","Tuvalu":"798","Uganda":"800","Ukraine":"804","The former Yugoslav Republic of Macedonia":"807","Macedonia, FYROM":"807","Egypt":"818","United Kingdom":"826","Guernsey":"831","Jersey":"832","Isle of Man":"833","Tanzania, United Republic of":"834","United States of America":"840","Virgin Islands U.S.":"850","Burkina Faso":"854","Uruguay":"858","Uzbekistan":"860","Venezuela":"862","Wallis and Futuna":"876","Samoa":"882","Yemen":"887","Zambia":"894"}
year = int(mlnk.group(1))
month = m3.index(mnz.group(1).lower())+1
day = calendar.monthrange(year, month)[1]
dateString = str(month) + '/' + str(day) + '/' + str(year-2000)
date = datetime(year, month, day).strftime('%Y%m%d')


def Main():
    # xmldata = pdftoxml(pdfdata)
    # root = lxml.etree.fromstring(xmldata)
    # print "After converting to xml it has %d bytes" % len(xmldata)
    # print "The first 2000 characters are: ", xmldata[:2000]
    #initialize varialbes
    currentCountry = None
    currentCountryISO3Num = None
    currentCountryISO3Alpha = None
    currentMission = None
    ldata = [ ]
    contributionData = None

    for page in list(root): #iterate through pages
        rtblocks = [ ] #initializes ?????
        #print lxml.etree.tostring(page)
        for text in page: #iterates through each text element
            if text.tag != "text": #checks to see if the element tag is 'text'. if not moves to next element in loop
                continue

            if 130 <= int(text.attrib.get("left")) <= 140: # IDs contributor blocks...if not, moves on
            #print lxml.etree.tostring(text)
                currentMission = None #Resets currentMission block
                currentCountry = textContent(text).strip()  #Sets current contributor to the text inside tag
                currentCountryISO3Num = iso3Num[currentCountry]
                currentCountryISO3Alpha = iso3Alpha[currentCountry]

            if 276 <= int(text.attrib.get("left")) <= 280: # IDs mission blocks...if not, moves on
                if rtblocks and contributionData: #Checks to see if  tag is already within mission and contributor block
                    lndata = parseMissionBlock(rtblocks, contributionData)
                    ldata.extend(lndata)
                currentMission = textContent(text).strip()
                contributionData = {"DATE":date, "DATE_STRING":dateString, "TCC":currentCountry, "TCC_ISO3_ALPHA":currentCountryISO3Alpha, "TCC_ISO3_NUM":currentCountryISO3Num, "MISSION":currentMission}
                rtblocks = [ ]

            if int(text.attrib.get("left")) > 350: #IDs description blocks
                rtblocks.append(text)

        if rtblocks and contributionData:
            lndata = parseMissionBlock(rtblocks, contributionData)
            ldata.extend(lndata)
    scraperwiki.sqlite.save(["DATE_STRING", "TCC_ISO3_ALPHA", "MISSION", "TYPE"], ldata)

def textContent(text):
    res = [ text.text or '' ]
    for r in text:
        res.append(r.text or '')
        res.append(r.tail or '')
    return "".join(res)

Ldescs = ["Contingent Troop", "Experts on Mission", "Formed Police Units", "Individual Police",
          'Military Observer', 'Troop', 'Police', 'Civilian Police' ]

def parseMissionBlock(rtblocks, data):
    descs = [ r  for r in rtblocks  if r.text and 380 <= int(r.attrib.get("left")) <=470 ]
    lndata = [ ]
    xx = "\n".join(lxml.etree.tostring(r)  for r in rtblocks)
    for d in descs:
        top = int(d.attrib.get("top"))
        drow = [ (int(r.attrib.get("left")), textContent(r))  for r in rtblocks  \
                    if r.text and top-2<=int(r.attrib.get("top"))<=top+2 ]
        drow.sort()
        np = [ int(lnp[1].replace(",", ""))  for lnp in drow[1:] ]
        desc = drow[0][1]
        if desc not in Ldescs:
            print "Unknown job description", desc
            print xx
            print data
            print drow
            assert False, desc
        if len(drow) == 2:
            assert data["year"] <= "2009" or data["urlEnd"] in ['may12_3.pdf']
            ndata = { "desc":desc, "people":np[0] }
        elif len(drow) == 4:
            ndata = { "TYPE":desc, "M":np[0], "F":np[1], "T":np[2] }
        elif len(drow) == 1:
            assert data["urlEnd"] in ['jul11_3.pdf', 'dec11_3.pdf', 'jun11_3.pdf', 'oct_3.pdf', 'may12_3.pdf'], (xx, data)
            ndata = None
        else:
            assert False, xx
        if ndata:
            ndata.update(data)
            lndata.append(ndata)
    return lndata

Main()import scraperwiki
import urllib2, urlparse
import lxml.html, lxml.etree
import re
import calendar
from datetime import datetime


url = "http://www.un.org/en/peacekeeping/contributors/2013/jul13_3.pdf"
pdfdata = urllib2.urlopen(url).read()
print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
root = lxml.etree.fromstring(xmldata)
print "After converting to xml it has %d bytes" % len(xmldata)
print "The first 2000 characters are: ", xmldata[:2000]

mlnk = re.search("contributors/(\d\d\d\d)/(.*?_3.pdf)", url)
urlEnd = mlnk.group(2)
mnz = re.match("(...).*?(?:\d\d)?(\d\d)?_3.pdf", urlEnd)
m3 = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
iso3Alpha = {"Aruba":"ABW","Afghanistan":"AFG","Angola":"AGO","Anguilla":"AIA","Aland Islands":"ALA","Albania":"ALB","Andorra":"AND","United Arab Emirates":"ARE","Argentina":"ARG","Armenia":"ARM","American Samoa":"ASM","Antarctica":"ATA","French Southern Territories":"ATF","Antigua and Barbuda":"ATG","Australia":"AUS","Austria":"AUT","Azerbaijan":"AZE","Burundi":"BDI","Belgium":"BEL","Benin":"BEN","Bonaire Sint Eustatius and Saba":"BES","Burkina Faso":"BFA","Bangladesh":"BGD","Bulgaria":"BGR","Bahrain":"BHR","Bahamas":"BHS","Bosnia and Herzegovina":"BIH","Saint Barthelemy":"BLM","Belarus":"BLR","Belize":"BLZ","Bermuda":"BMU","Bolivia":"BOL","Brazil":"BRA","Barbados":"BRB","Brunei":"BRN","Bhutan":"BTN","Bouvet Island":"BVT","Botswana":"BWA","Central African Republic":"CAF","Canada":"CAN","Cocos (Keeling) Islands":"CCK","Switzerland":"CHE","Chile":"CHL","China":"CHN","Cote d Ivoire":"CIV","Cameroon":"CMR","DR Congo":"COD","Congo":"COG","Cook Islands":"COK","Colombia":"COL","Comoros":"COM","Cape Verde":"CPV","Costa Rica":"CRI","Cuba":"CUB","Curacao":"CUW","Christmas Island":"CXR","Cayman Islands":"CYM","Cyprus":"CYP","Czech Republic":"CZE","Germany":"DEU","Djibouti":"DJI","Dominica":"DMA","Denmark":"DNK","Dominican Republic":"DOM","Algeria":"DZA","Ecuador":"ECU","Egypt":"EGY","Eritrea":"ERI","Western Sahara":"ESH","Spain":"ESP","Estonia":"EST","Ethiopia":"ETH","Finland":"FIN","Fiji":"FJI","Falkland Islands (Malvinas)":"FLK","France":"FRA","Faroe Islands":"FRO","Micronesia Federated States of":"FSM","Gabon":"GAB","United Kingdom":"GBR","Georgia":"GEO","Guernsey":"GGY","Ghana":"GHA","Gibraltar":"GIB","Guinea":"GIN","Guadeloupe":"GLP","Gambia":"GMB","Guinea-Bissau":"GNB","Equatorial Guinea":"GNQ","Greece":"GRC","Grenada":"GRD","Greenland":"GRL","Guatemala":"GTM","French Guiana":"GUF","Guam":"GUM","Guyana":"GUY","Hong Kong":"HKG","Heard Island and McDonald Islands":"HMD","Honduras":"HND","Croatia":"HRV","Haiti":"HTI","Hungary":"HUN","Indonesia":"IDN","Isle of Man":"IMN","India":"IND","British Indian Ocean Territory":"IOT","Ireland":"IRL","Iran":"IRN","Iraq":"IRQ","Iceland":"ISL","Israel":"ISR","Italy":"ITA","Jamaica":"JAM","Jersey":"JEY","Jordan":"JOR","Japan":"JPN","Kazakhstan":"KAZ","Kenya":"KEN","Kyrgyzstan":"KGZ","Cambodia":"KHM","Kiribati":"KIR","Saint Kitts and Nevis":"KNA","Republic of Korea":"KOR","Kuwait":"KWT","Lao People's Democratic Republic":"LAO","Lebanon":"LBN","Liberia":"LBR","Libya":"LBY","Saint Lucia":"LCA","Liechtenstein":"LIE","Sri Lanka":"LKA","Lesotho":"LSO","Lithuania":"LTU","Luxembourg":"LUX","Latvia":"LVA","The former Yugoslav Republic of Macedoniaao":"MAC","Saint Martin (French part)":"MAF","Morocco":"MAR","Monaco":"MCO","Moldova, Republic of":"MDA","Madagascar":"MDG","Maldives":"MDV","Mexico":"MEX","Marshall Islands":"MHL","The former Yugoslav Republic of Macedonia":"MKD","Macedonia, FYROM":"MKD","Mali":"MLI","Malta":"MLT","Myanmar":"MMR","Montenegro":"MNE","Mongolia":"MNG","Northern Mariana Islands":"MNP","Mozambique":"MOZ","Mauritania":"MRT","Montserrat":"MSR","Martinique":"MTQ","Mauritius":"MUS","Malawi":"MWI","Malaysia":"MYS","Mayotte":"MYT","Namibia":"NAM","New Caledonia":"NCL","Niger":"NER","Norfolk Island":"NFK","Nigeria":"NGA","Nicaragua":"NIC","Niue":"NIU","Netherlands":"NLD","Norway":"NOR","Nepal":"NPL","Nauru":"NRU","New Zealand":"NZL","Oman":"OMN","Pakistan":"PAK","Panama":"PAN","Pitcairn":"PCN","Peru":"PER","Philippines":"PHL","Palau":"PLW","Papua New Guinea":"PNG","Poland":"POL","Puerto Rico":"PRI","Korea Democratic People's Republic of":"PRK","Portugal":"PRT","Paraguay":"PRY","Palestine State of":"PSE","French Polynesia":"PYF","Qatar":"QAT","Reunion":"REU","Romania":"ROU","Russian Federation":"RUS","Rwanda":"RWA","Saudi Arabia":"SAU","Sudan":"SDN","Senegal":"SEN","Singapore":"SGP","South Georgia and the South Sandwich Islands":"SGS","Saint Helena Ascension and Tristan da Cunha":"SHN","Svalbard and Jan Mayen":"SJM","Solomon Islands":"SLB","Sierra Leone":"SLE","El Salvador":"SLV","San Marino":"SMR","Somalia":"SOM","Saint Pierre and Miquelon":"SPM","Serbia":"SRB","South Sudan":"SSD","Sao Tome and Principe":"STP","Suriname":"SUR","Slovakia":"SVK","Slovenia":"SVN","Sweden":"SWE","Swaziland":"SWZ","Sint Maarten (Dutch part)":"SXM","Seychelles":"SYC","Syrian Arab Republic":"SYR","Turks and Caicos Islands":"TCA","Chad":"TCD","Togo":"TGO","Thailand":"THA","Tajikistan":"TJK","Tokelau":"TKL","Turkmenistan":"TKM","Timor-Leste":"TLS","Tonga":"TON","Trinidad and Tobago":"TTO","Tunisia":"TUN","Turkey":"TUR","Tuvalu":"TUV","Taiwan Province of China":"TWN","Tanzania, United Republic of":"TZA","Uganda":"UGA","Ukraine":"UKR","United States Minor Outlying Islands":"UMI","Uruguay":"URY","United States of America":"USA","Uzbekistan":"UZB","Holy See (Vatican City State)":"VAT","Saint Vincent and the Grenadines":"VCT","Venezuela Bolivarian Republic of":"VEN","Virgin Islands British":"VGB","Virgin Islands U.S.":"VIR","Viet Nam":"VNM","Vanuatu":"VUT","Wallis and Futuna":"WLF","Samoa":"WSM","Yemen":"YEM","South Africa":"ZAF","Zambia":"ZMB","Zimbabwe":"ZWE"}
iso3Num = {"Afghanistan":"004","Albania":"008","Antarctica":"010","Algeria":"012","American Samoa":"016","Andorra":"020","Angola":"024","Antigua and Barbuda":"028","Azerbaijan":"031","Argentina":"032","Australia":"036","Austria":"040","Bahamas":"044","Bahrain":"048","Bangladesh":"050","Armenia":"051","Barbados":"052","Belgium":"056","Bermuda":"060","Bhutan":"064","Bolivia":"068","Bosnia and Herzegovina":"070","Botswana":"072","Bouvet Island":"074","Brazil":"076","Belize":"084","British Indian Ocean Territory":"086","Solomon Islands":"090","Virgin Islands British":"092","Brunei":"096","Bulgaria":"100","Myanmar":"104","Burundi":"108","Belarus":"112","Cambodia":"116","Cameroon":"120","Canada":"124","Cape Verde":"132","Cayman Islands":"136","Central African Republic":"140","Sri Lanka":"144","Chad":"148","Chile":"152","China":"156","Taiwan Province of China":"158","Christmas Island":"162","Cocos (Keeling) Islands":"166","Colombia":"170","Comoros":"174","Mayotte":"175","Congo":"178","DR Congo":"180","Cook Islands":"184","Costa Rica":"188","Croatia":"191","Cuba":"192","Cyprus":"196","Czech Republic":"203","Benin":"204","Denmark":"208","Dominica":"212","Dominican Republic":"214","Ecuador":"218","El Salvador":"222","Equatorial Guinea":"226","Ethiopia":"231","Eritrea":"232","Estonia":"233","Faroe Islands":"234","Falkland Islands (Malvinas)":"238","South Georgia and the South Sandwich Islands":"239","Fiji":"242","Finland":"246","Aland Islands":"248","France":"250","French Guiana":"254","French Polynesia":"258","French Southern Territories":"260","Djibouti":"262","Gabon":"266","Georgia":"268","Gambia":"270","Palestine":"275","Germany":"276","Ghana":"288","Gibraltar":"292","Kiribati":"296","Greece":"300","Greenland":"304","Grenada":"308","Guadeloupe":"312","Guam":"316","Guatemala":"320","Guinea":"324","Guyana":"328","Haiti":"332","Heard Island and McDonald Islands":"334","Holy See":"336","Honduras":"340","Hong Kong":"344","Hungary":"348","Iceland":"352","India":"356","Indonesia":"360","Iran":"364","Iraq":"368","Ireland":"372","Israel":"376","Italy":"380","Cote d Ivoire":"384","Jamaica":"388","Japan":"392","Kazakhstan":"398","Jordan":"400","Kenya":"404","Korea Democratic People's Republic of":"408","Republic of Korea":"410","Kuwait":"414","Kyrgyzstan":"417","Lao People's Democratic Republic":"418","Lebanon":"422","Lesotho":"426","Latvia":"428","Liberia":"430","Libya":"434","Liechtenstein":"438","Lithuania":"440","Luxembourg":"442","Macao":"446","Madagascar":"450","Malawi":"454","Malaysia":"458","Maldives":"462","Mali":"466","Malta":"470","Martinique":"474","Mauritania":"478","Mauritius":"480","Mexico":"484","Monaco":"492","Mongolia":"496","Moldova, Republic of":"498","Montenegro":"499","Montserrat":"500","Morocco":"504","Mozambique":"508","Oman":"512","Namibia":"516","Nauru":"520","Nepal":"524","Netherlands":"528","Curacao":"531","Aruba":"533","Sint Maarten":"534","Bonaire Sint Eustatius and Saba":"535","New Caledonia":"540","Vanuatu":"548","New Zealand":"554","Nicaragua":"558","Niger":"562","Nigeria":"566","Niue":"570","Norfolk Island":"574","Norway":"578","Northern Mariana Islands":"580","United States Minor Outlying Islands":"581","Micronesia Federated States of":"583","Marshall Islands":"584","Palau":"585","Pakistan":"586","Panama":"591","Papua New Guinea":"598","Paraguay":"600","Peru":"604","Philippines":"608","Pitcairn":"612","Poland":"616","Portugal":"620","Guinea-Bissaua":"624","Timor-Leste":"626","Puerto Rico":"630","Qatar":"634","Reunion":"638","Romania":"642","Russian Federation":"643","Rwanda":"646","Saint Barthalemy":"652","Saint Helena Ascension and Tristan da Cunha":"654","Saint Kitts and Nevis":"659","Anguilla":"660","Saint Lucia":"662","Saint Martin":"663","Saint Pierre and Miquelon":"666","Saint Vincent and the Grenadines":"670","San Marino":"674","Sao Tome and Principe":"678","Saudi Arabia":"682","Senegal":"686","Serbia":"688","Seychelles":"690","Sierra Leone":"694","Singapore":"702","Slovakia":"703","Viet Nam":"704","Slovenia":"705","Somalia":"706","South Africa":"710","Zimbabwe":"716","Spain":"724","South Sudan":"728","Sudan":"729","Western Sahara":"732","Suriname":"740","Svalbard and Jan Mayen":"744","Swaziland":"748","Sweden":"752","Switzerland":"756","Syrian Arab Republic":"760","Tajikistan":"762","Thailand":"764","Togo":"768","Tokelau":"772","Tonga":"776","Trinidad and Tobago":"780","United Arab Emirates":"784","Tunisia":"788","Turkey":"792","Turkmenistan":"795","Turks and Caicos Islands":"796","Tuvalu":"798","Uganda":"800","Ukraine":"804","The former Yugoslav Republic of Macedonia":"807","Macedonia, FYROM":"807","Egypt":"818","United Kingdom":"826","Guernsey":"831","Jersey":"832","Isle of Man":"833","Tanzania, United Republic of":"834","United States of America":"840","Virgin Islands U.S.":"850","Burkina Faso":"854","Uruguay":"858","Uzbekistan":"860","Venezuela":"862","Wallis and Futuna":"876","Samoa":"882","Yemen":"887","Zambia":"894"}
year = int(mlnk.group(1))
month = m3.index(mnz.group(1).lower())+1
day = calendar.monthrange(year, month)[1]
dateString = str(month) + '/' + str(day) + '/' + str(year-2000)
date = datetime(year, month, day).strftime('%Y%m%d')


def Main():
    # xmldata = pdftoxml(pdfdata)
    # root = lxml.etree.fromstring(xmldata)
    # print "After converting to xml it has %d bytes" % len(xmldata)
    # print "The first 2000 characters are: ", xmldata[:2000]
    #initialize varialbes
    currentCountry = None
    currentCountryISO3Num = None
    currentCountryISO3Alpha = None
    currentMission = None
    ldata = [ ]
    contributionData = None

    for page in list(root): #iterate through pages
        rtblocks = [ ] #initializes ?????
        #print lxml.etree.tostring(page)
        for text in page: #iterates through each text element
            if text.tag != "text": #checks to see if the element tag is 'text'. if not moves to next element in loop
                continue

            if 130 <= int(text.attrib.get("left")) <= 140: # IDs contributor blocks...if not, moves on
            #print lxml.etree.tostring(text)
                currentMission = None #Resets currentMission block
                currentCountry = textContent(text).strip()  #Sets current contributor to the text inside tag
                currentCountryISO3Num = iso3Num[currentCountry]
                currentCountryISO3Alpha = iso3Alpha[currentCountry]

            if 276 <= int(text.attrib.get("left")) <= 280: # IDs mission blocks...if not, moves on
                if rtblocks and contributionData: #Checks to see if  tag is already within mission and contributor block
                    lndata = parseMissionBlock(rtblocks, contributionData)
                    ldata.extend(lndata)
                currentMission = textContent(text).strip()
                contributionData = {"DATE":date, "DATE_STRING":dateString, "TCC":currentCountry, "TCC_ISO3_ALPHA":currentCountryISO3Alpha, "TCC_ISO3_NUM":currentCountryISO3Num, "MISSION":currentMission}
                rtblocks = [ ]

            if int(text.attrib.get("left")) > 350: #IDs description blocks
                rtblocks.append(text)

        if rtblocks and contributionData:
            lndata = parseMissionBlock(rtblocks, contributionData)
            ldata.extend(lndata)
    scraperwiki.sqlite.save(["DATE_STRING", "TCC_ISO3_ALPHA", "MISSION", "TYPE"], ldata)

def textContent(text):
    res = [ text.text or '' ]
    for r in text:
        res.append(r.text or '')
        res.append(r.tail or '')
    return "".join(res)

Ldescs = ["Contingent Troop", "Experts on Mission", "Formed Police Units", "Individual Police",
          'Military Observer', 'Troop', 'Police', 'Civilian Police' ]

def parseMissionBlock(rtblocks, data):
    descs = [ r  for r in rtblocks  if r.text and 380 <= int(r.attrib.get("left")) <=470 ]
    lndata = [ ]
    xx = "\n".join(lxml.etree.tostring(r)  for r in rtblocks)
    for d in descs:
        top = int(d.attrib.get("top"))
        drow = [ (int(r.attrib.get("left")), textContent(r))  for r in rtblocks  \
                    if r.text and top-2<=int(r.attrib.get("top"))<=top+2 ]
        drow.sort()
        np = [ int(lnp[1].replace(",", ""))  for lnp in drow[1:] ]
        desc = drow[0][1]
        if desc not in Ldescs:
            print "Unknown job description", desc
            print xx
            print data
            print drow
            assert False, desc
        if len(drow) == 2:
            assert data["year"] <= "2009" or data["urlEnd"] in ['may12_3.pdf']
            ndata = { "desc":desc, "people":np[0] }
        elif len(drow) == 4:
            ndata = { "TYPE":desc, "M":np[0], "F":np[1], "T":np[2] }
        elif len(drow) == 1:
            assert data["urlEnd"] in ['jul11_3.pdf', 'dec11_3.pdf', 'jun11_3.pdf', 'oct_3.pdf', 'may12_3.pdf'], (xx, data)
            ndata = None
        else:
            assert False, xx
        if ndata:
            ndata.update(data)
            lndata.append(ndata)
    return lndata

Main()