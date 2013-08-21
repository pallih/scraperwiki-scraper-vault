# author: Guan Ping Fan
# This is a scraper for fgcoffeetalk.com

import lxml.html
import bs4
import urllib
import urllib2
import urlparse
import re
import unicodedata
import datetime
import scraperwiki


#============== Utility Functions Begin ==============

def remove_html(string):
    return re.sub("<.*?>", "", string)

def clean(string):
    return safestr(clean_without_safestr(string))

def clean_without_safestr(string):
    return final_clean(strip_non_text(remove_html(string.strip())))

def strip_non_text(string):
    return re.sub("\n|\r|&\w{3};|<.*?>",",",string)

def final_clean(string):
    return re.sub("[, ]{2,10}", ",", string)


def split_and_clean(string, delim=","):
    return delim.join([clean_without_safestr(item) for item in string.split(delim)])


def safestr(string):
    if isinstance(string, unicode):
        return unicode(unicodedata.normalize('NFKD', string).encode('ascii', 'ignore'), 'ascii')
    else:
        return string


def extract_text(root_node, cssselector, is_multiple=False, empty_if_not_exist=False, is_clean=True):
    if not is_clean:
        clean_func = lambda a: a
    else:
        clean_func = clean
    selected_nodes = root_node.cssselect(cssselector)
    if selected_nodes:
        if is_multiple:
            return [clean_func(selected_node.text_content()) for selected_node in selected_nodes]
        else:
            return clean_func(selected_nodes[0].text_content())
    elif empty_if_not_exist:
        if is_multiple:
            return []
        else:
            return ""
    else:
        raise Exception("Failed to find a node which matches: %s" % cssselector)


def limit_length(text, length):
    if len(text) > length:
        text = text[:length]
    return text


def scrape(url, params=None, headers=()):
        req = urllib2.Request(url)
        for header in headers:
            req.headers[header[0]] = header[1]
        if params:
            r = urllib2.urlopen(req, urllib.urlencode(params))
        else:
            r = urllib2.urlopen(req)
        content = r.read()
        return content

def as_lxml_node(html_content, encoding="utf-8"):
    #ud = bs4.UnicodeDammit(html_content, is_html=True)
    #root = lxml.html.fromstring(ud.unicode_markup)
    root = lxml.html.fromstring(unicode(html_content, encoding))
    return root


#============== Utility Functions End ==============


# MyFgCoffeeTalk Scraper Below

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://fgcoffeetalk.com/CoffeeTalk_Yellow_Pages_list.php'

scraperwiki.sqlite.save_var("source", "fgcoffeetalk.com")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


class ScrapeInfo:
    fields = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'maincategory', 'categories',
                       'address', 'address2', 'city', 'state', 'zip', 'country', 
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'contact3first', 'contact3last', 'contact3title',
                       'yearfounded', 'description', 'certifications', 'contactlink', 'id')

    def __init__(self, list_url, root):
        self.list_url = list_url
        self.root = root
        self.my_data = {}

    def _fillBlankInfo(self):
        for field in self.fields:
            self.my_data[field] = ""

    def _findRowNum(self):
        gridRow = self.root
        m = re.match(r"gridRow(\d+)", gridRow.get("id"))
        row_num = m.group(1)
        self.row_num = row_num

    def _fillDateScraped(self):
        self.my_data["datescraped"] = clean(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))

    def _fillSourceUrl(self):
        gridRow = self.root
        viewLink = gridRow.cssselect("a#viewLink" + self.row_num)[0]
        viewLink_url = urlparse.urljoin(self.list_url, viewLink.get("href"))
        self.my_data["sourceurl"] = viewLink_url

    def _fillCompanyName(self):
        self.my_data["companyname"] = extract_text(self.root, "span#edit%s_Name" % self.row_num)

    def _fillWebsite(self):
        self.my_data["website"] = extract_text(self.root, "span#edit%s_Web" % self.row_num)

    def _fillAddressRelated(self):
        self.my_data["city"] = extract_text(self.root, "span#edit%s_City" % self.row_num)
        self.my_data["state"] = extract_text(self.root, "span#edit%s_State" % self.row_num)
        self.my_data["country"] = "United States"

    def _fillPhoneNumber(self):
        self.my_data["phonenumber"] = extract_text(self.root, "span#edit%s_Phone" % self.row_num)

    def _fillCategory(self):
        categories = split_and_clean(extract_text(self.root, "span#edit%s_Category" % self.row_num), ",")
        self.my_data["categories"] = categories

    def _fillId(self):
        self.my_data["id"] = extract_text(self.root, "span#edit%s_id" % self.row_num)

    def _fillNonBlankInfo(self):
        self._findRowNum()
        self._fillDateScraped()
        self._fillCompanyName()
        self._fillWebsite()
        self._fillAddressRelated()
        self._fillSourceUrl()
        self._fillPhoneNumber()
        self._fillCategory()
        self._fillId()

    def __call__(self):
        self._fillBlankInfo()
        self._fillNonBlankInfo()
        self.saveData()

    def saveData(self):
        #print my_data
        scraperwiki.sqlite.save(unique_keys=['id'], data=dict(self.my_data))


def process_list_page(list_url, page, html_content):
    root = as_lxml_node(html_content)
    # Check Current Page
    print "Processing List Page:", list_url

    #Parse List Items
    gridRows = root.xpath("//table[@class='runner-toptable']//td[@class='runner-center ']//tr[starts-with(@id, 'gridRow')]")
    for gridRow in gridRows:
        ScrapeInfo(list_url, gridRow)()
    
    print extract_text(root, "span#pageOf1").replace(",", "")
    m = re.match(r"Page\s+\d+\s+of\s+(\d+)", extract_text(root, "span#pageOf1").replace(",", ""))
    total_pages = int(m.group(1))
    return page >= total_pages

def scrape_site(start_url):
    page = 1
    finished = False
    while not finished:
        url = start_url + "?goto=%s" % page
        html_content = scrape(url)
        finished = process_list_page(url, page, html_content)
        page += 1
    print "No More Pages. Finished"


def main():
    scrape_site(s_url)

if __name__ == "scraper":
    main()


