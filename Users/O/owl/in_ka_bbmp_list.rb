require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML
BASE_URL = "http://www.bbmp.gov.in/"

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
        puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{default})"
    end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|:|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action,url)
  if action == "details"
      records = {"URL"=>url,"DOC"=>Time.now.to_s}
      Nokogiri::HTML(data).xpath("//table[@style='width: 60%; border-collapse: collapse;']/tbody/tr").each{|tr|
        td = tr.xpath("td")
        case text(td[0])
          when /Ward No/
            key = "WARD_NO"
          when /Ward Name/
            key = "WARD_NAME"
          when /Ward Area(in Sq Km)/
            key = "WARD_AREA"
          when /Assembly Constituency/
            key = "CONSTITUENCY"
          else
            key = nil
        end
        records[key] = text(td[1]) unless key.nil? 
      }
      Nokogiri::HTML(data).xpath("//table[@style='width: 80%; border-collapse: collapse;']/tbody/tr").each{|tr|
        td = tr.xpath("td")
        case text(td[0])
          when /Councillor Name/
            key = "NAME"
          when /Address/
            key = "ADDRESS"
          when /Phone Number/
            key = "PHONE"
          else
            key = nil
        end
        records[key] = text(td[1]) unless key.nil? 
      }
      #puts records.inspect
      ScraperWiki.save_sqlite(unique_keys=["WARD_NO"],records)
  elsif action=="list"
    records = []
    Nokogiri::HTML(data).xpath("//table[@bordercolor='#0000ff']/tbody/tr[position()>1]/td[2]/div").each{|div|
      records << attributes(div.xpath("a"),"href")
    }
    #puts records.inspect
    return records
  else
    raise "Unknown action type"
  end 
end

def ne(data)
  return attributes(Nokogiri::HTML(data).xpath("//a[text()='>']"),"href")
end

def action
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL+"index.php?option=com_content&view=article&id=401&Itemid=205"
    pg = br.get(s_url)
    links = scrape(pg.body,"list","")
    links.each{|lnk|
      begin
        l_pg = br.get(BASE_URL+lnk)
        re = scrape(l_pg.body,"details",BASE_URL+lnk) 
      rescue Exception => e
        puts "ERROR: While processing sub links :: #{e.inspect} :: #{e.backtrace}"
        #sleep(2)
        #retry unless e.inspect =~ /Timeout/ or e.inspect =~ /Service/
      end unless lnk.empty? 
    }
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
    sleep(10)
    retry unless e.inspect =~ /Timeout/ or e.inspect =~ /Service/
  end
    
end
action