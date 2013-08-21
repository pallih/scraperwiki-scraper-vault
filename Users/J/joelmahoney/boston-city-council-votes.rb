# work in progress...

require 'open-uri'
require 'nokogiri'
require 'mechanize'

url = 'http://www.cityofboston.gov/cityclerk/rollcall/Default.aspx'
html = Nokogiri::HTML(open(url))
agent = Mechanize.new

number_of_pages = html.at_css('#ctl00_MainContent_lblCurrentPage').inner_html.to_i

(1..number_of_pages).each do |i|
  pagination_form = agent.get(url).form_with(:name => 'aspnetForm')
  pagination_form.send('ctl00$MainContent$lblCurrentText='.to_sym, i)
pagination_form.submit
  agent.page.search('#ContainerPanel').each do |docket|
    title = docket.at_css('HeaderContent').inner_html.gsub(/\D/, '')
  end
end
