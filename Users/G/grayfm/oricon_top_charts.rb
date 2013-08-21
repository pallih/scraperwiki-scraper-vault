###############################################################################
# Oricon Top Charts
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.oricon.co.jp/rank/ns/?cat_id=upperrank'
html = Nokogiri::HTML(ScraperWiki.scrape(starting_url))
ScraperWiki.save_var('data_columns', ['Rank', 'Score', 'Artist', 'Track', 'Released'])

increment = 1
html.search('table.rank_m_01 tbody tr').each do |row|
  increment += 1
  record = {}
  record['Rank']      = increment
  record['Score']    = row.css('td')[1].inner_text
  record['Artist']     = row.css('td')[2].inner_text
  record['Track']  = row.css('td')[3].inner_text
  record['Released'] = row.css('td')[4].inner_text
  puts record

  ScraperWiki.save(["Rank"], record)
end