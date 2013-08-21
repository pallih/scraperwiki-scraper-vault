require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'
# encoding: UTF-8

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.bseindia.com"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
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
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? nil : t.first.attributes[attr].value
end


def scrape(data,act,grp)
  if act=="list"
    codes = []
    Nokogiri::HTML(data).xpath(".//a[@class='class1']").each{|anchor|
      records = {
        "DOC"=>Time.now.to_s,
        "NAME" => text(anchor.xpath("text()")),
        "GROUP" => grp,
        "URL" => BASE_URL+attributes(anchor.xpath("."),"href")
      }
      records["CODE"] = records["URL"].split("=")[1] unless records["URL"].nil? or records==BASE_URL
      #puts records.inspect
     ScraperWiki.save_sqlite(unique_keys=['CODE'],records,table_name='SWDATA',verbose=0)
     codes << records['CODE']
    }
    return codes
  elsif act=="check"
    return attributes(Nokogiri::HTML(data).xpath(".//a[text()='Next']"),"href")
  elsif act == "details"
    dump = data.split("\#@\#")
    #puts [dump[1],dump[3],grp].inspect
    ScraperWiki.sqliteexecute("update swdata set ISIN=?,INDUSTRY=? where CODE=?",[dump[1],dump[3],grp])
    ScraperWiki.commit()
  end
end


def action(grp)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    ["[A-Z]","[0-9]"].each{|alphabet|
      nex = "disp.asp?flag=#{grp}&curpage=1&select_alp=#{alphabet}"
      begin
        s_url = BASE_URL + "/datalibrary/"+nex
        pg = br.get(s_url)
        codes = scrape(pg.body,"list",grp)
        nex = scrape(pg.body,"check",nil)
        codes.each{|code|
          pg_dump = br.get(BASE_URL+"/bseplus/StockReach/AdvStockReach.aspx?scripcode=#{code}&section=tab2&IsPF=undefined&random=0.2467107730167909",[],BASE_URL+"/bseplus/StockReach/AdvanceStockReach.aspx?scripcd=#{code}")
          scrape(pg_dump.body,"details",code)
        }
      rescue Exception => e
        puts "ERROR: While processing #{s_url}:: #{e.inspect} :: #{e.backtrace}"
        sleep(30)
        retry if e.inspect =~ /Timeout|TIME|HTTP/
      end while not nex.nil? 
    }
  end
end

#puts ScraperWiki.sqliteexecute('select * from swdata where code=?',["532149"])
#puts ScraperWiki.sqliteexecute("update swdata set ISIN=?,INDUSTRY=? where CODE=?",['-','-',"532149"])
#puts ScraperWiki.commit()
#exit
range = ["A","B","S","T","TS","Z"]
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  begin
    action(srch)
    save_metadata("OFFSET",index.next)
  end unless index < offset
end
