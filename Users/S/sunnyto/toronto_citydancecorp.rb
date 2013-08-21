require 'nokogiri'
require 'mechanize'

Mechanize.html_parser=Nokogiri::HTML

brw = Mechanize.new { |b|
b.user_agent_alias = 'Linux Firefox'
b.read_timeout = 1200
}

BASE_URL='http://citydancecorps.com/'
START_URL='adult-dance'
#note they are using this www.healcode.com widgets! - https://www.healcode.com/

pg = brw.get(BASE_URL+START_URL)

#click into each category on right
puts pg.inspect
puts pg.body.inspect


classtypeslist = Nokogiri::HTML(pg.body).xpath("//div[@class='item-page']/table[2]/tbody/tr/td/h2/a")
classtypeslist.each do |type|
  #go to each type link
  #puts type.inspect
  #puts type.attr('href').inspect
  p2 = brw.get(BASE_URL+type.attr('href'))
  #get into each page and look for links and times
  puts p2.title

  #Mechanize::Page::Link.new(type.xpath('@href'), agent, pg).click
end