import scraperwiki
import lxml.html
import re

index = 0

########################################
# Provinces
########################################

# Get all the provinces
html = scraperwiki.scrape("http://www.worldgolf.com/courses/canada/")
root = lxml.html.fromstring(html)
provinces = root.cssselect("div[class='groupbody'] li > a")

# Loop provinces
province = provinces[9]
provinceURL  = province.attrib['href']
provinceName = province.text
print provinceName

########################################
# Cities
########################################

# Get all the cities for the current province
html2 = scraperwiki.scrape(provinceURL)
root2 = lxml.html.fromstring(html2)
cities = root2.cssselect("div[class='groupbody'] li > a")

# Loop cities
for city in cities:
    cityURL  = city.attrib['href']
    cityName = city.text
    print cityName

    ########################################
    # Golf Clubs
    ########################################

    # Get all the golf courses for the current city
    html3 = scraperwiki.scrape(cityURL)
    root3 = lxml.html.fromstring(html3)
    golfCourses = root3.cssselect("div[class='groupbody'] li > strong > a")

    # Loop golf courses
    for golfCourse in golfCourses:

        clubURL  = golfCourse.attrib['href']
        clubName = golfCourse.text
        print clubName

        ########################################
        # Club Details
        ########################################

        # Get the golf club details
        html4 = scraperwiki.scrape(clubURL)
        root4 = lxml.html.fromstring(html4)

        clubContact = root4.cssselect("div[class='contactswrap'] > div[class='groupbody']")
        courseInformation = clubContact[0].text_content()
        print courseInformation

        split_obj = courseInformation.strip(' \t\n\r').split('\t')

        # Address One
        clubAddressOne = ''
        if split_obj[0]:
            clubAddressOne = split_obj[0].split('\r')[0]

        # Address Two
        clubAddressTwo = ''

        # Postal Code
        clubPostcode = ''
        re_obj = re.search(r"\b[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}\b",courseInformation)
        if re_obj:
            clubPostcode = re_obj.group(0)

        # Phone Number
        clubPhone = ''
        if split_obj[2]:
            print split_obj[2]
            re_obj = re.search(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})\b", split_obj[2])
            if re_obj:
                clubPhone = re_obj.group(0)

        # Website
        clubWebsite = ''

        ########################################
        # Save all the data!
        ########################################

        index = index + 1

        data = {
            "id"           : index,
            "name"         : clubName.strip(),
            "address_one"  : clubAddressOne.strip(),
            "address_two"  : clubAddressTwo.strip(),
            "city"         : cityName.strip(),
            "province"     : provinceName.strip(),
            "postcode"     : clubPostcode.strip(),
            "phone_number" : clubPhone.strip(),
            "website"      : clubWebsite.strip()                         
        }

        scraperwiki.sqlite.save(unique_keys=['id'], table_name="golf_clubs", data=data)
import scraperwiki
import lxml.html
import re

index = 0

########################################
# Provinces
########################################

# Get all the provinces
html = scraperwiki.scrape("http://www.worldgolf.com/courses/canada/")
root = lxml.html.fromstring(html)
provinces = root.cssselect("div[class='groupbody'] li > a")

# Loop provinces
province = provinces[9]
provinceURL  = province.attrib['href']
provinceName = province.text
print provinceName

########################################
# Cities
########################################

# Get all the cities for the current province
html2 = scraperwiki.scrape(provinceURL)
root2 = lxml.html.fromstring(html2)
cities = root2.cssselect("div[class='groupbody'] li > a")

# Loop cities
for city in cities:
    cityURL  = city.attrib['href']
    cityName = city.text
    print cityName

    ########################################
    # Golf Clubs
    ########################################

    # Get all the golf courses for the current city
    html3 = scraperwiki.scrape(cityURL)
    root3 = lxml.html.fromstring(html3)
    golfCourses = root3.cssselect("div[class='groupbody'] li > strong > a")

    # Loop golf courses
    for golfCourse in golfCourses:

        clubURL  = golfCourse.attrib['href']
        clubName = golfCourse.text
        print clubName

        ########################################
        # Club Details
        ########################################

        # Get the golf club details
        html4 = scraperwiki.scrape(clubURL)
        root4 = lxml.html.fromstring(html4)

        clubContact = root4.cssselect("div[class='contactswrap'] > div[class='groupbody']")
        courseInformation = clubContact[0].text_content()
        print courseInformation

        split_obj = courseInformation.strip(' \t\n\r').split('\t')

        # Address One
        clubAddressOne = ''
        if split_obj[0]:
            clubAddressOne = split_obj[0].split('\r')[0]

        # Address Two
        clubAddressTwo = ''

        # Postal Code
        clubPostcode = ''
        re_obj = re.search(r"\b[ABCEGHJKLMNPRSTVXY]{1}\d{1}[A-Z]{1} *\d{1}[A-Z]{1}\d{1}\b",courseInformation)
        if re_obj:
            clubPostcode = re_obj.group(0)

        # Phone Number
        clubPhone = ''
        if split_obj[2]:
            print split_obj[2]
            re_obj = re.search(r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})\b", split_obj[2])
            if re_obj:
                clubPhone = re_obj.group(0)

        # Website
        clubWebsite = ''

        ########################################
        # Save all the data!
        ########################################

        index = index + 1

        data = {
            "id"           : index,
            "name"         : clubName.strip(),
            "address_one"  : clubAddressOne.strip(),
            "address_two"  : clubAddressTwo.strip(),
            "city"         : cityName.strip(),
            "province"     : provinceName.strip(),
            "postcode"     : clubPostcode.strip(),
            "phone_number" : clubPhone.strip(),
            "website"      : clubWebsite.strip()                         
        }

        scraperwiki.sqlite.save(unique_keys=['id'], table_name="golf_clubs", data=data)
