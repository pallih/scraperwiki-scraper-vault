# This scraper is a replacement for https://scraperwiki.com/scrapers/rockdale_applications/
# The council da tracker doesn't output rss correctly anymore. So, instead scraping the xml output

require 'mechanize'

url = "http://rccweb.rockdale.nsw.gov.au/EPlanning/Pages/XC.Track/SearchApplication.aspx?d=last14days&k=LodgementDate&t=217&o=xml"

agent = Mechanize.new
page = agent.get(url)
# Explicitly interpret as XML
page = Nokogiri::XML(page.content)

page.search('Application').each do |application|
  application_id = application.at("ApplicationId").inner_text
  info_url = "http://rccweb.rockdale.nsw.gov.au/EPlanning/Pages/XC.Track/SearchApplication.aspx?id=#{application_id}"
  record = {
    "council_reference" => application.at("ReferenceNumber").inner_text,
    "description" => application.at("ApplicationDetails").inner_text,
    "date_received" => Date.parse(application.at("LodgementDate").inner_text).to_s,
    # TODO: There can be multiple addresses per application
    "address" =>
      application.at("Address Line1").inner_text + ", " +
      application.at("Address Line2").inner_text,
    "date_scraped" => Date.today.to_s,
    "info_url" => info_url,
    # Can't find a specific url for commenting on applications.
    "comment_url" => info_url,
  }
  # DA03NY1 appears to be the event code for putting this application on exhibition
  e = application.search("Event EventCode").find{|e| e.inner_text.strip == "DA03NY1"}
  if e
    record["on_notice_from"] = Date.parse(e.parent.at("LodgementDate").inner_text).to_s
    record["on_notice_to"] = Date.parse(e.parent.at("DateDue").inner_text).to_s
  end
  
  if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end
