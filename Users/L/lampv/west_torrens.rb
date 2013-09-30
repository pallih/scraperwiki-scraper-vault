# This scraper is to scrape the summary of all Development Applications for a Sample Council
# The summary of a Development Application includes:

# 1. council_reference: The unique identification assigned for a Development Application by the authority

#    Example: 'TA/00323/2012'

# 2. address: The physical address that the Development Application relates to. This will be geocoded so doesn't need to be a specific format
#    but obviously the more explicit it is the more likely it will be successfully geo-coded.
#    If the original address did not include the state (e.g. "QLD") at the end, then add it.

#    Example: '1 Sowerby St, Goulburn, NSW'

# 3. description: A text description of what the Development Application seeks to carry out.

#    Example: 'Ground floor alterations to rear and first floor addition'

# 4. info_url:  A URL that provides more information about the Development Application.
#    This should be a persistent URL that preferably is specific to this particular Development Application.
#    In many cases councils force users to click through a license to access Development Application.
#    In this case be careful about what URL you provide. Test clicking the link in a browser that hasn't established a session
#    with the council's site to ensure you will be able to click the link and not be presented with an error.

#    Example: 'http://foo.gov.au/app?key=527230'

# 5. comment_url:  A URL where users can provide a response to council about this particular Development Application.
#    As in info_url this needs to be a persistent URL and should be specific to this particular Development Application if possible.
#    Email mailto links are also valid in this field.

#    Example: 'http://foo.gov.au/comment?key=527230'

# 6. date_scraped:  The date that the scraper collects this data (i.e. now). Should be in ISO 8601 format.
#    Use the following Ruby code: Date.today.to_s

#    Example: '2012-08-01'

# History: December 27, 2012
# By nhuanvn

# Required libraries

require 'rubygems'
require 'mechanize'

# The starting URL to get Development Applications from

STARTING_URL = 'https://epathway.wtcc.sa.gov.au/ePathway/Production/Web/default.aspx'


# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.
# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.
# Email mailto links are also valid in this field.

COMMENT_URL_PREFIX = ''


##
#get_all_das
#Parameters::
# *(Page) *params*:page
#Return:: All Development Applications from this council
#*Author*::
#----------------------------------------------------------------------------
def get_all_das(page)
  while (is_available(page)) do
    get_all_das_in_page(page)
    page = get_next_page(page)
  end
end


##
#is_available
#Parameters::
# *(Page) *params*:page
#Return:: Return true if the page is available for scraping Development Applications. Return false otherwise
#*Author*::
#----------------------------------------------------------------------------
def is_available(page)
  # Todo: Return true if the page is available for scraping Development Applications. Return false otherwise
  return !page.nil? 
end

##
#get_all_das_in_page

#Parameters::
# *(Page) *params*:page
#Return:: list of da in page
#*Author*::
#----------------------------------------------------------------------------
def get_all_das_in_page(page)
  # Todo: For each element of the page that contains the Development Application, get Development Application Summary.
  # For example:

  page.search('table.syn_applicationListTable tr').each do |tr|
    p tr
    get_da_summary(page, tr)
  end
end

##
#is available
#Parameters::
# *(Page) *params*:page
#Return:: true or false
#*Author*::
#----------------------------------------------------------------------------
def has_next_page(page)
  next_page_condition = page.at('input[id$=nextPageHyperLink]')
  unless next_page_condition.nil? || next_page_condition['onclick'] =~ /return false/
    return true
  else
    return false
  end
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_next_page(page)
  if has_next_page(page)
    next_page_condition = page.at('input[id$=nextPageHyperLink]')
    form = page.forms.first
  
    # The joy of dealing with ASP.NET
    form['__EVENTTARGET'] = next_page_condition['name']
    form['__EVENTARGUMENT'] = ''
    # It doesn't seem to work without these stupid values being set.
    # Would be good to figure out where precisely in the javascript these values are coming from.
    form['ctl00%24RadScriptManager1']=
'ctl00%24cphContent%24ctl00%24ctl00%24cphContent%24ctl00%24Radajaxpanel2Panel%7Cctl00%24cphContent%24ctl00%24ctl00%24RadGrid1%24ctl00%24ctl03%24ctl01%24ctl10'
    form['ctl00_RadScriptManager1_HiddenField']=
    '/wEPDwULLTE0MTExMDU2MDAPZBYCZg9kFgICAQ9kFgYCAw9kFgICBw9kFgICAg9kFgICAQ88KwANAgAPFgIeC18hRGF0YUJvdW5kZ2QMFCsABQUTMjowLDA6MCwwOjEsMDoyLDA6MxQrAAIWDB4EVGV4dAUPR2VuZXJhbCBFbnF1aXJ5HgZUYXJnZXQFBl9ibGFuax4HRW5hYmxlZGceClNlbGVjdGFibGVoHghEYXRhUGF0aAUgLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9MV0eCURhdGFCb3VuZGcUKwADBQcwOjAsMDoxFCsAAhYMHwEFDUVucXVpcnkgTGlzdHMeC05hdmlnYXRlVXJsBTkvZVBhdGh3YXkvUHJvZHVjdGlvbi9XZWIvR2VuZXJhbEVucXVpcnkvRW5xdWlyeUxpc3RzLmFzcHgfA2cfBGcfBQUwLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9MV0vKltwb3NpdGlvbigpPTFdHwZnZBQrAAIWDB8BBRNBcHBsaWNhdGlvbiBFbnF1aXJ5HwcFSC9lUGF0aHdheS9Qcm9kdWN0aW9uL1dlYi9HZW5lcmFsRW5xdWlyeS9FbnF1aXJ5TGlzdHMuYXNweD9Nb2R1bGVDb2RlPUxBUB8DZx8EZx8FBTAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9Ml0fBmdkFCsAAhYKHwEFBU90aGVyHwNnHwRoHwUFIC8qW3Bvc2l0aW9uKCk9MV0vKltwb3NpdGlvbigpPTJdHwZnFCsAAwUHMDowLDA6MRQrAAIWDh8BBQRIZWxwHwcFRC9lUGF0aHdheS9Qcm9kdWN0aW9uL1dlYi9oZWxwL2hlbHAuYXNweD9wYWdlPUVucXVpcnlTdW1tYXJ5Vmlldy5hc3B4HwIFBl9ibGFuax8DZx8EZx8FBTAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0yXS8qW3Bvc2l0aW9uKCk9MV0fBmdkFCsAAhYOHwEFCkNvbnRhY3QgVXMfBwUST3RoZXIvQ29udGFjdC5hc3B4HwIFBl9ibGFuax8DZx8EZx8FBTAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0yXS8qW3Bvc2l0aW9uKCk9Ml0fBmdkFCsAAhYMHwEFBEhvbWUfBwUlL2VQYXRod2F5L1Byb2R1Y3Rpb24vV2ViL2RlZmF1bHQuYXNweB8DZx8EZx8FBSAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0zXR8GZ2QUKwACFg4fAQUESGVscB8HBUQvZVBhdGh3YXkvUHJvZHVjdGlvbi9XZWIvaGVscC9oZWxwLmFzcHg/cGFnZT1FbnF1aXJ5U3VtbWFyeVZpZXcuYXNweB8CBQZfYmxhbmsfA2cfBGcfBQUgLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9NF0fBmdkZAIFD2QWCgIBD2QWAmYPZBYEZg9kFgJmD2QWAgIBDw8WAh8BBQxTdW1tYXJ5IFZpZXdkZAIBD2QWAmYPZBYCZg9kFgJmD2QWBGYPZBYCZg8PFgIeCEltYWdlVXJsBS4vZVBhdGh3YXkvUHJvZHVjdGlvbi9XZWIvSW1hZ2VzL3N0YWdlLWJhY2suZ2lmZGQCAQ9kFgJmDw8WAh8IBS4vZVBhdGh3YXkvUHJvZHVjdGlvbi9XZWIvSW1hZ2VzL3N0YWdlLW5leHQuZ2lmZGQCBQ8PFgYeCENzc0NsYXNzBRVBbHRlcm5hdGVDb250ZW50UGFuZWweB1Rvb2xUaXBlHgRfIVNCAgJkZAIHDw8WBh8BBUxVbmZvcnR1bmF0ZWx5IGZvciBzZWN1cml0eSByZWFzb25zIHlvdSBhcmUgbm90IGFsbG93ZWQgdG8gc2VlIHRoZXNlIHJlc3VsdHMuHwplHgdWaXNpYmxlaGRkAgkPZBYCZg9kFgICAQ9kFgRmD2QWAmYPZBYCZg8PFgIfAQUNUGFnZSAzIG9mIDI1MGRkAgEPZBYEZg9kFgQCAQ8PFgYeC1Bvc3RCYWNrVXJsBTV+L0dlbmVyYWxFbnF1aXJ5L0VucXVpcnlTdW1tYXJ5Vmlldy5hc3B4P1BhZ2VOdW1iZXI9MR8KBRFGaXJzdCBwYWdlIDEgLSAzMB8MZ2RkAgIPDxYGHwxnHw0FNX4vR2VuZXJhbEVucXVpcnkvRW5xdWlyeVN1bW1hcnlWaWV3LmFzcHg/UGFnZU51bWJlcj0yHwoFFVByZXZpb3VzIHBhZ2UgMzEgLSA2MGRkAgIPZBYEZg8PFgQfDQU1fi9HZW5lcmFsRW5xdWlyeS9FbnF1aXJ5U3VtbWFyeVZpZXcuYXNweD9QYWdlTnVtYmVyPTQfCgUSTmV4dCBwYWdlIDkxIC0gMTIwZGQCAQ8PFgQfDQU3fi9HZW5lcmFsRW5xdWlyeS9FbnF1aXJ5U3VtbWFyeVZpZXcuYXNweD9QYWdlTnVtYmVyPTI1MB8KBRVMYXN0IHBhZ2UgNzQ3MSAtIDc0OTNkZAINDw8WBB8BBTdUaGVyZSBhcmUgbm8gU2VhcmNoIFR5cGVzIHNldCB1cCBmb3IgdGhpcyBFbnF1aXJ5IExpc3QuHwxoZGQCBw8PFgIfDGhkFgICAQ9kFgJmD2QWAmYPZBYCAgEPDxYCHwxoZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgYFG2N0bDAwJE1haW5Cb2R5Q29udGVudCRjdGwwNQUnY3RsMDAkTWFpbkJvZHlDb250ZW50JENhbmNlbEltYWdlQnV0dG9uBTdjdGwwMCRNYWluQm9keUNvbnRlbnQkbVBhZ2luZ0NvbnRyb2wkZmlyc3RQYWdlSHlwZXJMaW5rBTpjdGwwMCRNYWluQm9keUNvbnRlbnQkbVBhZ2luZ0NvbnRyb2wkcHJldmlvdXNQYWdlSHlwZXJMaW5rBTZjdGwwMCRNYWluQm9keUNvbnRlbnQkbVBhZ2luZ0NvbnRyb2wkbmV4dFBhZ2VIeXBlckxpbmsFNmN0bDAwJE1haW5Cb2R5Q29udGVudCRtUGFnaW5nQ29udHJvbCRsYXN0UGFnZUh5cGVyTGluay4+4F7WI7vf96SLVT5cy4YwSrFK'
  
    button = form.button_with(:name => next_page_condition['name'])
 
    page = form.click_button(button)
    return page

  else
    return nil
  end
end

##
#get_da_summary

#Parameters::
# *(tag) *params*:da_container tag
#Return:: The Development Application Summary which contains the list of fields as described on the top of this source file
#*Author*::
#----------------------------------------------------------------------------
def get_da_summary(page, da_container)
  # Todo: Put your code to process the da_container to get the Development Application Summary here
  
  tds = da_container.search('td')

  record = {
    'info_url' => (page.uri + tds[0].at('a')['href']).to_s,
    'comment_url' => COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + clean_whitespace(tds[0].at('a').inner_text)),
    'council_reference' => clean_whitespace(tds[0].at('a').inner_text),
    'date_received' => Date.strptime(clean_whitespace(tds[1].at('span').inner_text), '%d/%m/%Y').to_s,
    'address' => clean_whitespace(tds[2].at('div').inner_text),
    'description' => CGI::unescapeHTML(clean_whitespace(tds[3].at('div').inner_text)),
    'status' => CGI::unescapeHTML(clean_whitespace(tds[4].at('div').inner_text)),
    'lodgement_date' => Date.strptime(clean_whitespace(tds[5].at('span').inner_text), '%d/%m/%Y').to_s,
    'date_scraped' => Date.today.to_s
  }
  #if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty?
    ScraperWiki.save_sqlite(['council_reference'], record)
  #else
  #  puts "Skipping already saved record " + record['council_reference']
  #end
end

###############################################################################################
# Start of helper functions section
###############################################################################################

##
#clean whitespace
#Parameters::
# *(tag) *params*: a tag
#Return::a tag
#*Author*::
#----------------------------------------------------------------------------
def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

###############################################################################################
# End of helper functions section
###############################################################################################



###############################################################################################
# The code to scrape will start running here
###############################################################################################

@agent = Mechanize.new do |a|
  a.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

page = @agent.get(STARTING_URL)
page = page.link_with(:href =>"GeneralEnquiry/EnquiryLists.aspx").click
p "aaaaa"

first_page_form = page.forms.first
first_page_form.add_field!('__EVENTTARGET','ctl00$MainBodyContent$mGeneralEnquirySearchControl$mTabControl$tabControlMenu')
first_page_form.add_field!('__EVENTARGUMENT','1')

#abc = first_page_form.field_with(:value => /mTabControl\$ti=1/)

second_page_address_search_tab = first_page_form.submit
p "pvlam"
p second_page_address_search_tab.body



#get_all_das(page)
# This scraper is to scrape the summary of all Development Applications for a Sample Council
# The summary of a Development Application includes:

# 1. council_reference: The unique identification assigned for a Development Application by the authority

#    Example: 'TA/00323/2012'

# 2. address: The physical address that the Development Application relates to. This will be geocoded so doesn't need to be a specific format
#    but obviously the more explicit it is the more likely it will be successfully geo-coded.
#    If the original address did not include the state (e.g. "QLD") at the end, then add it.

#    Example: '1 Sowerby St, Goulburn, NSW'

# 3. description: A text description of what the Development Application seeks to carry out.

#    Example: 'Ground floor alterations to rear and first floor addition'

# 4. info_url:  A URL that provides more information about the Development Application.
#    This should be a persistent URL that preferably is specific to this particular Development Application.
#    In many cases councils force users to click through a license to access Development Application.
#    In this case be careful about what URL you provide. Test clicking the link in a browser that hasn't established a session
#    with the council's site to ensure you will be able to click the link and not be presented with an error.

#    Example: 'http://foo.gov.au/app?key=527230'

# 5. comment_url:  A URL where users can provide a response to council about this particular Development Application.
#    As in info_url this needs to be a persistent URL and should be specific to this particular Development Application if possible.
#    Email mailto links are also valid in this field.

#    Example: 'http://foo.gov.au/comment?key=527230'

# 6. date_scraped:  The date that the scraper collects this data (i.e. now). Should be in ISO 8601 format.
#    Use the following Ruby code: Date.today.to_s

#    Example: '2012-08-01'

# History: December 27, 2012
# By nhuanvn

# Required libraries

require 'rubygems'
require 'mechanize'

# The starting URL to get Development Applications from

STARTING_URL = 'https://epathway.wtcc.sa.gov.au/ePathway/Production/Web/default.aspx'


# COMMENT_URL_PREFIX: The prefix of the URL where users can provide a response to the council about a particular Development Application.
# That URL needs to be a persistent URL and should be specific to a particular Development Application if possible.
# Email mailto links are also valid in this field.

COMMENT_URL_PREFIX = ''


##
#get_all_das
#Parameters::
# *(Page) *params*:page
#Return:: All Development Applications from this council
#*Author*::
#----------------------------------------------------------------------------
def get_all_das(page)
  while (is_available(page)) do
    get_all_das_in_page(page)
    page = get_next_page(page)
  end
end


##
#is_available
#Parameters::
# *(Page) *params*:page
#Return:: Return true if the page is available for scraping Development Applications. Return false otherwise
#*Author*::
#----------------------------------------------------------------------------
def is_available(page)
  # Todo: Return true if the page is available for scraping Development Applications. Return false otherwise
  return !page.nil? 
end

##
#get_all_das_in_page

#Parameters::
# *(Page) *params*:page
#Return:: list of da in page
#*Author*::
#----------------------------------------------------------------------------
def get_all_das_in_page(page)
  # Todo: For each element of the page that contains the Development Application, get Development Application Summary.
  # For example:

  page.search('table.syn_applicationListTable tr').each do |tr|
    p tr
    get_da_summary(page, tr)
  end
end

##
#is available
#Parameters::
# *(Page) *params*:page
#Return:: true or false
#*Author*::
#----------------------------------------------------------------------------
def has_next_page(page)
  next_page_condition = page.at('input[id$=nextPageHyperLink]')
  unless next_page_condition.nil? || next_page_condition['onclick'] =~ /return false/
    return true
  else
    return false
  end
end

##
#get_next_page
#Parameters::
# *(Page) *params*:page
#Return:: The next page to be scraped
#*Author*::
#----------------------------------------------------------------------------
def get_next_page(page)
  if has_next_page(page)
    next_page_condition = page.at('input[id$=nextPageHyperLink]')
    form = page.forms.first
  
    # The joy of dealing with ASP.NET
    form['__EVENTTARGET'] = next_page_condition['name']
    form['__EVENTARGUMENT'] = ''
    # It doesn't seem to work without these stupid values being set.
    # Would be good to figure out where precisely in the javascript these values are coming from.
    form['ctl00%24RadScriptManager1']=
'ctl00%24cphContent%24ctl00%24ctl00%24cphContent%24ctl00%24Radajaxpanel2Panel%7Cctl00%24cphContent%24ctl00%24ctl00%24RadGrid1%24ctl00%24ctl03%24ctl01%24ctl10'
    form['ctl00_RadScriptManager1_HiddenField']=
    '/wEPDwULLTE0MTExMDU2MDAPZBYCZg9kFgICAQ9kFgYCAw9kFgICBw9kFgICAg9kFgICAQ88KwANAgAPFgIeC18hRGF0YUJvdW5kZ2QMFCsABQUTMjowLDA6MCwwOjEsMDoyLDA6MxQrAAIWDB4EVGV4dAUPR2VuZXJhbCBFbnF1aXJ5HgZUYXJnZXQFBl9ibGFuax4HRW5hYmxlZGceClNlbGVjdGFibGVoHghEYXRhUGF0aAUgLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9MV0eCURhdGFCb3VuZGcUKwADBQcwOjAsMDoxFCsAAhYMHwEFDUVucXVpcnkgTGlzdHMeC05hdmlnYXRlVXJsBTkvZVBhdGh3YXkvUHJvZHVjdGlvbi9XZWIvR2VuZXJhbEVucXVpcnkvRW5xdWlyeUxpc3RzLmFzcHgfA2cfBGcfBQUwLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9MV0vKltwb3NpdGlvbigpPTFdHwZnZBQrAAIWDB8BBRNBcHBsaWNhdGlvbiBFbnF1aXJ5HwcFSC9lUGF0aHdheS9Qcm9kdWN0aW9uL1dlYi9HZW5lcmFsRW5xdWlyeS9FbnF1aXJ5TGlzdHMuYXNweD9Nb2R1bGVDb2RlPUxBUB8DZx8EZx8FBTAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9Ml0fBmdkFCsAAhYKHwEFBU90aGVyHwNnHwRoHwUFIC8qW3Bvc2l0aW9uKCk9MV0vKltwb3NpdGlvbigpPTJdHwZnFCsAAwUHMDowLDA6MRQrAAIWDh8BBQRIZWxwHwcFRC9lUGF0aHdheS9Qcm9kdWN0aW9uL1dlYi9oZWxwL2hlbHAuYXNweD9wYWdlPUVucXVpcnlTdW1tYXJ5Vmlldy5hc3B4HwIFBl9ibGFuax8DZx8EZx8FBTAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0yXS8qW3Bvc2l0aW9uKCk9MV0fBmdkFCsAAhYOHwEFCkNvbnRhY3QgVXMfBwUST3RoZXIvQ29udGFjdC5hc3B4HwIFBl9ibGFuax8DZx8EZx8FBTAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0yXS8qW3Bvc2l0aW9uKCk9Ml0fBmdkFCsAAhYMHwEFBEhvbWUfBwUlL2VQYXRod2F5L1Byb2R1Y3Rpb24vV2ViL2RlZmF1bHQuYXNweB8DZx8EZx8FBSAvKltwb3NpdGlvbigpPTFdLypbcG9zaXRpb24oKT0zXR8GZ2QUKwACFg4fAQUESGVscB8HBUQvZVBhdGh3YXkvUHJvZHVjdGlvbi9XZWIvaGVscC9oZWxwLmFzcHg/cGFnZT1FbnF1aXJ5U3VtbWFyeVZpZXcuYXNweB8CBQZfYmxhbmsfA2cfBGcfBQUgLypbcG9zaXRpb24oKT0xXS8qW3Bvc2l0aW9uKCk9NF0fBmdkZAIFD2QWCgIBD2QWAmYPZBYEZg9kFgJmD2QWAgIBDw8WAh8BBQxTdW1tYXJ5IFZpZXdkZAIBD2QWAmYPZBYCZg9kFgJmD2QWBGYPZBYCZg8PFgIeCEltYWdlVXJsBS4vZVBhdGh3YXkvUHJvZHVjdGlvbi9XZWIvSW1hZ2VzL3N0YWdlLWJhY2suZ2lmZGQCAQ9kFgJmDw8WAh8IBS4vZVBhdGh3YXkvUHJvZHVjdGlvbi9XZWIvSW1hZ2VzL3N0YWdlLW5leHQuZ2lmZGQCBQ8PFgYeCENzc0NsYXNzBRVBbHRlcm5hdGVDb250ZW50UGFuZWweB1Rvb2xUaXBlHgRfIVNCAgJkZAIHDw8WBh8BBUxVbmZvcnR1bmF0ZWx5IGZvciBzZWN1cml0eSByZWFzb25zIHlvdSBhcmUgbm90IGFsbG93ZWQgdG8gc2VlIHRoZXNlIHJlc3VsdHMuHwplHgdWaXNpYmxlaGRkAgkPZBYCZg9kFgICAQ9kFgRmD2QWAmYPZBYCZg8PFgIfAQUNUGFnZSAzIG9mIDI1MGRkAgEPZBYEZg9kFgQCAQ8PFgYeC1Bvc3RCYWNrVXJsBTV+L0dlbmVyYWxFbnF1aXJ5L0VucXVpcnlTdW1tYXJ5Vmlldy5hc3B4P1BhZ2VOdW1iZXI9MR8KBRFGaXJzdCBwYWdlIDEgLSAzMB8MZ2RkAgIPDxYGHwxnHw0FNX4vR2VuZXJhbEVucXVpcnkvRW5xdWlyeVN1bW1hcnlWaWV3LmFzcHg/UGFnZU51bWJlcj0yHwoFFVByZXZpb3VzIHBhZ2UgMzEgLSA2MGRkAgIPZBYEZg8PFgQfDQU1fi9HZW5lcmFsRW5xdWlyeS9FbnF1aXJ5U3VtbWFyeVZpZXcuYXNweD9QYWdlTnVtYmVyPTQfCgUSTmV4dCBwYWdlIDkxIC0gMTIwZGQCAQ8PFgQfDQU3fi9HZW5lcmFsRW5xdWlyeS9FbnF1aXJ5U3VtbWFyeVZpZXcuYXNweD9QYWdlTnVtYmVyPTI1MB8KBRVMYXN0IHBhZ2UgNzQ3MSAtIDc0OTNkZAINDw8WBB8BBTdUaGVyZSBhcmUgbm8gU2VhcmNoIFR5cGVzIHNldCB1cCBmb3IgdGhpcyBFbnF1aXJ5IExpc3QuHwxoZGQCBw8PFgIfDGhkFgICAQ9kFgJmD2QWAmYPZBYCAgEPDxYCHwxoZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgYFG2N0bDAwJE1haW5Cb2R5Q29udGVudCRjdGwwNQUnY3RsMDAkTWFpbkJvZHlDb250ZW50JENhbmNlbEltYWdlQnV0dG9uBTdjdGwwMCRNYWluQm9keUNvbnRlbnQkbVBhZ2luZ0NvbnRyb2wkZmlyc3RQYWdlSHlwZXJMaW5rBTpjdGwwMCRNYWluQm9keUNvbnRlbnQkbVBhZ2luZ0NvbnRyb2wkcHJldmlvdXNQYWdlSHlwZXJMaW5rBTZjdGwwMCRNYWluQm9keUNvbnRlbnQkbVBhZ2luZ0NvbnRyb2wkbmV4dFBhZ2VIeXBlckxpbmsFNmN0bDAwJE1haW5Cb2R5Q29udGVudCRtUGFnaW5nQ29udHJvbCRsYXN0UGFnZUh5cGVyTGluay4+4F7WI7vf96SLVT5cy4YwSrFK'
  
    button = form.button_with(:name => next_page_condition['name'])
 
    page = form.click_button(button)
    return page

  else
    return nil
  end
end

##
#get_da_summary

#Parameters::
# *(tag) *params*:da_container tag
#Return:: The Development Application Summary which contains the list of fields as described on the top of this source file
#*Author*::
#----------------------------------------------------------------------------
def get_da_summary(page, da_container)
  # Todo: Put your code to process the da_container to get the Development Application Summary here
  
  tds = da_container.search('td')

  record = {
    'info_url' => (page.uri + tds[0].at('a')['href']).to_s,
    'comment_url' => COMMENT_URL_PREFIX + CGI::escape("Development Application Enquiry: " + clean_whitespace(tds[0].at('a').inner_text)),
    'council_reference' => clean_whitespace(tds[0].at('a').inner_text),
    'date_received' => Date.strptime(clean_whitespace(tds[1].at('span').inner_text), '%d/%m/%Y').to_s,
    'address' => clean_whitespace(tds[2].at('div').inner_text),
    'description' => CGI::unescapeHTML(clean_whitespace(tds[3].at('div').inner_text)),
    'status' => CGI::unescapeHTML(clean_whitespace(tds[4].at('div').inner_text)),
    'lodgement_date' => Date.strptime(clean_whitespace(tds[5].at('span').inner_text), '%d/%m/%Y').to_s,
    'date_scraped' => Date.today.to_s
  }
  #if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty?
    ScraperWiki.save_sqlite(['council_reference'], record)
  #else
  #  puts "Skipping already saved record " + record['council_reference']
  #end
end

###############################################################################################
# Start of helper functions section
###############################################################################################

##
#clean whitespace
#Parameters::
# *(tag) *params*: a tag
#Return::a tag
#*Author*::
#----------------------------------------------------------------------------
def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

###############################################################################################
# End of helper functions section
###############################################################################################



###############################################################################################
# The code to scrape will start running here
###############################################################################################

@agent = Mechanize.new do |a|
  a.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

page = @agent.get(STARTING_URL)
page = page.link_with(:href =>"GeneralEnquiry/EnquiryLists.aspx").click
p "aaaaa"

first_page_form = page.forms.first
first_page_form.add_field!('__EVENTTARGET','ctl00$MainBodyContent$mGeneralEnquirySearchControl$mTabControl$tabControlMenu')
first_page_form.add_field!('__EVENTARGUMENT','1')

#abc = first_page_form.field_with(:value => /mTabControl\$ti=1/)

second_page_address_search_tab = first_page_form.submit
p "pvlam"
p second_page_address_search_tab.body



#get_all_das(page)
