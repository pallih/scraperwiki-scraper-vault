# Blank Ruby
# encoding: utf-8

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'



#allgemeine Funktion für alle Kategorien
def scrape(scrapurl, kat)
  site="http://www.dampfsaeg.de/"
  url=""

  agent = Mechanize.new
  agent.get(scrapurl)
  doc= agent.page.at('html/body/table/tr[3]/td/table/tr/td/table/tr[2]/td/table/tr/td[2]/table')
  for event in doc.search('tr')
    datum= event.at('td').text.strip
    namearr = event.at('td[3]').inner_html.split('<a href')
    namearr2 = namearr[0].split('>')
    namearr3 = namearr2[1].strip.split('</')
    name = namearr3[0].strip #namearr2[1].strip
    zeit = event.at('td[4]').text.strip
    preis = event.at('td[5]').text.strip
    url="test"
    begin
      url = event.at('td[3]/span/a').attributes['href']
      url2=""+url
      if url2.include? 'http://' 
        puts "includes?"+url
      else
        puts "notincludes"+url
      #  url=site+url
        url2=site+url2
      end
    rescue
      url = "fehler mit url"
      url2="fehler mit url"
    end

#      url = event.at('td[3]/span/a').attributes['href']
#      url2=""+url
#     # puts "r"+url2 #.encode("ISO-8859-1")

#      if url2.include? 'ht' #strpos(url,"http://")
#        puts "glrich"
#      else 
#        puts "no"
#        url2=site+url2
#      end



      data = {
        'datum' => datum,
        'name' => name.encode("UTF-8"),
        'zeit' => zeit,
        'preis' => preis,
        'kategorie' => kat,
        'url' => url2
      }
  #  puts data.to_json
    ScraperWiki.save_sqlite(unique_keys=['datum', 'name', 'zeit'], data=data) 
  end
end

agent = Mechanize.new
agent.get('http://dampfsaeg.de/index.php?inhalt=v_musik')

begin
scrape('http://dampfsaeg.de/index.php?inhalt=v_musik', 'Musik')
rescue
puts "fehler musik"
end
begin
scrape('http://dampfsaeg.de/index.php?inhalt=v_kino', 'Kino')
rescue
puts "fehler kino"
end
begin
scrape('http://dampfsaeg.de/index.php?inhalt=v_theater', 'Kabarett')
rescue
puts "fehler kabarett"
end
begin
scrape('http://dampfsaeg.de/index.php?inhalt=v_markt', 'Markt')
rescue
puts "fehler markt"
end
begin
scrape('http://dampfsaeg.de/index.php?inhalt=v_messe', 'Messen')
rescue
puts "fehler messen"
end
begin
scrape('http://dampfsaeg.de/index.php?inhalt=v_kinder', 'Kinder')
rescue
puts "fehler kinder"
end







