# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.bbc.co.uk"

class String
  def join(str)
    self+str
  end
  def pretty
    self.gsub(/\u00A0|&nbsp;/," ").gsub(/<br>|<i>|<\/i>/,"").gsub(/<A name=[0-9]><\/a>/,"").strip
  end
end
class Array
  def pretty
    self.join(";").gsub(/\u00A0|^:|;$/,'').strip
  end
end
class Hash
  def len
    self.delete_if{|k,v| v.nil? }.length
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
  tmp = []
  str.collect{|st| tmp << st.text.strip}
  return tmp.delete_if{|a| a.nil? or a.empty?}
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act,rec,seq)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//h2[@class='section-header']")
    doc.each{|ele|
      id = attributes(ele.xpath("."),"id")
      r = {"REGION"=>text(ele.xpath(".")).join("")}
      lnks = []
      ele.xpath("./following-sibling::p[preceding-sibling::h2[1][@id='#{id}']]").each{|lnk|
        lnks << attributes(lnk.xpath("./a"),"href")
      }
      r["LINKS"] = lnks
      records << r
    }
    return records
  elsif act == "details"
  records,idx = [],0
  begin
    if data[idx].pretty =~ /^#{seq}$/
      r = {}
      r['Day'] = data[idx].pretty
      idx = idx + 1
      
      tmp = data[idx].pretty
      #puts [tmp].inspect
      if tmp =~ /^\d+:\d+/
        if tmp =~ /[a-z]/
          r['Time'],r['Community'] = tmp.split(/(\d+\:\d+) (.*)/).delete_if{|a| a.empty?}
          idx = idx + 1
        else
          r['Time'] = tmp
          idx = idx + 1
          r['Community'] = data[idx].pretty
          idx = idx + 1
        end

      else
        r['Community'] = data[idx].pretty
        idx = idx + 1
      end
      #puts [tmp,tmp=~/^\d+\d+/,r,data[idx].pretty].inspect
      #puts [data[idx-r.len..idx]].flatten.inspect

      if not data[idx].pretty =~ /^#{r['Day']}/
        r['Travelling_on'] = data[idx].pretty
        idx = idx + 1
      end
      #puts r.inspect
      records << r.merge(rec)
    else
      idx = idx + 1
    end
    break if idx >= data.length
    end while(true)
    ScraperWiki.save_sqlite(unique_keys=[],records,table_name='swdata',verbose=2) unless records.length == 0
  end
end

def process_pdf(lnk,ele)
  file_name = lnk.split("/").last.split(".").first
  seq = lnk.scan(/day([0-9]+)/).flatten.first.to_i
  @br.get(lnk).save_as("#{file_name}.pdf")
  %x[/usr/bin/pdftohtml -noframes -i -enc UTF-8 #{file_name}.pdf >/dev/null]
  file = IO.readlines("#{file_name}.html").join("").force_encoding("UTF-8").split("\n")
  dt = Date.strptime(lnk.scan(/(\d+_\d+_\d+)_day/).flatten.first,"%d_%m_%y")
  from,to = lnk.scan(/day\d+_(.*)_(.*)\.pdf/).flatten
  scrape(file,"details",{"Region"=>ele['REGION'],"Date"=>dt,"From"=>from,"To"=>to},seq)
end

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

def action()
  s_url = BASE_URL + "/news/uk-17358291"
  list = scrape(@br.get(s_url).body,"list",nil,nil)
  list.each{|ele|
    ele['LINKS'].each{|lnk|
      process_pdf(lnk,ele)
    }
  }
end

action()

#process_pdf("http://news.bbc.co.uk/1/shared/bsp/hi/pdfs/19_03_12_day3_exeter_taunton.pdf","SOUTH WEST ENGLAND")# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.bbc.co.uk"

class String
  def join(str)
    self+str
  end
  def pretty
    self.gsub(/\u00A0|&nbsp;/," ").gsub(/<br>|<i>|<\/i>/,"").gsub(/<A name=[0-9]><\/a>/,"").strip
  end
end
class Array
  def pretty
    self.join(";").gsub(/\u00A0|^:|;$/,'').strip
  end
end
class Hash
  def len
    self.delete_if{|k,v| v.nil? }.length
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
  tmp = []
  str.collect{|st| tmp << st.text.strip}
  return tmp.delete_if{|a| a.nil? or a.empty?}
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,act,rec,seq)
  if act == "list"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//h2[@class='section-header']")
    doc.each{|ele|
      id = attributes(ele.xpath("."),"id")
      r = {"REGION"=>text(ele.xpath(".")).join("")}
      lnks = []
      ele.xpath("./following-sibling::p[preceding-sibling::h2[1][@id='#{id}']]").each{|lnk|
        lnks << attributes(lnk.xpath("./a"),"href")
      }
      r["LINKS"] = lnks
      records << r
    }
    return records
  elsif act == "details"
  records,idx = [],0
  begin
    if data[idx].pretty =~ /^#{seq}$/
      r = {}
      r['Day'] = data[idx].pretty
      idx = idx + 1
      
      tmp = data[idx].pretty
      #puts [tmp].inspect
      if tmp =~ /^\d+:\d+/
        if tmp =~ /[a-z]/
          r['Time'],r['Community'] = tmp.split(/(\d+\:\d+) (.*)/).delete_if{|a| a.empty?}
          idx = idx + 1
        else
          r['Time'] = tmp
          idx = idx + 1
          r['Community'] = data[idx].pretty
          idx = idx + 1
        end

      else
        r['Community'] = data[idx].pretty
        idx = idx + 1
      end
      #puts [tmp,tmp=~/^\d+\d+/,r,data[idx].pretty].inspect
      #puts [data[idx-r.len..idx]].flatten.inspect

      if not data[idx].pretty =~ /^#{r['Day']}/
        r['Travelling_on'] = data[idx].pretty
        idx = idx + 1
      end
      #puts r.inspect
      records << r.merge(rec)
    else
      idx = idx + 1
    end
    break if idx >= data.length
    end while(true)
    ScraperWiki.save_sqlite(unique_keys=[],records,table_name='swdata',verbose=2) unless records.length == 0
  end
end

def process_pdf(lnk,ele)
  file_name = lnk.split("/").last.split(".").first
  seq = lnk.scan(/day([0-9]+)/).flatten.first.to_i
  @br.get(lnk).save_as("#{file_name}.pdf")
  %x[/usr/bin/pdftohtml -noframes -i -enc UTF-8 #{file_name}.pdf >/dev/null]
  file = IO.readlines("#{file_name}.html").join("").force_encoding("UTF-8").split("\n")
  dt = Date.strptime(lnk.scan(/(\d+_\d+_\d+)_day/).flatten.first,"%d_%m_%y")
  from,to = lnk.scan(/day\d+_(.*)_(.*)\.pdf/).flatten
  scrape(file,"details",{"Region"=>ele['REGION'],"Date"=>dt,"From"=>from,"To"=>to},seq)
end

@br = Mechanize.new { |b|
  b.user_agent_alias = 'Linux Firefox'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}

def action()
  s_url = BASE_URL + "/news/uk-17358291"
  list = scrape(@br.get(s_url).body,"list",nil,nil)
  list.each{|ele|
    ele['LINKS'].each{|lnk|
      process_pdf(lnk,ele)
    }
  }
end

action()

#process_pdf("http://news.bbc.co.uk/1/shared/bsp/hi/pdfs/19_03_12_day3_exeter_taunton.pdf","SOUTH WEST ENGLAND")