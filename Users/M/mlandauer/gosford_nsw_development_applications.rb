require 'mechanize'

url = "https://ecouncil.gosford.nsw.gov.au/eservice/advertisedDAs.do?function_id=521&orderBy=suburb&nodeNum=263"

def clean(text)
  text.squeeze(' ').strip
end

agent = Mechanize.new

# Doing this as a workaround because there don't appear to be root certificates for Ruby 1.9 installed on
# Scraperwiki. Doesn't really make any difference because we're not sending anything requiring any kind
# of security back and forth
agent.verify_mode = OpenSSL::SSL::VERIFY_NONE

page = agent.get(url)

suburb = nil

page.at('.bodypanel').children.each do |c|
  case c.name
  when "h4"
    suburb =  clean(c.inner_text) + ", NSW"
  when "table"
    record = {
      'council_reference' => clean(c.search('tr')[3].search('td')[2].inner_text),
      'address' => clean(c.at('td.current-development-applications').inner_text) + ", " + suburb,
      'description' => c.search('td[colspan="2"]')[0].inner_text,
      'info_url' => url,
      'comment_url' => 'mailto:da.submissions@gosford.nsw.gov.au',
      'date_scraped' => Date.today.to_s,
      'on_notice_from' => c.search('tr')[4].search('td')[2].inner_text.split(' ')[0].split('/').reverse.join('-'),
      'on_notice_to' => c.search('tr')[4].search('td')[2].inner_text.split(' ')[-1].split('/').reverse.join('-'),
    }
    if (ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? rescue true)
      ScraperWiki.save_sqlite(['council_reference'], record)
    else
      puts "Skipping already saved record " + record['council_reference']
    end
  when "text", "comment", "script"
    # Do nothing
  else
    raise "Unexpected tag #{c.name} with content #{c}"
  end
end 