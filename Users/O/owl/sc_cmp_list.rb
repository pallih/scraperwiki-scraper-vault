# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "https://eservice.egov.sc"

@br = Mechanize.new {|b|
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
  def pretty
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='tableResults']/tbody/tr").each{|tr|
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/text()")),
        "company_name" => s_text(tr.xpath("./td[2]/text()")),
        "industry" => s_text(tr.xpath("./td[3]/text()")),
        "type" => s_text(tr.xpath("./td[4]/text()")),
        "doc" => Time.now
      }.merge(rec)
    }
    return records
  end
end

def action()
  range = ('A'..'ZZZ').to_a + (0..100).to_a
  rstart = get_metadata("range",0)
  pg = @br.get("https://eservice.egov.sc/BizRegistration/WebSearchBusiness.aspx")
  range[rstart..-1].each{|chr|
    tmp = {}
    pg.form_with(:name=>"aspnetForm").fields.each{|f|
      tmp[f.name] = f.value
    }
    tmp["ctl00$ContentPlaceHolder1$txtSearch"] = chr
    tmp["ctl00$ContentPlaceHolder1$btnSearch"] = "Search"
    pg_tmp = @br.post("https://eservice.egov.sc/BizRegistration/WebSearchBusiness.aspx",tmp) rescue nil
    next if pg_tmp.nil? 
    list = scrape(pg_tmp,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    rstart = rstart + 1
    save_metadata("range",rstart)
  }
  delete_metadata("range")
end

save_metadata("workaround",true)
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "https://eservice.egov.sc"

@br = Mechanize.new {|b|
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
  def pretty
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='tableResults']/tbody/tr").each{|tr|
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/text()")),
        "company_name" => s_text(tr.xpath("./td[2]/text()")),
        "industry" => s_text(tr.xpath("./td[3]/text()")),
        "type" => s_text(tr.xpath("./td[4]/text()")),
        "doc" => Time.now
      }.merge(rec)
    }
    return records
  end
end

def action()
  range = ('A'..'ZZZ').to_a + (0..100).to_a
  rstart = get_metadata("range",0)
  pg = @br.get("https://eservice.egov.sc/BizRegistration/WebSearchBusiness.aspx")
  range[rstart..-1].each{|chr|
    tmp = {}
    pg.form_with(:name=>"aspnetForm").fields.each{|f|
      tmp[f.name] = f.value
    }
    tmp["ctl00$ContentPlaceHolder1$txtSearch"] = chr
    tmp["ctl00$ContentPlaceHolder1$btnSearch"] = "Search"
    pg_tmp = @br.post("https://eservice.egov.sc/BizRegistration/WebSearchBusiness.aspx",tmp) rescue nil
    next if pg_tmp.nil? 
    list = scrape(pg_tmp,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    rstart = rstart + 1
    save_metadata("range",rstart)
  }
  delete_metadata("range")
end

save_metadata("workaround",true)
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "https://eservice.egov.sc"

@br = Mechanize.new {|b|
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
  def pretty
    self.collect{|a|a.strip}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='tableResults']/tbody/tr").each{|tr|
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/text()")),
        "company_name" => s_text(tr.xpath("./td[2]/text()")),
        "industry" => s_text(tr.xpath("./td[3]/text()")),
        "type" => s_text(tr.xpath("./td[4]/text()")),
        "doc" => Time.now
      }.merge(rec)
    }
    return records
  end
end

def action()
  range = ('A'..'ZZZ').to_a + (0..100).to_a
  rstart = get_metadata("range",0)
  pg = @br.get("https://eservice.egov.sc/BizRegistration/WebSearchBusiness.aspx")
  range[rstart..-1].each{|chr|
    tmp = {}
    pg.form_with(:name=>"aspnetForm").fields.each{|f|
      tmp[f.name] = f.value
    }
    tmp["ctl00$ContentPlaceHolder1$txtSearch"] = chr
    tmp["ctl00$ContentPlaceHolder1$btnSearch"] = "Search"
    pg_tmp = @br.post("https://eservice.egov.sc/BizRegistration/WebSearchBusiness.aspx",tmp) rescue nil
    next if pg_tmp.nil? 
    list = scrape(pg_tmp,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    rstart = rstart + 1
    save_metadata("range",rstart)
  }
  delete_metadata("range")
end

save_metadata("workaround",true)
action()