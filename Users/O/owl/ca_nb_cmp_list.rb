# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

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
  def strip
    self.collect{|a|a.strip}
  end
end


def scrape(pg,act,rec)
  data = pg.body rescue pg
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data)
    doc.xpath(".//table[@id='cphMain_gvResults']/tr[position()>1 and position()<last()]").each{|tr|
      r = {}
      r["company_number"] = s_text(tr.xpath("./td[1]/a/text()"))
      r["status"] = s_text(tr.xpath("./td[2]/a/text()"))
      r["flag"] = s_text(tr.xpath("./td[3]/a/text()"))
      r["company_name"] = s_text(tr.xpath("./td[4]/a/text()"))
      records << r.merge(rec)
    }
    return records,attributes(doc.xpath(".//table[@id='cphMain_gvResults']/tr[position()=last()]/td/font/table/tr/td[font/span]/following-sibling::*[1][self::td]/font/a"),"href").split("'")[3],s_text(doc.xpath(".//span[@id='cphMain_lblResultsHeader']/text()"))
  end
end

def action(srch)
  pg = @br.get("https://www.pxw2.snb.ca/card_online/Search/search.aspx") if @pg.nil? 
  params = {"ctl00$cphMain$txtKeyWordSingle"=>srch,"ctl00$cphMain$btnKeyWordSingle"=>"Search"}
  begin
    pg.form_with(:id=>"Main") do |f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
    list,nex,hdr = scrape(pg,"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(['company_number'],list)
    puts [nex,list.length,hdr].inspect
    break if list.nil? or list.empty? or list.length < 100 or nex.nil? or nex.empty? 
    params = {"__EVENTTARGET"=>"ctl00$cphMain$gvResults","__EVENTARGUMENT"=>nex}
  end while(true)
end

list = ('AA'..'ZZ').to_a + ('00'..'99').to_a
lstart = get_metadata("list",0)
list[lstart..-1].each{|srch|
  save_metadata("search",srch)
  action(srch)
  lstart = lstart + 1
  save_metadata("list",lstart)
}
delete_metadata("list")