# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://pretraga2.apr.gov.rs"

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
      return tmp
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
  records = []
  doc = Nokogiri::HTML(data).xpath(".//table[@class='ContentTable']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=> text(td[1].xpath(".")),
      "COMPANY_NAME"=> text(td[2].xpath(".")),
      "TYPE"=> text(td[0].xpath(".")),
      "STATUS"=> text(td[3].xpath(".")),
      "URL"=>attributes(td[4].xpath("a"),"href").gsub(/http:\/\/#/,""),
      "DOC" => Time.now
    }
    #puts r.inspect
    #puts [r['TYPE'],r['TYPE']=="\u041F\u0440\u0438\u0432\u0440\u0435\u0434\u043D\u043E \u0434\u0440\u0443\u0448\u0442\u0432\u043E"].inspect
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? or r['URL'].nil? or r['URL'].empty? #or r['TYPE'] == "\u041F\u0440\u0438\u0432\u0440\u0435\u0434\u043D\u043E \u0434\u0440\u0443\u0448\u0442\u0432\u043E"
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  pg = br.get(BASE_URL + "/ObjedinjenePretrage/Search/Search")
  token = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='__RequestVerificationToken']"),"value")
  begin
    s_url = BASE_URL + "/ObjedinjenePretrage/Search/SearchResult"
    params = {
     "SelectedRegisterId"=>1,
     "SearchByRegistryCodeString"=>"",
     "SearchByNameString"=>"#{srch}__",
     "X-Requested-With"=>"XMLHttpRequest",
     "__RequestVerificationToken"=>token
    }
    
    pg = br.post(s_url,params)
    return srch,scrape(pg.body)

  end
end


#save_metadata("TRIAL","A>>AB>>ABC")
trial = get_metadata("TRIAL","<non-alpha>")
srch = trial.nil? ? "<non-alpha>" : trial.split(">>").last
if srch == "<non-alpha>"
  range = ['\!','@','#','$','%','^','&','*','(',')'].to_a + (0..100).to_a + ('A1'..'Z9').to_a
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
  elsif ret == 101
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
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://pretraga2.apr.gov.rs"

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
      return tmp
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
  records = []
  doc = Nokogiri::HTML(data).xpath(".//table[@class='ContentTable']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=> text(td[1].xpath(".")),
      "COMPANY_NAME"=> text(td[2].xpath(".")),
      "TYPE"=> text(td[0].xpath(".")),
      "STATUS"=> text(td[3].xpath(".")),
      "URL"=>attributes(td[4].xpath("a"),"href").gsub(/http:\/\/#/,""),
      "DOC" => Time.now
    }
    #puts r.inspect
    #puts [r['TYPE'],r['TYPE']=="\u041F\u0440\u0438\u0432\u0440\u0435\u0434\u043D\u043E \u0434\u0440\u0443\u0448\u0442\u0432\u043E"].inspect
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? or r['URL'].nil? or r['URL'].empty? #or r['TYPE'] == "\u041F\u0440\u0438\u0432\u0440\u0435\u0434\u043D\u043E \u0434\u0440\u0443\u0448\u0442\u0432\u043E"
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  pg = br.get(BASE_URL + "/ObjedinjenePretrage/Search/Search")
  token = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='__RequestVerificationToken']"),"value")
  begin
    s_url = BASE_URL + "/ObjedinjenePretrage/Search/SearchResult"
    params = {
     "SelectedRegisterId"=>1,
     "SearchByRegistryCodeString"=>"",
     "SearchByNameString"=>"#{srch}__",
     "X-Requested-With"=>"XMLHttpRequest",
     "__RequestVerificationToken"=>token
    }
    
    pg = br.post(s_url,params)
    return srch,scrape(pg.body)

  end
end


#save_metadata("TRIAL","A>>AB>>ABC")
trial = get_metadata("TRIAL","<non-alpha>")
srch = trial.nil? ? "<non-alpha>" : trial.split(">>").last
if srch == "<non-alpha>"
  range = ['\!','@','#','$','%','^','&','*','(',')'].to_a + (0..100).to_a + ('A1'..'Z9').to_a
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
  elsif ret == 101
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
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://pretraga2.apr.gov.rs"

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
      return tmp
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
  records = []
  doc = Nokogiri::HTML(data).xpath(".//table[@class='ContentTable']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=> text(td[1].xpath(".")),
      "COMPANY_NAME"=> text(td[2].xpath(".")),
      "TYPE"=> text(td[0].xpath(".")),
      "STATUS"=> text(td[3].xpath(".")),
      "URL"=>attributes(td[4].xpath("a"),"href").gsub(/http:\/\/#/,""),
      "DOC" => Time.now
    }
    #puts r.inspect
    #puts [r['TYPE'],r['TYPE']=="\u041F\u0440\u0438\u0432\u0440\u0435\u0434\u043D\u043E \u0434\u0440\u0443\u0448\u0442\u0432\u043E"].inspect
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? or r['URL'].nil? or r['URL'].empty? #or r['TYPE'] == "\u041F\u0440\u0438\u0432\u0440\u0435\u0434\u043D\u043E \u0434\u0440\u0443\u0448\u0442\u0432\u043E"
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  pg = br.get(BASE_URL + "/ObjedinjenePretrage/Search/Search")
  token = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='__RequestVerificationToken']"),"value")
  begin
    s_url = BASE_URL + "/ObjedinjenePretrage/Search/SearchResult"
    params = {
     "SelectedRegisterId"=>1,
     "SearchByRegistryCodeString"=>"",
     "SearchByNameString"=>"#{srch}__",
     "X-Requested-With"=>"XMLHttpRequest",
     "__RequestVerificationToken"=>token
    }
    
    pg = br.post(s_url,params)
    return srch,scrape(pg.body)

  end
end


#save_metadata("TRIAL","A>>AB>>ABC")
trial = get_metadata("TRIAL","<non-alpha>")
srch = trial.nil? ? "<non-alpha>" : trial.split(">>").last
if srch == "<non-alpha>"
  range = ['\!','@','#','$','%','^','&','*','(',')'].to_a + (0..100).to_a + ('A1'..'Z9').to_a
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
  elsif ret == 101
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
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://pretraga2.apr.gov.rs"

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
      return tmp
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
  records = []
  doc = Nokogiri::HTML(data).xpath(".//table[@class='ContentTable']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER"=> text(td[1].xpath(".")),
      "COMPANY_NAME"=> text(td[2].xpath(".")),
      "TYPE"=> text(td[0].xpath(".")),
      "STATUS"=> text(td[3].xpath(".")),
      "URL"=>attributes(td[4].xpath("a"),"href").gsub(/http:\/\/#/,""),
      "DOC" => Time.now
    }
    #puts r.inspect
    #puts [r['TYPE'],r['TYPE']=="\u041F\u0440\u0438\u0432\u0440\u0435\u0434\u043D\u043E \u0434\u0440\u0443\u0448\u0442\u0432\u043E"].inspect
    records << r unless r["COMPANY_NUMBER"].nil? or r["COMPANY_NUMBER"].empty? or r['URL'].nil? or r['URL'].empty? #or r['TYPE'] == "\u041F\u0440\u0438\u0432\u0440\u0435\u0434\u043D\u043E \u0434\u0440\u0443\u0448\u0442\u0432\u043E"
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
  return doc.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history = 0
  }
  pg = br.get(BASE_URL + "/ObjedinjenePretrage/Search/Search")
  token = attributes(Nokogiri::HTML(pg.body).xpath(".//input[@name='__RequestVerificationToken']"),"value")
  begin
    s_url = BASE_URL + "/ObjedinjenePretrage/Search/SearchResult"
    params = {
     "SelectedRegisterId"=>1,
     "SearchByRegistryCodeString"=>"",
     "SearchByNameString"=>"#{srch}__",
     "X-Requested-With"=>"XMLHttpRequest",
     "__RequestVerificationToken"=>token
    }
    
    pg = br.post(s_url,params)
    return srch,scrape(pg.body)

  end
end


#save_metadata("TRIAL","A>>AB>>ABC")
trial = get_metadata("TRIAL","<non-alpha>")
srch = trial.nil? ? "<non-alpha>" : trial.split(">>").last
if srch == "<non-alpha>"
  range = ['\!','@','#','$','%','^','&','*','(',')'].to_a + (0..100).to_a + ('A1'..'Z9').to_a
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
  elsif ret == 101
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
