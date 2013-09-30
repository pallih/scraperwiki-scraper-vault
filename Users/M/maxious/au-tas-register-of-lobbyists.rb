require 'open-uri'
require 'yaml'
class Array
  def to_yaml_style
    :inline
  end
end

html = ScraperWiki.scrape("http://lobbyists.dpac.tas.gov.au/lobbyist_profiles")

# Next we use Nokogiri to extract the values from the HTML source.

require 'nokogiri'
page = Nokogiri::HTML(html)
baseurl = "http://lobbyists.dpac.tas.gov.au/lobbyist_profiles"
urls = page.search(".//table[@id = 'lobbyistsTable']//a").map {|a| a.attributes['href']}

# resume from the last incomplete url if the scraper was terminated
resumeFromHere = false
last_url = ScraperWiki.get_var("last_url", "")
if last_url == "" then resumeFromHere = true end

lobbyists = urls.map do |url|
puts resumeFromHere
  if url == last_url then resumeFromHere = true end
  if resumeFromHere
  ScraperWiki.save_var("last_url", url)
  url = "#{url}"
 
  puts "Downloading #{url}" 
begin
  lobbypage = Nokogiri::HTML(ScraperWiki.scrape(url))
  
  #thanks http://ponderer.org/download/xpath/ and http://www.zvon.org/xxl/XPathTutorial/Output/
  lobbyist = {"employees" => [], "clients" => [], "owners" => []}
  
  companyABN=lobbypage.xpath("//tr/td/strong[text() = 'A.B.N:']/ancestor::td/following-sibling::node()/text()")
  businessName=lobbypage.xpath("//tr/td/strong[text() = 'Business entity name:']/ancestor::td/following-sibling::node()/text()")
  tradingName=lobbypage.xpath("//tr/td/strong[text() = 'Trading name:']/ancestor::td/following-sibling::node()/text()")
  lobbyist["business_name"] = businessName.to_s.gsub(/\302\240/, '').strip
  lobbyist["trading_name"] = tradingName.to_s.gsub(/\302\240/, '').strip
  lobbyist["abn"] =  companyABN.to_s.strip.delete(' ').delete('.').to_i
  employeeNames = lobbypage.xpath("//strong[text() = 'Names and positions:'][1]/ancestor::td/following-sibling::node()/text()")
  a = employeeNames[0].to_s.split(';')  
  #lobbyist["employees"] << a.values_at(* a.each_index.select {|i| i.even?})
  lobbyist["employees"] = a.map! {|a| a.strip}
  names = lobbypage.xpath("//strong[text() = 'Name:'][1]/ancestor::td/following-sibling::node()/text()")
  lobbyist["clients"] = names[0].to_s.split(';').map! {|a| a.strip}
  lobbyist["owners"] = names[1].to_s.split(';').map! {|a| a.strip}
  lobbyist["last_updated"] = lobbypage.xpath("//div[@id='TG-footer']/p[3]/text()[2]").to_s.gsub('This page was last modified on','')

  lobbyist["employees"] = lobbyist["employees"].to_yaml
  lobbyist["clients"] = lobbyist["clients"].to_yaml
  lobbyist["owners"] = lobbyist["owners"].to_yaml
  ScraperWiki.save(unique_keys=["business_name","abn"],scraper_data=lobbyist)
     rescue Timeout::Error => e
        print "Timeout on #{url}"
     end
  end
end
ScraperWiki.save_var("last_url", "")require 'open-uri'
require 'yaml'
class Array
  def to_yaml_style
    :inline
  end
end

html = ScraperWiki.scrape("http://lobbyists.dpac.tas.gov.au/lobbyist_profiles")

# Next we use Nokogiri to extract the values from the HTML source.

require 'nokogiri'
page = Nokogiri::HTML(html)
baseurl = "http://lobbyists.dpac.tas.gov.au/lobbyist_profiles"
urls = page.search(".//table[@id = 'lobbyistsTable']//a").map {|a| a.attributes['href']}

# resume from the last incomplete url if the scraper was terminated
resumeFromHere = false
last_url = ScraperWiki.get_var("last_url", "")
if last_url == "" then resumeFromHere = true end

lobbyists = urls.map do |url|
puts resumeFromHere
  if url == last_url then resumeFromHere = true end
  if resumeFromHere
  ScraperWiki.save_var("last_url", url)
  url = "#{url}"
 
  puts "Downloading #{url}" 
begin
  lobbypage = Nokogiri::HTML(ScraperWiki.scrape(url))
  
  #thanks http://ponderer.org/download/xpath/ and http://www.zvon.org/xxl/XPathTutorial/Output/
  lobbyist = {"employees" => [], "clients" => [], "owners" => []}
  
  companyABN=lobbypage.xpath("//tr/td/strong[text() = 'A.B.N:']/ancestor::td/following-sibling::node()/text()")
  businessName=lobbypage.xpath("//tr/td/strong[text() = 'Business entity name:']/ancestor::td/following-sibling::node()/text()")
  tradingName=lobbypage.xpath("//tr/td/strong[text() = 'Trading name:']/ancestor::td/following-sibling::node()/text()")
  lobbyist["business_name"] = businessName.to_s.gsub(/\302\240/, '').strip
  lobbyist["trading_name"] = tradingName.to_s.gsub(/\302\240/, '').strip
  lobbyist["abn"] =  companyABN.to_s.strip.delete(' ').delete('.').to_i
  employeeNames = lobbypage.xpath("//strong[text() = 'Names and positions:'][1]/ancestor::td/following-sibling::node()/text()")
  a = employeeNames[0].to_s.split(';')  
  #lobbyist["employees"] << a.values_at(* a.each_index.select {|i| i.even?})
  lobbyist["employees"] = a.map! {|a| a.strip}
  names = lobbypage.xpath("//strong[text() = 'Name:'][1]/ancestor::td/following-sibling::node()/text()")
  lobbyist["clients"] = names[0].to_s.split(';').map! {|a| a.strip}
  lobbyist["owners"] = names[1].to_s.split(';').map! {|a| a.strip}
  lobbyist["last_updated"] = lobbypage.xpath("//div[@id='TG-footer']/p[3]/text()[2]").to_s.gsub('This page was last modified on','')

  lobbyist["employees"] = lobbyist["employees"].to_yaml
  lobbyist["clients"] = lobbyist["clients"].to_yaml
  lobbyist["owners"] = lobbyist["owners"].to_yaml
  ScraperWiki.save(unique_keys=["business_name","abn"],scraper_data=lobbyist)
     rescue Timeout::Error => e
        print "Timeout on #{url}"
     end
  end
end
ScraperWiki.save_var("last_url", "")