require 'openssl'
#disable encryption validation, we're fetching public data anyway
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE
I_KNOW_THAT_OPENSSL_VERIFY_PEER_EQUALS_VERIFY_NONE_IS_WRONG = nil

require 'mechanize'
require 'uri'

agent = Mechanize.new

# All applications submitted in the last month
baseurl = 'https://pdonline.toowoombarc.qld.gov.au/Masterview/Modules/ApplicationMaster/'
comment_url = 'mailto:info@toowoombaRC.qld.gov.au'
url = "https://pdonline.toowoombarc.qld.gov.au/Masterview/Modules/ApplicationMaster/default.aspx?page=found&1=lastmonth&4a=\'488\',\'487\',\'486\',\'495\',\'521\',\'540\',\'496\',\'562\'&6=F"
page = agent.get(url)

# Click the Agree button on the form
form = page.forms.first
form.submit(form.button_with(:name => 'ctl00$cphContent$ctl00$Button1'))

# Get the page again
doc = agent.get(url)
# Use the paging to get all the applications
# http://josephjefferson.wordpress.com/2012/04/19/ruby-mechanize-and-javascript-postback/
def get_pages (page, form, event_target)
  link = page.links_with(:class => 'rgCurrentPage')[0]
  /(ctl00[^']+)/.match(link.href).each do |another_page|
    form.add_field!('__EVENTTARGET', another_page)
    form.add_field!('__EVENTARGUMENT', '')
    yield form.submit
  end
end

def clean_whitespace(a)
  if a != nil 
    a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
  else
    a
  end
end

# Construct urls for each link in the table
def get_da_urls (doc,comment_url)
  doc.search('table tbody tr').each do |tr|
    # Columns in table
    # Show  Number  Submitted  Details
    tds = tr.search('td')
    # Yes, this is "where no records"[sic]
    break if tds[0].inner_text =~ /There where no records/

    h = tds.map{|td| td.inner_html}

    puts h
    info_url = 'https://pdonline.toowoombarc.qld.gov.au/Masterview/Modules/ApplicationMaster/' + tds[0].at('a')['href'].strip
    puts info_url
    descParts = h[3].split('<br>')
    record = {
      'info_url' => info_url,
      'comment_url' => comment_url,
      'council_reference' => clean_whitespace(h[1]),
      'date_received' => Date.strptime(clean_whitespace(h[2]), '%d/%m/%Y').to_s,
      # TODO: Some DAs have multiple addresses, we're just getting the first :(
      'address' => clean_whitespace(descParts[0]),
      'description' => clean_whitespace(descParts[1]),
      'date_scraped' => Date.today.to_s
    }

    if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
   end
  end
end
def scrape_and_follow_next_link(doc,comment_url)
  puts "next page"
  get_da_urls(doc, comment_url)
  nextButton = doc.at('.rgPageNext')
  unless nextButton.nil? || nextButton['onclick'] =~ /return false/
    form = doc.forms.first
    
    # The joy of dealing with ASP.NET
    form['__EVENTTARGET'] = nextButton['name']
    form['__EVENTARGUMENT'] = ''
    # It doesn't seem to work without these stupid values being set.
    # Would be good to figure out where precisely in the javascript these values are coming from.
    form['ctl00%24RadScriptManager1']=
      'ctl00%24cphContent%24ctl00%24ctl00%24cphContent%24ctl00%24Radajaxpanel2Panel%7Cctl00%24cphContent%24ctl00%24ctl00%24RadGrid1%24ctl00%24ctl03%24ctl01%24ctl10'
    form['ctl00_RadScriptManager1_HiddenField']=
      '%3B%3BSystem.Web.Extensions%2C%20Version%3D3.5.0.0%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D31bf3856ad364e35%3Aen-US%3A0d787d5c-3903-4814-ad72-296cea810318%3Aea597d4b%3Ab25378d2%3BTelerik.Web.UI%2C%20Version%3D2009.1.527.35%2C%20Culture%3Dneutral%2C%20PublicKeyToken%3D121fae78165ba3d4%3Aen-US%3A1e3fef00-f492-4ed8-96ce-6371bc241e1c%3A16e4e7cd%3Af7645509%3A24ee1bba%3Ae330518b%3A1e771326%3Ac8618e41%3A4cacbc31%3A8e6f0d33%3Aed16cbdc%3A58366029%3Aaa288e2d'
    doc = form.submit(form.button_with(:name => nextButton['name']))
    scrape_and_follow_next_link(doc,comment_url)
  end
end
# Visit each DA page so we can get the details
# For each page, for each item in the table
# visit the page and get the required information
# reference: span with id containing 'lblApplicationHeader'
# address: div with id 'lblProp', then text of a element
# description: second half of reference content, plus text before <br> in div with  id 'lblDetails', then text of a element
# info_url is the url of the da page
# comment_url is email address
# date received is the text after <br> in div with id 'lblDetails'
# on notice from may not be set
# on notice to is the corresponding cell to 'Decision Making Period' in the table in div with id 'lblTasks'


scrape_and_follow_next_link(doc,comment_url)


