require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://app.sos.ky.gov"

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
    end
end

def delete_metadata(name)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{name}"
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
      return tmp
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    Nokogiri::HTML(data,nil,'UTF-8').xpath(".//table[@border='0' and not(@cellspacing)]/tr[position()>1]").each do|tr|
      td = tr.xpath("td")
      r = {
         "COMPANY_NAME" => text(td[0].xpath("a")),
         "URL" => attributes(td[0].xpath("a"),"href"),
         "COMPANY_NUMBER" => text(td[1]),
         #"STATUS" => text(td[2]),
         "TYPE" => text(td[3]), 
         "DOC" => Time.now
      }
      records << r unless r['TYPE'] =~ /name/i
    end
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length == 0
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    pg = br.get(BASE_URL+"/ftsearch/default.aspx",[],BASE_URL+"/ftsearch/default.aspx")
    params = {"ctl00$ContentPlaceHolder1$FTUC$TextBox1"=>"#{srch}___","__EVENTTARGET"=>"ctl00$ContentPlaceHolder1$FTUC$TextBox1"}
    pg.form_with(:name => "aspnetForm") do |f|
      params.each{|k,v|
        f[k] = v
      }
      pg =  f.submit
    end unless pg.nil? or pg.form_with(:name=>"aspnetForm").nil? 
    scrape(pg.body,"list")
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /Timeout|HTTP|TIMED|/
  end
end
#action("ABCD")
#exit

range = ('AA'..'ZZ').to_a + (0..9).to_a + ['@','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next if index < offset
  action(srch)
  save_metadata("OFFSET",offset.next)
end

