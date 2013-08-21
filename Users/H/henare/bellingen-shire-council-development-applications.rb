require 'mechanize'
require 'uri'

agent = Mechanize.new

# All applications in the last month
url = 'http://infomaster.bellingen.nsw.gov.au/MasterViewLive/modules/applicationmaster/default.aspx?page=found&1=thismonth&4a=DA,CC,CDC,TA,MD&6=F'
page = agent.get(url)

# Click the Agree button on the form
form = page.forms_with(:name => /frmMasterView|frmMasterPlan|frmApplicationMaster/).first
form.submit(form.button_with(:name => /btnOk|Yes|Button1|Agree/))

# Get the page again
page = agent.get(url)

# Visit each DA page so we can get the details
(page/'//*[@id="ctl03_lblData"]').search("a").each do |a|
  begin
    info_page = agent.get(agent.page.uri + URI.parse(a.attributes['href']))
    details = (info_page/'//*[@id="lblDetails"]')

    council_reference = (info_page/'//*[@id="ctl03_lblHead"]').inner_text.split(' ')[0]
    record = {
      'council_reference' => council_reference,
      'description'       => details.at("td").inner_text.split("\r")[1].strip[13..-1],
      'address'           => (info_page/'//*[@id="lblLand"]').inner_text.strip[0..-4],
      'date_received'     => details.at("td").inner_html.split("<br>")[1].strip[11..-1],
      'info_url'          => info_page.uri.to_s,
      'comment_url'       => URI.escape("mailto:council@bellingen.nsw.gov.au?subject=Development Application Enquiry: #{council_reference}"),
      'date_scraped'      => Date.today.to_s
    }
  rescue Exception => e
    puts "Error getting details for development application #{a.to_s} so skipping"
    next
  end

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end

