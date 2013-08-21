# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/mcf'

BASE_URL = "http://www.online.gov.sz"
  
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
    doc = Nokogiri::HTML(data).xpath(".")
    doc.xpath(".//table[@id='GridView1']/tr[position()>1 and position()<last()]").each{|tr|
      records << {
        "company_name" => s_text(tr.xpath("./td[1]/text()")),
        "status" => s_text(tr.xpath("./td[2]/text()")),
        "reg_dt" => s_text(tr.xpath("./td[3]/text()")),
        "doc" => Time.now
      }.merge(rec)
    }
    tmp = attributes(doc.xpath(".//table[@border='0']/tr/td[span]/following-sibling::*[1]/a"),"href").split("'")
    return tmp[3],records
  end
end

def action()
  pg = @br.get(BASE_URL+"/company.aspx")
  
  alphas = ('a'..'z').to_a + (0..9).to_a
  astart = get_metadata("alpha",0)
  alphas[astart..-1].each{|alp|
    params = eval(get_metadata("form",'{"TextBox2"=>alp,"Button3"=>"Search+Company"}'))
    pg.form_with(:id=>"form1") do |f|
      params.each{|k,v| f[k] = v}
      pg = f.submit
    end
    begin
      nex,list = scrape(pg.body,"list",{})
      ScraperWiki.save_sqlite(unique_keys=['company_name'],list)
      break if list.nil? or list.length < 10 or nex.nil? or nex.empty? 
  
      params = {"__EVENTTARGET"=>"GridView1","__EVENTARGUMENT"=>nex}
  
      pg.form_with(:id=>"form1") do |f|
        params.each{|k,v| f[k] = v}
        pg = f.submit
      end
      tmp = {}
      pg.form_with(:id=>"form1").fields.each{|f|
        tmp[f.name] = f.value
      }
      save_metadata("form",tmp.to_s)
      sleep(2)
    end while(true)
    delete_metadata("form")

    astart = astart + 1
    save_metadata("alpha",astart)
  }
  delete_metadata("alpha")
end

action()
