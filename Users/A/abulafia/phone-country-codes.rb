require 'nokogiri'

url      = "http://en.wikipedia.org/wiki/List_of_country_calling_codes"
basepath = ".//*[@id='bodyContent']/div[4]/table[5]/tr"

html = ScraperWiki.scrape(url)
doc = Nokogiri::HTML(html)

unique_keys = ['cc']

doc.xpath(basepath).each do |row|
  cname = row.xpath("./td[1]").text
  codes = row.xpath("./td[2]/a").map {|el| el.text}

  # split multiple codes in a row
  codes = codes.map {|c| c.split(",")}.flatten
  
  codes.each do |code|
    # remove junk
    code.gsub!(/(\W|\+)/,"")

    result = {
      'name' => cname,
      'cc'   => code
    }

   ScraperWiki.save_sqlite(unique_keys, result)
    
  end

end




