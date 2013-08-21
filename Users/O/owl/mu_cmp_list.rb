# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0'
  b.read_timeout = 3600
  b.max_history=0
  b.keep_alive = true
  b.retry_change_requests = true
  #b.cert_store = cert_store
  #b.log = Logger.new(STDERR)
  b.verify_mode= OpenSSL::SSL::VERIFY_NONE
}

BASE_URL = "https://mns-portal.intnet.mu"

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
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act)
  if act == "main"
    doc = Nokogiri::HTML(data).xpath(".//*[@id='PageDiv']/table[2]/tr[position()>2]")
    records = []
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NUMBER"=>text(td[1].xpath("div")),
        "BR_NO"=>text(td[2].xpath("div")),
        "COMPANY_NAME"=>text(td[3].xpath("div")),
        "REG_DT"=>text(td[4].xpath("div")),
        "STATUS"=>text(td[5].xpath("div")),
        "URL"=>BASE_URL+"/cbris-name-search/"+attributes(td[0].xpath("div/a"),"href"),
        "DOC"=>Time.now
      }
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
    return doc.length
  elsif act == "others"
    doc = Nokogiri::HTML(data).xpath(".//*[@id='PageDiv']/table[2]/tr[position()>2]")
    return doc.length
  end 
end

def action(from,to,act)
  #@br = HTTPClient.new{|b|
  #  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  #}
  begin
    main_url = BASE_URL+"/cbris-name-search/MASTActionServlet?do=ViewList&act=search&id=ViewListCBRISDate.xml"
    others_url = BASE_URL+"/cbris-name-search/MASTActionServlet?do=ViewList&act=search&id=ViewListCBRISOthersDate.xml"
    if act == "main"
      
      pg = @br.get(main_url)
      params = {"referer"=>main_url,"FIL_1_1"=>"%","FIL_1_3"=>from,"FIL_1_3_DateTo"=>to}
      pg.form_with(:name=>"frm") do |f|
        params.each{|k,v| f[k] = v }
        pg = f.submit
      end
      scrape(pg.body,"main")
      begin
        nex = attributes(Nokogiri::HTML(pg.body).xpath(".//a[text()='Next']"),"href")
        break if nex.nil? or nex.empty? 
        params["pagenumber"]=nex.split("'")[1]
        pg.form_with(:name=>"frm") do |f|
          params.each{|k,v| f[k] = v }
          pg = f.submit
        end
        scrape(pg.body,"main")
      end while(true)
    elsif act == "others"
      pg = br.get(other_url)
      params = {"referer"=>main_url,"FIL_1_3"=>from,"FIL_1_1"=>"%","Message3"=>"Date To must be after Date From.","FIL_1_3_DateTo"=>to}
      pg.form_with(:name=>"frm") do |f|
        params.each{|k,v| f[k] = v }
        pg = f.submit
      end
      begin
        nex = attributes(Nokogiri::HTML(pg.body).xpath(".//a[text()='Next']"),"href")
        break if nex.nil? or nex.empty? 
        params["pagenumber"]=nex.split("'")[1]
        pg.form_with(:name=>"frm") do |f|
          params.each{|k,v| f[k] = v }
          pg = f.submit
        end
        scrape(pg.body,"main")
      end while(true)
    end
  end
end

action(Date.new(Date.today.year,Date.today.month,1).strftime("%d/%m/%Y"),Date.new(Date.today.year,Date.today.month,-1).strftime("%d/%m/%Y"),"main")
#puts Gem.loaded_specs["mechanize"].version
#puts Gem.loaded_specs["net-http-persistent"].version
#puts Gem.loaded_specs["nokogiri"].version
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

@br = Mechanize.new { |b|
  b.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0'
  b.read_timeout = 3600
  b.max_history=0
  b.keep_alive = true
  b.retry_change_requests = true
  #b.cert_store = cert_store
  #b.log = Logger.new(STDERR)
  b.verify_mode= OpenSSL::SSL::VERIFY_NONE
}

BASE_URL = "https://mns-portal.intnet.mu"

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
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act)
  if act == "main"
    doc = Nokogiri::HTML(data).xpath(".//*[@id='PageDiv']/table[2]/tr[position()>2]")
    records = []
    doc.each{|tr|
      td = tr.xpath("td")
      r = {
        "COMPANY_NUMBER"=>text(td[1].xpath("div")),
        "BR_NO"=>text(td[2].xpath("div")),
        "COMPANY_NAME"=>text(td[3].xpath("div")),
        "REG_DT"=>text(td[4].xpath("div")),
        "STATUS"=>text(td[5].xpath("div")),
        "URL"=>BASE_URL+"/cbris-name-search/"+attributes(td[0].xpath("div/a"),"href"),
        "DOC"=>Time.now
      }
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='swdata',verbose=2) unless records.length == 0
    return doc.length
  elsif act == "others"
    doc = Nokogiri::HTML(data).xpath(".//*[@id='PageDiv']/table[2]/tr[position()>2]")
    return doc.length
  end 
end

def action(from,to,act)
  #@br = HTTPClient.new{|b|
  #  b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  #}
  begin
    main_url = BASE_URL+"/cbris-name-search/MASTActionServlet?do=ViewList&act=search&id=ViewListCBRISDate.xml"
    others_url = BASE_URL+"/cbris-name-search/MASTActionServlet?do=ViewList&act=search&id=ViewListCBRISOthersDate.xml"
    if act == "main"
      
      pg = @br.get(main_url)
      params = {"referer"=>main_url,"FIL_1_1"=>"%","FIL_1_3"=>from,"FIL_1_3_DateTo"=>to}
      pg.form_with(:name=>"frm") do |f|
        params.each{|k,v| f[k] = v }
        pg = f.submit
      end
      scrape(pg.body,"main")
      begin
        nex = attributes(Nokogiri::HTML(pg.body).xpath(".//a[text()='Next']"),"href")
        break if nex.nil? or nex.empty? 
        params["pagenumber"]=nex.split("'")[1]
        pg.form_with(:name=>"frm") do |f|
          params.each{|k,v| f[k] = v }
          pg = f.submit
        end
        scrape(pg.body,"main")
      end while(true)
    elsif act == "others"
      pg = br.get(other_url)
      params = {"referer"=>main_url,"FIL_1_3"=>from,"FIL_1_1"=>"%","Message3"=>"Date To must be after Date From.","FIL_1_3_DateTo"=>to}
      pg.form_with(:name=>"frm") do |f|
        params.each{|k,v| f[k] = v }
        pg = f.submit
      end
      begin
        nex = attributes(Nokogiri::HTML(pg.body).xpath(".//a[text()='Next']"),"href")
        break if nex.nil? or nex.empty? 
        params["pagenumber"]=nex.split("'")[1]
        pg.form_with(:name=>"frm") do |f|
          params.each{|k,v| f[k] = v }
          pg = f.submit
        end
        scrape(pg.body,"main")
      end while(true)
    end
  end
end

action(Date.new(Date.today.year,Date.today.month,1).strftime("%d/%m/%Y"),Date.new(Date.today.year,Date.today.month,-1).strftime("%d/%m/%Y"),"main")
#puts Gem.loaded_specs["mechanize"].version
#puts Gem.loaded_specs["net-http-persistent"].version
#puts Gem.loaded_specs["nokogiri"].version
