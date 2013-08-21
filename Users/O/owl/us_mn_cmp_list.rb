# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://mblsportal.sos.state.mn.us"
  
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
  def to_i
    self.collect{|a| a.strip.to_i}
  end
end

def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@class='simpleGrid results selectable highlight']/tr").each{|tr|
      r = {}
      r["company_name"] = s_text(tr.xpath(".//div[@class='businessName']/text()"))
      tmp = a_text(tr.xpath(".//div[@class='details']")).reject(&:empty?).strip
      r["status"] = tmp[tmp.index("Business Status:")+1]
      r["type"] = tmp[tmp.index("Business Type:")+1]
      r["name_type"] = tmp[tmp.index("Name Type:")+1]
      r["link"] = append_base(BASE_URL,attributes(tr.xpath("./td[2]/a"),"href"))
      records << r.merge(rec)
    }
    return records
  end
end

def action(srch)
  records = scrape(@br.get(BASE_URL + "/Business/BusinessSearch?BusinessName=#{srch}&Status=&Type=BeginsWith"),"list",{"doc"=>Time.now})
  ScraperWiki.save_sqlite(unique_keys=['company_name'],records)
  return srch,records.length
end

chr = "A"
begin
  trail = get_metadata("trail",chr).split(">>")
  srch = trail.last
  MAX_T = 500
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
    save_metadata("trail",trail.join(">>"))
    sleep(10)
  end while(true)
end
