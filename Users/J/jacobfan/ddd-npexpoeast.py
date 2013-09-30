# author: Guan Ping Fan
# This is a scraper for expoeast.com
# This is a scraper for www.usorganicproducts.com
# Usage: When you run this scraper, please check if it ends up with an output line "DONE". If not, you need to re-run it to get more data.
#        This is due to scraperwiki.com CPU limit for one scraper running.

import urlparse
import cgi
import datetime
import re
import cPickle
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")


# NPExpoEast Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.expoeast.com/expoeast2012/public/ExhibitorList.aspx?Index=All&sortMenu=107007'

scrape = utilities.Scrape(headers=("User-Agent", user_agent), print_log=True)

scraperwiki.sqlite.save_var("source", "expoeast.com")
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

    def __init__(self, comp_url):
        self.comp_url = comp_url

    def _fillBlankInfo(self):
        self.my_data = utilities.initialize_my_data(self.fields, self.comp_url)

    def _fetchSourcePage(self):
        html_content = scrape(self.comp_url)
        self.root = utilities.as_lxml_node(html_content, encoding="utf-8")

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
        booth_labels = self.root.xpath("//span[starts-with(@id, 'lblBoothLabel')]")
        if not booth_labels:
            return False
        booth_text = utilities.extract_node_text(booth_labels[0])
        self._matchAndExtractSubText(r"(\d+)", booth_text, "boothnum")
        
        self.my_data["companyname"] = utilities.extract_text(self.root, "#lblCoName", empty_if_not_exist=True)
        contact_text = utilities.extract_text(self.root, "#pnlcontactname #lblContactName",
                        empty_if_not_exist=True)
        if contact_text:
            self._fillFirstLastName(contact_text)
        self.my_data["address"] = utilities.extract_text(self.root, "#lblAdd1", empty_if_not_exist=True)
        self.my_data["address2"] = utilities.extract_text(self.root, "#lblAdd2", empty_if_not_exist=True)
        self.my_data["city"] = utilities.extract_text(self.root, "#lblCity", empty_if_not_exist=True).strip(",")
        self.my_data["state"] = utilities.extract_text(self.root, "#lblState", empty_if_not_exist=True)
        self.my_data["zip"] = utilities.extract_text(self.root, "#lblZip", empty_if_not_exist=True)
        self.my_data["country"] = utilities.extract_text(self.root, "#lblCountry", empty_if_not_exist=True)
        self.my_data["phonenumber"] = utilities.extract_text(self.root, "#lblPhone", empty_if_not_exist=True)
        self.my_data["faxnumber"] = utilities.extract_text(self.root, "#lblFax", empty_if_not_exist=True)
        for a_node in self.root.cssselect("#pnlcontactname")[0].getparent().cssselect("a"):
            if a_node.get("href"):
                if a_node.get("href") and a_node.get("href").startswith("BoothURL.aspx"):
                    self.my_data["website"] = utilities.extract_node_text(a_node)
        description_nodes = self.root.cssselect("#lblWelcome")
        if description_nodes:
            self.my_data["description"] = utilities.extract_multiple_line_text(description_nodes[0])

        self._fillMainCategoryAndCategories()

        self.my_data["contactlink"] = self.my_data["sourceurl"] + "#lblSendMailMsg"
        return True

    def _fillMainCategoryAndCategories(self):
        maincategory = []
        categories = []

        maincategory_nodes = self.root.cssselect("#lblCategories ul")
        for maincategory_node in maincategory_nodes:
            maincategory.append(utilities.extract_node_text(maincategory_node))

        category_nodes = self.root.cssselect("#lblCategories li")
        for category_node in category_nodes:
            categories.append(utilities.extract_node_text(category_node))
        
        self.my_data["maincategory"] = ",".join(maincategory)
        self.my_data["categories"] = ",".join(categories)


    def __call__(self):
        self._fetchSourcePage()
        self._fillBlankInfo()
        if self._fillNonBlankInfo():
            self.saveData()

    def saveData(self):
        #print my_data
        scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=dict(self.my_data))


def scrape_site(s_url):
    if not scraperwiki.sqlite.get_var("COMP_URLS", None):
        COMP_URLS = {}
        pagenum = 1
        done = False
        while not done:
            print "Page:", pagenum
            url = s_url + "&pagenum=%d" % pagenum
            html_content = scrape(url)
            root = utilities.as_lxml_node(html_content, encoding="utf-8")

            for a_node in root.cssselect("#tableUpgraded tr#trnode a") + root.cssselect("#tableAll tr#trnode a"):
                if a_node.get("href") and "Booth.aspx?" in a_node.get("href"):
                    comp_url = urlparse.urljoin(url, a_node.get("href"))
                    params = cgi.parse_qs(urlparse.urlparse(comp_url).query)
                    if params.has_key("BoothID"):
                        COMP_URLS[params["BoothID"][0]] = comp_url
            found_next = False
            for a_node in root.cssselect("a"):
                if a_node.get('href') and "pagingNext" in a_node.get("href") and utilities.extract_node_text(a_node) == "Next":
                    found_next = True
                    break
            done = not found_next
            pagenum += 1
        COMP_URLS = COMP_URLS.values()
        scraperwiki.sqlite.save_var("COMP_URLS", cPickle.dumps(COMP_URLS))
    else:
        COMP_URLS = cPickle.loads(scraperwiki.sqlite.get_var("COMP_URLS"))

    last_comp_url = scraperwiki.sqlite.get_var("last_comp_url", None)

    if last_comp_url:
        found = False
        NEW_COMP_URLS = []
        print "RESUME From:", last_comp_url
        for comp_url in COMP_URLS:
            if comp_url == last_comp_url:
                found = True
            if found:
                NEW_COMP_URLS.append(comp_url)
        if NEW_COMP_URLS:
            COMP_URLS = NEW_COMP_URLS

    for comp_url in COMP_URLS:
        scraperwiki.sqlite.save_var("last_comp_url", comp_url)
        ScrapeInfo(comp_url)()
    print "DONE"

def main():
    scrape_site(s_url)
    #ScrapeInfo("http://www.expoeast.com/expoeast2012/Public/Booth.aspx?IndexInList=0&FromPage=ExhibitorSearch.aspx&BoothID=1107110")()
    #ScrapeInfo("http://www.expoeast.com/expoeast2012/public/Booth.aspx?IndexInList=19&FromPage=ExhibitorList.aspx&ParentBoothID=&ListByBooth=true&BoothID=1107983")()
    #ScrapeInfo("http://www.expoeast.com/expoeast2012/public/Booth.aspx?BoothID=1107971")()


if __name__ == "scraper":
    main()
# author: Guan Ping Fan
# This is a scraper for expoeast.com
# This is a scraper for www.usorganicproducts.com
# Usage: When you run this scraper, please check if it ends up with an output line "DONE". If not, you need to re-run it to get more data.
#        This is due to scraperwiki.com CPU limit for one scraper running.

import urlparse
import cgi
import datetime
import re
import cPickle
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")


# NPExpoEast Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.expoeast.com/expoeast2012/public/ExhibitorList.aspx?Index=All&sortMenu=107007'

scrape = utilities.Scrape(headers=("User-Agent", user_agent), print_log=True)

scraperwiki.sqlite.save_var("source", "expoeast.com")
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

    def __init__(self, comp_url):
        self.comp_url = comp_url

    def _fillBlankInfo(self):
        self.my_data = utilities.initialize_my_data(self.fields, self.comp_url)

    def _fetchSourcePage(self):
        html_content = scrape(self.comp_url)
        self.root = utilities.as_lxml_node(html_content, encoding="utf-8")

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
        booth_labels = self.root.xpath("//span[starts-with(@id, 'lblBoothLabel')]")
        if not booth_labels:
            return False
        booth_text = utilities.extract_node_text(booth_labels[0])
        self._matchAndExtractSubText(r"(\d+)", booth_text, "boothnum")
        
        self.my_data["companyname"] = utilities.extract_text(self.root, "#lblCoName", empty_if_not_exist=True)
        contact_text = utilities.extract_text(self.root, "#pnlcontactname #lblContactName",
                        empty_if_not_exist=True)
        if contact_text:
            self._fillFirstLastName(contact_text)
        self.my_data["address"] = utilities.extract_text(self.root, "#lblAdd1", empty_if_not_exist=True)
        self.my_data["address2"] = utilities.extract_text(self.root, "#lblAdd2", empty_if_not_exist=True)
        self.my_data["city"] = utilities.extract_text(self.root, "#lblCity", empty_if_not_exist=True).strip(",")
        self.my_data["state"] = utilities.extract_text(self.root, "#lblState", empty_if_not_exist=True)
        self.my_data["zip"] = utilities.extract_text(self.root, "#lblZip", empty_if_not_exist=True)
        self.my_data["country"] = utilities.extract_text(self.root, "#lblCountry", empty_if_not_exist=True)
        self.my_data["phonenumber"] = utilities.extract_text(self.root, "#lblPhone", empty_if_not_exist=True)
        self.my_data["faxnumber"] = utilities.extract_text(self.root, "#lblFax", empty_if_not_exist=True)
        for a_node in self.root.cssselect("#pnlcontactname")[0].getparent().cssselect("a"):
            if a_node.get("href"):
                if a_node.get("href") and a_node.get("href").startswith("BoothURL.aspx"):
                    self.my_data["website"] = utilities.extract_node_text(a_node)
        description_nodes = self.root.cssselect("#lblWelcome")
        if description_nodes:
            self.my_data["description"] = utilities.extract_multiple_line_text(description_nodes[0])

        self._fillMainCategoryAndCategories()

        self.my_data["contactlink"] = self.my_data["sourceurl"] + "#lblSendMailMsg"
        return True

    def _fillMainCategoryAndCategories(self):
        maincategory = []
        categories = []

        maincategory_nodes = self.root.cssselect("#lblCategories ul")
        for maincategory_node in maincategory_nodes:
            maincategory.append(utilities.extract_node_text(maincategory_node))

        category_nodes = self.root.cssselect("#lblCategories li")
        for category_node in category_nodes:
            categories.append(utilities.extract_node_text(category_node))
        
        self.my_data["maincategory"] = ",".join(maincategory)
        self.my_data["categories"] = ",".join(categories)


    def __call__(self):
        self._fetchSourcePage()
        self._fillBlankInfo()
        if self._fillNonBlankInfo():
            self.saveData()

    def saveData(self):
        #print my_data
        scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=dict(self.my_data))


def scrape_site(s_url):
    if not scraperwiki.sqlite.get_var("COMP_URLS", None):
        COMP_URLS = {}
        pagenum = 1
        done = False
        while not done:
            print "Page:", pagenum
            url = s_url + "&pagenum=%d" % pagenum
            html_content = scrape(url)
            root = utilities.as_lxml_node(html_content, encoding="utf-8")

            for a_node in root.cssselect("#tableUpgraded tr#trnode a") + root.cssselect("#tableAll tr#trnode a"):
                if a_node.get("href") and "Booth.aspx?" in a_node.get("href"):
                    comp_url = urlparse.urljoin(url, a_node.get("href"))
                    params = cgi.parse_qs(urlparse.urlparse(comp_url).query)
                    if params.has_key("BoothID"):
                        COMP_URLS[params["BoothID"][0]] = comp_url
            found_next = False
            for a_node in root.cssselect("a"):
                if a_node.get('href') and "pagingNext" in a_node.get("href") and utilities.extract_node_text(a_node) == "Next":
                    found_next = True
                    break
            done = not found_next
            pagenum += 1
        COMP_URLS = COMP_URLS.values()
        scraperwiki.sqlite.save_var("COMP_URLS", cPickle.dumps(COMP_URLS))
    else:
        COMP_URLS = cPickle.loads(scraperwiki.sqlite.get_var("COMP_URLS"))

    last_comp_url = scraperwiki.sqlite.get_var("last_comp_url", None)

    if last_comp_url:
        found = False
        NEW_COMP_URLS = []
        print "RESUME From:", last_comp_url
        for comp_url in COMP_URLS:
            if comp_url == last_comp_url:
                found = True
            if found:
                NEW_COMP_URLS.append(comp_url)
        if NEW_COMP_URLS:
            COMP_URLS = NEW_COMP_URLS

    for comp_url in COMP_URLS:
        scraperwiki.sqlite.save_var("last_comp_url", comp_url)
        ScrapeInfo(comp_url)()
    print "DONE"

def main():
    scrape_site(s_url)
    #ScrapeInfo("http://www.expoeast.com/expoeast2012/Public/Booth.aspx?IndexInList=0&FromPage=ExhibitorSearch.aspx&BoothID=1107110")()
    #ScrapeInfo("http://www.expoeast.com/expoeast2012/public/Booth.aspx?IndexInList=19&FromPage=ExhibitorList.aspx&ParentBoothID=&ListByBooth=true&BoothID=1107983")()
    #ScrapeInfo("http://www.expoeast.com/expoeast2012/public/Booth.aspx?BoothID=1107971")()


if __name__ == "scraper":
    main()
