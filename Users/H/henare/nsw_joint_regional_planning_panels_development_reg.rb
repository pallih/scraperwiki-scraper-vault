require 'mechanize'

def string_to_column_name(text)
  text.strip.downcase.gsub(' ','_').gsub(':','')
end

def get_record_for_id(id)
  agent = Mechanize.new
  url = "http://jrpp.nsw.gov.au/DevelopmentRegister/tabid/62/ctl/view/mid/424/JRPP_ID/#{id}/language/en-AU/Default.aspx"
  page = agent.get url

  result_table = page.at('#dnn_ctr424_ViewPublicMatter_FormView1').at(:table)
  raise "JRPP ID #{id} Not Found" if result_table.nil? 

  # Additional data we want to add to the DB
  record = {
    jrpp_id: id,
    date_scraped: Date.today,
    info_url: url
  }

  # Saves every field in the result detail table
  result_table.search(:tr).each do |r|
    next if r.at(:td).nil? || r.at(:td).attr(:class) == 'Table_Header'
    feild_name = string_to_column_name(r.search(:td)[0].inner_text)

    # JRPP Ref Nos are in HTML input fields so we have to check for that
    if r.search(:td)[1].at(:input).nil? 
      field_value = r.search(:td)[1].inner_text.strip
    else
      field_value = r.search(:td)[1].at(:input).attr(:value)
    end

    # Rename & process fields into what PlanningAlerts expects
    case feild_name
    when 'project_title'
      feild_name = 'description'
    when 'exhibition_finish_date'
      feild_name = 'on_notice_to'
      field_value = Date.parse(field_value)
    when 'exhibition_start_date'
      feild_name = 'on_notice_from'
      field_value = Date.parse(field_value)
    when 'jrpp_ref_no'
      feild_name = 'council_reference'
    when 'property_address'
      feild_name = 'address'
    when 'date_da_lodged_to_council'
      feild_name = 'date_received'
      field_value = Date.parse(field_value)
    end

    record[feild_name] = field_value
  end
  record
end

jrpp_id = (ScraperWiki::get_var(:starting_id).nil? ? 1 : ScraperWiki::get_var(:starting_id))
first_failure_id = nil
failure_count = 0

while true do
  begin
    ScraperWiki::save_var :starting_id, jrpp_id
    ScraperWiki::save_sqlite [:jrpp_id], get_record_for_id(jrpp_id)

    # If we've got this far the last ID successfully saved
    jrpp_id += 1
    first_failure_id = nil
    failure_count = 0
  rescue RuntimeError => e
    puts e.message

    # Set the first ID we failed on so we can rewind
    first_failure_id = jrpp_id if first_failure_id.nil? 

    # There's probably no new applications
    if failure_count > 15
      ScraperWiki::save_var :starting_id, first_failure_id
      break
    end

    failure_count += 1
    jrpp_id += 1
    retry
  end
end
require 'mechanize'

def string_to_column_name(text)
  text.strip.downcase.gsub(' ','_').gsub(':','')
end

def get_record_for_id(id)
  agent = Mechanize.new
  url = "http://jrpp.nsw.gov.au/DevelopmentRegister/tabid/62/ctl/view/mid/424/JRPP_ID/#{id}/language/en-AU/Default.aspx"
  page = agent.get url

  result_table = page.at('#dnn_ctr424_ViewPublicMatter_FormView1').at(:table)
  raise "JRPP ID #{id} Not Found" if result_table.nil? 

  # Additional data we want to add to the DB
  record = {
    jrpp_id: id,
    date_scraped: Date.today,
    info_url: url
  }

  # Saves every field in the result detail table
  result_table.search(:tr).each do |r|
    next if r.at(:td).nil? || r.at(:td).attr(:class) == 'Table_Header'
    feild_name = string_to_column_name(r.search(:td)[0].inner_text)

    # JRPP Ref Nos are in HTML input fields so we have to check for that
    if r.search(:td)[1].at(:input).nil? 
      field_value = r.search(:td)[1].inner_text.strip
    else
      field_value = r.search(:td)[1].at(:input).attr(:value)
    end

    # Rename & process fields into what PlanningAlerts expects
    case feild_name
    when 'project_title'
      feild_name = 'description'
    when 'exhibition_finish_date'
      feild_name = 'on_notice_to'
      field_value = Date.parse(field_value)
    when 'exhibition_start_date'
      feild_name = 'on_notice_from'
      field_value = Date.parse(field_value)
    when 'jrpp_ref_no'
      feild_name = 'council_reference'
    when 'property_address'
      feild_name = 'address'
    when 'date_da_lodged_to_council'
      feild_name = 'date_received'
      field_value = Date.parse(field_value)
    end

    record[feild_name] = field_value
  end
  record
end

jrpp_id = (ScraperWiki::get_var(:starting_id).nil? ? 1 : ScraperWiki::get_var(:starting_id))
first_failure_id = nil
failure_count = 0

while true do
  begin
    ScraperWiki::save_var :starting_id, jrpp_id
    ScraperWiki::save_sqlite [:jrpp_id], get_record_for_id(jrpp_id)

    # If we've got this far the last ID successfully saved
    jrpp_id += 1
    first_failure_id = nil
    failure_count = 0
  rescue RuntimeError => e
    puts e.message

    # Set the first ID we failed on so we can rewind
    first_failure_id = jrpp_id if first_failure_id.nil? 

    # There's probably no new applications
    if failure_count > 15
      ScraperWiki::save_var :starting_id, first_failure_id
      break
    end

    failure_count += 1
    jrpp_id += 1
    retry
  end
end
require 'mechanize'

def string_to_column_name(text)
  text.strip.downcase.gsub(' ','_').gsub(':','')
end

def get_record_for_id(id)
  agent = Mechanize.new
  url = "http://jrpp.nsw.gov.au/DevelopmentRegister/tabid/62/ctl/view/mid/424/JRPP_ID/#{id}/language/en-AU/Default.aspx"
  page = agent.get url

  result_table = page.at('#dnn_ctr424_ViewPublicMatter_FormView1').at(:table)
  raise "JRPP ID #{id} Not Found" if result_table.nil? 

  # Additional data we want to add to the DB
  record = {
    jrpp_id: id,
    date_scraped: Date.today,
    info_url: url
  }

  # Saves every field in the result detail table
  result_table.search(:tr).each do |r|
    next if r.at(:td).nil? || r.at(:td).attr(:class) == 'Table_Header'
    feild_name = string_to_column_name(r.search(:td)[0].inner_text)

    # JRPP Ref Nos are in HTML input fields so we have to check for that
    if r.search(:td)[1].at(:input).nil? 
      field_value = r.search(:td)[1].inner_text.strip
    else
      field_value = r.search(:td)[1].at(:input).attr(:value)
    end

    # Rename & process fields into what PlanningAlerts expects
    case feild_name
    when 'project_title'
      feild_name = 'description'
    when 'exhibition_finish_date'
      feild_name = 'on_notice_to'
      field_value = Date.parse(field_value)
    when 'exhibition_start_date'
      feild_name = 'on_notice_from'
      field_value = Date.parse(field_value)
    when 'jrpp_ref_no'
      feild_name = 'council_reference'
    when 'property_address'
      feild_name = 'address'
    when 'date_da_lodged_to_council'
      feild_name = 'date_received'
      field_value = Date.parse(field_value)
    end

    record[feild_name] = field_value
  end
  record
end

jrpp_id = (ScraperWiki::get_var(:starting_id).nil? ? 1 : ScraperWiki::get_var(:starting_id))
first_failure_id = nil
failure_count = 0

while true do
  begin
    ScraperWiki::save_var :starting_id, jrpp_id
    ScraperWiki::save_sqlite [:jrpp_id], get_record_for_id(jrpp_id)

    # If we've got this far the last ID successfully saved
    jrpp_id += 1
    first_failure_id = nil
    failure_count = 0
  rescue RuntimeError => e
    puts e.message

    # Set the first ID we failed on so we can rewind
    first_failure_id = jrpp_id if first_failure_id.nil? 

    # There's probably no new applications
    if failure_count > 15
      ScraperWiki::save_var :starting_id, first_failure_id
      break
    end

    failure_count += 1
    jrpp_id += 1
    retry
  end
end
require 'mechanize'

def string_to_column_name(text)
  text.strip.downcase.gsub(' ','_').gsub(':','')
end

def get_record_for_id(id)
  agent = Mechanize.new
  url = "http://jrpp.nsw.gov.au/DevelopmentRegister/tabid/62/ctl/view/mid/424/JRPP_ID/#{id}/language/en-AU/Default.aspx"
  page = agent.get url

  result_table = page.at('#dnn_ctr424_ViewPublicMatter_FormView1').at(:table)
  raise "JRPP ID #{id} Not Found" if result_table.nil? 

  # Additional data we want to add to the DB
  record = {
    jrpp_id: id,
    date_scraped: Date.today,
    info_url: url
  }

  # Saves every field in the result detail table
  result_table.search(:tr).each do |r|
    next if r.at(:td).nil? || r.at(:td).attr(:class) == 'Table_Header'
    feild_name = string_to_column_name(r.search(:td)[0].inner_text)

    # JRPP Ref Nos are in HTML input fields so we have to check for that
    if r.search(:td)[1].at(:input).nil? 
      field_value = r.search(:td)[1].inner_text.strip
    else
      field_value = r.search(:td)[1].at(:input).attr(:value)
    end

    # Rename & process fields into what PlanningAlerts expects
    case feild_name
    when 'project_title'
      feild_name = 'description'
    when 'exhibition_finish_date'
      feild_name = 'on_notice_to'
      field_value = Date.parse(field_value)
    when 'exhibition_start_date'
      feild_name = 'on_notice_from'
      field_value = Date.parse(field_value)
    when 'jrpp_ref_no'
      feild_name = 'council_reference'
    when 'property_address'
      feild_name = 'address'
    when 'date_da_lodged_to_council'
      feild_name = 'date_received'
      field_value = Date.parse(field_value)
    end

    record[feild_name] = field_value
  end
  record
end

jrpp_id = (ScraperWiki::get_var(:starting_id).nil? ? 1 : ScraperWiki::get_var(:starting_id))
first_failure_id = nil
failure_count = 0

while true do
  begin
    ScraperWiki::save_var :starting_id, jrpp_id
    ScraperWiki::save_sqlite [:jrpp_id], get_record_for_id(jrpp_id)

    # If we've got this far the last ID successfully saved
    jrpp_id += 1
    first_failure_id = nil
    failure_count = 0
  rescue RuntimeError => e
    puts e.message

    # Set the first ID we failed on so we can rewind
    first_failure_id = jrpp_id if first_failure_id.nil? 

    # There's probably no new applications
    if failure_count > 15
      ScraperWiki::save_var :starting_id, first_failure_id
      break
    end

    failure_count += 1
    jrpp_id += 1
    retry
  end
end
