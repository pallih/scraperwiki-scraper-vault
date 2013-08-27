titulo=String.new
descripcion=String.new
ciclo=String.new
startDate = Time.new
endDate = Time.new
record={}
$Url_conference={}

puts "*********************STARTING***************"
puts "*********************Getting list of concerts***************"

# Getting list of concerts
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=march_conferencias_id&query=select%20*%20from%20%60swdata%60%20limit%20100000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  if l==0 then
  else
    #puts datos.css("td")[2].inner_html
    $Url_conference[l-1]=datos.css("td")[2].inner_html
  end
  l=l+1
end

puts "*********************STARTING***************"
puts $Url_conference.length-1

for j in 0..$Url_conference.length-1
    url= $Url_conference[j]
    html= ScraperWiki.scrape(url,encoding="utf-8")     
    puts j.to_s() +" "+ html
    puts url
          
    html2 = html.slice (html.index("SUBTITULO Y FECHA")..html.length)
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html2 , nil, 'utf-8')
    doc.search('h1> a').each do |row|
      puts row.inner_html
      titulo= row.inner_html
    end
    
    doc.search('span[@id="tituloFechas"]').each do |row|
      #puts row.css("meta[@itemprop='startDate']").attr("content")
      #puts row.css("meta[@itemprop='endDate']").attr("content")
      if not row.css("meta[@itemprop='startDate']").nil? then
        startDate = row.css("meta[@itemprop='startDate']").attr("content")
      else
        startDate =""
      end
      if not row.css("meta[@itemprop='endDate']").attr("content").nil? then
        endDate = row.css("meta[@itemprop='endDate']").attr("content")
      else
        endDate =""
      end
    end
  
    doc.search('a[@id="tituloSeccion"]').each do |row|
      puts row.inner_html
      ciclo = row.inner_html
    end

    
    html2 = html.slice (html.index("Contenidos seg")+36..html.length)    
    doc.search('div[@id="presentacionContenido"]').each do |row|
      puts row.inner_html
      descripcion=row.text
    end
    
    record ['ID']= j.to_s()
    record ['Source']= url
    record ['Titulo']= titulo
    record ['Ciclo']= ciclo
    record ['Descripcion']= descripcion
    #record ['StartDate']= startDate
    #record ['EndDate']= endDate
    ScraperWiki.save_sqlite(["ID"], record)

endtitulo=String.new
descripcion=String.new
ciclo=String.new
startDate = Time.new
endDate = Time.new
record={}
$Url_conference={}

puts "*********************STARTING***************"
puts "*********************Getting list of concerts***************"

# Getting list of concerts
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=march_conferencias_id&query=select%20*%20from%20%60swdata%60%20limit%20100000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  if l==0 then
  else
    #puts datos.css("td")[2].inner_html
    $Url_conference[l-1]=datos.css("td")[2].inner_html
  end
  l=l+1
end

puts "*********************STARTING***************"
puts $Url_conference.length-1

for j in 0..$Url_conference.length-1
    url= $Url_conference[j]
    html= ScraperWiki.scrape(url,encoding="utf-8")     
    puts j.to_s() +" "+ html
    puts url
          
    html2 = html.slice (html.index("SUBTITULO Y FECHA")..html.length)
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html2 , nil, 'utf-8')
    doc.search('h1> a').each do |row|
      puts row.inner_html
      titulo= row.inner_html
    end
    
    doc.search('span[@id="tituloFechas"]').each do |row|
      #puts row.css("meta[@itemprop='startDate']").attr("content")
      #puts row.css("meta[@itemprop='endDate']").attr("content")
      if not row.css("meta[@itemprop='startDate']").nil? then
        startDate = row.css("meta[@itemprop='startDate']").attr("content")
      else
        startDate =""
      end
      if not row.css("meta[@itemprop='endDate']").attr("content").nil? then
        endDate = row.css("meta[@itemprop='endDate']").attr("content")
      else
        endDate =""
      end
    end
  
    doc.search('a[@id="tituloSeccion"]').each do |row|
      puts row.inner_html
      ciclo = row.inner_html
    end

    
    html2 = html.slice (html.index("Contenidos seg")+36..html.length)    
    doc.search('div[@id="presentacionContenido"]').each do |row|
      puts row.inner_html
      descripcion=row.text
    end
    
    record ['ID']= j.to_s()
    record ['Source']= url
    record ['Titulo']= titulo
    record ['Ciclo']= ciclo
    record ['Descripcion']= descripcion
    #record ['StartDate']= startDate
    #record ['EndDate']= endDate
    ScraperWiki.save_sqlite(["ID"], record)

endtitulo=String.new
descripcion=String.new
ciclo=String.new
startDate = Time.new
endDate = Time.new
record={}
$Url_conference={}

puts "*********************STARTING***************"
puts "*********************Getting list of concerts***************"

# Getting list of concerts
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=march_conferencias_id&query=select%20*%20from%20%60swdata%60%20limit%20100000"
html= ScraperWiki.scrape(url)

l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |datos|
  if l==0 then
  else
    #puts datos.css("td")[2].inner_html
    $Url_conference[l-1]=datos.css("td")[2].inner_html
  end
  l=l+1
end

puts "*********************STARTING***************"
puts $Url_conference.length-1

for j in 0..$Url_conference.length-1
    url= $Url_conference[j]
    html= ScraperWiki.scrape(url,encoding="utf-8")     
    puts j.to_s() +" "+ html
    puts url
          
    html2 = html.slice (html.index("SUBTITULO Y FECHA")..html.length)
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html2 , nil, 'utf-8')
    doc.search('h1> a').each do |row|
      puts row.inner_html
      titulo= row.inner_html
    end
    
    doc.search('span[@id="tituloFechas"]').each do |row|
      #puts row.css("meta[@itemprop='startDate']").attr("content")
      #puts row.css("meta[@itemprop='endDate']").attr("content")
      if not row.css("meta[@itemprop='startDate']").nil? then
        startDate = row.css("meta[@itemprop='startDate']").attr("content")
      else
        startDate =""
      end
      if not row.css("meta[@itemprop='endDate']").attr("content").nil? then
        endDate = row.css("meta[@itemprop='endDate']").attr("content")
      else
        endDate =""
      end
    end
  
    doc.search('a[@id="tituloSeccion"]').each do |row|
      puts row.inner_html
      ciclo = row.inner_html
    end

    
    html2 = html.slice (html.index("Contenidos seg")+36..html.length)    
    doc.search('div[@id="presentacionContenido"]').each do |row|
      puts row.inner_html
      descripcion=row.text
    end
    
    record ['ID']= j.to_s()
    record ['Source']= url
    record ['Titulo']= titulo
    record ['Ciclo']= ciclo
    record ['Descripcion']= descripcion
    #record ['StartDate']= startDate
    #record ['EndDate']= endDate
    ScraperWiki.save_sqlite(["ID"], record)

end