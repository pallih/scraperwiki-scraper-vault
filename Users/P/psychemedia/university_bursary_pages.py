import scraperwiki

import string,lxml.html

# A function I usually bring in with lxml that strips tags and just give you text contained in an XML substree
## via http://stackoverflow.com/questions/5757201/help-or-advice-me-get-started-with-lxml/5899005#5899005
def flatten(el):           
    result = [ (el.text or "") ]
    for sel in el:
        result.append(flatten(sel))
        result.append(sel.tail or "")
    return "".join(result)

# We want to poll through page URLs indexed by an uppercase alphachar
allTheLetters = string.uppercase

for letter in allTheLetters:
    #Generate the URL
    url="http://www.direct.gov.uk/en/EducationAndLearning/UniversityAndHigherEducation/StudentFinance/StudentfinanceA-Z/index.htm?indexChar="+letter
    print letter
    #Grab the HTML page from the URL and generate an XML object from it
    page=lxml.html.fromstring(scraperwiki.scrape(url))
    #There are probably more efficient ways of doing this scrape...
    for element in page.findall('.//div'):
        if element.find('h3')!=None and element.find('h3').text==letter:
            for uni in element.findall('.//li/a'):
                print uni.text,uni.get('href')
                scraperwiki.sqlite.save(unique_keys=["href"], data={"href":uni.get('href'), "uni":uni.text})

    