# Scraper for the EU Transparency Register

require 'nokogiri'
require 'open-uri'

BASE_URL  = "http://ec.europa.eu"
START_URL = "/transparencyregister/public/consultation/listlobbyists.do?alphabetName=LatinAlphabet"

def get(url)
  uri  = BASE_URL + url
  html = open(uri).read
  doc = Nokogiri::HTML(html)
end

# first level navigation
def tab_urls(url)
  doc = get(url)
  tab_urls = [url]
  tab_urls += doc.css("#sitecontent h2 a").map {|node| node['href']}
end

# second level navigation
def section_urls(url)
  doc = get(url)
  section_urls = doc.css("div.pagination p a").map {|node| node['href']}
end

# retrieve the number of pages of a section
def max_page(doc)
  last_page_link = doc.css("span.pagelinks a").last['href']
  Integer(last_page_link[/p=(\d+)&/,1])
end

# returns [start_url, max_page]
def pagination_info(url)
  doc = get(url)
  pagelinks = doc.css("span.pagelinks a")
  if (pagelinks && !pagelinks.empty? )
    start_url = pagelinks.first['href']
    [start_url, max_page(doc)]
  else
    [url, 1]
  end
end

# replace the page number in the baseurl
def page_url(url, page)
  url.gsub(/p=(\d+)&/, "p=#{page}&")
end

# extract the data from the table of a page
def parse_table(doc)
  rows = doc.css('table#listUsersTable tbody tr')
  data = rows.map do |row|
    id, name, details = row.search('td')
    url = details.search('a').first['href']
    {id: id.content, name: name.content, registry_url: BASE_URL + url}
  end
end

# save to store
def save(record)
  ScraperWiki.save_sqlite(['id'], record)
end

def scrape_section(url)
  start, max = pagination_info(url)
  pages = (1..max).map {|i| page_url(start, i)}
  pages.each {|page| scrape_page(page)}
end

def scrape_page(uri)
  doc = get(uri)
  data = parse_table(doc)
  data.each {|record| save(record)}
end


tabs = tab_urls(START_URL)
sections = tabs.map {|tab| section_urls(tab)}.flatten

sections.each {|section| scrape_section(section)}







# Scraper for the EU Transparency Register

require 'nokogiri'
require 'open-uri'

BASE_URL  = "http://ec.europa.eu"
START_URL = "/transparencyregister/public/consultation/listlobbyists.do?alphabetName=LatinAlphabet"

def get(url)
  uri  = BASE_URL + url
  html = open(uri).read
  doc = Nokogiri::HTML(html)
end

# first level navigation
def tab_urls(url)
  doc = get(url)
  tab_urls = [url]
  tab_urls += doc.css("#sitecontent h2 a").map {|node| node['href']}
end

# second level navigation
def section_urls(url)
  doc = get(url)
  section_urls = doc.css("div.pagination p a").map {|node| node['href']}
end

# retrieve the number of pages of a section
def max_page(doc)
  last_page_link = doc.css("span.pagelinks a").last['href']
  Integer(last_page_link[/p=(\d+)&/,1])
end

# returns [start_url, max_page]
def pagination_info(url)
  doc = get(url)
  pagelinks = doc.css("span.pagelinks a")
  if (pagelinks && !pagelinks.empty? )
    start_url = pagelinks.first['href']
    [start_url, max_page(doc)]
  else
    [url, 1]
  end
end

# replace the page number in the baseurl
def page_url(url, page)
  url.gsub(/p=(\d+)&/, "p=#{page}&")
end

# extract the data from the table of a page
def parse_table(doc)
  rows = doc.css('table#listUsersTable tbody tr')
  data = rows.map do |row|
    id, name, details = row.search('td')
    url = details.search('a').first['href']
    {id: id.content, name: name.content, registry_url: BASE_URL + url}
  end
end

# save to store
def save(record)
  ScraperWiki.save_sqlite(['id'], record)
end

def scrape_section(url)
  start, max = pagination_info(url)
  pages = (1..max).map {|i| page_url(start, i)}
  pages.each {|page| scrape_page(page)}
end

def scrape_page(uri)
  doc = get(uri)
  data = parse_table(doc)
  data.each {|record| save(record)}
end


tabs = tab_urls(START_URL)
sections = tabs.map {|tab| section_urls(tab)}.flatten

sections.each {|section| scrape_section(section)}







