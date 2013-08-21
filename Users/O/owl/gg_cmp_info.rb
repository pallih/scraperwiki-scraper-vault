# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.greg.gg/"

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
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip }
      return tmp.join("\n")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,url)
  doc = Nokogiri::HTML(data)
  r = {
    "COMPANY_NUMBER"=>text(doc.xpath(".//span[@id='ctl00_cntPortal_tbCompSearchDetails_TabPanel1_lblCompRegNum']")),
    "COMPANY_NAME"=>text(doc.xpath(".//span[@id='ctl00_cntPortal_tbCompSearchDetails_TabPanel1_lblCompName']")),
    "TYPE"=>text(doc.xpath(".//span[@id='ctl00_cntPortal_tbCompSearchDetails_TabPanel1_lblCompType']")),
    "STATUS"=>text(doc.xpath(".//span[@id='ctl00_cntPortal_tbCompSearchDetails_TabPanel1_lblCompStatus']")).split(" ")[0],
    "ADDR"=>text(doc.xpath(".//span[@id='ctl00_cntPortal_tbCompSearchDetails_TabPanel1_lblROAddr']")),
    "INC_DT"=>text(doc.xpath(".//span[@id='ctl00_cntPortal_tbCompSearchDetails_TabPanel1_lblRegDate']")),
    "URL"=>url
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER','COMPANY_NAME'],r,table_name='SWDATA',verbose=2) unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
  return r['COMPANY_NUMBER']
end

def action(srch,force)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
   }
  begin
    pg = br.get(BASE_URL+"webCompSearch.aspx?r=0&crn=#{srch}&cn=&rad=StartsWith&ck=False")
    len = Nokogiri::HTML(pg.body).xpath(".//table[@id='ctl00_cntPortal_grdSearchResults']/tr[position()>1]").length 
    idx = 2
    pg_tmp = nil
    pages = []
    len.times{
      pg.form_with(:name=>'aspnetForm') do|f|
        f["ctl00$ScriptManager2"]="ctl00$cntPortal$updPanel|ctl00$cntPortal$grdSearchResults$ctl0#{idx}$ibSelect"
        f["ctl00$cntPortal$grdSearchResults$ctl0#{idx}$ibSelect.x"]=7
        f["ctl00$cntPortal$grdSearchResults$ctl0#{idx}$ibSelect.y"]=4
        pg_tmp = f.submit
      end
      scrape(pg_tmp.body,pg_tmp.uri.to_s)
      idx = idx+1
    }
  rescue Exception => e
   puts "Failing to fetch #{srch}::#{force}::#{e.inspect}"
   retry if e.inspect =~ /http|Connection/i
   raise e unless e.inspect =~ /ssl|time/i
  end
end

save_metadata("STRT",55000)
strt = get_metadata("STRT",55000)
endd = strt + 50
(strt..endd).each{|srch|
  resp = action(srch,1)
  save_metadata("OFFSET",srch.next) unless resp.nil? or resp == 0
}
