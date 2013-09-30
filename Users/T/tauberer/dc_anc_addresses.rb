# Scrapes Washington DC ANC contact information from anc.dc.gov
require 'open-uri'
require 'nokogiri'

ancs = { 
          1=>["a","b","c","d"],
          2=>["a","b","c","d","e","f"],
          3=>["b","c","d","e","f","g"],
          4=>["a","b","c","d"],
          5=>["a","b","c","d","e"],
          6=>["a","b","c","d","e"],
          7=>["b","c","d","e","f"],
          8=>["a","b","c","d","e"]
        }
ScraperWiki::sqliteexecute("drop table if exists swdata")
ancs.each do |ward,offices|
  offices.each do |office|
    doc = Nokogiri::HTML(open("http://app.anc.dc.gov/wards.asp?ward=" + ward.to_s + "&office=" + office))
    doc.css("td[@width='307']").each do |v|
      data = {
        anc: ward.to_s + office,
        addresses_info: v.inner_text,
      }
      ScraperWiki::save_sqlite(['anc'], data)

      break
    end
  end
end# Scrapes Washington DC ANC contact information from anc.dc.gov
require 'open-uri'
require 'nokogiri'

ancs = { 
          1=>["a","b","c","d"],
          2=>["a","b","c","d","e","f"],
          3=>["b","c","d","e","f","g"],
          4=>["a","b","c","d"],
          5=>["a","b","c","d","e"],
          6=>["a","b","c","d","e"],
          7=>["b","c","d","e","f"],
          8=>["a","b","c","d","e"]
        }
ScraperWiki::sqliteexecute("drop table if exists swdata")
ancs.each do |ward,offices|
  offices.each do |office|
    doc = Nokogiri::HTML(open("http://app.anc.dc.gov/wards.asp?ward=" + ward.to_s + "&office=" + office))
    doc.css("td[@width='307']").each do |v|
      data = {
        anc: ward.to_s + office,
        addresses_info: v.inner_text,
      }
      ScraperWiki::save_sqlite(['anc'], data)

      break
    end
  end
end