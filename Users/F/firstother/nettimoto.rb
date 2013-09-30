#coding: utf-8
require 'nokogiri'         
require 'open-uri'
 
BASE_URL = 'http://www.nettimoto.com/'
SEARCH_PARMS = 'listAdvSearchFindAgent.php?id=12168949&tb=tmp_find_agent&PN[0]=adv_search&PL[0]=advSearch.php?id=12168949@tb=tmp_find_agent'

def scrape_table(page)
  page.css('.listingVifUrl').each do |item|
    ref = item.at_css('.childVifUrl')['href'].split(/\//).last.to_i
    names = item.at_css('.make_model_link')
    name = names.text if names
    briefs = item.at_css('.bold_link_list')
    brief = briefs.text.gsub(/\n/, '').gsub(/\s+/, ' ').strip if briefs
    years = item.at_css('.ma0.small_text85')
    year = years.text.to_i if years
    mileages = item.at_css('.col_set12')
    mileage = mileages.text.delete(' km').gsub(/\s+/,'').to_i if mileages
    prices = item.at_css('b.big_text')
    price = prices.text.delete(' €').gsub(/\s+/,'').to_i if prices
    locs = item.at_css('.pl10')
    loc = locs.text.gsub(/\n/,'#').gsub(/\s+/,'').split('#').last if locs
    url = BASE_URL + item.at_css('.childVifUrl')['href']
    img_url = item.at_css('.listing_thumb a img')['src']
    near = ['oulu','kempele','liminka','oulunsalo','kiiminki','haukipudas','ii','muhos','tyrnävä','ruukki','lumijoki'].include? (loc.downcase) ? true : false
    data = { ref: ref, name: name, brief: brief, year: year, mileage: mileage, price: price, loc: loc, url: url, img_url: img_url, near: near }
    ScraperWiki::save_sqlite(['ref'], data)
  end
end

def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_link = page.at_css("a[title='Seuraava']")
  if next_link 
    next_url = next_link['href']
    scrape_and_look_for_next_link(next_url)
  end
end

starting_url = BASE_URL + SEARCH_PARMS
scrape_and_look_for_next_link(starting_url)#coding: utf-8
require 'nokogiri'         
require 'open-uri'
 
BASE_URL = 'http://www.nettimoto.com/'
SEARCH_PARMS = 'listAdvSearchFindAgent.php?id=12168949&tb=tmp_find_agent&PN[0]=adv_search&PL[0]=advSearch.php?id=12168949@tb=tmp_find_agent'

def scrape_table(page)
  page.css('.listingVifUrl').each do |item|
    ref = item.at_css('.childVifUrl')['href'].split(/\//).last.to_i
    names = item.at_css('.make_model_link')
    name = names.text if names
    briefs = item.at_css('.bold_link_list')
    brief = briefs.text.gsub(/\n/, '').gsub(/\s+/, ' ').strip if briefs
    years = item.at_css('.ma0.small_text85')
    year = years.text.to_i if years
    mileages = item.at_css('.col_set12')
    mileage = mileages.text.delete(' km').gsub(/\s+/,'').to_i if mileages
    prices = item.at_css('b.big_text')
    price = prices.text.delete(' €').gsub(/\s+/,'').to_i if prices
    locs = item.at_css('.pl10')
    loc = locs.text.gsub(/\n/,'#').gsub(/\s+/,'').split('#').last if locs
    url = BASE_URL + item.at_css('.childVifUrl')['href']
    img_url = item.at_css('.listing_thumb a img')['src']
    near = ['oulu','kempele','liminka','oulunsalo','kiiminki','haukipudas','ii','muhos','tyrnävä','ruukki','lumijoki'].include? (loc.downcase) ? true : false
    data = { ref: ref, name: name, brief: brief, year: year, mileage: mileage, price: price, loc: loc, url: url, img_url: img_url, near: near }
    ScraperWiki::save_sqlite(['ref'], data)
  end
end

def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_link = page.at_css("a[title='Seuraava']")
  if next_link 
    next_url = next_link['href']
    scrape_and_look_for_next_link(next_url)
  end
end

starting_url = BASE_URL + SEARCH_PARMS
scrape_and_look_for_next_link(starting_url)#coding: utf-8
require 'nokogiri'         
require 'open-uri'
 
BASE_URL = 'http://www.nettimoto.com/'
SEARCH_PARMS = 'listAdvSearchFindAgent.php?id=12168949&tb=tmp_find_agent&PN[0]=adv_search&PL[0]=advSearch.php?id=12168949@tb=tmp_find_agent'

def scrape_table(page)
  page.css('.listingVifUrl').each do |item|
    ref = item.at_css('.childVifUrl')['href'].split(/\//).last.to_i
    names = item.at_css('.make_model_link')
    name = names.text if names
    briefs = item.at_css('.bold_link_list')
    brief = briefs.text.gsub(/\n/, '').gsub(/\s+/, ' ').strip if briefs
    years = item.at_css('.ma0.small_text85')
    year = years.text.to_i if years
    mileages = item.at_css('.col_set12')
    mileage = mileages.text.delete(' km').gsub(/\s+/,'').to_i if mileages
    prices = item.at_css('b.big_text')
    price = prices.text.delete(' €').gsub(/\s+/,'').to_i if prices
    locs = item.at_css('.pl10')
    loc = locs.text.gsub(/\n/,'#').gsub(/\s+/,'').split('#').last if locs
    url = BASE_URL + item.at_css('.childVifUrl')['href']
    img_url = item.at_css('.listing_thumb a img')['src']
    near = ['oulu','kempele','liminka','oulunsalo','kiiminki','haukipudas','ii','muhos','tyrnävä','ruukki','lumijoki'].include? (loc.downcase) ? true : false
    data = { ref: ref, name: name, brief: brief, year: year, mileage: mileage, price: price, loc: loc, url: url, img_url: img_url, near: near }
    ScraperWiki::save_sqlite(['ref'], data)
  end
end

def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_link = page.at_css("a[title='Seuraava']")
  if next_link 
    next_url = next_link['href']
    scrape_and_look_for_next_link(next_url)
  end
end

starting_url = BASE_URL + SEARCH_PARMS
scrape_and_look_for_next_link(starting_url)