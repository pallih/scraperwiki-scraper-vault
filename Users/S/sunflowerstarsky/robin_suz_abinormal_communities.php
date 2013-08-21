<?php
require 'nokogiri'

html = ScraperWiki.scrape("http://www.aboriginalcanada.gc.ca/acp/community/site.nsf/eng/mb-all-b.html")
puts html

doc = Nokogiri::HTML(html)
for v in doc.search("#results>ul>li>a")
  puts v.inner_html

  data = {
    'community' => v.inner_html 
  }

  ScraperWiki.save_sqlite(unique_keys=['community'], data=data)
end

?>
