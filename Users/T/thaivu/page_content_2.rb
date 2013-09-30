require 'rubygems'
require 'mechanize'
require 'active_support'

STARTING_URL = 'https://eservices.greatershepparton.com.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx'
COMMENT_URL_PREFIX = 'mailto:council@shepparton.vic.gov.au?subject='
PERIOD_DATE = 15.days


def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def go_to_development_application_page(page)
  #Planning Application Enquiry
  page = page.forms.first.click_button(page.forms.first.button_with(:id => "ctl00_MainBodyContent_mContinueButton"))
  page.forms.first.field_with(:id => "ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl04_mFromDatePicker_dateTextBox").value = "01/01/1997"
  page.forms.first.field_with(:id => "ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl04_mToDatePicker_dateTextBox").value = Time.now.strftime('%d/%m/%Y').to_s
  page = page.forms.first.click_button(page.forms.first.button_with(:value => "Search"))
  
  return page
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

#Planning Application Enquiry
page = @agent.get(STARTING_URL)
#Check plan_page radio_button
b_radio_value = page.form.radiobutton_with(:value => "ctl00$MainBodyContent$mDataList$ctl00$mDataGrid$ctl02$ctl00").check
#Go to plan application page
page = go_to_development_application_page(page)

def get_table_by_row(table)
  info = []
  
  list_tr = table.search('tr')
  if(list_tr.size > 0)
    list_tr.each do |tr|
      info_obj = {}
      list_td = tr.search('td')
      if(list_td.size > 1)
        info_obj[:key] = clean_whitespace(list_td[0].inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
        info_obj[:value] = clean_whitespace(list_td[1].inner_text)
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


def get_all_info_table(table)
  info = []

  list_td = table.search('td')  
  if(list_td.size > 0)
    list_td.each do |td|
      info << clean_whitespace(td.inner_text)
    end
  end

  return info
end

def get_content_link(table)
  src = ""
  
  iframe = table.search('iframe')
  if(iframe.size > 0)
    iframe = iframe[0]
    if(!iframe['src'].nil?)
      src = iframe['src']
    end
  end

  return src
end

def get_content_from_div(div)
  searched_a = div.search('a')
  if(searched_a.size > 0)
    content = []
    searched_a.each do |a|
      href = a['href']
      if(href.include?("mailto"))
        content << href
      elsif(href.include?("../"))
        content << DOCUMENT_PREFIX_URL + href.gsub("../","")
      else
        content << href
      end
    end
  else
    content = clean_whitespace(div.inner_html).gsub("<br>"," ").gsub("<i>","").gsub("</i>","").gsub("<b>","").gsub("</b>","")
  end

  return content
end

def get_content_from_table(table, count_tr)
  info = []

  list_tr = table.search('tr')
  if(list_tr.size > 4)
    list_key = []
    if(list_tr[1].search('th').size > 0)
      list_key_row = list_tr[1].search('th')
    else
      list_key_row = list_tr[1].search('td')
    end

    list_key_row.each do |item|
      list_key << clean_whitespace(item.inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
    end
     
    count = 3
    while count < list_tr.size-1
      list_td = list_tr[count].search('td')
      info_obj = {}
      for j in 0..list_key.length-1
        info_obj[list_key[j]] = ""
      end
      for j in 0..list_td.length-1
        info_obj[list_key[j]] = clean_whitespace(list_td[j].inner_text)
      end
      info << info_obj
      count += 2
    end
    
    count_tr += list_tr.size

    return info, count_tr
  end
  
  if(list_tr.size == 1)
    tr = list_tr[0]
    list_td = tr.search('td')
    if(list_td.size > 0)
      td = list_td[0]
      info = clean_whitespace(td.inner_html).gsub("<br>"," ").gsub("<i>","").gsub("</i>","").gsub("<b>","").gsub("</b>","")
      count_tr += 1
    end
  end

  if(list_tr.size > 1)
    info = get_table_content(table)
    count_tr += list_tr.size
  end

  return info, count_tr
end

def get_planning_type_table(table)
  info = []

  list_tr = table.search('tr')
  if(list_tr.size > 1)
    count = 0
    while count < list_tr.size-1
      info_obj = {}
      list_key_td = list_tr[count].search('td')
      if(list_key_td.size > 1)
        info_obj[:key] = clean_whitespace(list_key_td[1].inner_text).gsub(" ","_").gsub(":","").gsub(".","").gsub("\u00A0","_").downcase
        
        list_info_td = list_tr[count+1].search('td')
        if(list_info_td.size > 1)
          info_td = list_info_td[1]
          searched_table = info_td.search('table')
          if(searched_table.size > 0)
            table = searched_table[0]
            info_obj[:value], count = get_content_from_table(table, count)
          else
            searched_div = info_td.search('div')
            if(searched_div.size > 0)
              div = searched_div[0]
              info_obj[:value] = get_content_from_div(div)
            end
          end
        end
      end
      info << info_obj
      count += 2
    end
  end
  
  return info
end

page.search('table.ContentPanel tr[class$=ContentPanel]').each do |da_container|
  tds = da_container.search('td')
  href = tds[0].at('a')['href']
  detail_page = page.link_with(:href => "#{href}").click

  #puts detail_page.body.to_s
  
  list_table_content = detail_page.search('table.ContentPanel')

=begin
  info = []
  if(list_table_content.size > 0)
    property_details_table = list_table_content[0]
    info = get_table_content(property_details_table)
  end
  puts info
=end

=begin
  info = []
  if(list_table_content.size > 1)
    name_details_table = list_table_content[1]
    info = get_table_content(name_details_table)
  end
  puts info
=end

=begin
  info = []
  if(list_table_content.size > 2)
    application_fees_table = list_table_content[2]
    info = get_table_content(application_fees_table)
  end
  puts info
=end

=begin
  info = []
  if(list_table_content.size > 3)
    application_workflow_tasks_table = list_table_content[3]
    info = get_table_content(application_workflow_tasks_table)
  end
  puts info
=end

=begin
  info = []
  application_details_div = detail_page.search('#ctl00_MainBodyContent_group_66')
  if(!application_details_div.nil?)
    application_details_table = application_details_div.search('table')
    if(application_details_table.size > 2)
      application_details_table = application_details_table[2]
      info = get_table_by_row(application_details_table)
    end
  end  
  puts info
=end

  info = []
  status_details_div = detail_page.search('#ctl00_MainBodyContent_group_47')
  if(!status_details_div.nil?)
    status_details_table = status_details_div.search('table')
    if(status_details_table.size > 2)
      status_details_table = status_details_table[2]
      info = get_table_content(status_details_table)
    end
  end  
  puts info

=begin
  info = []
  container = detail_page.search('div.list')
  if(container.size > 0)
    container = container[0]
    table = container.search('table')
    if(table.size > 0)
      table = table[0]

      info = get_planning_type_table(table)
    end
  end
  puts info
=end


=begin
  info = []
  element = detail_page.search('#ctl00_MainBodyContent_group_66')
  if(!element.nil? )
    list_table = element.search('table')
    if(list_table.size > 2)
      table = list_table[2]
      info = get_table_by_row(table)
    end
  end
  puts info
=end


=begin
  table = detail_page.search('table.ContentPanel')
  if(table.size > 0)
    table_obj = table[0]
    info = get_table_content(table_obj)
  end
  
  puts info

  if(table.size > 1)
    table_obj = table[1]
    info = get_table_content(table_obj)
  end
  
  puts info

  content = detail_page.search('#ctl00_MainBodyContent_group_16')
  if(!content.nil?)
    list_table = content.search('table')
    if(list_table.size > 2)
      web_links_table = list_table[2]
      info = get_all_info_table(web_links_table)
    end
  end

  puts info

  content = detail_page.search('#ctl00_MainBodyContent_group_19')
  if(!content.nil?)
    list_table = content.search('table')
    if(list_table.size > 2)
      google_links_table = list_table[2]
      info = get_content_link(google_links_table)
    end
  end

  puts info
=end

=begin   
  first_table = detail_page.search('table.ContentPanel')[0]
  list_tr = first_table.search('tr')
  role_array = []
  for i in 1..list_tr.length-1
    list_td = list_tr[i].search('td')
    role_obj = {}
    role_obj[:role_type] = clean_whitespace(list_td[0].inner_text)
    role_obj[:name] = clean_whitespace(list_td[1].inner_text)
    role_obj[:address] = clean_whitespace(list_td[2].inner_text)

    role_array << role_obj
  end

  info_group_panel = detail_page.search('.GroupContentPanel')[2]
  info_group_table = info_group_panel.search('table')[2]
  info_group_tr = info_group_table.search('tr')
  puts info_group_tr
  info_group_info = []
  info_group_tr.each do |tr|
    info_group_td = tr.search('td')
    if (info_group_td.size > 0)
      info_group_obj = {}
      info_group_obj[:key] = clean_whitespace(info_group_td[0].inner_text).downcase
      info_group_obj[:field] = clean_whitespace(info_group_td[1].inner_text).downcase
  
      info_group_info << info_group_obj
    end
  end
  puts info_group_info

  address_panel = detail_page.search('.GroupContentPanel')[3]
  address_table = address_panel.search('table')[2]
  address_table = address_table.search('table')[0]
  address_tr = address_table.search('tr')
  address_key = []
  first_address_th = address_tr[0].search('th')
  first_address_th.each do |item|
    address_key << clean_whitespace(item.inner_text).gsub(" ","_").downcase
  end

  address_info = []
  address_td = address_tr[1].search('td')
  for i in 0..address_td.length-1
    address_obj =
    address_info[address_key[i]] = clean_whitespace(address_td[i].inner_text)
  end
  puts address_info

  fee_status_tr = detail_page.search('.ContentPanelHeading')[4]
  puts clean_whitespace(fee_status_tr.search('td')[0].inner_text)
=end

  break
endrequire 'rubygems'
require 'mechanize'
require 'active_support'

STARTING_URL = 'https://eservices.greatershepparton.com.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx'
COMMENT_URL_PREFIX = 'mailto:council@shepparton.vic.gov.au?subject='
PERIOD_DATE = 15.days


def clean_whitespace(a)
  a.gsub("\r", ' ').gsub("\n", ' ').squeeze(" ").strip
end

def go_to_development_application_page(page)
  #Planning Application Enquiry
  page = page.forms.first.click_button(page.forms.first.button_with(:id => "ctl00_MainBodyContent_mContinueButton"))
  page.forms.first.field_with(:id => "ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl04_mFromDatePicker_dateTextBox").value = "01/01/1997"
  page.forms.first.field_with(:id => "ctl00_MainBodyContent_mGeneralEnquirySearchControl_mTabControl_ctl04_mToDatePicker_dateTextBox").value = Time.now.strftime('%d/%m/%Y').to_s
  page = page.forms.first.click_button(page.forms.first.button_with(:value => "Search"))
  
  return page
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

#Planning Application Enquiry
page = @agent.get(STARTING_URL)
#Check plan_page radio_button
b_radio_value = page.form.radiobutton_with(:value => "ctl00$MainBodyContent$mDataList$ctl00$mDataGrid$ctl02$ctl00").check
#Go to plan application page
page = go_to_development_application_page(page)

def get_table_by_row(table)
  info = []
  
  list_tr = table.search('tr')
  if(list_tr.size > 0)
    list_tr.each do |tr|
      info_obj = {}
      list_td = tr.search('td')
      if(list_td.size > 1)
        info_obj[:key] = clean_whitespace(list_td[0].inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
        info_obj[:value] = clean_whitespace(list_td[1].inner_text)
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


def get_all_info_table(table)
  info = []

  list_td = table.search('td')  
  if(list_td.size > 0)
    list_td.each do |td|
      info << clean_whitespace(td.inner_text)
    end
  end

  return info
end

def get_content_link(table)
  src = ""
  
  iframe = table.search('iframe')
  if(iframe.size > 0)
    iframe = iframe[0]
    if(!iframe['src'].nil?)
      src = iframe['src']
    end
  end

  return src
end

def get_content_from_div(div)
  searched_a = div.search('a')
  if(searched_a.size > 0)
    content = []
    searched_a.each do |a|
      href = a['href']
      if(href.include?("mailto"))
        content << href
      elsif(href.include?("../"))
        content << DOCUMENT_PREFIX_URL + href.gsub("../","")
      else
        content << href
      end
    end
  else
    content = clean_whitespace(div.inner_html).gsub("<br>"," ").gsub("<i>","").gsub("</i>","").gsub("<b>","").gsub("</b>","")
  end

  return content
end

def get_content_from_table(table, count_tr)
  info = []

  list_tr = table.search('tr')
  if(list_tr.size > 4)
    list_key = []
    if(list_tr[1].search('th').size > 0)
      list_key_row = list_tr[1].search('th')
    else
      list_key_row = list_tr[1].search('td')
    end

    list_key_row.each do |item|
      list_key << clean_whitespace(item.inner_text).gsub(" ","_").gsub(":","").gsub(".","").downcase
    end
     
    count = 3
    while count < list_tr.size-1
      list_td = list_tr[count].search('td')
      info_obj = {}
      for j in 0..list_key.length-1
        info_obj[list_key[j]] = ""
      end
      for j in 0..list_td.length-1
        info_obj[list_key[j]] = clean_whitespace(list_td[j].inner_text)
      end
      info << info_obj
      count += 2
    end
    
    count_tr += list_tr.size

    return info, count_tr
  end
  
  if(list_tr.size == 1)
    tr = list_tr[0]
    list_td = tr.search('td')
    if(list_td.size > 0)
      td = list_td[0]
      info = clean_whitespace(td.inner_html).gsub("<br>"," ").gsub("<i>","").gsub("</i>","").gsub("<b>","").gsub("</b>","")
      count_tr += 1
    end
  end

  if(list_tr.size > 1)
    info = get_table_content(table)
    count_tr += list_tr.size
  end

  return info, count_tr
end

def get_planning_type_table(table)
  info = []

  list_tr = table.search('tr')
  if(list_tr.size > 1)
    count = 0
    while count < list_tr.size-1
      info_obj = {}
      list_key_td = list_tr[count].search('td')
      if(list_key_td.size > 1)
        info_obj[:key] = clean_whitespace(list_key_td[1].inner_text).gsub(" ","_").gsub(":","").gsub(".","").gsub("\u00A0","_").downcase
        
        list_info_td = list_tr[count+1].search('td')
        if(list_info_td.size > 1)
          info_td = list_info_td[1]
          searched_table = info_td.search('table')
          if(searched_table.size > 0)
            table = searched_table[0]
            info_obj[:value], count = get_content_from_table(table, count)
          else
            searched_div = info_td.search('div')
            if(searched_div.size > 0)
              div = searched_div[0]
              info_obj[:value] = get_content_from_div(div)
            end
          end
        end
      end
      info << info_obj
      count += 2
    end
  end
  
  return info
end

page.search('table.ContentPanel tr[class$=ContentPanel]').each do |da_container|
  tds = da_container.search('td')
  href = tds[0].at('a')['href']
  detail_page = page.link_with(:href => "#{href}").click

  #puts detail_page.body.to_s
  
  list_table_content = detail_page.search('table.ContentPanel')

=begin
  info = []
  if(list_table_content.size > 0)
    property_details_table = list_table_content[0]
    info = get_table_content(property_details_table)
  end
  puts info
=end

=begin
  info = []
  if(list_table_content.size > 1)
    name_details_table = list_table_content[1]
    info = get_table_content(name_details_table)
  end
  puts info
=end

=begin
  info = []
  if(list_table_content.size > 2)
    application_fees_table = list_table_content[2]
    info = get_table_content(application_fees_table)
  end
  puts info
=end

=begin
  info = []
  if(list_table_content.size > 3)
    application_workflow_tasks_table = list_table_content[3]
    info = get_table_content(application_workflow_tasks_table)
  end
  puts info
=end

=begin
  info = []
  application_details_div = detail_page.search('#ctl00_MainBodyContent_group_66')
  if(!application_details_div.nil?)
    application_details_table = application_details_div.search('table')
    if(application_details_table.size > 2)
      application_details_table = application_details_table[2]
      info = get_table_by_row(application_details_table)
    end
  end  
  puts info
=end

  info = []
  status_details_div = detail_page.search('#ctl00_MainBodyContent_group_47')
  if(!status_details_div.nil?)
    status_details_table = status_details_div.search('table')
    if(status_details_table.size > 2)
      status_details_table = status_details_table[2]
      info = get_table_content(status_details_table)
    end
  end  
  puts info

=begin
  info = []
  container = detail_page.search('div.list')
  if(container.size > 0)
    container = container[0]
    table = container.search('table')
    if(table.size > 0)
      table = table[0]

      info = get_planning_type_table(table)
    end
  end
  puts info
=end


=begin
  info = []
  element = detail_page.search('#ctl00_MainBodyContent_group_66')
  if(!element.nil? )
    list_table = element.search('table')
    if(list_table.size > 2)
      table = list_table[2]
      info = get_table_by_row(table)
    end
  end
  puts info
=end


=begin
  table = detail_page.search('table.ContentPanel')
  if(table.size > 0)
    table_obj = table[0]
    info = get_table_content(table_obj)
  end
  
  puts info

  if(table.size > 1)
    table_obj = table[1]
    info = get_table_content(table_obj)
  end
  
  puts info

  content = detail_page.search('#ctl00_MainBodyContent_group_16')
  if(!content.nil?)
    list_table = content.search('table')
    if(list_table.size > 2)
      web_links_table = list_table[2]
      info = get_all_info_table(web_links_table)
    end
  end

  puts info

  content = detail_page.search('#ctl00_MainBodyContent_group_19')
  if(!content.nil?)
    list_table = content.search('table')
    if(list_table.size > 2)
      google_links_table = list_table[2]
      info = get_content_link(google_links_table)
    end
  end

  puts info
=end

=begin   
  first_table = detail_page.search('table.ContentPanel')[0]
  list_tr = first_table.search('tr')
  role_array = []
  for i in 1..list_tr.length-1
    list_td = list_tr[i].search('td')
    role_obj = {}
    role_obj[:role_type] = clean_whitespace(list_td[0].inner_text)
    role_obj[:name] = clean_whitespace(list_td[1].inner_text)
    role_obj[:address] = clean_whitespace(list_td[2].inner_text)

    role_array << role_obj
  end

  info_group_panel = detail_page.search('.GroupContentPanel')[2]
  info_group_table = info_group_panel.search('table')[2]
  info_group_tr = info_group_table.search('tr')
  puts info_group_tr
  info_group_info = []
  info_group_tr.each do |tr|
    info_group_td = tr.search('td')
    if (info_group_td.size > 0)
      info_group_obj = {}
      info_group_obj[:key] = clean_whitespace(info_group_td[0].inner_text).downcase
      info_group_obj[:field] = clean_whitespace(info_group_td[1].inner_text).downcase
  
      info_group_info << info_group_obj
    end
  end
  puts info_group_info

  address_panel = detail_page.search('.GroupContentPanel')[3]
  address_table = address_panel.search('table')[2]
  address_table = address_table.search('table')[0]
  address_tr = address_table.search('tr')
  address_key = []
  first_address_th = address_tr[0].search('th')
  first_address_th.each do |item|
    address_key << clean_whitespace(item.inner_text).gsub(" ","_").downcase
  end

  address_info = []
  address_td = address_tr[1].search('td')
  for i in 0..address_td.length-1
    address_obj =
    address_info[address_key[i]] = clean_whitespace(address_td[i].inner_text)
  end
  puts address_info

  fee_status_tr = detail_page.search('.ContentPanelHeading')[4]
  puts clean_whitespace(fee_status_tr.search('td')[0].inner_text)
=end

  break
end