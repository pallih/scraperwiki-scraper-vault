# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.economicstimulusplan.gov.au"

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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::XML(data).xpath(".//results/result").each{|results|
    result = results.xpath(".")
    puts result.inner_html
    r={
      'PROJECT_ID'=>text(result[0].xpath("Project_ID/text()")),
      'TITLE'=>text(result[0].xpath("Title/text()")),
      'PROJECT_TYPE'=>text(result[0].xpath("Snapshot/text()")),
      'SNAPSHOT'=>text(result[0].xpath("Project_ID/text()")),
      'AGENCY'=>text(result[0].xpath("Agency/text()")),
      'STATUS'=>text(result[0].xpath("Status/text()")),
      'SUB_OR_TOWN'=>text(result[0].xpath("Suburb_Or_Town/text()")),
      'STATE'=>text(result[0].xpath("State/text()")),
      'POSTCODE'=>text(result[0].xpath("Postcode/text()")),
      'LAT'=>text(result[0].xpath("GIS_Loc_Latitude/text()")),
      'LONG'=>text(result[0].xpath("GIS_Loc_Longitude/text()")),
      'FUNDING'=>text(result[0].xpath("Approved_Funding/text()")),
      'PROJECTS'=>text(result[0].xpath("Projects/text()")),
    }
    records << r
  }
  ScraperWiki.save_sqlite(unique_keys=['PROJECT_ID'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    pg = br.get(BASE_URL+"/data/GetElectorateResultSet.aspx?electoratename=#{srch}&responsetype=xml")
    scrape(pg.body)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/i
    exit if e.inspect =~ /interrupt/i  
  end
end


range =  ['Aston','Ballarat','Batman','Bendigo','Bruce','Calwell','Casey','Chisholm','Corangamite','Corio','Deakin','Dunkley','Flinders','Gellibrand','Gippsland','Goldstein','Gorton','Higgins','Holt','Hotham','Indi','Isaacs','Jagajaga','Kooyong','Lalor','LaTrobe','Mallee','Maribyrnong','McEwen','McMillan','Melbourne','MelbournePorts','Menzies','Murray','Scullin','Wannon','Wills']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next  if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)

end# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.economicstimulusplan.gov.au"

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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::XML(data).xpath(".//results/result").each{|results|
    result = results.xpath(".")
    puts result.inner_html
    r={
      'PROJECT_ID'=>text(result[0].xpath("Project_ID/text()")),
      'TITLE'=>text(result[0].xpath("Title/text()")),
      'PROJECT_TYPE'=>text(result[0].xpath("Snapshot/text()")),
      'SNAPSHOT'=>text(result[0].xpath("Project_ID/text()")),
      'AGENCY'=>text(result[0].xpath("Agency/text()")),
      'STATUS'=>text(result[0].xpath("Status/text()")),
      'SUB_OR_TOWN'=>text(result[0].xpath("Suburb_Or_Town/text()")),
      'STATE'=>text(result[0].xpath("State/text()")),
      'POSTCODE'=>text(result[0].xpath("Postcode/text()")),
      'LAT'=>text(result[0].xpath("GIS_Loc_Latitude/text()")),
      'LONG'=>text(result[0].xpath("GIS_Loc_Longitude/text()")),
      'FUNDING'=>text(result[0].xpath("Approved_Funding/text()")),
      'PROJECTS'=>text(result[0].xpath("Projects/text()")),
    }
    records << r
  }
  ScraperWiki.save_sqlite(unique_keys=['PROJECT_ID'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    pg = br.get(BASE_URL+"/data/GetElectorateResultSet.aspx?electoratename=#{srch}&responsetype=xml")
    scrape(pg.body)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/i
    exit if e.inspect =~ /interrupt/i  
  end
end


range =  ['Aston','Ballarat','Batman','Bendigo','Bruce','Calwell','Casey','Chisholm','Corangamite','Corio','Deakin','Dunkley','Flinders','Gellibrand','Gippsland','Goldstein','Gorton','Higgins','Holt','Hotham','Indi','Isaacs','Jagajaga','Kooyong','Lalor','LaTrobe','Mallee','Maribyrnong','McEwen','McMillan','Melbourne','MelbournePorts','Menzies','Murray','Scullin','Wannon','Wills']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next  if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)

end# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.economicstimulusplan.gov.au"

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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::XML(data).xpath(".//results/result").each{|results|
    result = results.xpath(".")
    puts result.inner_html
    r={
      'PROJECT_ID'=>text(result[0].xpath("Project_ID/text()")),
      'TITLE'=>text(result[0].xpath("Title/text()")),
      'PROJECT_TYPE'=>text(result[0].xpath("Snapshot/text()")),
      'SNAPSHOT'=>text(result[0].xpath("Project_ID/text()")),
      'AGENCY'=>text(result[0].xpath("Agency/text()")),
      'STATUS'=>text(result[0].xpath("Status/text()")),
      'SUB_OR_TOWN'=>text(result[0].xpath("Suburb_Or_Town/text()")),
      'STATE'=>text(result[0].xpath("State/text()")),
      'POSTCODE'=>text(result[0].xpath("Postcode/text()")),
      'LAT'=>text(result[0].xpath("GIS_Loc_Latitude/text()")),
      'LONG'=>text(result[0].xpath("GIS_Loc_Longitude/text()")),
      'FUNDING'=>text(result[0].xpath("Approved_Funding/text()")),
      'PROJECTS'=>text(result[0].xpath("Projects/text()")),
    }
    records << r
  }
  ScraperWiki.save_sqlite(unique_keys=['PROJECT_ID'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    pg = br.get(BASE_URL+"/data/GetElectorateResultSet.aspx?electoratename=#{srch}&responsetype=xml")
    scrape(pg.body)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/i
    exit if e.inspect =~ /interrupt/i  
  end
end


range =  ['Aston','Ballarat','Batman','Bendigo','Bruce','Calwell','Casey','Chisholm','Corangamite','Corio','Deakin','Dunkley','Flinders','Gellibrand','Gippsland','Goldstein','Gorton','Higgins','Holt','Hotham','Indi','Isaacs','Jagajaga','Kooyong','Lalor','LaTrobe','Mallee','Maribyrnong','McEwen','McMillan','Melbourne','MelbournePorts','Menzies','Murray','Scullin','Wannon','Wills']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next  if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)

end# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'csv'


Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://www.economicstimulusplan.gov.au"

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
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

def text(str)
  begin
      return (str.nil? or str.text.nil?) ? "" : str.text.gsub(/\n|\t|^\s+|\s+$/,"")
  rescue Exception => es
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil?) ? "" : t.first.attributes[attr].value
end


def scrape(data)
  records = []
  Nokogiri::XML(data).xpath(".//results/result").each{|results|
    result = results.xpath(".")
    puts result.inner_html
    r={
      'PROJECT_ID'=>text(result[0].xpath("Project_ID/text()")),
      'TITLE'=>text(result[0].xpath("Title/text()")),
      'PROJECT_TYPE'=>text(result[0].xpath("Snapshot/text()")),
      'SNAPSHOT'=>text(result[0].xpath("Project_ID/text()")),
      'AGENCY'=>text(result[0].xpath("Agency/text()")),
      'STATUS'=>text(result[0].xpath("Status/text()")),
      'SUB_OR_TOWN'=>text(result[0].xpath("Suburb_Or_Town/text()")),
      'STATE'=>text(result[0].xpath("State/text()")),
      'POSTCODE'=>text(result[0].xpath("Postcode/text()")),
      'LAT'=>text(result[0].xpath("GIS_Loc_Latitude/text()")),
      'LONG'=>text(result[0].xpath("GIS_Loc_Longitude/text()")),
      'FUNDING'=>text(result[0].xpath("Approved_Funding/text()")),
      'PROJECTS'=>text(result[0].xpath("Projects/text()")),
    }
    records << r
  }
  ScraperWiki.save_sqlite(unique_keys=['PROJECT_ID'],records,table_name='SWDATA',verbose=2) unless records.length==0
end

def action(srch)
  begin
    br = Mechanize.new { |b|
      b.user_agent_alias = 'Linux Firefox'
      b.read_timeout = 1200
    }
    pg = br.get(BASE_URL+"/data/GetElectorateResultSet.aspx?electoratename=#{srch}&responsetype=xml")
    scrape(pg.body)
  rescue Exception => e
    puts "ERROR: While processing #{srch} :: #{e.inspect} :: #{e.backtrace}"
    retry if e.inspect =~ /time/i
    exit if e.inspect =~ /interrupt/i  
  end
end


range =  ['Aston','Ballarat','Batman','Bendigo','Bruce','Calwell','Casey','Chisholm','Corangamite','Corio','Deakin','Dunkley','Flinders','Gellibrand','Gippsland','Goldstein','Gorton','Higgins','Holt','Hotham','Indi','Isaacs','Jagajaga','Kooyong','Lalor','LaTrobe','Mallee','Maribyrnong','McEwen','McMillan','Melbourne','MelbournePorts','Menzies','Murray','Scullin','Wannon','Wills']
offset = get_metadata("OFFSET",0)
offset = 0 if offset >= range.length
range.each_with_index do|srch,index|
  next  if index < offset
  action(srch)
  save_metadata("OFFSET",index.next)

end