require 'nokogiri'
require 'mechanize'
require 'uri'
require 'net/http'

url = "http://planning.westoxon.gov.uk/MVM/Online/PL/GeneralSearch.aspx"
@agent = Mechanize.new
page = @agent.get(url)
@first_run = false


#setup the tables
if ScraperWiki.table_info(name="swdata") == []
  @first_run = true
  ScraperWiki.sqliteexecute("create table swdata (`application_number` string, `parish` string, `proposal` text, `submitted` date, `target_date` date, `decision_made` date, `decision` text, `address` string, `status` string, `type` string, `url` string)")
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
  if limit < 1
    raise "unexpected error submitting the form - #fail.message}"
  else
    begin
      return @agent.submit(form, form.buttons.first)
    rescue Timeout::Error
      sleep(10)
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

    application_url = "http://planning.westoxon.gov.uk/MVM/Online/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningTechAppraisalPK.xml&PARAM0=#{pk}&XSLT=/MVM/SiteFiles/Skins/wodc1/xslt/PL/PLTechAppraisalDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/MVM/SiteFiles/Skins/wodc1/Menus/PL.xml&DAURI=PLANNING"
    
    #store the data
    record = {'application_number' => application_number, 'parish' => parish_name, 'proposal' => proposal, 'submitted' => submitted, 'target_date' => target_date, 'decision_made' => decision_date, 'decision' => decision, 'address' => address, 'status' => status, 'type' => type, 'url' => application_url}
    ScraperWiki.save_sqlite(['application_number'], record)
  end
end

parishes = []

#collect all the parish names and codes
page.form_with(:name => 'M3Form') do |f|
  f.field_with(:name => "cboParishCode") do |field|
    field.options.each do |opt|
      unless opt.text == "< all >"
        parishes << {:text => opt.text, :value => opt.value}
      end
    end
  end
end

#loop through all the parishes we found earlier
parishes.each do |parish|
  search_results = ""

  #submit the form...
  page.form_with(:name => 'M3Form') do |f|
    puts parish[:text]
    f["cboParishCode"] = parish[:value]

    # PA - I had hoped the next two lines would limit the results to 1 month
    # now that we have a database going back to 2003, do we need to re-scrape
    # it all every night? Can we not insert/update the last 6 months?
    #
    # LC - Good point, limiting it to the last 14 days unless it's the first run
    unless @first_run 
      f.radiobutton_with(:id => "_ctl4").check
      f["_ctl2"] = "14" #last 2 weeks
    end
    search_results = submit_form(f)
  end
  
  #..and find the results XML (thanks to peteralm for the tip) [LC]
  doc = Nokogiri::HTML(search_results.body)
  form = doc.xpath("//form[@name='Template']")
  action = form.attr("action").to_s
  parts = action.split("&")
  xml_path = ""
  parts.each do |part|
    xml_path = part[7..999] if part[0..5] == "XMLLoc"
  end
  puts 'fetching http://planning.westoxon.gov.uk' + xml_path
  response = get_page(URI.parse('http://planning.westoxon.gov.uk' + xml_path.gsub(" ", "%20")))

  process_xml(response.body, parish[:text])
end