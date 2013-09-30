#coding: utf-8
require 'nokogiri'         
require 'open-uri'
 
LNK = 'http://tapahtumakalenteri.ouka.fi/cal/event/eventView.do?calPath=%2Fpublic%2Fcals%2FMainCal&guid='
BASE_URL = 'http://tapahtumakalenteri.ouka.fi/webcache/v1.0/'
SEARCH_PARMS = 'rssDaysWithMunicipality/Oulu/1/list-rss/no-filter.rss'

def scrape_table(doc)
  doc.css('item').each do |item|
    title = item.css('title').first.text
    link = item.css('link').first.text
    guid = link.clone
    guid.slice! LNK
    guid.slice! 'demobedework@mysite.edu&recurrenceId='
    # pubdate = item.css('pubdate') ? item.css('pubdate').first.text : ''
    description = item.css('description').first.text
    description.slice! "Kuvaus: "
    category = ''
    item.css('category').each do |c|
      category = c.text
    end   
    data = { guid: guid, title: title, link: link, description: description, category: category}
    ScraperWiki::save_sqlite(['guid'], data)
  end
end

starting_url = BASE_URL + SEARCH_PARMS
doc = Nokogiri::XML(open(starting_url))
scrape_table(doc)
#coding: utf-8
require 'nokogiri'         
require 'open-uri'
 
LNK = 'http://tapahtumakalenteri.ouka.fi/cal/event/eventView.do?calPath=%2Fpublic%2Fcals%2FMainCal&guid='
BASE_URL = 'http://tapahtumakalenteri.ouka.fi/webcache/v1.0/'
SEARCH_PARMS = 'rssDaysWithMunicipality/Oulu/1/list-rss/no-filter.rss'

def scrape_table(doc)
  doc.css('item').each do |item|
    title = item.css('title').first.text
    link = item.css('link').first.text
    guid = link.clone
    guid.slice! LNK
    guid.slice! 'demobedework@mysite.edu&recurrenceId='
    # pubdate = item.css('pubdate') ? item.css('pubdate').first.text : ''
    description = item.css('description').first.text
    description.slice! "Kuvaus: "
    category = ''
    item.css('category').each do |c|
      category = c.text
    end   
    data = { guid: guid, title: title, link: link, description: description, category: category}
    ScraperWiki::save_sqlite(['guid'], data)
  end
end

starting_url = BASE_URL + SEARCH_PARMS
doc = Nokogiri::XML(open(starting_url))
scrape_table(doc)
