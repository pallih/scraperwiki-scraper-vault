require 'nokogiri'

starting_url = 'http://www.parliament.uk/edm/2010-11/by-number'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)
doc.search('tr').each do |tr|
    x = tr.search('td').children
    if x[0] then
      p x
      p x[4].values 
    end
      #edm_number = td.inner_html if td['class'] == "number"
      #record = {'td' => td.inner_html, 'number' => edm_number}
      #ScraperWiki.save(['td'], record)
end
