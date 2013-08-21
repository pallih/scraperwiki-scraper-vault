require 'nokogiri'
html = ScraperWiki::scrape("http://www.bbc.co.uk/sport/olympics/2012/medals/countries")
doc = Nokogiri::HTML(html)

doc.css('.medals-table').each do |table|
  table.css('tbody tr').each do |row|
    medal_info = {}
    country_info = row.at_css('.country-text')
    medal_info[:country_name] = country_info['data-country-name']
    medal_info[:country_code] = country_info['data-country-code']
    ['gold', 'silver', 'bronze'].each do |medal|
      medal_info[medal] = row.at_css("td.#{medal}").inner_html.to_i
    end
    ScraperWiki.save([:country_code], medal_info)
  end
end
