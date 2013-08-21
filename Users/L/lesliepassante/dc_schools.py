import lxml.html
import scraperwiki

schools_html = scraperwiki.scrape('http://profiles.dcps.dc.gov/')

school_doc = lxml.html.fromstring(schools_html)

schools = school_doc.xpath('//tr')

school_list = []

for school in schools:
    try: 
        schooldict = {}
        schooldict["name"] = school.xpath('td')[1].xpath('h6/a[@class="schoolname"]')[0].text_content()
        schooldict["address"] = school.xpath('td')[2].text_content().replace("Washington"," Washington")
        schooldict["ward"] = school.xpath('td[@class="padleft"]/p')[0].text_content()
        schooldict["enrollment"] = school.xpath('td')[8].text_content()
        school_list.append(schooldict)
    except IndexError:
        pass


