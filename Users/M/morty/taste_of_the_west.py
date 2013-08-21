import urllib2
from lxml import etree
import scraperwiki

def get_sibling_text(el, title):
    parent = el.getparent()
    return parent.xpath("string()").replace(title, '').strip().replace('\r', '').replace('\n', ', ').replace('\t', '').replace(',,', '').strip(',')

req = urllib2.urlopen("http://www.tasteofthewest.co.uk/sugarsearch.html?type=&category=&county=&desc=&search=Search")
doc = etree.HTML(req.read())

records = []
current_record = None
for strong in doc.xpath("(//table)[2]/tr/td/strong"):
    text = get_sibling_text(strong, strong.text)
    if not text:
        continue

    if strong.text == "Company name:":
        if current_record:
            records.append(current_record)
        current_record = {'name': text}
    elif strong.text == "Phone:":
        current_record['phone'] = text
    elif strong.text == "Email:":
        current_record['email'] = text
    elif strong.text == "Address:":
        current_record['address'] = text
    elif strong.text == "Fax:":
        current_record['fax'] = text
    elif strong.text == "Contact:":
        current_record['contact'] = text
    elif strong.text == "Website:":
        current_record['website'] = text
    elif strong.text == "Description:":
        current_record['description'] = text
    elif strong.text == "Type of member:":
        current_record['type'] = text
    elif strong.text.strip() == "Organic:":
        current_record['organic'] = text
    elif strong.text.strip() == "Distribution Profile:":
        current_record['distribution_profile'] = text
    elif strong.text.strip() == "Product categories:":
        current_record['product_categories'] = text
    elif strong.text.strip() == "Business Type:":
        current_record['business_type'] = text
    elif strong.text.strip() == "Services:":
        current_record['services'] = text

for r in records:
    scraperwiki.sqlite.save(['name'], r)

