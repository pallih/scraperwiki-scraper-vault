# Escarba sucursales bancarias de http://oficinas.bankimia.com/
# http://rubular.com/
# http://www.ruby-doc.org/core-1.9.2/
# http://nokogiri.org/tutorials/

require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'scraperwiki'
require 'csv'
 
#page = MetaInspector.new('http://oficinas.bankimia.com/')
page = Nokogiri::HTML(open("http://oficinas.bankimia.com/"))

# tomamos solo las paginas internas que cumplan /e\d{4}/ enlaces de bancos
# http://oficinas.bankimia.com/oficinas-la-caixa-e4039
l_banco = page.xpath("//a").map{|a| a['href']}.select{|l| l=~/e\d{4}/ }
page = nil

# tomamos solo las paginas internas que cumplan /en\d{4}pro/ enlaces de bancos
# http://oficinas.bankimia.com/oficinas-la-caixa-en-alava-en4039-pro1
p_provincias=[] 
l_banco.each do |lb|
  #puts "http://oficinas.bankimia.com"+lb.to_s
  p_provincias << Nokogiri::HTML(open("http://oficinas.bankimia.com"+lb.to_s))
end
l_banco = nil
l_provincias = p_provincias.map{|pb| pb.xpath("//a")}.flatten.map{|ab| ab['href']}.select{|lb| lb=~/en\d{4}-pro/ }
p_provincias = nil

# tomamos solo las paginas internas que cumplan /oficina-\d+[a-z-]+\d+-bk\d{4}/ enlaces de bancos
# http://oficinas.bankimia.com/oficina-4708-de-la-caixa-o235279-bk4039
l_oficinas = [] 
l_provincias.each do |lp|
  p = Nokogiri::HTML(open("http://oficinas.bankimia.com"+lp.to_s))
  l_oficinas << p.xpath("//a").map{|ap| ap['href']}.select{|lb| lb=~/oficina-\d+[a-z-]+\d+-bk\d{4}/ } 
end
l_provincias = nil
l_oficinas.flatten!

i=1
 
l_oficinas.each do |lo|
  record={}
  record["cod_oficina"], id, record["id_banco"] = lo.to_s.scan(/\d+/)
  xml = Nokogiri::HTML(open("http://oficinas.bankimia.com"+lo.to_s))
  coor = xml.xpath("//script").detect{|xc| xc.to_s.include?('new google.maps.LatLng')}.to_s
  re = /(-?\d+\.\d+)/
  record["id"] = i
  record["x"], record["y"] =  coor.scan(re).flatten
  record["name"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="name"}.children.to_s
  record["streetAddress"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="streetAddress"}.children.to_s
  record["postalCode"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="postalCode"}.children.to_s
  record["locality"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="addressCountry"}.children.to_s
  record["province"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="addressLocality"}.children.to_s
  record["telephone"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="telephone"}.children.to_s
  record["faxNumber"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="faxNumber"}.children.to_s
#email = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="email"}.children.to_s
  i+=1
  ScraperWiki.save_sqlite(["id"], record)
  sleep rand(5)
end
# Escarba sucursales bancarias de http://oficinas.bankimia.com/
# http://rubular.com/
# http://www.ruby-doc.org/core-1.9.2/
# http://nokogiri.org/tutorials/

require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'scraperwiki'
require 'csv'
 
#page = MetaInspector.new('http://oficinas.bankimia.com/')
page = Nokogiri::HTML(open("http://oficinas.bankimia.com/"))

# tomamos solo las paginas internas que cumplan /e\d{4}/ enlaces de bancos
# http://oficinas.bankimia.com/oficinas-la-caixa-e4039
l_banco = page.xpath("//a").map{|a| a['href']}.select{|l| l=~/e\d{4}/ }
page = nil

# tomamos solo las paginas internas que cumplan /en\d{4}pro/ enlaces de bancos
# http://oficinas.bankimia.com/oficinas-la-caixa-en-alava-en4039-pro1
p_provincias=[] 
l_banco.each do |lb|
  #puts "http://oficinas.bankimia.com"+lb.to_s
  p_provincias << Nokogiri::HTML(open("http://oficinas.bankimia.com"+lb.to_s))
end
l_banco = nil
l_provincias = p_provincias.map{|pb| pb.xpath("//a")}.flatten.map{|ab| ab['href']}.select{|lb| lb=~/en\d{4}-pro/ }
p_provincias = nil

# tomamos solo las paginas internas que cumplan /oficina-\d+[a-z-]+\d+-bk\d{4}/ enlaces de bancos
# http://oficinas.bankimia.com/oficina-4708-de-la-caixa-o235279-bk4039
l_oficinas = [] 
l_provincias.each do |lp|
  p = Nokogiri::HTML(open("http://oficinas.bankimia.com"+lp.to_s))
  l_oficinas << p.xpath("//a").map{|ap| ap['href']}.select{|lb| lb=~/oficina-\d+[a-z-]+\d+-bk\d{4}/ } 
end
l_provincias = nil
l_oficinas.flatten!

i=1
 
l_oficinas.each do |lo|
  record={}
  record["cod_oficina"], id, record["id_banco"] = lo.to_s.scan(/\d+/)
  xml = Nokogiri::HTML(open("http://oficinas.bankimia.com"+lo.to_s))
  coor = xml.xpath("//script").detect{|xc| xc.to_s.include?('new google.maps.LatLng')}.to_s
  re = /(-?\d+\.\d+)/
  record["id"] = i
  record["x"], record["y"] =  coor.scan(re).flatten
  record["name"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="name"}.children.to_s
  record["streetAddress"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="streetAddress"}.children.to_s
  record["postalCode"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="postalCode"}.children.to_s
  record["locality"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="addressCountry"}.children.to_s
  record["province"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="addressLocality"}.children.to_s
  record["telephone"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="telephone"}.children.to_s
  record["faxNumber"] = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="faxNumber"}.children.to_s
#email = xml.xpath("//span").detect{|s| s.attributes.has_key?("itemprop") && s.attributes["itemprop"].value=="email"}.children.to_s
  i+=1
  ScraperWiki.save_sqlite(["id"], record)
  sleep rand(5)
end
