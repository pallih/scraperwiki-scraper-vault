require 'nokogiri'

starting_url = 'http://www.guardian.co.uk/world/blog/2011/mar/16/japan-nuclear-crisis-tsunami-aftermath-live'
html = ScraperWiki.scrape(starting_url)

doc = Nokogiri::HTML(html)

doc.xpath("//comment()[starts-with(string(), ' Block')]/following-sibling::p").each do |node| 
  p node.text 
  #puts block.inner_html
    unless node.text =~ /You can read our previous live blog|welcome to the Guardian\'s live coverage/
      record = {'block' => node.text}
      ScraperWiki.save(['block'], record)
    end
end
