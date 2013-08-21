require 'pp'
require 'nokogiri'           

base = "http://www.usnews.com/education/worlds-best-universities-rankings/top-400-universities-in-the-world?page="

(1..2).each do |i|
  url = "#{base}#{i}"

  html = ScraperWiki.scrape(url)

  headers = [ 'ranking', 'school', 'score', 'peer-review-score',
             'emp-review-score', 'student-faculty-score', 
             'intl-faculty-score', 'intl-student-score', 
             'citations-score']

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

