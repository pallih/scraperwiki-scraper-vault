# author: Guan Ping Fan
# This is a scraper for organic-market.info
import urlparse
import datetime
import time
import re
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")

# OrganicMarket Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.organic-market.info/web/Organic_Links/Organic_manufacturers/166/6/0/0.html'


scraperwiki.sqlite.save_var("source", "organic-market.info")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


class ScrapeInfo:
    fields = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'maincategory', 'categories',
                       'address', 'address2', 'city', 'state', 'zip', 'country', 
                       'boothnum',
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'contact3first', 'contact3last', 'contact3title',
                       'yearfounded', 'description', 'certifications', 'contactlink')

    def __init__(self, list_url, td_nodes):
        self.list_url = list_url
        self.td_nodes = td_nodes
        self.my_data = {}

    def _fillBlankInfo(self):
        for field in self.fields:
            self.my_data[field] = ""

    def _fillDateScraped(self):
        self.my_data["datescraped"] = utilities.clean(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))

    def _fillSourceUrl(self):
        self.my_data["sourceurl"] = self.source_page_url

    def _fillCompanyName(self):
        companyname = utilities.clean(self.source_page_link_node.text_content())
        self.my_data["companyname"] = companyname

    def _fillFirstLastName(self, value_text):
        names = value_text.split()
        if len(names) == 1:
            self.my_data["contact1first"] = names[0]
        elif len(names) == 2:
            self.my_data["contact1first"], self.my_data["contact1last"] = names
        elif len(names) > 2:
            # just use first name and last name?
            self.my_data["contact1first"] = names[0]
            self.my_data["contact1last"] = names[-1]

    def _extractSVANode(self):
        for dl_node in self.sva_node.cssselect("dl"):
            label_text = utilities.extract_text(dl_node, "dt")
            value_text = utilities.extract_text(dl_node, "dd")
            if label_text == "Contact:":
                self._fillFirstLastName(value_text)
            elif label_text == "Postcode:":
                self.my_data["zip"] = value_text
            elif label_text == "Phone:":
                self.my_data["phonenumber"] = value_text
            elif label_text == "Street:":
                self.my_data["address"] = value_text
            elif label_text == "City:":
                self.my_data["city"] = value_text
            elif label_text == "E-Mail:":
                onclick_script = dl_node.cssselect("dd img")[0].get("onclick")
                m = re.search(r"window\.open\(\'([^\']+)\'", onclick_script)
                contactlink = urlparse.urljoin(self.list_url, m.group(1))
                self.my_data["contactlink"] = contactlink
            elif label_text == "Webpage:":
                self.my_data["website"] = value_text

    def _extractDescription(self):
        for p_desc_head in self.source_page_root.cssselect("p.desc_head"):
            desc_head_text = utilities.clean(p_desc_head.text_content())
            if "Description" in desc_head_text and "english" in desc_head_text:
                description_text = utilities.extract_multiple_line_text(p_desc_head.getparent())
                description_text = re.sub(r"Description\s*\(english\)\:", "", description_text).strip()
                self.my_data["description"] = description_text

    def _fillNonBlankInfo(self):
        self._fillDateScraped()
        self._fillCompanyName()
        self._fillSourceUrl()
        self._extractSVANode()
        self._extractDescription()

    def _fetchSourcePage(self):
        import lxml.html
        self.source_page_link_node = self.td_nodes[1].cssselect("a")[0]
        self.source_page_url = urlparse.urljoin(self.list_url, self.source_page_link_node.get("href"))
        retry_times = 0
        while True:
            try:
                html_content = utilities.scrape(self.source_page_url)
                break
            except:
                if retry_times < 3:
                    time.sleep(3)
                else:
                    raise
        self.source_page_root = utilities.as_lxml_node(html_content, encoding="windows-1252")
        self.sva_node = self.source_page_root.cssselect("div.single_view_address")[0]

    def __call__(self):
        self._fetchSourcePage()
        self._fillBlankInfo()
        self._fillNonBlankInfo()
        self.saveData()

    def saveData(self):
        #print my_data
        scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=dict(self.my_data))


def scrape_site(s_url):
        html_content = utilities.scrape(s_url)
        # Parse List Items
        root = utilities.as_lxml_node(html_content, encoding="windows-1252")
        item_rows = root.xpath("//form[@name='address_list']//tr")
        valid_row_found = False
        count = 0
        for item_row in item_rows:
            count += 1
            print "Processing:%s/%s" % (count, len(item_rows))
            td_nodes = item_row.cssselect("td")
            if len(td_nodes) == 3 and td_nodes[1].cssselect("a"):
                ScrapeInfo(s_url, td_nodes)()
                valid_row_found = True
            time.sleep(0.3)
        if not valid_row_found:
            raise Exception("Found No Item on the List Page. Please check the scraper")


def main():
    scrape_site(s_url)

if __name__ == "scraper":
    main()
# author: Guan Ping Fan
# This is a scraper for organic-market.info
import urlparse
import datetime
import time
import re
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")

# OrganicMarket Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.organic-market.info/web/Organic_Links/Organic_manufacturers/166/6/0/0.html'


scraperwiki.sqlite.save_var("source", "organic-market.info")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


class ScrapeInfo:
    fields = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'maincategory', 'categories',
                       'address', 'address2', 'city', 'state', 'zip', 'country', 
                       'boothnum',
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'contact3first', 'contact3last', 'contact3title',
                       'yearfounded', 'description', 'certifications', 'contactlink')

    def __init__(self, list_url, td_nodes):
        self.list_url = list_url
        self.td_nodes = td_nodes
        self.my_data = {}

    def _fillBlankInfo(self):
        for field in self.fields:
            self.my_data[field] = ""

    def _fillDateScraped(self):
        self.my_data["datescraped"] = utilities.clean(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))

    def _fillSourceUrl(self):
        self.my_data["sourceurl"] = self.source_page_url

    def _fillCompanyName(self):
        companyname = utilities.clean(self.source_page_link_node.text_content())
        self.my_data["companyname"] = companyname

    def _fillFirstLastName(self, value_text):
        names = value_text.split()
        if len(names) == 1:
            self.my_data["contact1first"] = names[0]
        elif len(names) == 2:
            self.my_data["contact1first"], self.my_data["contact1last"] = names
        elif len(names) > 2:
            # just use first name and last name?
            self.my_data["contact1first"] = names[0]
            self.my_data["contact1last"] = names[-1]

    def _extractSVANode(self):
        for dl_node in self.sva_node.cssselect("dl"):
            label_text = utilities.extract_text(dl_node, "dt")
            value_text = utilities.extract_text(dl_node, "dd")
            if label_text == "Contact:":
                self._fillFirstLastName(value_text)
            elif label_text == "Postcode:":
                self.my_data["zip"] = value_text
            elif label_text == "Phone:":
                self.my_data["phonenumber"] = value_text
            elif label_text == "Street:":
                self.my_data["address"] = value_text
            elif label_text == "City:":
                self.my_data["city"] = value_text
            elif label_text == "E-Mail:":
                onclick_script = dl_node.cssselect("dd img")[0].get("onclick")
                m = re.search(r"window\.open\(\'([^\']+)\'", onclick_script)
                contactlink = urlparse.urljoin(self.list_url, m.group(1))
                self.my_data["contactlink"] = contactlink
            elif label_text == "Webpage:":
                self.my_data["website"] = value_text

    def _extractDescription(self):
        for p_desc_head in self.source_page_root.cssselect("p.desc_head"):
            desc_head_text = utilities.clean(p_desc_head.text_content())
            if "Description" in desc_head_text and "english" in desc_head_text:
                description_text = utilities.extract_multiple_line_text(p_desc_head.getparent())
                description_text = re.sub(r"Description\s*\(english\)\:", "", description_text).strip()
                self.my_data["description"] = description_text

    def _fillNonBlankInfo(self):
        self._fillDateScraped()
        self._fillCompanyName()
        self._fillSourceUrl()
        self._extractSVANode()
        self._extractDescription()

    def _fetchSourcePage(self):
        import lxml.html
        self.source_page_link_node = self.td_nodes[1].cssselect("a")[0]
        self.source_page_url = urlparse.urljoin(self.list_url, self.source_page_link_node.get("href"))
        retry_times = 0
        while True:
            try:
                html_content = utilities.scrape(self.source_page_url)
                break
            except:
                if retry_times < 3:
                    time.sleep(3)
                else:
                    raise
        self.source_page_root = utilities.as_lxml_node(html_content, encoding="windows-1252")
        self.sva_node = self.source_page_root.cssselect("div.single_view_address")[0]

    def __call__(self):
        self._fetchSourcePage()
        self._fillBlankInfo()
        self._fillNonBlankInfo()
        self.saveData()

    def saveData(self):
        #print my_data
        scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=dict(self.my_data))


def scrape_site(s_url):
        html_content = utilities.scrape(s_url)
        # Parse List Items
        root = utilities.as_lxml_node(html_content, encoding="windows-1252")
        item_rows = root.xpath("//form[@name='address_list']//tr")
        valid_row_found = False
        count = 0
        for item_row in item_rows:
            count += 1
            print "Processing:%s/%s" % (count, len(item_rows))
            td_nodes = item_row.cssselect("td")
            if len(td_nodes) == 3 and td_nodes[1].cssselect("a"):
                ScrapeInfo(s_url, td_nodes)()
                valid_row_found = True
            time.sleep(0.3)
        if not valid_row_found:
            raise Exception("Found No Item on the List Page. Please check the scraper")


def main():
    scrape_site(s_url)

if __name__ == "scraper":
    main()
