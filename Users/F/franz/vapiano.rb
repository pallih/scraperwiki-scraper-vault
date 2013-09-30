# Blank Ruby

require 'nokogiri'
require 'open-uri'

urlToScrap = 'http://www.vapiano.de/frame.php?section=specials&lang=at'

def scrape(url)
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  
  menu = {}
  menu['timeframe']=''
  menu['source']=url
  menu['name']=''
  menu['price']=''
  menu['description']=''

  doc.search('span.monat').each do |monat|
    mA = Array.new
    monat.text.strip.downcase.split('i').each{|m| 
    mA.push(m.gsub(/[^[:alnum:]]/, '').capitalize)  }
   menu['timeframe'] = mA.join(' ')
   puts menu['timeframe']
  end
  
  doc.search('.speise').each do |speisen|
  #option.attributes["value"].value
   puts speisen
    speisen.to_s.split('<br>').each do |speise|
      speise_html = Nokogiri::HTML(speise)
      sA = speise_html.search('span')
      if sA.length >= 2
      wA = Array.new
      sA[0].text.split(' ').each{|w| wA.push(w.capitalize) }
      menu['name'] = wA.join(' ')
      menu['price'] = sA[1].text
      puts menu['name']+' '+menu['price']
ScraperWiki.save(['timeframe','name', 'price', 'description', 'source'], menu)
      end
      puts '----------------------'
    end
    
  
   # puts speisen.content
   
  end
  

  
end

scrape(urlToScrap)# Blank Ruby

require 'nokogiri'
require 'open-uri'

urlToScrap = 'http://www.vapiano.de/frame.php?section=specials&lang=at'

def scrape(url)
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  
  menu = {}
  menu['timeframe']=''
  menu['source']=url
  menu['name']=''
  menu['price']=''
  menu['description']=''

  doc.search('span.monat').each do |monat|
    mA = Array.new
    monat.text.strip.downcase.split('i').each{|m| 
    mA.push(m.gsub(/[^[:alnum:]]/, '').capitalize)  }
   menu['timeframe'] = mA.join(' ')
   puts menu['timeframe']
  end
  
  doc.search('.speise').each do |speisen|
  #option.attributes["value"].value
   puts speisen
    speisen.to_s.split('<br>').each do |speise|
      speise_html = Nokogiri::HTML(speise)
      sA = speise_html.search('span')
      if sA.length >= 2
      wA = Array.new
      sA[0].text.split(' ').each{|w| wA.push(w.capitalize) }
      menu['name'] = wA.join(' ')
      menu['price'] = sA[1].text
      puts menu['name']+' '+menu['price']
ScraperWiki.save(['timeframe','name', 'price', 'description', 'source'], menu)
      end
      puts '----------------------'
    end
    
  
   # puts speisen.content
   
  end
  

  
end

scrape(urlToScrap)