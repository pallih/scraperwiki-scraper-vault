###############################################################################
# TowerBridge
###############################################################################

require 'hpricot'
require 'time'

MINUTE=60

starting_url = 'http://www.towerbridge.co.uk/TBE/EN/BridgeLiftTimes/'
html = ScraperWiki.scrape(starting_url)

doc = Hpricot(html)

rows = doc.search("table tr")
rows.shift

rows.each do |row|
  cells = row.search("td")
  timestring = (cells[0].html + " " + cells[1].html + " " + cells[2].html).gsub("&nbsp;", " ")
  time = Time.parse(timestring)
  open_time = time - (5*MINUTE)
  close_time = time + (5*MINUTE)

  vessel = cells[3].html
  direction_of_vessel = cells[4].html.downcase
  record = {"vessel" => vessel, "open_time" => open_time, "close_time" => close_time, "direction" => direction_of_vessel}
  ScraperWiki.save(%w{vessel direction open_time close_time}, record)
end
