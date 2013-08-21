# Blank Ruby

require 'nokogiri'
require 'open-uri'

@baseUrl = 'http://www.plz-postleitzahl.com/at/'
seedUrls = ['http://www.plz-postleitzahl.com/at/index.cfm']
urlsToScrap = Array.new

def collectUrls(seedUrlsA)
  urlCollectorA = Array.new
  seedUrlsA.each do |url|
    #urlCollectorA.push(url)
    puts url
    html = ScraperWiki.scrape(url)
    #puts html
    doc = Nokogiri::HTML(html) 
    puts doc
    #/HTML[1]/BODY[1]/TABLE[1]/TBODY[1]/TR[1]/TD[2]/TABLE[1]/TBODY[1]/TR[4]/TD[1]/TABLE[1]/TBODY[1]/TR[2]/TD[1]/TABLE[1]/TBODY[1]/TR[1]/TD[1]/TABLE[1]/TBODY[1]/TR[3]/TD[1]/TABLE[1]/TBODY[1]/TR[2]/TD[1]/TABLE[1]/TBODY[1]/TR[2]/TD[2]
    doc.xpath('//a[@href=plzinfo.cfm?parm=*]').each do |nav|
      puts nav
      puts @baseUrl+nav.attribute('href')
      urlCollectorA.push(@baseUrl+nav.attribute('href'))
    end
  end
  return urlCollectorA
end



def scrape(urlA)
  urlA.each do |url|
       d = {}
       d['city']=''
       d['plz']=''
       d['source']=url
       d['street']=''
       d['streetnr']=''
       d['tel']=''
    html = ScraperWiki.scrape(url)
    doc = Nokogiri::HTML(html)
    doc.search('#FABTTXImage').each do |img|
      s = img.attribute('alt').text
     # puts s
      re = /(Nachtdienst Dienstbereit bis ..\.00h|Nachtdienst|Dienstbereit bis ..\...h)(.*)(Bundesländer|Apotheken-Notruf|www.apotheker.at)/
      md = re.match(s)
      #puts md.class
      #puts md.length
      if md
       r=md[2].gsub(/\(Weitere Daten: siehe lokale Medien\) Dienstbereit bis ..\...h /,'')
       r = r.gsub(/str\./, 'str')
r = r.gsub(/Tel:/, '..Tel') 
r = r.gsub(/\.Bezirk/, ' Bezirk')
r = r.gsub(/St\./, 'Sankt ')
       reg = /(.*?)(\..*?Tel.)\s*([0-9]*\s*[0-9]*\s*[0-9]*\s*[0-9]*\s*[0-9]*)/
       rmd = reg.scan(r)
puts rmd.to_a
      else
puts "no match: "+s 
      end
     # md = re.match(s)
     # puts md[1]
    end
  end  
end
urlsToScrap = collectUrls(seedUrls)
#scrape(urlsToScrap)

#  d = {}
#  d['location']=''
#  d['source']=url
#  menu['name']=''
#  menu['price']=''#
#  menu['description']=''
#
#  doc.search('span.monat').each ').each do |monat|
#    mA = Array.new
#    monat.text.strip.downcase.split('i').each{|m| 
#    mA.push(m.gsub(/[^[:alnum:]]/, '').capitalize)  }
#   menu['timeframe'] = mA.join(' ')
#   puts menu['timeframe']
    #  end
#  
#  doc.search('.speise').each ').each do |speisen|
#  #option.attributes["value"].value
#   puts speisen
#    speisen.to_s.split('<br>').each ').each do |speise|
#      speise_html = Nokogiri::HTML(speise)
#      sA = speise_html.search('span')
#      if sA.length >= 2
#      wA = Array.new
#      sA[0].text.split(' ').each{|w| wA.push(w.capitalize) }
#      menu['name'] = wA.join(' ')
#      menu['price'] = sA[1].text
#      puts menu['name']+' '+menu['price']
#ScraperWiki.save(['timeframe','name', 'price', 'description', 'source'], menu)
  #    end
#      puts '----------------------'
#    end
    
  
   # puts speisen.content
   
 # end
  

  
#end

##scrape(urlToScrap)
