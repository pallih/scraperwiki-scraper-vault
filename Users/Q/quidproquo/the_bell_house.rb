# Ruby
require 'date'
require 'nokogiri'

def get_title(el)
  el.search('#bellhouse_performer_new').text.strip.split(/\t/)[0]
end

def first_quarter?(month)
  ['jan', 'feb', 'mar', 'apr'].include?(month.downcase)
end

def last_quarter?
  Date.today.month > 8
end

def get_date(el)
  today = Date.today
  divs = el.search('center div')
  day_of_month = divs[1].text
  month = divs[2].text
  year = (first_quarter?(month) && last_quarter?) ? today.year + 1 : today.year
  Date.parse("#{day_of_month} #{month} #{year}")
end

def get_time(el)
  el.search('div').xpath('./b[contains(text(), "pm")]').text.strip
end

def get_details(el)
  ''
end

html = ScraperWiki::scrape("http://www.thebellhouseny.com/calendar.php")
doc = Nokogiri::HTML html
events = []
doc.search('#bellhouse').each do |el|
  event = {
    title: get_title(el),
    date: get_date(el),
    time: get_time(el),
    details: get_details(el)
  }
  events << event
end

events.each do |event|
  p event
  ScraperWiki::save_sqlite(['date', 'time'], event)
end


# Ruby
require 'date'
require 'nokogiri'

def get_title(el)
  el.search('#bellhouse_performer_new').text.strip.split(/\t/)[0]
end

def first_quarter?(month)
  ['jan', 'feb', 'mar', 'apr'].include?(month.downcase)
end

def last_quarter?
  Date.today.month > 8
end

def get_date(el)
  today = Date.today
  divs = el.search('center div')
  day_of_month = divs[1].text
  month = divs[2].text
  year = (first_quarter?(month) && last_quarter?) ? today.year + 1 : today.year
  Date.parse("#{day_of_month} #{month} #{year}")
end

def get_time(el)
  el.search('div').xpath('./b[contains(text(), "pm")]').text.strip
end

def get_details(el)
  ''
end

html = ScraperWiki::scrape("http://www.thebellhouseny.com/calendar.php")
doc = Nokogiri::HTML html
events = []
doc.search('#bellhouse').each do |el|
  event = {
    title: get_title(el),
    date: get_date(el),
    time: get_time(el),
    details: get_details(el)
  }
  events << event
end

events.each do |event|
  p event
  ScraperWiki::save_sqlite(['date', 'time'], event)
end


