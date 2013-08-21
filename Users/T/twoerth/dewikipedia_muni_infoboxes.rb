require 'nokogiri'           
require 'open-uri'
require 'json'


ScraperWiki::attach("dewikipedia_swiss_municipalities")           
munis = ScraperWiki::select("* from dewikipedia_swiss_municipalities.swdata")

munis.each do |d|
  doc = Nokogiri::HTML( open( "http://de.wikipedia.org/wiki/#{ d['link'] }" ) )

  infobox = { 'id' => d['link'] }

  cells = []

  doc.css('table.toptextcells tr').each do |tr|
    tds = tr.css('td')
    next unless tds.size == 2
    
    cells << [ tds[0].inner_html, tds[1].inner_html ]
  end

  infobox['data'] = JSON.dump( cells )

  ScraperWiki.save_sqlite(['id'], infobox )
end