require 'nokogiri'
require 'mechanize'
require 'csv'

# ScraperWiki.sqliteexecute('create INDEX date_scraped_index on CMPLIST (date_scraped);')
#ScraperWiki.sqliteexecute('DELETE from CMPLIST where TYPE = "MARK";')
#exit

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://icrs.informe.org"
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
#@br.set_proxy("210.212.20.170",3128)

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    begin
      Nokogiri::HTML(data).xpath("//table[@width='100%'][1]/tr[position()>5]").each{|tr|
        td = tr.xpath("td")
        url = attributes(td[3].xpath("font/a"),"href")
        r = {
          "COMPANY_NAME" => text(td[1]),
          "TYPE" => text(td[2]),
          "URL" => BASE_URL + url,
          "COMPANY_NUMBER" => url.split("=")[1].sub('+',' '),
          "date_scraped" => Time.now
        }
        records << r if r['TYPE']=='LEGAL' #other sorts are trademarks, alt names, registered names etc
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NAME"],records,table_name="CMPLIST",verbose=2) unless records.length <=0
      len_str = text(Nokogiri::HTML(data).xpath(".//td[@bgcolor='#d3d3d3' and @colspan='4']/font[@face='Arial,Helvetica,Geneva,Swiss,SunSans-Regular']/b"))
      if len_str =~ /entities for query/
        return len_str.scan(/Found (.*) entities for query/)[0][0].to_i
      else
        return 0 
      end
    rescue Exception => e
      puts "ERROR: While scraping :: #{e.inspect} :: #{e.backtrace}"
      return 0
    end
  end
end

def action(srch)
  begin
    params = {"WAISqueryString" => srch+"%$","search"=>"search","number" =>""}
    @pg = @br.post(BASE_URL+"/nei-sos-icrs/ICRS",params)
    return scrape(@pg.body,"list")
  rescue Exception => e
    puts "Error: Unable to initialize the program :: #{e.inspect} :: #{e.backtrace}"
    exit if e.inspect =~ /refused/i
    retry
  end
end


begin
  @pg = @br.get(BASE_URL+"/nei-sos-icrs/ICRS?MainPage=x")
end

#save_metadata("TRIAL","M")
trial = get_metadata("TRIAL","A")
srch = trial.nil? ? "A" : trial.split(">>").last
if trial == "A"
  (0..999).to_a.each{|num|
    action(num)
  }
end
begin
  ret = action(srch+"__")
  if ret.nil? or ret == 0
    if trial.nil? or trial.empty? 
      srch = srch.next
      trial = srch.next
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? nil : t_s.next
      trial = (t_a << srch).join(">>")
    end
  elsif ret == 100
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
  sleep(3)
end while(true)
require 'nokogiri'
require 'mechanize'
require 'csv'

# ScraperWiki.sqliteexecute('create INDEX date_scraped_index on CMPLIST (date_scraped);')
#ScraperWiki.sqliteexecute('DELETE from CMPLIST where TYPE = "MARK";')
#exit

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://icrs.informe.org"
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
#@br.set_proxy("210.212.20.170",3128)

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    begin
      Nokogiri::HTML(data).xpath("//table[@width='100%'][1]/tr[position()>5]").each{|tr|
        td = tr.xpath("td")
        url = attributes(td[3].xpath("font/a"),"href")
        r = {
          "COMPANY_NAME" => text(td[1]),
          "TYPE" => text(td[2]),
          "URL" => BASE_URL + url,
          "COMPANY_NUMBER" => url.split("=")[1].sub('+',' '),
          "date_scraped" => Time.now
        }
        records << r if r['TYPE']=='LEGAL' #other sorts are trademarks, alt names, registered names etc
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NAME"],records,table_name="CMPLIST",verbose=2) unless records.length <=0
      len_str = text(Nokogiri::HTML(data).xpath(".//td[@bgcolor='#d3d3d3' and @colspan='4']/font[@face='Arial,Helvetica,Geneva,Swiss,SunSans-Regular']/b"))
      if len_str =~ /entities for query/
        return len_str.scan(/Found (.*) entities for query/)[0][0].to_i
      else
        return 0 
      end
    rescue Exception => e
      puts "ERROR: While scraping :: #{e.inspect} :: #{e.backtrace}"
      return 0
    end
  end
end

def action(srch)
  begin
    params = {"WAISqueryString" => srch+"%$","search"=>"search","number" =>""}
    @pg = @br.post(BASE_URL+"/nei-sos-icrs/ICRS",params)
    return scrape(@pg.body,"list")
  rescue Exception => e
    puts "Error: Unable to initialize the program :: #{e.inspect} :: #{e.backtrace}"
    exit if e.inspect =~ /refused/i
    retry
  end
end


begin
  @pg = @br.get(BASE_URL+"/nei-sos-icrs/ICRS?MainPage=x")
end

#save_metadata("TRIAL","M")
trial = get_metadata("TRIAL","A")
srch = trial.nil? ? "A" : trial.split(">>").last
if trial == "A"
  (0..999).to_a.each{|num|
    action(num)
  }
end
begin
  ret = action(srch+"__")
  if ret.nil? or ret == 0
    if trial.nil? or trial.empty? 
      srch = srch.next
      trial = srch.next
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? nil : t_s.next
      trial = (t_a << srch).join(">>")
    end
  elsif ret == 100
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
  sleep(3)
end while(true)
require 'nokogiri'
require 'mechanize'
require 'csv'

# ScraperWiki.sqliteexecute('create INDEX date_scraped_index on CMPLIST (date_scraped);')
#ScraperWiki.sqliteexecute('DELETE from CMPLIST where TYPE = "MARK";')
#exit

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://icrs.informe.org"
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
#@br.set_proxy("210.212.20.170",3128)

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    begin
      Nokogiri::HTML(data).xpath("//table[@width='100%'][1]/tr[position()>5]").each{|tr|
        td = tr.xpath("td")
        url = attributes(td[3].xpath("font/a"),"href")
        r = {
          "COMPANY_NAME" => text(td[1]),
          "TYPE" => text(td[2]),
          "URL" => BASE_URL + url,
          "COMPANY_NUMBER" => url.split("=")[1].sub('+',' '),
          "date_scraped" => Time.now
        }
        records << r if r['TYPE']=='LEGAL' #other sorts are trademarks, alt names, registered names etc
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NAME"],records,table_name="CMPLIST",verbose=2) unless records.length <=0
      len_str = text(Nokogiri::HTML(data).xpath(".//td[@bgcolor='#d3d3d3' and @colspan='4']/font[@face='Arial,Helvetica,Geneva,Swiss,SunSans-Regular']/b"))
      if len_str =~ /entities for query/
        return len_str.scan(/Found (.*) entities for query/)[0][0].to_i
      else
        return 0 
      end
    rescue Exception => e
      puts "ERROR: While scraping :: #{e.inspect} :: #{e.backtrace}"
      return 0
    end
  end
end

def action(srch)
  begin
    params = {"WAISqueryString" => srch+"%$","search"=>"search","number" =>""}
    @pg = @br.post(BASE_URL+"/nei-sos-icrs/ICRS",params)
    return scrape(@pg.body,"list")
  rescue Exception => e
    puts "Error: Unable to initialize the program :: #{e.inspect} :: #{e.backtrace}"
    exit if e.inspect =~ /refused/i
    retry
  end
end


begin
  @pg = @br.get(BASE_URL+"/nei-sos-icrs/ICRS?MainPage=x")
end

#save_metadata("TRIAL","M")
trial = get_metadata("TRIAL","A")
srch = trial.nil? ? "A" : trial.split(">>").last
if trial == "A"
  (0..999).to_a.each{|num|
    action(num)
  }
end
begin
  ret = action(srch+"__")
  if ret.nil? or ret == 0
    if trial.nil? or trial.empty? 
      srch = srch.next
      trial = srch.next
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? nil : t_s.next
      trial = (t_a << srch).join(">>")
    end
  elsif ret == 100
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
  sleep(3)
end while(true)
require 'nokogiri'
require 'mechanize'
require 'csv'

# ScraperWiki.sqliteexecute('create INDEX date_scraped_index on CMPLIST (date_scraped);')
#ScraperWiki.sqliteexecute('DELETE from CMPLIST where TYPE = "MARK";')
#exit

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://icrs.informe.org"
@br = Mechanize.new { |b|
  b.user_agent_alias = 'Mac Safari'
  b.read_timeout = 1200
  b.max_history=0
  b.retry_change_requests = true
  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
}
#@br.set_proxy("210.212.20.170",3128)

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
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data,action)
  if action == "list"
    records = []
    begin
      Nokogiri::HTML(data).xpath("//table[@width='100%'][1]/tr[position()>5]").each{|tr|
        td = tr.xpath("td")
        url = attributes(td[3].xpath("font/a"),"href")
        r = {
          "COMPANY_NAME" => text(td[1]),
          "TYPE" => text(td[2]),
          "URL" => BASE_URL + url,
          "COMPANY_NUMBER" => url.split("=")[1].sub('+',' '),
          "date_scraped" => Time.now
        }
        records << r if r['TYPE']=='LEGAL' #other sorts are trademarks, alt names, registered names etc
      }
      ScraperWiki.save_sqlite(unique_keys=["COMPANY_NAME"],records,table_name="CMPLIST",verbose=2) unless records.length <=0
      len_str = text(Nokogiri::HTML(data).xpath(".//td[@bgcolor='#d3d3d3' and @colspan='4']/font[@face='Arial,Helvetica,Geneva,Swiss,SunSans-Regular']/b"))
      if len_str =~ /entities for query/
        return len_str.scan(/Found (.*) entities for query/)[0][0].to_i
      else
        return 0 
      end
    rescue Exception => e
      puts "ERROR: While scraping :: #{e.inspect} :: #{e.backtrace}"
      return 0
    end
  end
end

def action(srch)
  begin
    params = {"WAISqueryString" => srch+"%$","search"=>"search","number" =>""}
    @pg = @br.post(BASE_URL+"/nei-sos-icrs/ICRS",params)
    return scrape(@pg.body,"list")
  rescue Exception => e
    puts "Error: Unable to initialize the program :: #{e.inspect} :: #{e.backtrace}"
    exit if e.inspect =~ /refused/i
    retry
  end
end


begin
  @pg = @br.get(BASE_URL+"/nei-sos-icrs/ICRS?MainPage=x")
end

#save_metadata("TRIAL","M")
trial = get_metadata("TRIAL","A")
srch = trial.nil? ? "A" : trial.split(">>").last
if trial == "A"
  (0..999).to_a.each{|num|
    action(num)
  }
end
begin
  ret = action(srch+"__")
  if ret.nil? or ret == 0
    if trial.nil? or trial.empty? 
      srch = srch.next
      trial = srch.next
    else
      t_a = trial.split(">>")
      t_s = t_a.pop
      t_s = t_a.pop until t_s=='Z' or not t_s.split(//).last == 'Z'
      srch = (t_s == 'Z')? nil : t_s.next
      trial = (t_a << srch).join(">>")
    end
  elsif ret == 100
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
  sleep(3)
end while(true)
