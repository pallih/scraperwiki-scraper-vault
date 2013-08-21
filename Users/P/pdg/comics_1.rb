# Blank Ruby
ScraperWiki::attach("xkcd")
xkcd = ScraperWiki::select( "* from xkcd.swdata limit 3" ) 
ScraperWiki::attach("explosm")
xkcd = ScraperWiki::select( "* from explosm.swdata limit 3" ) 

puts "<h1>xkcd</h1>"
xkcd.each do |comic|
puts "<h2>#{CGI::escapeHTML(comic['ctitle'])}</h2>"
puts "<a href='#{comic['link']}'><img src='#{comic['image']}' title=\"#{CGI::escapeHTML(comic['alt'])}\" /></a>"
end

puts "<h1>Cyanide and Happiness</h1>"
explosm.each do |comic|
puts "<a href='#{comic['link']}'><img src='#{comic['image']}' /></a>"
end
