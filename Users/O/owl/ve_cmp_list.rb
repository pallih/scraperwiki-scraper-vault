# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://rncenlinea.snc.gob.ve"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

class String
  def pretty
    self.strip
  end  
end

class Array
  def pretty
    self.collect{|a| a.strip}
  end
end

def scrape(data,act,rec)
  if act == "list"
    records = []
    Nokogiri::HTML(data.gsub("<UP-ATA.C.A","%3CUP-ATA.C.A")).xpath(".//table/tr[position()>1 and @class]").each{|tr|
      records << {
        "company_number" => s_text(tr.xpath("./td[2]/a/text()")),
        "link" => BASE_URL + attributes(tr.xpath("./td[2]/a"),"href"),
        "alt_number" => attributes(tr.xpath("./td[2]/a"),"href").scan(/index\/(\d+)\?mostrar/).flatten.first,
        "company_name" => s_text(tr.xpath("./td[3]/text()")),
        "status" => s_text(tr.xpath("./td[4]/text()")),
        "nivel" => s_text(tr.xpath("./td[5]/text()")),
        "person" => s_text(tr.xpath("./td[6]/text()")),
        "telephone" => s_text(tr.xpath("./td[7]/text()")),
        "doc" => Time.now
      }
    }
    return records
  end
end

def action()
  start = get_metadata("start",1)
  begin
    records = scrape(@br.get(BASE_URL + "/reportes/resultado_busqueda?nombre=%25&p=0&page=#{start}&search=NOMB").body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],records) unless records.empty? 
    start = (records.empty?)? 1 : (start + 1)
    save_metadata("start",start)
  end while(true)
end

#save_metadata("start",4656)
action()
