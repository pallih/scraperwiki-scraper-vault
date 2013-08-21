require 'nokogiri'

url = 'http://www.oreilly.co.jp/ebook/'
html = ScraperWiki.scrape(url)
doc = Nokogiri::HTML(html)

doc.search("table[@id='bookTable'] tbody tr").map do |tr|
  cells = tr.search('td')

  data = {
    'ISBN' => cells[0].inner_html,
    'TITLE' => cells[1].search('a')[0].inner_html,
    'PRICE' => cells[2].inner_html.gsub(/\,/,''),
    'PUBLISHDATE' => cells[3].inner_html
  }
  
  ScraperWiki.save_sqlite(['ISBN'], data)
end

