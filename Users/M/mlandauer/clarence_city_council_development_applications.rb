require 'open-uri'
require "pdf-reader"
require 'mechanize'

class PageTextReceiver
  attr_accessor :content

  def initialize
    @content = []
  end

  # Called when page parsing starts
  def begin_page(arg = nil)
    @content << ""
  end

  # record text that is drawn on the page
  def show_text(string, *params)
    @content.last << string
  end

  # there's a few text callbacks, so make sure we process them all
  alias :super_show_text :show_text
  alias :move_to_next_line_and_show_text :show_text
  alias :set_spacing_next_line_show_text :show_text

  # this final text callback takes slightly different arguments
  def show_text_with_positioning(*params)
    params = params.first
    params.each { |str| show_text(str) if str.kind_of?(String)}
  end
end

def scrape_pdf(url)
  begin
    o = open(url)
  rescue Exception
    puts "Couldn't load #{url}"
    return nil
  end
  receiver = PageTextReceiver.new
  reader = PDF::Reader.new
  reader.parse(o, receiver)
  text = receiver.content.join
  puts text
  match = text.match(/(DEVELOPMENT|SUBDIVISION) APPLICATION(.*)APPLICANT:(.*)PROPOSAL:(.*)LOCATION:(.*)ADVERTISING EXPIRY DATE:([^.]*)\./)
  if match.nil? 
    puts "WARNING: Returned text isn't matching regular expression"
    nil
  else
    {
      'council_reference' => match[2],
      'description' => match[4],
      'address' => match[5] + ", TAS",
      'info_url' => url,
      'comment_url' => 'mailto:clarence@ccc.tas.gov.au',
      'on_notice_to' => Date.parse(match[6]).to_s,
      'date_scraped' => Date.today.to_s
    }
  end
end

a = Mechanize.new
#a.get("http://www.ccc.tas.gov.au/site/page.cfm?u=1581") do |page|
#  page.search('.uContentList a').map{|a| a["href"]}.uniq.each do |a|
#    record = scrape_pdf(a)
#    ScraperWiki.save_sqlite(['council_reference'], record) if record
#  end
#end

a.get("http://www.ccc.tas.gov.au/page.aspx?u=1581") do |page|
  page.search('.u6ListItem a').each do |a|
    unless a.at('img')
      url = a['href']
      s = a.inner_text.split('-')
      # Skip over links that we don't know how to handle (e.g. Notice under Historic Cultural Heritage Act 1995)
      if s.count >= 5
        record = {
          'council_reference' => s[0..2].join('-').strip,
          'address' => s[3].strip + ", TAS",
          'description' => s[4..-2].join('-').strip,
          'on_notice_to' => Date.parse(s[-1].split(' ')[-3..-1].join(' ')).to_s,
          'date_scraped' => Date.today.to_s,
          'info_url' => ("http://www.ccc.tas.gov.au/" + url).gsub(" ", "%20"),
          'comment_url' => 'mailto:clarence@ccc.tas.gov.au'
        }
        if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
          ScraperWiki.save_sqlite(['council_reference'], record)
        else
          puts "Skipping already saved record " + record['council_reference']
        end
      end
    end
  end
end
