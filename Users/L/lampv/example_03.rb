require 'rubygems'
require 'mechanize'

STARTING_URL = 'http://www.eservices.lmc.nsw.gov.au/DATrackingUI/Modules/Applicationmaster/default.aspx?page=found&1=thismonth&6=F'
COMMENT_URL = 'mailto:leichhardt@lmc.nsw.gov.au?subject='


#
agent = Mechanize.new

# get page
page = agent.get(STARTING_URL)
page = page.forms.first.submit(page.forms.first.button_with(:value => "I Agree"))
page = agent.get(STARTING_URL)



##
#get all das
#Parameters::
# *(Page) *params*:page
#Return:: list of da
#*Author*::
#----------------------------------------------------------------------------
def get_all_das(page)
  while (is_available(page)) do
    get_all_das_in_page(page)
    page = get_next_page(page)
  end
  # case page has a page and the end page
  #get_all_das_in_page(page)
end


##
#is available
#Parameters::
# *(Page) *params*:page
#Return:: true or false
#*Author*::
#----------------------------------------------------------------------------
def is_available(page)
  puts page.body.inspect
  puts page.at('.rgPageLast').inspect
  if !page.at('.rgPageLast').nil? 
    return true
  else
    return false
  end
  
end


##
#get all das in page
#Parameters::
# *(Page) *params*:page
#Return:: list of da in page
#*Author*::
#----------------------------------------------------------------------------
def get_all_das_in_page(page)
  page.search('table tbody tr').each do |tr|
    get_da_summary(page, tr)
  end
end

##
#get page next
#Parameters::
# *(Page) *params*:page
#Return:: page next
#*Author*::
#----------------------------------------------------------------------------
def get_next_page(page)
  next_page_condition = page.at('.rgPageNext')
  form = page.forms.first
  
  # The joy of dealing with ASP.NET
  form['__EVENTTARGET'] = next_page_condition['name']
  form['__EVENTARGUMENT'] = ''
  # It doesn't seem to work without these stupid values being set.
  # Would be good to figure out where precisely in the javascript these values are coming from.
  form['ctl00%24RadScriptManager1']=
    'ctl00%24cphContent%24ctl00%24ctl00%24cphContent%24ctl00%24Radajaxpanel2Panel%7Cctl00%24cphContent%24ctl00%24ctl00%24RadGrid1%24ctl00%24ctl03%24ctl01%24ctl10'
  form['ctl00_RadScriptManager1_HiddenField']=
    '%3B%3BSystem.Web.Extensions%2C%20Version%3D3.5.0.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D31bf3856ad364e35%3Aen-US%3A0d787d5c-3903-4814-ad72-296cea810318%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C%20Version%3D2009.1.527.35%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A1e3fef00-f492-4ed8-96ce-6371bc241e1c%3A16e4e7cd%3Af7645509%3A24ee1bba%3Ae330518b%3A1e771326%3Ac8618e41%3A4cacbc31%3A8e6f0d33%3Aed16cbdc%3A58366029%3Aaa288e2d'
  
  page = form.submit(form.button_with(:name => next_page_condition['name']))
end

##
#get da summary
#Parameters::
# *(tag) *params*:tr tag
#Return:: list of da
#*Author*::
#----------------------------------------------------------------------------
def get_da_summary(page, tr)
  tds = tr.search('td')
    
  h = tds.map{|td| td.inner_html}

  record = {
    'info_url' => (page.uri + tds[0].at('a')['href']).to_s,
    'comment_url' => COMMENT_URL + CGI::escape("Development Application Enquiry: " + clean_whitespace(h[1])),
    'council_reference' => clean_whitespace(h[1]),
    'date_received' => Date.strptime(clean_whitespace(h[2]), '%d/%m/%Y').to_s,
    'address' => clean_whitespace(tds[3].at('b').inner_text),
    'description' => CGI::unescapeHTML(clean_whitespace(h[3].split('<br>')[1..-1].join)),
    'date_scraped' => Date.today.to_s
  }
  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
   # puts "Skipping already saved record " + record['council_reference']
  end
end

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

get_all_das(page)require 'rubygems'
require 'mechanize'

STARTING_URL = 'http://www.eservices.lmc.nsw.gov.au/DATrackingUI/Modules/Applicationmaster/default.aspx?page=found&1=thismonth&6=F'
COMMENT_URL = 'mailto:leichhardt@lmc.nsw.gov.au?subject='


#
agent = Mechanize.new

# get page
page = agent.get(STARTING_URL)
page = page.forms.first.submit(page.forms.first.button_with(:value => "I Agree"))
page = agent.get(STARTING_URL)



##
#get all das
#Parameters::
# *(Page) *params*:page
#Return:: list of da
#*Author*::
#----------------------------------------------------------------------------
def get_all_das(page)
  while (is_available(page)) do
    get_all_das_in_page(page)
    page = get_next_page(page)
  end
  # case page has a page and the end page
  #get_all_das_in_page(page)
end


##
#is available
#Parameters::
# *(Page) *params*:page
#Return:: true or false
#*Author*::
#----------------------------------------------------------------------------
def is_available(page)
  puts page.body.inspect
  puts page.at('.rgPageLast').inspect
  if !page.at('.rgPageLast').nil? 
    return true
  else
    return false
  end
  
end


##
#get all das in page
#Parameters::
# *(Page) *params*:page
#Return:: list of da in page
#*Author*::
#----------------------------------------------------------------------------
def get_all_das_in_page(page)
  page.search('table tbody tr').each do |tr|
    get_da_summary(page, tr)
  end
end

##
#get page next
#Parameters::
# *(Page) *params*:page
#Return:: page next
#*Author*::
#----------------------------------------------------------------------------
def get_next_page(page)
  next_page_condition = page.at('.rgPageNext')
  form = page.forms.first
  
  # The joy of dealing with ASP.NET
  form['__EVENTTARGET'] = next_page_condition['name']
  form['__EVENTARGUMENT'] = ''
  # It doesn't seem to work without these stupid values being set.
  # Would be good to figure out where precisely in the javascript these values are coming from.
  form['ctl00%24RadScriptManager1']=
    'ctl00%24cphContent%24ctl00%24ctl00%24cphContent%24ctl00%24Radajaxpanel2Panel%7Cctl00%24cphContent%24ctl00%24ctl00%24RadGrid1%24ctl00%24ctl03%24ctl01%24ctl10'
  form['ctl00_RadScriptManager1_HiddenField']=
    '%3B%3BSystem.Web.Extensions%2C%20Version%3D3.5.0.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D31bf3856ad364e35%3Aen-US%3A0d787d5c-3903-4814-ad72-296cea810318%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C%20Version%3D2009.1.527.35%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A1e3fef00-f492-4ed8-96ce-6371bc241e1c%3A16e4e7cd%3Af7645509%3A24ee1bba%3Ae330518b%3A1e771326%3Ac8618e41%3A4cacbc31%3A8e6f0d33%3Aed16cbdc%3A58366029%3Aaa288e2d'
  
  page = form.submit(form.button_with(:name => next_page_condition['name']))
end

##
#get da summary
#Parameters::
# *(tag) *params*:tr tag
#Return:: list of da
#*Author*::
#----------------------------------------------------------------------------
def get_da_summary(page, tr)
  tds = tr.search('td')
    
  h = tds.map{|td| td.inner_html}

  record = {
    'info_url' => (page.uri + tds[0].at('a')['href']).to_s,
    'comment_url' => COMMENT_URL + CGI::escape("Development Application Enquiry: " + clean_whitespace(h[1])),
    'council_reference' => clean_whitespace(h[1]),
    'date_received' => Date.strptime(clean_whitespace(h[2]), '%d/%m/%Y').to_s,
    'address' => clean_whitespace(tds[3].at('b').inner_text),
    'description' => CGI::unescapeHTML(clean_whitespace(h[3].split('<br>')[1..-1].join)),
    'date_scraped' => Date.today.to_s
  }
  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
   # puts "Skipping already saved record " + record['council_reference']
  end
end

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

get_all_das(page)