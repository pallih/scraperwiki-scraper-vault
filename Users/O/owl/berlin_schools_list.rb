# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"

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

def text(str)
  begin
    if str.length < 1
      return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
    else
      tmp = ""
      str.collect{|st| st.text.strip}.join(";")
    end
  rescue Exception => es
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "list"
    holder = []
    Nokogiri::HTML(data).xpath(".//*[@id='GridViewSchulen']/tr[position()>1]").each{|tr|
      r = {
        "ID"=>text(tr.xpath("td/a")),
        "URL"=>attributes(tr.xpath("td/a"),"href")
      }
      holder << r 
    }
    #ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
    return holder
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//*[@id='divAllgemein']")
    records = {'URL'=>s_url,'DOC'=>Time.now.to_s}
    begin
      tmp_str = text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblSchulname']")).split('-')
      records['SCHOOL_NAME'],records['ID']=tmp_str[0..tmp_str.length-2].join("-"),tmp_str.last.strip
      records['TYPE']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblSchulart']"))
      records['ADDR']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblStrasse']"))+","+text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblOrt']"))
      records['TEL']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblTelefon']"))
      records['FAX']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblFax']"))
      records['EMAIL']=text(doc.xpath("a[@id='ctl00_ContentPlaceHolderMenuListe_HLinkEMail']"))
      records['WEB']=text(doc.xpath("a[@id='ctl00_ContentPlaceHolderMenuListe_HLinkWeb']"))
      records['LEITUNG']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblLeitung']"))
      records['STUDENTS']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblSchueler']"))
      records['CRITERIA']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAufnKrit']/span[preceding::input[1][@checked]]"))
      records['LANGUAGES']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlSprachen']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblSprachen']"))
      records['ANGEBOTE']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAngebote']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblAngebote']"))
      records['GANZTAGSBETRIEB']= text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlGanztags']/following::input[@checked]/following::span[1]"))
      records['AUSSTATTUNG']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAusstattung']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblAusstattung']"))
      records['COMMUNITIES']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAGs']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblAGs']"))
      records['KOOPERATIONEN']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlKoop']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblKoop']")).gsub(/in Kooperation mit /,"")
      records['PARTNERS']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlPartner']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblPartner']"))
      records['DIFFERENTIATION']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlDiff']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblDiff']"))
      records['MITTAGESSEN']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlMittag']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblMittag']"))
      records['DUALES']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlDualesLernen']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblDualesLernen']"))
    end
    ScraperWiki.save_sqlite(unique_keys=['ID'],records,table_name='swdata',verbose=2) unless records['ID'].nil? or records['ID'].empty? 
    #puts records.inspect
  end
end

def exists(id)
  begin
    #puts [id,ScraperWiki.sqliteexecute("select count(*) from swdata where trim(id)=?",[id]).inspect].inspect
    return ScraperWiki.sqliteexecute("select count(*) from swdata where trim(id)=?",[id])['data'][0][0]
  rescue Exception => e
    puts "ERROR: While processing exists(#{id}) :: #{e.inspect} :: #{e.backtrace}"
    return 0
  end
end

def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "SchulListe.aspx"
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    #puts lst.inspect
    lst.each{|r|
      begin
        pg_tmp = br.get(BASE_URL+r['URL'])
        scrape(pg_tmp.body,"details",BASE_URL+r['URL'])
        #break
      rescue Exception => e
        puts "ERROR: While processing #{p_url}:: #{e.inspect} :: #{e.backtrace}"
        #retry if e.inspect =~ /Timeout|TIME|HTTP/
      end if exists(r['ID'])==0
    }
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
    #sleep(30)
    #retry if e.inspect =~ /Timeout|TIME|HTTP/
  end
end

#def action(s_url)
#  scrape(Mechanize.new.get(s_url).body,"details",s_url)  
#end
#action("https://good-practice.bibb.de/adb/suche.php?action=view&id=3314")
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"

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

def text(str)
  begin
    if str.length < 1
      return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
    else
      tmp = ""
      str.collect{|st| st.text.strip}.join(";")
    end
  rescue Exception => es
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "list"
    holder = []
    Nokogiri::HTML(data).xpath(".//*[@id='GridViewSchulen']/tr[position()>1]").each{|tr|
      r = {
        "ID"=>text(tr.xpath("td/a")),
        "URL"=>attributes(tr.xpath("td/a"),"href")
      }
      holder << r 
    }
    #ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
    return holder
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//*[@id='divAllgemein']")
    records = {'URL'=>s_url,'DOC'=>Time.now.to_s}
    begin
      tmp_str = text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblSchulname']")).split('-')
      records['SCHOOL_NAME'],records['ID']=tmp_str[0..tmp_str.length-2].join("-"),tmp_str.last.strip
      records['TYPE']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblSchulart']"))
      records['ADDR']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblStrasse']"))+","+text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblOrt']"))
      records['TEL']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblTelefon']"))
      records['FAX']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblFax']"))
      records['EMAIL']=text(doc.xpath("a[@id='ctl00_ContentPlaceHolderMenuListe_HLinkEMail']"))
      records['WEB']=text(doc.xpath("a[@id='ctl00_ContentPlaceHolderMenuListe_HLinkWeb']"))
      records['LEITUNG']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblLeitung']"))
      records['STUDENTS']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblSchueler']"))
      records['CRITERIA']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAufnKrit']/span[preceding::input[1][@checked]]"))
      records['LANGUAGES']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlSprachen']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblSprachen']"))
      records['ANGEBOTE']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAngebote']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblAngebote']"))
      records['GANZTAGSBETRIEB']= text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlGanztags']/following::input[@checked]/following::span[1]"))
      records['AUSSTATTUNG']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAusstattung']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblAusstattung']"))
      records['COMMUNITIES']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAGs']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblAGs']"))
      records['KOOPERATIONEN']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlKoop']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblKoop']")).gsub(/in Kooperation mit /,"")
      records['PARTNERS']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlPartner']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblPartner']"))
      records['DIFFERENTIATION']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlDiff']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblDiff']"))
      records['MITTAGESSEN']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlMittag']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblMittag']"))
      records['DUALES']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlDualesLernen']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblDualesLernen']"))
    end
    ScraperWiki.save_sqlite(unique_keys=['ID'],records,table_name='swdata',verbose=2) unless records['ID'].nil? or records['ID'].empty? 
    #puts records.inspect
  end
end

def exists(id)
  begin
    #puts [id,ScraperWiki.sqliteexecute("select count(*) from swdata where trim(id)=?",[id]).inspect].inspect
    return ScraperWiki.sqliteexecute("select count(*) from swdata where trim(id)=?",[id])['data'][0][0]
  rescue Exception => e
    puts "ERROR: While processing exists(#{id}) :: #{e.inspect} :: #{e.backtrace}"
    return 0
  end
end

def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "SchulListe.aspx"
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    #puts lst.inspect
    lst.each{|r|
      begin
        pg_tmp = br.get(BASE_URL+r['URL'])
        scrape(pg_tmp.body,"details",BASE_URL+r['URL'])
        #break
      rescue Exception => e
        puts "ERROR: While processing #{p_url}:: #{e.inspect} :: #{e.backtrace}"
        #retry if e.inspect =~ /Timeout|TIME|HTTP/
      end if exists(r['ID'])==0
    }
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
    #sleep(30)
    #retry if e.inspect =~ /Timeout|TIME|HTTP/
  end
end

#def action(s_url)
#  scrape(Mechanize.new.get(s_url).body,"details",s_url)  
#end
#action("https://good-practice.bibb.de/adb/suche.php?action=view&id=3314")
action()# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.berlin.de/sen/bildung/schulverzeichnis_und_portraets/anwendung/"

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

def text(str)
  begin
    if str.length < 1
      return (str.nil? or str.text.nil?) ? "" : str.text.strip#str.text.gsub(/\n|\t|^\s+|\s+$/,"")
    else
      tmp = ""
      str.collect{|st| st.text.strip}.join(";")
    end
  rescue Exception => es
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data,act,s_url)
  if act == "list"
    holder = []
    Nokogiri::HTML(data).xpath(".//*[@id='GridViewSchulen']/tr[position()>1]").each{|tr|
      r = {
        "ID"=>text(tr.xpath("td/a")),
        "URL"=>attributes(tr.xpath("td/a"),"href")
      }
      holder << r 
    }
    #ScraperWiki.save_sqlite(unique_keys=['NAME'],records,table_name='swdata',verbose=2) unless records.length == 0
    return holder
  elsif act == "details"
    doc = Nokogiri::HTML(data).xpath(".//*[@id='divAllgemein']")
    records = {'URL'=>s_url,'DOC'=>Time.now.to_s}
    begin
      tmp_str = text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblSchulname']")).split('-')
      records['SCHOOL_NAME'],records['ID']=tmp_str[0..tmp_str.length-2].join("-"),tmp_str.last.strip
      records['TYPE']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblSchulart']"))
      records['ADDR']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblStrasse']"))+","+text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblOrt']"))
      records['TEL']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblTelefon']"))
      records['FAX']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblFax']"))
      records['EMAIL']=text(doc.xpath("a[@id='ctl00_ContentPlaceHolderMenuListe_HLinkEMail']"))
      records['WEB']=text(doc.xpath("a[@id='ctl00_ContentPlaceHolderMenuListe_HLinkWeb']"))
      records['LEITUNG']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblLeitung']"))
      records['STUDENTS']=text(doc.xpath("span[@id='ctl00_ContentPlaceHolderMenuListe_lblSchueler']"))
      records['CRITERIA']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAufnKrit']/span[preceding::input[1][@checked]]"))
      records['LANGUAGES']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlSprachen']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblSprachen']"))
      records['ANGEBOTE']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAngebote']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblAngebote']"))
      records['GANZTAGSBETRIEB']= text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlGanztags']/following::input[@checked]/following::span[1]"))
      records['AUSSTATTUNG']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAusstattung']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblAusstattung']"))
      records['COMMUNITIES']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlAGs']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblAGs']"))
      records['KOOPERATIONEN']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlKoop']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblKoop']")).gsub(/in Kooperation mit /,"")
      records['PARTNERS']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlPartner']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblPartner']"))
      records['DIFFERENTIATION']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlDiff']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblDiff']"))
      records['MITTAGESSEN']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlMittag']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblMittag']"))
      records['DUALES']=text(doc.xpath("div[@id='ctl00_ContentPlaceHolderMenuListe_pnlDualesLernen']/span[@id='ctl00_ContentPlaceHolderMenuListe_lblDualesLernen']"))
    end
    ScraperWiki.save_sqlite(unique_keys=['ID'],records,table_name='swdata',verbose=2) unless records['ID'].nil? or records['ID'].empty? 
    #puts records.inspect
  end
end

def exists(id)
  begin
    #puts [id,ScraperWiki.sqliteexecute("select count(*) from swdata where trim(id)=?",[id]).inspect].inspect
    return ScraperWiki.sqliteexecute("select count(*) from swdata where trim(id)=?",[id])['data'][0][0]
  rescue Exception => e
    puts "ERROR: While processing exists(#{id}) :: #{e.inspect} :: #{e.backtrace}"
    return 0
  end
end

def action()
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    s_url = BASE_URL + "SchulListe.aspx"
    pg = br.get(s_url)
    lst = scrape(pg.body,"list",nil)
    #puts lst.inspect
    lst.each{|r|
      begin
        pg_tmp = br.get(BASE_URL+r['URL'])
        scrape(pg_tmp.body,"details",BASE_URL+r['URL'])
        #break
      rescue Exception => e
        puts "ERROR: While processing #{p_url}:: #{e.inspect} :: #{e.backtrace}"
        #retry if e.inspect =~ /Timeout|TIME|HTTP/
      end if exists(r['ID'])==0
    }
  rescue Exception => e
    puts "ERROR: While processing :: #{e.inspect} :: #{e.backtrace}"
    #sleep(30)
    #retry if e.inspect =~ /Timeout|TIME|HTTP/
  end
end

#def action(s_url)
#  scrape(Mechanize.new.get(s_url).body,"details",s_url)  
#end
#action("https://good-practice.bibb.de/adb/suche.php?action=view&id=3314")
action()