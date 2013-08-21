# Moved this scraper from https://github.com/openaustralia/planningalerts-parsers/blob/master/scrapers/bankstown_scraper.rb

require 'open-uri'
require 'nokogiri'

#Bankstown expose an xml file already, but it is not compatable with what planningalerts expects

# date_range can be any of {today,yesterday,thisweek,lastweek,thismonth,lastmonth}
def applications_search(date_range)
  base_url = "http://online.bankstown.nsw.gov.au/Planning/pages/xc.track/SearchApplication.aspx"
  search_url = base_url + "?o=xml&d=#{date_range}&k=LodgementDate&t=#396"
  #o=xml gives xml results rather than html (o=html)
  #d=thismonth gives results with the date in the current month (also valid are today,yesterday,thisweek,lastweek,thismonth,lastmonth)
  #k=LodgementDate searches for development applications based on date submitted, rather than date determined (k=DeterminationDate)
  #t=396 searches for development applications

  feed_data = open(search_url).read
    
  feed = Nokogiri::XML(feed_data)
  fetched_applications = feed.search('Application')
    
  fetched_applications.map do |a|
    record = {
      'council_reference' => a.at('ReferenceNumber').inner_text,
      # There was always a Line1 and Line 2 when I checked. I'm not sure if we should check for a Line3, or also work if there is no Line2.
      'address' => a.at('Address/Line1').inner_text + ", " + a.at('Address/Line2').inner_text.rstrip, 
      'description' => a.at('ApplicationDetails').inner_text,
      # dates look like 2010-12-29T00:00:00+10:00
      'date_received' => a.at('LodgementDate').inner_text.gsub(/T.*$/,""), 
      'info_url' => base_url + "?id=" + a.at('ApplicationId').inner_text,
      # Just use same as info_url
      'comment_url' => base_url + "?id=" + a.at('ApplicationId').inner_text, 
      'date_scraped' => Date.today.to_s
    }
    # I think this node of the XML file is only added after the application is determined. So depending on how oftern the scraper is run and if updates are allowed, this may or may not matter.
    if a.at('Determination/Date')
      record["on_notice_to"] = Date.parse(a.at('Determination/Date').inner_text).to_s
    end
    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end

  end
end
  
applications_search('thismonth')
applications_search('lastmonth')
