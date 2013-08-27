# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'httpclient'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://org.rdb.rw"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

#@br = HTTPClient.new{|b|
#}

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
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".")
    doc.xpath(".//table[@id='ctl00_C_GridView1']/tr[position()>1]").each{|tr|
      break if tr.xpath("td").length < 4
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/text()")),
        "reg_dt" => s_text(tr.xpath("./td[2]/text()")),
        "company_name" => s_text(tr.xpath("./td[3]/text()")),
        "address" => s_text(tr.xpath("./td[4]/text()")),
        "doc" => Time.now
      }.merge(rec)
    }
    tmp = attributes(doc.xpath(".//table[@border='0']/tr/td[span]/following-sibling::*[1]/a"),"href").split("'")
    return tmp[3],records
  end
end

def action(frm_dt,to_dt)
  pg = @br.get(BASE_URL+"/inf/Public/Products/EntSearch.aspx") rescue retry
  begin
    params = {
      "ctl00$C$REGISTRATION_DATE_FROMFilterFld"=>frm_dt.strftime("%d/%m/%Y"),
      "ctl00$C$REGISTRATION_DATE_TOFilterFld"=>to_dt.strftime("%d/%m/%Y"),"ctl00$C$BtnFilter"=>"Search"
    }
    begin
      pg.form_with(:name=>"aspnetForm") do |f|
        params.each{|k,v| f[k] = v}
        pg = f.submit rescue retry
      end 
    end
    begin
      nex,list = scrape(pg.body,"list",{})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
      break if list.nil? or list.length < 20 or nex.nil? or nex.empty? 
  
      params = {"__EVENTTARGET"=>"ctl00$C$GridView1","__EVENTARGUMENT"=>nex}
      begin
        pg.form_with(:name=>"aspnetForm") do |f|
          params.each{|k,v| f[k] = v}
          pg = f.submit rescue retry
        end
      end
    end while(true)
  end
end

start = Date.parse(get_metadata("start","01-01-2010"))

((start-30)..Date.today).each{|dt|
  action(dt,dt)
  save_metadata("start",dt.next.to_s)
}

#dt = Date.parse("01-01-2010")
#action(dt>>3,dt>>4)
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'httpclient'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://org.rdb.rw"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

#@br = HTTPClient.new{|b|
#}

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
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".")
    doc.xpath(".//table[@id='ctl00_C_GridView1']/tr[position()>1]").each{|tr|
      break if tr.xpath("td").length < 4
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/text()")),
        "reg_dt" => s_text(tr.xpath("./td[2]/text()")),
        "company_name" => s_text(tr.xpath("./td[3]/text()")),
        "address" => s_text(tr.xpath("./td[4]/text()")),
        "doc" => Time.now
      }.merge(rec)
    }
    tmp = attributes(doc.xpath(".//table[@border='0']/tr/td[span]/following-sibling::*[1]/a"),"href").split("'")
    return tmp[3],records
  end
end

def action(frm_dt,to_dt)
  pg = @br.get(BASE_URL+"/inf/Public/Products/EntSearch.aspx") rescue retry
  begin
    params = {
      "ctl00$C$REGISTRATION_DATE_FROMFilterFld"=>frm_dt.strftime("%d/%m/%Y"),
      "ctl00$C$REGISTRATION_DATE_TOFilterFld"=>to_dt.strftime("%d/%m/%Y"),"ctl00$C$BtnFilter"=>"Search"
    }
    begin
      pg.form_with(:name=>"aspnetForm") do |f|
        params.each{|k,v| f[k] = v}
        pg = f.submit rescue retry
      end 
    end
    begin
      nex,list = scrape(pg.body,"list",{})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
      break if list.nil? or list.length < 20 or nex.nil? or nex.empty? 
  
      params = {"__EVENTTARGET"=>"ctl00$C$GridView1","__EVENTARGUMENT"=>nex}
      begin
        pg.form_with(:name=>"aspnetForm") do |f|
          params.each{|k,v| f[k] = v}
          pg = f.submit rescue retry
        end
      end
    end while(true)
  end
end

start = Date.parse(get_metadata("start","01-01-2010"))

((start-30)..Date.today).each{|dt|
  action(dt,dt)
  save_metadata("start",dt.next.to_s)
}

#dt = Date.parse("01-01-2010")
#action(dt>>3,dt>>4)
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'httpclient'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://org.rdb.rw"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

#@br = HTTPClient.new{|b|
#}

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
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".")
    doc.xpath(".//table[@id='ctl00_C_GridView1']/tr[position()>1]").each{|tr|
      break if tr.xpath("td").length < 4
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/text()")),
        "reg_dt" => s_text(tr.xpath("./td[2]/text()")),
        "company_name" => s_text(tr.xpath("./td[3]/text()")),
        "address" => s_text(tr.xpath("./td[4]/text()")),
        "doc" => Time.now
      }.merge(rec)
    }
    tmp = attributes(doc.xpath(".//table[@border='0']/tr/td[span]/following-sibling::*[1]/a"),"href").split("'")
    return tmp[3],records
  end
end

def action(frm_dt,to_dt)
  pg = @br.get(BASE_URL+"/inf/Public/Products/EntSearch.aspx") rescue retry
  begin
    params = {
      "ctl00$C$REGISTRATION_DATE_FROMFilterFld"=>frm_dt.strftime("%d/%m/%Y"),
      "ctl00$C$REGISTRATION_DATE_TOFilterFld"=>to_dt.strftime("%d/%m/%Y"),"ctl00$C$BtnFilter"=>"Search"
    }
    begin
      pg.form_with(:name=>"aspnetForm") do |f|
        params.each{|k,v| f[k] = v}
        pg = f.submit rescue retry
      end 
    end
    begin
      nex,list = scrape(pg.body,"list",{})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
      break if list.nil? or list.length < 20 or nex.nil? or nex.empty? 
  
      params = {"__EVENTTARGET"=>"ctl00$C$GridView1","__EVENTARGUMENT"=>nex}
      begin
        pg.form_with(:name=>"aspnetForm") do |f|
          params.each{|k,v| f[k] = v}
          pg = f.submit rescue retry
        end
      end
    end while(true)
  end
end

start = Date.parse(get_metadata("start","01-01-2010"))

((start-30)..Date.today).each{|dt|
  action(dt,dt)
  save_metadata("start",dt.next.to_s)
}

#dt = Date.parse("01-01-2010")
#action(dt>>3,dt>>4)
