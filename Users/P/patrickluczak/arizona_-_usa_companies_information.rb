# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.azsos.gov"

def get_metadata(key, default)
    begin
      ret = ScraperWiki.get_var(key, default)
      if ret.nil? or ret.empty? 
        return default
      else
        return ret
      end
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

def text(str)
  begin
    return nil if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip }
      return tmp.uniq.first
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@align='center']/tr[position()>1]")
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
         "COMPANY_NUMBER" => text(td[0].xpath("a/font")),
         "COMPANY_NAME" => text(td[2].xpath("font|.|font/font/font|font/font")),
         "URL" => attributes(td[0].xpath("a"),"href"),
         "TYPE" => text(td[1].xpath(".")),
         "DOC" => Time.now
      }
      r['URL']=BASE_URL+r['URL'] unless r['URL'] =~ /azcc/i 
      records << r unless r['TYPE'].match(/TRADEMARK|TRADENAME|PENDING CORP./i)
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records.length<=0
    return doc.length
  end
end

def scraped(params)
  return get_metadata(params,nil)
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "/scripts/TnT_Search_Engine.dll/ListNames"
    params={'NIR_ID'=>'','AGENT'=>'','WORDS'=>srch,'SEARCH_TYPE'=>'PW'}
    pg = br.post(s_url,params)
    ret = scrape(pg.body,"list")
    return ret
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/i
  end
end

#save_metadata("TRIAL","A")
trial = get_metadata("TRIAL","<non-alpha>")
srch = trial.nil? ? get_metadata("TRIAL","<non-alpha>") : trial.split(">>").last
if srch == "<non-alpha>"
  range = ['\!','@','#','$','%','^','&','*','(',')'].to_a + (0..100).to_a
  offset = get_metadata("OFFSET",0)
  range.each_with_index{|srch,idx|
    next if idx < offset
    action(srch)
    save_metadata("OFFSET",idx.next)
  }
  save_metadata("TRIAL","A")
  delete_metadata("OFFSET")
  trial = "A"
  srch = "A"
end
begin
  ret = action(srch)
  if ret.nil? or ret == 0
    if trial.nil? or trial.empty? 
      trial = srch.next
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? 'A' : t_s.next
      trial = (t_a << srch).join(">>")
    end
  elsif ret == 500
    srch = srch+'A'
    trial = (trial.nil? or trial.empty?)? srch : (trial + ">>" + srch)  
  else
    t_a = trial.split(">>")
    t_s = t_a.pop
    t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
    srch = (t_s == 'Z')? 'A' : t_s.next
    trial = (t_a << srch).join(">>")
  end
  if srch.nil? 
    delete_metadata("TRIAL")
    break
  end
  save_metadata("TRIAL",trial)
end while(true)# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.azsos.gov"

def get_metadata(key, default)
    begin
      ret = ScraperWiki.get_var(key, default)
      if ret.nil? or ret.empty? 
        return default
      else
        return ret
      end
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

def text(str)
  begin
    return nil if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.collect{|st| tmp << st.text.strip }
      return tmp.uniq.first
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end


def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//table[@align='center']/tr[position()>1]")
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
         "COMPANY_NUMBER" => text(td[0].xpath("a/font")),
         "COMPANY_NAME" => text(td[2].xpath("font|.|font/font/font|font/font")),
         "URL" => attributes(td[0].xpath("a"),"href"),
         "TYPE" => text(td[1].xpath(".")),
         "DOC" => Time.now
      }
      r['URL']=BASE_URL+r['URL'] unless r['URL'] =~ /azcc/i 
      records << r unless r['TYPE'].match(/TRADEMARK|TRADENAME|PENDING CORP./i)
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="SWDATA",verbose=2) unless records.length<=0
    return doc.length
  end
end

def scraped(params)
  return get_metadata(params,nil)
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "/scripts/TnT_Search_Engine.dll/ListNames"
    params={'NIR_ID'=>'','AGENT'=>'','WORDS'=>srch,'SEARCH_TYPE'=>'PW'}
    pg = br.post(s_url,params)
    ret = scrape(pg.body,"list")
    return ret
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/i
  end
end

#save_metadata("TRIAL","A")
trial = get_metadata("TRIAL","<non-alpha>")
srch = trial.nil? ? get_metadata("TRIAL","<non-alpha>") : trial.split(">>").last
if srch == "<non-alpha>"
  range = ['\!','@','#','$','%','^','&','*','(',')'].to_a + (0..100).to_a
  offset = get_metadata("OFFSET",0)
  range.each_with_index{|srch,idx|
    next if idx < offset
    action(srch)
    save_metadata("OFFSET",idx.next)
  }
  save_metadata("TRIAL","A")
  delete_metadata("OFFSET")
  trial = "A"
  srch = "A"
end
begin
  ret = action(srch)
  if ret.nil? or ret == 0
    if trial.nil? or trial.empty? 
      trial = srch.next
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? 'A' : t_s.next
      trial = (t_a << srch).join(">>")
    end
  elsif ret == 500
    srch = srch+'A'
    trial = (trial.nil? or trial.empty?)? srch : (trial + ">>" + srch)  
  else
    t_a = trial.split(">>")
    t_s = t_a.pop
    t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
    srch = (t_s == 'Z')? 'A' : t_s.next
    trial = (t_a << srch).join(">>")
  end
  if srch.nil? 
    delete_metadata("TRIAL")
    break
  end
  save_metadata("TRIAL",trial)
end while(true)