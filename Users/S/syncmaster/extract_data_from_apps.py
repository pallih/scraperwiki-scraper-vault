import scraperwiki

# Blank Python
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs
import re
import urllib2

base_url = "http://civiccommons.org"
#app_url = "http://civiccommons.org/apps/citizen-budget"
#app_url = "http://civiccommons.org/apps/public-works-agency"
#app_url = "http://civiccommons.org/apps/mapbox"
#app_url = "http://civiccommons.org/apps/drupal"
#app_url = "http://civiccommons.org/apps/civiguard"
#app_url = "http://civiccommons.org/apps/red-hat-enterprise-linux"
#app_url = "http://civiccommons.org/apps/geocode-compare"
#app_url = "http://civiccommons.org/apps/votorola"
#app_url = "http://civiccommons.org/apps/public-art-archive"
app_url = "http://civiccommons.org/apps/livestream"


app_page = urllib2.urlopen(app_url)
app_soup = BeautifulSoup(app_page.read())

app_tag_title = app_soup.find('title')
title_end_index_value = app_tag_title.string.find(" | Civic Commons")
app_title = app_tag_title.string[:title_end_index_value]
#print "Title: "
#print app_title

app_div_block = app_soup.find(attrs= {"class" : "field field-name-field-application-description field-type-text-long field-label-hidden clearfix"})
complete_app_description = ""
para = app_div_block.find('p')
if para:
    while (para.nextSibling <> None):
        print "1"
        if (para == '\n'):
            print para
            para = para.nextSibling
            
            continue
        para_desc = para.contents[0]
        print para_desc
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

#print "Description:"
#print complete_app_description

#scraperwiki.sqlite.save(unique_keys=["url"], data={"name":app_title, "url":app_url, "description":complete_app_description}, table_name = "army_ants_civic_commons_apps")

