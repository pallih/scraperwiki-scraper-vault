# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://app.mt.gov"
  
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
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  uri = URI.parse(pg.uri.to_s) rescue nil
  base_uri = "#{uri.scheme}://#{uri.host}#{uri.path.split("/")[0..-2].join("/")}" rescue nil
  if act == "length"
    return Nokogiri::HTML(data).xpath(".//table[@width='100%' and @cellpadding='6']/tr[position()>1 and position()<last()-2]").length
  elsif act == "list"
    records = []
    Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@width='100%' and @cellpadding='6']/tr[position()>1 and position()<last()-2]").each{|tr|
      r = {}
      r["company_name"] = s_text(tr.xpath("./td[1]/a/text()")) 
      r["link"] = BASE_URL + attributes(tr.xpath("./td[1]/a"),"href")
      r["company_number"] = URI.parse(r['link']).query.split("&").select{|a| a=~ /^bessearch/}.first.split("=").last.strip rescue nil
      r["type"] = s_text(tr.xpath("./td[2]/text()"))
      r["city"],r["state"] = s_text(tr.xpath("./td[3]/text()")).split(",").pretty
      r["status"] = s_text(tr.xpath("./td[4]/text()"))
      records << r.merge(rec) unless r['company_number'].nil? 
    }
    return records
  end
end

def action()
  range = ('a'..'z').to_a + (0..9).to_a
  rstart = get_metadata("alphabet",0)
  range[rstart..-1].each{|srch|
    lnk = get_metadata("link",(BASE_URL + "/cgi-bin/bes/besCertificate.cgi?bessearch=#{srch}&action=list&submit=Submit+Query"))
    pg = @br.get(lnk) rescue nil
    begin
      raise "blocked" if pg.nil? or pg.uri.to_s =~ /warning/i
      records = scrape(pg,"list",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],records)
      nex = append_base(BASE_URL,attributes(Nokogiri::HTML(pg.body).xpath(".//a[contains(text(),'next>')]"),"href"))  
      break if nex.nil? or nex.empty? or nex == BASE_URL
      pg = @br.get(nex)
      save_metadata("link",nex)
      sleep(20)
    end while(true)
    delete_metadata("link")
    rstart = rstart + 1
    save_metadata("alphabet",rstart)
  }
  delete_metadata("alphabet")
end

action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://app.mt.gov"
  
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
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  uri = URI.parse(pg.uri.to_s) rescue nil
  base_uri = "#{uri.scheme}://#{uri.host}#{uri.path.split("/")[0..-2].join("/")}" rescue nil
  if act == "length"
    return Nokogiri::HTML(data).xpath(".//table[@width='100%' and @cellpadding='6']/tr[position()>1 and position()<last()-2]").length
  elsif act == "list"
    records = []
    Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@width='100%' and @cellpadding='6']/tr[position()>1 and position()<last()-2]").each{|tr|
      r = {}
      r["company_name"] = s_text(tr.xpath("./td[1]/a/text()")) 
      r["link"] = BASE_URL + attributes(tr.xpath("./td[1]/a"),"href")
      r["company_number"] = URI.parse(r['link']).query.split("&").select{|a| a=~ /^bessearch/}.first.split("=").last.strip rescue nil
      r["type"] = s_text(tr.xpath("./td[2]/text()"))
      r["city"],r["state"] = s_text(tr.xpath("./td[3]/text()")).split(",").pretty
      r["status"] = s_text(tr.xpath("./td[4]/text()"))
      records << r.merge(rec) unless r['company_number'].nil? 
    }
    return records
  end
end

def action()
  range = ('a'..'z').to_a + (0..9).to_a
  rstart = get_metadata("alphabet",0)
  range[rstart..-1].each{|srch|
    lnk = get_metadata("link",(BASE_URL + "/cgi-bin/bes/besCertificate.cgi?bessearch=#{srch}&action=list&submit=Submit+Query"))
    pg = @br.get(lnk) rescue nil
    begin
      raise "blocked" if pg.nil? or pg.uri.to_s =~ /warning/i
      records = scrape(pg,"list",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],records)
      nex = append_base(BASE_URL,attributes(Nokogiri::HTML(pg.body).xpath(".//a[contains(text(),'next>')]"),"href"))  
      break if nex.nil? or nex.empty? or nex == BASE_URL
      pg = @br.get(nex)
      save_metadata("link",nex)
      sleep(20)
    end while(true)
    delete_metadata("link")
    rstart = rstart + 1
    save_metadata("alphabet",rstart)
  }
  delete_metadata("alphabet")
end

action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://app.mt.gov"
  
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
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  uri = URI.parse(pg.uri.to_s) rescue nil
  base_uri = "#{uri.scheme}://#{uri.host}#{uri.path.split("/")[0..-2].join("/")}" rescue nil
  if act == "length"
    return Nokogiri::HTML(data).xpath(".//table[@width='100%' and @cellpadding='6']/tr[position()>1 and position()<last()-2]").length
  elsif act == "list"
    records = []
    Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@width='100%' and @cellpadding='6']/tr[position()>1 and position()<last()-2]").each{|tr|
      r = {}
      r["company_name"] = s_text(tr.xpath("./td[1]/a/text()")) 
      r["link"] = BASE_URL + attributes(tr.xpath("./td[1]/a"),"href")
      r["company_number"] = URI.parse(r['link']).query.split("&").select{|a| a=~ /^bessearch/}.first.split("=").last.strip rescue nil
      r["type"] = s_text(tr.xpath("./td[2]/text()"))
      r["city"],r["state"] = s_text(tr.xpath("./td[3]/text()")).split(",").pretty
      r["status"] = s_text(tr.xpath("./td[4]/text()"))
      records << r.merge(rec) unless r['company_number'].nil? 
    }
    return records
  end
end

def action()
  range = ('a'..'z').to_a + (0..9).to_a
  rstart = get_metadata("alphabet",0)
  range[rstart..-1].each{|srch|
    lnk = get_metadata("link",(BASE_URL + "/cgi-bin/bes/besCertificate.cgi?bessearch=#{srch}&action=list&submit=Submit+Query"))
    pg = @br.get(lnk) rescue nil
    begin
      raise "blocked" if pg.nil? or pg.uri.to_s =~ /warning/i
      records = scrape(pg,"list",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],records)
      nex = append_base(BASE_URL,attributes(Nokogiri::HTML(pg.body).xpath(".//a[contains(text(),'next>')]"),"href"))  
      break if nex.nil? or nex.empty? or nex == BASE_URL
      pg = @br.get(nex)
      save_metadata("link",nex)
      sleep(20)
    end while(true)
    delete_metadata("link")
    rstart = rstart + 1
    save_metadata("alphabet",rstart)
  }
  delete_metadata("alphabet")
end

action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://app.mt.gov"
  
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
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  uri = URI.parse(pg.uri.to_s) rescue nil
  base_uri = "#{uri.scheme}://#{uri.host}#{uri.path.split("/")[0..-2].join("/")}" rescue nil
  if act == "length"
    return Nokogiri::HTML(data).xpath(".//table[@width='100%' and @cellpadding='6']/tr[position()>1 and position()<last()-2]").length
  elsif act == "list"
    records = []
    Nokogiri::HTML(data,nil,'ISO-8859-1').xpath(".//table[@width='100%' and @cellpadding='6']/tr[position()>1 and position()<last()-2]").each{|tr|
      r = {}
      r["company_name"] = s_text(tr.xpath("./td[1]/a/text()")) 
      r["link"] = BASE_URL + attributes(tr.xpath("./td[1]/a"),"href")
      r["company_number"] = URI.parse(r['link']).query.split("&").select{|a| a=~ /^bessearch/}.first.split("=").last.strip rescue nil
      r["type"] = s_text(tr.xpath("./td[2]/text()"))
      r["city"],r["state"] = s_text(tr.xpath("./td[3]/text()")).split(",").pretty
      r["status"] = s_text(tr.xpath("./td[4]/text()"))
      records << r.merge(rec) unless r['company_number'].nil? 
    }
    return records
  end
end

def action()
  range = ('a'..'z').to_a + (0..9).to_a
  rstart = get_metadata("alphabet",0)
  range[rstart..-1].each{|srch|
    lnk = get_metadata("link",(BASE_URL + "/cgi-bin/bes/besCertificate.cgi?bessearch=#{srch}&action=list&submit=Submit+Query"))
    pg = @br.get(lnk) rescue nil
    begin
      raise "blocked" if pg.nil? or pg.uri.to_s =~ /warning/i
      records = scrape(pg,"list",{"doc"=>Time.now})
      ScraperWiki.save_sqlite(unique_keys=['company_number'],records)
      nex = append_base(BASE_URL,attributes(Nokogiri::HTML(pg.body).xpath(".//a[contains(text(),'next>')]"),"href"))  
      break if nex.nil? or nex.empty? or nex == BASE_URL
      pg = @br.get(nex)
      save_metadata("link",nex)
      sleep(20)
    end while(true)
    delete_metadata("link")
    rstart = rstart + 1
    save_metadata("alphabet",rstart)
  }
  delete_metadata("alphabet")
end

action()