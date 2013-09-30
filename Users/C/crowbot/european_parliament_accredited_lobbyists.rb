require 'nokogiri'

base_url = "http://www.europarl.europa.eu/parliament/expert/lobbyAlphaOrderByOrg.do?"

language = "SV"
letter = "A"

html = ScraperWiki.scrape(base_url + "letter=#{letter}&language=#{language}")
doc = Nokogiri::HTML(html)
require 'nokogiri'

base_url = "http://www.europarl.europa.eu/parliament/expert/lobbyAlphaOrderByOrg.do?"

language = "SV"
letter = "A"

html = ScraperWiki.scrape(base_url + "letter=#{letter}&language=#{language}")
doc = Nokogiri::HTML(html)
