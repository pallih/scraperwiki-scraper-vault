# author: Guan Ping Fan
# This is a scraper for newenglandspecialtyfoods.com
import urlparse
import urllib2
import datetime
import re
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")


# Nespecialty Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.newenglandspecialtyfoods.com'


scraperwiki.sqlite.save_var("source", "newenglandspecialtyfoods.com")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


FIELDS = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'maincategory', 'categories',
                       'address', 'address2', 'city', 'state', 'zip', 'country', 
                       'boothnum',
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'contact3first', 'contact3last', 'contact3title',
                       'yearfounded', 'description', 'certifications', 'contactlink')


COMPANIES = {}

def scrape_category(category_url):
    print "Working on:", category_url
    html_content = utilities.scrape(category_url)
    if not html_content:
        print "Can't get page: %s" % category_url
        return
    root = utilities.as_lxml_node(html_content, encoding="ISO-8859-1")
    if root.cssselect("#element4"):
        categories_text = utilities.extract_text(root, "#element4")
    else:
        categories_text = utilities.extract_text(root, "#element7")
    categories_list = [utilities.clean(category) for category in re.split(r"\,|\:", categories_text)]
    if categories_list[0] == "Home":
        categories_list = categories_list[1:]
    maincategory = categories_list[0]
    categories_list = categories_list[1:]
    
    comp_div_nodes = root.xpath("//div[@id='element5']//div[@align='center']")

    if comp_div_nodes:
        a_nodes = comp_div_nodes[0].cssselect("a")
        if len(categories_list) == 0 and len(a_nodes) > 1:
            if not a_nodes[0].get("href").startswith("http"):
                # this is a super category, just skip it
                return
            else:
                raise Exception("unexpected category page: %s,%s" % (lxml.html.tostring(comp_div_node),category_url))

    for comp_div_node in comp_div_nodes:
        comp_div_text = utilities.split_and_clean(utilities.extract_node_text(comp_div_node))
        if comp_div_text:
            m = re.match(r"(?P<comp_city>.*)(\,|\.)\s*(?P<state>[A-Za-z]{2})?(\,|\s)\s*(?P<phonenumber>(\(\d+\)\s+)?[0-9\-A-Z]+(\,\s*ext\.\d+)?\,)?\s*(?P<website>.*)", comp_div_text)
            if len(comp_div_text.split(",")) == 1:
                    continue
            if m:
                my_data = utilities.initialize_my_data(FIELDS, category_url)
                comp_city = m.group("comp_city")
                splitted = comp_city.split(",")
                my_data["companyname"] = ",".join(splitted[:-1])
                my_data["city"] = splitted[-1]

                if m.group("state"):
                    my_data["state"] = utilities.clean(m.group("state"))
                else:
                    my_data["state"] = ""
                if m.group("phonenumber"):
                    my_data["phonenumber"] = utilities.clean(m.group("phonenumber")).replace(",", "")
                else:
                    my_data["phonenumber"] = ""
                a_nodes = comp_div_node.cssselect("a")
                assert len(a_nodes) >= 1, "can't find a link for: %r of %s" % (comp_div_text, category_url)
                my_data["website"] = m.group("website")
                
                COMPANIES.setdefault(my_data["website"], {"my_data": my_data, "maincategory": [], "categories": []})
                COMPANIES[my_data["website"]]["maincategory"].append(maincategory)
                COMPANIES[my_data["website"]]["categories"] += categories_list

def save_all_data():
    for key in COMPANIES.keys():
        value = COMPANIES[key]
        print "========================="
        my_data = value["my_data"]
        my_data["maincategory"] = ",".join(utilities.list_distinct(value["maincategory"]))
        my_data["categories"] = ",".join(utilities.list_distinct(value["categories"]))
        scraperwiki.sqlite.save(unique_keys=['website'], data=dict(my_data))

def scrape_site(s_url):
    html_content = utilities.scrape(s_url)
    root = utilities.as_lxml_node(html_content, encoding="ISO-8859-1")
    category_links = []
    for a_node in root.cssselect("#element32 a"):
        if a_node.get("href"):
            category_links.append(urlparse.urljoin(s_url, a_node.get("href")))
    category_links = list(set(category_links))
    for category_link in category_links:
        scrape_category(category_link)
    save_all_data()
    print "DONE"

def main():
    scrape_site(s_url)
    #scrape_category("http://www.newenglandspecialtyfoods.com/HorsdOeuvres.html")
    #scrape_category("http://www.newenglandspecialtyfoods.com/Sauces.html")

if __name__ == "scraper":
    main()
# author: Guan Ping Fan
# This is a scraper for newenglandspecialtyfoods.com
import urlparse
import urllib2
import datetime
import re
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")


# Nespecialty Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.newenglandspecialtyfoods.com'


scraperwiki.sqlite.save_var("source", "newenglandspecialtyfoods.com")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


FIELDS = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'maincategory', 'categories',
                       'address', 'address2', 'city', 'state', 'zip', 'country', 
                       'boothnum',
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'contact3first', 'contact3last', 'contact3title',
                       'yearfounded', 'description', 'certifications', 'contactlink')


COMPANIES = {}

def scrape_category(category_url):
    print "Working on:", category_url
    html_content = utilities.scrape(category_url)
    if not html_content:
        print "Can't get page: %s" % category_url
        return
    root = utilities.as_lxml_node(html_content, encoding="ISO-8859-1")
    if root.cssselect("#element4"):
        categories_text = utilities.extract_text(root, "#element4")
    else:
        categories_text = utilities.extract_text(root, "#element7")
    categories_list = [utilities.clean(category) for category in re.split(r"\,|\:", categories_text)]
    if categories_list[0] == "Home":
        categories_list = categories_list[1:]
    maincategory = categories_list[0]
    categories_list = categories_list[1:]
    
    comp_div_nodes = root.xpath("//div[@id='element5']//div[@align='center']")

    if comp_div_nodes:
        a_nodes = comp_div_nodes[0].cssselect("a")
        if len(categories_list) == 0 and len(a_nodes) > 1:
            if not a_nodes[0].get("href").startswith("http"):
                # this is a super category, just skip it
                return
            else:
                raise Exception("unexpected category page: %s,%s" % (lxml.html.tostring(comp_div_node),category_url))

    for comp_div_node in comp_div_nodes:
        comp_div_text = utilities.split_and_clean(utilities.extract_node_text(comp_div_node))
        if comp_div_text:
            m = re.match(r"(?P<comp_city>.*)(\,|\.)\s*(?P<state>[A-Za-z]{2})?(\,|\s)\s*(?P<phonenumber>(\(\d+\)\s+)?[0-9\-A-Z]+(\,\s*ext\.\d+)?\,)?\s*(?P<website>.*)", comp_div_text)
            if len(comp_div_text.split(",")) == 1:
                    continue
            if m:
                my_data = utilities.initialize_my_data(FIELDS, category_url)
                comp_city = m.group("comp_city")
                splitted = comp_city.split(",")
                my_data["companyname"] = ",".join(splitted[:-1])
                my_data["city"] = splitted[-1]

                if m.group("state"):
                    my_data["state"] = utilities.clean(m.group("state"))
                else:
                    my_data["state"] = ""
                if m.group("phonenumber"):
                    my_data["phonenumber"] = utilities.clean(m.group("phonenumber")).replace(",", "")
                else:
                    my_data["phonenumber"] = ""
                a_nodes = comp_div_node.cssselect("a")
                assert len(a_nodes) >= 1, "can't find a link for: %r of %s" % (comp_div_text, category_url)
                my_data["website"] = m.group("website")
                
                COMPANIES.setdefault(my_data["website"], {"my_data": my_data, "maincategory": [], "categories": []})
                COMPANIES[my_data["website"]]["maincategory"].append(maincategory)
                COMPANIES[my_data["website"]]["categories"] += categories_list

def save_all_data():
    for key in COMPANIES.keys():
        value = COMPANIES[key]
        print "========================="
        my_data = value["my_data"]
        my_data["maincategory"] = ",".join(utilities.list_distinct(value["maincategory"]))
        my_data["categories"] = ",".join(utilities.list_distinct(value["categories"]))
        scraperwiki.sqlite.save(unique_keys=['website'], data=dict(my_data))

def scrape_site(s_url):
    html_content = utilities.scrape(s_url)
    root = utilities.as_lxml_node(html_content, encoding="ISO-8859-1")
    category_links = []
    for a_node in root.cssselect("#element32 a"):
        if a_node.get("href"):
            category_links.append(urlparse.urljoin(s_url, a_node.get("href")))
    category_links = list(set(category_links))
    for category_link in category_links:
        scrape_category(category_link)
    save_all_data()
    print "DONE"

def main():
    scrape_site(s_url)
    #scrape_category("http://www.newenglandspecialtyfoods.com/HorsdOeuvres.html")
    #scrape_category("http://www.newenglandspecialtyfoods.com/Sauces.html")

if __name__ == "scraper":
    main()
