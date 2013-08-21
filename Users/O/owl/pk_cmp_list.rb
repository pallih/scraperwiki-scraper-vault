# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.secp.gov.pk/ns/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.gsub(/^,|,$/,'').strip
  end
end

def scrape(pg,act,rec)
  data = pg.body
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//td[@valign='top']/table[@class='text']/tr[td]").each{|tr|
      td = tr.xpath("td")
      records << {
        "tmp_url" => BASE_URL + attributes(td[0].xpath("./a"),"href")
      }
    }
    return records
  elsif act == "details"
    r = {"doc"=>Time.now,"link"=>pg.uri.to_s}
    doc = Nokogiri::HTML(data).xpath(".//table[@class='linkmain']/tr")
    r["company_name"] = s_text(doc.xpath(".//td[normalize-space(text())='Name']/following-sibling::*[1][self::td]/b/text()"))
    r["company_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Registration #']/following-sibling::*[1][self::td]/b/text()"))
    r["incorporated"] = s_text(doc.xpath(".//td[normalize-space(text())='Registration Date']/following-sibling::*[1][self::td]/b/text()"))
    r["old_company_number"] = s_text(doc.xpath(".//td[normalize-space(text())='Old Registration #']/following-sibling::*[1][self::td]/b/text()"))
    r["cro"] = s_text(doc.xpath(".//td[normalize-space(text())='CRO']/following-sibling::*[1][self::td]/b/text()"))
    
    return r unless r["company_name"].nil? or r["company_name"].empty? 
  end
end

def srch()
  range = ('A'..'Z').to_a + (0..9).to_a + ['$','@','#','(','"','-','\'','.']
  rstart = get_metadata("start",0)
  range[rstart..-1].each{|srch|
    list = scrape(@br.post("http://www.secp.gov.pk/ns/searchresult.asp?id=",{"SortBy"=>"a","tName"=>srch,"rSearch"=>"b"}),"list",{})
    start = get_metadata("list",0)
    puts ["list",srch,start,list.length,list].inspect
    list[start..-1].each{|rec|
      begin
        pg = @br.get(rec['tmp_url']) rescue nil
        next if pg.nil? 
        record = scrape(pg,"details",nil)
        ScraperWiki.save_sqlite(unique_keys=['company_number'],record) unless record.nil?   
      end

      start = start + 1
      save_metadata("list",start)
    }
    delete_metadata("list")
    rstart = rstart + 1
    save_metadata("start",start)
  }
  delete_metadata("start")
  save_metadata("#{Time.now}","complete")
end

def range(id)
  record = scrape(@br.get("http://www.secp.gov.pk/ns/company.asp?COMPANY_CODE=#{'%07d' % id}&id="),"details",{}) rescue nil
  ScraperWiki.save_sqlite(unique_keys=['company_number'],record) unless record.nil? 
  save_metadata("offset",id+1) unless record.nil? or record.empty? 
end

start = get_metadata("offset",1)
(start..start+1000).each{|id|
  begin
    range(id)
  end #if ScraperWiki.select("count(*) as c from swdata where company_number=?",['%07d' % id]).first['c'] == 0
}