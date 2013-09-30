import scraperwiki

# Blank Python
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs
import re
import urllib2
import pdb

base_url = "http://civiccommons.org"
url = "http://civiccommons.org/apps"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())

list_of_links = [] 
for link_tag in soup.findAll('a', href=re.compile('^/software-functions.*')):
   string_temp_link = base_url+link_tag.get('href')
   list_of_links.append(string_temp_link)

for link_tag in soup.findAll('a', href=re.compile('^/civic-function.*')):
   string_temp_link = base_url+link_tag.get('href')
   list_of_links.append(string_temp_link)

for link_tag in soup.findAll('a', href=re.compile('^/software-licenses.*')):
   string_temp_link = base_url+link_tag.get('href')
   list_of_links.append(string_temp_link)

list_of_links = list(set(list_of_links)) 

list_of_next_pages = []
for categorized_apps_url in list_of_links:
   categorized_apps_page = urllib2.urlopen(categorized_apps_url)
   categorized_apps_soup = BeautifulSoup(categorized_apps_page.read())

   last_page_tag = categorized_apps_soup.find('a', title="Go to last page")
   if last_page_tag:
      last_page_url = base_url+last_page_tag.get('href')
      index_value = last_page_url.find("page=") + 5
      base_url_for_next_page = last_page_url[:index_value]
      for pageno in xrange(0, int(parse_qs(urlparse(last_page_url).query)['page'][0]) + 1):
         list_of_next_pages.append(base_url_for_next_page+str(pageno))
      
   else:
      list_of_next_pages.append(categorized_apps_url)
    
all_apps_list_of_links = []
for link_item in list_of_next_pages:
   next_page = urllib2.urlopen(link_item)
   soup_next_page = BeautifulSoup(next_page.read())
   for next_page_link_tag in soup_next_page.findAll('a', href=re.compile('^/apps/.*')):
      string_next_page_temp_link = base_url+next_page_link_tag.get('href')
      all_apps_list_of_links.append(string_next_page_temp_link)

all_apps_list_of_links = list(set(all_apps_list_of_links))  

for app_link_item in all_apps_list_of_links:
    complete_app_description = ""  
    try:
        app_page = urllib2.urlopen(app_link_item)
        app_soup = BeautifulSoup(app_page.read())
        
        app_tag_title = app_soup.find('title')
        title_end_index_value = app_tag_title.string.find(" | Civic Commons")
        app_title = app_tag_title.string[:title_end_index_value]
    #    print app_title
    
        app_div_block = app_soup.find(attrs= {"class" : "field field-name-field-application-description field-type-text-long field-label-hidden clearfix"})
        para = app_div_block.find('p')
        if para:
            while (para.nextSibling <> None):
                if (para == '\n'):
                    para = para.nextSibling
                    continue
                para_desc = para.contents[0]
                unicode_string_para = unicode(para_desc.string)
                complete_app_description = complete_app_description + unicode_string_para
                para = para.nextSibling
        
        list_items = app_div_block.find('li')
        if list_items:
            while (list_items.nextSibling <> None):
                if (list_items == '\n') :
                    list_items = list_items.nextSibling
                    continue
                list_desc = list_items.contents[0]
                unicode_string_list = unicode(list_desc.string)
                complete_app_description = complete_app_description + unicode_string_list
                list_items = list_items.nextSibling
        
    #    print complete_app_description
        
        scraperwiki.sqlite.save(unique_keys=["url"], data={"name":app_title, "url":app_link_item, "description":complete_app_description}, table_name = "army_ants_civic_commons_apps")    
    except URLError, e:
        print e.reason
    except HTTPError, e:
        print e.reason
import scraperwiki

# Blank Python
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs
import re
import urllib2
import pdb

base_url = "http://civiccommons.org"
url = "http://civiccommons.org/apps"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())

list_of_links = [] 
for link_tag in soup.findAll('a', href=re.compile('^/software-functions.*')):
   string_temp_link = base_url+link_tag.get('href')
   list_of_links.append(string_temp_link)

for link_tag in soup.findAll('a', href=re.compile('^/civic-function.*')):
   string_temp_link = base_url+link_tag.get('href')
   list_of_links.append(string_temp_link)

for link_tag in soup.findAll('a', href=re.compile('^/software-licenses.*')):
   string_temp_link = base_url+link_tag.get('href')
   list_of_links.append(string_temp_link)

list_of_links = list(set(list_of_links)) 

list_of_next_pages = []
for categorized_apps_url in list_of_links:
   categorized_apps_page = urllib2.urlopen(categorized_apps_url)
   categorized_apps_soup = BeautifulSoup(categorized_apps_page.read())

   last_page_tag = categorized_apps_soup.find('a', title="Go to last page")
   if last_page_tag:
      last_page_url = base_url+last_page_tag.get('href')
      index_value = last_page_url.find("page=") + 5
      base_url_for_next_page = last_page_url[:index_value]
      for pageno in xrange(0, int(parse_qs(urlparse(last_page_url).query)['page'][0]) + 1):
         list_of_next_pages.append(base_url_for_next_page+str(pageno))
      
   else:
      list_of_next_pages.append(categorized_apps_url)
    
all_apps_list_of_links = []
for link_item in list_of_next_pages:
   next_page = urllib2.urlopen(link_item)
   soup_next_page = BeautifulSoup(next_page.read())
   for next_page_link_tag in soup_next_page.findAll('a', href=re.compile('^/apps/.*')):
      string_next_page_temp_link = base_url+next_page_link_tag.get('href')
      all_apps_list_of_links.append(string_next_page_temp_link)

all_apps_list_of_links = list(set(all_apps_list_of_links))  

for app_link_item in all_apps_list_of_links:
    complete_app_description = ""  
    try:
        app_page = urllib2.urlopen(app_link_item)
        app_soup = BeautifulSoup(app_page.read())
        
        app_tag_title = app_soup.find('title')
        title_end_index_value = app_tag_title.string.find(" | Civic Commons")
        app_title = app_tag_title.string[:title_end_index_value]
    #    print app_title
    
        app_div_block = app_soup.find(attrs= {"class" : "field field-name-field-application-description field-type-text-long field-label-hidden clearfix"})
        para = app_div_block.find('p')
        if para:
            while (para.nextSibling <> None):
                if (para == '\n'):
                    para = para.nextSibling
                    continue
                para_desc = para.contents[0]
                unicode_string_para = unicode(para_desc.string)
                complete_app_description = complete_app_description + unicode_string_para
                para = para.nextSibling
        
        list_items = app_div_block.find('li')
        if list_items:
            while (list_items.nextSibling <> None):
                if (list_items == '\n') :
                    list_items = list_items.nextSibling
                    continue
                list_desc = list_items.contents[0]
                unicode_string_list = unicode(list_desc.string)
                complete_app_description = complete_app_description + unicode_string_list
                list_items = list_items.nextSibling
        
    #    print complete_app_description
        
        scraperwiki.sqlite.save(unique_keys=["url"], data={"name":app_title, "url":app_link_item, "description":complete_app_description}, table_name = "army_ants_civic_commons_apps")    
    except URLError, e:
        print e.reason
    except HTTPError, e:
        print e.reason
