# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

BASE_URL = "https://corp.dcra.dc.gov"

@br = Mechanize.new { |b|
  #b.user_agent_alias = 'Linux Firefox'
  b.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:14.0) Gecko/20100101 Firefox/14.0.1"
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    raise e unless e.inspect =~ /no such table/i    
  end
end
def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   raise e unless e.inspect =~ /no such table/i
  end
end
def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   raise e unless e.inspect =~ /no such table/i
  end
end

class String
  def pretty
    self.gsub(/\s+/,' ').strip
  end
end

def s_text(str)
  return str.text.strip.gsub(/\u00A0/,' ').pretty
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='BizEntitySearch_SearchResultsTable']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      tmp = s_text(td[5].xpath("./text()"))
      records << {
        "company_name" => s_text(td[1].xpath("./a/text()")),
        "company_number" => s_text(td[2].xpath("./text()")),
        "link" => BASE_URL + attributes(td[1].xpath("./a"),"href"),
        "effective_dt" => s_text(td[3].xpath("./text()")),
        "status" => s_text(td[4].xpath("./text()")),
        "type" => s_text(td[5].xpath("./text()")),
        "locale" => s_text(td[6].xpath("./text()")),
        "qualifier" => s_text(td[7].xpath("./text()")),
        "doc" => Time.now
      }.merge(rec) unless tmp == "Trade Name" or tmp == "Sole Proprietor" or tmp == "Name Reservation"
    }
    return records
  end
end

def init()
  params = {"username"=>"bob","password"=>"password","LogOn"=>"Log On"}
  @br.post("https://corp.dcra.dc.gov/Account.aspx/LogOn",params)
end

def action()
  list = (0..99).to_a + ('A'..'ZZZ').to_a
  lstart = get_metadata("list",0)
  list[lstart..-1].each{|srch|
    save_metadata("current",srch)
    params = {"BizEntitySearch_String"=>srch,"Search"=>"Search","BizEntitySearch_Type"=>"EntityName","BizEntitySearch_DepthType"=>"StartsWith"}
    list = scrape(@br.post(BASE_URL + "/Home.aspx/ProcessRequest",params).body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    lstart = lstart + 1
    save_metadata("list",lstart)
  }
  delete_metadata("list")
end

init()
action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

BASE_URL = "https://corp.dcra.dc.gov"

@br = Mechanize.new { |b|
  #b.user_agent_alias = 'Linux Firefox'
  b.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:14.0) Gecko/20100101 Firefox/14.0.1"
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    raise e unless e.inspect =~ /no such table/i    
  end
end
def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   raise e unless e.inspect =~ /no such table/i
  end
end
def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   raise e unless e.inspect =~ /no such table/i
  end
end

class String
  def pretty
    self.gsub(/\s+/,' ').strip
  end
end

def s_text(str)
  return str.text.strip.gsub(/\u00A0/,' ').pretty
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='BizEntitySearch_SearchResultsTable']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      tmp = s_text(td[5].xpath("./text()"))
      records << {
        "company_name" => s_text(td[1].xpath("./a/text()")),
        "company_number" => s_text(td[2].xpath("./text()")),
        "link" => BASE_URL + attributes(td[1].xpath("./a"),"href"),
        "effective_dt" => s_text(td[3].xpath("./text()")),
        "status" => s_text(td[4].xpath("./text()")),
        "type" => s_text(td[5].xpath("./text()")),
        "locale" => s_text(td[6].xpath("./text()")),
        "qualifier" => s_text(td[7].xpath("./text()")),
        "doc" => Time.now
      }.merge(rec) unless tmp == "Trade Name" or tmp == "Sole Proprietor" or tmp == "Name Reservation"
    }
    return records
  end
end

def init()
  params = {"username"=>"bob","password"=>"password","LogOn"=>"Log On"}
  @br.post("https://corp.dcra.dc.gov/Account.aspx/LogOn",params)
end

def action()
  list = (0..99).to_a + ('A'..'ZZZ').to_a
  lstart = get_metadata("list",0)
  list[lstart..-1].each{|srch|
    save_metadata("current",srch)
    params = {"BizEntitySearch_String"=>srch,"Search"=>"Search","BizEntitySearch_Type"=>"EntityName","BizEntitySearch_DepthType"=>"StartsWith"}
    list = scrape(@br.post(BASE_URL + "/Home.aspx/ProcessRequest",params).body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    lstart = lstart + 1
    save_metadata("list",lstart)
  }
  delete_metadata("list")
end

init()
action()
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

BASE_URL = "https://corp.dcra.dc.gov"

@br = Mechanize.new { |b|
  #b.user_agent_alias = 'Linux Firefox'
  b.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:14.0) Gecko/20100101 Firefox/14.0.1"
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}


def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    raise e unless e.inspect =~ /no such table/i    
  end
end
def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   raise e unless e.inspect =~ /no such table/i
  end
end
def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   raise e unless e.inspect =~ /no such table/i
  end
end

class String
  def pretty
    self.gsub(/\s+/,' ').strip
  end
end

def s_text(str)
  return str.text.strip.gsub(/\u00A0/,' ').pretty
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='BizEntitySearch_SearchResultsTable']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      tmp = s_text(td[5].xpath("./text()"))
      records << {
        "company_name" => s_text(td[1].xpath("./a/text()")),
        "company_number" => s_text(td[2].xpath("./text()")),
        "link" => BASE_URL + attributes(td[1].xpath("./a"),"href"),
        "effective_dt" => s_text(td[3].xpath("./text()")),
        "status" => s_text(td[4].xpath("./text()")),
        "type" => s_text(td[5].xpath("./text()")),
        "locale" => s_text(td[6].xpath("./text()")),
        "qualifier" => s_text(td[7].xpath("./text()")),
        "doc" => Time.now
      }.merge(rec) unless tmp == "Trade Name" or tmp == "Sole Proprietor" or tmp == "Name Reservation"
    }
    return records
  end
end

def init()
  params = {"username"=>"bob","password"=>"password","LogOn"=>"Log On"}
  @br.post("https://corp.dcra.dc.gov/Account.aspx/LogOn",params)
end

def action()
  list = (0..99).to_a + ('A'..'ZZZ').to_a
  lstart = get_metadata("list",0)
  list[lstart..-1].each{|srch|
    save_metadata("current",srch)
    params = {"BizEntitySearch_String"=>srch,"Search"=>"Search","BizEntitySearch_Type"=>"EntityName","BizEntitySearch_DepthType"=>"StartsWith"}
    list = scrape(@br.post(BASE_URL + "/Home.aspx/ProcessRequest",params).body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    lstart = lstart + 1
    save_metadata("list",lstart)
  }
  delete_metadata("list")
end

init()
action()
