require 'mechanize'

def scrape_icon_rest_xml(base_url, query, debug = false)
  agent = Mechanize.new
  page = agent.get("#{base_url}?#{query}")
  # Explicitly interpret as XML
  page = Nokogiri::XML(page.content)

  page.search('Application').each do |application|
    application_id = application.at("ApplicationId").inner_text
    info_url = "#{base_url}?id=#{application_id}"
    record = {
      "council_reference" => application.at("ReferenceNumber").inner_text,
      "description" => application.at("ApplicationDetails").inner_text,
      "date_received" => Date.parse(application.at("LodgementDate").inner_text).to_s,
      # TODO: There can be multiple addresses per application
      # We can't just create a new application for each address as we would then have multiple applications
      # with the same council_reference which isn't currently allowed.
      "address" =>
        application.at("Address Line1").inner_text + ", " +
        application.at("Address Line2").inner_text,
      "date_scraped" => Date.today.to_s,
      "info_url" => info_url,
      # Can't find a specific url for commenting on applications.
      "comment_url" => info_url,
    }
    # DA03NY1 appears to be the event code for putting this application on exhibition
    # Commenting this out because I don't know whether this can be applied generally to all
    # councils. It seems likely that the event codes are different in each council
    #e = application.search("Event EventCode").find{|e| e.inner_text.strip == "DA03NY1"}
    #if e
    #  record["on_notice_from"] = Date.parse(e.parent.at("LodgementDate").inner_text).to_s
    #  record["on_notice_to"] = Date.parse(e.parent.at("DateDue").inner_text).to_s
    #end
  
    if debug
      p record
    else
      if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
        ScraperWiki.save_sqlite(['council_reference'], record)
      else
        puts "Skipping already saved record " + record['council_reference']
      end
    end
  end
end

