#<Encoding:UTF-8>
require 'nokogiri'
require 'mechanize'
require 'uri'
require 'net/http'
require 'json'

url = "http://planning.westoxon.gov.uk/MVM/Online/PL/GeneralSearch.aspx"
@agent = Mechanize.new
@agent.user_agent_alias = 'Mac Safari'

page = @agent.get(url)


#setup the tables
if ScraperWiki.table_info(name="swdata") == []
  ScraperWiki.sqliteexecute("create table swdata (`application_number` string, `parish` string, `proposal` text, `submitted` date, `target_date` date, `decision_made` date, `decision` text, `address` string, `status` string, `type` string, `url` string, `lat` string, `lng` string)")
end

def get_page(url, limit=4)
  if limit < 1
    warn "unexpected error reaching #{uri} - #{fail.message} [ original url: #{original_uri} ]"     
    return nil
  else
    begin
      return Net::HTTP.get_response(url)
    rescue Timeout::Error
      sleep(10)
      get_page(url, limit-1)
    end
  end
end

def submit_form(form, limit=4)
  #puts "DEBUG: In submit_form"
  if limit < 1
    raise "unexpected error submitting the form - #fail.message}"
  else
    begin
      #puts "DEBUG: Start @agent.submit"
      return @agent.submit(form, form.buttons.first)

    rescue Timeout::Error
      submit_form(form, limit-1)
    end
  end
end

def process_xml(xml, parish_name)
  doc = Nokogiri::XML(xml)
  applications = doc.xpath("//mvm:M3_DC_LIVE_GENERAL_QUERY_LIST")
  applications.each do |application|
    application_number = application.at_xpath("mvm:APPLICATION_NUMBER").text
    pk = application.at_xpath("mvm:PK").text
    proposal = application.at_xpath("mvm:PROPOSAL").text
    submitted = application.at_xpath("mvm:DATE_RECEIVED")
    if submitted
      submitted = submitted.text[0..9]
    else
      submitted = ""
    end
    target_date = application.at_xpath("mvm:DATE_TARGET")
    if target_date
      target_date = target_date.text[0..9]
    else
      target_date = ""
    end
    decision_date = application.at_xpath("mvm:DATE_DECISION")
    if decision_date
      decision_date = decision_date.text[0..9]
    else
      decision_date = ""
    end
    decision = application.at_xpath("mvm:DECISION_DESCRIPTION")
    if decision
      decision = decision.text
    else
      decision = ""
    end
    address = application.at_xpath("mvm:SITE_ADDRESS").text
    status = application.at_xpath("mvm:STATUS_DESCRIPTION").text
    type = application.at_xpath("mvm:APPLICATION_TYPE_DESCRIPTION").text
    applicant_name = application.at_xpath("mvm:APPLICANT_NAME").text
    application_url = "http://planning.westoxon.gov.uk/MVM/Online/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningTechAppraisalPK.xml&PARAM0=#{pk}&XSLT=/MVM/SiteFiles/Skins/wodc1/xslt/PL/PLTechAppraisalDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/MVM/SiteFiles/Skins/wodc1/Menus/PL.xml&DAURI=PLANNING"
    
    #store the data
    #
    # Check to see if we have a record with the application number first

    data_q2 = ScraperWiki::select("* from swdata WHERE application_number = \"" + application_number + "\"")

    if data_q2.length > 0
      # FOUND A PREVIOUS RECORD THIS MEANS WE MAY ALREADY HAVE LAT LONG
      # IF THE LOOKUP FAILED WE DONT WANT TO OVERWRITE WITH 0
      # 
      #puts "Application " + application_number + " found"

      if data_q2[0]["lat"] == 0
        # mymsg = mymsg + "but no geo, "
        #
        # NO LONG LAT FOUND SO ATTEMPT LOOKUP
        # IE MINUS LONG LAT
        # USING SQL DIRECT
        # Generate a URL for geocoding the Address.
        user_address = URI.escape(address)
        geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=#{user_address}&sensor=false&region=uk"

        # Scrape the JSON, and parse it
        # Some come back with accented chars and this got nasty!
        ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
        valid_string = ic.iconv(ScraperWiki.scrape(geocode_url))
        #json = JSON.parse ScraperWiki.scrape(geocode_url) 
        json = JSON.parse valid_string

        # Store the lat/lng location of the LA.
        if json["status"] == "OK"
          location = json["results"][0]["geometry"]["location"]
          data_lat = location["lat"]
          data_lng = location["lng"]
          mymsg = "#{mymsg} looked up: #{json["status"]} #{data_lat.to_s()} #{data_lng.to_s()}"
        else
          data_lat = "0"
          data_lng = "0"
          mymsg = "#{mymsg} looked up: #{json["status"]}"
        end
        # NOW SAVE THE RESULTS
        record = {'application_number' => application_number, 'parish' => parish_name, 'proposal' => proposal, 'applicant_name' => applicant_name, 'submitted' => submitted, 'target_date' => target_date, 'decision_made' => decision_date, 'decision' => decision, 'address' => address, 'status' => status, 'type' => type, 'url' => application_url, 'lat' => data_lat, 'lng' => data_lng}
        ScraperWiki.save_sqlite(['application_number'], record)
        
      else # if data_q2[0]["lat"] == 0
        # SO WE DO HAVE THE LAT LONG ALREADY IN THE DB
        # SO DO NOT LOOK UP AGAIN AND JUST UPDATE THE DB

        record = {'application_number' => application_number, 'parish' => parish_name, 'proposal' => proposal, 'applicant_name' => applicant_name, 'submitted' => submitted, 'target_date' => target_date, 'decision_made' => decision_date, 'decision' => decision, 'address' => address, 'status' => status, 'type' => type, 'url' => application_url, 'lat' => data_q2[0]["lat"], 'lng' => data_q2[0]["lng"]}
        ScraperWiki.save_sqlite(['application_number'], record)

      end 
    else # if datalength >1 i.e a record - do below i.e. no record
      # ELSE - IE WE ARE CREATING A WHOLE NEW RECORD
      # THIS IS A NEW RECORD SO SQL SAVE OK WHO CARES ABOUT LAT/LONG SO SAVE IT ANYWAY
      mymsg = " #{mymsg} NOT PREVIOUSLY SEEN SO DO FULL SAVE"
      # Generate a URL for geocoding the Address.
      user_address = URI.escape(address)
      geocode_url = "http://maps.googleapis.com/maps/api/geocode/json?address=#{user_address}&sensor=false&region=uk"

      # Scrape the JSON, and parse it
      # Some come back with accented chars and this got nasty!
      ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
      valid_string = ic.iconv(ScraperWiki.scrape(geocode_url))
      #json = JSON.parse ScraperWiki.scrape(geocode_url) 
      json = JSON.parse valid_string
      # Store the lat/lng location of the LA.
      if json["status"] == "OK"
        location = json["results"][0]["geometry"]["location"]
        data_lat = location["lat"]
        data_lng = location["lng"]
        mymsg = "#{mymsg} looked up: #{json["status"]} #{data_lat.to_s()} #{data_lng.to_s()}"
      else
        data_lat = "0"
        data_lng = "0"
        mymsg = "#{mymsg} looked up: #{json["status"]}"
      end
        # NOW SAVE THE RESULTS
      puts "Application " + application_number + " not found"
      record = {'application_number' => application_number, 'parish' => parish_name, 'proposal' => proposal, 'applicant_name' => applicant_name, 'submitted' => submitted, 'target_date' => target_date, 'decision_made' => decision_date, 'decision' => decision, 'address' => address, 'status' => status, 'type' => type, 'url' => application_url, 'lat' => data_lat, 'lng' => data_lng}
        ScraperWiki.save_sqlite(['application_number'], record)

      puts mymsg
      #put the display thingy here so that it only shows if there is a new record.
    end 

  end
end


  search_results = []

  #submit the form to get the results page with XML...
  page.form_with(:name => 'M3Form') do |f|
    puts "Ducklington Manual"
    
    #f["cboParishCode"] = parish[:value]

    f["cboParishCode"] = "L28"

    search_results = submit_form(f)
  end
  
  #..and find the results XML (thanks to peteralm for the tip)
  doc = Nokogiri::HTML(search_results.body)
  form = doc.xpath("//form[@name='Template']")
  action = form.attr("action").to_s
  parts = action.split("&")
  xml_path = ""
  parts.each do |part|
    xml_path = part[7..999] if part[0..5] == "XMLLoc"
  end
  puts 'fetching xml http://planning.westoxon.gov.uk' + xml_path
  response = get_page(URI.parse('http://planning.westoxon.gov.uk' + xml_path))

  process_xml(response.body, "DUCKLINGTON")
#End