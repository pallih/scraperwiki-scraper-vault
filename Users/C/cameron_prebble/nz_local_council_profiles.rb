require 'nokogiri'

index_html = ScraperWiki.scrape("http://www.localcouncils.govt.nz/lgip.nsf/wpg_URL/Profiles-Index")
index = Nokogiri::HTML(index_html)
index.search("a.no-ul[href^='/lgip.nsf/wpg_URL/Profiles-Councils']").each do |link|
  puts link.inner_text
  if (ScraperWiki.select("name from swdata where name='#{link.inner_text.gsub('\'','\'\'')}'").empty?) 
    data = {}
    data['name'] = link.inner_text
    html = ScraperWiki.scrape("http://www.localcouncils.govt.nz#{link['href']}")
    doc = Nokogiri::HTML(html)
    doc.css("table.data").each do |table|
      table.search("tr").each do |row|
        data[row.search('th').inner_text] = row.search('td').inner_text
      end
    end
    ScraperWiki.save(unique_keys=['name'], data=data)
  end
end
require 'nokogiri'

index_html = ScraperWiki.scrape("http://www.localcouncils.govt.nz/lgip.nsf/wpg_URL/Profiles-Index")
index = Nokogiri::HTML(index_html)
index.search("a.no-ul[href^='/lgip.nsf/wpg_URL/Profiles-Councils']").each do |link|
  puts link.inner_text
  if (ScraperWiki.select("name from swdata where name='#{link.inner_text.gsub('\'','\'\'')}'").empty?) 
    data = {}
    data['name'] = link.inner_text
    html = ScraperWiki.scrape("http://www.localcouncils.govt.nz#{link['href']}")
    doc = Nokogiri::HTML(html)
    doc.css("table.data").each do |table|
      table.search("tr").each do |row|
        data[row.search('th').inner_text] = row.search('td').inner_text
      end
    end
    ScraperWiki.save(unique_keys=['name'], data=data)
  end
end
