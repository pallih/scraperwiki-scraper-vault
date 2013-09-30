# Blank Ruby



require 'nokogiri'
require 'net/http'
require 'open-uri'



begin

html = ScraperWiki.scrape('http://protectivestructures.org/memberlist.php')
doc = Nokogiri::HTML(html)


@names = doc.xpath('//p/b').map {|b| b.inner_html}
emails = doc.xpath('//p/a').map {|a| a.inner_html}


@emails = []
emails.each do |e|
if e.include? '@'
  @emails << e
end
end


doc.xpath('//b').each do |e|
e.remove
end

doc.xpath('//a').each do |e|
e.remove
end

content = doc.xpath('//p').map {|content| content} 
#puts content

re = /<("[^"]*"|'[^']*'|[^'">])*>/
content = content.to_s.gsub(/<br><br>/, "\n")
content = content.gsub!(re, '').strip.squeeze

@content = content.split(/\n/)


#Save records

0.upto(@emails.length-1) do |i|
ScraperWiki.save_sqlite(unique_keys=["Email"], data={"Email"=> @emails[i], "Name" => @names[i], "Location" => @content[i]})   
end



rescue Timeout::Error
retry
rescue
retry
end


# Blank Ruby



require 'nokogiri'
require 'net/http'
require 'open-uri'



begin

html = ScraperWiki.scrape('http://protectivestructures.org/memberlist.php')
doc = Nokogiri::HTML(html)


@names = doc.xpath('//p/b').map {|b| b.inner_html}
emails = doc.xpath('//p/a').map {|a| a.inner_html}


@emails = []
emails.each do |e|
if e.include? '@'
  @emails << e
end
end


doc.xpath('//b').each do |e|
e.remove
end

doc.xpath('//a').each do |e|
e.remove
end

content = doc.xpath('//p').map {|content| content} 
#puts content

re = /<("[^"]*"|'[^']*'|[^'">])*>/
content = content.to_s.gsub(/<br><br>/, "\n")
content = content.gsub!(re, '').strip.squeeze

@content = content.split(/\n/)


#Save records

0.upto(@emails.length-1) do |i|
ScraperWiki.save_sqlite(unique_keys=["Email"], data={"Email"=> @emails[i], "Name" => @names[i], "Location" => @content[i]})   
end



rescue Timeout::Error
retry
rescue
retry
end


