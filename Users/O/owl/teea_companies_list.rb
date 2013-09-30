
# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.teea.org.tw/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

@authors = {}
class String
  def blank?
    self.nil? or self.empty? 
  end
  def pretty
    self.gsub(/\n|\t|\r/,' ').gsub(/\s+/," ").gsub(/${##}|^{##}|;$|^;|,$|^,/,'').gsub(/\u2013/,'-').strip.gsub(/(\u00A1@)+/,'').strip
  end
  def join(str)
    self + str
  end
  def append_base(str)
    return nil if self.nil? or self.empty? 
    return BASE_URL + str + self
  end
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"
  if act == "details"
    doc = Nokogiri::HTML(data).xpath(".//table[@bordercolor='#ADD69A']/tbody/tr")
    r = {}
    r["company_name"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Company Name']]/following-sibling::*[1][self::td]/div/text()"))
    r["capital"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Capital']]/following-sibling::*[1][self::td]/div/text()"))
    r["cmp_addr"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Company Address']]/following-sibling::*[1][self::td]/div/text()"))
    r["contact_addr"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Contact Address']]/following-sibling::*[1][self::td]/div/text()"))
    r["incharge"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Person in charge']]/following-sibling::*[1][self::td]/div/text()"))
    r["contact_person"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Contact person
']]/following-sibling::*[1][self::td]/div/text()"))
    r["telephone"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Phone']]/following-sibling::*[1][self::td]/div/text()"))
    r["fax"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Fax']]/following-sibling::*[1][self::td]/div/text()"))
    r["website"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='URL']]/following-sibling::*[1][self::td]/div/a/text()"))
    r["email"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='E-Mail']]/following-sibling::*[1][self::td]/div/a/text()"))
    return r.merge(rec)
  end
end


def action(srch)
  begin
    pg = @br.get(BASE_URL + "vip_about_e.asp?sno=#{srch}")
    record = scrape(pg,"details",{"id"=>srch.to_i})
    ScraperWiki.save_sqlite(unique_keys=['id'],record,table_name='swdata',verbose=2) unless record['company_name'].nil? or record['company_name'].empty? 
    save_metadata("start",srch.next) unless record['company_name'].nil? or record['company_name'].empty? 
  rescue Exception => e
    puts [srch,e].inspect
  end if exists(srch,"swdata","id") == 0
end

start = get_metadata("start",1)
(start..(start+20)).each{|srch|
  action(srch)
}


# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.teea.org.tw/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

@authors = {}
class String
  def blank?
    self.nil? or self.empty? 
  end
  def pretty
    self.gsub(/\n|\t|\r/,' ').gsub(/\s+/," ").gsub(/${##}|^{##}|;$|^;|,$|^,/,'').gsub(/\u2013/,'-').strip.gsub(/(\u00A1@)+/,'').strip
  end
  def join(str)
    self + str
  end
  def append_base(str)
    return nil if self.nil? or self.empty? 
    return BASE_URL + str + self
  end
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"
  if act == "details"
    doc = Nokogiri::HTML(data).xpath(".//table[@bordercolor='#ADD69A']/tbody/tr")
    r = {}
    r["company_name"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Company Name']]/following-sibling::*[1][self::td]/div/text()"))
    r["capital"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Capital']]/following-sibling::*[1][self::td]/div/text()"))
    r["cmp_addr"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Company Address']]/following-sibling::*[1][self::td]/div/text()"))
    r["contact_addr"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Contact Address']]/following-sibling::*[1][self::td]/div/text()"))
    r["incharge"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Person in charge']]/following-sibling::*[1][self::td]/div/text()"))
    r["contact_person"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Contact person
']]/following-sibling::*[1][self::td]/div/text()"))
    r["telephone"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Phone']]/following-sibling::*[1][self::td]/div/text()"))
    r["fax"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Fax']]/following-sibling::*[1][self::td]/div/text()"))
    r["website"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='URL']]/following-sibling::*[1][self::td]/div/a/text()"))
    r["email"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='E-Mail']]/following-sibling::*[1][self::td]/div/a/text()"))
    return r.merge(rec)
  end
end


def action(srch)
  begin
    pg = @br.get(BASE_URL + "vip_about_e.asp?sno=#{srch}")
    record = scrape(pg,"details",{"id"=>srch.to_i})
    ScraperWiki.save_sqlite(unique_keys=['id'],record,table_name='swdata',verbose=2) unless record['company_name'].nil? or record['company_name'].empty? 
    save_metadata("start",srch.next) unless record['company_name'].nil? or record['company_name'].empty? 
  rescue Exception => e
    puts [srch,e].inspect
  end if exists(srch,"swdata","id") == 0
end

start = get_metadata("start",1)
(start..(start+20)).each{|srch|
  action(srch)
}


# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.teea.org.tw/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

@authors = {}
class String
  def blank?
    self.nil? or self.empty? 
  end
  def pretty
    self.gsub(/\n|\t|\r/,' ').gsub(/\s+/," ").gsub(/${##}|^{##}|;$|^;|,$|^,/,'').gsub(/\u2013/,'-').strip.gsub(/(\u00A1@)+/,'').strip
  end
  def join(str)
    self + str
  end
  def append_base(str)
    return nil if self.nil? or self.empty? 
    return BASE_URL + str + self
  end
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"
  if act == "details"
    doc = Nokogiri::HTML(data).xpath(".//table[@bordercolor='#ADD69A']/tbody/tr")
    r = {}
    r["company_name"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Company Name']]/following-sibling::*[1][self::td]/div/text()"))
    r["capital"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Capital']]/following-sibling::*[1][self::td]/div/text()"))
    r["cmp_addr"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Company Address']]/following-sibling::*[1][self::td]/div/text()"))
    r["contact_addr"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Contact Address']]/following-sibling::*[1][self::td]/div/text()"))
    r["incharge"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Person in charge']]/following-sibling::*[1][self::td]/div/text()"))
    r["contact_person"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Contact person
']]/following-sibling::*[1][self::td]/div/text()"))
    r["telephone"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Phone']]/following-sibling::*[1][self::td]/div/text()"))
    r["fax"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Fax']]/following-sibling::*[1][self::td]/div/text()"))
    r["website"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='URL']]/following-sibling::*[1][self::td]/div/a/text()"))
    r["email"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='E-Mail']]/following-sibling::*[1][self::td]/div/a/text()"))
    return r.merge(rec)
  end
end


def action(srch)
  begin
    pg = @br.get(BASE_URL + "vip_about_e.asp?sno=#{srch}")
    record = scrape(pg,"details",{"id"=>srch.to_i})
    ScraperWiki.save_sqlite(unique_keys=['id'],record,table_name='swdata',verbose=2) unless record['company_name'].nil? or record['company_name'].empty? 
    save_metadata("start",srch.next) unless record['company_name'].nil? or record['company_name'].empty? 
  rescue Exception => e
    puts [srch,e].inspect
  end if exists(srch,"swdata","id") == 0
end

start = get_metadata("start",1)
(start..(start+20)).each{|srch|
  action(srch)
}


# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.teea.org.tw/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

@authors = {}
class String
  def blank?
    self.nil? or self.empty? 
  end
  def pretty
    self.gsub(/\n|\t|\r/,' ').gsub(/\s+/," ").gsub(/${##}|^{##}|;$|^;|,$|^,/,'').gsub(/\u2013/,'-').strip.gsub(/(\u00A1@)+/,'').strip
  end
  def join(str)
    self + str
  end
  def append_base(str)
    return nil if self.nil? or self.empty? 
    return BASE_URL + str + self
  end
end
class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"
  if act == "details"
    doc = Nokogiri::HTML(data).xpath(".//table[@bordercolor='#ADD69A']/tbody/tr")
    r = {}
    r["company_name"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Company Name']]/following-sibling::*[1][self::td]/div/text()"))
    r["capital"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Capital']]/following-sibling::*[1][self::td]/div/text()"))
    r["cmp_addr"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Company Address']]/following-sibling::*[1][self::td]/div/text()"))
    r["contact_addr"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Contact Address']]/following-sibling::*[1][self::td]/div/text()"))
    r["incharge"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Person in charge']]/following-sibling::*[1][self::td]/div/text()"))
    r["contact_person"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Contact person
']]/following-sibling::*[1][self::td]/div/text()"))
    r["telephone"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Phone']]/following-sibling::*[1][self::td]/div/text()"))
    r["fax"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='Fax']]/following-sibling::*[1][self::td]/div/text()"))
    r["website"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='URL']]/following-sibling::*[1][self::td]/div/a/text()"))
    r["email"] = s_text(doc.xpath("./td[@bgcolor='#D3E9C9' and div[normalize-space(text())='E-Mail']]/following-sibling::*[1][self::td]/div/a/text()"))
    return r.merge(rec)
  end
end


def action(srch)
  begin
    pg = @br.get(BASE_URL + "vip_about_e.asp?sno=#{srch}")
    record = scrape(pg,"details",{"id"=>srch.to_i})
    ScraperWiki.save_sqlite(unique_keys=['id'],record,table_name='swdata',verbose=2) unless record['company_name'].nil? or record['company_name'].empty? 
    save_metadata("start",srch.next) unless record['company_name'].nil? or record['company_name'].empty? 
  rescue Exception => e
    puts [srch,e].inspect
  end if exists(srch,"swdata","id") == 0
end

start = get_metadata("start",1)
(start..(start+20)).each{|srch|
  action(srch)
}

