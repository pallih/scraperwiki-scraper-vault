###############################################################################
# Basic scraper
###############################################################################
require 'net/http'
require 'uri'

require 'nokogiri'

# retrieve a page
starting_url = 'http://www.moniker.com/domainname.jsp'
form_action = 'http://www.moniker.com/pub/DomainCmd'
html = Net::HTTP.get(URI.parse starting_url)

# use Nokogiri to get all domain checkboxes
params = {}
doc = Nokogiri::HTML(html)
doc.css('input').each do |tld|
    params[ tld['id'] ] = true if tld['id'] && tld['id'].match(/^dot[0-9]+$/)
end

# use an absurd domain name so the prices are listed
params['d_name'] = 'dsaflasldkfndjhdjhfmmddsafeefdfa'
# include the hidden values
params['cmd'] = 'check'
params['scope'] = 'single'

# retrieve pricing and availability page
html = Net::HTTP.post_form(URI.parse(form_action), params).body
doc = Nokogiri::HTML(html)

# grab pricing results
values = []
doc.css('table.searchresults tr').each do |tr|
  tld = tr.children.css('input')[2]['value'].sub('DOMAIN_','').downcase
  price = tr.children.css('td')[2].inner_html
  
  price.gsub!(/[$.]/,'')
  
  values << [tld, price]
end
puts values.join(",") 

