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
    Nokogiri::HTML(data).xpath(".//table[@id='searchActionForm:searchAction']/tbody/tr").each{|tr|
      r = {}
      r['company_name'] = s_text(tr.xpath("./td[2]/text()"))
      r['reg_no'] = s_text(tr.xpath("./td[3]/text()"))
      r['status'] = s_text(tr.xpath("./td[4]/text()"))
      r['inn'] = s_text(tr.xpath("./td[5]/text()"))
      r['enterprise_code'] = s_text(tr.xpath("./td[6]/text()"))
      r['date'] = s_text(tr.xpath("./td[7]/text()"))
      r['link'] = append_base("https://register.minjust.gov.kg/",attributes(tr.xpath("./td[8]/a"),"href"))
      records << r.merge(rec)
    }
    return records
  end
end

def action(srch)
  pg_no = get_metadata("page_no",0)
  begin
    pg = @br.get("https://register.minjust.gov.kg/register/SearchAction.seam?firstResult=#{pg_no}&number=&tin=&fullnameRu=#{srch}&logic=and&okpo=&cid=48404")
    records = scrape(pg,"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(['company_number'],records,'ocdata')
    break if records.length < 25
    pg_no = pg_no + 25
    save_metadata("page_no",pg_no)
  end while(true)
  puts ["<<||>>",srch,"complete"].inspect
  delete_metadata("page_no")
end


list = ('A'..'Z').to_a + (0..9).to_a
lstart = get_metadata("list",0)
list[lstart..-1].each{|srch|
  saves_metadata("search",srch)
  action(srch)
  lstart = lstart + 1
  saves_metadata("list",lstart)
}
delete_metadata("list")