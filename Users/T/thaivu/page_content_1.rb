require 'rubygems'
require 'mechanize'

STARTING_URL = 'http://www.casey.vic.gov.au/psr/townPlanningSearch.asp?Search+Planning+and+Subdivision+Applications=Search+Planning+and+Subdivision+Applications'


def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def go_to_development_application_page(page)
  page_forms = page.forms
  radio_value = page_forms[2].radiobutton_with(:value => "P").check

  page = page_forms[2].click_button(page_forms[2].button_with(:value => "Search"))
  
  return page
end


@agent = Mechanize.new{|a|
  a.ssl_version,
  a.verify_mode = 'SSLv3',
  OpenSSL::SSL::VERIFY_NONE,
  a.user_agent_alias = 'Linux Firefox'
}

page = @agent.get(STARTING_URL)

page = go_to_development_application_page(page)

page.search('div#content table tr[bgcolor$="#ecf6fd"]').each do |da_container|
  
  tds = da_container.search('td')
  href = tds[0].at('a')['href']
  detail_page = page.link_with(:href => "#{href}").click

  content = detail_page.search('#content')
  table = content.search('table')
  list_tr = table.search('tr')

  first_tr = list_tr[0]
  list_td = first_tr.search('td')
  referrals = clean_whitespace(list_td[0].inner_text.gsub("Referrals:",""))
  puts referrals
  subsequent_decisions = clean_whitespace(list_td[1].inner_text.gsub("Subsequent Decisions:",""))
  puts subsequent_decisions 
  appeals = clean_whitespace(list_td[2].inner_text.gsub("Appeals:",""))
  puts appeals 

  detail_info = []
  for i in 1..list_tr.length-1
    tds = list_tr[i].search('td')
    item_obj = {}
    item_obj[:key] = clean_whitespace(tds[0].inner_text).downcase
    item_obj[:field] = clean_whitespace(tds[1].inner_text).downcase

    detail_info << item_obj
  end
  puts detail_info

=begin
  people_div = detail_page.search('#lblPeople')
  content = clean_whitespace(people_div.inner_text)
  content = content.split("Principal Certifying Authority:")
  applicant = clean_whitespace(content[0].gsub("Applicant:",""))
  principal_certifying_authority = clean_whitespace(content[1])

  cost_content = detail_page.search('#lblDim')
  cost = clean_whitespace(cost_content.inner_text)

  progress_content = detail_page.search('#lblTasks')
  progress_content = progress_content.search('tr')
  progress = []
  for i in 3..progress_content.length-2
    progress_obj = {}
    progress_td = progress_content[i].search('td')
    progress_obj[:action] = clean_whitespace(progress_td[0].inner_text)
    progress_obj[:commenced] = clean_whitespace(progress_td[1].inner_text)
    progress_obj[:completed] = clean_whitespace(progress_td[2].inner_text)
    progress << progress_obj 
  end
  puts progress

  officer_content = detail_page.search('#lblOfficer')
  officer = clean_whitespace(officer_content.inner_text)
  puts officer

  related_content = detail_page.search('#lblRelated')
  related = clean_whitespace(related_content.inner_text)
  puts related 
=end


  break
end