require 'nokogiri'

def pageURL(page)
  "http://thenounproject.com/en-us/retrieve/partial/#{page}/"
end

def fetchPage(number)
  html = ScraperWiki.scrape(pageURL(number)) rescue false
  Nokogiri::HTML.parse(html) if html
  # consider adding a test for html content here in case the current http 500 behaviour changes?
  # e.g. 
  # if (html.text =~ /stop fetching/)
  #   return false
  # end
end

page = 0
# Resource returns a http 500 but oddly also content (JSON) if you try to retrieve a non-existant page. 
# In this case fetchPage will be false
while (doc = fetchPage(page)) do
  doc.css('.noun').each do |nounContainer|
    noun = {}
    li =  nounContainer.css('li:first')
    noun['noun'] = li.text
    noun['url'] = li.css('a:first').attr('href').text
    noun['id'] = nounContainer.css('.noun-id').text
    noun['svg_url'] = nounContainer.css('.svg_url').attr('href').text
    ScraperWiki.save_sqlite(unique_keys=['id'], data=noun)
    end
  page = page + 1
end
