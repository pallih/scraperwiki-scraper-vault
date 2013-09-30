#!/usr/bin/env ruby

# Henare started writing a scraper for the Victorian Liquor License Applications in Python.
# He didn't finish it. So he suggested I write one. So, here I am... writing one.... In Ruby.

require 'mechanize'
require 'date'

# This is the best URL to link to. Ugh. It's just the search page
INFO_URL = "https://liquor.justice.vic.gov.au/alarm_internet"
COMMENT_URL = "http://responsiblealcohol.vic.gov.au/wps/portal/rav/community/concerns/objecting_to_a_liquor_licence_application"

def scrape_index_page(index_page)
  return false if index_page.at('h1').inner_text == "Sorry"
  index_page.search('.result').each do |result|
    title = result.at(".result-title").inner_text
    fields = {}
    result.search(".result-details").each do |d|
      key, value = d.inner_text.split(': ')
      fields[key] = value
    end
    record = {
      'council_reference' => title.split(" ")[0],
      'date_received' => Date.strptime(fields["Application Received Date"], '%d/%m/%Y').to_s,
      'address' => fields["Premises Address"] + ", VIC",
      'date_scraped' => Date.today.to_s,
      'description' => fields["Application Type"],
      'info_url' => INFO_URL,
      'comment_url' => COMMENT_URL,
    }
    notice_text = fields["Public Notice Display Period"]
    unless notice_text == "NOT REQUIRED" || notice_text == "NOT RECORDED*" || notice_text == "TO BE ADVISED"
      date1, date2 = notice_text.split(" - ")
      #puts notice_text
      record['on_notice_from'] = Date.strptime(date1, '%d/%m/%Y').to_s
      record['on_notice_to'] = Date.strptime(date2, '%d/%m/%Y').to_s
    end    

    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  end
  true
end

agent = Mechanize.new

# Doing this as a workaround because there don't appear to be root certificates for Ruby 1.9 installed on
# Scraperwiki. Doesn't really make any difference because we're not sending anything requiring any kind
# of security back and forth
agent.verify_mode = OpenSSL::SSL::VERIFY_NONE

#puts agent.get(url).body

# I don't know about you, but I love navigating to web pages using forms. Who needs links... they're so old & simple!
license_application_search_page = agent.post("https://liquor.justice.vic.gov.au/alarm_internet/alarm_internet.ASP?WCI=index_action&amp;WCU", :index_action_flag => 8, :login_flag => 0)

form = license_application_search_page.forms_with(:name => "form1").first
field1 = form.field_with(:name => "local_gov_area")
field2 = form.field_with(:name => "licence_category")

# Go through all the local government areas collection applications for each one

# Will also need to check each "License Category" individually to ensure that we don't return too
# many applications at once which apparently the system doesn't like. Maybe they couldn't be bothered to
# implement paging? Sigh...

# Using this list because the license categories selection list is populated at runtime with javascript

license_categories = [
  "311 312|BYO Permit",
  "321|Full Club",
  "2000 2009 2010 2012 2100|General",
  "2024 2124 2200 2224 2300 2400 2500 2600 2700|Late night (general)",
  "3024 3124 3200 3300 3400 3500 3600 3700|Late night (on-premises)",
  "5024 5124 5200 5300 5400 5500 5600 5700|Late night (packaged)",
  "3000 3012 3100|On-premises",
  "5000 5009 5010 5012 5100 6010|Packaged liquor",
  "329 337|Pre-retail",
  "360 361|Renewable Limited",
  "4000 4012 4024 4100 4200 4300 4400 4500 4600 4700|Restaurant and cafe",
  "314|Restricted Club",
  "326|Wine &amp; Beer Producer's ",
]

field1.options[1..-1].each do |option|
  option.select
  puts "Going through #{option.value}..."
  unless scrape_index_page(form.submit)
    puts "Now have to try again in a slower way... Because someone couldn't be bothered to implement paging..."
    license_categories.each do |category|
      field2.value = category
      unless scrape_index_page(form.submit)
        raise "Fuck!"
      end
    end
  end
end


#!/usr/bin/env ruby

# Henare started writing a scraper for the Victorian Liquor License Applications in Python.
# He didn't finish it. So he suggested I write one. So, here I am... writing one.... In Ruby.

require 'mechanize'
require 'date'

# This is the best URL to link to. Ugh. It's just the search page
INFO_URL = "https://liquor.justice.vic.gov.au/alarm_internet"
COMMENT_URL = "http://responsiblealcohol.vic.gov.au/wps/portal/rav/community/concerns/objecting_to_a_liquor_licence_application"

def scrape_index_page(index_page)
  return false if index_page.at('h1').inner_text == "Sorry"
  index_page.search('.result').each do |result|
    title = result.at(".result-title").inner_text
    fields = {}
    result.search(".result-details").each do |d|
      key, value = d.inner_text.split(': ')
      fields[key] = value
    end
    record = {
      'council_reference' => title.split(" ")[0],
      'date_received' => Date.strptime(fields["Application Received Date"], '%d/%m/%Y').to_s,
      'address' => fields["Premises Address"] + ", VIC",
      'date_scraped' => Date.today.to_s,
      'description' => fields["Application Type"],
      'info_url' => INFO_URL,
      'comment_url' => COMMENT_URL,
    }
    notice_text = fields["Public Notice Display Period"]
    unless notice_text == "NOT REQUIRED" || notice_text == "NOT RECORDED*" || notice_text == "TO BE ADVISED"
      date1, date2 = notice_text.split(" - ")
      #puts notice_text
      record['on_notice_from'] = Date.strptime(date1, '%d/%m/%Y').to_s
      record['on_notice_to'] = Date.strptime(date2, '%d/%m/%Y').to_s
    end    

    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  end
  true
end

agent = Mechanize.new

# Doing this as a workaround because there don't appear to be root certificates for Ruby 1.9 installed on
# Scraperwiki. Doesn't really make any difference because we're not sending anything requiring any kind
# of security back and forth
agent.verify_mode = OpenSSL::SSL::VERIFY_NONE

#puts agent.get(url).body

# I don't know about you, but I love navigating to web pages using forms. Who needs links... they're so old & simple!
license_application_search_page = agent.post("https://liquor.justice.vic.gov.au/alarm_internet/alarm_internet.ASP?WCI=index_action&amp;WCU", :index_action_flag => 8, :login_flag => 0)

form = license_application_search_page.forms_with(:name => "form1").first
field1 = form.field_with(:name => "local_gov_area")
field2 = form.field_with(:name => "licence_category")

# Go through all the local government areas collection applications for each one

# Will also need to check each "License Category" individually to ensure that we don't return too
# many applications at once which apparently the system doesn't like. Maybe they couldn't be bothered to
# implement paging? Sigh...

# Using this list because the license categories selection list is populated at runtime with javascript

license_categories = [
  "311 312|BYO Permit",
  "321|Full Club",
  "2000 2009 2010 2012 2100|General",
  "2024 2124 2200 2224 2300 2400 2500 2600 2700|Late night (general)",
  "3024 3124 3200 3300 3400 3500 3600 3700|Late night (on-premises)",
  "5024 5124 5200 5300 5400 5500 5600 5700|Late night (packaged)",
  "3000 3012 3100|On-premises",
  "5000 5009 5010 5012 5100 6010|Packaged liquor",
  "329 337|Pre-retail",
  "360 361|Renewable Limited",
  "4000 4012 4024 4100 4200 4300 4400 4500 4600 4700|Restaurant and cafe",
  "314|Restricted Club",
  "326|Wine &amp; Beer Producer's ",
]

field1.options[1..-1].each do |option|
  option.select
  puts "Going through #{option.value}..."
  unless scrape_index_page(form.submit)
    puts "Now have to try again in a slower way... Because someone couldn't be bothered to implement paging..."
    license_categories.each do |category|
      field2.value = category
      unless scrape_index_page(form.submit)
        raise "Fuck!"
      end
    end
  end
end


