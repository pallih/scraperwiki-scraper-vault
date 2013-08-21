html = ScraperWiki.scrape("http://transparency.number10.gov.uk/money.php")

require 'nokogiri'
doc = Nokogiri::HTML(html)
table = doc.search('table')

require 'csv'

total = 0
uk = 0
table.search('tr').take(10).each do |tr|
  csvUrlMatches = tr.inner_html.scan(/"(http.*)\"/)
  csvUrlMatches.each do |url|
    httpUrl = url[0].sub(/https/, "http")

    next if httpUrl =~ /AGO/
    next if httpUrl =~ /BIS/

    puts httpUrl + "\n"

    # get the content of the csv file
    csvContent = ScraperWiki.scrape(httpUrl)

    # turn it into a csv data set
    csvData = CSV.parse(csvContent)
    puts csvData.length
    total += csvData.length
  
    # get the fields used in this file
    headers = csvData[0]
    #headers.each do |col|
    #  p col
    #end

    rows = 0
    csvData.take(5).each do |row|
      rows = rows + 1
      next if rows == 1
      #p row
      r = 0
      hash = {}
      hash['row'] = rows
      row.each do |col|
        txt = col
        if txt == nil
          txt = ""
        end
        key = headers[r]
        if key == nil
          key = "unk"
        end
        hash[key.gsub(/\s/, '_')] = txt
        r = r + 1
      end
      p hash
      puts "\n"
      ScraperWiki.save(['Transaction_Number','Expense_Area', 'row'], hash)
    end
  end
end

#puts total
