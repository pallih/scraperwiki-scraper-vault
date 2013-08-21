require 'mechanize'

def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def get_address(agent, info_url)
  page = agent.get(info_url)
  table = page.search('.application-details table').first
  tr_properties = table.search('tr').find{|t| t.inner_text.strip == "Properties"}
  # Only record the first address if there are several
  a = tr_properties.next_sibling.at('a')
  # It's possible that there are no addresses recorded against an application which makes
  # it pretty much useless. Ah well...
  clean_whitespace(a.inner_text) if a
end

def extract_page_content(agent, page)
  # They have an online submissions system.
  comment_url = "http://apps.thehills.nsw.gov.au/external/ERequest.aspx"

  page.at('table.rgMasterTable').search('tr.rgRow').each do |tr|
    record = {
      'info_url' => (page.uri + tr.at('a')['href']).to_s,
      'council_reference' => tr.search('td')[1].inner_text.strip,
      'date_received' => Date.strptime(tr.search('td')[2].inner_text.strip, '%d/%m/%Y').to_s,
      'description' => tr.search('td')[3].inner_text.strip,
      'date_scraped' => Date.today.to_s,
      'comment_url' => comment_url,
    }

    if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
      # The address is only shown on the application detail page. Only get it if this is a new record
      record['address'] = get_address(agent, record['info_url'])
      # Only save the record if there is actually an address
      ScraperWiki.save_sqlite(['council_reference'], record) if record['address']
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  end
end

# This is the javascript in the page:
#
# var theForm = document.forms['aspnetForm'];
# if (!theForm) {
#     theForm = document.aspnetForm;
# }
# function __doPostBack(eventTarget, eventArgument) {
#     if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
#         theForm.__EVENTTARGET.value = eventTarget;
#         theForm.__EVENTARGUMENT.value = eventArgument;
#         theForm.submit();
#     }
# }

# Simulate javascript asp.net postback
def doPostBack(page, button)
  unless button["onclick"] =~ /return false/
    m = button["onclick"].match(/javascript:__doPostBack\('(.*)','(.*)'\)/)
    eventTarget = m[1]
    eventArgument = m[2]
    form = page.form_with(:name => "aspnetForm")
    form["__EVENTTARGET"] = eventTarget
    form["__EVENTARGUMENT"] = eventArgument
    form.submit
  end
end

def do_search(range)
  agent = Mechanize.new

  url = "http://apps.thehills.nsw.gov.au/DATracking/Modules/ApplicationMaster/default.aspx?page=found&1=#{range}"

  page = agent.get(url)
  form = page.forms.first
  page = form.submit(form.button_with(:value => "I Agree"))

  begin
    extract_page_content(agent, page)
    # Click the next button
    next_button = page.at('.rgPageNext')
    page = doPostBack(page, next_button)
  end until page.nil? 
end


do_search("thismonth")
do_search("lastmonth")
