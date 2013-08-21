# Blank Ruby
require 'nokogiri'

url = "http://www.superherodb.com/characters"
html = ScraperWiki::scrape(url)         
doc = Nokogiri::HTML(html)

scrapped_heroes = ScraperWiki::get_var("scraped_heroes") || []

doc.search("div.contentCol3 li a").each do |v|
  
  data = { :name => v.text() }
  #scrapped_heroes.index(data[:name]) == nil && 
  if (data[:name] == "Batman")
    suburl = url + v.attr("href")
    subhtml = ScraperWiki::scrape(suburl)
    subdoc = Nokogiri::HTML(subhtml)

     p subdoc.search("h3")
    subdoc.search("div.contentColRight div.tableRow").each do |v|
     
      attr = v.search("div.tableCaptionGrid").text().strip().gsub("\"","").gsub(" ","_")
      value = v.search("div.tableData div.gridBar").attr("style").value()
      match = /width: (.+)px/.match(value)

      
      if (match.length)
        value = match[1].to_f / 160.0
      end
    
      if (attr.length > 0)
        data[attr.to_sym] = ("%.2f" % value).to_f
      end
    end

    subdoc.search("div.contentColLeft div.tableRow").each do |v|
      attr = v.search("div.tableCaption").text().strip().gsub("\"","").gsub(" ","_")
      value = v.search("div.tableData").text().strip().gsub("\"","")
      if (attr.length > 0)
        data[attr.to_sym] = value
      end
    end
    
    

    scrapped_heroes << data[:name]
    ScraperWiki::save_var("scraped_heroes", scrapped_heroes)
    ScraperWiki::save_sqlite(['name'], data)
  end
end

  