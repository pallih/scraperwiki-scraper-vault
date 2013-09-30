# Blank Ruby

$url={}

# Getting list of URLs to scrape
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=water_storage_year&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
  else
    #puts datos.inner_html
    $url[l-1]=datos.inner_html
  end
  l=l+1
end

puts l.to_s()

puts "http://www.melbournewater.com.au/"+ $url[1].to_s()


for p in -1..0

    html = ScraperWiki.scrape("http://www.melbournewater.com.au/"+ $url[p].to_s())
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

end
# Blank Ruby

$url={}

# Getting list of URLs to scrape
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=water_storage_year&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
  else
    #puts datos.inner_html
    $url[l-1]=datos.inner_html
  end
  l=l+1
end

puts l.to_s()

puts "http://www.melbournewater.com.au/"+ $url[1].to_s()


for p in -1..0

    html = ScraperWiki.scrape("http://www.melbournewater.com.au/"+ $url[p].to_s())
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

end
# Blank Ruby

$url={}

# Getting list of URLs to scrape
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=water_storage_year&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
  else
    #puts datos.inner_html
    $url[l-1]=datos.inner_html
  end
  l=l+1
end

puts l.to_s()

puts "http://www.melbournewater.com.au/"+ $url[1].to_s()


for p in -1..0

    html = ScraperWiki.scrape("http://www.melbournewater.com.au/"+ $url[p].to_s())
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

end
# Blank Ruby

$url={}

# Getting list of URLs to scrape
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=water_storage_year&query=select%20*%20from%20%60swdata%60%20limit%2010000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('td').each do |datos|
  if l==0 then
  else
    #puts datos.inner_html
    $url[l-1]=datos.inner_html
  end
  l=l+1
end

puts l.to_s()

puts "http://www.melbournewater.com.au/"+ $url[1].to_s()


for p in -1..0

    html = ScraperWiki.scrape("http://www.melbournewater.com.au/"+ $url[p].to_s())
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

end
