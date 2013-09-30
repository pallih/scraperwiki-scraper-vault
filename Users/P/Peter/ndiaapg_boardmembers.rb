# Blank Ruby


require 'mechanize'
require'nokogiri'



agent = Mechanize.new
agent.get('http://www.ndiaapg.org/board.php')
page = agent.page

doc = Nokogiri::HTML(page.body)

doc.css('html body div#container_out div.container_in div#center_out div.center_in div#main_out div.main_in div.officers ul').collect do |row|
results = {}
results['Officer Name'] = row.css('li.officer_name').inner_text.strip
results['Officer Title'] = row.css('li.officer_title').inner_text.strip
results['Officer Email'] = row.css('li.officer_data b a').inner_text.strip 
puts results['Officer Phone'] = row.css('li.officer_data b').inner_text.strip.sub(results['Officer Email'], '').strip
results['Officer Info'] = row.css('li.officer_data').inner_text.strip.sub(results['Officer Email'], '').strip.sub(results['Officer Phone'], '').strip.sub('Phone:', '').strip.sub('Email:', '').strip
#puts results


ScraperWiki.save(['Officer Name'], results)

end

# Blank Ruby


require 'mechanize'
require'nokogiri'



agent = Mechanize.new
agent.get('http://www.ndiaapg.org/board.php')
page = agent.page

doc = Nokogiri::HTML(page.body)

doc.css('html body div#container_out div.container_in div#center_out div.center_in div#main_out div.main_in div.officers ul').collect do |row|
results = {}
results['Officer Name'] = row.css('li.officer_name').inner_text.strip
results['Officer Title'] = row.css('li.officer_title').inner_text.strip
results['Officer Email'] = row.css('li.officer_data b a').inner_text.strip 
puts results['Officer Phone'] = row.css('li.officer_data b').inner_text.strip.sub(results['Officer Email'], '').strip
results['Officer Info'] = row.css('li.officer_data').inner_text.strip.sub(results['Officer Email'], '').strip.sub(results['Officer Phone'], '').strip.sub('Phone:', '').strip.sub('Email:', '').strip
#puts results


ScraperWiki.save(['Officer Name'], results)

end

