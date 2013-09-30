
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
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='ctl00_PlaceHolderMain_GridViewCompanies']/tr[position()>1]").each{|tr|
      r = {}
      r["company_number"] = s_text(tr.xpath("./td[2]/text()")).to_i
      r["company_name"] = s_text(tr.xpath("./td[3]/text()"))
      r["type"] = s_text(tr.xpath("./td[4]/text()"))
      records << r.merge(rec)
    }
    return records
  end
end
