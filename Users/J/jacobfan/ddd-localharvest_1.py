# author: Guan Ping Fan
# This is a scraper for www.localharvest.org
#
# Note: this scraper requires a proxymesh service to run successfully. recommended service to use: proxymesh.com
# Please fill the username, password in proxy_config below
#
import urlparse
import datetime
import time
import re
import cPickle
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")


# LocalHarvest Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.localharvest.org/store/'

scrape = utilities.Scrape(headers=("User-Agent", user_agent), print_log=True
            ,
            proxy_config={
                "proxies": {"http": 'http://%sus.proxymesh.com:31280'},
                #"username": "<fill your username>",
                #"password": "<fill your password>"
                "username": "jacobfan", "password": "detaseta"
            }
)

scraperwiki.sqlite.save_var("source", "localharvest.org")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


class ScrapeInfo:
    fields = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'categories',
                       'address', 'city', 'state', 'zip', 'country', 
                       'boothnum',
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'yearfounded', 'description', 'certifications', 'contactlink')

    def __init__(self, comp_url, categories_info):
        self.comp_url = comp_url
        self.categories_info = categories_info
        self.my_data = {}

    def _fillBlankInfo(self):
        for field in self.fields:
            self.my_data[field] = ""

    def _fillDateScraped(self):
        self.my_data["datescraped"] = utilities.clean(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))

    def _fillSourceUrl(self):
        self.my_data["sourceurl"] = self.comp_url

    def _fetchSourcePage(self):
        html_content = scrape(self.comp_url)
        self.root = utilities.as_lxml_node(html_content, encoding="windows-1252")
        self.html_content = html_content

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

    def _fillFirstLastName(self, value_text):
        self.my_data.update(utilities.parse_first_last_name(value_text, 1))

    def _matchAndExtractSubText(self, pattern, text, field_name, require_split_n_clean=False):
        matched_obj = re.search(pattern, text)
        if matched_obj:
            if require_split_n_clean:
                self.my_data[field_name] = utilities.split_and_clean(matched_obj.group(1))
            else:
                self.my_data[field_name] = utilities.clean(matched_obj.group(1))
        return matched_obj

    def _fillNonBlankInfo(self):
        self._fillDateScraped()
        self._fillSourceUrl()
        
        self.my_data["companyname"] = utilities.extract_text(self.root, "#listingbody h1")
        
        self._fillDescription()

        for subhead_g_node in self.root.cssselect("font.subhead_g"):
            subhead_text = utilities.extract_node_text(subhead_g_node)
            if subhead_text == "Location":
                p_node = subhead_g_node.getnext()
                assert p_node.tag == "p", "Unexpected node under 'Location'. %s" % self.comp_url
                location_text = utilities.extract_multiple_line_text(p_node)
                location_text = re.sub(r"\[.*get directions.*\]", "", location_text).strip()
                addresses = [address.strip() for address in location_text.split("\n")]
                self._processAddresses(addresses)
            elif subhead_text == "Contact Information":
                p_node = subhead_g_node.getnext()
                for script_node in p_node.cssselect("script"):
                    script_node.getparent().remove(script_node)
                assert p_node.tag == "p", "Unexpected node under 'Contact Information'. %s" % self.comp_url
                self._fillFirstLastName(p_node)

                a_nodes = p_node.cssselect("a")
                for a_node in a_nodes:
                    if not a_node.cssselect("img"):
                        self.my_data["website"] = urlparse.urljoin(self.comp_url, a_node.get("href"))

                #print "P_NODE_T:", utilities.extract_node_text(p_node)
                matched_obj = re.search(r"\s+(\(?\d{2,3}\)?)?\s*[0-9]+[0-9\-]+", utilities.extract_node_text(p_node))
                if matched_obj:
                    self.my_data["phonenumber"] = utilities.clean(matched_obj.group(0))

        self._fillContactLink()

        # Fill categories
        maincategory, categories = [], []
        for _maincategory, _category in self.categories_info:
            maincategory.append(_maincategory)
            categories.append(_category)
        self.my_data["maincategory"] = ",".join(utilities.clean_list(utilities.list_distinct(maincategory)))
        self.my_data["categories"] = ",".join(utilities.clean_list(utilities.list_distinct(categories)))

    def _fillFirstLastName(self, p_node):
        p_node_text = utilities.extract_multiple_line_text(p_node)
        contact_name_line = [utilities.clean(line) for line in p_node_text.split("\n")][0]
        #print "CONTACT_LINE:", contact_name_line
        name_titles = contact_name_line.split(",")
        if len(name_titles) == 2:
            full_name_text = name_titles[0]
            title = name_titles[1]
        elif len(name_titles) == 1:
            full_name_text = name_titles[0]
            title = ""
        else:
            raise Exception("failed to parse contact line: %r, %s" % (contact_name_line, self.comp_url))

        parsed_names = []
        for name in re.split(r" or | and |\&", full_name_text):
            parsed_names.append(utilities.parse_first_last_name(name, 1))
        #print "PARSED_NAMES:", parsed_names
        if len(parsed_names) > 1:
            last_name = None
            for parsed_name in parsed_names:
                last_name = parsed_name.get("contact1last", None)
            if last_name:
                for parsed_name in parsed_names:
                    if not parsed_name.get("contact1last", None):
                        parsed_name["contact1last"] = last_name
        cnt = 0
        for parsed_name in parsed_names:
            cnt += 1
            self.my_data["contact%dfirst" % cnt] = parsed_name["contact1first"]
            self.my_data["contact%dlast" % cnt] = parsed_name.get("contact1last", "")
            self.my_data["contact%dtitle" % cnt] = title

    def _fillContactLink(self):
        matched_obj = re.search(r"postemail\.jsp\!id\=(\d+)", self.html_content)
        if matched_obj:
            postemail_link = "http://www.localharvest.org/postemail.jsp?id=" + matched_obj.group(1)
            self.my_data["contactlink"] = postemail_link
        else:
            raise Exception("'Email Us' not found on %s" % self.com_url)

    def _fillDescription(self):
        description_nodes = self.root.xpath("//table//tr//td[@width='320']//p[@style='margin-top:0px']")
        assert len(description_nodes) == 1, "can't find description on: %s" % self.comp_url
        description1 = utilities.extract_multiple_line_text(description_nodes[0])
        description1 = re.sub(r"\(more\.{3}\)", "", description1)
        more_nodes = [a_node for a_node in description_nodes[0].cssselect("a") if "more..." in utilities.extract_node_text(a_node)]
        if more_nodes:
            description2 = self._getDescriptionPage2(more_nodes)
        else:
            description2 = ""
        description = "\n\n".join([description1, description2])
        self.my_data["description"] = description

    def _getDescriptionPage2(self, more_nodes):
        next_page_url = urlparse.urljoin(self.comp_url, more_nodes[0].get('href'))
        html_content = scrape(next_page_url)
        root = utilities.as_lxml_node(html_content, encoding="windows-1252")
        description_nodes = root.xpath("//table//tr//td[@width='320']//p[@style='margin-top:0px']")
        description = utilities.extract_multiple_line_text(description_nodes[0])
        return description

    def __call__(self):
        self._fetchSourcePage()
        self._fillBlankInfo()
        self._fillNonBlankInfo()
        self.saveData()

    def saveData(self):
        #print my_data
        scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=dict(self.my_data))


STORE_INFO = {}


def save_store_info(top_category, sub_category, store_link):
    info_value = STORE_INFO.setdefault(store_link, {})
    info_value[(top_category, sub_category)] = 1

def scrape_sub_category(top_category, sub_category, sub_category_link):
    # TODO: page through 
    #print top_category, sub_category, sub_category_link
    html_content = scrape(sub_category_link)
    if html_content:
        root = utilities.as_lxml_node(html_content, encoding="windows-1252")
        for a_node in root.cssselect("td font.txt0 a"):
            a_node_href = a_node.get("href")
            if re.match(r"\/store\/M\d+", a_node_href):
                save_store_info(top_category, sub_category, urlparse.urljoin(sub_category_link, a_node_href))

def scrape_top_category(top_category, top_category_link):
    IGNORE_LIST = ("CSA Subscriptions", "Flowers", "Local Foods")
    if top_category in IGNORE_LIST:
        return
    #print top_category, top_category_link
    html_content = scrape(top_category_link)
    root = utilities.as_lxml_node(html_content, encoding="windows-1252")
    p_txt0_nodes = root.cssselect("td p.txt0")
    #assert len(p_txt0_nodes) == 1, "Failed to find sub categories: %s" % top_category_link
    for p_txt0_node in p_txt0_nodes:
        for a_node in p_txt0_node.cssselect("a"):
            a_node_href = a_node.get("href")
            if re.search(r"\.jsp\?q\=.+", a_node_href):
                scrape_sub_category(top_category, utilities.extract_node_text(a_node), 
                            urlparse.urljoin(top_category_link, a_node_href))


def get_listing_url_from_store_url(store_url):
    html_content = scrape(store_url)
    root = utilities.as_lxml_node(html_content, encoding="windows-1252")
    listing_url = None
    for a_node in root.cssselect("p.txt1 a"):
        if utilities.extract_node_text(a_node) == "Visit our Listing":
            listing_url = urlparse.urljoin(store_url, a_node.get("href"))
            break
    if not listing_url:
        raise Exception("Failed to find listing_url on: %s" % store_url)
    else:
        return listing_url

def scrape_site(s_url):
    global STORE_INFO
    print 
    if scraperwiki.sqlite.get_var("scraping_status", None) != "STORE_INFO_READY":
        scraperwiki.sqlite.save_var("scraping_status", "BEGIN")
        html_content = scrape(s_url)
        root = utilities.as_lxml_node(html_content, encoding="windows-1252")
        for a_node in root.cssselect("#navlist li a"):
            top_category = utilities.extract_node_text(a_node)
            top_category_link = urlparse.urljoin(s_url, a_node.get("href"))
            scrape_top_category(top_category, top_category_link)
        scraperwiki.sqlite.save_var("STORE_INFO", cPickle.dumps(STORE_INFO))
        scraperwiki.sqlite.save_var("scraping_status", "STORE_INFO_READY")
    else:
        STORE_INFO = cPickle.loads(scraperwiki.sqlite.get_var("STORE_INFO"))
    scrape_listings()
    scraperwiki.sqlite.save_var("scraping_status", "DONE")


def scrape_listings():
    for store_url in STORE_INFO.keys():
        listing_url = get_listing_url_from_store_url(store_url)
        ScrapeInfo(listing_url, STORE_INFO[store_url].keys())()

def main():
    #scrape_top_category("Chocolate & Desserts", "http://www.localharvest.org/store/candy.jsp"); scrape_listings()
    scrape_site(s_url)
    #ScrapeInfo("http://www.localharvest.org/eichtens-hidden-acres-M6412", (('top1', 'sub1'), ('top2', 'sub2')))()
    #ScrapeInfo("http://www.localharvest.org/night-sky-farm-M20129")()
    #ScrapeInfo("http://www.localharvest.org/bayview-veggies-M25612", (('top1', 'sub1'), ('top2', 'sub2')))()
    #ScrapeInfo("http://www.localharvest.org/hamiltons-maple-syrup-M12611", (('top1', 'sub1'), ('top2', 'sub2')))()
    #ScrapeInfo("http://www.localharvest.org/bluebird-hill-farm-M17728", (('top1', 'sub1'), ('top2', 'sub2')))()

    #utilities.detect_page_encoding("http://www.localharvest.org/store/M9726")
    #utilities.detect_page_encoding("http://www.localharvest.org/store/candy.jsp")

if __name__ == "scraper":
    main()
