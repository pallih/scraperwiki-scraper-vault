# encoding: utf-8

require 'nokogiri'

url  = "http://c7.se/"
html = ScraperWiki::scrape url
doc  = Nokogiri::HTML html

doc.search("#current-projects .project").each do |p|
  a = p.at_css('h3 a')
  s = p.at_css('span')

  data = {
    title: a.text,
    description: s.text,
    href: a.attr('href')
  }

  ScraperWiki::save_sqlite unique_keys=["title"],
                           data=data,
                           table_name="projects"
end# encoding: utf-8

require 'nokogiri'

url  = "http://c7.se/"
html = ScraperWiki::scrape url
doc  = Nokogiri::HTML html

doc.search("#current-projects .project").each do |p|
  a = p.at_css('h3 a')
  s = p.at_css('span')

  data = {
    title: a.text,
    description: s.text,
    href: a.attr('href')
  }

  ScraperWiki::save_sqlite unique_keys=["title"],
                           data=data,
                           table_name="projects"
end