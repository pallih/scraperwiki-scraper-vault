# author: Guan Ping Fan
# This is a scraper for greenpeople.org
#
#IMPORTANT NOTE: Scraperwiki.com has a CPU Time limit for scripts. When the time limit reaches, the script
#                will be terminated.
#                The GreenPeople site is big enough to reach the limit.
#                So, when you run the script, after the script finished, please check swvariables "scrapting_status"
#                if the value of it is not "DONE", you need to run the script again and again until you see "DONE".
#
import urlparse
import datetime
import time
import re
import cPickle
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")


# GreenPeople Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.greenpeople.org/index.cfm?signedin=no'


scraperwiki.sqlite.save_var("source", "greenpeople.org")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


class ScrapeInfo:
    fields = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'maincategory', 'categories',
                       'address', 'address2', 'city', 'state', 'zip', 'country', 
                       'boothnum',
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'contact3first', 'contact3last', 'contact3title',
                       'yearfounded', 'description', 'certifications', 'contactlink', 'facebook')

    def __init__(self, comp_url):
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
        html_content, final_url = utilities.scrape2(self.comp_url)
        if final_url == self.comp_url:
            self.root = utilities.as_lxml_node(html_content, encoding="iso-8859-1")
            return True
        else:
            return False

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
        
        h1_nodes = self.root.cssselect("h1")
        if h1_nodes:
            self.my_data["companyname"] = utilities.extract_node_text(h1_nodes[0])
        else:
            font_nodes = self.root.xpath("//b/font[@size='5']")
            if font_nodes:
                self.my_data["companyname"] = utilities.extract_node_text(font_nodes[0])
            else:
                raise Exception("Failed to find companyname on: %s" % self.comp_url)

        states = {}
        #print "HA:", self.root.cssselect(".listingcontent")
        expect_description = False
        for tr_node in self.root.cssselect(".listingcontent table table tr"):
            for script_node in tr_node.cssselect("script"):
                script_node.getparent().remove(script_node)
            tr_node_text = utilities.extract_node_text(tr_node)
            #print "TNT:", tr_node_text
            
            done = self._matchAndExtractSubText(r"WebSite\:(.*)", tr_node_text, "website")

            if not done:
                #done = self._matchAndExtractSubText(r".*Contact\:(.*)", tr_node_text, "contact1first")
                matched_obj = re.search(r".*Contact\:(.*)", tr_node_text)
                if matched_obj:
                    self._fillFirstLastName(matched_obj.group(1))
                done = matched_obj

            if not done:
                done = self._matchAndExtractSubText(r"Address\:(.*)\sMap", tr_node_text, "address")

            if not done:
                matched_obj = re.search(r"City\,\s*State\:(?P<city_state>.*)\sZip\:(?P<zip>.*)", tr_node_text)
                if matched_obj:
                    city_states = matched_obj.group("city_state").split(",")
                    city_states = [item.strip() for item in city_states if item.strip()]
                    if len(city_states) >= 2:
                        city = ",".join(city_states[:-1])
                        state = city_states[-1]
                    else:
                        city = city_states[0]
                        state = ""
                    self.my_data["city"] = utilities.clean(city)
                    self.my_data["state"] = utilities.clean(state)
                    self.my_data["zip"] = utilities.clean(matched_obj.group("zip"))
                done = matched_obj
                
            if not done:
                done = self._matchAndExtractSubText(r"Phone\:\s*((\(\d+\))?\s+[^\s]+)", tr_node_text, "phonenumber")
                done = self._matchAndExtractSubText(r"Fax\:\s*((\(\d+\))?\s+[^\s]+)", tr_node_text, "faxnumber") or done
                done = self._matchAndExtractSubText(r"2nd Phone\:\s*((\(\d+\))?\s+[^\s]+)", tr_node_text, "phonenumber2") or done
                if self.my_data.get("phonenumber2", None):
                    self.my_data["phonenumber"] = ",".join([self.my_data["phonenumber"], self.my_data["phonenumber2"]])
                    del self.my_data["phonenumber2"]

            if expect_description:
                self.my_data["description"] = tr_node_text
                expect_description = False

            if tr_node_text.startswith("Description:"):
                expect_description = True

        email_button_a_nodes = self.root.cssselect("div#emailbutton a")
        if email_button_a_nodes:
            self.my_data["contactlink"] = urlparse.urljoin(self.comp_url, email_button_a_nodes[0].get("href"))

        for a_node in self.root.cssselect(".listingcontent table table tr td a"):
            a_node_href = a_node.get("href")
            if a_node_href and "facebook.com" in a_node_href:
                self.my_data["facebook"] = a_node_href

        # Extract Focuses
        focus_texts = [utilities.clean(re.sub(r"\d+\)", "", utilities.extract_node_text(focus_h3)))
                for focus_h3 in self.root.cssselect(".listingcontent table table h3.focustext")]
        self.my_data["categories"] = ",".join(focus_texts)

        # Extract maincategory
        for a_node in self.root.cssselect("#vmenu a"):
            if a_node.get("style") and "background" in a_node.get("style"):
                self.my_data["maincategory"] = utilities.extract_node_text(a_node)


    def __call__(self):
        succ = self._fetchSourcePage()
        if succ:
            self._fillBlankInfo()
            self._fillNonBlankInfo()
            self.saveData()
        else:
            print "fetch of %s failed. Just skip it." % self.comp_url

    def saveData(self):
        #print my_data
        scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=dict(self.my_data))


VISITED_COMP_URLS = {}


def scrape_single_list(list_url, resume_from=None):
    scraperwiki.sqlite.save_var("scraping_list_url", list_url)
    global VISITED_COMP_URLS
    html_content = utilities.scrape(list_url)
    root = utilities.as_lxml_node(html_content, encoding="iso-8859-1")
    comp_urls = []
    for a_node in root.cssselect("td.tagcol a"):
        comp_url = urlparse.urljoin(list_url, a_node.get("href"))
        comp_urls.append(comp_url)
    for a_node in root.cssselect("div.freelisting a"):
        comp_url = urlparse.urljoin(list_url, a_node.get("href"))
        comp_urls.append(comp_url)

    if resume_from:
        try:
            resume_from_index = comp_urls.index(resume_from)
            print "scrape_single_list: resume from %d - %s" % (resume_from_index, resume_from)
            comp_urls = comp_urls[resume_from_index:]
        except ValueError:
            pass

    for comp_url in comp_urls:
        if not VISITED_COMP_URLS.get(comp_url, False):
            scraperwiki.sqlite.save_var("scraping_comp_url", comp_url)
            ScrapeInfo(comp_url)()
            time.sleep(0.1)
            VISITED_COMP_URLS[comp_url] = True

def get_single_list_urls(s_url):
    html_content = utilities.scrape(s_url)
    root = utilities.as_lxml_node(html_content, encoding="iso-8859-1")
    SECTIONS = ("personal-care-products", "natural-baby-care", "organic-food", "vegan-foods", "kosher-foods", "natural-pet-care", "natural-home", "Natural Food Stores", "community-supported-agriculture")
    sections_not_v = list(SECTIONS)
    visited = {}
    single_list_urls = []
    for a_node in root.xpath("//td/div[@align='center']//a"):
        a_node_href = a_node.get("href")
        if a_node_href:
            m = re.search(r"mainsearch\=(.*)", a_node_href)
            if m:
                if m.group(1) in SECTIONS and not visited.get(a_node_href, False):
                    if m.group(1) in sections_not_v:
                        sections_not_v.remove(m.group(1))
                    visited[a_node_href] = 1
                    parent = a_node
                    while parent.tag != "td":
                        parent = parent.getparent()
                    td_node = parent
                    for a_node2 in td_node.cssselect("p a"):
                        single_list_urls.append(urlparse.urljoin(s_url, a_node2.get("href")))
    if sections_not_v:
        raise Exception("Sections Not Found: %r" % sections_not_v)
    single_list_urls = list(set(single_list_urls))
    return single_list_urls

def scrape_site(s_url):
    if scraperwiki.sqlite.get_var("scrapting_status", None) != "SINGLE_LIST_AVAILABLE":
        single_list_urls = get_single_list_urls(s_url)
        scraperwiki.sqlite.save_var("scraping_single_list_urls", cPickle.dumps(single_list_urls))
        scraperwiki.sqlite.save_var("scrapting_status", "SINGLE_LIST_AVAILABLE")
    else:
        single_list_urls = cPickle.loads(scraperwiki.sqlite.get_var("scraping_single_list_urls"))
    
    last_scraping_comp_url = scraperwiki.sqlite.get_var("scraping_comp_url", None)
    last_scraping_list_url = scraperwiki.sqlite.get_var("scraping_list_url", None)
    # TODO: make it resume to last position
    if last_scraping_list_url:
        last_list_url_index = single_list_urls.index(last_scraping_list_url)
        print "scrape_site: resume from: %d - %s" % (last_list_url_index, last_scraping_list_url)
        single_list_urls = single_list_urls[last_list_url_index:]
    for single_list_url in single_list_urls:
        print "Working on:", single_list_url
        scrape_single_list(single_list_url, resume_from=last_scraping_comp_url)
    scraperwiki.sqlite.save_var("scrapting_status", "DONE")

def scrape_site1():
    single_list_urls = cPickle.loads(scraperwiki.sqlite.get_var("scraping_single_list_urls"))
    for single_list_url in single_list_urls[44:]:
        print single_list_url
        scrape_single_list(single_list_url)
    scraperwiki.sqlite.save_var("scrapting_status", "DONE")

def main():
    #scrape_site(s_url)
    #ScrapeInfo("http://www.greenpeople.org/listing/The-Eco-Pet-Club-66987.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/JES-Organics-LLC-63770.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Herbs-of-Grace-Inc-3589.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Organic-Catnip-and-18871.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Earth-Angels-Veterinary-60946.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/ZeroWaste-USA-DBA-44185.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Global-Dog-Natural-26302.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Choice-Caring-Holistic-35148.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Seed-to-Shelf-Marketing-27510.cfm")()

    #scrape_single_list("http://www.greenpeople.org/natural-hair-care.html")
    #scrape_single_list("http://www.greenpeople.org/Organics-for-Baby-Cloth-Diapers.html")
    
    scrape_site(s_url)
    #scrape_site1()
    #scraperwiki.sqlite.save_var("scrapting_status", "SINGLE_LIST_AVAILABLE")

if __name__ == "scraper":
    main()
# author: Guan Ping Fan
# This is a scraper for greenpeople.org
#
#IMPORTANT NOTE: Scraperwiki.com has a CPU Time limit for scripts. When the time limit reaches, the script
#                will be terminated.
#                The GreenPeople site is big enough to reach the limit.
#                So, when you run the script, after the script finished, please check swvariables "scrapting_status"
#                if the value of it is not "DONE", you need to run the script again and again until you see "DONE".
#
import urlparse
import datetime
import time
import re
import cPickle
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")


# GreenPeople Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.greenpeople.org/index.cfm?signedin=no'


scraperwiki.sqlite.save_var("source", "greenpeople.org")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


class ScrapeInfo:
    fields = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'maincategory', 'categories',
                       'address', 'address2', 'city', 'state', 'zip', 'country', 
                       'boothnum',
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'contact3first', 'contact3last', 'contact3title',
                       'yearfounded', 'description', 'certifications', 'contactlink', 'facebook')

    def __init__(self, comp_url):
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
        html_content, final_url = utilities.scrape2(self.comp_url)
        if final_url == self.comp_url:
            self.root = utilities.as_lxml_node(html_content, encoding="iso-8859-1")
            return True
        else:
            return False

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
        
        h1_nodes = self.root.cssselect("h1")
        if h1_nodes:
            self.my_data["companyname"] = utilities.extract_node_text(h1_nodes[0])
        else:
            font_nodes = self.root.xpath("//b/font[@size='5']")
            if font_nodes:
                self.my_data["companyname"] = utilities.extract_node_text(font_nodes[0])
            else:
                raise Exception("Failed to find companyname on: %s" % self.comp_url)

        states = {}
        #print "HA:", self.root.cssselect(".listingcontent")
        expect_description = False
        for tr_node in self.root.cssselect(".listingcontent table table tr"):
            for script_node in tr_node.cssselect("script"):
                script_node.getparent().remove(script_node)
            tr_node_text = utilities.extract_node_text(tr_node)
            #print "TNT:", tr_node_text
            
            done = self._matchAndExtractSubText(r"WebSite\:(.*)", tr_node_text, "website")

            if not done:
                #done = self._matchAndExtractSubText(r".*Contact\:(.*)", tr_node_text, "contact1first")
                matched_obj = re.search(r".*Contact\:(.*)", tr_node_text)
                if matched_obj:
                    self._fillFirstLastName(matched_obj.group(1))
                done = matched_obj

            if not done:
                done = self._matchAndExtractSubText(r"Address\:(.*)\sMap", tr_node_text, "address")

            if not done:
                matched_obj = re.search(r"City\,\s*State\:(?P<city_state>.*)\sZip\:(?P<zip>.*)", tr_node_text)
                if matched_obj:
                    city_states = matched_obj.group("city_state").split(",")
                    city_states = [item.strip() for item in city_states if item.strip()]
                    if len(city_states) >= 2:
                        city = ",".join(city_states[:-1])
                        state = city_states[-1]
                    else:
                        city = city_states[0]
                        state = ""
                    self.my_data["city"] = utilities.clean(city)
                    self.my_data["state"] = utilities.clean(state)
                    self.my_data["zip"] = utilities.clean(matched_obj.group("zip"))
                done = matched_obj
                
            if not done:
                done = self._matchAndExtractSubText(r"Phone\:\s*((\(\d+\))?\s+[^\s]+)", tr_node_text, "phonenumber")
                done = self._matchAndExtractSubText(r"Fax\:\s*((\(\d+\))?\s+[^\s]+)", tr_node_text, "faxnumber") or done
                done = self._matchAndExtractSubText(r"2nd Phone\:\s*((\(\d+\))?\s+[^\s]+)", tr_node_text, "phonenumber2") or done
                if self.my_data.get("phonenumber2", None):
                    self.my_data["phonenumber"] = ",".join([self.my_data["phonenumber"], self.my_data["phonenumber2"]])
                    del self.my_data["phonenumber2"]

            if expect_description:
                self.my_data["description"] = tr_node_text
                expect_description = False

            if tr_node_text.startswith("Description:"):
                expect_description = True

        email_button_a_nodes = self.root.cssselect("div#emailbutton a")
        if email_button_a_nodes:
            self.my_data["contactlink"] = urlparse.urljoin(self.comp_url, email_button_a_nodes[0].get("href"))

        for a_node in self.root.cssselect(".listingcontent table table tr td a"):
            a_node_href = a_node.get("href")
            if a_node_href and "facebook.com" in a_node_href:
                self.my_data["facebook"] = a_node_href

        # Extract Focuses
        focus_texts = [utilities.clean(re.sub(r"\d+\)", "", utilities.extract_node_text(focus_h3)))
                for focus_h3 in self.root.cssselect(".listingcontent table table h3.focustext")]
        self.my_data["categories"] = ",".join(focus_texts)

        # Extract maincategory
        for a_node in self.root.cssselect("#vmenu a"):
            if a_node.get("style") and "background" in a_node.get("style"):
                self.my_data["maincategory"] = utilities.extract_node_text(a_node)


    def __call__(self):
        succ = self._fetchSourcePage()
        if succ:
            self._fillBlankInfo()
            self._fillNonBlankInfo()
            self.saveData()
        else:
            print "fetch of %s failed. Just skip it." % self.comp_url

    def saveData(self):
        #print my_data
        scraperwiki.sqlite.save(unique_keys=['sourceurl'], data=dict(self.my_data))


VISITED_COMP_URLS = {}


def scrape_single_list(list_url, resume_from=None):
    scraperwiki.sqlite.save_var("scraping_list_url", list_url)
    global VISITED_COMP_URLS
    html_content = utilities.scrape(list_url)
    root = utilities.as_lxml_node(html_content, encoding="iso-8859-1")
    comp_urls = []
    for a_node in root.cssselect("td.tagcol a"):
        comp_url = urlparse.urljoin(list_url, a_node.get("href"))
        comp_urls.append(comp_url)
    for a_node in root.cssselect("div.freelisting a"):
        comp_url = urlparse.urljoin(list_url, a_node.get("href"))
        comp_urls.append(comp_url)

    if resume_from:
        try:
            resume_from_index = comp_urls.index(resume_from)
            print "scrape_single_list: resume from %d - %s" % (resume_from_index, resume_from)
            comp_urls = comp_urls[resume_from_index:]
        except ValueError:
            pass

    for comp_url in comp_urls:
        if not VISITED_COMP_URLS.get(comp_url, False):
            scraperwiki.sqlite.save_var("scraping_comp_url", comp_url)
            ScrapeInfo(comp_url)()
            time.sleep(0.1)
            VISITED_COMP_URLS[comp_url] = True

def get_single_list_urls(s_url):
    html_content = utilities.scrape(s_url)
    root = utilities.as_lxml_node(html_content, encoding="iso-8859-1")
    SECTIONS = ("personal-care-products", "natural-baby-care", "organic-food", "vegan-foods", "kosher-foods", "natural-pet-care", "natural-home", "Natural Food Stores", "community-supported-agriculture")
    sections_not_v = list(SECTIONS)
    visited = {}
    single_list_urls = []
    for a_node in root.xpath("//td/div[@align='center']//a"):
        a_node_href = a_node.get("href")
        if a_node_href:
            m = re.search(r"mainsearch\=(.*)", a_node_href)
            if m:
                if m.group(1) in SECTIONS and not visited.get(a_node_href, False):
                    if m.group(1) in sections_not_v:
                        sections_not_v.remove(m.group(1))
                    visited[a_node_href] = 1
                    parent = a_node
                    while parent.tag != "td":
                        parent = parent.getparent()
                    td_node = parent
                    for a_node2 in td_node.cssselect("p a"):
                        single_list_urls.append(urlparse.urljoin(s_url, a_node2.get("href")))
    if sections_not_v:
        raise Exception("Sections Not Found: %r" % sections_not_v)
    single_list_urls = list(set(single_list_urls))
    return single_list_urls

def scrape_site(s_url):
    if scraperwiki.sqlite.get_var("scrapting_status", None) != "SINGLE_LIST_AVAILABLE":
        single_list_urls = get_single_list_urls(s_url)
        scraperwiki.sqlite.save_var("scraping_single_list_urls", cPickle.dumps(single_list_urls))
        scraperwiki.sqlite.save_var("scrapting_status", "SINGLE_LIST_AVAILABLE")
    else:
        single_list_urls = cPickle.loads(scraperwiki.sqlite.get_var("scraping_single_list_urls"))
    
    last_scraping_comp_url = scraperwiki.sqlite.get_var("scraping_comp_url", None)
    last_scraping_list_url = scraperwiki.sqlite.get_var("scraping_list_url", None)
    # TODO: make it resume to last position
    if last_scraping_list_url:
        last_list_url_index = single_list_urls.index(last_scraping_list_url)
        print "scrape_site: resume from: %d - %s" % (last_list_url_index, last_scraping_list_url)
        single_list_urls = single_list_urls[last_list_url_index:]
    for single_list_url in single_list_urls:
        print "Working on:", single_list_url
        scrape_single_list(single_list_url, resume_from=last_scraping_comp_url)
    scraperwiki.sqlite.save_var("scrapting_status", "DONE")

def scrape_site1():
    single_list_urls = cPickle.loads(scraperwiki.sqlite.get_var("scraping_single_list_urls"))
    for single_list_url in single_list_urls[44:]:
        print single_list_url
        scrape_single_list(single_list_url)
    scraperwiki.sqlite.save_var("scrapting_status", "DONE")

def main():
    #scrape_site(s_url)
    #ScrapeInfo("http://www.greenpeople.org/listing/The-Eco-Pet-Club-66987.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/JES-Organics-LLC-63770.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Herbs-of-Grace-Inc-3589.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Organic-Catnip-and-18871.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Earth-Angels-Veterinary-60946.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/ZeroWaste-USA-DBA-44185.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Global-Dog-Natural-26302.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Choice-Caring-Holistic-35148.cfm")()
    #ScrapeInfo("http://www.greenpeople.org/listing/Seed-to-Shelf-Marketing-27510.cfm")()

    #scrape_single_list("http://www.greenpeople.org/natural-hair-care.html")
    #scrape_single_list("http://www.greenpeople.org/Organics-for-Baby-Cloth-Diapers.html")
    
    scrape_site(s_url)
    #scrape_site1()
    #scraperwiki.sqlite.save_var("scrapting_status", "SINGLE_LIST_AVAILABLE")

if __name__ == "scraper":
    main()
