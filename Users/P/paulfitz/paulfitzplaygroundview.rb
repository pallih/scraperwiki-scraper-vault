# Work on highlighter diff generation
#   http://share.find.coop/doc/spec_hilite.html

sourcescraper = 'paulfitzplayground'

ScraperWiki.attach("paulfitzplayground")

# Bring in library stored in "coopy_ruby_lib"
# No easy way to import ruby code right now?  Use workaround.
coopy_src = ScraperWiki.get_var('coopy_src')
if coopy_src.nil? 
  require 'json'
  coopy_src = JSON.parse(ScraperWiki.scrape("http://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=coopy_ruby_lib&version=-1"))[0]["code"]
  ScraperWiki.save_var('coopy_src', coopy_src)
end
eval(coopy_src)

sql = ScraperwikiSqlWrapper.new(ScraperWiki)
sql.set_primary_key(["bridge"])
cmp = SqlCompare.new(sql,"paulfitzplayground.broken_bridge","paulfitzplayground.bridge")
render = DiffRenderHtml.new
cmp.set_output(render)
# puts "names " + sql.columns("paulfitzplayground.broken_bridge").inspect
cmp.apply
print render.to_string

# Work on highlighter diff generation
#   http://share.find.coop/doc/spec_hilite.html

sourcescraper = 'paulfitzplayground'

ScraperWiki.attach("paulfitzplayground")

# Bring in library stored in "coopy_ruby_lib"
# No easy way to import ruby code right now?  Use workaround.
coopy_src = ScraperWiki.get_var('coopy_src')
if coopy_src.nil? 
  require 'json'
  coopy_src = JSON.parse(ScraperWiki.scrape("http://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name=coopy_ruby_lib&version=-1"))[0]["code"]
  ScraperWiki.save_var('coopy_src', coopy_src)
end
eval(coopy_src)

sql = ScraperwikiSqlWrapper.new(ScraperWiki)
sql.set_primary_key(["bridge"])
cmp = SqlCompare.new(sql,"paulfitzplayground.broken_bridge","paulfitzplayground.bridge")
render = DiffRenderHtml.new
cmp.set_output(render)
# puts "names " + sql.columns("paulfitzplayground.broken_bridge").inspect
cmp.apply
print render.to_string

