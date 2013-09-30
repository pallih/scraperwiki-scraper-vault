# author: Guan Ping Fan
# This is a scraper for fancyfoodshows.com

import lxml.html
#import bs4
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


# MyFancyFoodShow Scraper Below

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://my.fancyfoodshows.com/networkNow/Public/nz_ALExhibitorSearch.aspx?ID=63'

scraperwiki.sqlite.save_var("source", "fancyfoodshows.com")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


def extract_dba(root, my_data):
    if root.cssselect("#ctl00_MainContent_lblBrandsMsg"):
        my_data.append(('dba', 
            split_and_clean(extract_text(root, "#ctl00_MainContent_lblBrands"), ",")))
    else:
        my_data.append(('dba', ''))


def extract_website(root, my_data):
    website = extract_text(root, "#lblURL", empty_if_not_exist=True, is_clean=False)
    if website:
        website = clean("http://" + website)
    my_data.append(('website', website))


def extract_maincategory_n_categories(root, my_data):
    if root.cssselect("#ctl00_MainContent_lblCategoriesMsg"):
        ul_node = root.cssselect("#ctl00_MainContent_lblCategories ul")[0]
        # maincategory
        my_data.append(("maincategory", clean(",".join(extract_text(ul_node, "u", is_multiple=True, is_clean=False)))))
        # categories
        my_data.append(("categories", clean(",".join(extract_text(ul_node, "li", is_multiple=True, is_clean=False)))))
    else:
        my_data.append(("categories", ""))
        my_data.append(("maincategory", ""))


def extract_address_related_info(root, my_data):
    my_data.append(('address', extract_text(root, "span#ctl00_MainContent_lblAdd1")))
    my_data.append(('address2', extract_text(root, "span#ctl00_MainContent_lblAdd2")))
    city = extract_text(root, "span#ctl00_MainContent_lblCity")
    if city.endswith(","):
        city = clean(city[:-1])
    my_data.append(('city', city))
    my_data.append(('state', extract_text(root, "span#ctl00_MainContent_lblState").replace(u'\xc2', '')))
    my_data.append(('zip', extract_text(root, "span#ctl00_MainContent_lblZip")))
    my_data.append(('country', extract_text(root, "span#ctl00_MainContent_lblCountry")))


def extract_boothnum(root, my_data, boothid):
    boothnum = extract_text(root, "#ctl00_MainContent_lblBoothLabel" + boothid)
    boothnum = re.search(r"\d+", boothnum).group(0)
    my_data.append(('boothnum', boothnum))


def extract_facebook_twitter(root, my_data):
    twitter = ""
    facebook_url = ""
    custom_field_list = root.cssselect("#ctl00_MainContent_ctrlCustomField_Logos_pnlCustomFieldList")[0]
    link_nodes = custom_field_list.cssselect("a")
    for link_node in link_nodes:
        link_url = link_node.get("href")
        twitter_matched = re.search(r"twitter\.com/([^\/]+)", link_url)
        if twitter_matched:
            twitter = twitter_matched.group(1)
        elif "www.facebook.com" in link_url:
            facebook_url = link_url
    my_data.append(("twitter", clean(twitter)))
    my_data.append(("facebook", clean(facebook_url)))


def scrape_info(comp_link, extra_infos):
    m = re.search(r"BoothID\=(\d+)", comp_link)
    boothid = m.group(1)
    html_content = scrape(comp_link)
    root = as_lxml_node(html_content)
    my_data = []
    my_data.append(('datescraped', clean(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))))
    my_data.append(('emails', ''))
    my_data.append(('companyname', extract_text(root, "#ctl00_MainContent_lblCoName")))
    extract_dba(root, my_data)
    extract_website(root, my_data)
    extract_maincategory_n_categories(root, my_data)
    extract_address_related_info(root, my_data)
    extract_boothnum(root, my_data, boothid)
    my_data.append(('sourceurl', clean(comp_link)))
    my_data.append(('salesmethod', ''))
    my_data.append(('phonenumber', extract_text(root, '#ctl00_MainContent_lblPhone', empty_if_not_exist=True)))
    my_data.append(('faxnumber', extract_text(root, '#ctl00_MainContent_lblFax', empty_if_not_exist=True)))
    my_data.append(('contact1first', ''))
    my_data.append(('contact1last', ''))
    my_data.append(('contact1title', ''))
    my_data.append(('contact2first', ''))
    my_data.append(('contact2last', ''))
    my_data.append(('contact2title', ''))
    my_data.append(('contact3first', ''))
    my_data.append(('contact3last', ''))
    my_data.append(('contact3title', ''))
    description = extract_text(root, '#ctl00_MainContent_lblProfile', is_clean=False)
    matched = re.search(r"founded in\s+(\d+)", description)
    if matched:
        my_data.append(('yearfounded', matched.group(1)))
    else:
        my_data.append(('yearfounded', ''))
    my_data.append(('description', clean(limit_length(description, 1000))))
    my_data.append(('certifications', ''))
    my_data.append(('contactlink', clean(extra_infos["contact_link"])))
    extract_facebook_twitter(root, my_data)

    #print my_data
    scraperwiki.sqlite.save(unique_keys=['boothnum'], data=dict(my_data))


def process_list_page(start_url, html_content, is_first_page):
    root = as_lxml_node(html_content)
    # Check Current Page
    page = extract_text(root, "a.rgCurrentPage")
    print "Page:", page

    #Parse List Items
    tr_list = root.cssselect('table.rgMasterTable tbody tr')
    for tr in tr_list:
        td_list = tr.cssselect("td")
        comp_link_node = td_list[1].cssselect("a")[0]
        assert comp_link_node.get("id").endswith("lnkCompanyName"), "Invalid link node found:%s " % comp_link_node.get("id")
        comp_link = urlparse.urljoin(start_url, comp_link_node.get("href"))
        contact_link_node = td_list[-2].cssselect("a")[0]
        assert contact_link_node.get("id").endswith("lnkSendEmail"), "Invalid link node found:%s " % contact_link_node.get("id")
        matched = re.search(r"\'(nz\_sendEmail.*)\'", contact_link_node.get("onclick"))
        extra_infos = {}
        extra_infos["contact_link"] = urlparse.urljoin(start_url, matched.group(1))
        scrape_info(comp_link, extra_infos)

    # Navigate to Next Page
    ctl00_MainContent_pnlExhibitorList = root.cssselect("#ctl00_MainContent_pnlExhibitorList")[0]
    input_next = ctl00_MainContent_pnlExhibitorList.cssselect("input.rgPageNext")[0]
    input_next_on_click = input_next.get("onclick")
    if (input_next_on_click is None) or ("return false" not in input_next.get("onclick")):
        form_values = {}
        input_next_name = input_next.get("name")
        if is_first_page:
            view_state_value = root.xpath("//input[@name='__VIEWSTATE']")[0].get("value")
        else:
            m = re.search(r"VIEWSTATE\|([^\|]+)", html_content)
            view_state_value = m.group(1)

        form_values = {
            "ctl00$MasterScriptManager": "ctl00$MainContent$ctrlExhibitorList$upContent|" + input_next_name,
            "ctl00_MasterScriptManager_TSM": ";;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:3de828f0-5e0d-4c7d-a36b-56a9773c0def:ea597d4b:b25378d2;Telerik.Web.UI, Version=2011.2.712.35, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:326e32e2-cd52-462c-ba2c-db5128e4371b:16e4e7cd:86526ba7:f7645509:24ee1bba:874f8ea2:f46195d3:19620875:490a9d4e:bd8f85e4:e330518b:1e771326:c8618e41:b7778d6c:58366029:aa288e2d;Flan.Controls:en-US:761ee250-93ab-46b1-85e7-8262be0e72f0:27a22b1e;",
            "ctl00_RadStyleSheetManager1_TSSM": ";Telerik.Web.UI, Version=2011.2.712.35, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:326e32e2-cd52-462c-ba2c-db5128e4371b:ef4a543:67d175d:92753c09:91f742eb:9e1572d6:e25b4b77:1c2121e:e24b8e95",
            "ctl00_frmDecorator_ClientState": "",
            "ctl00_Window1_ClientState": "",
            "ctl00_RadWindowManager1_ClientState": "",
            "ctl00$ctlP_welcomeNav$ddlLang": "en-US",
            "ctl00$ctlP_welcomeNav$hdnHome": "../public/nz_ALMyProfile.aspx",
            "ctl00_ctlP_Navigation_radNavigation_ClientState": "",
            "ctl00_LeftNav_txtKeyword_text": "Type your Keyword here",
            "ctl00$LeftNav$txtKeyword": "",
            "ctl00_LeftNav_txtKeyword_ClientState": '{"enabled":true,"emptyMessage":"Type your Keyword here"}',
            "ctl00_ucQuickLinks_radQuickLinks_ClientState": "",
            "ctl00$MainContent$ctrlExhibitorList$radExhibitorList$ctl00$ctl03$ctl01$PageSizeComboBox": "100",
            "ctl00_MainContent_ctrlExhibitorList_radExhibitorList_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState": '{"logEntries":[],"value":"100","text":"100","enabled":true,"checkedIndices":[]}',
            "ctl00_MainContent_ctrlExhibitorList_radExhibitorList_ClientState": "",
            "ctl00$MainContent$ctrlExhibitorList$hdnCustomFieldIDs": "15,16,17,19,14",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": view_state_value,
            "__ASYNCPOST": "true",
            input_next_name: ""
        }

        next_content = scrape(s_url, form_values, 
                    headers=(("User-Agent", user_agent),
                             ("X-MicrosoftAjax", "Delta=true"),
                             (('X-Requested-With', 'XMLHttpRequest')),
                             ("Referer", s_url)))
        
        process_list_page(start_url, next_content, is_first_page=False)
    else:
        print "No More Pages. Finished"


def scrape_site(start_url):
    html_content = scrape(start_url)
    process_list_page(start_url, html_content, is_first_page=True)


scrape_site(s_url)
# author: Guan Ping Fan
# This is a scraper for fancyfoodshows.com

import lxml.html
#import bs4
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


# MyFancyFoodShow Scraper Below

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:9.0.1) Gecko/20100101 Firefox/9.0.1'
s_url = 'http://my.fancyfoodshows.com/networkNow/Public/nz_ALExhibitorSearch.aspx?ID=63'

scraperwiki.sqlite.save_var("source", "fancyfoodshows.com")
scraperwiki.sqlite.save_var("author", "Guan Ping Fan")


def extract_dba(root, my_data):
    if root.cssselect("#ctl00_MainContent_lblBrandsMsg"):
        my_data.append(('dba', 
            split_and_clean(extract_text(root, "#ctl00_MainContent_lblBrands"), ",")))
    else:
        my_data.append(('dba', ''))


def extract_website(root, my_data):
    website = extract_text(root, "#lblURL", empty_if_not_exist=True, is_clean=False)
    if website:
        website = clean("http://" + website)
    my_data.append(('website', website))


def extract_maincategory_n_categories(root, my_data):
    if root.cssselect("#ctl00_MainContent_lblCategoriesMsg"):
        ul_node = root.cssselect("#ctl00_MainContent_lblCategories ul")[0]
        # maincategory
        my_data.append(("maincategory", clean(",".join(extract_text(ul_node, "u", is_multiple=True, is_clean=False)))))
        # categories
        my_data.append(("categories", clean(",".join(extract_text(ul_node, "li", is_multiple=True, is_clean=False)))))
    else:
        my_data.append(("categories", ""))
        my_data.append(("maincategory", ""))


def extract_address_related_info(root, my_data):
    my_data.append(('address', extract_text(root, "span#ctl00_MainContent_lblAdd1")))
    my_data.append(('address2', extract_text(root, "span#ctl00_MainContent_lblAdd2")))
    city = extract_text(root, "span#ctl00_MainContent_lblCity")
    if city.endswith(","):
        city = clean(city[:-1])
    my_data.append(('city', city))
    my_data.append(('state', extract_text(root, "span#ctl00_MainContent_lblState").replace(u'\xc2', '')))
    my_data.append(('zip', extract_text(root, "span#ctl00_MainContent_lblZip")))
    my_data.append(('country', extract_text(root, "span#ctl00_MainContent_lblCountry")))


def extract_boothnum(root, my_data, boothid):
    boothnum = extract_text(root, "#ctl00_MainContent_lblBoothLabel" + boothid)
    boothnum = re.search(r"\d+", boothnum).group(0)
    my_data.append(('boothnum', boothnum))


def extract_facebook_twitter(root, my_data):
    twitter = ""
    facebook_url = ""
    custom_field_list = root.cssselect("#ctl00_MainContent_ctrlCustomField_Logos_pnlCustomFieldList")[0]
    link_nodes = custom_field_list.cssselect("a")
    for link_node in link_nodes:
        link_url = link_node.get("href")
        twitter_matched = re.search(r"twitter\.com/([^\/]+)", link_url)
        if twitter_matched:
            twitter = twitter_matched.group(1)
        elif "www.facebook.com" in link_url:
            facebook_url = link_url
    my_data.append(("twitter", clean(twitter)))
    my_data.append(("facebook", clean(facebook_url)))


def scrape_info(comp_link, extra_infos):
    m = re.search(r"BoothID\=(\d+)", comp_link)
    boothid = m.group(1)
    html_content = scrape(comp_link)
    root = as_lxml_node(html_content)
    my_data = []
    my_data.append(('datescraped', clean(datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'))))
    my_data.append(('emails', ''))
    my_data.append(('companyname', extract_text(root, "#ctl00_MainContent_lblCoName")))
    extract_dba(root, my_data)
    extract_website(root, my_data)
    extract_maincategory_n_categories(root, my_data)
    extract_address_related_info(root, my_data)
    extract_boothnum(root, my_data, boothid)
    my_data.append(('sourceurl', clean(comp_link)))
    my_data.append(('salesmethod', ''))
    my_data.append(('phonenumber', extract_text(root, '#ctl00_MainContent_lblPhone', empty_if_not_exist=True)))
    my_data.append(('faxnumber', extract_text(root, '#ctl00_MainContent_lblFax', empty_if_not_exist=True)))
    my_data.append(('contact1first', ''))
    my_data.append(('contact1last', ''))
    my_data.append(('contact1title', ''))
    my_data.append(('contact2first', ''))
    my_data.append(('contact2last', ''))
    my_data.append(('contact2title', ''))
    my_data.append(('contact3first', ''))
    my_data.append(('contact3last', ''))
    my_data.append(('contact3title', ''))
    description = extract_text(root, '#ctl00_MainContent_lblProfile', is_clean=False)
    matched = re.search(r"founded in\s+(\d+)", description)
    if matched:
        my_data.append(('yearfounded', matched.group(1)))
    else:
        my_data.append(('yearfounded', ''))
    my_data.append(('description', clean(limit_length(description, 1000))))
    my_data.append(('certifications', ''))
    my_data.append(('contactlink', clean(extra_infos["contact_link"])))
    extract_facebook_twitter(root, my_data)

    #print my_data
    scraperwiki.sqlite.save(unique_keys=['boothnum'], data=dict(my_data))


def process_list_page(start_url, html_content, is_first_page):
    root = as_lxml_node(html_content)
    # Check Current Page
    page = extract_text(root, "a.rgCurrentPage")
    print "Page:", page

    #Parse List Items
    tr_list = root.cssselect('table.rgMasterTable tbody tr')
    for tr in tr_list:
        td_list = tr.cssselect("td")
        comp_link_node = td_list[1].cssselect("a")[0]
        assert comp_link_node.get("id").endswith("lnkCompanyName"), "Invalid link node found:%s " % comp_link_node.get("id")
        comp_link = urlparse.urljoin(start_url, comp_link_node.get("href"))
        contact_link_node = td_list[-2].cssselect("a")[0]
        assert contact_link_node.get("id").endswith("lnkSendEmail"), "Invalid link node found:%s " % contact_link_node.get("id")
        matched = re.search(r"\'(nz\_sendEmail.*)\'", contact_link_node.get("onclick"))
        extra_infos = {}
        extra_infos["contact_link"] = urlparse.urljoin(start_url, matched.group(1))
        scrape_info(comp_link, extra_infos)

    # Navigate to Next Page
    ctl00_MainContent_pnlExhibitorList = root.cssselect("#ctl00_MainContent_pnlExhibitorList")[0]
    input_next = ctl00_MainContent_pnlExhibitorList.cssselect("input.rgPageNext")[0]
    input_next_on_click = input_next.get("onclick")
    if (input_next_on_click is None) or ("return false" not in input_next.get("onclick")):
        form_values = {}
        input_next_name = input_next.get("name")
        if is_first_page:
            view_state_value = root.xpath("//input[@name='__VIEWSTATE']")[0].get("value")
        else:
            m = re.search(r"VIEWSTATE\|([^\|]+)", html_content)
            view_state_value = m.group(1)

        form_values = {
            "ctl00$MasterScriptManager": "ctl00$MainContent$ctrlExhibitorList$upContent|" + input_next_name,
            "ctl00_MasterScriptManager_TSM": ";;System.Web.Extensions, Version=3.5.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:3de828f0-5e0d-4c7d-a36b-56a9773c0def:ea597d4b:b25378d2;Telerik.Web.UI, Version=2011.2.712.35, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:326e32e2-cd52-462c-ba2c-db5128e4371b:16e4e7cd:86526ba7:f7645509:24ee1bba:874f8ea2:f46195d3:19620875:490a9d4e:bd8f85e4:e330518b:1e771326:c8618e41:b7778d6c:58366029:aa288e2d;Flan.Controls:en-US:761ee250-93ab-46b1-85e7-8262be0e72f0:27a22b1e;",
            "ctl00_RadStyleSheetManager1_TSSM": ";Telerik.Web.UI, Version=2011.2.712.35, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:326e32e2-cd52-462c-ba2c-db5128e4371b:ef4a543:67d175d:92753c09:91f742eb:9e1572d6:e25b4b77:1c2121e:e24b8e95",
            "ctl00_frmDecorator_ClientState": "",
            "ctl00_Window1_ClientState": "",
            "ctl00_RadWindowManager1_ClientState": "",
            "ctl00$ctlP_welcomeNav$ddlLang": "en-US",
            "ctl00$ctlP_welcomeNav$hdnHome": "../public/nz_ALMyProfile.aspx",
            "ctl00_ctlP_Navigation_radNavigation_ClientState": "",
            "ctl00_LeftNav_txtKeyword_text": "Type your Keyword here",
            "ctl00$LeftNav$txtKeyword": "",
            "ctl00_LeftNav_txtKeyword_ClientState": '{"enabled":true,"emptyMessage":"Type your Keyword here"}',
            "ctl00_ucQuickLinks_radQuickLinks_ClientState": "",
            "ctl00$MainContent$ctrlExhibitorList$radExhibitorList$ctl00$ctl03$ctl01$PageSizeComboBox": "100",
            "ctl00_MainContent_ctrlExhibitorList_radExhibitorList_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState": '{"logEntries":[],"value":"100","text":"100","enabled":true,"checkedIndices":[]}',
            "ctl00_MainContent_ctrlExhibitorList_radExhibitorList_ClientState": "",
            "ctl00$MainContent$ctrlExhibitorList$hdnCustomFieldIDs": "15,16,17,19,14",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": view_state_value,
            "__ASYNCPOST": "true",
            input_next_name: ""
        }

        next_content = scrape(s_url, form_values, 
                    headers=(("User-Agent", user_agent),
                             ("X-MicrosoftAjax", "Delta=true"),
                             (('X-Requested-With', 'XMLHttpRequest')),
                             ("Referer", s_url)))
        
        process_list_page(start_url, next_content, is_first_page=False)
    else:
        print "No More Pages. Finished"


def scrape_site(start_url):
    html_content = scrape(start_url)
    process_list_page(start_url, html_content, is_first_page=True)


scrape_site(s_url)
