require 'open-uri'
require 'yaml'
class Array
  def to_yaml_style
    :inline
  end
end

html = ScraperWiki.scrape("http://lobbyists.integrity.qld.gov.au/register-details/list-companies.aspx")

# Next we use Nokogiri to extract the values from the HTML source.

require 'nokogiri'
page = Nokogiri::HTML(html)

baseurl = "http://lobbyists.integrity.qld.gov.au/register-details/"
urls = page.search('.demo li a').map {|a| a.attributes['href']}

# resume from the last incomplete url if the scraper was terminated
resumeFromHere = false
last_url = ScraperWiki.get_var("last_url", "")
if last_url == "" then resumeFromHere = true end

lobbyists = urls.map do |url|
  url = "#{baseurl}/#{url}"

  if url == last_url then resumeFromHere = true end
  if resumeFromHere
  ScraperWiki.save_var("last_url", url) 

  puts "Downloading #{url}"
begin
  lobbypage = Nokogiri::HTML(ScraperWiki.scrape(url))
  
  #thanks http://ponderer.org/download/xpath/ and http://www.zvon.org/xxl/XPathTutorial/Output/
  lobbyist = {"employees" => [], "clients" => [], "owners" => []}
  
  companyABN=lobbypage.xpath("//tr/td/strong[text() = 'A B N:']/ancestor::td/following-sibling::node()/span/text()")
  companyName=lobbypage.xpath("//strong[text() = 'BUSINESS ENTITY NAME:']/ancestor::td/following-sibling::node()[2]/span/text()").first
  tradingName=lobbypage.xpath("//strong[text() = 'TRADING NAME:']/ancestor::td/following-sibling::node()[2]/span/text()").first
  lobbyist["business_name"] = companyName.to_s
  lobbyist["trading_name"] = tradingName.to_s
  lobbyist["abn"] =  companyABN.to_s.gsub(" ","")
  lobbypage.xpath("//strong[text() = 'CURRENT THIRD PARTY CLIENT DETAILS:']/ancestor::p/following-sibling::node()[4]//tr/td[1]/text()").each do |client|
    clientName = client.content.strip
    if clientName.empty? == false and clientName.class != 'binary'
      lobbyist["clients"] << clientName
    end
  end
  lobbypage.xpath("//strong[text() = 'PREVIOUS THIRD PARTY CLIENT DETAILS:']/ancestor::p/following-sibling::node()[4]//td/text()").each do |client|
    clientName = client.content.strip
    if clientName.empty? == false and clientName.class != 'binary'
      lobbyist["clients"] << clientName
    end
  end
  lobbypage.xpath("//strong[text() = 'OWNER DETAILS']/ancestor::p/following-sibling::node()[4]//td").each do |owner|
    ownerName = owner.content.strip
    if ownerName.empty? == false and ownerName.class != 'binary'
      lobbyist["owners"] << ownerName
    end
  end
  lobbypage.xpath("//strong[text() = 'DETAILS OF ALL PERSONS OR EMPLOYEES WHO CONDUCT LOBBYING ACTIVITIES:']/ancestor::p/following-sibling::node()[4]//tr//td[1]/text()").each do |employee|
    employeeName = employee.content.gsub("  ", " ").strip
    if employeeName.empty? == false and employeeName.class != 'binary'
      lobbyist["employees"] << employeeName
    end
  end

  lobbyist["employees"] = lobbyist["employees"].to_yaml
  lobbyist["clients"] = lobbyist["clients"].to_yaml
  lobbyist["owners"] = lobbyist["owners"].to_yaml
  ScraperWiki.save(["business_name","abn"],lobbyist)
     rescue Timeout::Error => e
        print "Timeout on #{url}"
     end
  end
end
ScraperWiki.save_var("last_url", "")