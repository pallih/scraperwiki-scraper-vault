# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.moic.gov.bh/CReServices/inquiry/"

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
      str.collect{|st| tmp << st.text.strip}
      return tmp.join(" ")
    end
  rescue Exception => e
    puts e.inspect
    return str.text unless str.nil? 
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  doc = Nokogiri::HTML(data).xpath(".//div[@class='suchergebnis_gesamt']/div[@class='suchergebnis']/div[@class='vcard mapme']")
  doc.each{|div|
    
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.xpath("a").length
end

def action(dt)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
      b.verify_mode = OpenSSL::SSL::VERIFY_NONE
      #b.log = Logger.new(STDERR)
    }
    s_url = BASE_URL+"CREnqiury.aspx"
    pg = br.get(s_url)
    params = {'__EVENTTARGET'=>'FindCRAdvanceSearch'}
    pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
    params = {'__EVENTTARGET'=>'lnkShowMoreCRSearchOptions'}
    pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
    params = {'__EVENTTARGET'=>'ddlToMonth','ddlFromMonth'=>1,'ddlToMonth'=>1}
    2.times{
      pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
    }
    params = {
      'ddlFromDay'=>dt.day,'ddlFromMonth'=>dt.month,'ddlFromYear'=>dt.year,'ddlToDay'=>dt.next.day,'ddlToMonth'=>dt.next.month,'ddlTOYear'=>dt.next.year,
      'btnFindCr'=>'Submit'}
    pg.form_with(:name => "form1") do |f|
      params.each{|k,v| f[k]=v }
      pg = f.submit
    end
    ttl = scrape(pg.body)
    begin
      nex = text(Nokogiri::HTML(pg.body).xpath(".//td/table[@border and not(@cellpadding)]/tbody/tr/td[span]/following-sibling::td[1]/a"))
      break if nex.nil? or nex.empty? 
      params = {"__EVENTTARGET"=>"grdCR","__EVENTARGUMENT"=>"Page$#{nex}"}
      pg.form_with(:name=>"Form1") do |f|
        params.each{|k,v| f[k]=v }
        pg = f.submit    
      end
      ttl = ttl + scrape(pg.body)
    rescue Exception=>e
      puts "ERROR: While looping #{dt} :: #{e.inspect} :: #{e.backtrace}"  
      retry
    end while(true)
  rescue Exception => e
    puts "ERROR: While processing #{dt} :: #{e.inspect} :: #{e.backtrace}"
    retry
  end
  return ttl
end

#save_metadata("TRIAL","S")
#delete_metadata("OFFSET")
trial = get_metadata("TRIAL","<non-alpha>")
srch = trial.nil? ? "<non-alpha>" : trial.split(">>").last
if srch == "<non-alpha>"
  range = ['\!','@','#','$','%','^','&','*','(',')'].to_a + (0..100).to_a
  offset = get_metadata("OFFSET",0)
  #breaif offset >= range.length
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
  elsif ret == 200
    srch = srch+'A'
    trial = (trial.nil? or trial.empty?)? srch : (trial + ">>" + srch)
  else
    t_a = trial.split(">>")
    t_s = t_a.pop
    t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
    srch = (t_s == 'Z')? nil : t_s.next
    trial = (t_a << srch).join(">>")
  end
  if srch.nil? 
    delete_metadata("TRIAL")
    break
  end
  save_metadata("TRIAL",trial)
end while(true)
