# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.cipro.gov.za/"

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
    doc = Nokogiri::HTML(data).xpath(".//table[@class='tableselect']/tr[position()>1]")
    doc.each{|tr|
      key = s_text(tr.xpath("./td[3]/font/a/text()"))
      next if key.nil? or key.empty? 
      records << {
        "company_number"=>key,
        "company_name" => s_text(tr.xpath("./td[2]/font/a/text()")),
        "url" => attributes(tr.xpath("./td[2]/font/a"),"href"),
        "doc" => Time.now
      }
    }
    return doc.length,records
  end
end


def action(srch)
  pg = @br.get(BASE_URL + "namesearch/cdirect.aspx?QueryText=#{srch}*&VerSearchSubmit=Search&Action=Filtersearch&collection=Reserved%2CRegister&collection=Reserved&Filter=UUNETout_regf.hts&ResultCount=20000&ResultTemplate=UUNETnormalnamesearchdev.asp&verityRegion=&veritySIC=")
  len,list = scrape(pg.body,"list",{})
  #puts ["list",list.length].inspect
  ScraperWiki.save_sqlite(unique_keys=['company_number'],list)
  return srch,len
end


begin
  trail = get_metadata("trail","A").split(">>")
  srch = trail.last
  MAX_T = 200
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
    sleep(2)
  end while(true)
end
delete_metadata("trail")


