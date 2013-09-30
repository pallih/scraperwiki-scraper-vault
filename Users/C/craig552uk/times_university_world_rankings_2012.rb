#
# Scraper to get THE World University Rankings
#
# Only fetches first 200 universities as data is witheld for 201-400
#
# Author: Craig Russell <craig@craig-russell.co.uk>
#

require 'hpricot'

url = 'http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/001-200'

doc  = Hpricot(ScraperWiki::scrape(url))
rows = doc.search('table.ranking tbody tr')

rows.each do |tr| 
  uni = {}
  uni['id']                          = tr[:id].strip.gsub('rating-','')
  uni['rank']                        = tr.search('.rank strong').inner_html.strip
  uni['name']                        = tr.search('.uni a').inner_html.strip.gsub(/[^a-zA-Z0-9 ]/, '') # Strip unfriendly chars - not perfect
  uni['country']                     = tr.search('.region-title').inner_html.strip
  uni['score-overall']               = tr.search('.overall-score').first['data-overall'].strip
  uni['score-teaching']              = tr.search('.overall-score').first['data-teaching'].strip
  uni['score-international-outlook'] = tr.search('.overall-score').first['data-international-outlook'].strip
  uni['score-industry-income']       = tr.search('.overall-score').first['data-industry-income'].strip
  uni['score-research']              = tr.search('.overall-score').first['data-research'].strip
  uni['score-citations']             = tr.search('.overall-score').first['data-citations'].strip
  ScraperWiki::save_sqlite(unique_keys=[:id], data=uni)
end

#
# Scraper to get THE World University Rankings
#
# Only fetches first 200 universities as data is witheld for 201-400
#
# Author: Craig Russell <craig@craig-russell.co.uk>
#

require 'hpricot'

url = 'http://www.timeshighereducation.co.uk/world-university-rankings/2012-13/world-ranking/range/001-200'

doc  = Hpricot(ScraperWiki::scrape(url))
rows = doc.search('table.ranking tbody tr')

rows.each do |tr| 
  uni = {}
  uni['id']                          = tr[:id].strip.gsub('rating-','')
  uni['rank']                        = tr.search('.rank strong').inner_html.strip
  uni['name']                        = tr.search('.uni a').inner_html.strip.gsub(/[^a-zA-Z0-9 ]/, '') # Strip unfriendly chars - not perfect
  uni['country']                     = tr.search('.region-title').inner_html.strip
  uni['score-overall']               = tr.search('.overall-score').first['data-overall'].strip
  uni['score-teaching']              = tr.search('.overall-score').first['data-teaching'].strip
  uni['score-international-outlook'] = tr.search('.overall-score').first['data-international-outlook'].strip
  uni['score-industry-income']       = tr.search('.overall-score').first['data-industry-income'].strip
  uni['score-research']              = tr.search('.overall-score').first['data-research'].strip
  uni['score-citations']             = tr.search('.overall-score').first['data-citations'].strip
  ScraperWiki::save_sqlite(unique_keys=[:id], data=uni)
end

