require 'nokogiri'

uri = URI.parse('http://portal.gov.cz/portal/rejstriky/data/10013/index-2013.xml')

puts "Fetching #{uri.to_s}"

html = ScraperWiki::scrape(uri.to_s)
doc = Nokogiri::XML(html)

items = doc.xpath("//pvs:Rejstrik/pvs:Polozka/pvs:PolozkaURL", {"pvs" => "http://portal.gov.cz/portal/xsd/PvsRejstrikObsah"}).collect(&:inner_text)

puts "Fetching #{items.size} pages"
items.each{|item|
  puts "Fetching #{item}"
  html = ScraperWiki::scrape(item)
  doc = Nokogiri::XML(html)
  puts doc.xpath("//pvs:PREDMET", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text

  ScraperWiki::save_sqlite(unique_keys=[:uri], data={
    :uri => item,
    :predmet => doc.xpath("//pvs:PREDMET", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :partner_nazev => doc.xpath("//pvs:PARTNER_NAZEV", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :partner_ico => doc.xpath("//pvs:PARTNER_ICO", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :partner_adresa => doc.xpath("//pvs:PARTNER_ADRESA", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :datum_vystaveni => doc.xpath("//pvs:DATUM_VYSTAVENI", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :agenda => doc.xpath("//pvs:AGENDA", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :cislo => doc.xpath("//pvs:CISLO", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :schvalil => doc.xpath("//pvs:SCHVALIL", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :castka_bez_dph => doc.xpath("//pvs:CASTKA_BEZ_DPH", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :castka_s_dph => doc.xpath("//pvs:CASTKA_S_DPH", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :typ_dokumentu => doc.xpath("//pvs:TYP_DOKUMENTU", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text
  })
}

require 'nokogiri'

uri = URI.parse('http://portal.gov.cz/portal/rejstriky/data/10013/index-2013.xml')

puts "Fetching #{uri.to_s}"

html = ScraperWiki::scrape(uri.to_s)
doc = Nokogiri::XML(html)

items = doc.xpath("//pvs:Rejstrik/pvs:Polozka/pvs:PolozkaURL", {"pvs" => "http://portal.gov.cz/portal/xsd/PvsRejstrikObsah"}).collect(&:inner_text)

puts "Fetching #{items.size} pages"
items.each{|item|
  puts "Fetching #{item}"
  html = ScraperWiki::scrape(item)
  doc = Nokogiri::XML(html)
  puts doc.xpath("//pvs:PREDMET", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text

  ScraperWiki::save_sqlite(unique_keys=[:uri], data={
    :uri => item,
    :predmet => doc.xpath("//pvs:PREDMET", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :partner_nazev => doc.xpath("//pvs:PARTNER_NAZEV", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :partner_ico => doc.xpath("//pvs:PARTNER_ICO", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :partner_adresa => doc.xpath("//pvs:PARTNER_ADRESA", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :datum_vystaveni => doc.xpath("//pvs:DATUM_VYSTAVENI", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :agenda => doc.xpath("//pvs:AGENDA", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :cislo => doc.xpath("//pvs:CISLO", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :schvalil => doc.xpath("//pvs:SCHVALIL", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :castka_bez_dph => doc.xpath("//pvs:CASTKA_BEZ_DPH", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :castka_s_dph => doc.xpath("//pvs:CASTKA_S_DPH", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text,
    :typ_dokumentu => doc.xpath("//pvs:TYP_DOKUMENTU", {"pvs"=>"http://portal.gov.cz/portal/xsd/PvsRejstrikData"}).inner_text
  })
}

