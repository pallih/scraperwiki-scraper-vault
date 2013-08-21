require 'nokogiri'
require 'iconv'

def replaces(str)
  str = str.gsub(/[\r\n\t]/, "").gsub("<br>", " ").gsub("<br />", " ")
end

begin
  ScraperWiki::sqliteexecute("delete from swdata")
rescue Exception=>e
  #...
end


html = ScraperWiki::scrape('http://www.meteo.cat/xema/AppJava/Mapper.do', {'inputSource' => 'SeleccioTotesEstacions', 'team' => 'ObservacioTeledeteccio'})

html = Iconv.new('ISO-8859-1//IGNORE//TRANSLIT', 'UTF-8').iconv(html)

doc = Nokogiri::HTML html

doc.search("table[@class='sortable'] tbody tr").each do |row|
  cells = row.search 'td'
  if cells.count > 10
    data = {}
    data["locality"] = replaces(cells[0].search('a').first.inner_html).gsub(/\[.*\]/,"")
    data["data"] = replaces(cells[3].search('span').first.inner_html)
    data["tavg"] = replaces(cells[4].search('span').first.inner_html)
    data["tmax"] = replaces(cells[5].search('span').first.inner_html)
    data["tmin"] = replaces(cells[6].search('span').first.inner_html)
    data["humidity"] = replaces(cells[7].search('span').first.inner_html)
    ScraperWiki::save_sqlite(["locality"], data)
  end
end

