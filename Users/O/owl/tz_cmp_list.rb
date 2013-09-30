# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.brela-tz.org"
  
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
    doc = Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@bgcolor='LIGHTYELLOW']/tr[position()>1 and position()<last()]")
    doc.each{|tr|
      r = {}
      r["company_number"] = s_text(tr.xpath("./td[1]/text()"))
      r["company_name"] = s_text(tr.xpath("./td[2]/text()"))

      tmp = Date.strptime(s_text(tr.xpath("./td[3]/text()")),'%d/%m/%Y').to_s rescue nil
      tmp = Date.parse(s_text(tr.xpath("./td[3]/text()"))).to_s rescue nil if tmp.nil? 
      tmp = Date.strptime(s_text(tr.xpath("./td[3]/text()")),'%m/%d/%Y').to_s rescue nil if tmp.nil? 
      #puts tr
      #puts tmp.inspect
      if s_text(tr.xpath("./td[1]/text()")) == s_text(tr.xpath("./td[3]/text()"))
        r["type"] = s_text(tr.xpath("./td[4]/text()"))
      else
        if tmp.nil? 
          r["company_name"] = r["company_name"] + " " + s_text(tr.xpath("./td[3]/text()"))
          tm = Date.strptime(s_text(tr.xpath("./td[4]/text()")),'%d/%m/%Y').to_s rescue nil
          tm = Date.parse(s_text(tr.xpath("./td[4]/text()"))).to_s rescue nil
          if tm.nil? 
            r["company_name"] = r["company_name"] + " " + s_text(tr.xpath("./td[3]/text()")) + " " + s_text(tr.xpath("./td[4]/text()"))
          else
            r["inc_dt"] = tm
          end
        else
          r["inc_dt"] = tmp
          r["type"] = s_text(tr.xpath("./td[4]/text()"))
        end
      end
      raise "Invalid company name found #{r}" if r["company_name"] =~ /\/20[0-9]+/
      puts ["Invalid Date",r].inspect if r["inc_dt"].nil? or r["inc_dt"].empty? 
      records << r.merge(rec)
    }
    return doc.length,records
  end
end

def action()
  pg_no = get_metadata("page_no",1)
  begin
    pg = @br.get(BASE_URL + "/?section=companies&page=search&type=compreg&value=&p=#{pg_no}")
    len,list = scrape(pg.body,"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    break if len.nil? or len < 50 or pg.at("a[@title='Next']").nil? 
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
    sleep(2)
  end while(true)
  delete_metadata("page_no")
end

#save_metadata("page_no",1725)
action()

#puts scrape(@br.get("http://www.brela-tz.org/?section=companies&page=search&type=compname&value=JEDELMAC").body,"list",{})
#puts scrape(@br.get("http://www.brela-tz.org/?section=companies&page=search&type=compname&value=ALLEN WACK & THETHERD LIMITED&p=1").body,"list",{})

# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.brela-tz.org"
  
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
    doc = Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@bgcolor='LIGHTYELLOW']/tr[position()>1 and position()<last()]")
    doc.each{|tr|
      r = {}
      r["company_number"] = s_text(tr.xpath("./td[1]/text()"))
      r["company_name"] = s_text(tr.xpath("./td[2]/text()"))

      tmp = Date.strptime(s_text(tr.xpath("./td[3]/text()")),'%d/%m/%Y').to_s rescue nil
      tmp = Date.parse(s_text(tr.xpath("./td[3]/text()"))).to_s rescue nil if tmp.nil? 
      tmp = Date.strptime(s_text(tr.xpath("./td[3]/text()")),'%m/%d/%Y').to_s rescue nil if tmp.nil? 
      #puts tr
      #puts tmp.inspect
      if s_text(tr.xpath("./td[1]/text()")) == s_text(tr.xpath("./td[3]/text()"))
        r["type"] = s_text(tr.xpath("./td[4]/text()"))
      else
        if tmp.nil? 
          r["company_name"] = r["company_name"] + " " + s_text(tr.xpath("./td[3]/text()"))
          tm = Date.strptime(s_text(tr.xpath("./td[4]/text()")),'%d/%m/%Y').to_s rescue nil
          tm = Date.parse(s_text(tr.xpath("./td[4]/text()"))).to_s rescue nil
          if tm.nil? 
            r["company_name"] = r["company_name"] + " " + s_text(tr.xpath("./td[3]/text()")) + " " + s_text(tr.xpath("./td[4]/text()"))
          else
            r["inc_dt"] = tm
          end
        else
          r["inc_dt"] = tmp
          r["type"] = s_text(tr.xpath("./td[4]/text()"))
        end
      end
      raise "Invalid company name found #{r}" if r["company_name"] =~ /\/20[0-9]+/
      puts ["Invalid Date",r].inspect if r["inc_dt"].nil? or r["inc_dt"].empty? 
      records << r.merge(rec)
    }
    return doc.length,records
  end
end

def action()
  pg_no = get_metadata("page_no",1)
  begin
    pg = @br.get(BASE_URL + "/?section=companies&page=search&type=compreg&value=&p=#{pg_no}")
    len,list = scrape(pg.body,"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    break if len.nil? or len < 50 or pg.at("a[@title='Next']").nil? 
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
    sleep(2)
  end while(true)
  delete_metadata("page_no")
end

#save_metadata("page_no",1725)
action()

#puts scrape(@br.get("http://www.brela-tz.org/?section=companies&page=search&type=compname&value=JEDELMAC").body,"list",{})
#puts scrape(@br.get("http://www.brela-tz.org/?section=companies&page=search&type=compname&value=ALLEN WACK & THETHERD LIMITED&p=1").body,"list",{})

# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.brela-tz.org"
  
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
    doc = Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@bgcolor='LIGHTYELLOW']/tr[position()>1 and position()<last()]")
    doc.each{|tr|
      r = {}
      r["company_number"] = s_text(tr.xpath("./td[1]/text()"))
      r["company_name"] = s_text(tr.xpath("./td[2]/text()"))

      tmp = Date.strptime(s_text(tr.xpath("./td[3]/text()")),'%d/%m/%Y').to_s rescue nil
      tmp = Date.parse(s_text(tr.xpath("./td[3]/text()"))).to_s rescue nil if tmp.nil? 
      tmp = Date.strptime(s_text(tr.xpath("./td[3]/text()")),'%m/%d/%Y').to_s rescue nil if tmp.nil? 
      #puts tr
      #puts tmp.inspect
      if s_text(tr.xpath("./td[1]/text()")) == s_text(tr.xpath("./td[3]/text()"))
        r["type"] = s_text(tr.xpath("./td[4]/text()"))
      else
        if tmp.nil? 
          r["company_name"] = r["company_name"] + " " + s_text(tr.xpath("./td[3]/text()"))
          tm = Date.strptime(s_text(tr.xpath("./td[4]/text()")),'%d/%m/%Y').to_s rescue nil
          tm = Date.parse(s_text(tr.xpath("./td[4]/text()"))).to_s rescue nil
          if tm.nil? 
            r["company_name"] = r["company_name"] + " " + s_text(tr.xpath("./td[3]/text()")) + " " + s_text(tr.xpath("./td[4]/text()"))
          else
            r["inc_dt"] = tm
          end
        else
          r["inc_dt"] = tmp
          r["type"] = s_text(tr.xpath("./td[4]/text()"))
        end
      end
      raise "Invalid company name found #{r}" if r["company_name"] =~ /\/20[0-9]+/
      puts ["Invalid Date",r].inspect if r["inc_dt"].nil? or r["inc_dt"].empty? 
      records << r.merge(rec)
    }
    return doc.length,records
  end
end

def action()
  pg_no = get_metadata("page_no",1)
  begin
    pg = @br.get(BASE_URL + "/?section=companies&page=search&type=compreg&value=&p=#{pg_no}")
    len,list = scrape(pg.body,"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    break if len.nil? or len < 50 or pg.at("a[@title='Next']").nil? 
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
    sleep(2)
  end while(true)
  delete_metadata("page_no")
end

#save_metadata("page_no",1725)
action()

#puts scrape(@br.get("http://www.brela-tz.org/?section=companies&page=search&type=compname&value=JEDELMAC").body,"list",{})
#puts scrape(@br.get("http://www.brela-tz.org/?section=companies&page=search&type=compname&value=ALLEN WACK & THETHERD LIMITED&p=1").body,"list",{})

# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.brela-tz.org"
  
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
    doc = Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@bgcolor='LIGHTYELLOW']/tr[position()>1 and position()<last()]")
    doc.each{|tr|
      r = {}
      r["company_number"] = s_text(tr.xpath("./td[1]/text()"))
      r["company_name"] = s_text(tr.xpath("./td[2]/text()"))

      tmp = Date.strptime(s_text(tr.xpath("./td[3]/text()")),'%d/%m/%Y').to_s rescue nil
      tmp = Date.parse(s_text(tr.xpath("./td[3]/text()"))).to_s rescue nil if tmp.nil? 
      tmp = Date.strptime(s_text(tr.xpath("./td[3]/text()")),'%m/%d/%Y').to_s rescue nil if tmp.nil? 
      #puts tr
      #puts tmp.inspect
      if s_text(tr.xpath("./td[1]/text()")) == s_text(tr.xpath("./td[3]/text()"))
        r["type"] = s_text(tr.xpath("./td[4]/text()"))
      else
        if tmp.nil? 
          r["company_name"] = r["company_name"] + " " + s_text(tr.xpath("./td[3]/text()"))
          tm = Date.strptime(s_text(tr.xpath("./td[4]/text()")),'%d/%m/%Y').to_s rescue nil
          tm = Date.parse(s_text(tr.xpath("./td[4]/text()"))).to_s rescue nil
          if tm.nil? 
            r["company_name"] = r["company_name"] + " " + s_text(tr.xpath("./td[3]/text()")) + " " + s_text(tr.xpath("./td[4]/text()"))
          else
            r["inc_dt"] = tm
          end
        else
          r["inc_dt"] = tmp
          r["type"] = s_text(tr.xpath("./td[4]/text()"))
        end
      end
      raise "Invalid company name found #{r}" if r["company_name"] =~ /\/20[0-9]+/
      puts ["Invalid Date",r].inspect if r["inc_dt"].nil? or r["inc_dt"].empty? 
      records << r.merge(rec)
    }
    return doc.length,records
  end
end

def action()
  pg_no = get_metadata("page_no",1)
  begin
    pg = @br.get(BASE_URL + "/?section=companies&page=search&type=compreg&value=&p=#{pg_no}")
    len,list = scrape(pg.body,"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    break if len.nil? or len < 50 or pg.at("a[@title='Next']").nil? 
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
    sleep(2)
  end while(true)
  delete_metadata("page_no")
end

#save_metadata("page_no",1725)
action()

#puts scrape(@br.get("http://www.brela-tz.org/?section=companies&page=search&type=compname&value=JEDELMAC").body,"list",{})
#puts scrape(@br.get("http://www.brela-tz.org/?section=companies&page=search&type=compname&value=ALLEN WACK & THETHERD LIMITED&p=1").body,"list",{})

