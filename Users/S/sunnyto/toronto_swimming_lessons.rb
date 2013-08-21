require 'nokogiri'
require 'mechanize'

Mechanize.html_parser=Nokogiri::HTML

brw = Mechanize.new { |b|
b.user_agent_alias = 'Linux Firefox'
b.read_timeout = 1200
b.agent.http.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

BASE_URL = "https://efun.toronto.ca/torontofun/Activities/ActivitiesAdvSearch.asp"
#pg = brw.get(BASE_URL)


#build initial cookie:

#post options
pg = brw.post(BASE_URL,
{"name"=>"cookie", 
"value"=>"value",
"Domain"=>"efun.toronto.ca",
"AdvSearch"=>"true",
"AllCatogerySubcatogerySelectedHintText"=>"All%20categories%2Fsubcategories%20",
"DateRangeFrom"=>"",
"DateRangeTo"=>"",
"KeywordSearch"=>"",
"SuperDropDownFrom"=>"dd-mm-yyyy",
"SuperDropDownFrom"=>"0",
"SuperDropDownTo"=>"dd-mm-yyyy",
"SuperDropDownTo"=>"0",
"chkKeywordRegistrationAvailable"=>"",
"chkWeekDay8"=>"9"} )




#do an advanced search on 'ALL' and traverse into each item in each page.

#do an initial POST command

def scrapebody(page_body)
  puts page_body.inspect
end

def scrape_and_look_for_next_link(page)
  scrapebody(page.body)
  #scrape_and_look_for_next_link() #keep looking for next page of data
end

puts pg.inspect
f = pg.form_with(:name => "all_search_form")
#f['KeywordSearch']='Bronze'
#f['__EVENTTARGET'] = 'ProviderSearchResultsTable1$NextLinkButton'
#f['__EVENTARGUMENT'] = ''

puts f.inspect
pg = brw.submit(f)
puts pg.inspect



#select program, times, dates, age group, description, and link
#use primary keys of website + program code or generated id??? or unique name?