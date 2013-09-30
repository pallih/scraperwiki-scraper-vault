import re
import sys
import lxml.html
import mechanize
import traceback
import scraperwiki 

def NavigateThorgills(url):
    mBrowser.open(url)
    for link in mBrowser.links(url_regex='/property/'):
        if link.url[0:1] == '/':
            propertyURL = 'http://www.thorgills.com' + link.url
        else:
            propertyURL = 'http://www.thorgills.com/' + link.url

        if not propertyURL in propertiesURLsList:
            propertiesURLsList.append(propertyURL)

def GetAllNextProperties(br):
    isThereNext = True
    while isThereNext:
        try:
            response1 = br.follow_link(text_regex=r"Next", nr=1)
        except:
             isThereNext = False
             break
        
        next_url = response1.geturl()
        if next_url:
            NavigateThorgills(next_url)
            ShowProgress("Properties Found.", len(propertiesURLsList))
        else:
            isThereNext = False

def ShowProgress(state, progress):
    sys.stdout.write("\r%d"  %progress + ' ' + state)
    sys.stdout.flush()

def ShowPercentage(x):#Display a percentage progress in console
    sys.stdout.write("\r%d%%" %x)    # or print >> sys.stdout, "\r%d%%" %i,
    sys.stdout.flush()

def ReportState(state):
    print state

def ParseNumber(str):
    if str == 'One':
        return '1'
    elif str == 'Two':
        return '2'
    elif str == 'Three':
        return '3'
    elif str == 'Four':
        return '4'
    elif str == 'Five':
        return '5'
    elif str == 'Six':
        return '6'
    elif str == 'Seven':
        return '7'
    elif str == 'Eight':
        return '8'
    elif str == 'Nine':
        return '9'
    elif str == 'Ten':
        return '10'

propertiesURLsList = []

areasNames = ('Acton','Brentford','Chiswick','Ealing','Hammersmith',
              'Hanger Lane','Hanwell','Hounslow','Isleworth',
              'Northolt','Perivale','Shepherds Bush','Southall')

startURL = 'http://www.thorgills.com/results.asp?onmap=2&displayperpage=10&view=list&displayorder=PriceAskd&pricehigh=0&pricelow=0&pricetype=3&offset=0'

mBrowser = mechanize.Browser()

ReportState("Collecting Properties URLs...")

NavigateThorgills(startURL)

ShowProgress("Properties Found.", len(propertiesURLsList))

GetAllNextProperties(mBrowser)

data = {}
counter = 0
Numbers = {'One': '1', 'Two': '2', 'Three': '3', 'Four': '4', 'Five': '5', 'Six': '6', 'Seven': '7', 'Eight': '8', 'Nine': '9', 'Ten': '10'}

#Scraping Loop...
for propertyURL in propertiesURLsList:
    counter = counter + 1
    ReportState(str(counter) + " of " + str(len(propertiesURLsList)))
    try:
        mBrowser.open(propertyURL)
        pageSource = mBrowser.response().read()
        root = lxml.html.fromstring(pageSource)

        title = root.find(".//title").text
        titleTagArr = title.split(',')

        bedrooms = ''
        matchObj = re.search(r'(\d+)\sBedroom', title)
        if matchObj:
            bedrooms = matchObj.group(1)

        bathrooms = ''
        matchObj = re.search(r'<li><strong>(.+?) Bathrooms</strong></li>', pageSource)
        if matchObj:
            res = matchObj.group(1)
            bathrooms = ParseNumber(res)

        FeaturesLst = root.xpath('//*[@id="DetailText"]/div/div[*]/span/text()')
        Features = '||'.join(FeaturesLst)

        agent_ref = ''
        postCode1 = titleTagArr[2].split('|')[0].strip()
        if postCode1 == 'W5' or postCode1 == 'W13' or postCode1 == 'W7' or postCode1 == 'W3' or postCode1 == 'UB6':
            agent_ref = '1001'
        elif  postCode1 == 'W4' or postCode1 == 'TW8' or postCode1 == 'TW7' or postCode1 == 'W6' or postCode1 == 'W12':
            agent_ref = '1002'

        images = ''
        ImagesLst = root.xpath('//*[@id="thumbs"]/ul/li[*]/a/img')
        for image in ImagesLst:
            src = image.attrib['src']
            if images == '':
                images = src
            else:
                images = images + ';' + image.attrib['src']

        AdditionalFeatures = ''
        AdditionalFeaturesLst = root.xpath('//*[@id="DetailText"]/ul/li[*]/strong')
        for feature in AdditionalFeaturesLst:
            featureDesc = feature.text
            if AdditionalFeatures == '':
                AdditionalFeatures = featureDesc
            else:
                AdditionalFeatures = AdditionalFeatures + '||' + featureDesc

        property_link = propertyURL

        price = ''
        titleHeading = root.xpath('//*[@id="detail_h1"]')
        titleHeadingStr = titleHeading[0].text
        matchObj = re.search(r'([0-9,]+) pcm', titleHeadingStr)
        if matchObj:
            price = matchObj.group(1)
        titleHeadingStrArr = titleHeadingStr.split(',')
        address1 = titleHeadingStrArr[0]
        town = titleHeadingStrArr[1]

        receptions = ''
        matchObj = re.search(r'<li><strong>([a-zA-Z]+) Reception Rooms</strong></li>', pageSource)
        if matchObj:
            receptions = ParseNumber(matchObj.group(1))
        else:
            receptions = "No"

        details_text = root.xpath('//*[@id="DetailText"]/p/text()')

        gardens = ''
        matchObj = re.search(r'<li><strong>([a-zA-Z]+) Garden</strong></li>', pageSource)
        if matchObj:
            gardens = 'Y'
        else:
            gardens = 'N'

        data.update({'let_type_id': counter, 'bathrooms': bathrooms, 'features': Features,
                     'agent_ref': agent_ref, 'images': images, 'property_link': property_link,
                     'postcode2': '', 'postcode1': postCode1, 'let_boolean': '','let_date_available': '',
                     'price': price,'let_rent_frequency': 'Price per Month','bedrooms': bedrooms,
                     'receptions': receptions, 'address1': address1, 'address2': '',
                     'address3': '', 'address4': '','details_text': details_text,
                     'town': town, 'trans_type': '2', 'gardens': gardens})
        scraperwiki.sqlite.save(unique_keys=['let_type_id'], data=data)
    except Exception, err:
        print traceback.format_exc()
# End of Scraping Loop
