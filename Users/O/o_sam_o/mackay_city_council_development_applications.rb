require 'nokogiri'
require 'open-uri'
require 'date'

def clean_whitespace(a)
  a.gsub(/[\r\n\t]/, ' ').squeeze(" ").strip
end

base_url = 'http://planning.mackay.qld.gov.au/masterview/Modules/Applicationmaster/'
url = "#{base_url}default.aspx?page=found&1=thisweek" # add &6=T to see determined
doc = Nokogiri::HTML(open(url))
das = doc.xpath("//a[contains(@href,'&key=')]").collect do |approval_anchor|
  approval_link = "#{base_url}#{approval_anchor['href']}"
  approval_page = Nokogiri::HTML(open(approval_link))
  page_info = {}
  page_info['council_reference'] = $1 if clean_whitespace(approval_page.at_css('.ControlHeader').inner_text) =~ /([A-Z]+ - \d+ - \d+)/
  page_info['info_url'] = approval_link
  page_info['description'] = $1 if approval_page.at_css('#lblDetails').inner_text.strip =~ /Description: (.+)Submitted:/
  page_info['date_received'] = Date.strptime($1.strip, '%d/%m/%Y').to_s if approval_page.at_css('#lblDetails').inner_text.strip =~ /Submitted: (.+)/
  page_info['address'] = clean_whitespace(approval_page.at_css('#lblProp').inner_text)
  page_info['date_scraped'] = Date.today.to_s
  # Lazily set a generic email as PlanningAlerts is just going to enable commenting
  #page_info['comment_url'] = approval_page.at_css('.ControlContent').at_xpath("//a[contains(@href, 'mailto:')]")['href']
  page_info['comment_url'] = "mailto:development.services@mackay.qld.gov.au"
  
  page_info
end

das.each do |record|
   if record['address'] == 'No properties recorded against this application.'
      p "Skipping #{record['council_reference']} as no address"
      next
   end

   if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
     ScraperWiki.save_sqlite(['council_reference'], record)
   else
     puts "Skipping already saved record " + record['council_reference']
   end
end
