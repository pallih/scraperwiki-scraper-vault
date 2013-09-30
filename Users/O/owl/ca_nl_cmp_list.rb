# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'scrapers/mcf'
require 'logger'
Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  #b.log = Logger.new(STDERR)
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
    doc.xpath(".//table[@width='100%' and @cellpadding='5']/tr[position()>1 and position()<last()]").each{|tr|
      r = {}
      r["company_name"] = s_text(tr.xpath("./td[1]/a/text()"))
      r["status"] = s_text(tr.xpath("./td[2]/span/text()"))
      r["company_number"] = s_text(tr.xpath("./td[3]/text()"))
      r["type"] = s_text(tr.xpath("./td[4]/text()"))
      r["inc_dt"] = s_text(tr.xpath("./td[5]/span/text()"))
      records << r.merge(rec)
    }
    return records,attributes(doc.xpath(".//a[@id='lbtNext']"),"href").split("'")[1],[s_text(doc.xpath(".//span[@id='lblRecordsFound']/text()")),s_text(doc.xpath(".//span[@id='lblViewingRecords']/text()"))]
  end
end

def action(srch)
  return srch,300 if srch.length == 1
  pg = @br.get("https://cado.eservices.gov.nl.ca/Company/CompanyNameNumberSearch.aspx")
  params = {"txtNameKeywords1"=>srch,"btnSearch.x"=>"21","btnSearch.y"=>"11"}
  ttl = 0
  begin
    pg.form_with(:id=>"form") do |f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
    return srch,300 if pg.body =~ /Search returned more than 300 matching results/
    list,nex,hdr = scrape(pg,"list",{"doc"=>Time.now})
    ttl = ttl + list.length
    ScraperWiki.save_sqlite(['company_number'],list)
    puts [srch,nex,list.length,hdr].inspect
    break if list.nil? or list.empty? or list.length < 10 or nex.nil? or nex.empty? 
    params = {"__EVENTTARGET"=>nex,"__EVENTARGUMENT"=>""}
  end while(true)
  return srch,ttl
end

begin
  trail = get_metadata("trail","A").split(">>")
  srch = trail.last
  MAX_T = 300
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