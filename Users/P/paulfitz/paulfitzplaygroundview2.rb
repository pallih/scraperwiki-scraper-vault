# Work on highlighter diff generation
#   http://share.find.coop/doc/spec_hilite.html

# Name of scraper to monitor
watch_scraper = 'paulfitzplayground'

# Name of tables to monitor
watch_tables = ['bridge_evolve']

# If PRIMARY KEY not set up for a watched table, override it here with a list of columns
watch_keys = { 'bridge_evolve' => ['bridge'] }

# Bring in library stored in "coopy_ruby_lib"
# No easy way to import ruby code right now?  Use workaround.
coopy_src = ScraperWiki.get_var('coopy_src')
if coopy_src.nil? 
  require 'json'
  # coopy_src = JSON.parse(ScraperWiki.scrape("http://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=coopy_ruby_lib&version=-1"))[0]["code"]
  coopy_src = ScraperWiki.scrape("https://scraperwiki.com/editor/raw/coopy_ruby_lib")
  ScraperWiki.save_var('coopy_src', coopy_src)
end
eval(coopy_src)

ScraperWiki.attach(watch_scraper)
link_tables(watch_scraper,watch_tables)

coopy_html = ScraperWiki.get_var('coopy_html') || ""
watch_tables.each do |tbl|
  diff = sync_table(watch_scraper,tbl,watch_keys[tbl])
  result = diff.html
  if result.include? "<td>"
    coopy_html = result + coopy_html
    ScraperWiki.save_var('coopy_html', coopy_html)
  end
end
print coopy_html
