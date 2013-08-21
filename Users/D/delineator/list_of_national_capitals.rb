require 'nokogiri'

starting_url = 'http://en.wikipedia.org/wiki/List_of_national_capitals'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

doc.search('span.flagicon').each do |f|
  cells = f.parent.parent.parent.search('td')
  capital = cells[0].inner_text
  country = cells[1].inner_text
  flag = f.at('img')['src']
  record = {'capital' => capital, 'country' => country, 'flag' => flag}
  ScraperWiki.save(['capital'], record)
end
