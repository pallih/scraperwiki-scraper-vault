# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://appext9.dos.state.ny.us/corp_public/"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    retry
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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
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

def scrape(data)
  records = []
  doc = Nokogiri::HTML(data,nil,"ISO-8859-1").xpath(".//table[@summary='This table contains links to entity information for the entities found.']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME" => text(td[0].xpath("a")),
      "URL" => BASE_URL+attributes(td[0].xpath("a"),"href"),
      "DOC" => Time.now
    }
    r['NAME_ID'],r['COMPANY_NUMBER'] = r['URL'].scan(/p_nameid=(.*)&p_corpid=(.*)&p_entity_name/)[0]
    records << r unless r['COMPANY_NUMBER'].nil? or r['NAME_ID'].nil? 
  }
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length==0
  return doc.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    params = {"p_entity_name"=>srch,"p_name_type"=>"%","p_search_type"=>"BEGINS"}
    s_url = BASE_URL + "CORPSEARCH.SELECT_ENTITY"
    pg = br.post(s_url,params)
    ttl = scrape(pg.body)

    begin
      nex = pg.link_with(:text => "Next Page")
      break if nex.nil? 
      pg = br.click(nex)
      ttl = ttl + scrape(pg.body)
    rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while true
    return srch,ttl
  end
end

#delete_metadata("OFFSET")
#save_metadata("TRIAL","C")
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
  if srch.nil? 
    delete_metadata("TRIAL")
    break
  end
  save_metadata("TRIAL",trial)
end while(true)

# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://appext9.dos.state.ny.us/corp_public/"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    retry
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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
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

def scrape(data)
  records = []
  doc = Nokogiri::HTML(data,nil,"ISO-8859-1").xpath(".//table[@summary='This table contains links to entity information for the entities found.']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME" => text(td[0].xpath("a")),
      "URL" => BASE_URL+attributes(td[0].xpath("a"),"href"),
      "DOC" => Time.now
    }
    r['NAME_ID'],r['COMPANY_NUMBER'] = r['URL'].scan(/p_nameid=(.*)&p_corpid=(.*)&p_entity_name/)[0]
    records << r unless r['COMPANY_NUMBER'].nil? or r['NAME_ID'].nil? 
  }
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length==0
  return doc.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    params = {"p_entity_name"=>srch,"p_name_type"=>"%","p_search_type"=>"BEGINS"}
    s_url = BASE_URL + "CORPSEARCH.SELECT_ENTITY"
    pg = br.post(s_url,params)
    ttl = scrape(pg.body)

    begin
      nex = pg.link_with(:text => "Next Page")
      break if nex.nil? 
      pg = br.click(nex)
      ttl = ttl + scrape(pg.body)
    rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while true
    return srch,ttl
  end
end

#delete_metadata("OFFSET")
#save_metadata("TRIAL","C")
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
  if srch.nil? 
    delete_metadata("TRIAL")
    break
  end
  save_metadata("TRIAL",trial)
end while(true)

# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://appext9.dos.state.ny.us/corp_public/"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    retry
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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
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

def scrape(data)
  records = []
  doc = Nokogiri::HTML(data,nil,"ISO-8859-1").xpath(".//table[@summary='This table contains links to entity information for the entities found.']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME" => text(td[0].xpath("a")),
      "URL" => BASE_URL+attributes(td[0].xpath("a"),"href"),
      "DOC" => Time.now
    }
    r['NAME_ID'],r['COMPANY_NUMBER'] = r['URL'].scan(/p_nameid=(.*)&p_corpid=(.*)&p_entity_name/)[0]
    records << r unless r['COMPANY_NUMBER'].nil? or r['NAME_ID'].nil? 
  }
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length==0
  return doc.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    params = {"p_entity_name"=>srch,"p_name_type"=>"%","p_search_type"=>"BEGINS"}
    s_url = BASE_URL + "CORPSEARCH.SELECT_ENTITY"
    pg = br.post(s_url,params)
    ttl = scrape(pg.body)

    begin
      nex = pg.link_with(:text => "Next Page")
      break if nex.nil? 
      pg = br.click(nex)
      ttl = ttl + scrape(pg.body)
    rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while true
    return srch,ttl
  end
end

#delete_metadata("OFFSET")
#save_metadata("TRIAL","C")
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
  if srch.nil? 
    delete_metadata("TRIAL")
    break
  end
  save_metadata("TRIAL",trial)
end while(true)

# encoding: ISO-8859-1
require 'nokogiri'
require 'mechanize'
require 'csv'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://appext9.dos.state.ny.us/corp_public/"

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    retry
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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
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

def scrape(data)
  records = []
  doc = Nokogiri::HTML(data,nil,"ISO-8859-1").xpath(".//table[@summary='This table contains links to entity information for the entities found.']/tr[position()>1]")
  doc.each{|tr|
    td = tr.xpath("td")
    r = {
      "COMPANY_NAME" => text(td[0].xpath("a")),
      "URL" => BASE_URL+attributes(td[0].xpath("a"),"href"),
      "DOC" => Time.now
    }
    r['NAME_ID'],r['COMPANY_NUMBER'] = r['URL'].scan(/p_nameid=(.*)&p_corpid=(.*)&p_entity_name/)[0]
    records << r unless r['COMPANY_NUMBER'].nil? or r['NAME_ID'].nil? 
  }
  ScraperWiki.save_sqlite(unique_keys=["COMPANY_NUMBER"],records,table_name="swdata",verbose=2) unless records.length==0
  return doc.length
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history = 0
    }
    params = {"p_entity_name"=>srch,"p_name_type"=>"%","p_search_type"=>"BEGINS"}
    s_url = BASE_URL + "CORPSEARCH.SELECT_ENTITY"
    pg = br.post(s_url,params)
    ttl = scrape(pg.body)

    begin
      nex = pg.link_with(:text => "Next Page")
      break if nex.nil? 
      pg = br.click(nex)
      ttl = ttl + scrape(pg.body)
    rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    end while true
    return srch,ttl
  end
end

#delete_metadata("OFFSET")
#save_metadata("TRIAL","C")
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
  if srch.nil? 
    delete_metadata("TRIAL")
    break
  end
  save_metadata("TRIAL",trial)
end while(true)

