require 'yaml'
require 'openssl'
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE
class Array
  def to_yaml_style
    :inline
  end
end
require 'net/https'
require 'uri'

html = ""
uri = URI.parse("https://www.lobbyists.wa.gov.au")
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true if uri.scheme == "https"  # enable SSL/TLS
http.verify_mode = OpenSSL::SSL::VERIFY_NONE
http.start {
  http.request_get("/Pages/WhoIsOnTheRegister.aspx") {|res|
    html = res.body
  }
}

# resume from the last incomplete url if the scraper was terminated
resumeFromHere = false
last_url = ScraperWiki.get_var("last_url", "")
if last_url == "" or last_url.length < 3 then resumeFromHere = true end

# Next we use Nokogiri to extract the values from the HTML source.

require 'nokogiri'
page = Nokogiri::HTML(html)
urls = page.css('#MSOZoneCell_WebPartWPQ3 table').search('a').map {|a| a.attributes['href']}
lobbyists = urls.map do |url|
  if url == last_url and resumeFromHere == false
    resumeFromHere = true
  end

  if resumeFromHere
    ScraperWiki.save_var("last_url", url)
    puts "Downloading #{url}" 
    begin
      lobbyhtml = ""
      http.start {
        http.request_get("/Pages/#{url}") {|res|
          lobbyhtml = res.body
        }
      }
      lobbypage = Nokogiri::HTML(lobbyhtml)
  
      #thanks http://ponderer.org/download/xpath/ and http://www.zvon.org/xxl/XPathTutorial/Output/
      lobbyist = {"employees" => [], "clients" => [], "owners" => []}
  
  
      companyABN=lobbypage.xpath("//tr/td/b[text() = 'A.B.N: ']/ancestor::td/following-sibling::node()/text()")
      companyName=lobbypage.xpath("//b[text() = 'Company Details']/ancestor::table/following-sibling::node()//b[text() = 'Name: ']/ancestor::td/following-sibling::node()/text()").first
      lobbyist["business_name"] = companyName.to_s
      lobbyist["trading_name"] = companyName.to_s
      lobbyist["abn"] =  companyABN.to_s
      lobbypage.xpath("//tr/td/b[text() = 'Client Details']/ancestor::table/following-sibling::node()[1]//td/text()").each do |client|
        clientName = client.content.gsub(/\u00a0/, '').strip
        if clientName.empty? == false and clientName.class != 'binary'
            lobbyist["clients"] << clientName
        end
      end
      lobbypage.xpath("//tr/td/b[text() = 'Owner Details']/ancestor::table/following-sibling::node()[1]//td/text()").each do |owner|
        ownerName = owner.content.gsub(/\u00a0/, '').strip
        if ownerName.empty? == false and ownerName.class != 'binary'
            lobbyist["owners"] << ownerName
        end
      end
      lobbypage.xpath("//tr/td/b[text() = 'Lobbyist Details']/ancestor::table/following-sibling::node()[1]//td/text()").each do |employee|
        employeeName = employee.content.gsub(/\u00a0/, '').gsub("  ", " ").strip
        if employeeName.empty? == false and employeeName.class != 'binary'
            lobbyist["employees"] << employeeName
        end
      end 
      lobbyist["last_updated"] = lobbypage.xpath("//b[text() = 'Details Last Updated: ']/ancestor::td/text()")

      lobbyist["employees"] = lobbyist["employees"].to_yaml
      lobbyist["clients"] = lobbyist["clients"].to_yaml
      lobbyist["owners"] = lobbyist["owners"].to_yaml
      ScraperWiki.save(unique_keys=["business_name","abn"],scraper_data=lobbyist)
    rescue Timeout::Error => e
      print "Timeout on #{url}"
    end
  else
    puts "Skipping #{url}"    
  end
end
ScraperWiki.save_var("last_url", "")