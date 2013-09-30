require 'scraperwiki'
require 'mechanize'

agent = Mechanize.new
base_url = 'http://lobbyists.pmc.gov.au/'
table = agent.get("#{base_url}who_register.cfm").at(:table)

agencies = table.at(:tbody).search(:tr).map do |row|
  {url: base_url + row.search(:td)[1].at(:a).attr(:href),
   business_entity_name: row.search(:td)[1].inner_text,
   trading_name: row.search(:td)[2].inner_text,
   abn: row.search(:td)[3].inner_text,
   details_last_updated: Date.parse(row.search(:td)[4].inner_text)}
end

agencies.each do |agency|
  agency_id = agency[:url].match('id=(.*)')[1]

  if !ScraperWiki.select("* FROM agencies WHERE `abn`='#{agency[:abn]}' AND `details_last_updated`='#{agency[:details_last_updated]}'").empty? 
    puts "Skipping existing record agency ID #{agency_id}"
    next
  end

  agency_page = agent.get agency[:url]
  
  agency_details = {
    id: agency_id,
    url: agency[:url],
    business_entity_name: agency[:business_entity_name],
    trading_name: agency[:trading_name],
    abn: agency[:abn],
    details_last_updated: agency[:details_last_updated],
    date_scraped: Date.today
  }

  ScraperWiki.save_sqlite([:id], agency_details, 'agencies')

  # Save owners
  owners = agency_page.at('#profile').search(:ul).last.search(:li).map do |li|
    {agency_id: agency_id,
     agency_business_entity_name: agency[:business_entity_name],
     owner_name: li.inner_text}
  end

  ScraperWiki.save_sqlite([:agency_id, :owner_name], owners, 'owners')

  # Save lobbyists
  if agency_page.at('#lobbyistDetails')
    lobbyists = agency_page.at('#lobbyistDetails').at(:tbody).search(:tr).map do |row|
      {agency_id: agency_id,
       agency_business_entity_name: agency[:business_entity_name],
       lobbyist_name: row.search(:td)[1].inner_text,
       position: row.search(:td)[2].inner_text,
       former_government_representative: row.search(:td)[3].inner_text,
       cessation_date: row.search(:td)[4].inner_text.strip}
    end

    ScraperWiki.save_sqlite([:agency_id, :lobbyist_name], lobbyists, 'lobbyists')
  end

  # Save clients
  if agency_page.at('#clientDetails')
    clients = agency_page.at('#clientDetails').at(:tbody).search(:tr).map do |row|
      {agency_id: agency_id,
       agency_business_entity_name: agency[:business_entity_name],
       client_name: row.search(:td)[1].inner_text}
    end

    ScraperWiki.save_sqlite([:agency_id, :client_name], clients, 'clients')
  end
end
require 'scraperwiki'
require 'mechanize'

agent = Mechanize.new
base_url = 'http://lobbyists.pmc.gov.au/'
table = agent.get("#{base_url}who_register.cfm").at(:table)

agencies = table.at(:tbody).search(:tr).map do |row|
  {url: base_url + row.search(:td)[1].at(:a).attr(:href),
   business_entity_name: row.search(:td)[1].inner_text,
   trading_name: row.search(:td)[2].inner_text,
   abn: row.search(:td)[3].inner_text,
   details_last_updated: Date.parse(row.search(:td)[4].inner_text)}
end

agencies.each do |agency|
  agency_id = agency[:url].match('id=(.*)')[1]

  if !ScraperWiki.select("* FROM agencies WHERE `abn`='#{agency[:abn]}' AND `details_last_updated`='#{agency[:details_last_updated]}'").empty? 
    puts "Skipping existing record agency ID #{agency_id}"
    next
  end

  agency_page = agent.get agency[:url]
  
  agency_details = {
    id: agency_id,
    url: agency[:url],
    business_entity_name: agency[:business_entity_name],
    trading_name: agency[:trading_name],
    abn: agency[:abn],
    details_last_updated: agency[:details_last_updated],
    date_scraped: Date.today
  }

  ScraperWiki.save_sqlite([:id], agency_details, 'agencies')

  # Save owners
  owners = agency_page.at('#profile').search(:ul).last.search(:li).map do |li|
    {agency_id: agency_id,
     agency_business_entity_name: agency[:business_entity_name],
     owner_name: li.inner_text}
  end

  ScraperWiki.save_sqlite([:agency_id, :owner_name], owners, 'owners')

  # Save lobbyists
  if agency_page.at('#lobbyistDetails')
    lobbyists = agency_page.at('#lobbyistDetails').at(:tbody).search(:tr).map do |row|
      {agency_id: agency_id,
       agency_business_entity_name: agency[:business_entity_name],
       lobbyist_name: row.search(:td)[1].inner_text,
       position: row.search(:td)[2].inner_text,
       former_government_representative: row.search(:td)[3].inner_text,
       cessation_date: row.search(:td)[4].inner_text.strip}
    end

    ScraperWiki.save_sqlite([:agency_id, :lobbyist_name], lobbyists, 'lobbyists')
  end

  # Save clients
  if agency_page.at('#clientDetails')
    clients = agency_page.at('#clientDetails').at(:tbody).search(:tr).map do |row|
      {agency_id: agency_id,
       agency_business_entity_name: agency[:business_entity_name],
       client_name: row.search(:td)[1].inner_text}
    end

    ScraperWiki.save_sqlite([:agency_id, :client_name], clients, 'clients')
  end
end
require 'scraperwiki'
require 'mechanize'

agent = Mechanize.new
base_url = 'http://lobbyists.pmc.gov.au/'
table = agent.get("#{base_url}who_register.cfm").at(:table)

agencies = table.at(:tbody).search(:tr).map do |row|
  {url: base_url + row.search(:td)[1].at(:a).attr(:href),
   business_entity_name: row.search(:td)[1].inner_text,
   trading_name: row.search(:td)[2].inner_text,
   abn: row.search(:td)[3].inner_text,
   details_last_updated: Date.parse(row.search(:td)[4].inner_text)}
end

agencies.each do |agency|
  agency_id = agency[:url].match('id=(.*)')[1]

  if !ScraperWiki.select("* FROM agencies WHERE `abn`='#{agency[:abn]}' AND `details_last_updated`='#{agency[:details_last_updated]}'").empty? 
    puts "Skipping existing record agency ID #{agency_id}"
    next
  end

  agency_page = agent.get agency[:url]
  
  agency_details = {
    id: agency_id,
    url: agency[:url],
    business_entity_name: agency[:business_entity_name],
    trading_name: agency[:trading_name],
    abn: agency[:abn],
    details_last_updated: agency[:details_last_updated],
    date_scraped: Date.today
  }

  ScraperWiki.save_sqlite([:id], agency_details, 'agencies')

  # Save owners
  owners = agency_page.at('#profile').search(:ul).last.search(:li).map do |li|
    {agency_id: agency_id,
     agency_business_entity_name: agency[:business_entity_name],
     owner_name: li.inner_text}
  end

  ScraperWiki.save_sqlite([:agency_id, :owner_name], owners, 'owners')

  # Save lobbyists
  if agency_page.at('#lobbyistDetails')
    lobbyists = agency_page.at('#lobbyistDetails').at(:tbody).search(:tr).map do |row|
      {agency_id: agency_id,
       agency_business_entity_name: agency[:business_entity_name],
       lobbyist_name: row.search(:td)[1].inner_text,
       position: row.search(:td)[2].inner_text,
       former_government_representative: row.search(:td)[3].inner_text,
       cessation_date: row.search(:td)[4].inner_text.strip}
    end

    ScraperWiki.save_sqlite([:agency_id, :lobbyist_name], lobbyists, 'lobbyists')
  end

  # Save clients
  if agency_page.at('#clientDetails')
    clients = agency_page.at('#clientDetails').at(:tbody).search(:tr).map do |row|
      {agency_id: agency_id,
       agency_business_entity_name: agency[:business_entity_name],
       client_name: row.search(:td)[1].inner_text}
    end

    ScraperWiki.save_sqlite([:agency_id, :client_name], clients, 'clients')
  end
end
require 'scraperwiki'
require 'mechanize'

agent = Mechanize.new
base_url = 'http://lobbyists.pmc.gov.au/'
table = agent.get("#{base_url}who_register.cfm").at(:table)

agencies = table.at(:tbody).search(:tr).map do |row|
  {url: base_url + row.search(:td)[1].at(:a).attr(:href),
   business_entity_name: row.search(:td)[1].inner_text,
   trading_name: row.search(:td)[2].inner_text,
   abn: row.search(:td)[3].inner_text,
   details_last_updated: Date.parse(row.search(:td)[4].inner_text)}
end

agencies.each do |agency|
  agency_id = agency[:url].match('id=(.*)')[1]

  if !ScraperWiki.select("* FROM agencies WHERE `abn`='#{agency[:abn]}' AND `details_last_updated`='#{agency[:details_last_updated]}'").empty? 
    puts "Skipping existing record agency ID #{agency_id}"
    next
  end

  agency_page = agent.get agency[:url]
  
  agency_details = {
    id: agency_id,
    url: agency[:url],
    business_entity_name: agency[:business_entity_name],
    trading_name: agency[:trading_name],
    abn: agency[:abn],
    details_last_updated: agency[:details_last_updated],
    date_scraped: Date.today
  }

  ScraperWiki.save_sqlite([:id], agency_details, 'agencies')

  # Save owners
  owners = agency_page.at('#profile').search(:ul).last.search(:li).map do |li|
    {agency_id: agency_id,
     agency_business_entity_name: agency[:business_entity_name],
     owner_name: li.inner_text}
  end

  ScraperWiki.save_sqlite([:agency_id, :owner_name], owners, 'owners')

  # Save lobbyists
  if agency_page.at('#lobbyistDetails')
    lobbyists = agency_page.at('#lobbyistDetails').at(:tbody).search(:tr).map do |row|
      {agency_id: agency_id,
       agency_business_entity_name: agency[:business_entity_name],
       lobbyist_name: row.search(:td)[1].inner_text,
       position: row.search(:td)[2].inner_text,
       former_government_representative: row.search(:td)[3].inner_text,
       cessation_date: row.search(:td)[4].inner_text.strip}
    end

    ScraperWiki.save_sqlite([:agency_id, :lobbyist_name], lobbyists, 'lobbyists')
  end

  # Save clients
  if agency_page.at('#clientDetails')
    clients = agency_page.at('#clientDetails').at(:tbody).search(:tr).map do |row|
      {agency_id: agency_id,
       agency_business_entity_name: agency[:business_entity_name],
       client_name: row.search(:td)[1].inner_text}
    end

    ScraperWiki.save_sqlite([:agency_id, :client_name], clients, 'clients')
  end
end
