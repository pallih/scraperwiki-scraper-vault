# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'logger'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://sdatcert3.resiusa.org/UCC-Charter/"

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

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else str.children().length > 1
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
  Nokogiri::HTML(data).xpath(".//table[@id='Results']/tr[position()>1]").each{|tr|
    break if tr.inner_html =~ /No Information available/
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER" => text(td[0].xpath(".")).gsub(/\(|\)/,""),
      "COMPANY_NAME" => text(td[1].xpath(".")),
      "URL" => BASE_URL+attributes(td[2].xpath("a"),"href"),
      "STATUS" => text(td[5].xpath(".")),
      "DOC" => Time.now
    }
    records << r  if r['COMPANY_NUMBER'].match(/^L/).nil? and r['COMPANY_NUMBER'].match(/^T/).nil? unless r['STATUS']=='OLD NAME'
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
    }
    pg = br.get(BASE_URL+"CharterSearch_f.aspx")
    params = {'VisibleEntityName'=>srch,'search2'=>'Search','EntityName'=>''}
    pg.form_with(:action=>'searchByName_a.aspx?mode=name') do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
    end
    re = scrape(pg.body)
    cnt = Nokogiri::HTML(pg.body).xpath(".//select[@name='SelectedPage']/option").length
    (cnt-1).times{|cn|
      params = {'__EVENTTARGET'=>'SelectedPage','SelectedPage'=>cn+2}
      pg.form_with(:name=>'Form1') do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      scrape(pg.body)
      save_metadata("PGNO",cn+2)
    }
    delete_metadata("PGNO") unless cnt>=1
  end
end


#save_metadata("OFFSET",0)
offset = get_metadata("OFFSET",0)
range = ('A'..'ZZZ').to_a.sort + (0..100).to_a
offset = 0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx<offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'logger'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://sdatcert3.resiusa.org/UCC-Charter/"

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

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else str.children().length > 1
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
  Nokogiri::HTML(data).xpath(".//table[@id='Results']/tr[position()>1]").each{|tr|
    break if tr.inner_html =~ /No Information available/
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER" => text(td[0].xpath(".")).gsub(/\(|\)/,""),
      "COMPANY_NAME" => text(td[1].xpath(".")),
      "URL" => BASE_URL+attributes(td[2].xpath("a"),"href"),
      "STATUS" => text(td[5].xpath(".")),
      "DOC" => Time.now
    }
    records << r  if r['COMPANY_NUMBER'].match(/^L/).nil? and r['COMPANY_NUMBER'].match(/^T/).nil? unless r['STATUS']=='OLD NAME'
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
    }
    pg = br.get(BASE_URL+"CharterSearch_f.aspx")
    params = {'VisibleEntityName'=>srch,'search2'=>'Search','EntityName'=>''}
    pg.form_with(:action=>'searchByName_a.aspx?mode=name') do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
    end
    re = scrape(pg.body)
    cnt = Nokogiri::HTML(pg.body).xpath(".//select[@name='SelectedPage']/option").length
    (cnt-1).times{|cn|
      params = {'__EVENTTARGET'=>'SelectedPage','SelectedPage'=>cn+2}
      pg.form_with(:name=>'Form1') do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      scrape(pg.body)
      save_metadata("PGNO",cn+2)
    }
    delete_metadata("PGNO") unless cnt>=1
  end
end


#save_metadata("OFFSET",0)
offset = get_metadata("OFFSET",0)
range = ('A'..'ZZZ').to_a.sort + (0..100).to_a
offset = 0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx<offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'logger'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://sdatcert3.resiusa.org/UCC-Charter/"

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

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else str.children().length > 1
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
  Nokogiri::HTML(data).xpath(".//table[@id='Results']/tr[position()>1]").each{|tr|
    break if tr.inner_html =~ /No Information available/
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER" => text(td[0].xpath(".")).gsub(/\(|\)/,""),
      "COMPANY_NAME" => text(td[1].xpath(".")),
      "URL" => BASE_URL+attributes(td[2].xpath("a"),"href"),
      "STATUS" => text(td[5].xpath(".")),
      "DOC" => Time.now
    }
    records << r  if r['COMPANY_NUMBER'].match(/^L/).nil? and r['COMPANY_NUMBER'].match(/^T/).nil? unless r['STATUS']=='OLD NAME'
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
    }
    pg = br.get(BASE_URL+"CharterSearch_f.aspx")
    params = {'VisibleEntityName'=>srch,'search2'=>'Search','EntityName'=>''}
    pg.form_with(:action=>'searchByName_a.aspx?mode=name') do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
    end
    re = scrape(pg.body)
    cnt = Nokogiri::HTML(pg.body).xpath(".//select[@name='SelectedPage']/option").length
    (cnt-1).times{|cn|
      params = {'__EVENTTARGET'=>'SelectedPage','SelectedPage'=>cn+2}
      pg.form_with(:name=>'Form1') do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      scrape(pg.body)
      save_metadata("PGNO",cn+2)
    }
    delete_metadata("PGNO") unless cnt>=1
  end
end


#save_metadata("OFFSET",0)
offset = get_metadata("OFFSET",0)
range = ('A'..'ZZZ').to_a.sort + (0..100).to_a
offset = 0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx<offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}

# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'
require 'logger'
require 'open-uri'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://sdatcert3.resiusa.org/UCC-Charter/"

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

def delete_metadata(key)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[key])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
   retry
  end
end

def text(str)
  begin
    return "" if str.nil? or str.text.nil? or str.text.empty? or str.children().length == 0
    if str.children().length == 1
      return str.text.strip
    else str.children().length > 1
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
  Nokogiri::HTML(data).xpath(".//table[@id='Results']/tr[position()>1]").each{|tr|
    break if tr.inner_html =~ /No Information available/
    td = tr.xpath("td")
    r = {
      "COMPANY_NUMBER" => text(td[0].xpath(".")).gsub(/\(|\)/,""),
      "COMPANY_NAME" => text(td[1].xpath(".")),
      "URL" => BASE_URL+attributes(td[2].xpath("a"),"href"),
      "STATUS" => text(td[5].xpath(".")),
      "DOC" => Time.now
    }
    records << r  if r['COMPANY_NUMBER'].match(/^L/).nil? and r['COMPANY_NUMBER'].match(/^T/).nil? unless r['STATUS']=='OLD NAME'
  }
  ScraperWiki.save_sqlite(unique_keys=['COMPANY_NUMBER'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
      b.max_history=0
    }
    pg = br.get(BASE_URL+"CharterSearch_f.aspx")
    params = {'VisibleEntityName'=>srch,'search2'=>'Search','EntityName'=>''}
    pg.form_with(:action=>'searchByName_a.aspx?mode=name') do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
    end
    re = scrape(pg.body)
    cnt = Nokogiri::HTML(pg.body).xpath(".//select[@name='SelectedPage']/option").length
    (cnt-1).times{|cn|
      params = {'__EVENTTARGET'=>'SelectedPage','SelectedPage'=>cn+2}
      pg.form_with(:name=>'Form1') do|f|
        params.each{|k,v| f[k]=v}
        pg = f.submit
      end
      scrape(pg.body)
      save_metadata("PGNO",cn+2)
    }
    delete_metadata("PGNO") unless cnt>=1
  end
end


#save_metadata("OFFSET",0)
offset = get_metadata("OFFSET",0)
range = ('A'..'ZZZ').to_a.sort + (0..100).to_a
offset = 0 if offset>=range.length
range.each_with_index{|srch,idx|
  next if idx<offset
  action(srch)
  save_metadata("OFFSET",idx.next)
}

