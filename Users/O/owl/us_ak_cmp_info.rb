# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'

def get_metadata(key, default)
  ScraperWiki.get_metadata(key, default)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
  retry
end

def save_metadata(key, value)
  ScraperWiki.save_metadata(key, value)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
  retry
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://commerce.alaska.gov/CBP/Main/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}#{uri.path.split("/")[0..-2].join("/")}"  
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data)
    doc.xpath(".//table[@id='ctl00_cphMain_GridViewResults']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        "EntityType" => tr.xpath(".//*[contains(@id,'_type')]/text()").text.strip,
        "CompanyNumber" => tr.xpath(".//*[contains(@id,'_entityNum')]/text()").text.strip,
        "CompanyName" => tr.xpath(".//*[contains(@id,'_name')]/text()").text.strip,
        "Status" => tr.xpath(".//*[contains(@id,'_status')]/text()").text.strip,
        "Doc" => Time.now
      }.merge(rec)
    }
    nex = attributes(doc.xpath(".//div[@id='main']/a[contains(@id,'_lb') and b]/following-sibling::*[1][self::a]"),"href").split("'")[1]
    puts nex.inspect
    return records,nex
  end
end

def action(srch)
  pg = @br.get(BASE_URL + "CBPLSearch.aspx?mode=Corp")
  params = {
      "ctl00$cphMain$TextBoxEntityName"=>srch,
      "ctl00$cphMain$entitySearchType"=>"rbEntityStartsWith",
      "ctl00$cphMain$Search"=>"Search"
  }
  ttl = 0
  begin
    pg.form_with(:name=>"aspnetForm") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
    records,nex = scrape(pg,"list",{})
    ttl = ttl + records.length
    ScraperWiki.save_sqlite(unique_keys=['CompanyNumber'],records) unless records.nil? or records.empty? 
    params = {"__EVENTTARGET"=>nex}
    break if nex.nil? or nex.empty? or records.empty? 
  end while(true)
  return srch,ttl
end

def import
  @br.get("http://commerce.alaska.gov/CBP/DBDownloads/CorporationsDownload.CSV").save_as("CorporationsDownload.CSV")
  csv_data = CSV.read 'CorporationsDownload.CSV'
  headers = csv_data.shift.map {|i| i.to_s }
  string_data = csv_data.map {|row| row.map {|cell| cell.to_s } }
  records = string_data.map {|row| Hash[*headers.zip(row).flatten] }
  puts records.length
  ScraperWiki.save_sqlite(unique_keys=['EntityNumber'],records)
end


import()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'

def get_metadata(key, default)
  ScraperWiki.get_metadata(key, default)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
  retry
end

def save_metadata(key, value)
  ScraperWiki.save_metadata(key, value)
rescue Timeout::Error => e
  puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
  retry
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://commerce.alaska.gov/CBP/Main/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}#{uri.path.split("/")[0..-2].join("/")}"  
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data)
    doc.xpath(".//table[@id='ctl00_cphMain_GridViewResults']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      records << {
        "EntityType" => tr.xpath(".//*[contains(@id,'_type')]/text()").text.strip,
        "CompanyNumber" => tr.xpath(".//*[contains(@id,'_entityNum')]/text()").text.strip,
        "CompanyName" => tr.xpath(".//*[contains(@id,'_name')]/text()").text.strip,
        "Status" => tr.xpath(".//*[contains(@id,'_status')]/text()").text.strip,
        "Doc" => Time.now
      }.merge(rec)
    }
    nex = attributes(doc.xpath(".//div[@id='main']/a[contains(@id,'_lb') and b]/following-sibling::*[1][self::a]"),"href").split("'")[1]
    puts nex.inspect
    return records,nex
  end
end

def action(srch)
  pg = @br.get(BASE_URL + "CBPLSearch.aspx?mode=Corp")
  params = {
      "ctl00$cphMain$TextBoxEntityName"=>srch,
      "ctl00$cphMain$entitySearchType"=>"rbEntityStartsWith",
      "ctl00$cphMain$Search"=>"Search"
  }
  ttl = 0
  begin
    pg.form_with(:name=>"aspnetForm") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
    records,nex = scrape(pg,"list",{})
    ttl = ttl + records.length
    ScraperWiki.save_sqlite(unique_keys=['CompanyNumber'],records) unless records.nil? or records.empty? 
    params = {"__EVENTTARGET"=>nex}
    break if nex.nil? or nex.empty? or records.empty? 
  end while(true)
  return srch,ttl
end

def import
  @br.get("http://commerce.alaska.gov/CBP/DBDownloads/CorporationsDownload.CSV").save_as("CorporationsDownload.CSV")
  csv_data = CSV.read 'CorporationsDownload.CSV'
  headers = csv_data.shift.map {|i| i.to_s }
  string_data = csv_data.map {|row| row.map {|cell| cell.to_s } }
  records = string_data.map {|row| Hash[*headers.zip(row).flatten] }
  puts records.length
  ScraperWiki.save_sqlite(unique_keys=['EntityNumber'],records)
end


import()