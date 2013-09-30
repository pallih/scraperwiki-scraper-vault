# encoding: utf-8
# Blank Ruby

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'

#allgemeine Funktion für alle Events
def scrape(a, b)
base="http://www.kaminwerk.de/"
  puts a+b
  agent = Mechanize.new
  agent.get(a)  #("http://www.kaminwerk.de/event.html?&tx_ttnews[tt_news]=593&tx_ttnews[backPid]=8")
  begin
    event = agent.page.at('div[@class="news-single-item"]')
  rescue
    puts('Fehler beim Laden des Events')
  end
  imgurl = event.at('div[@class="news-single-img"]/a').attributes['href']
  name = event.at('table/tr/td[2]/h2')
  datum = ""
    datum.force_encoding("UTF-8")
  datum = datum+event.at('span[@class="news-single-date"]')
  rohdatum = ""+datum
    datum.gsub!('. März ', '-03-')
    datum.gsub!('. April ', '-04-')
    datum.gsub!('. Mai ', '-05-')
    datum.gsub!('. Juni ', '-06-')
    datum.gsub!('. Juli ', '-07-')
    datum.gsub!('. August ', '-08-')
    datum.gsub!('. September ', '-09-')
    datum.gsub!('. Oktober ', '-10-')
    datum.gsub!('. November ', '-11-')
    datum.gsub!('. Dezember ', '-12-')
    datum.gsub!('. Januar ', '-01-')
    datum.gsub!('. Februar ', '-02-')
    datum.gsub!('Montag, ', '')
    datum.gsub!('Dienstag, ', '')
    datum.gsub!('Mittwoch, ', '')
    datum.gsub!('Donnerstag, ', '')
    datum.gsub!('Freitag, ', '')
    datum.gsub!('Samstag, ', '')
    datum.gsub!('Sonntag, ', '')
    puts datum.encoding.name
    #puts datum.valid_encoding? 
    puts datum

  zeitpreis= event.at('div[@class="news-single-entry"]')

  begin
    zptemp = ""
    zptemp.force_encoding("UTF-8")

    zptemp = zptemp + zeitpreis.text
    #myarray = zptemp.match(/(\d\d:\d\d) \((\d\d:\d\d) Einlass/)  #warum ist da noch ein zeichen???
    myarray = zptemp.match(/(\d\d:\d\d) .\((\d\d(\.|:)\d\d)/)
    einlass = myarray[2]
    einlass.gsub!('.', ':')
    zeit = myarray[1]
  rescue
    einlass = ""
    zeit = ""
  end

  begin
     tpreis = zeitpreis.text.split(") ")
    preis = tpreis[1]
  rescue
    preis = "?"
  end

  kurz = event.at('table/tr/td[2]/h3').text
  lang = event.at('table[2]/tr[2]/td').text
  begin
    url=""
    nodes = event.search('table[2]/tr[2]/td/dd//a')
    for link in nodes
      url = url+link.attributes['href']+"\n"
    end
  rescue
    url = ""
  end

      data = {
        'imgurl' => base+imgurl,
        'name' => name.text, 
        'date' => datum,#.text,
        'time' => zeit,
        'doortime' => einlass,
        'rawtime' => zeitpreis.text,
        'price' => preis,
        'sdesc' => kurz,
        'desc' => lang,
        'url' => url,
        'rawdate' => rohdatum,
        'evurl' => a
      }

  ScraperWiki.save_sqlite(unique_keys=['name'], data=data) 
end

  site="http://www.kaminwerk.de/index.php"
  base="http://www.kaminwerk.de/"
                           
  agent = Mechanize.new
  agent.get(site)
  doc= agent.page.at('/html/body/div/div/div/div/div/div[2]/div/table/tr')
  nodes = agent.page.search('//h3/a')

  for link in nodes
    evurl = base + link.attributes['href']
    scrape(evurl, 'lali')
  end
# encoding: utf-8
# Blank Ruby

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'

#allgemeine Funktion für alle Events
def scrape(a, b)
base="http://www.kaminwerk.de/"
  puts a+b
  agent = Mechanize.new
  agent.get(a)  #("http://www.kaminwerk.de/event.html?&tx_ttnews[tt_news]=593&tx_ttnews[backPid]=8")
  begin
    event = agent.page.at('div[@class="news-single-item"]')
  rescue
    puts('Fehler beim Laden des Events')
  end
  imgurl = event.at('div[@class="news-single-img"]/a').attributes['href']
  name = event.at('table/tr/td[2]/h2')
  datum = ""
    datum.force_encoding("UTF-8")
  datum = datum+event.at('span[@class="news-single-date"]')
  rohdatum = ""+datum
    datum.gsub!('. März ', '-03-')
    datum.gsub!('. April ', '-04-')
    datum.gsub!('. Mai ', '-05-')
    datum.gsub!('. Juni ', '-06-')
    datum.gsub!('. Juli ', '-07-')
    datum.gsub!('. August ', '-08-')
    datum.gsub!('. September ', '-09-')
    datum.gsub!('. Oktober ', '-10-')
    datum.gsub!('. November ', '-11-')
    datum.gsub!('. Dezember ', '-12-')
    datum.gsub!('. Januar ', '-01-')
    datum.gsub!('. Februar ', '-02-')
    datum.gsub!('Montag, ', '')
    datum.gsub!('Dienstag, ', '')
    datum.gsub!('Mittwoch, ', '')
    datum.gsub!('Donnerstag, ', '')
    datum.gsub!('Freitag, ', '')
    datum.gsub!('Samstag, ', '')
    datum.gsub!('Sonntag, ', '')
    puts datum.encoding.name
    #puts datum.valid_encoding? 
    puts datum

  zeitpreis= event.at('div[@class="news-single-entry"]')

  begin
    zptemp = ""
    zptemp.force_encoding("UTF-8")

    zptemp = zptemp + zeitpreis.text
    #myarray = zptemp.match(/(\d\d:\d\d) \((\d\d:\d\d) Einlass/)  #warum ist da noch ein zeichen???
    myarray = zptemp.match(/(\d\d:\d\d) .\((\d\d(\.|:)\d\d)/)
    einlass = myarray[2]
    einlass.gsub!('.', ':')
    zeit = myarray[1]
  rescue
    einlass = ""
    zeit = ""
  end

  begin
     tpreis = zeitpreis.text.split(") ")
    preis = tpreis[1]
  rescue
    preis = "?"
  end

  kurz = event.at('table/tr/td[2]/h3').text
  lang = event.at('table[2]/tr[2]/td').text
  begin
    url=""
    nodes = event.search('table[2]/tr[2]/td/dd//a')
    for link in nodes
      url = url+link.attributes['href']+"\n"
    end
  rescue
    url = ""
  end

      data = {
        'imgurl' => base+imgurl,
        'name' => name.text, 
        'date' => datum,#.text,
        'time' => zeit,
        'doortime' => einlass,
        'rawtime' => zeitpreis.text,
        'price' => preis,
        'sdesc' => kurz,
        'desc' => lang,
        'url' => url,
        'rawdate' => rohdatum,
        'evurl' => a
      }

  ScraperWiki.save_sqlite(unique_keys=['name'], data=data) 
end

  site="http://www.kaminwerk.de/index.php"
  base="http://www.kaminwerk.de/"
                           
  agent = Mechanize.new
  agent.get(site)
  doc= agent.page.at('/html/body/div/div/div/div/div/div[2]/div/table/tr')
  nodes = agent.page.search('//h3/a')

  for link in nodes
    evurl = base + link.attributes['href']
    scrape(evurl, 'lali')
  end
