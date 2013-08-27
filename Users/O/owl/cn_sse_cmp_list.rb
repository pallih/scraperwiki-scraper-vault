# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.sse.com.cn"

@br = Mechanize.new {|b|
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
  def downcase
    self.collect{|a| a.strip.downcase}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  uri = URI.parse(pg.uri.to_s) rescue nil
  base_uri = "#{uri.scheme}://#{uri.host}#{uri.path.split("/")[0..-2].join("/")}" rescue nil  
  if act == "list"
    records = []
    Nokogiri::HTML(data,nil,'iso-8859-1').xpath(".//table[@bgcolor='#dbdbdb']/tr[position()>1]").each{|tr|
      records << {
        "code" => s_text(tr.xpath("./td[1]/text()")),
        "name_in_cn" =>s_text(tr.xpath("./td[2]/text()")),
        "short_name" =>s_text(tr.xpath("./td[3]/text()")),
        "name_in_en" =>s_text(tr.xpath("./td[4]/text()")),
        "telephone" =>s_text(tr.xpath("./td[5]/text()")),
        "website" =>s_text(tr.xpath("./td[6]/text()"))
      }.merge(rec)
    }
    return records
  end
end

def action()
  offset = 1
  begin
    pg = @br.get(BASE_URL + "/sseportal/en/jsp/companieslist.jsp?CURSOR=#{offset}") rescue nil
    next if pg.nil? 
    records = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['code'],records)
    break if records.length < 15
    offset = offset + 15
  end while(true)
end


## Action
action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.sse.com.cn"

@br = Mechanize.new {|b|
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
  def downcase
    self.collect{|a| a.strip.downcase}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  uri = URI.parse(pg.uri.to_s) rescue nil
  base_uri = "#{uri.scheme}://#{uri.host}#{uri.path.split("/")[0..-2].join("/")}" rescue nil  
  if act == "list"
    records = []
    Nokogiri::HTML(data,nil,'iso-8859-1').xpath(".//table[@bgcolor='#dbdbdb']/tr[position()>1]").each{|tr|
      records << {
        "code" => s_text(tr.xpath("./td[1]/text()")),
        "name_in_cn" =>s_text(tr.xpath("./td[2]/text()")),
        "short_name" =>s_text(tr.xpath("./td[3]/text()")),
        "name_in_en" =>s_text(tr.xpath("./td[4]/text()")),
        "telephone" =>s_text(tr.xpath("./td[5]/text()")),
        "website" =>s_text(tr.xpath("./td[6]/text()"))
      }.merge(rec)
    }
    return records
  end
end

def action()
  offset = 1
  begin
    pg = @br.get(BASE_URL + "/sseportal/en/jsp/companieslist.jsp?CURSOR=#{offset}") rescue nil
    next if pg.nil? 
    records = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['code'],records)
    break if records.length < 15
    offset = offset + 15
  end while(true)
end


## Action
action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.sse.com.cn"

@br = Mechanize.new {|b|
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
  def downcase
    self.collect{|a| a.strip.downcase}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  uri = URI.parse(pg.uri.to_s) rescue nil
  base_uri = "#{uri.scheme}://#{uri.host}#{uri.path.split("/")[0..-2].join("/")}" rescue nil  
  if act == "list"
    records = []
    Nokogiri::HTML(data,nil,'iso-8859-1').xpath(".//table[@bgcolor='#dbdbdb']/tr[position()>1]").each{|tr|
      records << {
        "code" => s_text(tr.xpath("./td[1]/text()")),
        "name_in_cn" =>s_text(tr.xpath("./td[2]/text()")),
        "short_name" =>s_text(tr.xpath("./td[3]/text()")),
        "name_in_en" =>s_text(tr.xpath("./td[4]/text()")),
        "telephone" =>s_text(tr.xpath("./td[5]/text()")),
        "website" =>s_text(tr.xpath("./td[6]/text()"))
      }.merge(rec)
    }
    return records
  end
end

def action()
  offset = 1
  begin
    pg = @br.get(BASE_URL + "/sseportal/en/jsp/companieslist.jsp?CURSOR=#{offset}") rescue nil
    next if pg.nil? 
    records = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['code'],records)
    break if records.length < 15
    offset = offset + 15
  end while(true)
end


## Action
action()
