# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "http://www.crps.me"
  
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
    Nokogiri::HTML(data).xpath(".//table[@id='admin']/tr[position()>1]").each{|tr|
      r = {}
      r["company_number"] = s_text(tr.xpath("./td[1]/text()")).split("/")[0]
      r["identification_no"] = s_text(tr.xpath("./td[2]/text()"))
      r["type"] = s_text(tr.xpath("./td[3]/text()"))
      r["company_name"] = s_text(tr.xpath("./td[4]/text()"))
      r["activity"] = s_text(tr.xpath("./td[5]/text()"))
      r["place"] = s_text(tr.xpath("./td[6]/text()"))
      r["status"] = s_text(tr.xpath("./td[7]/text()"))
      tmp = attributes(tr.xpath("./td[8]/form/input[@name='idDosijea']"),"value")
      r["reference_no"] = tmp
      r["link"] = "http://www.crps.me/CRPSPublic/prikazidrustvo.action?idDosijea=#{tmp}"
      r["doc"] = Time.now
      records << r.merge(rec)
    }
    return records
  end
end

def action()
  strt = get_metadata("start",0)
  begin
    pg = @br.get(BASE_URL + "/CRPSPublic/rezultatpretrageregistra.action?od=#{strt}&privrednaDjelatnost=0&naziv=&opstina=0&lice=&djelatnostId=&sortiranje=1&regBr=&prikazati=0")
    list = scrape(pg,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)

    break if list.nil? or list.empty? or list.length < 15
    strt = strt + 15
    save_metadata("start",strt) 
    sleep(5)
  end while(true)
  delete_metadata("start")
end

action()