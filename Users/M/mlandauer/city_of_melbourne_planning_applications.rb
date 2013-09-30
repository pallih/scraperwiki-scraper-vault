require 'mechanize'

agent = Mechanize.new

comment_url = "http://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/planningpermits/Pages/Objecting.aspx"

base_url = "http://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/Pages/Planningregisteronlinesearchresults.aspx"
# Get applications from the last two weeks
start_date = (Date.today - 14).strftime("%d/%m/%Y")
end_date = Date.today.strftime("%d/%m/%Y")

page = 1
all_urls = []
begin
  url = "#{base_url}?std=#{start_date}&end=#{end_date}&page=#{page}"
  p = agent.get(url)
  urls = p.search('table.permitsList .detail .column1 a').map{|a| a["href"]}
  all_urls += urls
  page += 1
end until urls.count == 0

all_urls = ["http://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/Pages/Planningregisteronlinesearchresults.aspx?appid=182372"]
all_urls.each do |url|
  p = agent.get(url)
  record = {"info_url" => url, "date_scraped" => Date.today.to_s, "comment_url" => comment_url}
  p.at('.permitDetail').search('tr').each do |tr|
    heading = tr.at('th').inner_text
    value = tr.at('td').inner_text
    case heading
    when "Permit Number"
      record["council_reference"] = value
    when "Date Received"
      day, month, year = value.split("/")
      record["date_received"] = Date.new(year.to_i, month.to_i, day.to_i).to_s
    when "Address of Land"
      t = value.split("(").first
      if t
        record["address"] = t.strip
      else
        record["address"] = ""
      end
    when "Applicant's Name and Address", "Officer's Name", "Objections Received", "Application Status",
      "Decision", "Expiry Date"
      # Do nothing with this
    when "Proposed Use or Development"
      record["description"] = value
    else
      raise "Unexpected #{heading}"
    end
  end
  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end

require 'mechanize'

agent = Mechanize.new

comment_url = "http://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/planningpermits/Pages/Objecting.aspx"

base_url = "http://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/Pages/Planningregisteronlinesearchresults.aspx"
# Get applications from the last two weeks
start_date = (Date.today - 14).strftime("%d/%m/%Y")
end_date = Date.today.strftime("%d/%m/%Y")

page = 1
all_urls = []
begin
  url = "#{base_url}?std=#{start_date}&end=#{end_date}&page=#{page}"
  p = agent.get(url)
  urls = p.search('table.permitsList .detail .column1 a').map{|a| a["href"]}
  all_urls += urls
  page += 1
end until urls.count == 0

all_urls = ["http://www.melbourne.vic.gov.au/BuildingandPlanning/Planning/Pages/Planningregisteronlinesearchresults.aspx?appid=182372"]
all_urls.each do |url|
  p = agent.get(url)
  record = {"info_url" => url, "date_scraped" => Date.today.to_s, "comment_url" => comment_url}
  p.at('.permitDetail').search('tr').each do |tr|
    heading = tr.at('th').inner_text
    value = tr.at('td').inner_text
    case heading
    when "Permit Number"
      record["council_reference"] = value
    when "Date Received"
      day, month, year = value.split("/")
      record["date_received"] = Date.new(year.to_i, month.to_i, day.to_i).to_s
    when "Address of Land"
      t = value.split("(").first
      if t
        record["address"] = t.strip
      else
        record["address"] = ""
      end
    when "Applicant's Name and Address", "Officer's Name", "Objections Received", "Application Status",
      "Decision", "Expiry Date"
      # Do nothing with this
    when "Proposed Use or Development"
      record["description"] = value
    else
      raise "Unexpected #{heading}"
    end
  end
  if ScraperWiki.select("* from swdata where `council_reference`='#{record['council_reference']}'").empty? 
    ScraperWiki.save_sqlite(['council_reference'], record)
  else
    puts "Skipping already saved record " + record['council_reference']
  end
end

