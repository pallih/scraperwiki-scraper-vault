# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'open-uri'
require 'scrapers/mcf'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://rjsc.gov.ns.ca/"

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history = 0
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


def scrape(data,act)
  if act == "details"
    records = []
    Nokogiri::HTML(data).xpath(".//form//table[@border='1']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NAME"=>s_text(td[0].xpath("a/text()")),
        "COMPANY_NUMBER"=>attributes(td[0].xpath("a"),"href").split("'")[1],
        "TYPE"=>s_text(td[1].xpath("./text()")),
        "STATUS"=>s_text(td[2].xpath("./text()")),
        "DOC"=>Time.now
      }
      records << r unless r['COMPANY_NUMBER'].nil? 
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER','TYPE'],records,table_name='SWDATA',verbose=2) unless records.length==0
  end
end

def action(srch)
  begin
    params = {
      "fullName" => srch
    }
    pg = @pg.form_with(:name=>'NameSearchActionForm').submit
    
    pgno = 1
    begin
      pg.form_with(:action=>(pgno==1)? "/rjsc/search/doSearch.do" : "/rjsc/search/paging.do") do|f| 
        params.each{|k,v| f[k] = v } 
        pg = f.submit 
      end
      scrape(pg.body,"details")
      break if pg.at("a[@name='NSFrom']").nil? 
      pgno = pgno +1
      params = {'jump'=>pgno}
    end while(true)
    return srch,pgno
  rescue Exception => e
    puts ["Exception",e,srch].inspect
    sleep(10)
    retry
  end
end

s_url = BASE_URL + "rjsc/"
@pg = @br.get(s_url)



trail = get_metadata("trail",'A').split(">>")
srch = trail.last
MAX_T = 19
begin
  prev,ret = action({"name"=>srch})
  if ret >= MAX_T
    srch = srch + "A"
    trail << srch
  else
    tmp = ''
    begin tmp = trail.pop end while tmp =='Z' or tmp.split(//).last == 'Z' rescue nil
    if tmp.nil? or tmp.empty? 
      trail = ["A"]
    else
      srch = (tmp == 'Z')? "A" : tmp.next
      trail << srch
    end
  end
  puts [ret,prev,srch,trail].inspect
  save_metadata("trail",trail.join(">>"))
  sleep(5)
end while(true)
