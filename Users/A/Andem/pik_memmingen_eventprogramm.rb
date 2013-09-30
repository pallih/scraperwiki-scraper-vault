# Blank Ruby

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'
agent = Mechanize.new
#agent.user_agent = 'Friendly Mechanize Script"
#agent.user_agent_alias = 'Mac Safari'
agent.get('http://www.pik-mm.de/index.php?id=47&tx_eventcalendar_pi1[pointer]=0&tx_eventcalendar_pi1[mode]=1&cHash=e28a629240')

doc= agent.page.at('div[@class="tx-eventcalendar-pi1"]')

for event in doc.search('div[@class="tx-eventcalendar-detail-container"]')

  datetime= event.at('div[@class="tx-eventcalendar-detail-eventtimebox"]')
  datum = datetime.at('div[@class="tx-eventcalendar-detail-date"]').text
  zeit = datetime.at('div[@class="tx-eventcalendar-detail-begin"]').text
  name = event.at('div[@class="tx-eventcalendar-detail-artist"]').text.strip

  eventurl = event.at('div[@class="tx-eventcalendar-detail-artist"]/a')
  follow = false
  if eventurl
    url = "http://www.pik-mm.de/"+eventurl.attributes['href']
    follow=true
  elsif name == "Jazz Session"
    url = "http://www.pik-mm.de/index.php?id=16#c26"
  elsif name == "Folk Session"
    url = "http://www.pik-mm.de/index.php?id=16#c27"
  else
    url = "err"+name+"err"
  end
  
 # puts name
 # puts url 
#  puts datum
 # puts zeit
name2=""
imgurl=""
beschreibung=""
eventurl=""
kat=""
preis=""

  if follow
    doc2 = agent.transact do
      doc2 =agent.get(url)
      abox = doc2.at('div[@class="tx-eventcalendar-item-abstractbox"]')
      name2 = abox.at('h4').text
puts name2
      imgurl = "http://www.pik-mm.de/"+abox.at('a').attributes['href']
#puts imgurl
      beschreibung = abox.at('p[@class="bodytext"]').text
#puts beschreibung
      eventurl = abox.at('div[@class="tx-eventcalendar-item-websitelink"]').text.strip
      if eventurl != ""
        eventurl="http://www.pik-mm.de/"+eventurl
      end
#puts eventurl
      kat = abox.at('div[@class="tx-eventcalendar-item-note1"]').text.strip
      if kat == ""
        kat = "Musik"
      end
#puts kat
      preis = abox.at('div[@class="tx-eventcalendar-item-price"]').text
#puts preis
    end    
  end

     data = {
          'name' => name,
          'name2' => name2,
          'url' => url,
          'datum' => datum,
          'zeit' => zeit,
          'ort' => 'PIK, Memmingen',
          'img' => imgurl,
          'beschreibung' => beschreibung,
          'evurl' => eventurl,
          'kategorie' => kat,
          'preis' => preis
        }
      puts data.to_json
      ScraperWiki.save_sqlite(unique_keys=['name', 'datum', 'zeit'], data=data) 

end







# Blank Ruby

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'
agent = Mechanize.new
#agent.user_agent = 'Friendly Mechanize Script"
#agent.user_agent_alias = 'Mac Safari'
agent.get('http://www.pik-mm.de/index.php?id=47&tx_eventcalendar_pi1[pointer]=0&tx_eventcalendar_pi1[mode]=1&cHash=e28a629240')

doc= agent.page.at('div[@class="tx-eventcalendar-pi1"]')

for event in doc.search('div[@class="tx-eventcalendar-detail-container"]')

  datetime= event.at('div[@class="tx-eventcalendar-detail-eventtimebox"]')
  datum = datetime.at('div[@class="tx-eventcalendar-detail-date"]').text
  zeit = datetime.at('div[@class="tx-eventcalendar-detail-begin"]').text
  name = event.at('div[@class="tx-eventcalendar-detail-artist"]').text.strip

  eventurl = event.at('div[@class="tx-eventcalendar-detail-artist"]/a')
  follow = false
  if eventurl
    url = "http://www.pik-mm.de/"+eventurl.attributes['href']
    follow=true
  elsif name == "Jazz Session"
    url = "http://www.pik-mm.de/index.php?id=16#c26"
  elsif name == "Folk Session"
    url = "http://www.pik-mm.de/index.php?id=16#c27"
  else
    url = "err"+name+"err"
  end
  
 # puts name
 # puts url 
#  puts datum
 # puts zeit
name2=""
imgurl=""
beschreibung=""
eventurl=""
kat=""
preis=""

  if follow
    doc2 = agent.transact do
      doc2 =agent.get(url)
      abox = doc2.at('div[@class="tx-eventcalendar-item-abstractbox"]')
      name2 = abox.at('h4').text
puts name2
      imgurl = "http://www.pik-mm.de/"+abox.at('a').attributes['href']
#puts imgurl
      beschreibung = abox.at('p[@class="bodytext"]').text
#puts beschreibung
      eventurl = abox.at('div[@class="tx-eventcalendar-item-websitelink"]').text.strip
      if eventurl != ""
        eventurl="http://www.pik-mm.de/"+eventurl
      end
#puts eventurl
      kat = abox.at('div[@class="tx-eventcalendar-item-note1"]').text.strip
      if kat == ""
        kat = "Musik"
      end
#puts kat
      preis = abox.at('div[@class="tx-eventcalendar-item-price"]').text
#puts preis
    end    
  end

     data = {
          'name' => name,
          'name2' => name2,
          'url' => url,
          'datum' => datum,
          'zeit' => zeit,
          'ort' => 'PIK, Memmingen',
          'img' => imgurl,
          'beschreibung' => beschreibung,
          'evurl' => eventurl,
          'kategorie' => kat,
          'preis' => preis
        }
      puts data.to_json
      ScraperWiki.save_sqlite(unique_keys=['name', 'datum', 'zeit'], data=data) 

end







