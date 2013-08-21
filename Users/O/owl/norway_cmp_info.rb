# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://w2.brreg.no/"

def get_metadata(key, default)
    begin
      ScraperWiki.get_var(key, default)
    rescue Exception => e
      puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
      retry
    end
end

def save_metadata(key, value)
    begin
      ScraperWiki.save_var(key, value)
    rescue Exception => e
      puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
      retry
    end
end

def delete_metadata(key)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where key=?",[key])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
    retry
  end
end


def text(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@style='border-color: #999999;']//td/table/tr[not(@bgcolor='#cccccc') and count(td)>1]").each{|tr|
      td = tr.xpath("td[not(normalize-space(.|p)='')]")
      #puts td.inner_html
      r = {
        "COMPANY_NAME" => text(td[1].xpath("p/text()")),
        "COMPANY_NUMBER" => text(td[3].xpath("p/text()")),
        "DOC" => Time.now.to_s
      }
      r['URL']=BASE_URL+"enhet/sok/detalj.jsp?orgnr=#{r['COMPANY_NUMBER'].gsub(/ /,'')}" 
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    }
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records.length <=0
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "kunngjoring/kombisok.jsp?datoFra=#{srch}"
    pg = br.get(s_url)
    scrape(pg.body,"list")
    return true
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    if e.inspect=~ /time/i
      sleep(30)
      retry
    end
    return false
  end
end

save_metadata("DATE","01.01.2000")
strt = Date.parse(get_metadata("DATE","01.01.2000"))
range = (strt..Date.today)

range.each{|dt|
  ret = action(("%02d" % dt.day.to_s)+"."+("%02d" % dt.month.to_s)+"."+dt.year.to_s)
  save_metadata("DATE",dt.next.to_s) unless dt.next>Date.today and ret==false
}

