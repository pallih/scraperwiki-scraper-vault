require 'nokogiri'
require 'uri'
require 'open-uri'

base_url = "http://www.open.ac.uk/researchprojects/makingbritain/"
index_page = "individual_v"
p_url = base_url + index_page
pages = 0..8
people = []
pages.each do |page|
  if (page == 0)
    url = p_url
  else 
    url = p_url + "?page=" + page.to_s
  end

  index_doc = Nokogiri::HTML(open(url))

  index_doc.xpath('//table[1]/tbody/tr/td/div/span/a').each do |person|
    p = person.inner_text.chomp.strip.to_s + "|" + "http://www.open.ac.uk" +person.attributes['href'].to_s
    if p.to_s.length > 0
      people.push(p)
    end
  end
end
 
people.each do |person|
  data = {
      name: person.split("|").first,
      url: person.split("|").last
      }
      ScraperWiki::save_sqlite(['name'], data) 
end
