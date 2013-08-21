# example code from http://nokogiri.org/

require 'nokogiri'
require 'open-uri'

# Get a Nokogiri::HTML:Document for the page we’re interested in...
doc = Nokogiri::HTML(open('http://nohodrink.com.sg/noho_testimonials.html'))

# Do funky things with it using Nokogiri::XML::Node methods...
####
# Search for nodes by css
doc.xpath('.//p[contains(text(), "facebook")]').each do |link|
    puts link, "\n"


end