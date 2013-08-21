require 'mechanize'
require 'date'

base_url   = "https://epathway.yarraranges.vic.gov.au/ePathway/Production/Web"
main_url   = "#{base_url}/GeneralEnquiry"
splash_url = "#{base_url}/default.aspx"

agent = Mechanize.new do |a|
  a.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

p "Setting up session by visiting splash page..."
splash_page = agent.get( splash_url )
p "Splash page: '#{splash_page.title.strip}'"

p "Loading search form so that we can submit it..."
first_page = agent.get( "#{main_url}/EnquiryLists.aspx" )
p "Search page: '#{first_page.title.strip}'"

search_form = first_page.forms.first

p "Submitting search form."
p "The form will result in all applications since the beginning of time, however, they should be sorted in reverse chronological order. This means we can scrape indefinetaly until we hit one we've seen before."

summary_page = agent.submit( search_form, search_form.buttons.first )
p "Summary page: '#{summary_page.title.strip}'"

data     = []
continue = true
page_num = 1

now             = Date.today.to_s
comment_address = 'mail@yarraranges.vic.gov.au&subject=Application ' # will be suffixed with the application number

# Only figure out the header stuff the first time...
headers               = nil
idx_council_reference = nil
idx_description       = nil
idx_date_received     = nil
idx_address           = nil

table_exists = ScraperWiki.show_tables().length > 0

while continue and summary_page
  p "Processing: Page #{page_num}..."
  
  table = summary_page.root.at_css('table.ContentPanel')

  unless headers
    headers = table.css('th').collect { |th| th.inner_text.strip } 
    idx_council_reference = headers.index( 'Number'      )
    idx_description       = headers.index( 'Description' )
    idx_date_received     = headers.index( 'Lodged'      )
    idx_address           = headers.index( 'Location'    )
  end

  data = table.css('.ContentPanel, .AlternateContentPanel').collect do |tr| 
    tr.css('td').collect { |td| td.inner_text.strip }
  end

  to_ignore = []

  applications = data.each do |application|

    # p application

    info = {}
    info['council_reference'] = application[ idx_council_reference ]
    info['address']           = application[ idx_address           ]
    info['description']       = application[ idx_description       ]
    info['info_url']          = splash_url # There is a direct link but you need a session to access it :(
    info['date_received']     = Date.strptime( application[ idx_date_received ], '%d/%m/%Y' ).to_s
    info['date_scraped']      = now
    info['comment_url']       = comment_address + application[ idx_council_reference ]
    
    # p info

    if !table_exists || ScraperWiki.select( "* from swdata where `council_reference` = '#{info['council_reference']}'" ).empty? 
      ScraperWiki.save_sqlite( ['council_reference'], info )
    else
      to_ignore = to_ignore + [ info['council_reference'] ]
    end

  end

  if to_ignore.length > 0 
    p "Found #{to_ignore.length} items we have already seen:"
    pp to_ignore
    p "Not continuing any further."
    continue = false
  end

  if continue
    page_num = page_num + 1
    summary_page = agent.get( "#{main_url}/EnquirySummaryView.aspx", { :PageNumber => page_num } )
  end
end

p "Finished."
