# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'json'
require 'scrapers/cf'

BASE_URL = "http://www.egazette.com.sg"
  
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
    doc = Nokogiri::HTML(data).xpath(".//tr[contains(@id,'GridView1_')]")
    doc.each{|tr|
      td = tr.xpath("td")
      title = s_text(td[2].xpath("./a[@id]/text()"))
      if title =~ /Section 344/
        records << {
          "notification_no"=>s_text(td[0].xpath("./span[@id]/text()")),
          "section"=>"344",
          "tmp_link"=> append_base(BASE_URL,attributes(td[2].xpath("./a[@id]"),"href")),
          "title" => title,
          "published_dt" => Date.parse(s_text(td[3].xpath("./span[@id]/text()"))),
          "tmp_act" => "344"
        }.merge(rec)
      elsif title =~ /Submit Particulars of Debts or Claims/
        records << {
          "notification_no"=>s_text(td[0].xpath("./span[@id]/text()")),
          "tmp_link"=>append_base(BASE_URL,attributes(td[2].xpath("./a[@id]"),"href")),
          "title" => title,
          "published_dt" => Date.parse(s_text(td[3].xpath("./span[@id]/text()"))),
          "tmp_act" => "DebtsOrClaims"
        }.merge(rec)
      elsif title =~ /Notice of Intended Dividend/
        records << {
          "notification_no"=>s_text(td[0].xpath("./span[@id]/text()")),
          "tmp_link"=>append_base(BASE_URL,attributes(td[2].xpath("./a[@id]"),"href")),
          "title" => title,
          "published_dt" => Date.parse(s_text(td[3].xpath("./span[@id]/text()"))),
          "tmp_act" => "dividend"
        }.merge(rec)
      elsif title =~ /Business Registration Act - Registration cancelled/
        records << {
          "notification_no"=>s_text(td[0].xpath("./span[@id]/text()")),
          "tmp_link"=>append_base(BASE_URL,attributes(td[2].xpath("./a[@id]"),"href")),
          "title" => title,
          "published_dt" => Date.parse(s_text(td[3].xpath("./span[@id]/text()"))),
          "tmp_act" => "cancelled"
        }.merge(rec)
      elsif not title =~ /Immigration|Notice|Societies|Mental|Revenue|Housing|Winding|Maintenance|Choice/
        records << {
          "notification_no"=>s_text(td[0].xpath("./span[@id]/text()")),
          "tmp_link"=>append_base(BASE_URL,attributes(td[2].xpath("./a[@id]"),"href")),
          "title" => title,
          "published_dt" => Date.parse(s_text(td[3].xpath("./span[@id]/text()"))),
          "tmp_act" => "unknown"
        }.merge(rec)
      end
    }
    return records,doc.length
  elsif act == "344"
    records = []
    doc = Nokogiri::HTML(data).xpath(".")
    doc.xpath(".//p[contains(text(),'Registration')]/following-sibling::*[following-sibling::p[contains(text(),'Senior Assistant Registrar of Companies')]]").each{|ele|
      tmp = s_text(ele.xpath("./text()"))
      r = {}
      r["company_number"] = tmp.split(" ")[1]
      r["company_name"] = tmp.split("\u2014").last
      r["description"] = s_text(doc.xpath(".//p[contains(text(),'SECTION 344')]/following-sibling::*[1]"))
      records << r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}
    }
    return records
  elsif act == "DebtsOrClaims"
    records = []
    doc = Nokogiri::HTML(data).xpath(".")
    r = {}
    r["company_name"] = s_text(doc.xpath(".//p[contains(text(),'IN THE MATTER')][2]/following-sibling::*[1][self::p]"))
    tmp = s_text(doc.xpath(".//p[contains(text(),'Company Registration')]/text()"))
    r["company_number"] = tmp.scan(/Company Registration No. (.*)\)/).flatten.first
    r["description"] = a_text(doc.xpath(".//p[contains(text(),'NOTICE TO SUBMIT')]/following-sibling::*[self::p[following-sibling::p[contains(text(),'Dated this')]]]")).join(" ").pretty
    records << r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}
    return records
  elsif act == "dividend"
    records = []
    doc = Nokogiri::HTML(data).xpath(".")
    r = {}
    r["company_name"] = s_text(doc.xpath(".//p[contains(text(),'Name of Company :')]")).split(" : ").last.strip
    r["company_number"] = s_text(doc.xpath(".//p[contains(text(),'Reg. No.')]")).split(" : ").last.strip

    records << r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}
    return records
  elsif act == "cancelled"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//p[contains(normalize-space(text()),'Registration No.')]/following-sibling::p[following-sibling::p[contains(text(),'Senior Assistant')]]")
    doc.each_with_index{|ele,idx|
      tmp = s_text(ele.xpath("./text()"))
      next unless tmp =~ /^\d+\./
      puts tmp.inspect
      r = {}
      r["company_number"] = tmp.split(" ")[1]
      r["company_name"] = tmp.split(" ")[2..-2].join(" ").strip
      r["expiry_dt"] = Date.parse(tmp.split(" ").last) rescue nil
      r["expiry_dt"] = Date.parse(doc[idx+1]) rescue nil if r["expiry_dt"].nil? 

      records << r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}

    }
    return records
  elsif act == "unknown"
    records = []
    doc = Nokogiri::HTML(data).xpath(".")
    if data =~ /BALANCE SHEET AS/
      r = {}
      r["company_name"] = s_text(doc.xpath(".//p[contains(normalize-space(text()),'BALANCE SHEET AS')]/preceding-sibling::*[2]/text()")).gsub(/\((.*)\)/,"").strip
      r["company_number"] = s_text(doc.xpath(".//p[contains(normalize-space(text()),'BALANCE SHEET AS')]/preceding-sibling::*[1]/text()")).gsub(/\(|\)/,'').split(" ").last.strip
      r["published_dt"] = Date.parse(s_text(doc.xpath(".//p[contains(normalize-space(text()),'BALANCE SHEET AS')]/text()")).split("AT").last)
      records << r.merge(rec).delete_if{|k,v| k=~ /^tmp_/}
    else
      #raise "unknown #{rec}"
    end
    return records
  end
end

def action()
  pg = @br.get("http://www.egazette.com.sg/gazetteViewDetail.aspx?ct=gg&subscriber=0")
  pg_no = 1
  begin
    list,len = scrape(pg.body,"list",{})    
    puts ["list",len,list.length,list].inspect
    list.each{|rec|
      begin
        pg_tmp = @br.get(rec['tmp_link'])
        pg_tmp.save_as(pg_tmp.filename)
        tmp = %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar  ExtractText -html -console "#{pg_tmp.filename}"]
        ScraperWiki.save_sqlite(unique_keys=['company_number','link'],scrape(tmp,rec['tmp_act'],rec.merge({"link"=>pg_tmp.uri.to_s})))
      end if exists(rec['tmp_link'],'swdata','link') == 0
    }
    break if len < 20
    pg_no = pg_no + 1
    params = {"__EVENTTARGET"=>"GridView1","__EVENTARGUMENT"=>"Page$#{pg_no}"}
    pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
  end while(true)
end

action()

#pg_tmp = @br.get("http://www.egazette.com.sg/pdf.aspx?ct=gg&yr=2012&filename=12bal8194.pdf")
#pg_tmp.save_as(pg_tmp.filename)
#tmp = %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar  ExtractText -html -console "#{pg_tmp.filename}"]
#puts scrape(tmp,"unknown",{})
