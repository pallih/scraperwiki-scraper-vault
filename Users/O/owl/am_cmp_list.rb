# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

BASE_URL = "https://www.e-register.am"
  
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
  if act == "details"
    doc = Nokogiri::HTML(data).xpath(".")
    r = {"link"=>pg.uri.to_s}
    tmp = s_text(doc.xpath(".//div[@class='compname']/text()")).split(" - ").strip
    if tmp.length == 2
      r["company_name_in_am"],r["company_name"] = tmp
    elsif tmp.length == 1
      r["company_name_in_am"] = tmp.first
    end
    r["status"] = s_text(doc.xpath(".//td[@class='fnam' and text()='Status']/following-sibling::*[1][self::td]/text()"))
    tmp = s_text(doc.xpath(".//td[@class='fnam' and text()='Registration number:']/following-sibling::*[1][self::td]/text()")).split(" / ")
    r["company_number"] = tmp[0]
    r["reg_dt"] = Date.parse(tmp[1]).to_s
    r["tax_id"] = s_text(doc.xpath(".//td[@class='fnam' and text()='Tax ID:']/following-sibling::*[1][self::td]/text()"))

    tmp = a_text(doc.xpath(".//td[@class='fnam' and text()='Obsoleted by:']/following-sibling::*[1][self::td]")).delete_if{|a| a.empty?}.join(" ").split("/").strip
    r["obsolete_cmp_no"] = tmp[0]
    r["obsoleted_dt"] = tmp[1]
    
    tmp = []
    doc.xpath(".//table[@id='founders']/tr[@class='datarow']").each{|tr|
      tmp << {
        "name" => s_text(tr.xpath("./td[1]/text()")),
        "nationality" => s_text(tr.xpath("./td[2]/text()")),
      }
    }
    r["founders"] = JSON.generate tmp unless tmp.nil? or tmp.empty? 

    return r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}    
  end
end

def action()
  strt = get_metadata("start",894600)
  
  (strt..strt+2000).each{|id|
    pg = @br.get(BASE_URL + "/en/companies/#{id}") rescue nil
    next if pg.body =~ /Invalid company ID/
    record = scrape(pg,"details",{"reference_no"=>id})
    begin
      ScraperWiki.save_sqlite(unique_keys=['reference_no'],record)
      save_metadata("start",id) 
    end unless record.nil? or record.empty? 
    sleep(5)
  }
end

action()