# Blank Ruby
require 'nokogiri'
require 'open-uri'




#aquire list of all PLZ in austria i.e. via http://www.plz-postleitzahl.com/at/index.cfm

@baseUrl = 'http://www.plz-postleitzahl.com/index.cfm?parm='
seedUrls = [@baseUrl+'at/index.cfm']
paramValues = ['Burgenland', 'Klagenfurt', 'Nieder%F6sterreich', 'Ober%F6sterreich', 'Salzburg', 'Steiermark', 'Tirol', 'Vorarlberg', 'Wien']
urlsToScrap = []

def collectPlz(seedUrlsA)
  urlCollectorA = Array.new
  seedUrlsA.each do |url|
   puts url
   # urlCollectorA.push(url)
    html = ScraperWiki.scrape(url)
    puts html
    doc = Nokogiri::HTML(html) 
    #puts doc
#/HTML[1]/BODY[1]/TABLE[1]/TBODY[1]/TR[1]/TD[2]/TABLE[1]/TBODY[1]/TR[4]/TD[1]/TABLE[1]/TBODY[1]/TR[2]/TD[1]/TABLE[1]/TBODY[1]/TR[1]/TD[1]/TABLE[1]/TBODY[1]/TR[3]/TD[1]/TABLE[1]/TBODY[1]/TR[2]/TD[1]/TABLE[1]/TBODY[1]/TR[2]/TD[3]
    doc.xpath('//a').each do |a|
      #puts a
      #urlCollectorA.push(@baseUrl+nav.attribute('href'))
    end
  end
  #return urlCollectorA
end

def loopIt(paramValues)
  paramValues.each do |param|
    collectPlz(@baseUrl+param)
  end
end

loopIt(paramValues)
