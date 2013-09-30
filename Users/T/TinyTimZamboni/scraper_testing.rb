# Blank Ruby
# Blank Ruby
require 'rubygems'
require 'mechanize'

agent = Mechanize.new
agent.get('http://pa.mypublicnotices.com/PublicNotice.asp') do |page|
  results_page = page.form_with(:name => 'frmPublicNotice').submit
     page_links = Array.new
     results_page.links.each do |link|
       cls = link.attributes.attributes['class']
       page_links << link if cls && cls.value == 'SearchResultsHeading'
     end
  #  page_links.each do |link|
       agent.get('http://pa.mypublicnotices.com/PublicNotice.asp?Page=PublicNotice&AdId=' +     page_links[0].href.scan(/ID=AD........D/).to_s[6..12]) do |page|
         ScraperWiki.save_sqlite(unique_keys=["title"], data={"title"=>page.search(".Heading").text, "content"=>page.search(".Notice").text})
       end
  #  end
#     results_page = results_page.link_with(:href =>/JumpToResultsPage/).click 
end
# Blank Ruby
# Blank Ruby
require 'rubygems'
require 'mechanize'

agent = Mechanize.new
agent.get('http://pa.mypublicnotices.com/PublicNotice.asp') do |page|
  results_page = page.form_with(:name => 'frmPublicNotice').submit
     page_links = Array.new
     results_page.links.each do |link|
       cls = link.attributes.attributes['class']
       page_links << link if cls && cls.value == 'SearchResultsHeading'
     end
  #  page_links.each do |link|
       agent.get('http://pa.mypublicnotices.com/PublicNotice.asp?Page=PublicNotice&AdId=' +     page_links[0].href.scan(/ID=AD........D/).to_s[6..12]) do |page|
         ScraperWiki.save_sqlite(unique_keys=["title"], data={"title"=>page.search(".Heading").text, "content"=>page.search(".Notice").text})
       end
  #  end
#     results_page = results_page.link_with(:href =>/JumpToResultsPage/).click 
end
