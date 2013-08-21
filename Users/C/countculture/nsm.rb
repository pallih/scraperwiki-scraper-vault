require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://tools.morningstar.co.uk/tsweu6nqxu/globaldocuments/list/default.aspx'

def parse_filings(page)
  filings = page.search('#ctl00_ContentPlaceHolder1_gvwDocuments tr.gridItem')
  puts "Found #{filings.size} filings"
  if filings.size == 0
    puts page.parser.to_s
  end
  filings_data = filings.collect do |filing|
    res = {}
    date_td = filing.at('.gridDocumentsDate a')
    res[:filed_at] = date_td.inner_text.split('/').reverse.join('-') + ' ' + filing.at('.gridDocumentsTime a').inner_text
    headline = filing.at('.gridDocumentsHeadline a')
    res[:title] = headline.inner_text
    path = headline[:onclick][/open\(\'([^\']*)/,1]
    res[:filing_id] = path[/DocumentId=(\d+)/,1]
    res[:url] = 'http://tools.morningstar.co.uk'+ path
    res[:company_name] = filing.at('.gridDocumentsCompanyName a').inner_text
    res[:filing_type] = filing.at('.gridDocumentsType a').inner_text
    res[:date_scraped] = Time.now
    p res
  end
  ScraperWiki.save_sqlite([:filing_id], filings_data)
end

def get_page(page, page_number=1)
  form = page.form
  form['ctl00$ContentPlaceHolder1$ddlPageSize'] = 100
  form['__EVENTARGUMENT'] = page_number
  form['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$pgrDocumentList'
  form['ctl00$ContentPlaceHolder1$txtDateFrom'] = (Time.now - (3* 24 * 60 * 60)).strftime('%d/%m/%Y')
  form['ctl00$ContentPlaceHolder1$txtDateTo'] = Time.now.strftime('%d/%m/%Y')
  result = form.submit
end

@browser = Mechanize.new { |browser|
  browser.user_agent_alias = 'Linux Firefox'
}
# get first page to pick up cookies etc
page = @browser.get(BASE_URL)
page_number = 1

loop do 
  page = get_page(page, page_number)
  parse_filings(page)
  break if page.at('a.disabled[text()*="Next"]')
  page_number += 1
end


