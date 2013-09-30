import scraperwiki
import lxml.html

for num in range(1,202): 
    html = scraperwiki.scrape("http://www.yellowpages.co.za/hearing_aid_service/hearing_aid_service/" + str(num))
    list = lxml.html.fromstring(html).cssselect("div#results-list > div")
#    print list
    i = 0
    for el in list:
        data = {}
        i = i + 1
        data['id'] = str(num) + " - " + el.attrib['id']
        d = el.cssselect("div.resultAddressbar h2")
        if len(d) == 1:
            try: 
                data['name'] = lxml.etree.tostring(d[0], method="text", encoding=unicode)
            except UnicodeEncodeError:
                print lxml.etree.tostring(d[0])
        d = el.cssselect("div.resultAddressbar div.where")
        if len(d) == 1:
            data['address'] = lxml.etree.tostring(d[0], method="text")
        d = el.cssselect("div.details h3")
        if len(d) == 1:
            data['tel'] = lxml.etree.tostring(d[0], method="text")
        d = el.cssselect("div.details div.resultFaxBar")
        if len(d) == 1:
            data['fax'] = lxml.etree.tostring(d[0], method="text")
        d = el.cssselect("div.details div.resultEmailBar")
        if len(d) == 1:
            data['email'] = lxml.etree.tostring(d[0])
        d = el.cssselect("div.details div.resultWebsiteBar")
        if len(d) == 1:
            data['website'] = lxml.etree.tostring(d[0])
        d = el.cssselect("div.resultAddressbar > div.resultDirectionBar > a")
        if len(d) == 1:
            data['latlong'] = d[0].attrib["href"]

        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

import scraperwiki
import lxml.html

cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Patna", "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan", "Vasai", "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi Mumbai", "Allahabad", "Ranchi", "Howrah", "Coimbatore", "Jabalpur", "Gwalior", "Vijayawada", "Jodhpur", "Madurai", "Raipur-Chhattisgarh", "Kota-Rajasthan", "Guwahati", "Chandigarh", "Solapur", "Dharwad", "Bareilly", "Moradabad", "Mysore", "Gurgaon", "Aligarh", "Jalandhar", "Bhubaneshwar", "Salem", "Trivandrum", "Bhigwan", "Saharanpur", "Gorakhpur", "Guntur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai", "Warangal", "Mangalore", "Cuttack", "Firozabad", "Kochi (Cochin)", "Bhavnagar", "Dehradun", "Durgapur", "Asansol", "Nanded", "Kolhapur", "Ajmer", "Gulbarga", "Jamnagar", "Ujjain", "Siliguri", "Jhansi", "Nellore", "Jammu", "Sangli-Miraj & Kupwad", "Belgaum", "Tirunelveli", "Malegaon", "Gaya", "Jalgaon", "Udaipur-Rajasthan", "Tirupur", "Davangere", "Kozhikode", "Akola", "Kurnool", "Rajpur Sonarpur", "Bokaro", "South Dumdum", "Bellary", "Patiala", "Gopalpur", "Agartala", "Bhagalpur", "Muzaffarnagar", "Bhatapara", "Latur", "Dhule", "Rohtak", "Korba", "Bhilwara", "Brahmapur", "Muzaffarpur", "Ahmednagar", "Mathura", "Kollam (Quilon)", "Rajahmundry", "Kadapa", "Bijapur-Chhattisgarh", "Bijapur-Karnataka", "Shahjahanpur", "Rampur", "Shivamogga (Shimoga)", "Chandrapur", "Junagadh", "Thrissur", "Alwar", "Bardhaman", "Kulti", "Kakinada", "Nizamabad", "Parbhani", "Tumkur", "Hissar", "Ozhukarai", "Bihar Sharif", "Panipat", "Darbhanga", "Ballia", "Aizawl", "Dewas", "Ichalkaranji", "Tirupati", "Karnal", "Bathinda", "Jalna", "Kirari Suleman Nagar", "Purnia", "Satna", "Mau", "Sonitpur", "Farrukhabad", "Sagar", "Rourkela", "Durg", "Imphal", "Ratlam", "Hapur", "Anantapur", "Arrah", "Karimnagar", "Etawah", "North Dumdum", "Bharatpur", "Begusarai", "New Delhi", "Gandhidham", "Puducherry", "Sikar", "Thoothukudi", "Rewa", "Mirzapur", "Raichur", "Pali-Maharashtra", "Pali-Rajasthan", "Ramagundam", "Vizianagaram", "Katihar", "Haridwar", "Sri Ganganagar", "Karawal Nagar", "Nagercoil", "Bulandshahr", "Thanjavur"]

translation = {
     "jai": "address",
     "jti": "phone",
     "jfx": "fax",
     "jwi": "website",
     'unknown': 'unknown'
}

def scrapeLocationData(url):
    html = scraperwiki.scrape(url)
    list = lxml.html.fromstring(html).cssselect("section.jadtl dl")
    data = {}
    data["sourceurl"] = url
    for con in list:
        data[translation.get(con[0].attrib.get('class', 'unknown'),'unknown')] = con[1].text
    scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=data)
#    print url

def scrapeStatePageData(url):
    html = scraperwiki.scrape(url)
    list = lxml.html.fromstring(html).cssselect("span.jcn a")
#    print list[0].tag
    for el in list:
        scrapeLocationData(el.attrib['href'])
    next = lxml.html.fromstring(html).cssselect("div.jpag a")
    if next[-1].attrib.get('class', False) == False:
        scrapeStatePageData(next[-1].attrib['href'])

for city in cities: 
    scrapeStatePageData(url = "http://www.justdial.com/" + city + "/Hearing-Aid-Dealers/ct-3860/page-1")
    

#scrapeLocationData("http://www.justdial.com/Mumbai/Atharva-Speech-Hearing-Clinic-%3Cnear%3E-Opp-TBZ-Naupada-Thane-West/022PXX22-XX22-130308122953-N7L2_TXVtYmFpIEhlYXJpbmcgQWlkIERlYWxlcnM=_BZDET")




#    print list
#    i = 0
#    for el in list:
#        data = {}
#        i = i + 1
#        data['id'] = str(num) + " - " + el.attrib['id']
#        d = el.cssselect("div.resultAddressbar h2")
#        if len(d) == 1:
#            try: 
#                data['name'] = lxml.etree.tostring(d[0], method="text", encoding=unicode)
#            except UnicodeEncodeError:
#                print lxml.etree.tostring(d[0])
#        d = el.cssselect("div.resultAddressbar div.where")
#        if len(d) == 1:
#            data['address'] = lxml.etree.tostring(d[0], method="text")
#        d = el.cssselect("div.details h3")
#        if len(d) == 1:
#            data['tel'] = lxml.etree.tostring(d[0], method="text")
#        d = el.cssselect("div.details div.resultFaxBar")
#        if len(d) == 1:
#            data['fax'] = lxml.etree.tostring(d[0], method="text")
#        d = el.cssselect("div.details div.resultEmailBar")
#        if len(d) == 1:
#            data['email'] = lxml.etree.tostring(d[0])
#        d = el.cssselect("div.details div.resultWebsiteBar")
#        if len(d) == 1:
#            data['website'] = lxml.etree.tostring(d[0])
#        d = el.cssselect("div.resultAddressbar > div.resultDirectionBar > a")
#        if len(d) == 1:
#            data['latlong'] = d[0].attrib["href"]
#
#        scraperwiki.sqlite.save(unique_keys=['id'], data=data)

