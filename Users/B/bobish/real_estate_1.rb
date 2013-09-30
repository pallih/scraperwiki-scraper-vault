require 'nokogiri'
require 'nokogiri' 

for i in 0..14          
  html = ScraperWiki::scrape("http://www.agentuk.com/alpha/A/#{i}/estate_agent.htm")           
  p html
  
  doc = Nokogiri::HTML html
  
  doc.css('td.maincol a').each do |link|           
      if link['href'].include?("town")  
        #puts link.text, "http://www.agentuk.com"+link['href']
        puts i
        
      end
  end
end


require 'nokogiri'
require 'nokogiri' 

for i in 0..14          
  html = ScraperWiki::scrape("http://www.agentuk.com/alpha/A/#{i}/estate_agent.htm")           
  p html
  
  doc = Nokogiri::HTML html
  
  doc.css('td.maincol a').each do |link|           
      if link['href'].include?("town")  
        #puts link.text, "http://www.agentuk.com"+link['href']
        puts i
        
      end
  end
end


