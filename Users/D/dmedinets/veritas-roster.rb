require 'nokogiri'

# retrieve a page
starting_url = 'http://us.battle.net/wow/en/guild/earthen-ring/veritas/roster'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)
roster = doc.css("#roster")
#puts roster

roster.search('tr').each do |tr|
    name_node = tr.search('td').first
    unless name_node.nil? 
      name = name_node.inner_text.strip
      next if name == 'Nothing found.'
      url = name_node.search('a').first.attribute('href').value
      ScraperWiki.save(unique_keys = ['name'], data = { 'name' => name, 'url' => url })
    end
end

# The End.

require 'nokogiri'

# retrieve a page
starting_url = 'http://us.battle.net/wow/en/guild/earthen-ring/veritas/roster'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)
roster = doc.css("#roster")
#puts roster

roster.search('tr').each do |tr|
    name_node = tr.search('td').first
    unless name_node.nil? 
      name = name_node.inner_text.strip
      next if name == 'Nothing found.'
      url = name_node.search('a').first.attribute('href').value
      ScraperWiki.save(unique_keys = ['name'], data = { 'name' => name, 'url' => url })
    end
end

# The End.

