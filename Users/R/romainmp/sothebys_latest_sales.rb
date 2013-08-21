# By RMP under the MIT License.
# 12/02/2012

#require 'rubygems'
require 'mechanize'
require 'open-uri'

a = Mechanize.new { |agent| agent.user_agent_alias = 'iPhone' }
ScraperWiki.save_metadata('data_columns', ['Sale', 'Title', 'Link', 'Infos'])

url = 'http://m.sothebys.com/en/auction_results.html'

while url
  puts "INF: Visiting #{url}"
  l = a.get(url)
  
  unless l.nil? 
    #For each Sale, save Title, URI and sale number
    l.search("div.listImg div.right").each do |sale|
      record = {}
      record['Year'] = sale.at('a').attributes['href'].value.split("\/")[4]
      record['Title'] = sale.at('a').text
      record['Link'] = URI.join('http://m.sothebys.com',sale.at('a').attributes['href'].value).to_s
      record['Sale'] = sale.at('h3').content
      record['Infos'] = sale.css('p.small').inner_html
      ScraperWiki.save(["Sale"], record)
    end
    n = l.at(".bottom .right a")
    unless n.nil? 
      url = n.attributes['href'].value
    else
      url = nil
    end
  else
    break
  end
end