require 'typhoeus'
require 'nokogiri'

# Category 15 is Digital / Interactive Agencies
category = 15

response = Typhoeus::Request.post("http://mumbrella.com.au/wp-content/plugins/business-directory/requests.php",
                                :params        => {action: "SearchListings", category: category})

# This returns javascript that inserts some html. Extract the html
html = response.body.match(/innerHTML = '(.*)'/)[1]

Nokogiri::HTML(html).search('td').each do |td|
  ScraperWiki.save_sqlite([], {
    website: td.at('a')['href'][2..-3], 
    name: td.at('a').inner_text,
    description: td.at('p').inner_html
  })
end

