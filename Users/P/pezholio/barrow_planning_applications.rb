require 'rubygems'
require 'nokogiri'
require 'mechanize'
require 'open-uri'
require 'date'
require 'yaml'

def get_viewstate(url)
  a = Mechanize.new
  a.get(url) do |page|
    doc = Nokogiri.HTML(page.body)
        
    result = {}
    result['viewstate'] = doc.search('#__VIEWSTATE')[0][:value]
    result['eventvalidation'] = doc.search('#__EVENTVALIDATION')[0][:value]
    return result
  end  
end

def get_details(doc, from_date = nil)
  rows = doc.search('#maintextarea table')[2].search('tr')
  rows.shift
  
  rows.each do |row|
    col = row.search('td')
    details = {}
    details['uid'] = col[0].inner_text
    details['url'] = "https://views.scraperwiki.com/run/barrow_planning_redirect/?id=#{details['uid']}"
    rec_date = Date.parse(col[3].inner_text.strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-'))
    if from_date == nil
      ScraperWiki.save(["uid"], details)
    else
      if rec_date >= from_date
        ScraperWiki.save(["uid"], details)
      else
        break
      end
    end
  end
end

def search_for_new_applications
  url = "http://www.barrowbc.gov.uk/papps/search.aspx"
  doc = Nokogiri.HTML(open(url))
    
  from_date = Date.today - 14
  get_details(doc, from_date)
end

def get_all_apps
  url = "http://www.barrowbc.gov.uk/papps/search.aspx"
  states = get_viewstate(url)

  a = Mechanize.new
  a.get(url) do |page|
    doc = Nokogiri.HTML(page.body)
    get_details(doc)
    
    viewstate = doc.search('#__VIEWSTATE')[0][:value]
    eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]
    
    pages = doc.search('#PageCountLabel')[0].inner_text.gsub('/ ', '').to_i
    num = 1
    
    while num < pages
      num += 1
      p = a.post(url, {
        "__EVENTTARGET" => "JumpPage",
        "__VIEWSTATE" => viewstate,
        "__EVENTVALIDATION" => eventvalidation,
        "JumpPage" => num
      })
      doc = Nokogiri.HTML(p.body)
      
      viewstate = doc.search('#__VIEWSTATE')[0][:value]
      eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]    
    
      get_details(doc)
    end
    
  end  
end

def update_stale_applications
  unpopulated_applications = ScraperWiki.select("* from swdata WHERE date_scraped IS NULL LIMIT 100")
  unpopulated_applications.each do |app|
    populate_application_details(app)
  end
  current_applications = ScraperWiki.select("* from swdata WHERE start_date > '#{(Date.today-60).strftime('%F')}' ORDER BY date_scraped LIMIT 500")
  current_applications.each do |app|
    populate_application_details(app)
  end
end

def populate_application_details(app_info)
  url = "http://www.barrowbc.gov.uk/papps/search.aspx"

  ref = app_info['uid']

  a = Mechanize.new
  a.get(url) do |page|
    doc = Nokogiri.HTML(page.body)
    
    viewstate = doc.search('#__VIEWSTATE')[0][:value]
    eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]

    p = a.post(url, {
      "__EVENTTARGET" => "",
      "__EVENTARGUMENT" => "",
      "__LASTFOCUS" => "",
      "__VIEWSTATE" => viewstate,
      "__EVENTVALIDATION" => eventvalidation,
      "txtSearch" => ref,
      "txtSearch2" => "",
      "btnSearch" => "Ref No: Search",
    })
    
    doc = Nokogiri.HTML(p.body)

    viewstate = doc.search('#__VIEWSTATE')[0][:value]
    eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]

    p = a.post(url, {
      "__EVENTTARGET" => "",
      "__EVENTARGUMENT" => "",
      "__LASTFOCUS" => "",
      "__VIEWSTATE" => viewstate,
      "__EVENTVALIDATION" => eventvalidation,
      "txtSearch" => ref,
      "txtSearch2" => "",
      "JumpPage" => "1",
      "myRepeater$ctl01$btnDetails1" => "Details of #{ref}"
    })
    
    doc = Nokogiri.HTML(p.body)
            
    inputs = doc.search('#niceform fieldset .row-div').inject({}){|hsh,div| hsh[div.at('label').inner_text.strip] = div.search('input').attr('value').to_str rescue nil if div.at('input') && div.at('label');hsh}
    
    textareas = doc.search('#niceform fieldset .row-div-big').inject({}){|hsh,div| hsh[div.at('label').inner_text.strip] = div.search('textarea').inner_text if div.at('label') && div.at('textarea');hsh}
    
    details_hash = inputs.merge(textareas)
            
    details = app_info
    details[:address] = details_hash['Site Address'].strip rescue nil
    details[:applicant_address] = details_hash['Applicant Address'].strip rescue nil
    details[:applicant_name] = details_hash['Applicant Name'].strip rescue nil
    details[:start_date] = Date.parse(details_hash['Received Date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) # Required
    details[:date_validated] = Date.parse(details_hash['Valid Date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
    details[:description] = details_hash['Proposal'].strip #required
    details[:reference] = details_hash['Link'].strip rescue nil
    details[:agent_address] = details_hash['Agent Address'].strip rescue nil
    details[:agent_name] = details_hash['Agent Name'].strip rescue nil
    details[:appeal_date] = Date.parse(details_hash['Appeal Lodged'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
    details[:appeal_decision_date] = Date.parse(details_hash['Appeal Decision Date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
    details[:appeal_result] = details_hash['Appeal Decision'].strip rescue nil 
    details[:application_type] = details_hash['Application Type']
    details[:case_officer] = doc.search('#niceform fieldset .row-div a[@href*="caseofficers.aspx"]').inner_text rescue nil
    details[:consultation_start_date] = Date.parse(details_hash['Public Consult Start'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
    details[:consultation_end_date] = Date.parse(details_hash['Public Consult End'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
    details[:decided_by] = details_hash['Committee Type'] rescue nil
    details[:decision] = details_hash['Decision'] rescue nil
    details[:decision_issued_date] = Date.parse(details_hash['Decision Notice Sent Date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
    details[:easting] = details_hash['Eastings'] rescue nil
    details[:northing] = details_hash['Northings'] rescue nil
    details[:meeting_date] = Date.parse(details_hash['Committee Date'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
    details[:parish] = details_hash['Parish'] rescue nil
    details[:target_decision_date] = Date.parse(details_hash['TargetDate'].strip.gsub(/[^\d\/]/,'').split('/').reverse.join('-')) rescue nil
    details[:ward_name] = details_hash['Ward'] rescue nil
        
    details[:date_scraped] = Time.now

    ScraperWiki.save([:uid], details)
            
  end  

  rescue Exception => e
    puts "Exception (#{e.inspect}) raised populating application details (#{app_info.inspect}). Backtrace:\n#{e.backtrace}"
end

search_for_new_applications
update_stale_applications