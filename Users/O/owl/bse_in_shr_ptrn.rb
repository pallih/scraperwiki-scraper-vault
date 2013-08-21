# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.bseindia.com"
  
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
  if act == "list"
    records = []
    data.split("~").each{|a|
      r = {}
      r["short_code"],r["company_name"],r["script_code"] = a.split(":")
      records << r
    }
    return records
  elsif act == "details"
    r = {}
    doc = Nokogiri::HTML(data).xpath(".")
    return r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}
  end
end

def action()  
  pg = @br.get("http://www.bseindia.com/common/backpageAsset.aspx?inputstr=&strFlag=0&ShowSusp=true&no=0.7173871165763637")
  puts scrape(pg.body,"list",{})
end

action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.bseindia.com"
  
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
  if act == "list"
    records = []
    data.split("~").each{|a|
      r = {}
      r["short_code"],r["company_name"],r["script_code"] = a.split(":")
      records << r
    }
    return records
  elsif act == "details"
    r = {}
    doc = Nokogiri::HTML(data).xpath(".")
    return r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}
  end
end

def action()  
  pg = @br.get("http://www.bseindia.com/common/backpageAsset.aspx?inputstr=&strFlag=0&ShowSusp=true&no=0.7173871165763637")
  puts scrape(pg.body,"list",{})
end

action()
