# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://vfsc.vu"

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


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "details"
    doc = Nokogiri::HTML(data)
    r = {}
    keys = a_text(doc.xpath(".//table[@id='table1']/tr[position()>1]/td[@width='150' and b]")).delete_if{|a| a.empty?}
    keys.each{|key|
      val = a_text(doc.xpath(".//table[@id='table1']/tr[position()>1 and td[@width='150' and b/text()='#{key}']]/td[3]")).join("\n").strip
      case key
        when "Skrásetingar-nr."
          r["company_number"] = val.to_i
        when "Navn:"
          r["company_name"] = val
        when "Adressa:"
          r["address"] = val
        when "Kommuna:"
          r["municipality"] = val
        when "Hjanøvn:"
          r["alternative_name"] = val
      end
    }
    return r.merge(rec)
  end
end

def action()
  lstart = ScraperWiki.select("max(company_number) as maxid from ocdata").first['maxid']
  (lstart..lstart+20).each{|id|
    pg = @br.get("http://skraseting.skraseting.fo/app/tegning1.asp?id=#{id}")
    next if pg.nil? 
    r = scrape(pg,"details",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(['company_number'],r,'ocdata') unless r['company_number'].nil? 
    sleep(5)
  }
end

action()