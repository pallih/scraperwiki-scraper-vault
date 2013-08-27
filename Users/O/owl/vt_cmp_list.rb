# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://cgi3.sec.state.vt.us"
  
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
    Nokogiri::HTML(data).xpath(".//form/table/tr[td[not(a)]]").each{|tr|
      type = tr.xpath("./td/text()")
      next if type == "Tradename Records"
      tr.xpath("./following-sibling::tr").each{|tr|
        tmp = s_text(tr.xpath("./td/a/text()"))
        break if tmp.empty? 
        records << {
          "type"=>type,
          "company_name"=>tmp,
          "url"=>append_base(BASE_URL,attributes(tr.xpath("./td/a"),"href")),
          "company_number" => append_base(BASE_URL,attributes(tr.xpath("./td/a"),"href")).split("=").last,
          "doc" => Time.now
        }.merge(rec)
      }
    }
    return records
  end
end

def action(srch)

  @br.get("http://corps.sec.state.vt.us/corpbrow.aspx")
  params = {"form_id"=>"CORPBROW","CORPNAME"=>srch,"submit"=>"Retrieve+Information"}
  pg = @br.post(BASE_URL + "/cgi-shl/nhayer.exe",params)
  tmp = eval(get_metadata("form",""))
  pg = @br.post(BASE_URL + "/cgi-shl/nhayer.exe",tmp) unless tmp.nil? or tmp.empty? 
  begin
    records = scrape(pg.body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],records)

    tmp = attributes(Nokogiri::HTML(pg.body).xpath(".//form/font[1]/input[@type='image' and @src='/images/next(1).gif']"),"src")
    break if tmp.nil? or tmp.empty? or not tmp =~ /next/
    
    
    pg = pg.form_with(:method=>"POST").submit rescue nil
    break if pg.nil? 
    tmp = {}
    pg.form_with(:method=>"POST").fields.each{|f|
      tmp[f.name] = f.value
    }
    save_metadata("form",tmp.to_s)
    sleep(5)
  end while(true)
end

save_metadata("workaround",true)
range = ('a'..'z').to_a + (0..9).to_a
start = get_metadata("start",0)
start = 0 if start>=range.length
range[start..-1].each{|srch|
  action(srch)
  start = start + 1
  save_metadata("start",start)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://cgi3.sec.state.vt.us"
  
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
    Nokogiri::HTML(data).xpath(".//form/table/tr[td[not(a)]]").each{|tr|
      type = tr.xpath("./td/text()")
      next if type == "Tradename Records"
      tr.xpath("./following-sibling::tr").each{|tr|
        tmp = s_text(tr.xpath("./td/a/text()"))
        break if tmp.empty? 
        records << {
          "type"=>type,
          "company_name"=>tmp,
          "url"=>append_base(BASE_URL,attributes(tr.xpath("./td/a"),"href")),
          "company_number" => append_base(BASE_URL,attributes(tr.xpath("./td/a"),"href")).split("=").last,
          "doc" => Time.now
        }.merge(rec)
      }
    }
    return records
  end
end

def action(srch)

  @br.get("http://corps.sec.state.vt.us/corpbrow.aspx")
  params = {"form_id"=>"CORPBROW","CORPNAME"=>srch,"submit"=>"Retrieve+Information"}
  pg = @br.post(BASE_URL + "/cgi-shl/nhayer.exe",params)
  tmp = eval(get_metadata("form",""))
  pg = @br.post(BASE_URL + "/cgi-shl/nhayer.exe",tmp) unless tmp.nil? or tmp.empty? 
  begin
    records = scrape(pg.body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],records)

    tmp = attributes(Nokogiri::HTML(pg.body).xpath(".//form/font[1]/input[@type='image' and @src='/images/next(1).gif']"),"src")
    break if tmp.nil? or tmp.empty? or not tmp =~ /next/
    
    
    pg = pg.form_with(:method=>"POST").submit rescue nil
    break if pg.nil? 
    tmp = {}
    pg.form_with(:method=>"POST").fields.each{|f|
      tmp[f.name] = f.value
    }
    save_metadata("form",tmp.to_s)
    sleep(5)
  end while(true)
end

save_metadata("workaround",true)
range = ('a'..'z').to_a + (0..9).to_a
start = get_metadata("start",0)
start = 0 if start>=range.length
range[start..-1].each{|srch|
  action(srch)
  start = start + 1
  save_metadata("start",start)
}# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://cgi3.sec.state.vt.us"
  
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
    Nokogiri::HTML(data).xpath(".//form/table/tr[td[not(a)]]").each{|tr|
      type = tr.xpath("./td/text()")
      next if type == "Tradename Records"
      tr.xpath("./following-sibling::tr").each{|tr|
        tmp = s_text(tr.xpath("./td/a/text()"))
        break if tmp.empty? 
        records << {
          "type"=>type,
          "company_name"=>tmp,
          "url"=>append_base(BASE_URL,attributes(tr.xpath("./td/a"),"href")),
          "company_number" => append_base(BASE_URL,attributes(tr.xpath("./td/a"),"href")).split("=").last,
          "doc" => Time.now
        }.merge(rec)
      }
    }
    return records
  end
end

def action(srch)

  @br.get("http://corps.sec.state.vt.us/corpbrow.aspx")
  params = {"form_id"=>"CORPBROW","CORPNAME"=>srch,"submit"=>"Retrieve+Information"}
  pg = @br.post(BASE_URL + "/cgi-shl/nhayer.exe",params)
  tmp = eval(get_metadata("form",""))
  pg = @br.post(BASE_URL + "/cgi-shl/nhayer.exe",tmp) unless tmp.nil? or tmp.empty? 
  begin
    records = scrape(pg.body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],records)

    tmp = attributes(Nokogiri::HTML(pg.body).xpath(".//form/font[1]/input[@type='image' and @src='/images/next(1).gif']"),"src")
    break if tmp.nil? or tmp.empty? or not tmp =~ /next/
    
    
    pg = pg.form_with(:method=>"POST").submit rescue nil
    break if pg.nil? 
    tmp = {}
    pg.form_with(:method=>"POST").fields.each{|f|
      tmp[f.name] = f.value
    }
    save_metadata("form",tmp.to_s)
    sleep(5)
  end while(true)
end

save_metadata("workaround",true)
range = ('a'..'z').to_a + (0..9).to_a
start = get_metadata("start",0)
start = 0 if start>=range.length
range[start..-1].each{|srch|
  action(srch)
  start = start + 1
  save_metadata("start",start)
}