import scraperwiki
import lxml.html
import re
import StringIO

def detail_url_collection():
    regex = re.compile(".*data_id=(\d*).*")
    list_xpath = '//div[6]/div/div/ul/li/ul/li/a'
    start_url = 'http://www.orpha.net/consor/cgi-bin/Clinics_Search_Simple.php?lng=EN&LnkId=411&Typ=Pat&CnsGen=n '
    html = scraperwiki.scrape(start_url)
    root = lxml.html.fromstring(html)
    urls = root.xpath(list_xpath)
    for url in urls:
        record = {}
        record['id'] = regex.findall(url.attrib['href'])[0]
        scraperwiki.sqlite.save(unique_keys=["id"], data=record,table_name="detail_urls")   

def contents_at_xpath (xpath, tree):
    results = tree.xpath(xpath)
    ## Only deal with single hits.
    if (len(results) != 1):
        return None
    string = lxml.etree.tostring(results[0], method="text",
                                 encoding='utf-8')
    return string.strip()

def kv_xpath (key):
    return ("//tr[substring(td/text(), 1, %d) = '%s']/"
            "child::td[position()=2]" % (len(key), key))


def contents_at_xpath (xpath, tree):
    results = tree.xpath(xpath)
    ## Only deal with single hits.
    if (len(results) != 1):
        return None
    string = lxml.etree.tostring(results[0], method="text",
                                 encoding='utf-8')
    return string.strip()

## Finds the second TD in <tr><td>$key</td><td>....</td></tr>
## (Slightly brittle: don't use it with a ' in the key)
def contents_with_key (key, tree):
    return contents_at_xpath (kv_xpath (key), tree)

## Scheme: Special characters are _<something>. Ordinary characters
## are <char>rubbish
special_chars = {
    'arobase': '@',
    'tiret': '-',
    'dot': '.'
}

def image_url_to_char (url):
    pieces = url[0:len(url)-4].split("/")
    basename = pieces[len(pieces)-1]
    if basename[0] == '_':
        return special_chars.get(basename[1:], "<<%s>>" % basename[1:])
    else:
        return basename[0]

def extract_email (tree):
    results = tree.xpath(kv_xpath ("Contact secretary"))
    if len(results) != 1:
        return None;
    images = results[0].find("a").findall("img")
    bits = [image_url_to_char (img.get ("src")) for img in images]
    return ''.join(bits)

## This works through the text content, inserting \n whenever it sees
## a <br> tag.
def extract_address (tree):
    results = tree.xpath("//td[@class='adress']")
    if len(results) != 1:
        return None;
    acc = []
    acc.append (results[0].text or '')
    for child in results[0]:
        acc.append (child.text or '')
        if child.tag == 'br':
            acc.append ("\n")
        acc.append (child.tail or '')
    acc.append (results[0].tail or '')
    return ''.join(acc).strip()

def fill_details (detail):
    url = 'http://www.orpha.net/consor/cgi-bin/Clinics_Search.php?lng=EN&data_id=' + detail['id']
    html = scraperwiki.scrape(url)
    tree = lxml.etree.parse(StringIO.StringIO(html),
                            lxml.etree.HTMLParser(encoding='iso8859-1'))
    detail['name'] = contents_at_xpath ("//div[@id='content']/h1", tree)
    detail['address'] = extract_address (tree)
    detail['head'] = contents_with_key ('Head', tree)
    detail['phone1'] = contents_with_key ('Phone', tree)
    detail['phone2'] = contents_with_key ('Additional', tree)
    detail['fax'] = contents_with_key ('Fax', tree)
    detail['orpha_num'] = contents_with_key ('Orpha', tree)
    detail['age_range'] = contents_with_key ('Age range', tree)
    detail['types'] = contents_with_key ('Type(s)', tree)
    detail['sec_email'] = extract_email (tree)
    scraperwiki.sqlite.save(unique_keys=["id"], data=detail, table_name="detail_urls") 

#####

detail_list = scraperwiki.sqlite.select("* from detail_urls")
for detail in detail_list:
    fill_details (detail)

