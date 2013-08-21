# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://cgov.sos.state.ga.us"

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
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='BizEntitySearch_SearchResultsTable']/tbody/tr").each{|tr|
      r = {}
      r["company_name"] = s_text(tr.xpath("./td[2]/a/text()"))
      r["control_number"] = s_text(tr.xpath("./td[3]/text()"))
      r["effective_dt"] = Date.parse(s_text(tr.xpath("./td[4]/text()"))).to_s
      r["status"] = s_text(tr.xpath("./td[5]/text()"))
      r["type"] = s_text(tr.xpath("./td[6]/text()"))
      r["locale"] = s_text(tr.xpath("./td[7]/text()"))
      r["qualifier"] = s_text(tr.xpath("./td[8]/text()"))
      r["link"] = append_base(BASE_URL,attributes(tr.xpath("./td[2]/a"),"href"))
      r["entity_id"] = URI.parse(r['link']).query.split("&").select{|a| a=~ /^entityId/}.first.split("=")[1]

      return r.merge(rec)
    }
    return records
  end
end

def action(srch)
  pg = @br.post(BASE_URL + "/Account.aspx/SearchRequest",{
        "BizEntitySearch_String"=>srch,
        "Search"=>"Search",
        "BizEntitySearch_Type"=>"EntityName",
        "BizEntitySearch_DepthType"=>"StartsWith"})
  list = scrape(pg,"list",{"doc"=>Time.now})
  ScraperWiki.save_sqlite(unique_keys=['entity_id'],list)
  return srch,list.length
end

begin
  chr = "A"
  trail = get_metadata("trail",chr).split(">>")
  srch = trail.last
  MAX_T = 250
  begin
    prev,ret = action(srch)
    if ret >= MAX_T
      srch = srch + "A"
      trail << srch
    else
      tmp = ''
      begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
      if tmp.nil? 
        trail == ["A"]
      else
        srch = (tmp == 'Z')? "A" : tmp.next
        trail << srch
      end
    end
    puts [ret,prev,srch,trail.join(">>")].inspect
    save_metadata("trail",trail.join(">>"))
    sleep(10)
  end while(true)
end