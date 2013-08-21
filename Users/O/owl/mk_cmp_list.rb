# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.crm.com.mk"
  
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
    Nokogiri::HTML(data).xpath(".//table[@id='cphMain_ctl00_ucPADArchiveContent_ucConAnnouncements_dgAnnouncements']/tr[position()>1 and position()<last()]").each{|tr|
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/a[contains(@id,'DocumentID')]/text()")),
        "company_name" => s_text(tr.xpath("./td[2]/text()")),
        "doc" => Time.now
      }.merge(rec)
    }
    return records
  end
end

def action(dt_f,dt_t)
  pg = @br.get(BASE_URL + "/ds/default.aspx?MainId=3")
  params = {"ctl00$ddlLanguages"=>"mk-MK", "ctl00$cphMain$ctl00$ucPADArchiveContent$ddlDocTypeID"=>"100", "ctl00$cphMain$ctl00$ucPADArchiveContent$DtpFrom$TxtDateCtrl"=>dt_f.strftime('%d.%m.%Y'), "ctl00$cphMain$ctl00$ucPADArchiveContent$DtpTo$TxtDateCtrl"=>dt_t.strftime('%d.%m.%Y'),"ctl00$cphMain$ctl00$ucPADArchiveContent$imgbLoadAnnounc.x"=>"29", "ctl00$cphMain$ctl00$ucPADArchiveContent$imgbLoadAnnounc.y"=>"22"}
  begin
    pg.form_with(:id => "frmInfoContent") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
    list = scrape(pg.body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)

    nex = attributes(Nokogiri::HTML(pg.body).xpath(".//tr[@class='Pager']/td/span/following-sibling::*[1][self::a]"),"href").split("'")[1]
    break if nex.nil? or nex.empty? or list.length < 100
    params["__EVENTTARGET"] = nex
    params.delete("ctl00$cphMain$ctl00$ucPADArchiveContent$imgbLoadAnnounc.x")
    params.delete("ctl00$cphMain$ctl00$ucPADArchiveContent$imgbLoadAnnounc.y")
  end while(true)
end

start = Date.parse(get_metadata("start","2006-01-01"))
(start..Date.parse(Time.now.to_s)).each{|dt|
  action(dt-30,dt)
  save_metadata("start",dt.to_s)
}
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.crm.com.mk"
  
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
    Nokogiri::HTML(data).xpath(".//table[@id='cphMain_ctl00_ucPADArchiveContent_ucConAnnouncements_dgAnnouncements']/tr[position()>1 and position()<last()]").each{|tr|
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/a[contains(@id,'DocumentID')]/text()")),
        "company_name" => s_text(tr.xpath("./td[2]/text()")),
        "doc" => Time.now
      }.merge(rec)
    }
    return records
  end
end

def action(dt_f,dt_t)
  pg = @br.get(BASE_URL + "/ds/default.aspx?MainId=3")
  params = {"ctl00$ddlLanguages"=>"mk-MK", "ctl00$cphMain$ctl00$ucPADArchiveContent$ddlDocTypeID"=>"100", "ctl00$cphMain$ctl00$ucPADArchiveContent$DtpFrom$TxtDateCtrl"=>dt_f.strftime('%d.%m.%Y'), "ctl00$cphMain$ctl00$ucPADArchiveContent$DtpTo$TxtDateCtrl"=>dt_t.strftime('%d.%m.%Y'),"ctl00$cphMain$ctl00$ucPADArchiveContent$imgbLoadAnnounc.x"=>"29", "ctl00$cphMain$ctl00$ucPADArchiveContent$imgbLoadAnnounc.y"=>"22"}
  begin
    pg.form_with(:id => "frmInfoContent") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
    list = scrape(pg.body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)

    nex = attributes(Nokogiri::HTML(pg.body).xpath(".//tr[@class='Pager']/td/span/following-sibling::*[1][self::a]"),"href").split("'")[1]
    break if nex.nil? or nex.empty? or list.length < 100
    params["__EVENTTARGET"] = nex
    params.delete("ctl00$cphMain$ctl00$ucPADArchiveContent$imgbLoadAnnounc.x")
    params.delete("ctl00$cphMain$ctl00$ucPADArchiveContent$imgbLoadAnnounc.y")
  end while(true)
end

start = Date.parse(get_metadata("start","2006-01-01"))
(start..Date.parse(Time.now.to_s)).each{|dt|
  action(dt-30,dt)
  save_metadata("start",dt.to_s)
}
