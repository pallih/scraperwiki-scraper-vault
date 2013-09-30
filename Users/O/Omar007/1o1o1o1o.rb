#coding: utf-8
require 'nokogiri'         
require 'open-uri'
 
BASE_URL = 'http://www.ownersdirect.co.uk/'

def scrape_table(page)
  page.css('.list_properties_item').each do |item|
    ref = item.at_css('.list_properties_right').text.split(/Ref\.\s/).last
    locs = item.at_css('.linksgrysml')
    loc = locs.text.split(/\s>\s/).last if locs
    titles = item.at_css('p.linkslisttitle')
    name = titles.text if titles
    briefs = item.at_css('p.list_text')
    brief = briefs.text if briefs
    prices = item.at_css('p.listprice')
    price = prices.text.sub('Prices from ','').sub('.00','').strip if prices
    mult = 7
    if price.scan(' per week').count > 0
      price.sub(' per week','')
      mult = 1
    elsif price.scan(' per night').count > 0
      price.sub(' per night','')
      mult = 7
    elsif price.scan(' per month').count > 0
      price.sub(' per month','')
      mult = 0.25
    end
    if price[0] = '£'
      val = price.sub('£','').to_f*1.24*mult
    else
      val = price.sub('€','').to_f*mult
    end
    url = BASE_URL + item.at_css('.list_properties_right a')['href']
    img_url = item.at_css('.list_properties_right img')['src']
    data = { ref: ref, loc: loc, name: name, brief: brief, price: val, url: url, img_url: img_url }
    ScraperWiki::save_sqlite(['ref'], data) 
  end
end

def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_link = page.at_css("#paginglinks td[style='width:50px'] a")
  if next_link 
    p next_link
    next_url = BASE_URL + next_link['href']
    p next_url
    scrape_and_look_for_next_link(next_url)
  end
end

starting_url = BASE_URL + 'usa-florida-orlando-kissimmee-3bed.htm'
scrape_and_look_for_next_link(starting_url)#coding: utf-8
require 'nokogiri'         
require 'open-uri'
 
BASE_URL = 'http://www.ownersdirect.co.uk/'

def scrape_table(page)
  page.css('.list_properties_item').each do |item|
    ref = item.at_css('.list_properties_right').text.split(/Ref\.\s/).last
    locs = item.at_css('.linksgrysml')
    loc = locs.text.split(/\s>\s/).last if locs
    titles = item.at_css('p.linkslisttitle')
    name = titles.text if titles
    briefs = item.at_css('p.list_text')
    brief = briefs.text if briefs
    prices = item.at_css('p.listprice')
    price = prices.text.sub('Prices from ','').sub('.00','').strip if prices
    mult = 7
    if price.scan(' per week').count > 0
      price.sub(' per week','')
      mult = 1
    elsif price.scan(' per night').count > 0
      price.sub(' per night','')
      mult = 7
    elsif price.scan(' per month').count > 0
      price.sub(' per month','')
      mult = 0.25
    end
    if price[0] = '£'
      val = price.sub('£','').to_f*1.24*mult
    else
      val = price.sub('€','').to_f*mult
    end
    url = BASE_URL + item.at_css('.list_properties_right a')['href']
    img_url = item.at_css('.list_properties_right img')['src']
    data = { ref: ref, loc: loc, name: name, brief: brief, price: val, url: url, img_url: img_url }
    ScraperWiki::save_sqlite(['ref'], data) 
  end
end

def scrape_and_look_for_next_link(url)
  page = Nokogiri::HTML(open(url))
  scrape_table(page)
  next_link = page.at_css("#paginglinks td[style='width:50px'] a")
  if next_link 
    p next_link
    next_url = BASE_URL + next_link['href']
    p next_url
    scrape_and_look_for_next_link(next_url)
  end
end

starting_url = BASE_URL + 'usa-florida-orlando-kissimmee-3bed.htm'
scrape_and_look_for_next_link(starting_url)