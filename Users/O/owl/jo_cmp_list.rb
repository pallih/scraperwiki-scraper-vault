# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.ccd.gov.jo:7779"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
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
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "details"
    doc = Nokogiri::HTML(data,nil,'WINDOWS-1256').xpath(".")
    r = {"link"=>pg.uri.to_s}

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[2]/td/font[contains(text(),'الرقم الوطني للمنشأه')]/text()")).split(":")[1].strip rescue nil
    r["origin_no"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[3]/td/font[contains(text(),'رقم الشركة')]/text()")).split(":").last.strip
    r["company_number"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[3]/td/font[contains(text(),'نوع الشركة')]/text()")).split(":").last.strip
    r["type"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[4]/td/font[contains(text(),'اسم الشركة')]/text()")).split(":").last.strip
    r["company_name"] = tmp

    tmp = Date.parse(s_text(doc.xpath(".//table[@width='700']/tr[6]/td/font[contains(text(),'تاريخ تسجيل الشركة')]/text()")).split(":").last.strip).to_s rescue nil
    r["reg_dt"] = tmp


    return r.merge(rec).delete_if{|k,v| k =~ /^tmp_/}
  end
end

def action()
  strt = get_metadata("start",1)
  (strt..strt+10000).each_with_index{|id,idx|
    pg = @br.get(BASE_URL + "/ccd/aims_q1a?c_id=#{id}")
    next if pg.nil? 
    record = scrape(pg,"details",{"reference_no"=>id})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],record)
    save_metadata("start",strt+idx)
  }
end

action()
#puts scrape(@br.get("http://www.ccd.gov.jo:7779/ccd/aims_q1a?c_id=1"),"details",{})
#puts scrape(@br.get("http://www.ccd.gov.jo:7779/ccd/aims_q1a?c_id=169678"),"details",{})# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.ccd.gov.jo:7779"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
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
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "details"
    doc = Nokogiri::HTML(data,nil,'WINDOWS-1256').xpath(".")
    r = {"link"=>pg.uri.to_s}

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[2]/td/font[contains(text(),'الرقم الوطني للمنشأه')]/text()")).split(":")[1].strip rescue nil
    r["origin_no"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[3]/td/font[contains(text(),'رقم الشركة')]/text()")).split(":").last.strip
    r["company_number"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[3]/td/font[contains(text(),'نوع الشركة')]/text()")).split(":").last.strip
    r["type"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[4]/td/font[contains(text(),'اسم الشركة')]/text()")).split(":").last.strip
    r["company_name"] = tmp

    tmp = Date.parse(s_text(doc.xpath(".//table[@width='700']/tr[6]/td/font[contains(text(),'تاريخ تسجيل الشركة')]/text()")).split(":").last.strip).to_s rescue nil
    r["reg_dt"] = tmp


    return r.merge(rec).delete_if{|k,v| k =~ /^tmp_/}
  end
end

def action()
  strt = get_metadata("start",1)
  (strt..strt+10000).each_with_index{|id,idx|
    pg = @br.get(BASE_URL + "/ccd/aims_q1a?c_id=#{id}")
    next if pg.nil? 
    record = scrape(pg,"details",{"reference_no"=>id})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],record)
    save_metadata("start",strt+idx)
  }
end

action()
#puts scrape(@br.get("http://www.ccd.gov.jo:7779/ccd/aims_q1a?c_id=1"),"details",{})
#puts scrape(@br.get("http://www.ccd.gov.jo:7779/ccd/aims_q1a?c_id=169678"),"details",{})# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.ccd.gov.jo:7779"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
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
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "details"
    doc = Nokogiri::HTML(data,nil,'WINDOWS-1256').xpath(".")
    r = {"link"=>pg.uri.to_s}

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[2]/td/font[contains(text(),'الرقم الوطني للمنشأه')]/text()")).split(":")[1].strip rescue nil
    r["origin_no"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[3]/td/font[contains(text(),'رقم الشركة')]/text()")).split(":").last.strip
    r["company_number"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[3]/td/font[contains(text(),'نوع الشركة')]/text()")).split(":").last.strip
    r["type"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[4]/td/font[contains(text(),'اسم الشركة')]/text()")).split(":").last.strip
    r["company_name"] = tmp

    tmp = Date.parse(s_text(doc.xpath(".//table[@width='700']/tr[6]/td/font[contains(text(),'تاريخ تسجيل الشركة')]/text()")).split(":").last.strip).to_s rescue nil
    r["reg_dt"] = tmp


    return r.merge(rec).delete_if{|k,v| k =~ /^tmp_/}
  end
end

def action()
  strt = get_metadata("start",1)
  (strt..strt+10000).each_with_index{|id,idx|
    pg = @br.get(BASE_URL + "/ccd/aims_q1a?c_id=#{id}")
    next if pg.nil? 
    record = scrape(pg,"details",{"reference_no"=>id})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],record)
    save_metadata("start",strt+idx)
  }
end

action()
#puts scrape(@br.get("http://www.ccd.gov.jo:7779/ccd/aims_q1a?c_id=1"),"details",{})
#puts scrape(@br.get("http://www.ccd.gov.jo:7779/ccd/aims_q1a?c_id=169678"),"details",{})# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.ccd.gov.jo:7779"
  
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 3600
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
  def strip
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "details"
    doc = Nokogiri::HTML(data,nil,'WINDOWS-1256').xpath(".")
    r = {"link"=>pg.uri.to_s}

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[2]/td/font[contains(text(),'الرقم الوطني للمنشأه')]/text()")).split(":")[1].strip rescue nil
    r["origin_no"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[3]/td/font[contains(text(),'رقم الشركة')]/text()")).split(":").last.strip
    r["company_number"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[3]/td/font[contains(text(),'نوع الشركة')]/text()")).split(":").last.strip
    r["type"] = tmp

    tmp = s_text(doc.xpath(".//table[@width='700']/tr[4]/td/font[contains(text(),'اسم الشركة')]/text()")).split(":").last.strip
    r["company_name"] = tmp

    tmp = Date.parse(s_text(doc.xpath(".//table[@width='700']/tr[6]/td/font[contains(text(),'تاريخ تسجيل الشركة')]/text()")).split(":").last.strip).to_s rescue nil
    r["reg_dt"] = tmp


    return r.merge(rec).delete_if{|k,v| k =~ /^tmp_/}
  end
end

def action()
  strt = get_metadata("start",1)
  (strt..strt+10000).each_with_index{|id,idx|
    pg = @br.get(BASE_URL + "/ccd/aims_q1a?c_id=#{id}") rescue nil
     next if pg.nil? 
    record = scrape(pg,"details",{"reference_no"=>id})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],record)
    save_metadata("start",strt+idx)
  }
end

action()
#puts scrape(@br.get("http://www.ccd.gov.jo:7779/ccd/aims_q1a?c_id=1"),"details",{})
#puts scrape(@br.get("http://www.ccd.gov.jo:7779/ccd/aims_q1a?c_id=169678"),"details",{})