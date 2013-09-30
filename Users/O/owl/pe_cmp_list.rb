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
    Nokogiri::HTML(data).xpath(".//table[@width='99%']/tr[position()>1]").each{|tr|
      r = {}
      r['company_number'] = s_text(tr.xpath("./td[2]/text()"))
      r['company_name'] = s_text(tr.xpath("./td[3]/text()"))
      r['siglas'] = s_text(tr.xpath("./td[4]/text()"))
      r['oficina'] = s_text(tr.xpath("./td[5]/text()"))
      records << r.merge(rec)
    }
    return records
  elsif act == "length"
    return Nokogiri::HTML(data).xpath(".//table[@width='99%']/tr[position()>1]").length
  end
end

def action(srch)
  pg_no = get_metadata("page_no",1)
  pg = @br.post("http://www.sunarp.gob.pe/RelacionS_01r.asp",{"tRazon"=>srch,"tSiglas"=>""})
  begin
    pg = @br.post("http://www.sunarp.gob.pe/RelacionS_01r.asp",{"pagina"=>pg_no,"tRazon"=>srch})
    records = scrape(pg,"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(['company_number'],records,'ocdata')
    break if records.length < 20
    pg_no = pg_no + 1
    save_metadata("page_no",pg_no)
  end while(true)
  puts ["<<||>>",srch,"complete"].inspect
  delete_metadata("page_no")
end


list = ('A'..'Z').to_a + (0..9).to_a
lstart = get_metadata("list",0)
list[lstart..-1].each{|srch|
  begin
    action(srch)
  end
}
delete_metadata("list")