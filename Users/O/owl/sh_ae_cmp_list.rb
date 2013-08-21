# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.sharjah.gov.ae"
  
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
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[contains(@id,'gvCompanies')]/tr[position()>1 and position()<last()]").each{|tr|
      r = {}
      r["company_number"] = s_text(tr.xpath("./td[1]/text()"))
      r["company_name"] = s_text(tr.xpath("./td[2]/text()"))
      r["zip"] = s_text(tr.xpath("./td[3]/text()"))
      r["fax"] = s_text(tr.xpath("./td[4]/text()"))
      r["email"] = s_text(tr.xpath("./td[5]/text()"))
      r["telephone"] = s_text(tr.xpath("./td[6]/text()"))
      r["street"] = s_text(tr.xpath("./td[7]/text()"))
      r["activity"] = s_text(tr.xpath("./td[8]/text()"))
      r["doc"] = Time.now
      records << r.merge(rec)
    }
    tmp = attributes(Nokogiri::HTML(data).xpath(".//tr[@class='PagerStyle']/td/table/tr/td[span]/following-sibling::*[1][self::td]/a"),"href").split("'").strip
    return records,tmp[1],tmp[3]
  end
end

def action()
  pg = @br.get(BASE_URL + "/EN/Services/Pages/BusinessDirectory.aspx")
  params = eval(get_metadata("form","{'ctl00$ctl13$g_86e72c28_0aff_4af1_ab95_8300adcf55c4$ctl00$ddlColumns'=>'CompanyName_en', 'ctl00$ctl13$g_86e72c28_0aff_4af1_ab95_8300adcf55c4$ctl00$txtValue'=>'_', 'ctl00$ctl13$g_86e72c28_0aff_4af1_ab95_8300adcf55c4$ctl00$Button1'=>'Search', 'ctl00$ctl13$g_86e72c28_0aff_4af1_ab95_8300adcf55c4$ctl00$rblOptions'=>'0'}"))
  begin
    pg.form_with(:name=>"aspnetForm") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
  end unless params.nil? or params.empty? 
  begin
    list,tar,arg = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    params = {"__EVENTTARGET"=>tar,"__EVENTARGUMENT"=>arg}
    pg.form_with(:name=>"aspnetForm") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
    tmp = {}
    pg.form_with(:name=>"aspnetForm").fields.each{|f|
      tmp[f.name] = f.value
    }
    save_metadata("form",tmp.to_s)
  end while(true)
  delete_metadata("form")
end

action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.sharjah.gov.ae"
  
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
end

def scrape(pg,act,rec)
  data = pg.body rescue data
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[contains(@id,'gvCompanies')]/tr[position()>1 and position()<last()]").each{|tr|
      r = {}
      r["company_number"] = s_text(tr.xpath("./td[1]/text()"))
      r["company_name"] = s_text(tr.xpath("./td[2]/text()"))
      r["zip"] = s_text(tr.xpath("./td[3]/text()"))
      r["fax"] = s_text(tr.xpath("./td[4]/text()"))
      r["email"] = s_text(tr.xpath("./td[5]/text()"))
      r["telephone"] = s_text(tr.xpath("./td[6]/text()"))
      r["street"] = s_text(tr.xpath("./td[7]/text()"))
      r["activity"] = s_text(tr.xpath("./td[8]/text()"))
      r["doc"] = Time.now
      records << r.merge(rec)
    }
    tmp = attributes(Nokogiri::HTML(data).xpath(".//tr[@class='PagerStyle']/td/table/tr/td[span]/following-sibling::*[1][self::td]/a"),"href").split("'").strip
    return records,tmp[1],tmp[3]
  end
end

def action()
  pg = @br.get(BASE_URL + "/EN/Services/Pages/BusinessDirectory.aspx")
  params = eval(get_metadata("form","{'ctl00$ctl13$g_86e72c28_0aff_4af1_ab95_8300adcf55c4$ctl00$ddlColumns'=>'CompanyName_en', 'ctl00$ctl13$g_86e72c28_0aff_4af1_ab95_8300adcf55c4$ctl00$txtValue'=>'_', 'ctl00$ctl13$g_86e72c28_0aff_4af1_ab95_8300adcf55c4$ctl00$Button1'=>'Search', 'ctl00$ctl13$g_86e72c28_0aff_4af1_ab95_8300adcf55c4$ctl00$rblOptions'=>'0'}"))
  begin
    pg.form_with(:name=>"aspnetForm") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
  end unless params.nil? or params.empty? 
  begin
    list,tar,arg = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    params = {"__EVENTTARGET"=>tar,"__EVENTARGUMENT"=>arg}
    pg.form_with(:name=>"aspnetForm") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
    tmp = {}
    pg.form_with(:name=>"aspnetForm").fields.each{|f|
      tmp[f.name] = f.value
    }
    save_metadata("form",tmp.to_s)
  end while(true)
  delete_metadata("form")
end

action()