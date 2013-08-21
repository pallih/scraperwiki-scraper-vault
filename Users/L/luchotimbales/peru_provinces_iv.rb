##################################################################################################
# Fourth part of the Ruby script to obtains electoral results from Peru @ http://www.infogob.com.pe
##################################################################################################

require 'mechanize'

$url={}
$date={}
$proceso={}

###################################################################
# These are the two functions we will need to use
###################################################################

# Scrape page, look for 'next' link: if found, submit the page form
def scrape_and_look_for_next_link(page, page_num, url, proceso,j)
  scrape_table(page.body, page_num, url, proceso,j)
  link = page.link_with(:text => '2')
  if link
    page.form_with(:name => 'aspnetForm') do |f|
      f['__EVENTTARGET'] = 'ctl00$ContentPlaceHolder1$detalleproceso_orgpol1$gvOrgPol'
      f['__EVENTARGUMENT'] = 'Page$2'
      page = f.submit()
      p page.body
    end
  scrape_and_look_for_next_link(page, '2', url, proceso,j)
  end
end

# scrape_table function: gets passed an individual page to scrape (not important for tutorial)
def scrape_table(page_body, page_number, url, proceso,j)
  i=0 
  data_table = Nokogiri::HTML(page_body).css('table#ctl00_ContentPlaceHolder1_detalleproceso_orgpol1_gvOrgPol tr').collect do |row|
    #puts row
    if i==0 then
      i=i+1
    else
      if i<7 and row.css('td')[0].inner_text!="12" then
        #puts row.css('td')[3].css('a').attr('href')
        record = {}
        record['ID']= url+"_&Pag="+ page_number +"_&Num="+ i.to_s()
        record['Organizacion'] = row.css('td')[0].inner_text
        record['Proceso'] =proceso
        record['Iteracion'] =j
        if not row.css('td')[3].nil? then
          record['Total votos']= row.css('td')[3].inner_text
        end
        if not row.css('td')[4].nil? then
          record['Porcentaje votos validos']= row.css('td')[4].inner_text
        end
        ScraperWiki.save_sqlite(["ID"], record)
        i=i+1
      end
    end
  end
end

###########################################################################
# we start downloading the district codes from the first script
###########################################################################


puts "*********************STARTING***************"
puts "*********************Getting list of distritos***************"
url= "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=htmltable&name=peru_provinces_iii&query=select%20*%20from%20%60swdata%60%20limit%201000000"
html= ScraperWiki.scrape(url)
l=0
require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('tr').each do |row|
    if l==0 then
      l=l+1
    else
      $url[l]=row.css('td')[0].inner_text
      $date[l]=row.css('td')[1].inner_text[6..9]
      $proceso[l]=row.css('td')[2].inner_text
      #puts $url[l]
      #puts $date[l]
      l=l+1
    end

end


for j in 1227..l-1
  if  $date[j].to_i >1965 and  $date[j].to_i <1996 then
    BASE_URL = 'http://www.infogob.com.pe/Localidad/'+ $url[j]
    puts "URL to scrapte: "+BASE_URL
    puts "iteracion: "+ j.to_s()
    
    # ---------------------------------------------------------------------------
    # START HERE: setting up Mechanize We need to set the user-agent header so the page thinks we're a browser,
    # as otherwise it won't show all the fields we need
    # ---------------------------------------------------------------------------
    
    starting_url = BASE_URL
    @br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
      browser.user_agent_alias = 'Linux Firefox'
    end
    page = @br.get(starting_url)
    p page.body
    
    # start scraping
    scrape_and_look_for_next_link(page, '1', $url[j], $proceso[j], j)
  end
end


