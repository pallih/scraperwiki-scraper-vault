#-*- encoding: utf-8 -*-
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://federalreserve.gov"

class String
  def join(arg)
    return self
  end
end

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

def p0(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//div[@id='releaseIndex']//dt")
    records = []
    doc.each{|dt|
      r = {}
      tmp = text(dt.xpath("."))
      if tmp.is_a?(Array)
        r["release_date"] = tmp[0..1].join("")
      else
        r["release_date"] = tmp.strip
      end
      r["url"] = attributes(dt.xpath("a"),"href")
      if r["url"].nil? or r["url"].empty? 
        dt.xpath("following-sibling::dd[1]//a").each{|a|
          title = text(a.xpath(".|following-sibling::text()[1]")).join("")
          records << {
            "release_date" => r["release_date"],
            "url" => BASE_URL + attributes(a.xpath("."),"href"),
            "title" => title
          } unless title.nil? or title.empty? 
        }
      else
        r["url"] = BASE_URL + r["url"]
        r["title"] = text(dt.xpath("following-sibling::dd[1]")).join(" ")
        records << r
      end

    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='press_release',verbose=2) unless records.length == 0
  end
end

def p1(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//ul[@id='releaseIndex']/li")
    records = []
    doc.each{|li|
      r = {
        "release_date"=>li.xpath("./text()").to_s,
        "title" => text(li.xpath("div[@class='indent']/a")),
        "url" => BASE_URL + attributes(li.xpath("div[@class='indent']/a"),"href"),
      }
      if r['release_date'].nil? or r['release_date'].empty? 
        puts "p0:Invalid data: #{r}"
      else
        records << r
      end
    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='press_release',verbose=2) unless records.length == 0
  end
end


def p2(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//div[@id='speechIndex']/dl/dt[normalize-space()]")
    records = []
    doc.each{|dt|
     #puts dt.xpath("following-sibling::dd[1]").inner_html.inspect
      r = {
        "release_date"=> text(dt.xpath("a|dt/a")),
        "url"=> BASE_URL + attributes(dt.xpath("a|dt/a"),"href"),
        "title" => text(dt.xpath("following-sibling::dd[1]/i|following-sibling::dd[1]/em")).join(""),
        "location" => dt.xpath("following-sibling::dd[1]/text()").text.strip,
      }
      r["speaker"] = text(dt.xpath("following-sibling::dd[1]/b[1]|following-sibling::dd[1]/strong[1]"))
      r["notes"] = text(dt.xpath("following-sibling::dd[1]/b[2]/i|following-sibling::dd[1]/strong[2]/em")).join(" ")
      if r['release_date'].nil? or r['release_date'].empty? 
        raise "p2:Invalid data: #{r}"
      else
        records << r
      end
    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='speeches',verbose=2) unless records.length == 0
  end
end

def p3(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//ul[@id='speechIndex']/li")
    records = []
    doc.each{|li|
      r = {
        "release_date"=>li.xpath("./text()").to_s,
        "title" => text(li.xpath("div[@class='title']/a")),
        "speaker"=>text(li.xpath("div[@class='speaker']")),
        "location"=>text(li.xpath("div[@class='location']")).join(""),
        "notes"=>text(li.xpath("div[@class='boldital']")),
        "url"=> BASE_URL + attributes(li.xpath("div[@class='title']/a"),"href"),
      }
      if r['release_date'].nil? or r['release_date'].empty? 
        puts "p3:Invalid data: #{r}"
      else
        records << r
      end
    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='speeches',verbose=2) unless records.length == 0
  end
end

def p4(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//div[@id='testimonyIndex']//dt[normalize-space()]")
    records = []
    doc.each{|dt|
      r = {
        "release_date"=> text(dt.xpath("a|dt/a")),
        "url"=> BASE_URL + attributes(dt.xpath("a|dt/a"),"href"),
        "title" => text(dt.xpath("following-sibling::dd[1]/i|following-sibling::dd[1]/em")).join(""),
        "location" => dt.xpath("following-sibling::dd[1]/text()").text.strip,
      }
      r["speaker"],r["notes"]= text(dt.xpath("following-sibling::dd[1]/b|following-sibling::dd[1]/strong"))
      if r['release_date'].nil? or r['release_date'].empty? 
        raise "p4:Invalid data: #{r}"
      else
        records << r
      end

    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='testimonials',verbose=2) unless records.length == 0
  end
end

def p5(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//ul[@id='testimonyIndex']/li")
    records = []
    doc.each{|li|
      r = {
        "release_date"=>li.xpath("./text()").to_s,
        "title" => text(li.xpath("div[@class='title']/a")).join(""),
        "speaker"=>text(li.xpath("div[@class='speaker']")),
        "location"=>text(li.xpath("div[@class='location']")).join(""),
        "notes"=>text(li.xpath("div[@class='boldital']")),
        "url"=> BASE_URL + attributes(li.xpath("div[@class='title']/a"),"href"),
      }
      if r['release_date'].nil? or r['release_date'].empty? 
        puts "p5:Invalid data: #{r}"
      else
        records << r
      end
    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='testimonials',verbose=2) unless records.length == 0
  end
end


def speech(yr)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    pg = br.get(BASE_URL+"/newsevents/speech/#{yr}speech.htm") rescue retry
    p3(pg.body,"list")
  rescue Exception => e
    puts ["SP",yr,e,e.backtrace].inspect
  end
end


def testimonials(yr)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    pg = br.get(BASE_URL+"/newsevents/testimony/#{yr}testimony.htm") rescue retry
    p4(pg.body,"list")
  rescue Exception => e
    puts ["TS",yr,e].inspect
  end
end

def press_release(yr)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    pg = br.get(BASE_URL+"/newsevents/press/all/#{yr}all.htm") rescue retry
    p1(pg.body,"list")
  rescue Exception => e
    puts ["PR",yr,e].inspect
  end
end

("1996".."2005").each{|yr|
#  press_release(yr)
  testimonials(yr)
#  speech(yr)
}
#("2006".."2012").each{|yr|
  #press_release(yr)
#  testimonials(yr)
  #speech(yr)
#}#-*- encoding: utf-8 -*-
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://federalreserve.gov"

class String
  def join(arg)
    return self
  end
end

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

def p0(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//div[@id='releaseIndex']//dt")
    records = []
    doc.each{|dt|
      r = {}
      tmp = text(dt.xpath("."))
      if tmp.is_a?(Array)
        r["release_date"] = tmp[0..1].join("")
      else
        r["release_date"] = tmp.strip
      end
      r["url"] = attributes(dt.xpath("a"),"href")
      if r["url"].nil? or r["url"].empty? 
        dt.xpath("following-sibling::dd[1]//a").each{|a|
          title = text(a.xpath(".|following-sibling::text()[1]")).join("")
          records << {
            "release_date" => r["release_date"],
            "url" => BASE_URL + attributes(a.xpath("."),"href"),
            "title" => title
          } unless title.nil? or title.empty? 
        }
      else
        r["url"] = BASE_URL + r["url"]
        r["title"] = text(dt.xpath("following-sibling::dd[1]")).join(" ")
        records << r
      end

    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='press_release',verbose=2) unless records.length == 0
  end
end

def p1(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//ul[@id='releaseIndex']/li")
    records = []
    doc.each{|li|
      r = {
        "release_date"=>li.xpath("./text()").to_s,
        "title" => text(li.xpath("div[@class='indent']/a")),
        "url" => BASE_URL + attributes(li.xpath("div[@class='indent']/a"),"href"),
      }
      if r['release_date'].nil? or r['release_date'].empty? 
        puts "p0:Invalid data: #{r}"
      else
        records << r
      end
    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='press_release',verbose=2) unless records.length == 0
  end
end


def p2(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//div[@id='speechIndex']/dl/dt[normalize-space()]")
    records = []
    doc.each{|dt|
     #puts dt.xpath("following-sibling::dd[1]").inner_html.inspect
      r = {
        "release_date"=> text(dt.xpath("a|dt/a")),
        "url"=> BASE_URL + attributes(dt.xpath("a|dt/a"),"href"),
        "title" => text(dt.xpath("following-sibling::dd[1]/i|following-sibling::dd[1]/em")).join(""),
        "location" => dt.xpath("following-sibling::dd[1]/text()").text.strip,
      }
      r["speaker"] = text(dt.xpath("following-sibling::dd[1]/b[1]|following-sibling::dd[1]/strong[1]"))
      r["notes"] = text(dt.xpath("following-sibling::dd[1]/b[2]/i|following-sibling::dd[1]/strong[2]/em")).join(" ")
      if r['release_date'].nil? or r['release_date'].empty? 
        raise "p2:Invalid data: #{r}"
      else
        records << r
      end
    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='speeches',verbose=2) unless records.length == 0
  end
end

def p3(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//ul[@id='speechIndex']/li")
    records = []
    doc.each{|li|
      r = {
        "release_date"=>li.xpath("./text()").to_s,
        "title" => text(li.xpath("div[@class='title']/a")),
        "speaker"=>text(li.xpath("div[@class='speaker']")),
        "location"=>text(li.xpath("div[@class='location']")).join(""),
        "notes"=>text(li.xpath("div[@class='boldital']")),
        "url"=> BASE_URL + attributes(li.xpath("div[@class='title']/a"),"href"),
      }
      if r['release_date'].nil? or r['release_date'].empty? 
        puts "p3:Invalid data: #{r}"
      else
        records << r
      end
    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='speeches',verbose=2) unless records.length == 0
  end
end

def p4(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//div[@id='testimonyIndex']//dt[normalize-space()]")
    records = []
    doc.each{|dt|
      r = {
        "release_date"=> text(dt.xpath("a|dt/a")),
        "url"=> BASE_URL + attributes(dt.xpath("a|dt/a"),"href"),
        "title" => text(dt.xpath("following-sibling::dd[1]/i|following-sibling::dd[1]/em")).join(""),
        "location" => dt.xpath("following-sibling::dd[1]/text()").text.strip,
      }
      r["speaker"],r["notes"]= text(dt.xpath("following-sibling::dd[1]/b|following-sibling::dd[1]/strong"))
      if r['release_date'].nil? or r['release_date'].empty? 
        raise "p4:Invalid data: #{r}"
      else
        records << r
      end

    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='testimonials',verbose=2) unless records.length == 0
  end
end

def p5(data,act)
  if act == "list"
    doc = Nokogiri::HTML(data).xpath(".//ul[@id='testimonyIndex']/li")
    records = []
    doc.each{|li|
      r = {
        "release_date"=>li.xpath("./text()").to_s,
        "title" => text(li.xpath("div[@class='title']/a")).join(""),
        "speaker"=>text(li.xpath("div[@class='speaker']")),
        "location"=>text(li.xpath("div[@class='location']")).join(""),
        "notes"=>text(li.xpath("div[@class='boldital']")),
        "url"=> BASE_URL + attributes(li.xpath("div[@class='title']/a"),"href"),
      }
      if r['release_date'].nil? or r['release_date'].empty? 
        puts "p5:Invalid data: #{r}"
      else
        records << r
      end
    }
    ScraperWiki.save_sqlite(unique_keys=['title','release_date'],records,table_name='testimonials',verbose=2) unless records.length == 0
  end
end


def speech(yr)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    pg = br.get(BASE_URL+"/newsevents/speech/#{yr}speech.htm") rescue retry
    p3(pg.body,"list")
  rescue Exception => e
    puts ["SP",yr,e,e.backtrace].inspect
  end
end


def testimonials(yr)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    pg = br.get(BASE_URL+"/newsevents/testimony/#{yr}testimony.htm") rescue retry
    p4(pg.body,"list")
  rescue Exception => e
    puts ["TS",yr,e].inspect
  end
end

def press_release(yr)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
    }
    pg = br.get(BASE_URL+"/newsevents/press/all/#{yr}all.htm") rescue retry
    p1(pg.body,"list")
  rescue Exception => e
    puts ["PR",yr,e].inspect
  end
end

("1996".."2005").each{|yr|
#  press_release(yr)
  testimonials(yr)
#  speech(yr)
}
#("2006".."2012").each{|yr|
  #press_release(yr)
#  testimonials(yr)
  #speech(yr)
#}