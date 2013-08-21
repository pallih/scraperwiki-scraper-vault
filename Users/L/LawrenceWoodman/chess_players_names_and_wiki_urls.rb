require 'nokogiri' 


def scrape_url(url)
  html = ScraperWiki.scrape(url)

  people = {}
  doc = Nokogiri::HTML(html)
  doc.css('div#bodyContent h2').each do |h2|
    h2_text = h2.css('span.mw-headline').inner_text
    if h2_text =~ /^[A-Z]{1,1}$/
      h2.next_element.css('li').each do |person|
        anchor = person.css('a').first
        name = anchor.inner_text
        wiki_url = anchor.attribute('href')
        absolute_url = "http://wikipedia.org#{wiki_url}"
        people[absolute_url] = name
      end
    end
  end

  dump_people(people, url)
end

def dump_people(people, source_url)
  # Save data to database
  people.each do |url, name|
    data = {
      'url' => url,
      'name' => name,
      'field' => source_url.sub(/^.*?List_of_/, '').sub(/s$/, '')
    }
    ScraperWiki.save_sqlite(unique_keys=['url'], data=data)
  end
end

urls = [
  'http://en.wikipedia.org/wiki/List_of_chess_players'
]

urls.each {|url| scrape_url(url)}
