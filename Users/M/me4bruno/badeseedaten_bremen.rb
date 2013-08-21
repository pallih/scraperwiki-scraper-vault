require 'nokogiri'

baseurl = "http://www.umwelt.bremen.de/sixcms/detail.php?template=99_od_d"

basehtml = ScraperWiki.scrape(baseurl)
# falsch geschriebenes start tag ersetzen durch das richtige start tag
basehtml.gsub!("Deitailseite$i", "Detailseite")

basedoc = Nokogiri::XML(basehtml)
badeseenNodes = basedoc.xpath(".//Badesee")
badeseenNodes.each do |badeseeNode|

  name = badeseeNode.xpath(".//Name").text
  temperatur = badeseeNode.xpath(".//Temperatur").text
  badeempfehlung = badeseeNode.xpath(".//Badeempfehlung").text
  bedenklichkeiten = badeseeNode.xpath(".//Bedenklichkeiten").text
  letzte_messung = badeseeNode.xpath(".//Letzte_messung").text

  result = {
    'name' => name,
    'temperatur' => temperatur,
    'badeempfehlung' => badeempfehlung,
    'bedenklichkeiten' => bedenklichkeiten,
    'letzte_messung' => letzte_messung
  }

  unique_keys = ['name']
  
  ScraperWiki.save_sqlite(unique_keys, result)
end
