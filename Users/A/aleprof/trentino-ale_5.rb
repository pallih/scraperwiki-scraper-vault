# Blank Ruby
require 'nokogiri'
require 'open-uri'
continua = true
num = 0
cercaurl = "http://www.eventiesagre.it/cerca/eventi/sez/mesi/Trentino+Alto+Adige/prov/cit/intit/rilib"
host = "http://www.eventiesagre.it/"
suburl = "pagine/Eventi/sez/mesi/Trentino+Alto+Adige/prov/cit/intit/rilib/"

doctot = Nokogiri::HTML(open(cercaurl))
totale = doctot.xpath('//a[contains(text(),"Avanti")]/@href').to_s().gsub(/^.*\//, '').gsub(/-.*/, '')

while continua == true
  continua = false;
  url = host + suburl + totale.to_s() + "-" + num.to_s() + "-data-ASC.htm"
  puts "scraping page from " + (num*10+1).to_s() + " to " + (num*10 + 10).to_s() +" of " + totale.to_s() 
  num = num + 1
  doc = Nokogiri::HTML(open(url))
  doc.xpath('//tr[@class="elenco1 vevent"]').each do | blocco |
    urlevento = host + blocco.xpath('.//a[@class="url summary"]/@href').to_s()
    tipoevento = blocco.xpath('.//span[@class="testoxxsmall category"]/i/text()')
    # puts tipoevento
    nomeevento = blocco.xpath('.//a[@class="url summary"]/text()')
    # puts "nomeevento:".concat(nomeevento.to_s())
    altri = blocco.xpath('.//span[@class="testoxxsmall"]')
    sottotitolo = altri.xpath('./i/b/text()')
    # puts "sottotitolo:".concat(sottotitolo.to_s())
    datainizio =  altri.xpath('.//span[@class="dtstart"]/text()')
    # puts "datainizio:".concat(datainizio.to_s())
    datafine =  altri.xpath('.//span[@class="dtend"]/text()')
    # puts "datafine:".concat(datafine.to_s())
    # doc2 = Nokogiri::HTML(open(url))
    # puts doc2
    # nomeevento = doc2.xpath('//div[@class="vevent"]')
    location = blocco.xpath('.//span[@class="location"]')
    regione = location.xpath('./b/text()')
    luogo = location.xpath('./i/text()')
    strprovincia = /\((.*)\)/.match(luogo.to_s())
    provincia = ""
    if strprovincia != nil then provincia = strprovincia[1].to_s() end
    localita = /[^\(]*/.match(luogo.to_s()).to_s()
    description = blocco.xpath('.//span[@class="testoxxsmall description"]/text()').to_s()
    imgurl = blocco.xpath('.//img/@src').to_s()
    doc2 = Nokogiri::HTML(open(urlevento))
    locationvcard = doc2.xpath('//div[@class="location vcard"]')
    locationlogourl = locationvcard.xpath('.//img/@src').to_s()
    locationinfocontact = ""
    locationinfocontact = doc2.xpath('//img[@alt="info evento"]/../../td[2]').inner_html().gsub(/<[^>]*>/, ' ')
    locationemail = doc2.xpath('//img[@alt="e-mail"]/../a/text()').to_s()
    locationweb = doc2.xpath('//img[@alt="Sito Web Esterno"]/../a/@href').to_s()
    locationfonte = doc2.xpath('//b[text()="Fonte:"]/../text()').to_s()

    data = {       
      'urlevento' => urlevento,
      'tipoevento' => tipoevento, 
      'nomeevento' => nomeevento,
      'sottotitolo' => sottotitolo,
      'datainizio' => datainizio,
      'datafine' => datafine,
      'regione' => regione,
      'localita' => localita,
      'provincia' => provincia,
      'description' => description,
      'imgurl' => imgurl,
      'locationlogourl' => locationlogourl,
      'locationinfocontact' => locationinfocontact,
      'locationemail' => locationemail,
      'locationweb' => locationweb,
      'locationfonte' => locationfonte
    }

    ScraperWiki.save_sqlite(unique_keys=['urlevento'], data=data)
    continua = true
  end
end

