require 'nokogiri'
require 'date'

base_url = 'http://www.geelongaustralia.com.au/residents/planning/'
applications_url = base_url + 'advertising.aspx'
html = ScraperWiki.scrape applications_url
page = Nokogiri.parse html
table = page.at 'table#ctl00_MainContentPlaceHolder_GridView1'

table.search('tr.table_body').each do |r|
  application_url = base_url + r.at('a').attr('href')

  # Cargo culting: http://po-ru.com/diary/fixing-invalid-utf-8-in-ruby-revisited/
  ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  valid_string = ic.iconv(ScraperWiki.scrape(application_url))

  # TODO: We don't need to scrape the detail page if we've already saved this DA
  description = Nokogiri.parse(valid_string).at('#ctl00_MainContentPlaceHolder_FormView2_Label2').inner_text

  # Some dates are empty
  on_notice_from_text = r.search('td')[3].inner_text
  on_notice_from = on_notice_from_text.gsub("\u00A0",'').empty? ? nil : Date.parse(r.search('td')[3].inner_text)

  record = {
    :council_reference => r.search('td')[0].inner_text,
    :address => "#{r.search('td')[1].inner_text.strip}, #{r.search('td')[2].inner_text.strip}",
    :on_notice_from => on_notice_from,
    :on_notice_to => Date.parse(r.search('td')[4].inner_text),
    :info_url => application_url,
    :comment_url => application_url,
    :description => description,
    :date_scraped => Date.today
  }

  if (ScraperWiki.select("* from swdata where `council_reference`='#{record[:council_reference]}'").empty? rescue true)
    ScraperWiki.save_sqlite([:council_reference], record)
  else
    puts "Skipping already saved record " + record[:council_reference]
  end
end
