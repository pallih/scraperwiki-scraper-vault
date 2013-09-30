import scraperwiki
from lxml import etree

def innerText(element):
    if element.text:
        return element.text.replace(',', '').strip()
    else:
        # Assuming each nested element contains only one child
        return innerText(element.getchildren()[0])
    
def parse_ward(name, xml):
    root = etree.XML(xml)
        
    page1_elements = list(root.xpath('//page[@number="1"]/text[@font="3"]'))

    result = {'ward_name': name}
    result['total_pop_male'] = innerText(page1_elements[2])
    result['total_pop_female'] = innerText(page1_elements[3])
    result['total_pop_total'] = innerText(page1_elements[4])

    result['child_pop_male'] = innerText(page1_elements[6])
    result['child_pop_female'] = innerText(page1_elements[7])
    result['child_pop_total'] = innerText(page1_elements[8])

    result['working_pop_male'] = innerText(page1_elements[10])
    result['working_pop_female'] = innerText(page1_elements[11])
    result['working_pop_total'] = innerText(page1_elements[12])

    result['retired_pop_male'] = innerText(page1_elements[14])
    result['retired_pop_female'] = innerText(page1_elements[15])
    result['retired_pop_total'] = innerText(page1_elements[16])

    result['area_in_hectares'] = innerText(page1_elements[18])
    result['population_density'] = innerText(page1_elements[22])
    
    result['2011_pop_proj'] = innerText(page1_elements[27])
    result['2015_pop_proj'] = innerText(page1_elements[31])
    result['pop_change_06_15'] = innerText(page1_elements[35])
    
    page2_elements = list(root.xpath('//page[position()="2"]/text[@font="3"]'))
    
    result['unemployment_total'] = innerText(page2_elements[9])
    result['unemployment_male'] = innerText(page2_elements[13])
    result['unemployment_female'] = innerText(page2_elements[17])
    
    result['incapacity_total'] = innerText(page2_elements[22])
    result['incapacity_rate'] = innerText(page2_elements[26])
    
    result['income_support_total'] = innerText(page2_elements[30])
    result['income_support_rate'] = innerText(page2_elements[34])
    
    result['5_a_to_gcses'] = innerText(page2_elements[39])
    result['5_a_to_gcses_inc_maths'] = innerText(page2_elements[43])
    result['no_qualifications'] = innerText(page2_elements[47])
    
    page3_elements = list(root.xpath('//page[position()="3"]/text[@font="3"]'))
    result['under_18_total'] = innerText(page3_elements[15])
    result['under_18_per_1000'] = innerText(page3_elements[19])
    result['fruit_and_veg_consumption'] = innerText(page3_elements[36])
    
    return result

def get_download_link(url):
    html = scraperwiki.scrape('http://www.manchester.gov.uk' + url)
    root = etree.HTML(html)
    a = root.xpath('//div[@class="furtherInfo rounded"]//a')[0]
    return a.get('href')
    

root_url = "http://www.manchester.gov.uk/info/10020/policies_and_plans/3954/joint_strategic_needs_assessment/2"

url = "http://www.manchester.gov.uk/download/13375/manchester_joint_strategic_needs_assessment_2008-2013_ward_factsheet_ancoats_and_clayton"
#url = "http://www.manchester.gov.uk/download/13274/manchester_joint_strategic_needs_assessment_2008-2013_ward_factsheet_sharston"
#url = "http://www.manchester.gov.uk/download/13276/manchester_joint_strategic_needs_assessment_2008-2013_ward_factsheet_old_moat"
#url = "http://www.manchester.gov.uk/download/13269/manchester_joint_strategic_needs_assessment_2008-2013_ward_factsheet_miles_platting_and_newton_heath"

xml = scraperwiki.pdftoxml(scraperwiki.scrape(url))
print xml

print parse_ward("XXX", xml)

root = etree.HTML(scraperwiki.scrape(root_url))
for a in root.xpath('//div[@class="byEditor"]/ul/li/a'):
    title = a.get('title')
    print title
    
    link = get_download_link(a.get('href'))
    
    xml = scraperwiki.pdftoxml(scraperwiki.scrape(link))
    result = parse_ward(title, xml)
    
    scraperwiki.sqlite.save(['ward_name'], result)
import scraperwiki
from lxml import etree

def innerText(element):
    if element.text:
        return element.text.replace(',', '').strip()
    else:
        # Assuming each nested element contains only one child
        return innerText(element.getchildren()[0])
    
def parse_ward(name, xml):
    root = etree.XML(xml)
        
    page1_elements = list(root.xpath('//page[@number="1"]/text[@font="3"]'))

    result = {'ward_name': name}
    result['total_pop_male'] = innerText(page1_elements[2])
    result['total_pop_female'] = innerText(page1_elements[3])
    result['total_pop_total'] = innerText(page1_elements[4])

    result['child_pop_male'] = innerText(page1_elements[6])
    result['child_pop_female'] = innerText(page1_elements[7])
    result['child_pop_total'] = innerText(page1_elements[8])

    result['working_pop_male'] = innerText(page1_elements[10])
    result['working_pop_female'] = innerText(page1_elements[11])
    result['working_pop_total'] = innerText(page1_elements[12])

    result['retired_pop_male'] = innerText(page1_elements[14])
    result['retired_pop_female'] = innerText(page1_elements[15])
    result['retired_pop_total'] = innerText(page1_elements[16])

    result['area_in_hectares'] = innerText(page1_elements[18])
    result['population_density'] = innerText(page1_elements[22])
    
    result['2011_pop_proj'] = innerText(page1_elements[27])
    result['2015_pop_proj'] = innerText(page1_elements[31])
    result['pop_change_06_15'] = innerText(page1_elements[35])
    
    page2_elements = list(root.xpath('//page[position()="2"]/text[@font="3"]'))
    
    result['unemployment_total'] = innerText(page2_elements[9])
    result['unemployment_male'] = innerText(page2_elements[13])
    result['unemployment_female'] = innerText(page2_elements[17])
    
    result['incapacity_total'] = innerText(page2_elements[22])
    result['incapacity_rate'] = innerText(page2_elements[26])
    
    result['income_support_total'] = innerText(page2_elements[30])
    result['income_support_rate'] = innerText(page2_elements[34])
    
    result['5_a_to_gcses'] = innerText(page2_elements[39])
    result['5_a_to_gcses_inc_maths'] = innerText(page2_elements[43])
    result['no_qualifications'] = innerText(page2_elements[47])
    
    page3_elements = list(root.xpath('//page[position()="3"]/text[@font="3"]'))
    result['under_18_total'] = innerText(page3_elements[15])
    result['under_18_per_1000'] = innerText(page3_elements[19])
    result['fruit_and_veg_consumption'] = innerText(page3_elements[36])
    
    return result

def get_download_link(url):
    html = scraperwiki.scrape('http://www.manchester.gov.uk' + url)
    root = etree.HTML(html)
    a = root.xpath('//div[@class="furtherInfo rounded"]//a')[0]
    return a.get('href')
    

root_url = "http://www.manchester.gov.uk/info/10020/policies_and_plans/3954/joint_strategic_needs_assessment/2"

url = "http://www.manchester.gov.uk/download/13375/manchester_joint_strategic_needs_assessment_2008-2013_ward_factsheet_ancoats_and_clayton"
#url = "http://www.manchester.gov.uk/download/13274/manchester_joint_strategic_needs_assessment_2008-2013_ward_factsheet_sharston"
#url = "http://www.manchester.gov.uk/download/13276/manchester_joint_strategic_needs_assessment_2008-2013_ward_factsheet_old_moat"
#url = "http://www.manchester.gov.uk/download/13269/manchester_joint_strategic_needs_assessment_2008-2013_ward_factsheet_miles_platting_and_newton_heath"

xml = scraperwiki.pdftoxml(scraperwiki.scrape(url))
print xml

print parse_ward("XXX", xml)

root = etree.HTML(scraperwiki.scrape(root_url))
for a in root.xpath('//div[@class="byEditor"]/ul/li/a'):
    title = a.get('title')
    print title
    
    link = get_download_link(a.get('href'))
    
    xml = scraperwiki.pdftoxml(scraperwiki.scrape(link))
    result = parse_ward(title, xml)
    
    scraperwiki.sqlite.save(['ward_name'], result)
