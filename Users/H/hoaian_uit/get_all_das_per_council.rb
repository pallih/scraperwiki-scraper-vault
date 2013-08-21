require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'json'


STARTING_URL = 'http://fiverr.com/gigs/search?utf8=%E2%9C%93&query=pinterest+followers&order=rating&x=-625&y=-151'
COMMENT_URL = 'mailto:leichhardt@lmc.nsw.gov.au?subject='


def is_next_page_available(page)
  next_page_condition = page.at('.rgPageNext')
  unless next_page_condition.nil? || next_page_condition['onclick'] =~ /return false/
    return true
  else
    return false
  end
end

def get_list_page(page)
  list_page = []
  while(is_next_page_available(page)) do
    list_page << page
    page = get_next_page(page)
  end
  list_page << page
  puts << page.length
end

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
end


##
#is available
#Parameters::
# *(Page) *params*:page
#Return:: true or false
#*Author*::
#----------------------------------------------------------------------------
def is_available(page)
  next_page_condition = page.at('.rgPageNext')
  unless next_page_condition.nil? || next_page_condition['onclick'] =~ /return false/
    return true
  else
    return false
  end
end

##
#get a page
#Parameters::
# *(Page) *params*:page
#Return:: list of da
#*Author*::
#----------------------------------------------------------------------------
def get_a_page(page)
  return page
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
    puts "Skipping already saved record " + record['council_reference']
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

# new ================
ORIGIN_URL = 'http://fiverr.com'

def process_link link
  page = @agent.get(link['href'])
  
  # get description
  record = {
  :url => ORIGIN_URL + link['href'],
  :subject => link.inner_text,
  :desc => page.search('.gig-desc span').inner_html,
  :user_name => page.search('.gig-stats.prime a').inner_text,
  :user_name_url => ORIGIN_URL + page.search('.gig-stats.prime a').first['href']
  }

  ScraperWiki.save_sqlite(['url'], record)
  
end

def process_links links
  links.each {|item| process_link item}
end

# main ---------------------------------------------------------------------
@agent = Mechanize.new

# get page
total = 0
page_num  = 1
links = nil

until links && links.count == 0 do
  page = @agent.get("#{STARTING_URL}&page=" + page_num.to_s)
  links = page.search('.content h2 a')
  total += links.count
  
  # with each link
  process_links links
end





