# Blank Ruby

require 'nokogiri'

LINEE = []

GET_LINEE_PAGE = "http://www.atb.bergamo.it/ITA/Default.aspx?SEZ=2&PAG=38&MOD=LIN"
GET_LINEE_XPATH = "//div[@id='content']//table//tr/th//a"

GET_LINEA_PAGE = "http://www.atb.bergamo.it/ITA/Default.aspx?language=ITA&SEZ=2&PAG=38&MOD=LIN&COD="
MARKER_REGEX = /addMarker\((.+),(.+),'(.+)','(.+)'\)/

Nokogiri::HTML(ScraperWiki.scrape(GET_LINEE_PAGE)).xpath(GET_LINEE_XPATH).each do |linea|
  stripped = linea.content.strip
  stripped.scan(/Linea (.+)/)
  LINEE << {:id => $1, :linea => stripped}
end

LINEE.each do |linea|
  l = Nokogiri::HTML(ScraperWiki.scrape("#{GET_LINEA_PAGE}#{linea[:id]}"))
  entries = l.xpath("//body").attribute("onload").content.strip.split ";"
  entries[1..-1].each do |marker|
    marker.scan(MARKER_REGEX)

    addit = Nokogiri::HTML($3).xpath("//span").children
    ScraperWiki.save(['_id'], {'geo_lat' => $1.to_f,
                                'geo_lon' => $2.to_f,
                            '_id' => $4,
                            'linea' => linea[:linea],
                            'ind' => addit[0].content.strip.scan(/Palina #{$4} - (.+)/).flatten.first.capitalize,
                            'loc' => addit[2].content.strip})
  end
end