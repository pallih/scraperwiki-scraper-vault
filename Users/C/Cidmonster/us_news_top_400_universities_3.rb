require 'pp'
require 'nokogiri'           

base = "http://www.defense.gov/contracts/contract.aspx?contractid="

(4600..4631).each do |i|
  url = "#{base}#{i}"

  html = ScraperWiki.scrape(url)

  headers = ['branch', 'company1', 'contract amount', 'contract type',
             'state', 'company2', 'state2']

  data = []

  doc = Nokogiri::HTML(html)
  for row in doc.search("div#content div.wide table tr")[1..-1]

    hindex = 0
    row_dict = {}
    row.search('td').each do |cell|
      heading = headers[hindex]
      cell_data = cell.content.strip.gsub("\n","")
      row_dict[heading] = cell_data
      hindex += 1
    end
    pp row_dict
    ScraperWiki.save_sqlite(unique_keys=['school'], data=row_dict)           
    puts ""

  end
end

