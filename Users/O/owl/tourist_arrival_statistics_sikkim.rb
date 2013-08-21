# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.sikkimtourism.travel"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end

class Array
  def pretty
    self.collect{|a|a.strip}
  end
end

def scrape(data,act,rec)
  if act == "details"
    records = []
    #Weather
    doc = Nokogiri::HTML(@br.get("http://imdsikkim.gov.in/monthlymetparam.html").body).xpath(".")
    weather = {}
    doc.xpath(".//table[@width='93%']/tr[position()>2]").each{|tr|
      td = tr.xpath("td")
      weather[s_text(td[0].xpath("./div/text()")).downcase] = {
        "air_daily_max"=>s_text(td[1].xpath("./text()")),
        "air_daily_min"=>s_text(td[2].xpath("./text()")),
        "rain_monthly_total"=>s_text(td[3].xpath("./text()")),
        "no_of_rainy_days"=>s_text(td[4].xpath("./text()")),
        "relative_humidity"=>s_text(td[5].xpath("./text()")),
        "mean_wind_speed"=>s_text(td[6].xpath("./text()")),
      }
    }    

    doc = Nokogiri::HTML(data).xpath(".")
    hdrs = a_text(doc.xpath(".//div[@id='TourismAwards']/table/tr[1]/td/strong"))
    #Domestic
    doc.xpath(".//div[@id='TourismAwards']/table/tr[position()>1 and following-sibling::tr[count(td)=1]]").each{|tr|
      td = tr.xpath("td")
      break if td.length < 1 or s_text(td[0].xpath("./text()")) =~ /TOTAL/
      hdrs[1..-1].each_with_index{|h,idx|
        tmp = {"type"=>"domestic","month" => s_text(td[0].xpath('./text()')).downcase,"year"=>h.to_i,"no_of_visitors"=>s_text(td[idx+1].xpath("./text()")).to_i}
        tm = weather.select{|k,v| k =~ /^#{tmp['month']}/}.values.first
        records << tmp.merge(tm)
      }
    }
    #Foreign
    doc.xpath(".//div[@id='TourismAwards']/table/tr[td/strong[contains(text(),'FOREIGN')]]/following-sibling::tr[position()>1]").each{|tr|
      break
      td = tr.xpath("td")
      break if td.length < 1 or s_text(td[0].xpath("./text()")) =~ /TOTAL/
      hdrs[1..-1].each_with_index{|h,idx|
        tmp = {"type"=>"domestic","month" => s_text(td[0].xpath('./text()')),"year"=>h.to_i,"no_of_visitors"=>s_text(td[idx+1].xpath("./text()")).to_i} 
        tm = weather.select{|k,v| k =~ /^#{tmp['month']}/}.values.first
        records << tmp.merge(tm)

      }
    }
    return records
  end
end

def action()
  list = scrape(@br.get(BASE_URL + "/Webforms/General/DepartmentStakeholders/TouristArrivalStats.aspx").body,"details",{})
  ScraperWiki.save_sqlite(unique_keys=['type','month','year'],list)
end

action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.sikkimtourism.travel"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/\r|\n|\t|\s+/,' ').strip
  end
end

class Array
  def pretty
    self.collect{|a|a.strip}
  end
end

def scrape(data,act,rec)
  if act == "details"
    records = []
    #Weather
    doc = Nokogiri::HTML(@br.get("http://imdsikkim.gov.in/monthlymetparam.html").body).xpath(".")
    weather = {}
    doc.xpath(".//table[@width='93%']/tr[position()>2]").each{|tr|
      td = tr.xpath("td")
      weather[s_text(td[0].xpath("./div/text()")).downcase] = {
        "air_daily_max"=>s_text(td[1].xpath("./text()")),
        "air_daily_min"=>s_text(td[2].xpath("./text()")),
        "rain_monthly_total"=>s_text(td[3].xpath("./text()")),
        "no_of_rainy_days"=>s_text(td[4].xpath("./text()")),
        "relative_humidity"=>s_text(td[5].xpath("./text()")),
        "mean_wind_speed"=>s_text(td[6].xpath("./text()")),
      }
    }    

    doc = Nokogiri::HTML(data).xpath(".")
    hdrs = a_text(doc.xpath(".//div[@id='TourismAwards']/table/tr[1]/td/strong"))
    #Domestic
    doc.xpath(".//div[@id='TourismAwards']/table/tr[position()>1 and following-sibling::tr[count(td)=1]]").each{|tr|
      td = tr.xpath("td")
      break if td.length < 1 or s_text(td[0].xpath("./text()")) =~ /TOTAL/
      hdrs[1..-1].each_with_index{|h,idx|
        tmp = {"type"=>"domestic","month" => s_text(td[0].xpath('./text()')).downcase,"year"=>h.to_i,"no_of_visitors"=>s_text(td[idx+1].xpath("./text()")).to_i}
        tm = weather.select{|k,v| k =~ /^#{tmp['month']}/}.values.first
        records << tmp.merge(tm)
      }
    }
    #Foreign
    doc.xpath(".//div[@id='TourismAwards']/table/tr[td/strong[contains(text(),'FOREIGN')]]/following-sibling::tr[position()>1]").each{|tr|
      break
      td = tr.xpath("td")
      break if td.length < 1 or s_text(td[0].xpath("./text()")) =~ /TOTAL/
      hdrs[1..-1].each_with_index{|h,idx|
        tmp = {"type"=>"domestic","month" => s_text(td[0].xpath('./text()')),"year"=>h.to_i,"no_of_visitors"=>s_text(td[idx+1].xpath("./text()")).to_i} 
        tm = weather.select{|k,v| k =~ /^#{tmp['month']}/}.values.first
        records << tmp.merge(tm)

      }
    }
    return records
  end
end

def action()
  list = scrape(@br.get(BASE_URL + "/Webforms/General/DepartmentStakeholders/TouristArrivalStats.aspx").body,"details",{})
  ScraperWiki.save_sqlite(unique_keys=['type','month','year'],list)
end

action()
