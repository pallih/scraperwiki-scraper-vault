# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='incident_table' and not(contains(@title,'Search'))]").each{|doc|
      r = {
        "name" => doc.xpath("./tr/td[@class='emphasized' and text()='Name:']/following-sibling::*[1][self::td]").inner_text.strip,
        "county" => doc.xpath("./tr/td[@class='emphasized' and text()='County:']/following-sibling::*[1][self::td]").inner_text.strip,
        "location" => doc.xpath("./tr/td[@class='emphasized' and text()='Location:']/following-sibling::*[1][self::td]").inner_text.strip,
        "unit" => doc.xpath("./tr/td[@class='emphasized' and text()='Administrative Unit:']/following-sibling::*[1][self::td]").inner_text.strip,
        "started_dt" => doc.xpath("./tr/td[@class='emphasized' and text()='Date Started:']/following-sibling::*[1][self::td]").inner_text.strip,
        "update_dt" => doc.xpath("./tr/td[@class='emphasized' and text()='Last update:']/following-sibling::*[1][self::td]").inner_text.strip
      }
      tmp = doc.xpath("./tr/td[@class='emphasized' and text()='Status/Notes:']/following-sibling::*[1][self::td]").inner_text.strip
      if tmp =~ /acres/i
        #puts tmp.gsub(",","").scan(/(\d+) acres/i).flatten.first + " acres"
        r["status"] = tmp.gsub(",","").scan(/(\d+) acres/i).flatten.first + " acres" rescue nil
      end
      records << r.merge(rec)
    }
    return records
  end
end

def action(yr)
  list = scrape(Mechanize.new.post("http://cdfdata.fire.ca.gov/incidents/incidents_archived",{"archive_year"=>yr,"pc"=>"all"}).body,"list",{"year"=>yr})
  ScraperWiki.save_sqlite(unique_keys=['name'],list)
end

years = (2003..2011).to_a
years.each{|yr|
  action(yr)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='incident_table' and not(contains(@title,'Search'))]").each{|doc|
      r = {
        "name" => doc.xpath("./tr/td[@class='emphasized' and text()='Name:']/following-sibling::*[1][self::td]").inner_text.strip,
        "county" => doc.xpath("./tr/td[@class='emphasized' and text()='County:']/following-sibling::*[1][self::td]").inner_text.strip,
        "location" => doc.xpath("./tr/td[@class='emphasized' and text()='Location:']/following-sibling::*[1][self::td]").inner_text.strip,
        "unit" => doc.xpath("./tr/td[@class='emphasized' and text()='Administrative Unit:']/following-sibling::*[1][self::td]").inner_text.strip,
        "started_dt" => doc.xpath("./tr/td[@class='emphasized' and text()='Date Started:']/following-sibling::*[1][self::td]").inner_text.strip,
        "update_dt" => doc.xpath("./tr/td[@class='emphasized' and text()='Last update:']/following-sibling::*[1][self::td]").inner_text.strip
      }
      tmp = doc.xpath("./tr/td[@class='emphasized' and text()='Status/Notes:']/following-sibling::*[1][self::td]").inner_text.strip
      if tmp =~ /acres/i
        #puts tmp.gsub(",","").scan(/(\d+) acres/i).flatten.first + " acres"
        r["status"] = tmp.gsub(",","").scan(/(\d+) acres/i).flatten.first + " acres" rescue nil
      end
      records << r.merge(rec)
    }
    return records
  end
end

def action(yr)
  list = scrape(Mechanize.new.post("http://cdfdata.fire.ca.gov/incidents/incidents_archived",{"archive_year"=>yr,"pc"=>"all"}).body,"list",{"year"=>yr})
  ScraperWiki.save_sqlite(unique_keys=['name'],list)
end

years = (2003..2011).to_a
years.each{|yr|
  action(yr)
}