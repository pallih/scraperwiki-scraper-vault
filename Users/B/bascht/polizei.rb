#!/usr/bin/env ruby

require 'nokogiri'

soup = ScraperWiki.scrape('http://www.polizei.sachsen.de/pd_leipzig/5785.htm')

soup.gsub!("&nbsp;", " ")

domset = Nokogiri.parse(soup)
messages = domset.xpath '//div[@id="content"]'
locations = messages.xpath("//p[contains(text(), \"Ort\")]")

data = locations.collect.each_with_index do |location, i|
  headline = location.previous_element
  content = location.next_element.text.strip

  location_and_time = location.text.split("Zeit:")

  location = location_and_time[0].gsub("Ort:", "")
  time     = location_and_time[1]

  author = content.scan(/(\((.*?)\))/).last.last

  set = {
    "id"       => i,
    "headline" => headline.text.strip,
    "location" => location.strip,
    "time"     => time.strip,
    "content"  => content,
    "author"   => author
  }

  ScraperWiki.save_sqlite(unique_keys=["id"], data=set)           

end


