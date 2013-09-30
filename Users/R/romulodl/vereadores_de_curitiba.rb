require 'nokogiri'

html = ScraperWiki.scrape("http://www.cmc.pr.gov.br/ver.php")
Nokogiri::HTML(html).css("table table table table>tr.tab4a").each_with_index do |v, i|
  cells = v.search('td')

  name = cells[0].search("a").inner_html.force_encoding("UTF-8")
  party = cells[1].inner_html.force_encoding("UTF-8")
  email = cells[2].search("a").inner_html.force_encoding("UTF-8")

  data = {
    'id' => i,
    'name' => cells[0].search("a").inner_html,
    'party' => cells[1].inner_html,
    'email' => cells[2].search("a").inner_html
  }
  unique_keys = ['id', 'name', 'email']
  ScraperWiki.save_sqlite(['test'], {'test' => 'hello'})
endrequire 'nokogiri'

html = ScraperWiki.scrape("http://www.cmc.pr.gov.br/ver.php")
Nokogiri::HTML(html).css("table table table table>tr.tab4a").each_with_index do |v, i|
  cells = v.search('td')

  name = cells[0].search("a").inner_html.force_encoding("UTF-8")
  party = cells[1].inner_html.force_encoding("UTF-8")
  email = cells[2].search("a").inner_html.force_encoding("UTF-8")

  data = {
    'id' => i,
    'name' => cells[0].search("a").inner_html,
    'party' => cells[1].inner_html,
    'email' => cells[2].search("a").inner_html
  }
  unique_keys = ['id', 'name', 'email']
  ScraperWiki.save_sqlite(['test'], {'test' => 'hello'})
end