require 'nokogiri'
require 'open-uri'
require 'json'

def get_page(url)
  req = open(url)
  data = JSON.parse(req.read)
  return data
end

def fetch_org
  page_num = 1
  total_pages = 1

  until page_num > total_pages
    data_container = get_page("http://hotell.difi.no/api/json/difi/etatsbasen/organization?page=#{page_num}")
    page_num += 1
    data_container['entries'].each do |entry|
      data = entry
      ScraperWiki::save_sqlite(['tailid'], data, 'org')
    end
    if data_container['pages'] >= total_pages
      total_pages = data_container['pages']
    else
      raise 'Unexcepted total_page in org'
    end
    puts "org: Total pages: #{total_pages} Finished: %s" % data_container['page']
  end
end

def fetch_urls
  page_num = 1
  total_pages = 1

  until page_num > total_pages
    data_container = get_page("http://hotell.difi.no/api/json/difi/etatsbasen/url?page=#{page_num}")
    page_num += 1
    data_container['entries'].each do |entry|
      data = entry
      ScraperWiki::save_sqlite(['tailid', 'language'], data, 'url')
    end
    if data_container['pages'] >= total_pages
      total_pages = data_container['pages']
    else
      raise 'Unexcepted total_page in url'
    end
    puts "urL: Total pages: #{total_pages} Finished: %s" % data_container['page']
  end
end

def main
  fetch_org
  fetch_urls
end

mainrequire 'nokogiri'
require 'open-uri'
require 'json'

def get_page(url)
  req = open(url)
  data = JSON.parse(req.read)
  return data
end

def fetch_org
  page_num = 1
  total_pages = 1

  until page_num > total_pages
    data_container = get_page("http://hotell.difi.no/api/json/difi/etatsbasen/organization?page=#{page_num}")
    page_num += 1
    data_container['entries'].each do |entry|
      data = entry
      ScraperWiki::save_sqlite(['tailid'], data, 'org')
    end
    if data_container['pages'] >= total_pages
      total_pages = data_container['pages']
    else
      raise 'Unexcepted total_page in org'
    end
    puts "org: Total pages: #{total_pages} Finished: %s" % data_container['page']
  end
end

def fetch_urls
  page_num = 1
  total_pages = 1

  until page_num > total_pages
    data_container = get_page("http://hotell.difi.no/api/json/difi/etatsbasen/url?page=#{page_num}")
    page_num += 1
    data_container['entries'].each do |entry|
      data = entry
      ScraperWiki::save_sqlite(['tailid', 'language'], data, 'url')
    end
    if data_container['pages'] >= total_pages
      total_pages = data_container['pages']
    else
      raise 'Unexcepted total_page in url'
    end
    puts "urL: Total pages: #{total_pages} Finished: %s" % data_container['page']
  end
end

def main
  fetch_org
  fetch_urls
end

main