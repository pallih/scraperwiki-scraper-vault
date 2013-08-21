require 'nokogiri'
require 'mechanize'
require 'pp'
Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://ucc.state.ri.us/'
@br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}

#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS CMPLIST (ID INTEGER PRIMARY KEY AUTOINCREMENT , ENTITY_NUMBER TEXT,ENTITY_NAME TEXT,CHARTER TEXT,STATUS TEXT,TYPE TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS CMPINFO (ID INTEGER PRIMARY KEY AUTOINCREMENT , ENTITY_NAME TEXT, NEW_ENTITY_NAME TEXT, CHANGED_ON TEXT, TYPE TEXT,ENTITY_NUMBER TEXT, DOI TEXT,DOO TEXT,P_ADDR1 TEXT,P_ADDR2 TEXT,P_CITY TEXT,P_STATE TEXT,P_ZIP TEXT,P_COUNTRY TEXT,M_ADDR1 TEXT,M_ADDR2 TEXT,M_CITY TEXT,M_STATE TEXT,M_ZIP TEXT,M_COUNTRY TEXT,AGNT_RESIGNED TEXT,ADDR_MAINTAINED TEXT,AGNT_NAME TEXT,AGNT_ADDR1 TEXT,AGNT_ADDR2 TEXT,AGNT_CITY TEXT,AGNT_STATE TEXT,AGNT_ZIP TEXT,AGNT_COUNTRY TEXT,PURPOSE TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS PRINCIPALS (ID INTEGER PRIMARY KEY AUTOINCREMENT , ENTITY_NUMBER TEXT,TITLE TEXT,NAME TEXT,ADDR TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS SHARES (ID INTEGER PRIMARY KEY AUTOINCREMENT , ENTITY_NUMBER TEXT,CLASS TEXT,SERIES TEXT,PARVALUE TEXT,TOTAL_SHARES TEXT,TOTAL_ISSUED TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS ERROR_LOG (ID INTEGER PRIMARY KEY AUTOINCREMENT ,  KEYWORD TEXT,CODE TEXT, TRACE TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS INVALID(ID INTEGER PRIMARY KEY AUTOINCREMENT,ENTITY_NUMBER TEXT);")
#ScraperWiki.sqliteexecute("CREATE INDEX IF NOT EXISTS IDX_E_CL ON CMPLIST(ENTITY_NUMBER);")
#ScraperWiki.sqliteexecute("CREATE INDEX IF NOT EXISTS IDX_E_CI ON CMPINFO(ENTITY_NUMBER);")
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

def persist_principals(records)
  ScraperWiki.sqliteexecute("insert into PRINCIPALS(ENTITY_NUMBER,TITLE,NAME,ADDR) values(?,?,?,?);",[records['ENTITY_NUMBER'],records['TITLE'],records['NAME'],records['ADDR']])
  ScraperWiki.commit()
end

def persist_list(records)
    ScraperWiki.sqliteexecute("INSERT INTO CMPLIST(ENTITY_NAME,ENTITY_NUMBER,CHARTER,STATUS,TYPE) VALUES(?,?,?,?,?);",[records['ENTITY_NAME'],records['ENTITY_NUMBER'],records['CHARTER'],records['STATUS'],records['TYPE']])
  ScraperWiki.commit()
    end

def persist_info(records)
    ScraperWiki.sqliteexecute("INSERT INTO CMPINFO (ENTITY_NAME,NEW_ENTITY_NAME,CHANGED_ON,TYPE,ENTITY_NUMBER,DOI,DOO,DOR,P_ADDR1,P_ADDR2,P_CITY,P_STATE,P_ZIP,P_COUNTRY,M_ADDR1,M_ADDR2,M_CITY,M_STATE ,M_ZIP ,M_COUNTRY ,AGNT_RESIGNED ,ADDR_MAINTAINED ,AGNT_NAME ,AGNT_ADDR1 ,AGNT_ADDR2 ,AGNT_CITY ,AGNT_STATE ,AGNT_ZIP ,AGNT_COUNTRY ,PURPOSE) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",[records['ENTITY_NAME'],records['NEW_ENTITY_NAME'],records['CHANGED_ON'],records['TYPE'],records['ENTITY_NUMBER'],records['DOI'],records['DOO'],records['DOR'],records['P_ADDR1'],records['P_ADDR2'],records['P_CITY'],records['P_STATE'],records['P_ZIP'],records['P_COUNTRY'],records['M_ADDR1'],records['M_ADDR2'],records['M_CITY'],records['M_STATE'],records['M_ZIP'],records['M_COUNTRY'],records['AGNT_RESIGNED'],records['ADDR_MAINTAINED'],records['AGNT_NAME'],records['AGNT_ADDR1'],records['AGNT_ADDR2'],records['AGNT_CITY'],records['AGNT_STATE'],records['AGNT_ZIP'],records['AGNT_COUNTRY'],records['PURPOSE']])
    ScraperWiki.commit()
end
def persist_stock(records)
    ScraperWiki.sqliteexecute("INSERT INTO SHARES (ENTITY_NUMBER,CLASS,SERIES,PARVALUE,TOTAL_SHARES,TOTAL_ISSUED) values(?,?,?,?,?,?);",records['ENTITY_NUMBER'],records['CLASS'],records['SERIES'],records['PARVALUE'],records['TOTAL_SHARES'],records['TOTAL_ISSUED'])
    ScraperWiki.commit()
end


def persist_log(records)
  begin
    ScraperWiki.sqliteexecute("insert into ERROR_LOG(KEYWORD,CODE,TRACE) values(?,?,?);",[records['KEYWORD'],records['CODE'],records['TRACE']])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during persist_log"
  end
end

def get_entities
    return ScraperWiki.sqliteexecute("select distinct substr(entity_number,1,length(entity_number)) as ent_num from cmplist WHERE ENT_NUM NOT IN (SELECT ENTITY_NUMBER FROM CMPINFO);")['data']
end

def is_valid(num)
  return ScraperWiki.sqliteexecute("select count(*) from invalid where entity_number = ?",[num])['data'][0][0]
end


def is_entity(num)
    return ScraperWiki.sqliteexecute("select count(*) from cmpinfo where entity_number = ?",[num])['data'][0][0]
end

def is_there(name,num)
    return ScraperWiki.sqliteexecute("select count(*) from cmplist where entity_name=? and entity_number=?",[name,num])['data'][0][0]
end


def strip(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/[\x80-\xff]|^\s+|:|\s+$|\n|\t|\r/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def scrape_list(data,type,ent_num)
  if type=="list"
    Nokogiri::HTML(data).xpath("//tr[@bgcolor='#C0C0C0']/following-sibling::tr[1]/td/table/tr[position()>1]").each{|tr| #Search results
      td = tr.xpath("td")
      records = {
        "ENTITY_NAME" => strip(td[0]),
        "ENTITY_NUMBER" => strip(td[1]),
        "CHARTER" => strip(td[2]),
        "STATUS" => strip(td[3]),
        "TYPE" => strip(td[4])
      }
      #puts records.inspect
      #ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],records,table_name="CMPLIST")
      persist_list(records) unless is_there(records['ENTITY_NAME'],records['ENTITY_NUMBER']) > 1
    }
  elsif type=="details"
    records = { }
    doc = Nokogiri::HTML(data)
    begin
        e_names = doc.xpath("//input[@name='EntityName']/following-sibling::u")
        begin
         records['ENTITY_NAME'] = strip(e_names[0])
         records['NEW_ENTITY_NAME'] = strip(e_names[1])
         records['CHANGED_ON'] = strip(e_names[2])
        end unless e_names.nil? 
        records['TYPE'] = strip(doc.xpath("//input[@name='EntityTypeDescriptor']/following-sibling::u"))
        records['ENTITY_NUMBER'] = strip(doc.xpath("//input[@name='FEIN']/following-sibling::u")) 
        if records['ENTITY_NUMBER'].nil? or records['ENTITY_NUMBER'].empty? 
          ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],{'ENTITY_NUMBER' => ent_num},table_name="INVALID")
          return
        end

        records['DOI'] = strip(doc.xpath("//input[@name='DateOfOrganization']/following-sibling::u"))
        records['DOO'] = strip(doc.xpath("//input[@name='JurisdictionDate']/following-sibling::u"))
        records['DOR'] = strip(doc.xpath("//input[@name='InactiveDate']/following-sibling::u"))  
        records['P_ADDR1'] = strip(doc.xpath("//input[@name='Addr1']/following-sibling::u"))
        records['P_ADDR2'] = strip(doc.xpath("//input[@name='Addr2']/following-sibling::u"))
        records['P_CITY'] = strip(doc.xpath("//input[@name='City']/following-sibling::u"))
        records['P_STATE'] = strip(doc.xpath("//input[@name='State']/following-sibling::u"))
        records['P_ZIP'] = strip(doc.xpath("//input[@name='PostalCode']/following-sibling::u"))
        records['P_COUNTRY'] = strip(doc.xpath("//input[@name='CountryCode']/following-sibling::u"))
        records['M_ADDR1'] = strip(doc.xpath("//input[@name='OtherAddr1']/following-sibling::u"))
        records['M_ADDR2'] = strip(doc.xpath("//input[@name='OtherAddr2']/following-sibling::u"))
        records['M_CITY'] = strip(doc.xpath("//input[@name='OtherCity']/following-sibling::u"))
        records['M_STATE'] = strip(doc.xpath("//input[@name='OtherState']/following-sibling::u"))
        records['M_ZIP'] = strip(doc.xpath("//input[@name='OtherPostalCode']/following-sibling::u"))
        records['M_COUNTRY'] = strip(doc.xpath("//input[@name='OtherCountryCode']/following-sibling::u"))
        records['AGNT_RESIGNED'] = strip(doc.xpath("//input[@name='ProfitFlag']/following-sibling::u"))
        records['ADDR_MAINTAINED'] = strip(doc.xpath("//input[@name='ConsentFlag']/following-sibling::u"))
        records['AGNT_NAME'] = strip(doc.xpath("//input[@name='AgentName']/following-sibling::u"))
        records['AGNT_ADDR1'] = strip(doc.xpath("//input[@name='AgentAddr1']/following-sibling::u"))
        records['AGNT_ADDR2'] = strip(doc.xpath("//input[@name='AgentAddr2']/following-sibling::u"))
        records['AGNT_CITY'] = strip(doc.xpath("//input[@name='AgentCity']/following-sibling::u"))
        records['AGNT_STATE'] = strip(doc.xpath("//input[@name='AgentState']/following-sibling::u"))
        records['AGNT_ZIP'] = strip(doc.xpath("//input[@name='AgentPostalCode']/following-sibling::u"))
        records['AGNT_COUNTRY'] = strip(doc.xpath("//input[@name='AgentCountryCode']/following-sibling::u"))
        records['PURPOSE'] = strip(doc.xpath("//td[@wrap='soft']"))
        #puts records.inspect
        ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],records,table_name="CMPINFO")
        prin = doc.xpath("//table[@bordercolor='#COCOCO']/tr[position()>1]")
        begin
            prin.each{|tr|
                td = tr.xpath('td')
                principals = {
                    "ENTITY_NUMBER" => records['ENTITY_NUMBER'],
                    "TITLE" => strip(td[0]),
                    "NAME" => strip(td[1]),
                    "ADDR" => strip(td[2])
                }
                #puts principals.inspect
                ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],principals,table_name="PRINCIPALS") unless principals['NAME'].nil? or principals['NAME'].empty? 
            }
        end unless prin.nil? 

        stock = doc.xpath("//table[@bordercolor='#C0C0C0']/tr[position()>1]")
        begin
          td = stock.xpath("td")
          shares = {
              "ENTITY_NUMBER" => records['ENTITY_NUMBER'],
              "CLASS" => strip(td[0]),
              "SERIES" => strip(td[1]),
              "PARVALUE" => strip(td[2]),
              "TOTAL_SHARES" => strip(td[3]),
              "TOTAL_ISSUED" => strip(td[4])
          }
          #puts shares.inspect
          ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],shares,table_name="SHARES") unless shares['CLASS'].nil? or shares['CLASS'].empty? 
        end unless stock.nil? 
    end
  else
    puts "Info:Unknown action type"
  end
  return nil
end


def perform_action(keyword,action,idn)
  begin
    if action == "search"
      begin
      pg_num = get_metadata(keyword,1).to_i#strt[1].to_i
      s_url = BASE_URL+"CorpSearch/CorpSearchEntityList.asp?ReadFromDB=True&UpdateAllowed="
      p = {"EntityName" => "#{keyword}", "SearchType" => "E", "LastName" => "", "FirstName" => "", "MiddleName" => "", "iPageNum" => "#{pg_num}", "lstDisplay" => "5000", "TotalPageCount" => "", "TotalRecords" => "", "SearchMethod" => "B", "Purpose" => "", "AgentName" => "", "Address" => "", "ActiveFlagCrit" => "Y", "ActiveFlag" => ""}
      @pg = @br.post(s_url,p)
      scrape_list(@pg.body,"list")
      begin
        pg_num = pg_num +1
        p["iPageNum"] = pg_num
        @pg.form_with(:name => "frmCorpSearch") do |f|
          p.each {|k,v|
            f[k] = v
          }
          @pg =  f.submit
        end
        scrape_list(@pg.body,"list",nil)
        save_metadata(keyword,pg_num)
      end while @pg.at("input[@name='cmdNext']")
      rescue Exception => e
        puts "Error: While processing :: #{e.inspect} :: #{e.backtrace}"
      end
    elsif action == "list"
      idn.each{|num|
        begin
          #pp "Processing #{num} "#:: #{is_entity(num[0])} :: #{is_valid(num[0])}"
          begin
            de_pg = @br.get(BASE_URL+"CorpSearch/CorpSearchSummary.asp?ReadFromDB=False&UpdateAllowed=&FEIN=#{num[0]}")
            scrape_list(de_pg.body,"details",num[0])
          end unless is_entity(num[0]) > 0 or is_valid(num[0]) > 0
        rescue Exception => e
          puts "Error: While processing :: #{e.inspect} :: #{e.backtrace}"
        end 
      }
      
    else
      puts "Unknown action type"
    end
  rescue Exception => e
    puts "Error: While processing :: #{e.inspect} :: #{e.backtrace}"
    records = { "KEYWORD" => keyword, "CODE" => e.inspect, "TRACE" => e.backtrace.join("\n") }
    #persist_log(records)
  end
end

#perform_action("-","search",nil)


#strt = 0#get_metadata("PARAM","A")
#("A".."Z").each{|c|
#  puts "Processing #{c} currently"
#  perform_action(c,"search",nil)
#}


perform_action(nil,"list",get_entities)

require 'nokogiri'
require 'mechanize'
require 'pp'
Mechanize.html_parser = Nokogiri::HTML
BASE_URL = 'http://ucc.state.ri.us/'
@br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
}

#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS CMPLIST (ID INTEGER PRIMARY KEY AUTOINCREMENT , ENTITY_NUMBER TEXT,ENTITY_NAME TEXT,CHARTER TEXT,STATUS TEXT,TYPE TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS CMPINFO (ID INTEGER PRIMARY KEY AUTOINCREMENT , ENTITY_NAME TEXT, NEW_ENTITY_NAME TEXT, CHANGED_ON TEXT, TYPE TEXT,ENTITY_NUMBER TEXT, DOI TEXT,DOO TEXT,P_ADDR1 TEXT,P_ADDR2 TEXT,P_CITY TEXT,P_STATE TEXT,P_ZIP TEXT,P_COUNTRY TEXT,M_ADDR1 TEXT,M_ADDR2 TEXT,M_CITY TEXT,M_STATE TEXT,M_ZIP TEXT,M_COUNTRY TEXT,AGNT_RESIGNED TEXT,ADDR_MAINTAINED TEXT,AGNT_NAME TEXT,AGNT_ADDR1 TEXT,AGNT_ADDR2 TEXT,AGNT_CITY TEXT,AGNT_STATE TEXT,AGNT_ZIP TEXT,AGNT_COUNTRY TEXT,PURPOSE TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS PRINCIPALS (ID INTEGER PRIMARY KEY AUTOINCREMENT , ENTITY_NUMBER TEXT,TITLE TEXT,NAME TEXT,ADDR TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS SHARES (ID INTEGER PRIMARY KEY AUTOINCREMENT , ENTITY_NUMBER TEXT,CLASS TEXT,SERIES TEXT,PARVALUE TEXT,TOTAL_SHARES TEXT,TOTAL_ISSUED TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS ERROR_LOG (ID INTEGER PRIMARY KEY AUTOINCREMENT ,  KEYWORD TEXT,CODE TEXT, TRACE TEXT);")
#ScraperWiki.sqliteexecute("CREATE TABLE IF NOT EXISTS INVALID(ID INTEGER PRIMARY KEY AUTOINCREMENT,ENTITY_NUMBER TEXT);")
#ScraperWiki.sqliteexecute("CREATE INDEX IF NOT EXISTS IDX_E_CL ON CMPLIST(ENTITY_NUMBER);")
#ScraperWiki.sqliteexecute("CREATE INDEX IF NOT EXISTS IDX_E_CI ON CMPINFO(ENTITY_NUMBER);")
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

def persist_principals(records)
  ScraperWiki.sqliteexecute("insert into PRINCIPALS(ENTITY_NUMBER,TITLE,NAME,ADDR) values(?,?,?,?);",[records['ENTITY_NUMBER'],records['TITLE'],records['NAME'],records['ADDR']])
  ScraperWiki.commit()
end

def persist_list(records)
    ScraperWiki.sqliteexecute("INSERT INTO CMPLIST(ENTITY_NAME,ENTITY_NUMBER,CHARTER,STATUS,TYPE) VALUES(?,?,?,?,?);",[records['ENTITY_NAME'],records['ENTITY_NUMBER'],records['CHARTER'],records['STATUS'],records['TYPE']])
  ScraperWiki.commit()
    end

def persist_info(records)
    ScraperWiki.sqliteexecute("INSERT INTO CMPINFO (ENTITY_NAME,NEW_ENTITY_NAME,CHANGED_ON,TYPE,ENTITY_NUMBER,DOI,DOO,DOR,P_ADDR1,P_ADDR2,P_CITY,P_STATE,P_ZIP,P_COUNTRY,M_ADDR1,M_ADDR2,M_CITY,M_STATE ,M_ZIP ,M_COUNTRY ,AGNT_RESIGNED ,ADDR_MAINTAINED ,AGNT_NAME ,AGNT_ADDR1 ,AGNT_ADDR2 ,AGNT_CITY ,AGNT_STATE ,AGNT_ZIP ,AGNT_COUNTRY ,PURPOSE) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);",[records['ENTITY_NAME'],records['NEW_ENTITY_NAME'],records['CHANGED_ON'],records['TYPE'],records['ENTITY_NUMBER'],records['DOI'],records['DOO'],records['DOR'],records['P_ADDR1'],records['P_ADDR2'],records['P_CITY'],records['P_STATE'],records['P_ZIP'],records['P_COUNTRY'],records['M_ADDR1'],records['M_ADDR2'],records['M_CITY'],records['M_STATE'],records['M_ZIP'],records['M_COUNTRY'],records['AGNT_RESIGNED'],records['ADDR_MAINTAINED'],records['AGNT_NAME'],records['AGNT_ADDR1'],records['AGNT_ADDR2'],records['AGNT_CITY'],records['AGNT_STATE'],records['AGNT_ZIP'],records['AGNT_COUNTRY'],records['PURPOSE']])
    ScraperWiki.commit()
end
def persist_stock(records)
    ScraperWiki.sqliteexecute("INSERT INTO SHARES (ENTITY_NUMBER,CLASS,SERIES,PARVALUE,TOTAL_SHARES,TOTAL_ISSUED) values(?,?,?,?,?,?);",records['ENTITY_NUMBER'],records['CLASS'],records['SERIES'],records['PARVALUE'],records['TOTAL_SHARES'],records['TOTAL_ISSUED'])
    ScraperWiki.commit()
end


def persist_log(records)
  begin
    ScraperWiki.sqliteexecute("insert into ERROR_LOG(KEYWORD,CODE,TRACE) values(?,?,?);",[records['KEYWORD'],records['CODE'],records['TRACE']])
    ScraperWiki.commit()
  rescue Exception => e
    puts "ERROR: #{e.inspect} during persist_log"
  end
end

def get_entities
    return ScraperWiki.sqliteexecute("select distinct substr(entity_number,1,length(entity_number)) as ent_num from cmplist WHERE ENT_NUM NOT IN (SELECT ENTITY_NUMBER FROM CMPINFO);")['data']
end

def is_valid(num)
  return ScraperWiki.sqliteexecute("select count(*) from invalid where entity_number = ?",[num])['data'][0][0]
end


def is_entity(num)
    return ScraperWiki.sqliteexecute("select count(*) from cmpinfo where entity_number = ?",[num])['data'][0][0]
end

def is_there(name,num)
    return ScraperWiki.sqliteexecute("select count(*) from cmplist where entity_name=? and entity_number=?",[name,num])['data'][0][0]
end


def strip(str)
  begin
      return (str.nil? or str.text.nil?) ? nil : str.text.gsub(/[\x80-\xff]|^\s+|:|\s+$|\n|\t|\r/,"")
  rescue Exception => e
      return str.text unless str.nil? 
      puts e.backtrace
  end
end

def scrape_list(data,type,ent_num)
  if type=="list"
    Nokogiri::HTML(data).xpath("//tr[@bgcolor='#C0C0C0']/following-sibling::tr[1]/td/table/tr[position()>1]").each{|tr| #Search results
      td = tr.xpath("td")
      records = {
        "ENTITY_NAME" => strip(td[0]),
        "ENTITY_NUMBER" => strip(td[1]),
        "CHARTER" => strip(td[2]),
        "STATUS" => strip(td[3]),
        "TYPE" => strip(td[4])
      }
      #puts records.inspect
      #ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],records,table_name="CMPLIST")
      persist_list(records) unless is_there(records['ENTITY_NAME'],records['ENTITY_NUMBER']) > 1
    }
  elsif type=="details"
    records = { }
    doc = Nokogiri::HTML(data)
    begin
        e_names = doc.xpath("//input[@name='EntityName']/following-sibling::u")
        begin
         records['ENTITY_NAME'] = strip(e_names[0])
         records['NEW_ENTITY_NAME'] = strip(e_names[1])
         records['CHANGED_ON'] = strip(e_names[2])
        end unless e_names.nil? 
        records['TYPE'] = strip(doc.xpath("//input[@name='EntityTypeDescriptor']/following-sibling::u"))
        records['ENTITY_NUMBER'] = strip(doc.xpath("//input[@name='FEIN']/following-sibling::u")) 
        if records['ENTITY_NUMBER'].nil? or records['ENTITY_NUMBER'].empty? 
          ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],{'ENTITY_NUMBER' => ent_num},table_name="INVALID")
          return
        end

        records['DOI'] = strip(doc.xpath("//input[@name='DateOfOrganization']/following-sibling::u"))
        records['DOO'] = strip(doc.xpath("//input[@name='JurisdictionDate']/following-sibling::u"))
        records['DOR'] = strip(doc.xpath("//input[@name='InactiveDate']/following-sibling::u"))  
        records['P_ADDR1'] = strip(doc.xpath("//input[@name='Addr1']/following-sibling::u"))
        records['P_ADDR2'] = strip(doc.xpath("//input[@name='Addr2']/following-sibling::u"))
        records['P_CITY'] = strip(doc.xpath("//input[@name='City']/following-sibling::u"))
        records['P_STATE'] = strip(doc.xpath("//input[@name='State']/following-sibling::u"))
        records['P_ZIP'] = strip(doc.xpath("//input[@name='PostalCode']/following-sibling::u"))
        records['P_COUNTRY'] = strip(doc.xpath("//input[@name='CountryCode']/following-sibling::u"))
        records['M_ADDR1'] = strip(doc.xpath("//input[@name='OtherAddr1']/following-sibling::u"))
        records['M_ADDR2'] = strip(doc.xpath("//input[@name='OtherAddr2']/following-sibling::u"))
        records['M_CITY'] = strip(doc.xpath("//input[@name='OtherCity']/following-sibling::u"))
        records['M_STATE'] = strip(doc.xpath("//input[@name='OtherState']/following-sibling::u"))
        records['M_ZIP'] = strip(doc.xpath("//input[@name='OtherPostalCode']/following-sibling::u"))
        records['M_COUNTRY'] = strip(doc.xpath("//input[@name='OtherCountryCode']/following-sibling::u"))
        records['AGNT_RESIGNED'] = strip(doc.xpath("//input[@name='ProfitFlag']/following-sibling::u"))
        records['ADDR_MAINTAINED'] = strip(doc.xpath("//input[@name='ConsentFlag']/following-sibling::u"))
        records['AGNT_NAME'] = strip(doc.xpath("//input[@name='AgentName']/following-sibling::u"))
        records['AGNT_ADDR1'] = strip(doc.xpath("//input[@name='AgentAddr1']/following-sibling::u"))
        records['AGNT_ADDR2'] = strip(doc.xpath("//input[@name='AgentAddr2']/following-sibling::u"))
        records['AGNT_CITY'] = strip(doc.xpath("//input[@name='AgentCity']/following-sibling::u"))
        records['AGNT_STATE'] = strip(doc.xpath("//input[@name='AgentState']/following-sibling::u"))
        records['AGNT_ZIP'] = strip(doc.xpath("//input[@name='AgentPostalCode']/following-sibling::u"))
        records['AGNT_COUNTRY'] = strip(doc.xpath("//input[@name='AgentCountryCode']/following-sibling::u"))
        records['PURPOSE'] = strip(doc.xpath("//td[@wrap='soft']"))
        #puts records.inspect
        ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],records,table_name="CMPINFO")
        prin = doc.xpath("//table[@bordercolor='#COCOCO']/tr[position()>1]")
        begin
            prin.each{|tr|
                td = tr.xpath('td')
                principals = {
                    "ENTITY_NUMBER" => records['ENTITY_NUMBER'],
                    "TITLE" => strip(td[0]),
                    "NAME" => strip(td[1]),
                    "ADDR" => strip(td[2])
                }
                #puts principals.inspect
                ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],principals,table_name="PRINCIPALS") unless principals['NAME'].nil? or principals['NAME'].empty? 
            }
        end unless prin.nil? 

        stock = doc.xpath("//table[@bordercolor='#C0C0C0']/tr[position()>1]")
        begin
          td = stock.xpath("td")
          shares = {
              "ENTITY_NUMBER" => records['ENTITY_NUMBER'],
              "CLASS" => strip(td[0]),
              "SERIES" => strip(td[1]),
              "PARVALUE" => strip(td[2]),
              "TOTAL_SHARES" => strip(td[3]),
              "TOTAL_ISSUED" => strip(td[4])
          }
          #puts shares.inspect
          ScraperWiki.save_sqlite(unique_keys=['ENTITY_NUMBER'],shares,table_name="SHARES") unless shares['CLASS'].nil? or shares['CLASS'].empty? 
        end unless stock.nil? 
    end
  else
    puts "Info:Unknown action type"
  end
  return nil
end


def perform_action(keyword,action,idn)
  begin
    if action == "search"
      begin
      pg_num = get_metadata(keyword,1).to_i#strt[1].to_i
      s_url = BASE_URL+"CorpSearch/CorpSearchEntityList.asp?ReadFromDB=True&UpdateAllowed="
      p = {"EntityName" => "#{keyword}", "SearchType" => "E", "LastName" => "", "FirstName" => "", "MiddleName" => "", "iPageNum" => "#{pg_num}", "lstDisplay" => "5000", "TotalPageCount" => "", "TotalRecords" => "", "SearchMethod" => "B", "Purpose" => "", "AgentName" => "", "Address" => "", "ActiveFlagCrit" => "Y", "ActiveFlag" => ""}
      @pg = @br.post(s_url,p)
      scrape_list(@pg.body,"list")
      begin
        pg_num = pg_num +1
        p["iPageNum"] = pg_num
        @pg.form_with(:name => "frmCorpSearch") do |f|
          p.each {|k,v|
            f[k] = v
          }
          @pg =  f.submit
        end
        scrape_list(@pg.body,"list",nil)
        save_metadata(keyword,pg_num)
      end while @pg.at("input[@name='cmdNext']")
      rescue Exception => e
        puts "Error: While processing :: #{e.inspect} :: #{e.backtrace}"
      end
    elsif action == "list"
      idn.each{|num|
        begin
          #pp "Processing #{num} "#:: #{is_entity(num[0])} :: #{is_valid(num[0])}"
          begin
            de_pg = @br.get(BASE_URL+"CorpSearch/CorpSearchSummary.asp?ReadFromDB=False&UpdateAllowed=&FEIN=#{num[0]}")
            scrape_list(de_pg.body,"details",num[0])
          end unless is_entity(num[0]) > 0 or is_valid(num[0]) > 0
        rescue Exception => e
          puts "Error: While processing :: #{e.inspect} :: #{e.backtrace}"
        end 
      }
      
    else
      puts "Unknown action type"
    end
  rescue Exception => e
    puts "Error: While processing :: #{e.inspect} :: #{e.backtrace}"
    records = { "KEYWORD" => keyword, "CODE" => e.inspect, "TRACE" => e.backtrace.join("\n") }
    #persist_log(records)
  end
end

#perform_action("-","search",nil)


#strt = 0#get_metadata("PARAM","A")
#("A".."Z").each{|c|
#  puts "Processing #{c} currently"
#  perform_action(c,"search",nil)
#}


perform_action(nil,"list",get_entities)

