# work in progress...

require 'open-uri'
require 'nokogiri'
require 'mechanize'

url = 'http://www.bostonpublicschools.org/view/all-schools-z'
html = Nokogiri::HTML(open(url))
agent = Mechanize.new

html.css('table.views-view-grid td a').each do |link|

end
# work in progress...

require 'open-uri'
require 'nokogiri'
require 'mechanize'

url = 'http://www.bostonpublicschools.org/view/all-schools-z'
html = Nokogiri::HTML(open(url))
agent = Mechanize.new

html.css('table.views-view-grid td a').each do |link|

end
