# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://rgd.bahamas.gov.bs:8081"

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
    Nokogiri::HTML(data).xpath(".//table[@width='95%']/tr[position()>1]").each{|tr|
      records << {
        "type" => s_text(tr.xpath("./td[2]/small/font/text()")),
        "company_number" => s_text(tr.xpath("./td[3]/small/font/text()")),
        "company_name" => s_text(tr.xpath("./td[4]/small/font/text()")),
        "stng" => s_text(tr.xpath("./td[5]/bold/font/text()")),
      }.merge(rec)
    }
    return records
  end
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  params = {"cnam"=>srch,"x"=>"2","y"=>srch,"action"=>"Search Again"}
  pg = br.post(BASE_URL+"/netdata/db2www.pgm/findcompany.ndm/showcomps?retfield=ctyp&retfield2=cnum&retfield3=cnam&formname=selectcompany",params)
  list = scrape(pg.body,"list",{"doc"=>Time.now})
  ScraperWiki.save_sqlite(['company_number'],list)
end

save_metadata("wa",true)

begin
  trail = get_metadata("trail","A").split(">>")
  srch = trail.last
  MAX_T = 20
  begin
    prev,ret = action(srch)
    if ret >= MAX_T
      srch = srch + "A"
      trail << srch
    else
      tmp = ''
      begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
      end
    end
    puts [ret,prev,srch,trail.join(">>")].inspect
    save_metadata("trail",trail.join(">>"))
    sleep(5)
  end while(true)
end
delete_metadata("trail")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://rgd.bahamas.gov.bs:8081"

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
    Nokogiri::HTML(data).xpath(".//table[@width='95%']/tr[position()>1]").each{|tr|
      records << {
        "type" => s_text(tr.xpath("./td[2]/small/font/text()")),
        "company_number" => s_text(tr.xpath("./td[3]/small/font/text()")),
        "company_name" => s_text(tr.xpath("./td[4]/small/font/text()")),
        "stng" => s_text(tr.xpath("./td[5]/bold/font/text()")),
      }.merge(rec)
    }
    return records
  end
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  params = {"cnam"=>srch,"x"=>"2","y"=>srch,"action"=>"Search Again"}
  pg = br.post(BASE_URL+"/netdata/db2www.pgm/findcompany.ndm/showcomps?retfield=ctyp&retfield2=cnum&retfield3=cnam&formname=selectcompany",params)
  list = scrape(pg.body,"list",{"doc"=>Time.now})
  ScraperWiki.save_sqlite(['company_number'],list)
end

save_metadata("wa",true)

begin
  trail = get_metadata("trail","A").split(">>")
  srch = trail.last
  MAX_T = 20
  begin
    prev,ret = action(srch)
    if ret >= MAX_T
      srch = srch + "A"
      trail << srch
    else
      tmp = ''
      begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
      end
    end
    puts [ret,prev,srch,trail.join(">>")].inspect
    save_metadata("trail",trail.join(">>"))
    sleep(5)
  end while(true)
end
delete_metadata("trail")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://rgd.bahamas.gov.bs:8081"

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
    Nokogiri::HTML(data).xpath(".//table[@width='95%']/tr[position()>1]").each{|tr|
      records << {
        "type" => s_text(tr.xpath("./td[2]/small/font/text()")),
        "company_number" => s_text(tr.xpath("./td[3]/small/font/text()")),
        "company_name" => s_text(tr.xpath("./td[4]/small/font/text()")),
        "stng" => s_text(tr.xpath("./td[5]/bold/font/text()")),
      }.merge(rec)
    }
    return records
  end
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  params = {"cnam"=>srch,"x"=>"2","y"=>srch,"action"=>"Search Again"}
  pg = br.post(BASE_URL+"/netdata/db2www.pgm/findcompany.ndm/showcomps?retfield=ctyp&retfield2=cnum&retfield3=cnam&formname=selectcompany",params)
  list = scrape(pg.body,"list",{"doc"=>Time.now})
  ScraperWiki.save_sqlite(['company_number'],list)
end

save_metadata("wa",true)

begin
  trail = get_metadata("trail","A").split(">>")
  srch = trail.last
  MAX_T = 20
  begin
    prev,ret = action(srch)
    if ret >= MAX_T
      srch = srch + "A"
      trail << srch
    else
      tmp = ''
      begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
      end
    end
    puts [ret,prev,srch,trail.join(">>")].inspect
    save_metadata("trail",trail.join(">>"))
    sleep(5)
  end while(true)
end
delete_metadata("trail")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://rgd.bahamas.gov.bs:8081"

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
    Nokogiri::HTML(data).xpath(".//table[@width='95%']/tr[position()>1]").each{|tr|
      records << {
        "type" => s_text(tr.xpath("./td[2]/small/font/text()")),
        "company_number" => s_text(tr.xpath("./td[3]/small/font/text()")),
        "company_name" => s_text(tr.xpath("./td[4]/small/font/text()")),
        "stng" => s_text(tr.xpath("./td[5]/bold/font/text()")),
      }.merge(rec)
    }
    return records
  end
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  params = {"cnam"=>srch,"x"=>"2","y"=>srch,"action"=>"Search Again"}
  pg = br.post(BASE_URL+"/netdata/db2www.pgm/findcompany.ndm/showcomps?retfield=ctyp&retfield2=cnum&retfield3=cnam&formname=selectcompany",params)
  list = scrape(pg.body,"list",{"doc"=>Time.now})
  ScraperWiki.save_sqlite(['company_number'],list)
end

save_metadata("wa",true)

begin
  trail = get_metadata("trail","A").split(">>")
  srch = trail.last
  MAX_T = 20
  begin
    prev,ret = action(srch)
    if ret >= MAX_T
      srch = srch + "A"
      trail << srch
    else
      tmp = ''
      begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
      end
    end
    puts [ret,prev,srch,trail.join(">>")].inspect
    save_metadata("trail",trail.join(">>"))
    sleep(5)
  end while(true)
end
delete_metadata("trail")
