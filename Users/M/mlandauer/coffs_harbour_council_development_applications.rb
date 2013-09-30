# This scraper is a replacement for https://github.com/openaustralia/planningalerts-parsers/blob/master/scrapers/coffs_harbour_scraper.rb

require 'mechanize'

url = "http://datracking.coffsharbour.nsw.gov.au/ICON/Pages/XC.Track/SearchApplication.aspx?d=last14days&o=rss"

agent = Mechanize.new
page = agent.get(url)
puts page.content

# Do the "I agree" dance

p page.forms.count
form = page.forms.first
form.checkbox_with(:name => /Agree/).value = true

button = form.button_with(:value => "I Agree")
p button.node["onclick"]
p form
form["__LASTFOCUS"] = "ctl00$ctMain1$BtnAgree"
form["__EVENTTARGET"] = "ctl00$ctMain1$BtnAgree"
#
#       theForm.__EVENTTARGET.value = eventTarget;
#        theForm.__EVENTARGUMENT.value = eventArgument;
#        theForm.submit();
page = form.submit

puts page.content

exit

# WebForm_DoPostBackWithOptions(
# new WebForm_PostBackOptions(\"ctl00$ctMain1$BtnAgree\", \"\", true, \"\", \"\", false, false)
#)

#function WebForm_PostBackOptions(eventTarget, eventArgument, validation, validationGroup, actionUrl, trackFocus, clientSubmit) {
#    this.eventTarget = eventTarget;
#    this.eventArgument = eventArgument;
#    this.validation = validation;
#    this.validationGroup = validationGroup;
#    this.actionUrl = actionUrl;
#    this.trackFocus = trackFocus;
#    this.clientSubmit = clientSubmit;
#}
#function WebForm_DoPostBackWithOptions(options) {
#    var validationResult = true;
#    if (options.validation) {
#        if (typeof(Page_ClientValidate) == 'function') {
#            validationResult = Page_ClientValidate(options.validationGroup);
#        }
#    }
#    if (validationResult) {
#        if ((typeof(options.actionUrl) != "undefined") && (options.actionUrl != null) && (options.actionUrl.length > 0)) {
#            theForm.action = options.actionUrl;
#        }
#        if (options.trackFocus) {
#            var lastFocus = theForm.elements["__LASTFOCUS"];
#            if ((typeof(lastFocus) != "undefined") && (lastFocus != null)) {
#                if (typeof(document.activeElement) == "undefined") {
#                    lastFocus.value = options.eventTarget;
#                }
#                else {
#                    var active = document.activeElement;
#                    if ((typeof(active) != "undefined") && (active != null)) {
#                        if ((typeof(active.id) != "undefined") && (active.id != null) && (active.id.length > 0)) {
#                            lastFocus.value = active.id;
#                        }
#                        else if (typeof(active.name) != "undefined") {
#                            lastFocus.value = active.name;
#                        }
#                    }
#                }
#            }
#        }
#    }
#    if (options.clientSubmit) {
#        __doPostBack(options.eventTarget, options.eventArgument);
#    }
#}

# Explicitly interpret as XML
page = Nokogiri::XML(page.content)

page.search('Application').each do |application|
  application_id = application.at("ApplicationId").inner_text
  info_url = "http://datracking.coffsharbour.nsw.gov.au/ICON/Pages/XC.Track/SearchApplication.aspx?id=#{application_id}"
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
  p record
  #if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
  #  ScraperWiki.save_sqlite(['council_reference'], record)
  #else
  #  puts "Skipping already saved record " + record['council_reference']
  #end
end
# This scraper is a replacement for https://github.com/openaustralia/planningalerts-parsers/blob/master/scrapers/coffs_harbour_scraper.rb

require 'mechanize'

url = "http://datracking.coffsharbour.nsw.gov.au/ICON/Pages/XC.Track/SearchApplication.aspx?d=last14days&o=rss"

agent = Mechanize.new
page = agent.get(url)
puts page.content

# Do the "I agree" dance

p page.forms.count
form = page.forms.first
form.checkbox_with(:name => /Agree/).value = true

button = form.button_with(:value => "I Agree")
p button.node["onclick"]
p form
form["__LASTFOCUS"] = "ctl00$ctMain1$BtnAgree"
form["__EVENTTARGET"] = "ctl00$ctMain1$BtnAgree"
#
#       theForm.__EVENTTARGET.value = eventTarget;
#        theForm.__EVENTARGUMENT.value = eventArgument;
#        theForm.submit();
page = form.submit

puts page.content

exit

# WebForm_DoPostBackWithOptions(
# new WebForm_PostBackOptions(\"ctl00$ctMain1$BtnAgree\", \"\", true, \"\", \"\", false, false)
#)

#function WebForm_PostBackOptions(eventTarget, eventArgument, validation, validationGroup, actionUrl, trackFocus, clientSubmit) {
#    this.eventTarget = eventTarget;
#    this.eventArgument = eventArgument;
#    this.validation = validation;
#    this.validationGroup = validationGroup;
#    this.actionUrl = actionUrl;
#    this.trackFocus = trackFocus;
#    this.clientSubmit = clientSubmit;
#}
#function WebForm_DoPostBackWithOptions(options) {
#    var validationResult = true;
#    if (options.validation) {
#        if (typeof(Page_ClientValidate) == 'function') {
#            validationResult = Page_ClientValidate(options.validationGroup);
#        }
#    }
#    if (validationResult) {
#        if ((typeof(options.actionUrl) != "undefined") && (options.actionUrl != null) && (options.actionUrl.length > 0)) {
#            theForm.action = options.actionUrl;
#        }
#        if (options.trackFocus) {
#            var lastFocus = theForm.elements["__LASTFOCUS"];
#            if ((typeof(lastFocus) != "undefined") && (lastFocus != null)) {
#                if (typeof(document.activeElement) == "undefined") {
#                    lastFocus.value = options.eventTarget;
#                }
#                else {
#                    var active = document.activeElement;
#                    if ((typeof(active) != "undefined") && (active != null)) {
#                        if ((typeof(active.id) != "undefined") && (active.id != null) && (active.id.length > 0)) {
#                            lastFocus.value = active.id;
#                        }
#                        else if (typeof(active.name) != "undefined") {
#                            lastFocus.value = active.name;
#                        }
#                    }
#                }
#            }
#        }
#    }
#    if (options.clientSubmit) {
#        __doPostBack(options.eventTarget, options.eventArgument);
#    }
#}

# Explicitly interpret as XML
page = Nokogiri::XML(page.content)

page.search('Application').each do |application|
  application_id = application.at("ApplicationId").inner_text
  info_url = "http://datracking.coffsharbour.nsw.gov.au/ICON/Pages/XC.Track/SearchApplication.aspx?id=#{application_id}"
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
  p record
  #if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
  #  ScraperWiki.save_sqlite(['council_reference'], record)
  #else
  #  puts "Skipping already saved record " + record['council_reference']
  #end
end
