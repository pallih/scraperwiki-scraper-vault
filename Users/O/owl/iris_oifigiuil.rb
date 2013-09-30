# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    raise e unless e.inspect =~ /no such table/i    
  end
end
def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   raise e unless e.inspect =~ /no such table/i
  end
end
def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   raise e unless e.inspect =~ /no such table/i
  end
end


def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip unless st.text.nil? or st.text.empty?}
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

def exists(lnk)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where link=?",[lnk])['data'].flatten.first rescue 0
end

def scrape(data,rec)
  paras = Nokogiri::HTML(data).xpath(".//p")
  records = []
  r = nil
  paras.each{|para|
    txt = text(para.xpath("."))
    if txt =~ /(\[\d*\w*\])/
      txt_a = txt.gsub(/\n/,'').scan(/(.*)(\[\d*\w*\])/)[0]
      if txt_a.kind_of?(Array)
        r["section"]= (r['section'].nil?)? txt_a[0..-2].join("\n"):r['section']+"\n"+txt_a[0..-2].join("\n") unless r.nil? or txt_a.first.empty? 
      end
      r['notice_id']= txt_a.length==1 ? txt_a.first.to_s.gsub(/\[|\]/,"") : txt_a.last.to_s.gsub(/\[|\]/,"") unless r.nil? 
      r["doc"] = Time.now unless r.nil? 
      records << r.merge(rec) unless r.nil? 
      r = nil
    elsif txt == "————" or txt=~ /^Number [0-9]*/ or txt =~ /^Published by Authority/ or txt.match(/^IRIS OIFIGIÚIL/) or txt.match(/^This publication is registered for transmission by Inland Post as a newspaper/)
      #ignore
    else
      if r.nil? 
        r = {"section"=>txt} 
      else
        r["section"]=(r['section'].nil?)? txt:r['section']+"\n"+txt
      end
    end

  }
  #puts records.inspect
  #puts data.inspect
  ScraperWiki.save_sqlite(unique_keys=['edition','issue_id','notice_id'],records,table_name='swdata',verbose=2) unless records.length==0
end

#ScraperWiki.sqliteexecute("update swdata set doc = ?",[Time.now])
#ScraperWiki.commit()

#save_metadata("list",914)
ScraperWiki::attach("ie_official_notices_pdf_urls","ie")
list = ScraperWiki.sqliteexecute("select edition,issue_number,url from ie.swdata")['data']
start = get_metadata("list",0)
list[start..-1].each{|ele|
  begin
    rec = {"edition"=>ele[0],"issue_id"=>ele[1],"link"=>ele[2]}
    puts ["list",start,list.length,rec].inspect
  
    Mechanize.new.get(ele[2]).save_as("#{ele[0]}_#{ele[1]}.pdf")
    tmp = %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar  ExtractText -html -console "#{ele[0]}_#{ele[1]}.pdf"]
    scrape(tmp,rec)
  end if exists(ele[2]) == 0
  start = start + 1
  save_metadata("list",start)
}
delete_metadata("list")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    raise e unless e.inspect =~ /no such table/i    
  end
end
def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   raise e unless e.inspect =~ /no such table/i
  end
end
def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   raise e unless e.inspect =~ /no such table/i
  end
end


def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip unless st.text.nil? or st.text.empty?}
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

def exists(lnk)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where link=?",[lnk])['data'].flatten.first rescue 0
end

def scrape(data,rec)
  paras = Nokogiri::HTML(data).xpath(".//p")
  records = []
  r = nil
  paras.each{|para|
    txt = text(para.xpath("."))
    if txt =~ /(\[\d*\w*\])/
      txt_a = txt.gsub(/\n/,'').scan(/(.*)(\[\d*\w*\])/)[0]
      if txt_a.kind_of?(Array)
        r["section"]= (r['section'].nil?)? txt_a[0..-2].join("\n"):r['section']+"\n"+txt_a[0..-2].join("\n") unless r.nil? or txt_a.first.empty? 
      end
      r['notice_id']= txt_a.length==1 ? txt_a.first.to_s.gsub(/\[|\]/,"") : txt_a.last.to_s.gsub(/\[|\]/,"") unless r.nil? 
      r["doc"] = Time.now unless r.nil? 
      records << r.merge(rec) unless r.nil? 
      r = nil
    elsif txt == "————" or txt=~ /^Number [0-9]*/ or txt =~ /^Published by Authority/ or txt.match(/^IRIS OIFIGIÚIL/) or txt.match(/^This publication is registered for transmission by Inland Post as a newspaper/)
      #ignore
    else
      if r.nil? 
        r = {"section"=>txt} 
      else
        r["section"]=(r['section'].nil?)? txt:r['section']+"\n"+txt
      end
    end

  }
  #puts records.inspect
  #puts data.inspect
  ScraperWiki.save_sqlite(unique_keys=['edition','issue_id','notice_id'],records,table_name='swdata',verbose=2) unless records.length==0
end

#ScraperWiki.sqliteexecute("update swdata set doc = ?",[Time.now])
#ScraperWiki.commit()

#save_metadata("list",914)
ScraperWiki::attach("ie_official_notices_pdf_urls","ie")
list = ScraperWiki.sqliteexecute("select edition,issue_number,url from ie.swdata")['data']
start = get_metadata("list",0)
list[start..-1].each{|ele|
  begin
    rec = {"edition"=>ele[0],"issue_id"=>ele[1],"link"=>ele[2]}
    puts ["list",start,list.length,rec].inspect
  
    Mechanize.new.get(ele[2]).save_as("#{ele[0]}_#{ele[1]}.pdf")
    tmp = %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar  ExtractText -html -console "#{ele[0]}_#{ele[1]}.pdf"]
    scrape(tmp,rec)
  end if exists(ele[2]) == 0
  start = start + 1
  save_metadata("list",start)
}
delete_metadata("list")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    raise e unless e.inspect =~ /no such table/i    
  end
end
def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   raise e unless e.inspect =~ /no such table/i
  end
end
def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   raise e unless e.inspect =~ /no such table/i
  end
end


def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip unless st.text.nil? or st.text.empty?}
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

def exists(lnk)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where link=?",[lnk])['data'].flatten.first rescue 0
end

def scrape(data,rec)
  paras = Nokogiri::HTML(data).xpath(".//p")
  records = []
  r = nil
  paras.each{|para|
    txt = text(para.xpath("."))
    if txt =~ /(\[\d*\w*\])/
      txt_a = txt.gsub(/\n/,'').scan(/(.*)(\[\d*\w*\])/)[0]
      if txt_a.kind_of?(Array)
        r["section"]= (r['section'].nil?)? txt_a[0..-2].join("\n"):r['section']+"\n"+txt_a[0..-2].join("\n") unless r.nil? or txt_a.first.empty? 
      end
      r['notice_id']= txt_a.length==1 ? txt_a.first.to_s.gsub(/\[|\]/,"") : txt_a.last.to_s.gsub(/\[|\]/,"") unless r.nil? 
      r["doc"] = Time.now unless r.nil? 
      records << r.merge(rec) unless r.nil? 
      r = nil
    elsif txt == "————" or txt=~ /^Number [0-9]*/ or txt =~ /^Published by Authority/ or txt.match(/^IRIS OIFIGIÚIL/) or txt.match(/^This publication is registered for transmission by Inland Post as a newspaper/)
      #ignore
    else
      if r.nil? 
        r = {"section"=>txt} 
      else
        r["section"]=(r['section'].nil?)? txt:r['section']+"\n"+txt
      end
    end

  }
  #puts records.inspect
  #puts data.inspect
  ScraperWiki.save_sqlite(unique_keys=['edition','issue_id','notice_id'],records,table_name='swdata',verbose=2) unless records.length==0
end

#ScraperWiki.sqliteexecute("update swdata set doc = ?",[Time.now])
#ScraperWiki.commit()

#save_metadata("list",914)
ScraperWiki::attach("ie_official_notices_pdf_urls","ie")
list = ScraperWiki.sqliteexecute("select edition,issue_number,url from ie.swdata")['data']
start = get_metadata("list",0)
list[start..-1].each{|ele|
  begin
    rec = {"edition"=>ele[0],"issue_id"=>ele[1],"link"=>ele[2]}
    puts ["list",start,list.length,rec].inspect
  
    Mechanize.new.get(ele[2]).save_as("#{ele[0]}_#{ele[1]}.pdf")
    tmp = %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar  ExtractText -html -console "#{ele[0]}_#{ele[1]}.pdf"]
    scrape(tmp,rec)
  end if exists(ele[2]) == 0
  start = start + 1
  save_metadata("list",start)
}
delete_metadata("list")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'

Mechanize.html_parser = Nokogiri::HTML

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    raise e unless e.inspect =~ /no such table/i    
  end
end
def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   raise e unless e.inspect =~ /no such table/i
  end
end
def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   raise e unless e.inspect =~ /no such table/i
  end
end


def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? 
    if str.children().length == 1
      return str.text.strip
    else
      tmp = []
      str.children().collect{|st| tmp << st.text.strip unless st.text.nil? or st.text.empty?}
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

def exists(lnk)
  return ScraperWiki.sqliteexecute("select count(*) from swdata where link=?",[lnk])['data'].flatten.first rescue 0
end

def scrape(data,rec)
  paras = Nokogiri::HTML(data).xpath(".//p")
  records = []
  r = nil
  paras.each{|para|
    txt = text(para.xpath("."))
    if txt =~ /(\[\d*\w*\])/
      txt_a = txt.gsub(/\n/,'').scan(/(.*)(\[\d*\w*\])/)[0]
      if txt_a.kind_of?(Array)
        r["section"]= (r['section'].nil?)? txt_a[0..-2].join("\n"):r['section']+"\n"+txt_a[0..-2].join("\n") unless r.nil? or txt_a.first.empty? 
      end
      r['notice_id']= txt_a.length==1 ? txt_a.first.to_s.gsub(/\[|\]/,"") : txt_a.last.to_s.gsub(/\[|\]/,"") unless r.nil? 
      r["doc"] = Time.now unless r.nil? 
      records << r.merge(rec) unless r.nil? 
      r = nil
    elsif txt == "————" or txt=~ /^Number [0-9]*/ or txt =~ /^Published by Authority/ or txt.match(/^IRIS OIFIGIÚIL/) or txt.match(/^This publication is registered for transmission by Inland Post as a newspaper/)
      #ignore
    else
      if r.nil? 
        r = {"section"=>txt} 
      else
        r["section"]=(r['section'].nil?)? txt:r['section']+"\n"+txt
      end
    end

  }
  #puts records.inspect
  #puts data.inspect
  ScraperWiki.save_sqlite(unique_keys=['edition','issue_id','notice_id'],records,table_name='swdata',verbose=2) unless records.length==0
end

#ScraperWiki.sqliteexecute("update swdata set doc = ?",[Time.now])
#ScraperWiki.commit()

#save_metadata("list",914)
ScraperWiki::attach("ie_official_notices_pdf_urls","ie")
list = ScraperWiki.sqliteexecute("select edition,issue_number,url from ie.swdata")['data']
start = get_metadata("list",0)
list[start..-1].each{|ele|
  begin
    rec = {"edition"=>ele[0],"issue_id"=>ele[1],"link"=>ele[2]}
    puts ["list",start,list.length,rec].inspect
  
    Mechanize.new.get(ele[2]).save_as("#{ele[0]}_#{ele[1]}.pdf")
    tmp = %x[java -Xms256m -Xmx1024m -jar /usr/share/java/pdfbox-app-1.7.0.jar  ExtractText -html -console "#{ele[0]}_#{ele[1]}.pdf"]
    scrape(tmp,rec)
  end if exists(ele[2]) == 0
  start = start + 1
  save_metadata("list",start)
}
delete_metadata("list")
