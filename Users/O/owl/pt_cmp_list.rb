# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.portaldaempresa.pt"

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


def scrape(data,act)
  if act == "details"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='dataGridResultado']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      break unless td.length == 6
      r = {
        "COMPANY_NUMBER"=>attributes(td[0].xpath("input"),"value"),
        "CERTIFICATE_NUMBER"=>attributes(td[1].xpath("input"),"value"),
        "COMPANY_NAME"=>text(td[2].xpath(".")),
        "COUNTY"=>text(td[3].xpath(".")),
        "STATUS"=>text(td[4].xpath(".")),
        "DOC"=>Time.now
      }
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    }
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length==0
  end
end

def action(srch,force)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
   }
  
  begin
    pg = br.get(BASE_URL+"/RegistoOnline/Services/PesquisaSICONF/PesquisaSICONF.aspx") rescue retry 
    params = { "ctl00$phBody$txtbxNome"=>(force ==1)? srch.gsub(//,'*') : srch, "ctl00$phBody$btnPesquisar"=>"Pesquisar"}
    pg.form_with(:id => "form1") do |f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
    params = { "ctl00$phBody$btnListaCompleta"=>"Ver lista completa" }
    pg.form_with(:id=>'form1') do |f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
  rescue Exception=>e
    if e.inspect =~ /internal/i
      if pg.body =~ /foram encontrados registos/i
        if force == 0
          return
        else
          force = 0
          retry
        end
      else
        return
      end
    elsif e.inspect =~ /HTTPFatalError/i
      raise e
    else
      puts "Failing to parse #{srch}::#{force}::#{e.inspect}::#{e.backtrace}"
      retry
    end
  end
  r_cnt = 0
  begin
   return nil if pg.nil? or pg.body.force_encoding("UTF-8") =~ /Desculpe o incómodo. Serviço momentaneamente indisponível por falha de comunicações./
   scrape(pg.body.gsub(/id="__VIEWSTATE" value=(.*)>/,">"),"details")
   len = Nokogiri.HTML(pg.body).xpath(".//*[@id='dataGridResultado']/tr[position()>1]").length
   nxt_t = attributes(Nokogiri::HTML(pg.body).xpath(".//*[@id='dataGridResultado']/tr[position()>last()-1]/td/span/following-sibling::a[1]"),"href")
   nxt = (nxt_t.nil? or nxt_t.empty?)? nil : nxt_t.split("'")[1]
   if len==0 or (nxt.nil? or nxt.empty?)
     break
   else
     begin
       params = {"__EVENTARGUMENT"=>"","__EVENTTARGET"=>nxt}
       pg.form_with(:id=>'form1') do |f|
         params.each{|k,v| f[k]=v}
         pg = f.submit
       end
     rescue Exception=>e
       puts "Failing to get the search pages #{srch}::#{force}::#{e.inspect}"
       r_cnt = r_cnt+1
       break if r_cnt == 30
       retry 
     end
   end
  rescue Exception => e
   puts "Failing to parse #{srch}::#{force}::#{e.inspect}::#{e.backtrace}"
   raise e
  end while(true)
end

Mechanize.new().get("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=scrabble_word_lists&query=select+word+from+%60swdata%60&apikey=").save_as("word_list.csv") rescue retry
range = IO.readlines("word_list.csv") + ('a'..'zzzz').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >=range.length

range.each_with_index{|srch,idx|
  next if idx < offset
  srch = srch.strip
  action(srch,0)
  save_metadata("OFFSET",idx.next)
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "https://www.portaldaempresa.pt"

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


def scrape(data,act)
  if act == "details"
    records = []
    Nokogiri::HTML(data).xpath(".//table[@id='dataGridResultado']/tr[position()>1]").each{|tr|
      td = tr.xpath("td")
      break unless td.length == 6
      r = {
        "COMPANY_NUMBER"=>attributes(td[0].xpath("input"),"value"),
        "CERTIFICATE_NUMBER"=>attributes(td[1].xpath("input"),"value"),
        "COMPANY_NAME"=>text(td[2].xpath(".")),
        "COUNTY"=>text(td[3].xpath(".")),
        "STATUS"=>text(td[4].xpath(".")),
        "DOC"=>Time.now
      }
      records << r unless r['COMPANY_NUMBER'].nil? or r['COMPANY_NUMBER'].empty? 
    }
    ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length==0
  end
end

def action(srch,force)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
   }
  
  begin
    pg = br.get(BASE_URL+"/RegistoOnline/Services/PesquisaSICONF/PesquisaSICONF.aspx") rescue retry 
    params = { "ctl00$phBody$txtbxNome"=>(force ==1)? srch.gsub(//,'*') : srch, "ctl00$phBody$btnPesquisar"=>"Pesquisar"}
    pg.form_with(:id => "form1") do |f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
    params = { "ctl00$phBody$btnListaCompleta"=>"Ver lista completa" }
    pg.form_with(:id=>'form1') do |f|
      params.each{|k,v| f[k]=v}
      pg = f.submit
    end
  rescue Exception=>e
    if e.inspect =~ /internal/i
      if pg.body =~ /foram encontrados registos/i
        if force == 0
          return
        else
          force = 0
          retry
        end
      else
        return
      end
    elsif e.inspect =~ /HTTPFatalError/i
      raise e
    else
      puts "Failing to parse #{srch}::#{force}::#{e.inspect}::#{e.backtrace}"
      retry
    end
  end
  r_cnt = 0
  begin
   return nil if pg.nil? or pg.body.force_encoding("UTF-8") =~ /Desculpe o incómodo. Serviço momentaneamente indisponível por falha de comunicações./
   scrape(pg.body.gsub(/id="__VIEWSTATE" value=(.*)>/,">"),"details")
   len = Nokogiri.HTML(pg.body).xpath(".//*[@id='dataGridResultado']/tr[position()>1]").length
   nxt_t = attributes(Nokogiri::HTML(pg.body).xpath(".//*[@id='dataGridResultado']/tr[position()>last()-1]/td/span/following-sibling::a[1]"),"href")
   nxt = (nxt_t.nil? or nxt_t.empty?)? nil : nxt_t.split("'")[1]
   if len==0 or (nxt.nil? or nxt.empty?)
     break
   else
     begin
       params = {"__EVENTARGUMENT"=>"","__EVENTTARGET"=>nxt}
       pg.form_with(:id=>'form1') do |f|
         params.each{|k,v| f[k]=v}
         pg = f.submit
       end
     rescue Exception=>e
       puts "Failing to get the search pages #{srch}::#{force}::#{e.inspect}"
       r_cnt = r_cnt+1
       break if r_cnt == 30
       retry 
     end
   end
  rescue Exception => e
   puts "Failing to parse #{srch}::#{force}::#{e.inspect}::#{e.backtrace}"
   raise e
  end while(true)
end

Mechanize.new().get("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=scrabble_word_lists&query=select+word+from+%60swdata%60&apikey=").save_as("word_list.csv") rescue retry
range = IO.readlines("word_list.csv") + ('a'..'zzzz').to_a
offset = get_metadata("OFFSET",0)
offset = 0 if offset >=range.length

range.each_with_index{|srch,idx|
  next if idx < offset
  srch = srch.strip
  action(srch,0)
  save_metadata("OFFSET",idx.next)
}

