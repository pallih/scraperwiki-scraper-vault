require 'rubygems'
require 'mechanize'

def store_results(pg)
  page_links = Array.new
  pg.links.each do |link|
    cls = link.attributes.attributes['class']
    page_links << link if cls && cls.value == 'SearchResultsHeading'
  end
  #page_links.each do |link|
    agent = Mechanize.new
    agent.get('http://pa.mypublicnotices.com/PublicNotice.asp?Page=PublicNotice&AdId=' + page_links[0].href.scan(/ID=AD........D/).to_s[6..12]) do |page|
      ScraperWiki.save_sqlite(unique_keys=["title"], data={"title"=>page.search(".Heading").text, "content"=>page.search(".Notice").text})
    end
  #end
end



agent = Mechanize.new
agent.get('http://pa.mypublicnotices.com/PublicNotice.asp') do |page|
  results_page = page.form_with(:name => 'frmPublicNotice').submit
#  store_results(results_page)
  next_results_page = results_page.link_with(:text => /Next/).click()
puts next_results_page
end
require 'rubygems'
require 'mechanize'

def store_results(pg)
  page_links = Array.new
  pg.links.each do |link|
    cls = link.attributes.attributes['class']
    page_links << link if cls && cls.value == 'SearchResultsHeading'
  end
  #page_links.each do |link|
    agent = Mechanize.new
    agent.get('http://pa.mypublicnotices.com/PublicNotice.asp?Page=PublicNotice&AdId=' + page_links[0].href.scan(/ID=AD........D/).to_s[6..12]) do |page|
      ScraperWiki.save_sqlite(unique_keys=["title"], data={"title"=>page.search(".Heading").text, "content"=>page.search(".Notice").text})
    end
  #end
end



agent = Mechanize.new
agent.get('http://pa.mypublicnotices.com/PublicNotice.asp') do |page|
  results_page = page.form_with(:name => 'frmPublicNotice').submit
#  store_results(results_page)
  next_results_page = results_page.link_with(:text => /Next/).click()
puts next_results_page
end
