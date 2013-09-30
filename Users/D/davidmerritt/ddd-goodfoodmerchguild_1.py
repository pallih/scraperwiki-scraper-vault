# author: Guan Ping Fan
# This is a scraper for goodfoodmerchantsguild.org
import urlparse
import datetime
import re
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")


# OrganicTrade Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.goodfoodmerchantsguild.org/directorylisting'


scraperwiki.sqlite.save_var("source", "goodfoodmerchantsguild.org")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


FIELDS = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'maincategory', 'categories',
                       'address', 'address2', 'city', 'state', 'zip', 'country', 
                       'boothnum',
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'contact3first', 'contact3last', 'contact3title',
                       'yearfounded', 'description', 'certifications', 'contactlink')


def scrape_site(s_url):
    html_content = utilities.scrape(s_url)
    root = utilities.as_lxml_node(html_content, encoding="utf-8")

    for comp_div in \
        root.xpath("//div[@class='directory']//div[@class='content']//div[@class='box thesameheight']"):
        my_data = utilities.initialize_my_data(FIELDS, s_url)
        a_nodes = comp_div.xpath("a")
        assert len(a_nodes) == 1, "Failed to find website link"
        my_data["companyname"] = utilities.extract_node_text(a_nodes[0])
        my_data["website"] = a_nodes[0].get("href")
        lines = utilities.extract_multiple_line_text(comp_div).split("\n")
        assert lines[0] == my_data["companyname"], "something is wrong for: %s" % lines
        my_data["city"], my_data["state"] = lines[1].split(",")
        my_data["maincategory"] = utilities.split_and_clean(lines[2])
        scraperwiki.sqlite.save(unique_keys=['website'], data=dict(my_data))

def main():
    scrape_site(s_url)


if __name__ == "scraper":
    main()# author: Guan Ping Fan
# This is a scraper for goodfoodmerchantsguild.org
import urlparse
import datetime
import re
import lxml.html
import scraperwiki


utilities = scraperwiki.utils.swimport("jacobfan-utilities")


# OrganicTrade Scraper Below
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://www.goodfoodmerchantsguild.org/directorylisting'


scraperwiki.sqlite.save_var("source", "goodfoodmerchantsguild.org")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


FIELDS = ('datescraped', 'emails', 'companyname', 'dba', 'website', 'maincategory', 'categories',
                       'address', 'address2', 'city', 'state', 'zip', 'country', 
                       'boothnum',
                       'sourceurl', 'salesmethod', 'phonenumber', 'faxnumber',
                       'contact1first', 'contact1last', 'contact1title', 
                       'contact2first', 'contact2last', 'contact2title', 
                       'contact3first', 'contact3last', 'contact3title',
                       'yearfounded', 'description', 'certifications', 'contactlink')


def scrape_site(s_url):
    html_content = utilities.scrape(s_url)
    root = utilities.as_lxml_node(html_content, encoding="utf-8")

    for comp_div in \
        root.xpath("//div[@class='directory']//div[@class='content']//div[@class='box thesameheight']"):
        my_data = utilities.initialize_my_data(FIELDS, s_url)
        a_nodes = comp_div.xpath("a")
        assert len(a_nodes) == 1, "Failed to find website link"
        my_data["companyname"] = utilities.extract_node_text(a_nodes[0])
        my_data["website"] = a_nodes[0].get("href")
        lines = utilities.extract_multiple_line_text(comp_div).split("\n")
        assert lines[0] == my_data["companyname"], "something is wrong for: %s" % lines
        my_data["city"], my_data["state"] = lines[1].split(",")
        my_data["maincategory"] = utilities.split_and_clean(lines[2])
        scraperwiki.sqlite.save(unique_keys=['website'], data=dict(my_data))

def main():
    scrape_site(s_url)


if __name__ == "scraper":
    main()