# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.difc.ae"
  
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
    Nokogiri::HTML(data).xpath(".//table[@id='browse-directory']/tbody/tr").each{|tr|
      td = tr.xpath("td")
      r = {}
      r["company_name"] = s_text(td[0].xpath("./a/text()"))
      r["company_number"] = s_text(td[1].xpath("./text()"))
      r["doc"] = Time.now
      tmp = s_text(td[2].xpath("./text()"))
      r["status"] = tmp
      r["link"] = append_base(BASE_URL,attributes(tr.xpath("./td[1]/a"),"href"))
  
      records << r.merge(rec)
    }
    return records
  end
end

def action()
  pg_no = get_metadata("page_no",0)
  begin
    list = scrape(@br.get(BASE_URL + "/browse-directory?page=#{pg_no}").body,"list",{})
    ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
    break if list.nil? or list.empty? or list.length < 30
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
  end while(true)
  delete_metadata("page_no")
end

action()
