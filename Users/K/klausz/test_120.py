import re
import mechanize
import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import sys
import lxml.html



#Template/Sample from Friedrich Lindenberg

# Newsfeed available (most recent ?): feed://cmiskp.echr.coe.int/rss/JudDec-123-EN.xml

# http://cmiskp.echr.coe.int/tkp197/search.asp?sessionid=80311369&skin=hudoc-en

# from here we should get a session id
# http://www.echr.coe.int/echr/en/hudoc/
# http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en


###############################################################################
# 
# Website:  
# Fields:
#
###############################################################################
 

 
# worked:
response = mechanize.urlopen("http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en")
print response.read()

base_url = 'http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en'

# base_url = 'https://www.unternehmensregister.de/ureg/result.html'
# https://www.unternehmensregister.de/ureg/result.html;jsessionid=2F75FB29FC1AF95F5A67809E1A176B5E.www04-1
#http://scraperwikiviews.com/run/python_mechanize_cheat_sheet/
 
#  Use mechanize to fill the form with a start  parameter, the page will  not come up with content. If there is nothing  there is an empty table
# So we start with '00' 
# Another reason for meachanize was, in the link the page cannot be adressed directly
 
br = mechanize.Browser()
br.set_handle_robots(False)
html = br.open(base_url).read()
# print html #deactivated 201106290945


# print response.read() 
 

# br.select_form("form1")         # works when form has a name 
# br.form = list(br.forms())[0]  # use when form is unnamed
# br.select_form("globalSearchForm")
br.form = list(br.forms())[0]


#table class="mainTable"

# print br.form #deactivated 201106290946
 


# <input id="globalSearchForm:extendedResearchCompanyName" type="text" style="width:175px;height:16px;
# font-size:1.1em;" size="30" value="aa" name="globalSearchForm:extendedResearchCompanyName">
#  <input id="globalSearchForm:hidden_element_used_for_validation_only" type="text" style="display:none;" value="aaa" name="globalSearchForm:hidden_element_used_for_validation_only">
## br["globalSearchForm:extendedResearchCompanyName"] = "00"

#   <input id="pd_metadatalanguage_english" type="checkbox" checked="" onchange="javascript:m_bDirty  = true;" name="pd_metadatalanguage_english">
# <span class="textital">English</span>
#br["pd_pd_metadatalanguage_english"] = ""

# <input id="pd_respondent" class="criteriainput" onchange="javascript:m_bDirty = true;" value="" name="pd_respondent">
#   <input class="lookupButtons" type="button" onclick="javascript:lookup(  'pd_respondent', lookupLanguages() );" value="...">
br["pd_respondent"] = "GERMANY" 
 
#  <input id="pd_kp_date_from" class="criteriainputdate" onchange="javascript:m_bDirty  = true;dateCheck( document.frmSearch.pd_kp_date_from,  document.frmSearch.pd_kp_date_to      );" value="" name="pd_kp_date_from">
br["pd_kp_date_from"] = "01/01/2011" 

#<input id="pd_kp_date_to" class="criteriainputdate" value="18/10/2011" onchange="javascript:m_bDirty  = true;dateCheck( document.frmSearch.pd_kp_date_from,  document.frmSearch.pd_kp_date_to );" name="pd_kp_date_to">
# <span class="textital"> dd/mm/yyyy</span>
br["pd_kp_date_to"] = "01/02/2011" 


html1 = br.submit().read()
# print html1 #deactivated 201106290947
#root = lxml.html.fromstring(html1)
#print root
# for rec in root.cssselect("div.result_item"): #deactivated 201106290950
#for rec in root.cssselect("div.company_result"): #thats where I reduce the data to within the record
#   print lxml.html.tostring(rec)
#sys.exit(0)import re
import mechanize
import scraperwiki
from BeautifulSoup import BeautifulSoup
import mechanize
import sys
import lxml.html



#Template/Sample from Friedrich Lindenberg

# Newsfeed available (most recent ?): feed://cmiskp.echr.coe.int/rss/JudDec-123-EN.xml

# http://cmiskp.echr.coe.int/tkp197/search.asp?sessionid=80311369&skin=hudoc-en

# from here we should get a session id
# http://www.echr.coe.int/echr/en/hudoc/
# http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en


###############################################################################
# 
# Website:  
# Fields:
#
###############################################################################
 

 
# worked:
response = mechanize.urlopen("http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en")
print response.read()

base_url = 'http://cmiskp.echr.coe.int/tkp197/search.asp?skin=hudoc-en'

# base_url = 'https://www.unternehmensregister.de/ureg/result.html'
# https://www.unternehmensregister.de/ureg/result.html;jsessionid=2F75FB29FC1AF95F5A67809E1A176B5E.www04-1
#http://scraperwikiviews.com/run/python_mechanize_cheat_sheet/
 
#  Use mechanize to fill the form with a start  parameter, the page will  not come up with content. If there is nothing  there is an empty table
# So we start with '00' 
# Another reason for meachanize was, in the link the page cannot be adressed directly
 
br = mechanize.Browser()
br.set_handle_robots(False)
html = br.open(base_url).read()
# print html #deactivated 201106290945


# print response.read() 
 

# br.select_form("form1")         # works when form has a name 
# br.form = list(br.forms())[0]  # use when form is unnamed
# br.select_form("globalSearchForm")
br.form = list(br.forms())[0]


#table class="mainTable"

# print br.form #deactivated 201106290946
 


# <input id="globalSearchForm:extendedResearchCompanyName" type="text" style="width:175px;height:16px;
# font-size:1.1em;" size="30" value="aa" name="globalSearchForm:extendedResearchCompanyName">
#  <input id="globalSearchForm:hidden_element_used_for_validation_only" type="text" style="display:none;" value="aaa" name="globalSearchForm:hidden_element_used_for_validation_only">
## br["globalSearchForm:extendedResearchCompanyName"] = "00"

#   <input id="pd_metadatalanguage_english" type="checkbox" checked="" onchange="javascript:m_bDirty  = true;" name="pd_metadatalanguage_english">
# <span class="textital">English</span>
#br["pd_pd_metadatalanguage_english"] = ""

# <input id="pd_respondent" class="criteriainput" onchange="javascript:m_bDirty = true;" value="" name="pd_respondent">
#   <input class="lookupButtons" type="button" onclick="javascript:lookup(  'pd_respondent', lookupLanguages() );" value="...">
br["pd_respondent"] = "GERMANY" 
 
#  <input id="pd_kp_date_from" class="criteriainputdate" onchange="javascript:m_bDirty  = true;dateCheck( document.frmSearch.pd_kp_date_from,  document.frmSearch.pd_kp_date_to      );" value="" name="pd_kp_date_from">
br["pd_kp_date_from"] = "01/01/2011" 

#<input id="pd_kp_date_to" class="criteriainputdate" value="18/10/2011" onchange="javascript:m_bDirty  = true;dateCheck( document.frmSearch.pd_kp_date_from,  document.frmSearch.pd_kp_date_to );" name="pd_kp_date_to">
# <span class="textital"> dd/mm/yyyy</span>
br["pd_kp_date_to"] = "01/02/2011" 


html1 = br.submit().read()
# print html1 #deactivated 201106290947
#root = lxml.html.fromstring(html1)
#print root
# for rec in root.cssselect("div.result_item"): #deactivated 201106290950
#for rec in root.cssselect("div.company_result"): #thats where I reduce the data to within the record
#   print lxml.html.tostring(rec)
#sys.exit(0)