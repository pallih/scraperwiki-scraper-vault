# Blank Ruby

id_areas={}
id_areas[0]="2001"
id_areas[1]="2002"
id_areas[2]="2003"
id_areas[3]="2004"
id_areas[4]="2005"
id_areas[5]="2006"
id_areas[6]="2007"
id_areas[7]="2008"
id_areas[8]="2009"
id_areas[9]="2010"
id_areas[10]="2011"
id_areas[11]="2012"
id_areas[12]="2013"

for i in 0..12
    counter=0
    html = ScraperWiki.scrape("http://www.melbournewater.com.au/content/water_storages/water_report/weekly_water_report_archives.asp?year="+ id_areas[i].to_s())
    puts html
    
    require 'nokogiri'
    
    doc = Nokogiri::HTML(html, nil, 'utf-8')
      
      doc.search('td> ul >li').each do |row|
      counter=counter+1

      puts row
      puts row.css('a').attr('href')
      record={}
      record ['ID']= "year_"+ id_areas[i].to_s() +"_" +counter.to_s()
      record ['URL']=row.css('a').attr('href')
      ScraperWiki.save_sqlite(["ID"], record)
    
    end
end

   
   
  

