require 'rubygems'
require 'mechanize'
require 'active_support'

STARTING_URL = 'http://connect.richmondvalley.nsw.gov.au/MasterView/modules/ApplicationMaster/default.aspx?page=search'
PERIOD_DATE = 50.days

def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def go_to_development_application_page(page)
  page = page.forms.first.click_button(page.forms.first.button_with(:value => "Agree"))
  
  return page
end

def get_table_by_row(table)
  info = []
  
  list_tr = table.search('tr')
  if(list_tr.size > 0)
    list_tr.each do |tr|
      info_obj = {}
      list_td = tr.search('td')
      if(list_td.size > 2)
        info_obj[:key] = clean_whitespace(list_td[1].inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
        info_obj[:value] = clean_whitespace(list_td[2].inner_text)
      end
      info << info_obj
    end
  end

  return info
end

def get_table_content(table)
  info = []

  list_tr = table.search('tr')
  if(list_tr.size > 1)
    list_key = []
    if(list_tr[0].search('th').size > 0)
      list_key_row = list_tr[0].search('th')
    else
      list_key_row = list_tr[0].search('td')
    end

    list_key_row.each do |item|
      list_key << clean_whitespace(item.inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
    end

    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      if(list_td.length == list_key.length)
        info_obj = {}
        for j in 0..list_td.length-1
          info_obj[list_key[j]] = clean_whitespace(list_td[j].inner_text)
        end
        info << info_obj
      end
    end
  end
  
  return info
end

@agent = Mechanize.new{|a|
  a.ssl_version,
  a.verify_mode = 'SSLv3',
  OpenSSL::SSL::VERIFY_NONE,
  a.idle_timeout = 10000000,
  a.open_timeout = 10000000,
  a.read_timeout = 10000000,
  a.user_agent_alias = 'Linux Firefox'
}
page = @agent.get(STARTING_URL)
page = go_to_development_application_page(page)
from_date = Time.new(1985)
to_date = Time.now
iterator_from_date = to_date - PERIOD_DATE
flag = false
#while (iterator_from_date.year >= from_date.year) do
 
  #while (iterator_from_date.year >= from_date.year) do
    #Get page_form_search and initialize 'DADateFrom' and 'DADateTo' fields
    page_form_search = page.forms.first
    page_form_search.field_with(:id => "_ctl3_drDates_txtDay1").value = iterator_from_date.day.to_s
    page_form_search.field_with(:id => "_ctl3_drDates_txtMonth1").value = iterator_from_date.month.to_s
    page_form_search.field_with(:id => "_ctl3_drDates_txtYear1").value = iterator_from_date.year.to_s
    
    page_form_search.field_with(:id => "_ctl3_drDates_txtDay2").value = to_date.day.to_s
    page_form_search.field_with(:id => "_ctl3_drDates_txtMonth2").value = to_date.month.to_s
    page_form_search.field_with(:id => "_ctl3_drDates_txtYear2").value = to_date.year.to_s
    page = page_form_search.click_button(page.forms.first.button_with(:id => "_ctl3_btnSearch"))


  table = page.search('table table')
  da_containers = (table != nil) ? table.search('tr[onclick]') : []
  da_containers.each do |da_container|
    detail_page = nil
    tds = da_container.search('td')
    href = tds[0].at('a')['href']
    detail_page = page.link_with(:href => "#{href}").click

    #puts detail_page.body.to_s

    info = []
    info_table = detail_page.search('table.list')
    if(info_table.size > 0)
      info_table = info_table[0]
      
      info = get_table_by_row(info_table)
    end
    
    event_table = detail_page.search('#lblHistory')
    if(!event_table.nil?)
      event_info = get_table_content(event_table)
      info.each do |item|
        if(item[:key] == "events")
          item[:value] = event_info
          break
        end
      end
    end   

    puts info

    break
  end

=begin
    info = []
    element = detail_page.search('#Content')
    if(element.size > 0 )
      list_table = element[0].search('table.list')
      if(list_table.size > 0)
        table = list_table[0]
        info = get_table_by_row(table)
      end
    end
    puts info
=end

=begin
    info = []
    element = detail_page.search('#Content')
    if(element.size > 1 )
      list_table = element[1].search('table.list')
      if(list_table.size > 0)
        table = list_table[0]
        info = get_table_content(table)
      end
    end
    puts info
=end

=begin
    info = {}
    element = detail_page.search('.innerWrap')
    if(element.size > 2 )
      info[:key] = clean_whitespace(element[2].inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
      info[:value] = ""
    end
    puts info
=end


=begin
    flag = true
    break
  end
  
  if(flag)
    break
  end
=end

=begin
  page_form_search = page.forms[1]
  page_form_search.field_with(:id => "DADateFrom").value = iterator_from_date.strftime('%d/%m/%Y').to_s
  page_form_search.field_with(:id => "DADateTo").value = to_date.strftime('%d/%m/%Y').to_s
  
  #Get page
  page = page_form_search.click_button(page.forms.first.button_with(:value => "Search"))
  
  #Get page_links and item_count
  page_links = page.search("div#fullcontent h4[class$=non_table_headers]")
  item_count = page_links.length
  
  #Update global variables
  @index = 0
  @max_index = page_links.length - 1
  @url = page.uri
  
  #Get all development applications based on page_links
  if item_count > 0
    (@index..@max_index).each do |i|
       a = CHILD_URL + page_links[i].at('a')[:href]
       child_page = @agent.get(a)

       da_container = child_page.search("div#fullcontent p[class$=rowDataOnly]")
       

       instruction = child_page.search('#instructions-content')
       puts clean_whitespace(instruction.inner_html)

       flag = true

       break

    end
    if flag
      break
    end
  end
=end

#end

require 'rubygems'
require 'mechanize'
require 'active_support'

STARTING_URL = 'http://connect.richmondvalley.nsw.gov.au/MasterView/modules/ApplicationMaster/default.aspx?page=search'
PERIOD_DATE = 50.days

def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def go_to_development_application_page(page)
  page = page.forms.first.click_button(page.forms.first.button_with(:value => "Agree"))
  
  return page
end

def get_table_by_row(table)
  info = []
  
  list_tr = table.search('tr')
  if(list_tr.size > 0)
    list_tr.each do |tr|
      info_obj = {}
      list_td = tr.search('td')
      if(list_td.size > 2)
        info_obj[:key] = clean_whitespace(list_td[1].inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
        info_obj[:value] = clean_whitespace(list_td[2].inner_text)
      end
      info << info_obj
    end
  end

  return info
end

def get_table_content(table)
  info = []

  list_tr = table.search('tr')
  if(list_tr.size > 1)
    list_key = []
    if(list_tr[0].search('th').size > 0)
      list_key_row = list_tr[0].search('th')
    else
      list_key_row = list_tr[0].search('td')
    end

    list_key_row.each do |item|
      list_key << clean_whitespace(item.inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
    end

    for i in 1..list_tr.length-1
      list_td = list_tr[i].search('td')
      if(list_td.length == list_key.length)
        info_obj = {}
        for j in 0..list_td.length-1
          info_obj[list_key[j]] = clean_whitespace(list_td[j].inner_text)
        end
        info << info_obj
      end
    end
  end
  
  return info
end

@agent = Mechanize.new{|a|
  a.ssl_version,
  a.verify_mode = 'SSLv3',
  OpenSSL::SSL::VERIFY_NONE,
  a.idle_timeout = 10000000,
  a.open_timeout = 10000000,
  a.read_timeout = 10000000,
  a.user_agent_alias = 'Linux Firefox'
}
page = @agent.get(STARTING_URL)
page = go_to_development_application_page(page)
from_date = Time.new(1985)
to_date = Time.now
iterator_from_date = to_date - PERIOD_DATE
flag = false
#while (iterator_from_date.year >= from_date.year) do
 
  #while (iterator_from_date.year >= from_date.year) do
    #Get page_form_search and initialize 'DADateFrom' and 'DADateTo' fields
    page_form_search = page.forms.first
    page_form_search.field_with(:id => "_ctl3_drDates_txtDay1").value = iterator_from_date.day.to_s
    page_form_search.field_with(:id => "_ctl3_drDates_txtMonth1").value = iterator_from_date.month.to_s
    page_form_search.field_with(:id => "_ctl3_drDates_txtYear1").value = iterator_from_date.year.to_s
    
    page_form_search.field_with(:id => "_ctl3_drDates_txtDay2").value = to_date.day.to_s
    page_form_search.field_with(:id => "_ctl3_drDates_txtMonth2").value = to_date.month.to_s
    page_form_search.field_with(:id => "_ctl3_drDates_txtYear2").value = to_date.year.to_s
    page = page_form_search.click_button(page.forms.first.button_with(:id => "_ctl3_btnSearch"))


  table = page.search('table table')
  da_containers = (table != nil) ? table.search('tr[onclick]') : []
  da_containers.each do |da_container|
    detail_page = nil
    tds = da_container.search('td')
    href = tds[0].at('a')['href']
    detail_page = page.link_with(:href => "#{href}").click

    #puts detail_page.body.to_s

    info = []
    info_table = detail_page.search('table.list')
    if(info_table.size > 0)
      info_table = info_table[0]
      
      info = get_table_by_row(info_table)
    end
    
    event_table = detail_page.search('#lblHistory')
    if(!event_table.nil?)
      event_info = get_table_content(event_table)
      info.each do |item|
        if(item[:key] == "events")
          item[:value] = event_info
          break
        end
      end
    end   

    puts info

    break
  end

=begin
    info = []
    element = detail_page.search('#Content')
    if(element.size > 0 )
      list_table = element[0].search('table.list')
      if(list_table.size > 0)
        table = list_table[0]
        info = get_table_by_row(table)
      end
    end
    puts info
=end

=begin
    info = []
    element = detail_page.search('#Content')
    if(element.size > 1 )
      list_table = element[1].search('table.list')
      if(list_table.size > 0)
        table = list_table[0]
        info = get_table_content(table)
      end
    end
    puts info
=end

=begin
    info = {}
    element = detail_page.search('.innerWrap')
    if(element.size > 2 )
      info[:key] = clean_whitespace(element[2].inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
      info[:value] = ""
    end
    puts info
=end


=begin
    flag = true
    break
  end
  
  if(flag)
    break
  end
=end

=begin
  page_form_search = page.forms[1]
  page_form_search.field_with(:id => "DADateFrom").value = iterator_from_date.strftime('%d/%m/%Y').to_s
  page_form_search.field_with(:id => "DADateTo").value = to_date.strftime('%d/%m/%Y').to_s
  
  #Get page
  page = page_form_search.click_button(page.forms.first.button_with(:value => "Search"))
  
  #Get page_links and item_count
  page_links = page.search("div#fullcontent h4[class$=non_table_headers]")
  item_count = page_links.length
  
  #Update global variables
  @index = 0
  @max_index = page_links.length - 1
  @url = page.uri
  
  #Get all development applications based on page_links
  if item_count > 0
    (@index..@max_index).each do |i|
       a = CHILD_URL + page_links[i].at('a')[:href]
       child_page = @agent.get(a)

       da_container = child_page.search("div#fullcontent p[class$=rowDataOnly]")
       

       instruction = child_page.search('#instructions-content')
       puts clean_whitespace(instruction.inner_html)

       flag = true

       break

    end
    if flag
      break
    end
  end
=end

#end

