require 'rubygems'
require 'hpricot'
require 'open-uri'

base_url = "http://www.cttt.nsw.gov.au"

list_page = Hpricot(open("#{base_url}/Dispute_resolution/Hearing_lists.html"))

# Get all of the links, we're going visiting
(list_page/"//td").search("a").each do |l|
  page = Hpricot(open(base_url + l.attributes["href"]))
  
  # These few places have an extra link on their page
  exceptions = [
    "Hurstville",
    "Liverpool",
    "Newcastle",
    "Parramatta",
    "Penrith",
    "Sydney",
    "Tamworth",
    "Wollongong"
  ]
  link = 1
  if exceptions.index(l.inner_text)
    link = 2
  end
  
  url = (page/'div#contentstart').search("a")[link].attributes["href"]
  
  venue = {
    'postcode' => url[-4..-1],
    'location' => l.inner_text,
    'URL' => url
  }

  ScraperWiki.save(['postcode'], venue)
end

require 'rubygems'
require 'hpricot'
require 'open-uri'

base_url = "http://www.cttt.nsw.gov.au"

list_page = Hpricot(open("#{base_url}/Dispute_resolution/Hearing_lists.html"))

# Get all of the links, we're going visiting
(list_page/"//td").search("a").each do |l|
  page = Hpricot(open(base_url + l.attributes["href"]))
  
  # These few places have an extra link on their page
  exceptions = [
    "Hurstville",
    "Liverpool",
    "Newcastle",
    "Parramatta",
    "Penrith",
    "Sydney",
    "Tamworth",
    "Wollongong"
  ]
  link = 1
  if exceptions.index(l.inner_text)
    link = 2
  end
  
  url = (page/'div#contentstart').search("a")[link].attributes["href"]
  
  venue = {
    'postcode' => url[-4..-1],
    'location' => l.inner_text,
    'URL' => url
  }

  ScraperWiki.save(['postcode'], venue)
end

require 'rubygems'
require 'hpricot'
require 'open-uri'

base_url = "http://www.cttt.nsw.gov.au"

list_page = Hpricot(open("#{base_url}/Dispute_resolution/Hearing_lists.html"))

# Get all of the links, we're going visiting
(list_page/"//td").search("a").each do |l|
  page = Hpricot(open(base_url + l.attributes["href"]))
  
  # These few places have an extra link on their page
  exceptions = [
    "Hurstville",
    "Liverpool",
    "Newcastle",
    "Parramatta",
    "Penrith",
    "Sydney",
    "Tamworth",
    "Wollongong"
  ]
  link = 1
  if exceptions.index(l.inner_text)
    link = 2
  end
  
  url = (page/'div#contentstart').search("a")[link].attributes["href"]
  
  venue = {
    'postcode' => url[-4..-1],
    'location' => l.inner_text,
    'URL' => url
  }

  ScraperWiki.save(['postcode'], venue)
end

require 'rubygems'
require 'hpricot'
require 'open-uri'

base_url = "http://www.cttt.nsw.gov.au"

list_page = Hpricot(open("#{base_url}/Dispute_resolution/Hearing_lists.html"))

# Get all of the links, we're going visiting
(list_page/"//td").search("a").each do |l|
  page = Hpricot(open(base_url + l.attributes["href"]))
  
  # These few places have an extra link on their page
  exceptions = [
    "Hurstville",
    "Liverpool",
    "Newcastle",
    "Parramatta",
    "Penrith",
    "Sydney",
    "Tamworth",
    "Wollongong"
  ]
  link = 1
  if exceptions.index(l.inner_text)
    link = 2
  end
  
  url = (page/'div#contentstart').search("a")[link].attributes["href"]
  
  venue = {
    'postcode' => url[-4..-1],
    'location' => l.inner_text,
    'URL' => url
  }

  ScraperWiki.save(['postcode'], venue)
end

