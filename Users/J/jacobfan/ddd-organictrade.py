# author: Guan Ping Fan
# This is a scraper for www.usorganicproducts.com
# Usage: When you run this scraper, please check if it ends up with an output line "DONE". If not, you need to re-run it to get more data.
#        This is due to scraperwiki.com CPU limit for one scraper running.
#
import urlparse
import datetime
import re
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")

# OrganicTrade Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.usorganicproducts.com/export-cn.cfm'


scraperwiki.sqlite.save_var("source", "usorganicproducts.com")
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

    def __init__(self, list_url, comp_url):
        self.list_url = list_url
        self.comp_url = comp_url
        self.my_data = {}

    def _fillBlankInfo(self):
        for field in self.fields:
            self.my_data[field] = ""

    def _fillDateScraped(self):
        self.my_data["datescraped"] = utilities.clean(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))

    def _fillSourceUrl(self):
        self.my_data["sourceurl"] = self.comp_url

    def _fetchSourcePage(self):
        html_content = utilities.scrape(self.comp_url)
        self.root = utilities.as_lxml_node(html_content, encoding="utf-8")

    def _fillFirstLastName(self, value_text):
        self.my_data.update(utilities.parse_first_last_name(value_text, 1))

    def _fillTitle(self, value_text):
        self.my_data["contact1title"] = value_text

    def _processAddresses(self, addresses):
        assert len(addresses) <= 3, "unexpected addresses: %r, for: %s" % (addresses, self.comp_url)
        self.my_data["address"] = addresses[0]
        self.my_data["address2"] = ",".join(addresses[1:])

        matched_obj = re.match(r"(?P<city>[^\,]+)\,\s*(?P<state>[A-Z]{2})\s+(?P<zip>\d{5}(\-\d{4})?)", addresses[-1])
        if matched_obj:
            self.my_data["city"] = matched_obj.group("city")
            self.my_data["state"] = matched_obj.group("state")
            self.my_data["zip"] = matched_obj.group("zip")
        else:
            matched_obj = re.match(r".*\s+(?P<zip>\d{5}(\-\d{4})?)", addresses[-1])
            if matched_obj:
                self.my_data["zip"] = matched_obj.group("zip")
            else:
                print "Cannot match address: %s" % ("%r, for: %s" % (addresses, self.comp_url))

    def _matchAndExtractSubText(self, pattern, text, field_name, require_split_n_clean=False):
        matched_obj = re.search(pattern, text)
        if matched_obj:
            if require_split_n_clean:
                self.my_data[field_name] = utilities.split_and_clean(matched_obj.group(1))
            else:
                self.my_data[field_name] = utilities.clean(matched_obj.group(1))
        return matched_obj

    def _extractWebSites(self, container):
        # Multiple websites will be separated by comma
        container_text = utilities.clean(container.text_content())
        iter = re.finditer(r"Web site\:\s+([^\s]+)", container_text)
        self.my_data["website"] = ",".join(matched_obj.group(1) for matched_obj in iter)

    def _extractFields(self):
        container = self.root.cssselect("table blockquote dl")[0]
        self._extractWebSites(container)
        state = "BEGINING"
        addresses = []
        idx = 0
        while idx < len(container):
            child_node = container[idx]
            child_node_text = utilities.extract_node_text(child_node)
            #print state, "->", child_node_text
            if child_node.tag == "dt":
                self.my_data["companyname"] = child_node_text
                state = "AFTER_COMPNAME"
            if child_node.tag == "dd":
                if state == "AFTER_COMPNAME":
                    if not child_node_text.startswith("Secondary Company:"):
                        splitted = [utilities.clean(item) for item in child_node_text.split(",")]
                        if len(splitted) > 1:
                            title = splitted[-1]
                            name = splitted[0]
                        else:
                            name = splitted[0]
                            title = ""
                        self._fillFirstLastName(name)
                        self._fillTitle(title)
                        state = "AFTER_NAME_TITLE"
                elif state == "AFTER_NAME_TITLE":
                    if not (child_node_text.startswith("Phone:") or child_node_text.startswith("Fax:")
                            or child_node_text.startswith("E-mail:")):
                        addresses.append(child_node_text)
                    else:
                        self._processAddresses(addresses)
                        idx -= 1
                        state = "AFTER_ADDRESSES"
                elif state == "AFTER_ADDRESSES":
                    if child_node_text.startswith("Phone:") \
                        or child_node_text.startswith("Fax:") \
                        or child_node_text.startswith("E-mail:"):
                        self._matchAndExtractSubText(r"Phone\:(.*)", child_node_text, "phonenumber")
                        self._matchAndExtractSubText(r"Fax\:(.*)", child_node_text, "faxnumber")
                        self._matchAndExtractSubText(r"E\-mail\:(.*)", child_node_text, "emails")
                    else:
                        idx -= 1
                        state = "AFTER_CONTACT_INFO"
                elif state == "AFTER_CONTACT_INFO":
                    self.my_data["description"] = child_node_text
                    state = "AFTER_DESC"
                elif state == "AFTER_DESC":
                    if "Business Type:" in child_node_text:
                        business_types = []
                        search_words = []
                        below_search_words = False
                        child_node_text_lines = utilities.extract_multiple_line_text(child_node).split("\n")
                        for line in child_node_text_lines:
                            line = line.strip()
                            if line.startswith("Business Type:"):
                                business_types.append(line[len("Business Type:"):].strip())
                                below_search_words = False
                            elif line.startswith("Search Words"):
                                below_search_words = True
                            elif below_search_words and line:
                                search_words.append(utilities.split_and_clean(line.strip()))
                        self.my_data["maincategory"] = ",".join(business_types)
                        self.my_data["categories"] = ",".join(search_words)

                    self._matchAndExtractSubText(r"Certification\:(.*)", child_node_text, "certifications", 
                                    require_split_n_clean=True)
                    self._matchAndExtractSubText(r"Founded\:(.*)", child_node_text, "yearfounded")
                    self._matchAndExtractSubText(r"Export Regions\:(.*)", child_node_text, "exportregions")
            idx += 1



    def _fillNonBlankInfo(self):
        self._fillDateScraped()
        self._fillSourceUrl()
        self._extractFields()

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
    root = utilities.as_lxml_node(html_content, encoding="utf-8")
    link_nodes = root.cssselect("a")
    # if we stopped before complete last time, just resume from last comp_url
    last_comp_url = scraperwiki.sqlite.get_var("last_comp_url", None)
    if last_comp_url:
        found = False
        new_link_nodes = []
        for link_node in link_nodes:
            if link_node.get("href") == last_comp_url:
                found = True
            if found:
                new_link_nodes.append(link_node)
        if new_link_nodes:
            link_nodes = new_link_nodes
    for link_node in link_nodes:
        comp_url = link_node.get("href")
        scraperwiki.sqlite.save_var("last_comp_url", comp_url)
        if comp_url and re.search(r"companydetails\.cfm\?language\=English\&idnumber\=\d+", comp_url):
            comp_url = urlparse.urljoin(s_url, comp_url)
            ScrapeInfo(s_url, comp_url)()
    print "DONE"
    scraperwiki.sqlite.save_var("last_comp_url", None)

def main():
    scrape_site(s_url)
    #ScrapeInfo(s_url, "http://www.usorganicproducts.com/companydetails.cfm?language=English&idnumber=9753")()    
    #ScrapeInfo(s_url, "http://www.usorganicproducts.com/companydetails.cfm?language=English&idnumber=11301")()
    #ScrapeInfo(s_url, "http://www.usorganicproducts.com/companydetails.cfm?language=English&idnumber=7303")()

if __name__ == "scraper":
    main()

# author: Guan Ping Fan
# This is a scraper for www.usorganicproducts.com
# Usage: When you run this scraper, please check if it ends up with an output line "DONE". If not, you need to re-run it to get more data.
#        This is due to scraperwiki.com CPU limit for one scraper running.
#
import urlparse
import datetime
import re
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")

# OrganicTrade Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.usorganicproducts.com/export-cn.cfm'


scraperwiki.sqlite.save_var("source", "usorganicproducts.com")
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

    def __init__(self, list_url, comp_url):
        self.list_url = list_url
        self.comp_url = comp_url
        self.my_data = {}

    def _fillBlankInfo(self):
        for field in self.fields:
            self.my_data[field] = ""

    def _fillDateScraped(self):
        self.my_data["datescraped"] = utilities.clean(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))

    def _fillSourceUrl(self):
        self.my_data["sourceurl"] = self.comp_url

    def _fetchSourcePage(self):
        html_content = utilities.scrape(self.comp_url)
        self.root = utilities.as_lxml_node(html_content, encoding="utf-8")

    def _fillFirstLastName(self, value_text):
        self.my_data.update(utilities.parse_first_last_name(value_text, 1))

    def _fillTitle(self, value_text):
        self.my_data["contact1title"] = value_text

    def _processAddresses(self, addresses):
        assert len(addresses) <= 3, "unexpected addresses: %r, for: %s" % (addresses, self.comp_url)
        self.my_data["address"] = addresses[0]
        self.my_data["address2"] = ",".join(addresses[1:])

        matched_obj = re.match(r"(?P<city>[^\,]+)\,\s*(?P<state>[A-Z]{2})\s+(?P<zip>\d{5}(\-\d{4})?)", addresses[-1])
        if matched_obj:
            self.my_data["city"] = matched_obj.group("city")
            self.my_data["state"] = matched_obj.group("state")
            self.my_data["zip"] = matched_obj.group("zip")
        else:
            matched_obj = re.match(r".*\s+(?P<zip>\d{5}(\-\d{4})?)", addresses[-1])
            if matched_obj:
                self.my_data["zip"] = matched_obj.group("zip")
            else:
                print "Cannot match address: %s" % ("%r, for: %s" % (addresses, self.comp_url))

    def _matchAndExtractSubText(self, pattern, text, field_name, require_split_n_clean=False):
        matched_obj = re.search(pattern, text)
        if matched_obj:
            if require_split_n_clean:
                self.my_data[field_name] = utilities.split_and_clean(matched_obj.group(1))
            else:
                self.my_data[field_name] = utilities.clean(matched_obj.group(1))
        return matched_obj

    def _extractWebSites(self, container):
        # Multiple websites will be separated by comma
        container_text = utilities.clean(container.text_content())
        iter = re.finditer(r"Web site\:\s+([^\s]+)", container_text)
        self.my_data["website"] = ",".join(matched_obj.group(1) for matched_obj in iter)

    def _extractFields(self):
        container = self.root.cssselect("table blockquote dl")[0]
        self._extractWebSites(container)
        state = "BEGINING"
        addresses = []
        idx = 0
        while idx < len(container):
            child_node = container[idx]
            child_node_text = utilities.extract_node_text(child_node)
            #print state, "->", child_node_text
            if child_node.tag == "dt":
                self.my_data["companyname"] = child_node_text
                state = "AFTER_COMPNAME"
            if child_node.tag == "dd":
                if state == "AFTER_COMPNAME":
                    if not child_node_text.startswith("Secondary Company:"):
                        splitted = [utilities.clean(item) for item in child_node_text.split(",")]
                        if len(splitted) > 1:
                            title = splitted[-1]
                            name = splitted[0]
                        else:
                            name = splitted[0]
                            title = ""
                        self._fillFirstLastName(name)
                        self._fillTitle(title)
                        state = "AFTER_NAME_TITLE"
                elif state == "AFTER_NAME_TITLE":
                    if not (child_node_text.startswith("Phone:") or child_node_text.startswith("Fax:")
                            or child_node_text.startswith("E-mail:")):
                        addresses.append(child_node_text)
                    else:
                        self._processAddresses(addresses)
                        idx -= 1
                        state = "AFTER_ADDRESSES"
                elif state == "AFTER_ADDRESSES":
                    if child_node_text.startswith("Phone:") \
                        or child_node_text.startswith("Fax:") \
                        or child_node_text.startswith("E-mail:"):
                        self._matchAndExtractSubText(r"Phone\:(.*)", child_node_text, "phonenumber")
                        self._matchAndExtractSubText(r"Fax\:(.*)", child_node_text, "faxnumber")
                        self._matchAndExtractSubText(r"E\-mail\:(.*)", child_node_text, "emails")
                    else:
                        idx -= 1
                        state = "AFTER_CONTACT_INFO"
                elif state == "AFTER_CONTACT_INFO":
                    self.my_data["description"] = child_node_text
                    state = "AFTER_DESC"
                elif state == "AFTER_DESC":
                    if "Business Type:" in child_node_text:
                        business_types = []
                        search_words = []
                        below_search_words = False
                        child_node_text_lines = utilities.extract_multiple_line_text(child_node).split("\n")
                        for line in child_node_text_lines:
                            line = line.strip()
                            if line.startswith("Business Type:"):
                                business_types.append(line[len("Business Type:"):].strip())
                                below_search_words = False
                            elif line.startswith("Search Words"):
                                below_search_words = True
                            elif below_search_words and line:
                                search_words.append(utilities.split_and_clean(line.strip()))
                        self.my_data["maincategory"] = ",".join(business_types)
                        self.my_data["categories"] = ",".join(search_words)

                    self._matchAndExtractSubText(r"Certification\:(.*)", child_node_text, "certifications", 
                                    require_split_n_clean=True)
                    self._matchAndExtractSubText(r"Founded\:(.*)", child_node_text, "yearfounded")
                    self._matchAndExtractSubText(r"Export Regions\:(.*)", child_node_text, "exportregions")
            idx += 1



    def _fillNonBlankInfo(self):
        self._fillDateScraped()
        self._fillSourceUrl()
        self._extractFields()

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
    root = utilities.as_lxml_node(html_content, encoding="utf-8")
    link_nodes = root.cssselect("a")
    # if we stopped before complete last time, just resume from last comp_url
    last_comp_url = scraperwiki.sqlite.get_var("last_comp_url", None)
    if last_comp_url:
        found = False
        new_link_nodes = []
        for link_node in link_nodes:
            if link_node.get("href") == last_comp_url:
                found = True
            if found:
                new_link_nodes.append(link_node)
        if new_link_nodes:
            link_nodes = new_link_nodes
    for link_node in link_nodes:
        comp_url = link_node.get("href")
        scraperwiki.sqlite.save_var("last_comp_url", comp_url)
        if comp_url and re.search(r"companydetails\.cfm\?language\=English\&idnumber\=\d+", comp_url):
            comp_url = urlparse.urljoin(s_url, comp_url)
            ScrapeInfo(s_url, comp_url)()
    print "DONE"
    scraperwiki.sqlite.save_var("last_comp_url", None)

def main():
    scrape_site(s_url)
    #ScrapeInfo(s_url, "http://www.usorganicproducts.com/companydetails.cfm?language=English&idnumber=9753")()    
    #ScrapeInfo(s_url, "http://www.usorganicproducts.com/companydetails.cfm?language=English&idnumber=11301")()
    #ScrapeInfo(s_url, "http://www.usorganicproducts.com/companydetails.cfm?language=English&idnumber=7303")()

if __name__ == "scraper":
    main()

