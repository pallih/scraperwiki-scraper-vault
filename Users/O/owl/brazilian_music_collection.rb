require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://bases.fundaj.gov.br/"

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

def delete_metadata(name)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end

def text(str)
  begin
    return (str.nil? or str.text.nil?) ? "" : str.text.strip.gsub(/ |\.|:|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def name(str)
  return (str.nil? or str.text.nil?) ? "" : str.text.strip.gsub(/ |\n|\t|\^\s+|\s+$/,"_").gsub(/\.|:/,"").upcase
end
def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)
  Nokogiri::HTML(data,nil,"ISO-8859-1").xpath("//table[not(@cellspacing)]").each do|tbl|
    tr = tbl.xpath("tr[td[not(@colspan)]]")
    records = {"DOC"=>Time.now.to_s}
    tr.each_with_index{|row,idx|
      begin
        td=row.xpath("td")
        records[name(td[0])]=text(td[1])
      end unless idx==0
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["N_ACESSO"],records,table_name="swdata",verbose=0)
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout=120000
    }
    params = {
      'v3'=>'',
      'v4'=>'1',
      'v5'=>'500000',
      'v1'=>'disco',
      'v2'=>'',
      'v7'=>'termo+exato',
      'v8'=>'qualquer+campo',
      'v9'=>'OU',
      'v12'=>'',
      'v17'=>'termo+exato',
      'v18'=>'qualquer+campo',
      'v19'=>'OU',
      'v22'=>srch,
      'v27'=>'termo+exato',
      'v28'=>'qualquer+campo',
      'v6'=>'Procurar'
    }
    begin
      pg = br.post(BASE_URL+"cgi-bin/isis3g-b.pl",params)
      scrape(pg.body)
    rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
      sleep(30)
      retry
    end
  end
end
#records={"Número"=>"21212"}
#ScraperWiki.save_sqlite(unique_keys=["Número"],records,table_name="swdata",verbose=0)
#exit
#save_metadata("OFFSET",25)
range = ('A'..'Z').to_a #+ (0..9).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)

offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  next if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
end
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://bases.fundaj.gov.br/"

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

def delete_metadata(name)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end

def text(str)
  begin
    return (str.nil? or str.text.nil?) ? "" : str.text.strip.gsub(/ |\.|:|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def name(str)
  return (str.nil? or str.text.nil?) ? "" : str.text.strip.gsub(/ |\n|\t|\^\s+|\s+$/,"_").gsub(/\.|:/,"").upcase
end
def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)
  Nokogiri::HTML(data,nil,"ISO-8859-1").xpath("//table[not(@cellspacing)]").each do|tbl|
    tr = tbl.xpath("tr[td[not(@colspan)]]")
    records = {"DOC"=>Time.now.to_s}
    tr.each_with_index{|row,idx|
      begin
        td=row.xpath("td")
        records[name(td[0])]=text(td[1])
      end unless idx==0
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["N_ACESSO"],records,table_name="swdata",verbose=0)
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout=120000
    }
    params = {
      'v3'=>'',
      'v4'=>'1',
      'v5'=>'500000',
      'v1'=>'disco',
      'v2'=>'',
      'v7'=>'termo+exato',
      'v8'=>'qualquer+campo',
      'v9'=>'OU',
      'v12'=>'',
      'v17'=>'termo+exato',
      'v18'=>'qualquer+campo',
      'v19'=>'OU',
      'v22'=>srch,
      'v27'=>'termo+exato',
      'v28'=>'qualquer+campo',
      'v6'=>'Procurar'
    }
    begin
      pg = br.post(BASE_URL+"cgi-bin/isis3g-b.pl",params)
      scrape(pg.body)
    rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
      sleep(30)
      retry
    end
  end
end
#records={"Número"=>"21212"}
#ScraperWiki.save_sqlite(unique_keys=["Número"],records,table_name="swdata",verbose=0)
#exit
#save_metadata("OFFSET",25)
range = ('A'..'Z').to_a #+ (0..9).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)

offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  next if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
end
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://bases.fundaj.gov.br/"

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

def delete_metadata(name)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end

def text(str)
  begin
    return (str.nil? or str.text.nil?) ? "" : str.text.strip.gsub(/ |\.|:|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def name(str)
  return (str.nil? or str.text.nil?) ? "" : str.text.strip.gsub(/ |\n|\t|\^\s+|\s+$/,"_").gsub(/\.|:/,"").upcase
end
def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)
  Nokogiri::HTML(data,nil,"ISO-8859-1").xpath("//table[not(@cellspacing)]").each do|tbl|
    tr = tbl.xpath("tr[td[not(@colspan)]]")
    records = {"DOC"=>Time.now.to_s}
    tr.each_with_index{|row,idx|
      begin
        td=row.xpath("td")
        records[name(td[0])]=text(td[1])
      end unless idx==0
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["N_ACESSO"],records,table_name="swdata",verbose=0)
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout=120000
    }
    params = {
      'v3'=>'',
      'v4'=>'1',
      'v5'=>'500000',
      'v1'=>'disco',
      'v2'=>'',
      'v7'=>'termo+exato',
      'v8'=>'qualquer+campo',
      'v9'=>'OU',
      'v12'=>'',
      'v17'=>'termo+exato',
      'v18'=>'qualquer+campo',
      'v19'=>'OU',
      'v22'=>srch,
      'v27'=>'termo+exato',
      'v28'=>'qualquer+campo',
      'v6'=>'Procurar'
    }
    begin
      pg = br.post(BASE_URL+"cgi-bin/isis3g-b.pl",params)
      scrape(pg.body)
    rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
      sleep(30)
      retry
    end
  end
end
#records={"Número"=>"21212"}
#ScraperWiki.save_sqlite(unique_keys=["Número"],records,table_name="swdata",verbose=0)
#exit
#save_metadata("OFFSET",25)
range = ('A'..'Z').to_a #+ (0..9).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)

offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  next if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
end
require 'nokogiri'
require 'mechanize'
require 'pp'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://bases.fundaj.gov.br/"

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

def delete_metadata(name)
  begin
    ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
  rescue Exception => e
    puts "ERROR: #{e.inspect} during delete_metadata(#{key})"
  end
end

def text(str)
  begin
    return (str.nil? or str.text.nil?) ? "" : str.text.strip.gsub(/ |\.|:|\n|\t|^\s+|\s+$/,"")
  rescue Exception => e
    return str.text unless str.nil? 
    puts e.backtrace
  end
end

def name(str)
  return (str.nil? or str.text.nil?) ? "" : str.text.strip.gsub(/ |\n|\t|\^\s+|\s+$/,"_").gsub(/\.|:/,"").upcase
end
def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end

def scrape(data)
  Nokogiri::HTML(data,nil,"ISO-8859-1").xpath("//table[not(@cellspacing)]").each do|tbl|
    tr = tbl.xpath("tr[td[not(@colspan)]]")
    records = {"DOC"=>Time.now.to_s}
    tr.each_with_index{|row,idx|
      begin
        td=row.xpath("td")
        records[name(td[0])]=text(td[1])
      end unless idx==0
    }
    #puts records.inspect
    ScraperWiki.save_sqlite(unique_keys=["N_ACESSO"],records,table_name="swdata",verbose=0)
  end
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout=120000
    }
    params = {
      'v3'=>'',
      'v4'=>'1',
      'v5'=>'500000',
      'v1'=>'disco',
      'v2'=>'',
      'v7'=>'termo+exato',
      'v8'=>'qualquer+campo',
      'v9'=>'OU',
      'v12'=>'',
      'v17'=>'termo+exato',
      'v18'=>'qualquer+campo',
      'v19'=>'OU',
      'v22'=>srch,
      'v27'=>'termo+exato',
      'v28'=>'qualquer+campo',
      'v6'=>'Procurar'
    }
    begin
      pg = br.post(BASE_URL+"cgi-bin/isis3g-b.pl",params)
      scrape(pg.body)
    rescue Exception => e
      puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
      sleep(30)
      retry
    end
  end
end
#records={"Número"=>"21212"}
#ScraperWiki.save_sqlite(unique_keys=["Número"],records,table_name="swdata",verbose=0)
#exit
#save_metadata("OFFSET",25)
range = ('A'..'Z').to_a #+ (0..9).to_a + ['$','@','#','(','"','-','\'','.']
offset = get_metadata("OFFSET",0)

offset = 0 if offset >= range.length

range.each_with_index do|srch,index|
  next if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)
end
