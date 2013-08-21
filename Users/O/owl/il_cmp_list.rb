# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://havarot.justice.gov.il"
  
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
  def to_i
    self.collect{|a|a.to_i}
  end

end

def scrape(data,act,rec)
  if act == "list"
    records = []

    Nokogiri::HTML(data,nil,'UTF-8').xpath(".//table[@id='CPHCenter_dgCompalies']/tr[position()>1]").each{|tr|
      records << {
        "company_number" => s_text(tr.xpath("./td[1]/a/text()")),
        "company_name_hebrew" => attributes(tr.xpath("./td[2]"),"title").strip,
        "company_name_english" => attributes(tr.xpath("./td[3]"),"title").strip,
        "type" => s_text(tr.xpath("./td[4]/text()")),
        "status" => s_text(tr.xpath("./td[5]/text()")),
        "url" => BASE_URL + "/CompaniesDetails.aspx?id=#{s_text(tr.xpath('./td[1]/a/text()'))}",
        "doc" => Time.now
      }.merge(rec)
    }
    
    return records
  end
end

def action()
  pg = @br.get(BASE_URL)
  c,cid = pg.body.scan(/\r\nChallenge=(\d+);\r\nChallengeId=(\d+);\r\n/).flatten.to_i
  key = p1(c)
  pg = @br.post(BASE_URL,{"X-AA-Challenge-ID"=>cid,"X-AA-Challenge-Result"=>key,"X-AA-Challenge"=>c,"Content-Type"=>"text/plain"})
  params = eval(get_metadata("form",'{"ctl00$CPHCenter$txtCompanyName"=>"____","ctl00$CPHCenter$btnSearch"=>"חפש"}'))
  begin
    pg.form_with(:id=>"aspnetForm") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
  
    list = scrape(pg.body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    break if list.nil? or list.length < 10

    params = {"__EVENTTARGET"=>"ctl00$CPHCenter$btnNext"}

    tmp = {}
    pg.form_with(:method=>"POST").fields.each{|f|
      tmp[f.name] = f.value
    }
    save_metadata("form",tmp.to_s)
    sleep(2)
  end while(true)
  delete_metadata("form")
end

action()
