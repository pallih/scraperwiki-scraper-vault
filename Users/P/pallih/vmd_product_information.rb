require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

### SETUP

$checklist = (0..300).step(20).to_a #we really should check if the number is dividable by 20 or not, instead of a check against this array

url = "http://www.vmd.defra.gov.uk/ProductInformationDatabase/"
$agent = Mechanize.new
$page = $agent.get(url)


### DEFS


def get_next_page(page, page_number)
  event_target = "ctl00$ctl00$VMDMaster$PIDMaster$WebTab1$tmpl1$CAPGridPage" + page_number
  page.form_with(:name => 'aspnetForm') do |f|
    f["__EVENTTARGET"] = event_target
    search_results = $agent.submit(f, f.buttons.first)
    process(search_results.body)
    current_page = Nokogiri::HTML(search_results.body).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGridPages"]/a[@class="CurrentCurrentPage"]/.')
    puts "Processed page: " + page_number
    next_page = Nokogiri::HTML(search_results.body).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGridPages"]/a[@class="CurrentCurrentPage"]/following-sibling::a[@class="alphabetLinkButton"]/.')
    if next_page.css('a').inner_text != ""
     next_page_number = page_number.succ
     puts "There is a next page and it is number " + next_page_number
       if $checklist.include? page_number.to_i #Every 20 pages we need to refresh the pagination by submitting the form
         puts "We are at the end of pagination - we need to get the next batch of 20 pages"
         page.form_with(:name => 'aspnetForm') do |f|
         f["__EVENTTARGET"] = 'ctl00$ctl00$VMDMaster$PIDMaster$WebTab1$tmpl1$CAPGridNextSet'
         search_results = $agent.submit(f, f.buttons.first)
         end
       end 

     get_next_page(search_results, page_number.succ)
    else
      puts "last page - done!"
    end

  end
end

def process(search_results)
  tr = Nokogiri::HTML(search_results).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGrid_ctl00"]//tr[@id[contains(.,"chlGCnt:1")]]').each do |td|
    record = {}
      record['number']            = td.css('td')[1].inner_text
      record['name']            = td.css('td')[2].inner_text
      record['ma_holder']            = td.css('td')[3].inner_text
      record['vm_number']            = td.css('td')[4].inner_text
      record['date_of_issue']            = td.css('td')[5].inner_text
      record['authorisation_route']            = td.css('td')[6].inner_text
      record['active_substance']            = td.css('td')[7].inner_text
      record['controlled_drug']            = td.css('td')[8].inner_text
      record['target_species']            = td.css('td')[9].inner_text
      record['distribution_category']            = td.css('td')[10].inner_text
  ScraperWiki.save_sqlite(unique_keys=["vm_number"],record, table_name="VMD_product_info")
  end

end


### GET FIRST PAGE AND SELECT ALL RECORDS

$page.form_with(:name => 'aspnetForm') do |f|
  f["__EVENTTARGET"] = ["ctl00$ctl00$VMDMaster$lbtnAll"] #Select all records
  search_results = $agent.submit(f, f.buttons.first)
  process(search_results.body)
  current_page = Nokogiri::HTML(search_results.body).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGridPages"]/a[@class="CurrentCurrentPage"]/.')
  current_page_number = current_page.css('a')[0].inner_text
  puts "Current page: " + current_page_number
  next_page = Nokogiri::HTML(search_results.body).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGridPages"]/a[@class="CurrentCurrentPage"]/following-sibling::a[@class="alphabetLinkButton"]/.')
  if next_page != nil 
    puts "there is a next page and it is number " + current_page_number.succ
    get_next_page(search_results, current_page_number.succ)
  else
    puts "This was the last page. We are done!"
  end
end




require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'

### SETUP

$checklist = (0..300).step(20).to_a #we really should check if the number is dividable by 20 or not, instead of a check against this array

url = "http://www.vmd.defra.gov.uk/ProductInformationDatabase/"
$agent = Mechanize.new
$page = $agent.get(url)


### DEFS


def get_next_page(page, page_number)
  event_target = "ctl00$ctl00$VMDMaster$PIDMaster$WebTab1$tmpl1$CAPGridPage" + page_number
  page.form_with(:name => 'aspnetForm') do |f|
    f["__EVENTTARGET"] = event_target
    search_results = $agent.submit(f, f.buttons.first)
    process(search_results.body)
    current_page = Nokogiri::HTML(search_results.body).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGridPages"]/a[@class="CurrentCurrentPage"]/.')
    puts "Processed page: " + page_number
    next_page = Nokogiri::HTML(search_results.body).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGridPages"]/a[@class="CurrentCurrentPage"]/following-sibling::a[@class="alphabetLinkButton"]/.')
    if next_page.css('a').inner_text != ""
     next_page_number = page_number.succ
     puts "There is a next page and it is number " + next_page_number
       if $checklist.include? page_number.to_i #Every 20 pages we need to refresh the pagination by submitting the form
         puts "We are at the end of pagination - we need to get the next batch of 20 pages"
         page.form_with(:name => 'aspnetForm') do |f|
         f["__EVENTTARGET"] = 'ctl00$ctl00$VMDMaster$PIDMaster$WebTab1$tmpl1$CAPGridNextSet'
         search_results = $agent.submit(f, f.buttons.first)
         end
       end 

     get_next_page(search_results, page_number.succ)
    else
      puts "last page - done!"
    end

  end
end

def process(search_results)
  tr = Nokogiri::HTML(search_results).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGrid_ctl00"]//tr[@id[contains(.,"chlGCnt:1")]]').each do |td|
    record = {}
      record['number']            = td.css('td')[1].inner_text
      record['name']            = td.css('td')[2].inner_text
      record['ma_holder']            = td.css('td')[3].inner_text
      record['vm_number']            = td.css('td')[4].inner_text
      record['date_of_issue']            = td.css('td')[5].inner_text
      record['authorisation_route']            = td.css('td')[6].inner_text
      record['active_substance']            = td.css('td')[7].inner_text
      record['controlled_drug']            = td.css('td')[8].inner_text
      record['target_species']            = td.css('td')[9].inner_text
      record['distribution_category']            = td.css('td')[10].inner_text
  ScraperWiki.save_sqlite(unique_keys=["vm_number"],record, table_name="VMD_product_info")
  end

end


### GET FIRST PAGE AND SELECT ALL RECORDS

$page.form_with(:name => 'aspnetForm') do |f|
  f["__EVENTTARGET"] = ["ctl00$ctl00$VMDMaster$lbtnAll"] #Select all records
  search_results = $agent.submit(f, f.buttons.first)
  process(search_results.body)
  current_page = Nokogiri::HTML(search_results.body).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGridPages"]/a[@class="CurrentCurrentPage"]/.')
  current_page_number = current_page.css('a')[0].inner_text
  puts "Current page: " + current_page_number
  next_page = Nokogiri::HTML(search_results.body).xpath('//div[@id="ctl00_ctl00_VMDMaster_PIDMaster_WebTab1_tmpl1_CAPGridPages"]/a[@class="CurrentCurrentPage"]/following-sibling::a[@class="alphabetLinkButton"]/.')
  if next_page != nil 
    puts "there is a next page and it is number " + current_page_number.succ
    get_next_page(search_results, current_page_number.succ)
  else
    puts "This was the last page. We are done!"
  end
end




