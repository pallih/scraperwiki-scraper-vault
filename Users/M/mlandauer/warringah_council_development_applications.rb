#require 'scrapers/icon_rest_xml'

require 'mechanize'

def scrape_icon_rest_xml(base_url, query, debug = false)
  agent = Mechanize.new
  page = agent.get("#{base_url}?#{query}")
  # Explicitly interpret as XML
  page = Nokogiri::XML(page.content)

  page.search('Application').each do |application|
    # If there is no address it's likely to be a newly received application that hasn't been processed yet.
    # So, let's just skip over it.
    if application.at("Address")
      application_id = application.at("ApplicationId").inner_text
      info_url = "#{base_url}?id=#{application_id}"
      record = {
        "council_reference" => application.at("ReferenceNumber").inner_text,
        "description" => application.at("ApplicationDetails").inner_text,
        "date_received" => Date.parse(application.at("LodgementDate").inner_text).to_s,
        "date_scraped" => Date.today.to_s,
        "info_url" => info_url,
        # Can't find a specific url for commenting on applications.
        "comment_url" => info_url,
      }

      # TODO: There can be multiple addresses per application
      # We can't just create a new application for each address as we would then have multiple applications
      # with the same council_reference which isn't currently allowed.

      record["address"] = application.at("Address Line1").inner_text + ", " +
        application.at("Address Line2").inner_text

      if application.at("NotificationStart")
        record["on_notice_from"] = Date.parse(application.at("NotificationStart").inner_text).to_s
      end
      if application.at("NotificationEnd")
        record["on_notice_to"] = Date.parse(application.at("NotificationEnd").inner_text).to_s
      end
  
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
end

scrape_icon_rest_xml("http://www.warringah.nsw.gov.au/ePlanning/Pages/XC.Track/SearchApplication.aspx", "d=thismonth&k=LodgementDate&t=DevApp&o=xml", true)

