# www.pueblosdelperu.org

html=ScraperWiki::scrape("http://www.pueblosdelperu.org")
puts html


id_areas={}
id_areas[0]="amazonas"
id_areas[1]="ancash"
id_areas[2]="apurimac"
id_areas[3]="arequipa"
id_areas[4]="ayacucho"
id_areas[5]="cajamarca"
id_areas[6]="provincia-constitucional-del-callao"
id_areas[7]="cusco"
id_areas[8]="huancavelica"
id_areas[9]="huanuco"
id_areas[10]="ica"
id_areas[11]="junin"
id_areas[12]="la-libertad"
id_areas[13]="lambayeque"
id_areas[14]="lima"
id_areas[15]="loreto"
id_areas[16]="madre-de-dios"
id_areas[17]="moquegua"
id_areas[18]="pasco"
id_areas[19]="piura"
id_areas[20]="puno"
id_areas[21]="san-martin"
id_areas[22]="tacna"
id_areas[23]="tumbes"
id_areas[24]="ucayali"
# id_areas[25]=""

for i in 0..24
  URL="http://www.pueblosdelperu.org"+ id_areas[i].to_s()
  html = ScraperWiki.scrape(URL)
  puts URL

  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-25')
  doc.search('td[@valign="top"]> div[align="left"]> table[@class="style24"]> tr').each do |row|  
    puts row
    puts row.css('td')[2].text
    puts row.css('td')[3].text
    puts row.css('td')[4].text
    
    record={}
    record ['Province 1']= id_areas[i].to_s() +"_" +row.css('td')[2].text
    record ['Province 2']=row.css('td')[2].text
    record ['Province 3']=row.css('td')[3].text
    record ['Province 4']= row.css('td')[4].text
    ScraperWiki.save_sqlite(["Province"], record)

end
end

