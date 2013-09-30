# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://ariregister.rik.ee"
WAIT_INTERVAL=3600

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
    Nokogiri::HTML(data).xpath(".//table[@class='tbl_listing']/tr[position()>1]").each{|tr|
      r = {}
      r["company_name"] = s_text(tr.xpath("./td[2]/a/text()"))
      r["invalid_names"] = a_text(tr.xpath("./td[3]")).delete_if{|a| a.nil? or a.empty?}.join("")
      r["company_number"] = s_text(tr.xpath("./td[4]/text()"))
      r["inc_dt"] = s_text(tr.xpath("./td[5]/text()"))
      tmp = a_text(tr.xpath("./td[6]")).delete_if{|a| a.nil? or a.empty?}
      r["status"] = JSON.generate tmp unless tmp.nil? or tmp.empty? 
      r["area"] = s_text(tr.xpath("./td[7]/text()"))
      r["address"] = s_text(tr.xpath("./td[8]/text()"))
      r["share_capital"] = s_text(tr.xpath("./td[9]/text()"))
      r["webpage"] = attributes(tr.xpath("./td[10]/a"),"href")
      r["registration_no"] = attributes(tr.xpath("./td[11]/a"),"href").split("'")[3]

      records << r.merge(rec)
    }
    return records
  elsif act == "length"
    return Nokogiri::HTML(data).xpath(".//table[@class='tbl_listing']/tr[position()>1]").length
  elsif act == "det"
    #return s_text(Nokogiri::HTML(data).xpath(".//td[text()='Commercial registry code:']/following-sibling::*[1][self::td]/text()"))
    return s_text(Nokogiri::HTML(data).xpath(".//td[text()='Commercial registry code:']/following-sibling::*[1][self::td]/text()"))
  elsif act == "batch_count"
    return s_text(Nokogiri::HTML(data).xpath(".//span[@class='batch_count']/text()")).split(/\s/)[1].to_i
  end
end

def ginc()
  if @gidx == 15
    sleep(WAIT_INTERVAL) 
    @gidx = 1
  end
  @gidx = @gidx + 1
end


def action(srch)
  pg_no = get_metadata("#{srch}_page_no",0).to_i
  bc = nil
  begin
    pg = @br.get(BASE_URL + "/lihtparing.py",{"id"=>"","source"=>"lihtparing","sess"=>"","lang"=>"eng","search"=>"1","nimi"=>srch,"sub"=>"Search from the Commercial Register","qs"=>pg_no})
    raise "death by captcha" if pg.body =~ /captcha\.py/

    records = scrape(pg,"list",{"doc"=>Time.now})
    ScraperWiki.save_sqlite(['company_number'],records,'ocdata')
    break if records.length < 10
    pg_no = pg_no + 10
    save_metadata("#{srch}_page_no",pg_no)

    ## Global Increment
    ginc()
  end while(true)
  puts ["<<||>>",srch,"complete"].inspect
  delete_metadata("#{srch}_page_no")
end

@gidx = 1
list = ('A'..'Z').to_a + (0..9).to_a
lstart = get_metadata("list",0)
list[lstart..-1].each{|srch|
  begin
    action(srch)
  end
}
delete_metadata("list")