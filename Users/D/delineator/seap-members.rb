require 'hpricot'
# require 'open-uri'
starting_url = 'http://seap.be/member_list.html'
html = ScraperWiki.scrape(starting_url)
# html = open(starting_url).read
# puts html

# use Hpricot to get all <td> tags
doc = Hpricot(html)
doc.search('tr').each do |row|
  cells = row.search('td')
  puts '0 ' + cells[0].inner_html
  puts '1 ' + cells[1].inner_html
  puts '2 ' + cells[2].inner_html
    record = {'td' => td.inner_html}
   ScraperWiki.save(['td'], record)
end
require 'hpricot'
# require 'open-uri'
starting_url = 'http://seap.be/member_list.html'
html = ScraperWiki.scrape(starting_url)
# html = open(starting_url).read
# puts html

# use Hpricot to get all <td> tags
doc = Hpricot(html)
doc.search('tr').each do |row|
  cells = row.search('td')
  puts '0 ' + cells[0].inner_html
  puts '1 ' + cells[1].inner_html
  puts '2 ' + cells[2].inner_html
    record = {'td' => td.inner_html}
   ScraperWiki.save(['td'], record)
end
