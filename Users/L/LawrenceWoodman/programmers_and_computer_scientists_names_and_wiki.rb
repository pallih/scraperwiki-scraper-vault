require 'nokogiri' 


def scrape_url(url)
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
puts "html: #{html}"
puts "doc: #{doc}"

  doc.css('div#bodyContent ul li').each do |person|
    anchor = person.css('a').first
    name = anchor.inner_text
    wiki_url = anchor.attribute('href')
    if wiki_url !~ /redlink=1$/
      absolute_url = "http://wikipedia.org#{wiki_url}"
      save_person_to_database(name, absolute_url)
    end
  end
end

def save_person_to_database(name, url)
  data = {
    'url' => url,
    'name' => name
  }
  ScraperWiki.save_sqlite(unique_keys=['url'], data=data)
end

urls = [
 #'http://en.wikipedia.org/wiki/List_of_programmers',
 'http://en.wikipedia.org/wiki/List_of_computer_scientists'
]

urls.each {|url| scrape_url(url)}require 'nokogiri' 


def scrape_url(url)
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
puts "html: #{html}"
puts "doc: #{doc}"

  doc.css('div#bodyContent ul li').each do |person|
    anchor = person.css('a').first
    name = anchor.inner_text
    wiki_url = anchor.attribute('href')
    if wiki_url !~ /redlink=1$/
      absolute_url = "http://wikipedia.org#{wiki_url}"
      save_person_to_database(name, absolute_url)
    end
  end
end

def save_person_to_database(name, url)
  data = {
    'url' => url,
    'name' => name
  }
  ScraperWiki.save_sqlite(unique_keys=['url'], data=data)
end

urls = [
 #'http://en.wikipedia.org/wiki/List_of_programmers',
 'http://en.wikipedia.org/wiki/List_of_computer_scientists'
]

urls.each {|url| scrape_url(url)}