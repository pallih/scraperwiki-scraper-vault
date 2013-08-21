require 'nokogiri' 


def scrape_url(url)
  html = ScraperWiki.scrape(url)

  people = {}
  doc = Nokogiri::HTML(html)
  doc.css('div#bodyContent ul li').each do |person|
    anchor = person.css('a').first
    if anchor
      name = anchor.inner_text
      wiki_url = anchor.attribute('href')
      absolute_url = "http://wikipedia.org#{wiki_url}"
      people[absolute_url] = name
    end
  end

  dump_people(people, url)
end

def dump_people(people, source_url)
  # Save data to database
  people.each do |url, name|
    data = {
      'url' => url,
      'name' => name
    }
    ScraperWiki.save_sqlite(unique_keys=['url'], data=data)
  end
end

url = 'http://en.wikipedia.org/wiki/List_of_poets'
scrape_url(url)