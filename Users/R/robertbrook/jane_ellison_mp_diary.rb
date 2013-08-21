
require 'nokogiri'

starting_url = 'http://www.janeellison.net/janesdiary.php'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)
doc.search('td').each do |td|
    puts td.inner_html
    record = {'td' => td.inner_html}
    ScraperWiki.save(['td'], record)
end
