require 'rubygems'
require 'mechanize'
require 'date'

agent = Mechanize.new do |a|
  a.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

url = 'https://www.ntlis.nt.gov.au/planning/lta.dar.list'

page = agent.get(url)

page.search('div.apps_application').each do |a|
  next if a.at('div.app_address').nil?  # No addresses on this DA

  address = a.at('div.app_address').at('p').inner_html.split('<br>')
  council_reference = a.at('div.app_map').inner_html.match(/\d{8}/).to_s

  a.search('h6').each do |h|
    case h.inner_text
    when "Description of Proposal:"
      @description = h.next.inner_text
    when "Exhibition ends at:"
      @on_notice_to = Date.parse(h.next.inner_text).to_s
    end
  end

  record = {
    'address' => "#{address[1].strip}, #{address[2].strip}, NT",
    'description' => @description,
    'on_notice_to' => @on_notice_to,
    'council_reference' => council_reference,
    'info_url' => "https://www.ntlis.nt.gov.au/planningPopup/lta.dar.view/#{council_reference}",
    'comment_url' => "https://www.ntlis.nt.gov.au/planningPopup/lta.dar.submitOpinion/#{council_reference}",
    'date_scraped' => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end
require 'rubygems'
require 'mechanize'
require 'date'

agent = Mechanize.new do |a|
  a.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

url = 'https://www.ntlis.nt.gov.au/planning/lta.dar.list'

page = agent.get(url)

page.search('div.apps_application').each do |a|
  next if a.at('div.app_address').nil?  # No addresses on this DA

  address = a.at('div.app_address').at('p').inner_html.split('<br>')
  council_reference = a.at('div.app_map').inner_html.match(/\d{8}/).to_s

  a.search('h6').each do |h|
    case h.inner_text
    when "Description of Proposal:"
      @description = h.next.inner_text
    when "Exhibition ends at:"
      @on_notice_to = Date.parse(h.next.inner_text).to_s
    end
  end

  record = {
    'address' => "#{address[1].strip}, #{address[2].strip}, NT",
    'description' => @description,
    'on_notice_to' => @on_notice_to,
    'council_reference' => council_reference,
    'info_url' => "https://www.ntlis.nt.gov.au/planningPopup/lta.dar.view/#{council_reference}",
    'comment_url' => "https://www.ntlis.nt.gov.au/planningPopup/lta.dar.submitOpinion/#{council_reference}",
    'date_scraped' => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end
require 'rubygems'
require 'mechanize'
require 'date'

agent = Mechanize.new do |a|
  a.verify_mode = OpenSSL::SSL::VERIFY_NONE
end

url = 'https://www.ntlis.nt.gov.au/planning/lta.dar.list'

page = agent.get(url)

page.search('div.apps_application').each do |a|
  next if a.at('div.app_address').nil?  # No addresses on this DA

  address = a.at('div.app_address').at('p').inner_html.split('<br>')
  council_reference = a.at('div.app_map').inner_html.match(/\d{8}/).to_s

  a.search('h6').each do |h|
    case h.inner_text
    when "Description of Proposal:"
      @description = h.next.inner_text
    when "Exhibition ends at:"
      @on_notice_to = Date.parse(h.next.inner_text).to_s
    end
  end

  record = {
    'address' => "#{address[1].strip}, #{address[2].strip}, NT",
    'description' => @description,
    'on_notice_to' => @on_notice_to,
    'council_reference' => council_reference,
    'info_url' => "https://www.ntlis.nt.gov.au/planningPopup/lta.dar.view/#{council_reference}",
    'comment_url' => "https://www.ntlis.nt.gov.au/planningPopup/lta.dar.submitOpinion/#{council_reference}",
    'date_scraped' => Date.today.to_s
  }

  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end
