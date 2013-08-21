# scrape vworker for jobs
require 'nokogiri'
url = "http://www.vworker.com/RentACoder/DotNet/misc/BidRequests/ShowBidRequests.aspx?lngBidRequestListType=4&cmSearch=Search&optSortTitle=2&lngSortColumn=-6&optBiddingExpiration=1&txtMaxNumberOfEntriesPerPage=10&blnModeVerbose=True&txtCriteria=extract"

def scrape div
  data = {:description => div.at('td').text.strip, :pubDate => Date.today}
  a = div.at('./preceding-sibling::tr[2]/td[2]//a')
  data[:link], data[:title] = 'http://www.vworker.com' + a[:href], a.text.strip
  ScraperWiki.save_sqlite(unique_keys=[:link], data = data)
end

doc = Nokogiri::HTML(ScraperWiki.scrape(url))
#puts doc
doc.xpath('//tr[@class="NormalRow_Small"]/comment()[. = "description"]/..').each{|row| scrape row}