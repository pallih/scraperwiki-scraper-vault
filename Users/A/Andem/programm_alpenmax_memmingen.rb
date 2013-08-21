# Blank Ruby
# encoding: utf-8

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'



#allgemeine Funktion für alle Events
def scrape(a)
  base="http://www.kaminwerk.de/"
  puts a
  agent = Mechanize.new
  agent.get(a)  
  begin
    event = agent.page.at('div[@id="event_detail_container"]')
  rescue
    puts('Fehler beim Laden des Events')
  end
  datum = event.at('div[@id="event_detail_extra"]/h2')
  zeit = event.at('div[@id="event_detail_extra"]/h2[2]')
  name = event.at('div[@id="event_detail_extra"]/h1')
  desc = event.at('div[@id="event_detail_extra"]/p').text
  imgurl = event.at('div[@id="event_detail_image"]/img').attributes['src']
  url = a

      data = {
        'datum' => datum,
        'zeit' => zeit, 
        'name' => name,
        'beschreibung' => desc,
        'bild' => imgurl,
        'www' => url
      }
  ScraperWiki.save_sqlite(unique_keys=['name'], data=data) 
end

  site="http://www.discofun.de/memmingen/events.php?&m=12&y=2011" #events.php?&m=12&y=2011
  base="http://www.discofun.de/memmingen/"

# alternative übersich: http://www.discofun.de/memmingen/events2.php?&d=18&m=11&y=2011
# event-seite: http://www.discofun.de/memmingen/events3.php?id=103
                           
  agent = Mechanize.new
  agent.get(site)
  doc= agent.page.at('/')#.at('table')#.at('div[@id="page-loader"]')
  puts doc
  nodes = agent.page.search('//div[@class="events_container"]')

  for event in nodes
    puts event
    tnimgurl = base+event.at('div[@class="events_img"]/img').attributes['src']
    imgurl = tnimgurl.sub("/tn_","/")
    datum = event.at('div[@class="events_date"]')
    name = event.at('div[@class="events_headline"]')
    teaser = event.at('div[@class="event_teaser"]')
puts imgurl
puts datum.text
puts name.text
puts teaser.text

      data = {
        'imgurl' => imgurl,
        'name' => name.text, 
        'datum' => datum.text,
      #  'zeit' => zeitpreis.text,
      #  'preis' => preis,
        'kurz' => teaser.text
      #  'lang' => lang,
    # 'url' => url
      }
  ScraperWiki.save_sqlite(unique_keys=['name'], data=data) 
  end