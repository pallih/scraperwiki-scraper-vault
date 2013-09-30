require 'nokogiri'
require 'uri'

url = 'http://www.parliament.uk/business/committees/committees-a-z'
base_url = URI.parse url
html = ScraperWiki.scrape(url)

doc = Nokogiri::HTML(html)
candidate_hrefs = doc.search("a[@href]")

hrefs = candidate_hrefs.select {|this_one| !this_one.nil?}

hrefs.each do |a|
  if a['href'] =~ /business\/committees\/committees-a-z\//
    title = a.inner_html
    permalink = 'http://www.parliament.uk' + a['href']
    unless ['Committees A-Z','Commons Select','Lords Select','Joint Select','Other Committees','Former Committees','Back to top'].include? title
      path_bits = a['href'].split('/')

      record = {'permalink' => permalink, 'name' => a.inner_html, 'type' => path_bits[4], 'stub' => path_bits[5]}
      ScraperWiki.save(['permalink'], record)
    end
  end
end
require 'nokogiri'
require 'uri'

url = 'http://www.parliament.uk/business/committees/committees-a-z'
base_url = URI.parse url
html = ScraperWiki.scrape(url)

doc = Nokogiri::HTML(html)
candidate_hrefs = doc.search("a[@href]")

hrefs = candidate_hrefs.select {|this_one| !this_one.nil?}

hrefs.each do |a|
  if a['href'] =~ /business\/committees\/committees-a-z\//
    title = a.inner_html
    permalink = 'http://www.parliament.uk' + a['href']
    unless ['Committees A-Z','Commons Select','Lords Select','Joint Select','Other Committees','Former Committees','Back to top'].include? title
      path_bits = a['href'].split('/')

      record = {'permalink' => permalink, 'name' => a.inner_html, 'type' => path_bits[4], 'stub' => path_bits[5]}
      ScraperWiki.save(['permalink'], record)
    end
  end
end
