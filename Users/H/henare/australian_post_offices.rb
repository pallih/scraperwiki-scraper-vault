#Disabled, remove this line when we want to run it again
exit

require 'rubygems'
require 'mechanize'

agent = Mechanize.new
base_url = 'http://apps.nowwhere.com.au/austpost/PostOfficeLocator/default.aspx?cbPO=on&btnSearch.y=0&btnSearch.x=0&__VIEWSTATE=%2FwEPDwULLTEyNTAyMzU0ODUPZBYCAgMPFgIeBm9ubG9hZAURbG9hZEZpbHRlck5hbWVzKCkWAgIDD2QWBgIBDw8WAh4HVmlzaWJsZWdkFgYCAQ8WBB8BaB4Fc3R5bGUFEnZpc2liaWxpdHk6aGlkZGVuO2QCAw8WAh4EVGV4dAV%2FPHAgaWQ9ImVycm9yTXNnIiBjbGFzcz0iZXJyb3IiPlBsZWFzZSBzZWxlY3Qgb25lIG9yIG1vcmUgb2YgdGhlIG9wdGlvbnMgaW4gJ0ZpbmQgYSBQb3N0IE9mZmljZSBvcjxici8%2BIFN0cmVldCBQb3N0aW5nIEJveCcuPC9wPmQCEQ8PFgIfAWhkFgICAw8QZGQUKwEAZAICDw8WAh8BaGQWAgIBDxYEHwFoHwIFEnZpc2liaWxpdHk6aGlkZGVuO2QCBA9kFgICAQ8PFgIfAWhkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBQUEY2JQTwUGY2JSU1BCBQZjYkVTUEIFCWJ0blNlYXJjaAUIYnRuQ2xlYXJxHjoYbP26EYYOmYdc5fLldcCCoQ%3D%3D&txtPostcode='

#Pick up where we left off
postcode_progress = ScraperWiki.get_var('postcode_progress')
exit if postcode_progress > 9999

(800..999).each do |n|
  puts "Getting postcode 0#{n.to_s}"
  page = agent.get(base_url + '0' + n.to_s)
  
  # Skip this if it's an error page
  next if !page.at('#errorMsg').nil? 
  
  page.at('.searchResults').search('tr').each do |r|
    # Skip the header row
    next if r.search('td')[0].nil? 
    
    # This row's corresponding details div
    div_id = r.search('td')[3].at('a').attribute('onclick').value.split(',')[0].gsub('\'','').split('(')[1]
    
    # Some entries have a different amount of tables so we need to accommodate that
    details_tables = page.at('div#' + div_id).search('table')
    if details_tables[1].search('td')[0].inner_text == 'MON'
      base_table_id = 0
    else
      base_table_id = 1
    end
    
    # Lots of "Community Postal Agencies" don't have services
    services_general = ''
    services_business_banking = ''
    services_form_lodgement = ''
    services_travel_money = ''
    services_money_transfer = ''
    details_tables[base_table_id + 2].search('tr').each do |sr|
      case sr.at('th').inner_text
        when'Services available'
          next
        when 'General'
          services_general = sr.at('td').inner_text.strip
        when 'Business Banking'
          services_business_banking = sr.at('td').inner_text.strip
        when 'Application & Form Lodgement'
          services_form_lodgement = sr.at('td').inner_text.strip
        when 'Travel Money Services'
          services_travel_money = sr.at('td').inner_text.strip
        when 'Money Transfer'
          services_money_transfer = sr.at('td').inner_text.strip
      end
    end
    
    post_office = {
      'type' => r.search('td')[2].inner_text,
      'name' => r.search('td')[3].inner_text,
      'address' => r.search('td')[4].inner_text.strip,
      'postcode' => r.search('td')[5].inner_text,
      'long' => r.search('td')[3].at('a').attribute('onclick').value.split(',')[1].gsub('\'',''),
      'lat' => r.search('td')[3].at('a').attribute('onclick').value.split(',')[2].gsub('\'',''),
      'identifier' => details_tables[base_table_id].search('td')[0].inner_text,
      'opening_hours_mon' => details_tables[base_table_id + 1].search('tr')[1].search('td')[0].inner_text,
      'opening_hours_tue' => details_tables[base_table_id + 1].search('tr')[1].search('td')[1].inner_text,
      'opening_hours_wed' => details_tables[base_table_id + 1].search('tr')[1].search('td')[2].inner_text,
      'opening_hours_thur' => details_tables[base_table_id + 1].search('tr')[1].search('td')[3].inner_text,
      'opening_hours_fri' => details_tables[base_table_id + 1].search('tr')[1].search('td')[4].inner_text,
      'opening_hours_sat' => details_tables[base_table_id + 1].search('tr')[1].search('td')[5].inner_text,
      'opening_hours_sun' => details_tables[base_table_id + 1].search('tr')[1].search('td')[6].inner_text,
      'services_general' => services_general,
      'services_business_banking' => services_business_banking,
      'services_form_lodgement' => services_form_lodgement,
      'services_travel_money' => services_travel_money,
      'services_money_transfer' => services_money_transfer
    }
    
    #pp post_office
    ScraperWiki.save_sqlite(['identifier'], post_office)
  end
  ScraperWiki.save_var('postcode_progress', n)
end
#Disabled, remove this line when we want to run it again
exit

require 'rubygems'
require 'mechanize'

agent = Mechanize.new
base_url = 'http://apps.nowwhere.com.au/austpost/PostOfficeLocator/default.aspx?cbPO=on&btnSearch.y=0&btnSearch.x=0&__VIEWSTATE=%2FwEPDwULLTEyNTAyMzU0ODUPZBYCAgMPFgIeBm9ubG9hZAURbG9hZEZpbHRlck5hbWVzKCkWAgIDD2QWBgIBDw8WAh4HVmlzaWJsZWdkFgYCAQ8WBB8BaB4Fc3R5bGUFEnZpc2liaWxpdHk6aGlkZGVuO2QCAw8WAh4EVGV4dAV%2FPHAgaWQ9ImVycm9yTXNnIiBjbGFzcz0iZXJyb3IiPlBsZWFzZSBzZWxlY3Qgb25lIG9yIG1vcmUgb2YgdGhlIG9wdGlvbnMgaW4gJ0ZpbmQgYSBQb3N0IE9mZmljZSBvcjxici8%2BIFN0cmVldCBQb3N0aW5nIEJveCcuPC9wPmQCEQ8PFgIfAWhkFgICAw8QZGQUKwEAZAICDw8WAh8BaGQWAgIBDxYEHwFoHwIFEnZpc2liaWxpdHk6aGlkZGVuO2QCBA9kFgICAQ8PFgIfAWhkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WBQUEY2JQTwUGY2JSU1BCBQZjYkVTUEIFCWJ0blNlYXJjaAUIYnRuQ2xlYXJxHjoYbP26EYYOmYdc5fLldcCCoQ%3D%3D&txtPostcode='

#Pick up where we left off
postcode_progress = ScraperWiki.get_var('postcode_progress')
exit if postcode_progress > 9999

(800..999).each do |n|
  puts "Getting postcode 0#{n.to_s}"
  page = agent.get(base_url + '0' + n.to_s)
  
  # Skip this if it's an error page
  next if !page.at('#errorMsg').nil? 
  
  page.at('.searchResults').search('tr').each do |r|
    # Skip the header row
    next if r.search('td')[0].nil? 
    
    # This row's corresponding details div
    div_id = r.search('td')[3].at('a').attribute('onclick').value.split(',')[0].gsub('\'','').split('(')[1]
    
    # Some entries have a different amount of tables so we need to accommodate that
    details_tables = page.at('div#' + div_id).search('table')
    if details_tables[1].search('td')[0].inner_text == 'MON'
      base_table_id = 0
    else
      base_table_id = 1
    end
    
    # Lots of "Community Postal Agencies" don't have services
    services_general = ''
    services_business_banking = ''
    services_form_lodgement = ''
    services_travel_money = ''
    services_money_transfer = ''
    details_tables[base_table_id + 2].search('tr').each do |sr|
      case sr.at('th').inner_text
        when'Services available'
          next
        when 'General'
          services_general = sr.at('td').inner_text.strip
        when 'Business Banking'
          services_business_banking = sr.at('td').inner_text.strip
        when 'Application & Form Lodgement'
          services_form_lodgement = sr.at('td').inner_text.strip
        when 'Travel Money Services'
          services_travel_money = sr.at('td').inner_text.strip
        when 'Money Transfer'
          services_money_transfer = sr.at('td').inner_text.strip
      end
    end
    
    post_office = {
      'type' => r.search('td')[2].inner_text,
      'name' => r.search('td')[3].inner_text,
      'address' => r.search('td')[4].inner_text.strip,
      'postcode' => r.search('td')[5].inner_text,
      'long' => r.search('td')[3].at('a').attribute('onclick').value.split(',')[1].gsub('\'',''),
      'lat' => r.search('td')[3].at('a').attribute('onclick').value.split(',')[2].gsub('\'',''),
      'identifier' => details_tables[base_table_id].search('td')[0].inner_text,
      'opening_hours_mon' => details_tables[base_table_id + 1].search('tr')[1].search('td')[0].inner_text,
      'opening_hours_tue' => details_tables[base_table_id + 1].search('tr')[1].search('td')[1].inner_text,
      'opening_hours_wed' => details_tables[base_table_id + 1].search('tr')[1].search('td')[2].inner_text,
      'opening_hours_thur' => details_tables[base_table_id + 1].search('tr')[1].search('td')[3].inner_text,
      'opening_hours_fri' => details_tables[base_table_id + 1].search('tr')[1].search('td')[4].inner_text,
      'opening_hours_sat' => details_tables[base_table_id + 1].search('tr')[1].search('td')[5].inner_text,
      'opening_hours_sun' => details_tables[base_table_id + 1].search('tr')[1].search('td')[6].inner_text,
      'services_general' => services_general,
      'services_business_banking' => services_business_banking,
      'services_form_lodgement' => services_form_lodgement,
      'services_travel_money' => services_travel_money,
      'services_money_transfer' => services_money_transfer
    }
    
    #pp post_office
    ScraperWiki.save_sqlite(['identifier'], post_office)
  end
  ScraperWiki.save_var('postcode_progress', n)
end
