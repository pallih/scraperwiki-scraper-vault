# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'
require 'logger'

BASE_URL = "http://goir.ap.gov.in"
  
@br = Mechanize.new { |b|
  b.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:15.0) Gecko/20100101 Firefox/15.0.1'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
#  b.log = Logger.new(STDERR)
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
    Nokogiri::HTML(data).xpath(".//table[@id='ctl00_ContentPlaceHolder1_FileMoveList2']/tr[position()>1]").each{|tr|
      records << {
        "type" => s_text(tr.xpath("./td[3]/text()")),
        "go_no" => s_text(tr.xpath("./td[4]/text()")),
        "published_dt" => Date.strptime(s_text(tr.xpath("./td[5]/text()")),'%d/%m/%Y').to_s,
        "category" => s_text(tr.xpath("./td[6]/text()")),
        "abstract" => s_text(tr.xpath("./td[7]/text()")),
        "department" => s_text(tr.xpath("./td[9]/text()")),
        "section" => s_text(tr.xpath("./td[10]/text()")),
        "amount" => s_text(tr.xpath("./td[11]/text()")),
      }.merge(rec)
    }
    return records
  end
end

def action(dt_f,dt_t)
  params = {"__EVENTTARGET"=>"", "__EVENTARGUMENT"=>"", "__LASTFOCUS"=>"", "ctl00$ContentPlaceHolder1$radio"=>"RdBtnGo", "ctl00$ContentPlaceHolder1$DDLDeptname"=>"Select", "ctl00$ContentPlaceHolder1$DDLGoType"=>"Select", "ctl00$ContentPlaceHolder1$DdlGo_cat"=>"Select", "ctl00$ContentPlaceHolder1$txtGoNo"=>"", "ctl00$ContentPlaceHolder1$txtfrmdate"=>dt_f.strftime("%d%m%Y"), "ctl00$ContentPlaceHolder1$txttodate"=>dt_t.strftime("%d%m%Y"), "ctl00$ContentPlaceHolder1$fAmount"=>"", "ctl00$ContentPlaceHolder1$tAmount"=>"", "ctl00$ContentPlaceHolder1$txtSearchText"=>"", "ctl00$ContentPlaceHolder1$BtnSearch"=>"search","ctl00$ContentPlaceHolder1$ddlPages"=>"100"}
  pg = @br.get("http://goir.ap.gov.in/Reports.aspx")
  tmp = {}
  pg.form_with(:name => "aspnetForm").fields.each{|f|
    tmp[f.name] = CGI::escape(f.value) unless f.value.nil? 
  }
  str = ""
  tmp.merge(params).collect{|k,v| str = str+"#{k}=#{v}&" }
  pg = @br.post("http://goir.ap.gov.in/Reports.aspx",str,{"Content-Type"=>"application/x-www-form-urlencoded"})
  list = scrape(pg.body,"list",{})
  ScraperWiki.save_sqlite(unique_keys=['go_no','published_dt','department','section','category','abstract'],list)
end

#start = Date.parse(get_metadata("start","2012-01-01"))
#(start..Date.parse(Time.now.to_s)).each{|dt|
#  action(dt,dt)
#  save_metadata("start",dt.to_s)
#}

action(Date.parse("1999-01-01"),Date.parse("1999-01-31"))