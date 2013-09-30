require 'scrapers/coopy_ruby_lib'

watch_scraper = 'hackerspacesorg_-_all_spaces'
watch_tables = ['swdata']

ScraperWiki.attach(watch_scraper)
link_tables(watch_scraper,watch_tables)

coopy_html = ScraperWiki.get_var('coopy_html') || ""
watch_tables.each do |tbl|
  diff = sync_table(watch_scraper,tbl,nil)
  ScraperWiki.commit
  result = diff.html
  if result.include? "<td>"
    now = Time.new
    coopy_html = "<h2>#{now.inspect}</h2>\n" + result + coopy_html
    ScraperWiki.save_var('coopy_html', coopy_html)
  end
end
#    coopy_html = coopy_html.gsub(/^.*2012.07.27.20.28/m,"<h2>2012-07-27 20:28")
#    ScraperWiki.save_var('coopy_html', coopy_html)
puts coopy_html

require 'scrapers/coopy_ruby_lib'

watch_scraper = 'hackerspacesorg_-_all_spaces'
watch_tables = ['swdata']

ScraperWiki.attach(watch_scraper)
link_tables(watch_scraper,watch_tables)

coopy_html = ScraperWiki.get_var('coopy_html') || ""
watch_tables.each do |tbl|
  diff = sync_table(watch_scraper,tbl,nil)
  ScraperWiki.commit
  result = diff.html
  if result.include? "<td>"
    now = Time.new
    coopy_html = "<h2>#{now.inspect}</h2>\n" + result + coopy_html
    ScraperWiki.save_var('coopy_html', coopy_html)
  end
end
#    coopy_html = coopy_html.gsub(/^.*2012.07.27.20.28/m,"<h2>2012-07-27 20:28")
#    ScraperWiki.save_var('coopy_html', coopy_html)
puts coopy_html

