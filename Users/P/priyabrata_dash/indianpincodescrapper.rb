#######################################################################################################
# START HERE: Scraping ASP.NET page of India post PIN Search (HTML pages that has ASPX code), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on
# .aspx pages, you're actually submitting a form.
# This scrapper captures the list of Indian States, Districts & Pin codes based on districts
#######################################################################################################

require 'mechanize'
require 'nokogiri'

# Function to search pin
def click_search(tagent,tpage,turl)
   
end

# Initialize arrays for statues & districts
states = Array.new
districts = Array.new

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser,
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------
BASE_URL = 'http://www.indiapost.gov.in/'
starting_url = BASE_URL + 'pin/pinsearch.aspx'

@br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
end

# Search for all the states & Districts in India identified by India Post
page = @br.get(starting_url)
doc = Nokogiri::HTML(page.body)
doc.xpath("//select[@id='ddl_state']/option").each do |state_segemnt|
  tState= state_segemnt.content
  states.push tState
end

states.each do |state|
  #puts state
end

doc.xpath("//select[@id='ddl_dist']/option").each do |district_segemnt|
  tDistrict= district_segemnt.content
  districts.push tDistrict
end

districts.each do |district|
  #puts district
end


#Click Searchclick_search(page)

record = {};
   record["__EVENTTARGET"] = "";
   record["__EVENTARGUMENT"] = "";
   record["__VIEWSTATE"] = doc.xpath("//input[@type='hidden' and @id='__VIEWSTATE']").first['__VIEWSTATE']
   record["__VIEWSTATEENCRYPTED"] = "";
   record["__EVENTVALIDATION"] = doc.xpath("//input[@type='hidden' and @id='__EVENTVALIDATION']").first['__EVENTVALIDATION']
   puts record["__VIEWSTATE"]
   puts record["__EVENTVALIDATION"]
   record["txt_offname"] = "";
   record["search_on"]="Search";
   record["ddl_dist"]="0";
   record["txt_dist_on"] = "";
   record["ddl_state"]="1";
   record["txt_stateon"]="";
   record["hdn_tabchoice"]="1";
   page = @br.post(starting_url,record); 
   pp page.body
#Click Seach End



doc = Nokogiri::HTML(page.body)

totalCount=0
doc.xpath("//span[@id='lbl_remarks']").each do |count|
  totalCount = count.content.scan(/\d+/).map{|i| i.to_i}[0]
end

puts "Number of Pin Records: #{totalCount}"

#Parse the tables for Pin codes
currentCount = 0
pageCount = 0
bLink = true
#pinDetails = Array.new

#Parse All Pin details in the Page
while bLink==true
  pageCount = pageCount + 1
  rowCount = 0
  data_table = Nokogiri::HTML(page.body).xpath("//table[@id='gvw_offices']/tr[@style and not(@align=center)]").collect do |row|
    if rowCount !=0
      currentCount = currentCount + 1
      record = {}
      record['currentCount'] = currentCount.to_s          
      record['Office_Name'] = row.css('td')[1].inner_text
      record['Pin_code']  = row.css('td')[2].inner_text
      record['District'] = row.css('td')[3].inner_text
      #ScraperWiki.save_sqlite(["currentCount"], record)
      puts record.values.join(';').to_s
    end
    rowCount = rowCount + 1
  end
  
  #Parse the Next link in the page & click it
  if page.at("//a[contains(@href,'Page$#{(currentCount+1)}')]") == true 
    page.form_with(:name => 'form1') do |f|
      f['__EVENTTARGET'] = 'gvw_offices'
      f['__EVENTARGUMENT'] = "Page$#{(currentCount+1)}"
      page = f.submit()
    end
  end

end

#######################################################################################################
# START HERE: Scraping ASP.NET page of India post PIN Search (HTML pages that has ASPX code), using the
# very powerful Mechanize library. In general, when you follow a 'next' link on
# .aspx pages, you're actually submitting a form.
# This scrapper captures the list of Indian States, Districts & Pin codes based on districts
#######################################################################################################

require 'mechanize'
require 'nokogiri'

# Function to search pin
def click_search(tagent,tpage,turl)
   
end

# Initialize arrays for statues & districts
states = Array.new
districts = Array.new

# ---------------------------------------------------------------------------
# START HERE: setting up Mechanize
# We need to set the user-agent header so the page thinks we're a browser,
# as otherwise it won't show all the fields we need
# ---------------------------------------------------------------------------
BASE_URL = 'http://www.indiapost.gov.in/'
starting_url = BASE_URL + 'pin/pinsearch.aspx'

@br = Mechanize.new do |browser|      # Set the user-agent as Firefox - if the page knows we're Mechanize, it won't return all fields
  browser.user_agent_alias = 'Linux Firefox'
end

# Search for all the states & Districts in India identified by India Post
page = @br.get(starting_url)
doc = Nokogiri::HTML(page.body)
doc.xpath("//select[@id='ddl_state']/option").each do |state_segemnt|
  tState= state_segemnt.content
  states.push tState
end

states.each do |state|
  #puts state
end

doc.xpath("//select[@id='ddl_dist']/option").each do |district_segemnt|
  tDistrict= district_segemnt.content
  districts.push tDistrict
end

districts.each do |district|
  #puts district
end


#Click Searchclick_search(page)

record = {};
   record["__EVENTTARGET"] = "";
   record["__EVENTARGUMENT"] = "";
   record["__VIEWSTATE"] = doc.xpath("//input[@type='hidden' and @id='__VIEWSTATE']").first['__VIEWSTATE']
   record["__VIEWSTATEENCRYPTED"] = "";
   record["__EVENTVALIDATION"] = doc.xpath("//input[@type='hidden' and @id='__EVENTVALIDATION']").first['__EVENTVALIDATION']
   puts record["__VIEWSTATE"]
   puts record["__EVENTVALIDATION"]
   record["txt_offname"] = "";
   record["search_on"]="Search";
   record["ddl_dist"]="0";
   record["txt_dist_on"] = "";
   record["ddl_state"]="1";
   record["txt_stateon"]="";
   record["hdn_tabchoice"]="1";
   page = @br.post(starting_url,record); 
   pp page.body
#Click Seach End



doc = Nokogiri::HTML(page.body)

totalCount=0
doc.xpath("//span[@id='lbl_remarks']").each do |count|
  totalCount = count.content.scan(/\d+/).map{|i| i.to_i}[0]
end

puts "Number of Pin Records: #{totalCount}"

#Parse the tables for Pin codes
currentCount = 0
pageCount = 0
bLink = true
#pinDetails = Array.new

#Parse All Pin details in the Page
while bLink==true
  pageCount = pageCount + 1
  rowCount = 0
  data_table = Nokogiri::HTML(page.body).xpath("//table[@id='gvw_offices']/tr[@style and not(@align=center)]").collect do |row|
    if rowCount !=0
      currentCount = currentCount + 1
      record = {}
      record['currentCount'] = currentCount.to_s          
      record['Office_Name'] = row.css('td')[1].inner_text
      record['Pin_code']  = row.css('td')[2].inner_text
      record['District'] = row.css('td')[3].inner_text
      #ScraperWiki.save_sqlite(["currentCount"], record)
      puts record.values.join(';').to_s
    end
    rowCount = rowCount + 1
  end
  
  #Parse the Next link in the page & click it
  if page.at("//a[contains(@href,'Page$#{(currentCount+1)}')]") == true 
    page.form_with(:name => 'form1') do |f|
      f['__EVENTTARGET'] = 'gvw_offices'
      f['__EVENTARGUMENT'] = "Page$#{(currentCount+1)}"
      page = f.submit()
    end
  end

end

