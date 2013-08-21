require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://secure.in.gov"

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
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip}
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
    Nokogiri::HTML(data).xpath(".//*[@id='grdViewResults']/tr[position()>2 and position()<last()]").each do|tr|
      td = tr.xpath("td")
      r = {
         "COMPANY_NAME" => text(td[0]),
         "URL" => "https://secure.in.gov/sos/online_corps/"+attributes(td[0].xpath("a"),"href"),
         "TYPE" => text(td[1]),
         "STATUS" => text(td[2]),
         "PLACE" => text(td[3]),
         "DOC" => Time.now
      }
      r["GUID"]=r["URL"].split("=")[1]
      records << r
    end
    ScraperWiki.save_sqlite(unique_keys=["GUID"],records,table_name="swdata",verbose=2) unless records.length == 0
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
    }
    s_url = BASE_URL + "/sos/online_corps/name_search_results.aspx?search_name=#{srch}&search_type=partial&client_id=&submit.x=2&submit.y=3&search_mode=search"
    pg = br.get(s_url)
    total_cnt = text(pg.at("span[@id='lblSearchCount']"))[/There were (.*) /,1].to_f
    scrape(pg.body.gsub(/id="__VIEWSTATE" value=(.*)>/,">"),"list")
    iter = (total_cnt/30).ceil
    iter.times{
      begin
      params = { "__EVENTTARGET" => "grdViewResults$_ctl1$lnkNextPage"} 
      pg.form_with(:name=>"Form1") do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      scrape(pg.body.gsub(/id="__VIEWSTATE" value=(.*)>/,">"),"list")
      rescue Exception=>e
        puts [srch,"Error while paginating",e].inspect        
      end
    } unless iter == 1
    return srch,total_cnt
  end
end

#save_metadata("TRIAL","A")
trial = get_metadata("TRIAL","<num>")
srch = (trial.nil? or trial.empty? or trial=="<num>") ? "A" : trial.split(">>").last
if trial == "<num>"
  (0..99).to_a.each{|num|
    action(num)
  }
  save_metadata("TRIAL","A")
end
begin
  prev,ret = action(srch)
  if ret.nil? or ret == 0
    if trial.nil? or trial.empty? 
      srch = srch.next
      trial = srch
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? nil : t_s.next
      trial = (t_a << srch).join(">>")
    end
  elsif ret == 5000.0
    srch = srch+'A'
    trial = (trial.nil? or trial.empty?)? srch : (trial + ">>" + srch)
  else
    t_a = trial.split(">>")
    t_s = t_a.pop
    t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
    srch = (t_s == 'Z')? nil : t_s.next
    trial = (t_a << srch).join(">>")
  end
  save_metadata("TRIAL",(trail.nil? or trial.empty?)? "<num>":trial)
end while(true)

