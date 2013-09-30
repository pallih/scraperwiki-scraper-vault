# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.secretary.state.nc.us/corporations/"

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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip}
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


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@id='SosContent_SosContent_dgCorps']/tr[position()>1 and td/img[@alt='Legal NC Corporate Name']]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME" => text(td[1].xpath("a")),
      "TYPE" => text(td[2].xpath(".")),
      "STATUS" => text(td[3].xpath("a")),
      "CREATION_DT" => text(td[4].xpath(".")),
      "URL" => BASE_URL+attributes(td[1].xpath("a"),"href"),
    }
    r["COMPANY_NUMBER"]=r['URL'].split("=")[1]
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"searchresults.aspx?onlyactive=OFF&Words=STARTING&searchstr=#{srch}"
    pg = br.get(s_url)
    resp =  scrape(pg.body)
    len = Nokogiri::HTML(pg.body).xpath(".//table[@id='SosContent_SosContent_dgCorps']/tr[position()>1]").length
    return srch,len
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end

begin
  trial = get_metadata("TRIAL","A")
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
    elsif ret == 500
      srch = srch+'A'
      trial = (trial.nil? or trial.empty?)? srch : (trial + ">>" + srch)
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? nil : t_s.next
      trial = (t_a << srch).join(">>")
    end
    save_metadata("TRIAL",trial)
    if t_s.nil? or t_s.empty? or srch.nil? or s.empty? 
      delete_metadata("TRIAL") 
      break
    end
  end while(true)
end

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'pp'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.secretary.state.nc.us/corporations/"

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

def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length==0
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip}
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


def scrape(data)
  records = []
  Nokogiri::HTML(data).xpath(".//table[@id='SosContent_SosContent_dgCorps']/tr[position()>1 and td/img[@alt='Legal NC Corporate Name']]").each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME" => text(td[1].xpath("a")),
      "TYPE" => text(td[2].xpath(".")),
      "STATUS" => text(td[3].xpath("a")),
      "CREATION_DT" => text(td[4].xpath(".")),
      "URL" => BASE_URL+attributes(td[1].xpath("a"),"href"),
    }
    r["COMPANY_NUMBER"]=r['URL'].split("=")[1]
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    s_url = BASE_URL+"searchresults.aspx?onlyactive=OFF&Words=STARTING&searchstr=#{srch}"
    pg = br.get(s_url)
    resp =  scrape(pg.body)
    len = Nokogiri::HTML(pg.body).xpath(".//table[@id='SosContent_SosContent_dgCorps']/tr[position()>1]").length
    return srch,len
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
  end
end

begin
  trial = get_metadata("TRIAL","A")
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
    elsif ret == 500
      srch = srch+'A'
      trial = (trial.nil? or trial.empty?)? srch : (trial + ">>" + srch)
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? nil : t_s.next
      trial = (t_a << srch).join(">>")
    end
    save_metadata("TRIAL",trial)
    if t_s.nil? or t_s.empty? or srch.nil? or s.empty? 
      delete_metadata("TRIAL") 
      break
    end
  end while(true)
end

