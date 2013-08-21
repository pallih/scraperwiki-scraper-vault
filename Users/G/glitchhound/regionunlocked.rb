require 'nokogiri'
require 'open-uri'

doc = Nokogiri::HTML open("http://gaming.wikia.com/wiki/Region_Free_Xbox_360_Games")

doc.search("tr").each do |row|
  cells = row.search 'td'
  if cells.count == 5
    game_title = cells[0].search("a").inner_html.strip.downcase
    game_region = cells[1].inner_html.strip.upcase
    ntscj = cells[2].inner_html.strip.capitalize
    ntscu = cells[3].inner_html.strip.capitalize
    pal = cells[4].inner_html.strip.capitalize
    final_game = {title: game_title,
                  region: game_region,
                  ntsc_j: ntscj,
                  ntsc_u: ntscu,
                  pal: pal}
    ScraperWiki::save_sqlite(['title', 'region'], final_game)
  end
end

