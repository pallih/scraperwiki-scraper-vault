require 'nokogiri'           

url = 'https://www.mvs.fi/data/srk/jyvaskyla/lehteen/tapahtumat.phtml?hakusana=&seurakunta=0&hakualue=Jumalanpalvelukset&kieli=fi'

html = ScraperWiki::scrape(url)

doc = Nokogiri::HTML html
doc.search("#tapahtumat tr").each do |event_row|
  event_cells = event_row.search('td')
  next unless event_cells.count == 2
  start_time = event_cells.first.inner_html.sub('<br>', ' ')
  event_link_tag = event_cells.last.search('a')
  event_title = event_link_tag.inner_text
  event_url = event_link_tag.attr('href').value
  event_id = event_url.match(/nayta=(\d+)/)[1]
  event_description = if desc_node = event_cells.last.children[2]
                        desc_node.text
                      end
  event = {
    id: event_id,
    title: event_title,
    description: event_description,
    start_time: start_time,
    event_url: event_url,
  }
  ScraperWiki::save_sqlite(['id'], event)
end