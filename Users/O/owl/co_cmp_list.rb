# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'csv'
require 'scrapers/cf'

BASE_URL = "http://www.supersociedades.gov.co/ss/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
class String
  def pretty
    self.strip
  end
end


def scrape(data,act)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//td[@width='100%']/table[@width='100%' and not(@bgcolor)]/tr[position()>3]").each{|tr|
      td = tr.xpath("td")
      records << {
        "company_number" => s_text(td[0].xpath("./font/a/text()")),
        "company_name" => s_text(td[1].xpath("./font/text()")),
        "url" => BASE_URL + attributes(td[0].xpath("./font/a"),"href"),
        "doc" => Time.now
      }
    }
    return records
  end
end

def action(srch)
  begin
    cap = 5000
    offset = get_metadata("offset",1)
    begin
      pg = @br.get(BASE_URL + "drvisapi.dll?MIval=ppal&dir=104&START=#{offset}&WINSIZE=#{cap}&tipo=2&razso=#{srch}")
      list = scrape(pg.body,"list")
      ScraperWiki.save_sqlite(unique_keys=['company_number'],list) unless list.nil? or list.empty? 
      tmp = s_text(Nokogiri::HTML(pg.body).xpath(".//a/font[contains(text(),'Siguientes')]/text()"))
      break if tmp.empty? or list.nil? or list.empty? or list.length < cap
      offset = offset + cap
    end while(true)
  rescue Exception => e
    raise e
  end
end

range = ('A'..'Z').to_a + (0..9).to_a + ['#','@','.']
start = get_metadata("start",0)
range[start..-1].each_with_index{|srch,idx|
  action(srch)
  save_metadata("start",start + idx)
}
delete_metadata("start")# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'csv'
require 'scrapers/cf'

BASE_URL = "http://www.supersociedades.gov.co/ss/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
class String
  def pretty
    self.strip
  end
end


def scrape(data,act)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//td[@width='100%']/table[@width='100%' and not(@bgcolor)]/tr[position()>3]").each{|tr|
      td = tr.xpath("td")
      records << {
        "company_number" => s_text(td[0].xpath("./font/a/text()")),
        "company_name" => s_text(td[1].xpath("./font/text()")),
        "url" => BASE_URL + attributes(td[0].xpath("./font/a"),"href"),
        "doc" => Time.now
      }
    }
    return records
  end
end

def action(srch)
  begin
    cap = 5000
    offset = get_metadata("offset",1)
    begin
      pg = @br.get(BASE_URL + "drvisapi.dll?MIval=ppal&dir=104&START=#{offset}&WINSIZE=#{cap}&tipo=2&razso=#{srch}")
      list = scrape(pg.body,"list")
      ScraperWiki.save_sqlite(unique_keys=['company_number'],list) unless list.nil? or list.empty? 
      tmp = s_text(Nokogiri::HTML(pg.body).xpath(".//a/font[contains(text(),'Siguientes')]/text()"))
      break if tmp.empty? or list.nil? or list.empty? or list.length < cap
      offset = offset + cap
    end while(true)
  rescue Exception => e
    raise e
  end
end

range = ('A'..'Z').to_a + (0..9).to_a + ['#','@','.']
start = get_metadata("start",0)
range[start..-1].each_with_index{|srch,idx|
  action(srch)
  save_metadata("start",start + idx)
}
delete_metadata("start")# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'csv'
require 'scrapers/cf'

BASE_URL = "http://www.supersociedades.gov.co/ss/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
class String
  def pretty
    self.strip
  end
end


def scrape(data,act)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//td[@width='100%']/table[@width='100%' and not(@bgcolor)]/tr[position()>3]").each{|tr|
      td = tr.xpath("td")
      records << {
        "company_number" => s_text(td[0].xpath("./font/a/text()")),
        "company_name" => s_text(td[1].xpath("./font/text()")),
        "url" => BASE_URL + attributes(td[0].xpath("./font/a"),"href"),
        "doc" => Time.now
      }
    }
    return records
  end
end

def action(srch)
  begin
    cap = 5000
    offset = get_metadata("offset",1)
    begin
      pg = @br.get(BASE_URL + "drvisapi.dll?MIval=ppal&dir=104&START=#{offset}&WINSIZE=#{cap}&tipo=2&razso=#{srch}")
      list = scrape(pg.body,"list")
      ScraperWiki.save_sqlite(unique_keys=['company_number'],list) unless list.nil? or list.empty? 
      tmp = s_text(Nokogiri::HTML(pg.body).xpath(".//a/font[contains(text(),'Siguientes')]/text()"))
      break if tmp.empty? or list.nil? or list.empty? or list.length < cap
      offset = offset + cap
    end while(true)
  rescue Exception => e
    raise e
  end
end

range = ('A'..'Z').to_a + (0..9).to_a + ['#','@','.']
start = get_metadata("start",0)
range[start..-1].each_with_index{|srch,idx|
  action(srch)
  save_metadata("start",start + idx)
}
delete_metadata("start")# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'sqlite3'
require 'json'
require 'csv'
require 'scrapers/cf'

BASE_URL = "http://www.supersociedades.gov.co/ss/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
class String
  def pretty
    self.strip
  end
end


def scrape(data,act)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//td[@width='100%']/table[@width='100%' and not(@bgcolor)]/tr[position()>3]").each{|tr|
      td = tr.xpath("td")
      records << {
        "company_number" => s_text(td[0].xpath("./font/a/text()")),
        "company_name" => s_text(td[1].xpath("./font/text()")),
        "url" => BASE_URL + attributes(td[0].xpath("./font/a"),"href"),
        "doc" => Time.now
      }
    }
    return records
  end
end

def action(srch)
  begin
    cap = 5000
    offset = get_metadata("offset",1)
    begin
      pg = @br.get(BASE_URL + "drvisapi.dll?MIval=ppal&dir=104&START=#{offset}&WINSIZE=#{cap}&tipo=2&razso=#{srch}")
      list = scrape(pg.body,"list")
      ScraperWiki.save_sqlite(unique_keys=['company_number'],list) unless list.nil? or list.empty? 
      tmp = s_text(Nokogiri::HTML(pg.body).xpath(".//a/font[contains(text(),'Siguientes')]/text()"))
      break if tmp.empty? or list.nil? or list.empty? or list.length < cap
      offset = offset + cap
    end while(true)
  rescue Exception => e
    raise e
  end
end

range = ('A'..'Z').to_a + (0..9).to_a + ['#','@','.']
start = get_metadata("start",0)
range[start..-1].each_with_index{|srch,idx|
  action(srch)
  save_metadata("start",start + idx)
}
delete_metadata("start")