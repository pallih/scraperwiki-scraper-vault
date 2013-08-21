# Blank Ruby
# encoding: ISO-8859-1
#wutf-8
# warum hier keine umlaute???

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'


#  site="http://www.schwarzeradler-egelsee.de/"
#  url=""
  url2get='http://www.schwarzeradler-egelsee.de/body/programm/programm.php'

  agent = Mechanize.new
  agent.get('http://www.schwarzeradler-egelsee.de/body/programm/programm.php')



mpage = agent.page
yon = mpage.body.scan (/<<([^<]+)>>/)


  doc= agent.page.at('html') #doc= agent.page.at('html/body/table') 
puts "start" #doc.inner_html
  nodes = doc.search('tr')
  i = 3
  j=0
  while i < nodes.length do
  #   puts i
     puts yon[j]
     datumname=yon[j]
puts datumname[0].encoding
     puts nodes[i].text.strip
     desc=nodes[i].text.strip
puts desc[0].encoding
     i += 3
     j+=1
      data = {
        'datumname' => datumname,
        'beschreibung' => desc, #name.encode("UTF-8"),
        'ort' => 'Schwarzer Adler, Memmingen',
   #    # 'preis' => preis,
        'kategorie' => 'Konzert?',
        'url' => url2get
      }
 #   begin
 #     puts data.to_json
 #   rescue
 #     puts "kein output "#+i._to_s()
 #   end
    begin
      ScraperWiki.save_sqlite(unique_keys=['datumname'], data=data) 
    rescue
      puts "kein output "#+i.to_s()
    end
    
  end


#mpage = agent.page#.at('html')
#yon = mpage.body.scan (/<<([^<]+)>>/)
#puts yon

