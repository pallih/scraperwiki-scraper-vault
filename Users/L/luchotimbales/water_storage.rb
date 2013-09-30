# Blank Ruby

html = ScraperWiki.scrape("http://www.melbournewater.com.au/content/water_storages/water_report/weekly_water_report_archives.asp?year=2001&file=wrr011221.html")
puts html

require 'nokogiri'

doc = Nokogiri::HTML(html, nil, 'utf-8')
counter=0



  puts "hi"
  doc.search('table >tr').each do |row|
  if counter < 3 then
      counter=counter+1
      puts row
      puts row.css('td')[0].text
      puts row.css('td')[3].text

      if not counter=0 then  
        record={}
        record ['ID']= "year0001"+ counter.to_s()
        record ['Reservoir']=row.css('td')[0].text
        record ['Percentage']=row.css('td')[3].text
        ScraperWiki.save_sqlite(["ID"], record)
      end
  end  
end
# Blank Ruby

html = ScraperWiki.scrape("http://www.melbournewater.com.au/content/water_storages/water_report/weekly_water_report_archives.asp?year=2001&file=wrr011221.html")
puts html

require 'nokogiri'

doc = Nokogiri::HTML(html, nil, 'utf-8')
counter=0



  puts "hi"
  doc.search('table >tr').each do |row|
  if counter < 3 then
      counter=counter+1
      puts row
      puts row.css('td')[0].text
      puts row.css('td')[3].text

      if not counter=0 then  
        record={}
        record ['ID']= "year0001"+ counter.to_s()
        record ['Reservoir']=row.css('td')[0].text
        record ['Percentage']=row.css('td')[3].text
        ScraperWiki.save_sqlite(["ID"], record)
      end
  end  
end
# Blank Ruby

html = ScraperWiki.scrape("http://www.melbournewater.com.au/content/water_storages/water_report/weekly_water_report_archives.asp?year=2001&file=wrr011221.html")
puts html

require 'nokogiri'

doc = Nokogiri::HTML(html, nil, 'utf-8')
counter=0



  puts "hi"
  doc.search('table >tr').each do |row|
  if counter < 3 then
      counter=counter+1
      puts row
      puts row.css('td')[0].text
      puts row.css('td')[3].text

      if not counter=0 then  
        record={}
        record ['ID']= "year0001"+ counter.to_s()
        record ['Reservoir']=row.css('td')[0].text
        record ['Percentage']=row.css('td')[3].text
        ScraperWiki.save_sqlite(["ID"], record)
      end
  end  
end
# Blank Ruby

html = ScraperWiki.scrape("http://www.melbournewater.com.au/content/water_storages/water_report/weekly_water_report_archives.asp?year=2001&file=wrr011221.html")
puts html

require 'nokogiri'

doc = Nokogiri::HTML(html, nil, 'utf-8')
counter=0



  puts "hi"
  doc.search('table >tr').each do |row|
  if counter < 3 then
      counter=counter+1
      puts row
      puts row.css('td')[0].text
      puts row.css('td')[3].text

      if not counter=0 then  
        record={}
        record ['ID']= "year0001"+ counter.to_s()
        record ['Reservoir']=row.css('td')[0].text
        record ['Percentage']=row.css('td')[3].text
        ScraperWiki.save_sqlite(["ID"], record)
      end
  end  
end
