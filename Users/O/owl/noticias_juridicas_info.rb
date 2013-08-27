# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://noticias.juridicas.com/guia/"

class String
  def join(str)
    self+str
  end
  def pretty
    self.gsub(/\n|\t|\r/,'').gsub(/,$/,'').strip
  end

end
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


def scrape(data,act,rec)
  if act == "list"
    records = []
    list = Nokogiri::HTML(data).xpath(".//div[@style='width: 580px; float: left; margin: 3px']/p[@align='left']/a")
    list.each{|ele|
      records << attributes(ele.xpath("."),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//h4[text()='Datos Personales']/following::table[1]/tr")
    r = {"ID"=>rec['ID'],"URL"=>rec['URL'],'DOC'=>Time.now}
    begin
      r["NAME"],r["SURNAME"] = text(doc.xpath("td[@class='remarcado' and text()='Nombre:']/following-sibling::td")).split(",")
      r["ADDRESS"] = text(doc.xpath("td[@class='remarcado' and text()='Dirección Postal:']/following-sibling::td")).join(",").pretty
      r["CITY"] = text(doc.xpath("td[@class='remarcado' and text()='Población:']/following-sibling::td")).join(",").pretty
      r["TELEPHONE"] = text(doc.xpath("td[@class='remarcado' and text()='Teléfono:']/following-sibling::td")).join(",").pretty
      r["FAX"] = text(doc.xpath("td[@class='remarcado' and text()='Fax:']/following-sibling::td")).join(",").pretty
      r["E-MAIL"] = text(doc.xpath("td[@class='remarcado' and text()='E-Mail:']/following-sibling::td")).join(",").pretty
    end

    doc = Nokogiri::HTML(data).xpath(".//h4[text()='Datos Profesionales']/following::table[1]/tr")
    begin
      r["COL_NO"] = text(doc.xpath("td[@class='remarcado' and text()='Colegiado núm.:']/following-sibling::td")).join(",").pretty
      r["PROVINCE"] = text(doc.xpath("td[@class='remarcado' and text()='Colegio(s):']/following-sibling::td")).join(",").pretty
      r["SPECIALITY"] = text(doc.xpath("td[@class='remarcado' and text()='Especialidad/es:']/following-sibling::td")).join(",").pretty
      r["WEBPAGE"] = text(doc.xpath("td[@class='remarcado' and text()='Página WEB:']/following-sibling::td")).join(",").pretty
      r["REMARKS"] = text(doc.xpath("td[@class='remarcado' and text()='Observaciones:']/following-sibling::td")).join(",").pretty
    end
    records << r unless r['NAME'].nil? or r['NAME'].empty? 
  end
  ScraperWiki.save_sqlite(unique_keys=['ID'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  begin
  s_url = BASE_URL + "rsl_abogado.php?COLEGIO=#{srch}"
  pg = br.get(s_url)
  urls = scrape(pg.body,"list",nil)
  urls.each{|url|
    a_url = BASE_URL + url
    pg_tmp = br.get(a_url)
    scrape(pg_tmp.body,"details",{"ID"=>url.split(/=/).last,"URL"=>a_url})
  }
  rescue Exception => e
   raise e
  end
end

#save_metadata("OFFSET",0)
provinces = {""=>"0","A Coruña"=>"0015001", "Alava"=>"0001001", "Albacete"=>"0002001", "Alcala de Henares"=>"0028002", "Alcoi"=>"0003003", "Alicante"=>"0003001", "Almeria"=>"0004011", "Alzira"=>"0016002", "Antequera"=>"0029001", "Ávila"=>"0005001", "Badajoz"=>"0006001", "Barcelona"=>"0008001", "Burgos"=>"0009001", "Caceres"=>"0010001", "Cádiz"=>"0011001", "Cartagena"=>"0030003", "Castellón"=>"0012001", "Ceuta"=>"0051001", "Ciudad Real"=>"0013001", "Córdoba"=>"0014001", "Cuenca"=>"0016001", "Elche"=>"0003002", "Estella"=>"0031004", "Ferrol"=>"0015003", "Figueres"=>"0017002", "Gijón"=>"0033200", "Girona"=>"0017001", "Granada"=>"0018001", "Granollers"=>"0008007", "Guadalajara"=>"0019001", "Huelva"=>"0021001", "Huesca"=>"0022001", "Jaén"=>"0023001", "Jerez de la frontera"=>"0011002", "Lanzarote"=>"0038004", "Las Palmas de Gran Canaria"=>"0038003", "León"=>"0024001", "Lleida"=>"0025001", "Logroño"=>"0026001", "Lorca"=>"0030002", "Lucena"=>"0014002", "Lugo"=>"0027001", "Madrid"=>"0028001", "Málaga"=>"0029002", "Manresa"=>"0008006", "Mataró"=>"0008005", "Melilla"=>"0052001", "Murcia"=>"0030001", "Oriola"=>"0046004", "Ourense"=>"0032001", "Oviedo"=>"0033001", "Palencia"=>"0034001", "Palma de Mallorca"=>"0007001", "Pamplona"=>"0031001", "Pontevedra"=>"0036002", "Reus"=>"0043002", "Sabadell"=>"0008003", "Salamanca"=>"0037001", "San Sebastian"=>"0020001", "Sant Feliu de Llobregat"=>"0008002", "Santander"=>"0039001", "Santiago de Compostela"=>"0015002", "Segovia"=>"0040001", "Sevilla"=>"0041000", "Soria"=>"0042001", "Sta. Cruz de La Palma"=>"0038002", "Sta. Cruz de Tenerife"=>"0038001", "Sueca"=>"0046003", "Tafalla"=>"0031003", "Talavera de la Reina"=>"0045002", "Tarragona"=>"0043001", "Terrassa"=>"0008004", "Teruel"=>"0044001", "Toledo"=>"0045001", "Tortosa"=>"0043003", "Tudela"=>"0031002", "Valencia"=>"0046001", "Valladolid"=>"0047001", "Vic"=>"0008009", "Vigo"=>"0036001", "Vizcaya"=>"0048001", "Zamora"=>"0049001", "Zaragoza"=>"0050280"}
offset = get_metadata("OFFSET",0)
provinces.each_with_index{|province,idx|
  next if idx < offset
  action(province.last)
  save_metadata("OFFSET",idx.next)

}
delete_metadata("OFFSET")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://noticias.juridicas.com/guia/"

class String
  def join(str)
    self+str
  end
  def pretty
    self.gsub(/\n|\t|\r/,'').gsub(/,$/,'').strip
  end

end
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


def scrape(data,act,rec)
  if act == "list"
    records = []
    list = Nokogiri::HTML(data).xpath(".//div[@style='width: 580px; float: left; margin: 3px']/p[@align='left']/a")
    list.each{|ele|
      records << attributes(ele.xpath("."),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//h4[text()='Datos Personales']/following::table[1]/tr")
    r = {"ID"=>rec['ID'],"URL"=>rec['URL'],'DOC'=>Time.now}
    begin
      r["NAME"],r["SURNAME"] = text(doc.xpath("td[@class='remarcado' and text()='Nombre:']/following-sibling::td")).split(",")
      r["ADDRESS"] = text(doc.xpath("td[@class='remarcado' and text()='Dirección Postal:']/following-sibling::td")).join(",").pretty
      r["CITY"] = text(doc.xpath("td[@class='remarcado' and text()='Población:']/following-sibling::td")).join(",").pretty
      r["TELEPHONE"] = text(doc.xpath("td[@class='remarcado' and text()='Teléfono:']/following-sibling::td")).join(",").pretty
      r["FAX"] = text(doc.xpath("td[@class='remarcado' and text()='Fax:']/following-sibling::td")).join(",").pretty
      r["E-MAIL"] = text(doc.xpath("td[@class='remarcado' and text()='E-Mail:']/following-sibling::td")).join(",").pretty
    end

    doc = Nokogiri::HTML(data).xpath(".//h4[text()='Datos Profesionales']/following::table[1]/tr")
    begin
      r["COL_NO"] = text(doc.xpath("td[@class='remarcado' and text()='Colegiado núm.:']/following-sibling::td")).join(",").pretty
      r["PROVINCE"] = text(doc.xpath("td[@class='remarcado' and text()='Colegio(s):']/following-sibling::td")).join(",").pretty
      r["SPECIALITY"] = text(doc.xpath("td[@class='remarcado' and text()='Especialidad/es:']/following-sibling::td")).join(",").pretty
      r["WEBPAGE"] = text(doc.xpath("td[@class='remarcado' and text()='Página WEB:']/following-sibling::td")).join(",").pretty
      r["REMARKS"] = text(doc.xpath("td[@class='remarcado' and text()='Observaciones:']/following-sibling::td")).join(",").pretty
    end
    records << r unless r['NAME'].nil? or r['NAME'].empty? 
  end
  ScraperWiki.save_sqlite(unique_keys=['ID'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  begin
  s_url = BASE_URL + "rsl_abogado.php?COLEGIO=#{srch}"
  pg = br.get(s_url)
  urls = scrape(pg.body,"list",nil)
  urls.each{|url|
    a_url = BASE_URL + url
    pg_tmp = br.get(a_url)
    scrape(pg_tmp.body,"details",{"ID"=>url.split(/=/).last,"URL"=>a_url})
  }
  rescue Exception => e
   raise e
  end
end

#save_metadata("OFFSET",0)
provinces = {""=>"0","A Coruña"=>"0015001", "Alava"=>"0001001", "Albacete"=>"0002001", "Alcala de Henares"=>"0028002", "Alcoi"=>"0003003", "Alicante"=>"0003001", "Almeria"=>"0004011", "Alzira"=>"0016002", "Antequera"=>"0029001", "Ávila"=>"0005001", "Badajoz"=>"0006001", "Barcelona"=>"0008001", "Burgos"=>"0009001", "Caceres"=>"0010001", "Cádiz"=>"0011001", "Cartagena"=>"0030003", "Castellón"=>"0012001", "Ceuta"=>"0051001", "Ciudad Real"=>"0013001", "Córdoba"=>"0014001", "Cuenca"=>"0016001", "Elche"=>"0003002", "Estella"=>"0031004", "Ferrol"=>"0015003", "Figueres"=>"0017002", "Gijón"=>"0033200", "Girona"=>"0017001", "Granada"=>"0018001", "Granollers"=>"0008007", "Guadalajara"=>"0019001", "Huelva"=>"0021001", "Huesca"=>"0022001", "Jaén"=>"0023001", "Jerez de la frontera"=>"0011002", "Lanzarote"=>"0038004", "Las Palmas de Gran Canaria"=>"0038003", "León"=>"0024001", "Lleida"=>"0025001", "Logroño"=>"0026001", "Lorca"=>"0030002", "Lucena"=>"0014002", "Lugo"=>"0027001", "Madrid"=>"0028001", "Málaga"=>"0029002", "Manresa"=>"0008006", "Mataró"=>"0008005", "Melilla"=>"0052001", "Murcia"=>"0030001", "Oriola"=>"0046004", "Ourense"=>"0032001", "Oviedo"=>"0033001", "Palencia"=>"0034001", "Palma de Mallorca"=>"0007001", "Pamplona"=>"0031001", "Pontevedra"=>"0036002", "Reus"=>"0043002", "Sabadell"=>"0008003", "Salamanca"=>"0037001", "San Sebastian"=>"0020001", "Sant Feliu de Llobregat"=>"0008002", "Santander"=>"0039001", "Santiago de Compostela"=>"0015002", "Segovia"=>"0040001", "Sevilla"=>"0041000", "Soria"=>"0042001", "Sta. Cruz de La Palma"=>"0038002", "Sta. Cruz de Tenerife"=>"0038001", "Sueca"=>"0046003", "Tafalla"=>"0031003", "Talavera de la Reina"=>"0045002", "Tarragona"=>"0043001", "Terrassa"=>"0008004", "Teruel"=>"0044001", "Toledo"=>"0045001", "Tortosa"=>"0043003", "Tudela"=>"0031002", "Valencia"=>"0046001", "Valladolid"=>"0047001", "Vic"=>"0008009", "Vigo"=>"0036001", "Vizcaya"=>"0048001", "Zamora"=>"0049001", "Zaragoza"=>"0050280"}
offset = get_metadata("OFFSET",0)
provinces.each_with_index{|province,idx|
  next if idx < offset
  action(province.last)
  save_metadata("OFFSET",idx.next)

}
delete_metadata("OFFSET")
# encoding: UTF-8
require 'nokogiri'
require 'mechanize'
require 'logger'
require 'csv'
require 'thread'

Mechanize.html_parser = Nokogiri::HTML

BASE_URL = "http://noticias.juridicas.com/guia/"

class String
  def join(str)
    self+str
  end
  def pretty
    self.gsub(/\n|\t|\r/,'').gsub(/,$/,'').strip
  end

end
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


def scrape(data,act,rec)
  if act == "list"
    records = []
    list = Nokogiri::HTML(data).xpath(".//div[@style='width: 580px; float: left; margin: 3px']/p[@align='left']/a")
    list.each{|ele|
      records << attributes(ele.xpath("."),"href")
    }
    return records
  elsif act == "details"
    records = []
    doc = Nokogiri::HTML(data).xpath(".//h4[text()='Datos Personales']/following::table[1]/tr")
    r = {"ID"=>rec['ID'],"URL"=>rec['URL'],'DOC'=>Time.now}
    begin
      r["NAME"],r["SURNAME"] = text(doc.xpath("td[@class='remarcado' and text()='Nombre:']/following-sibling::td")).split(",")
      r["ADDRESS"] = text(doc.xpath("td[@class='remarcado' and text()='Dirección Postal:']/following-sibling::td")).join(",").pretty
      r["CITY"] = text(doc.xpath("td[@class='remarcado' and text()='Población:']/following-sibling::td")).join(",").pretty
      r["TELEPHONE"] = text(doc.xpath("td[@class='remarcado' and text()='Teléfono:']/following-sibling::td")).join(",").pretty
      r["FAX"] = text(doc.xpath("td[@class='remarcado' and text()='Fax:']/following-sibling::td")).join(",").pretty
      r["E-MAIL"] = text(doc.xpath("td[@class='remarcado' and text()='E-Mail:']/following-sibling::td")).join(",").pretty
    end

    doc = Nokogiri::HTML(data).xpath(".//h4[text()='Datos Profesionales']/following::table[1]/tr")
    begin
      r["COL_NO"] = text(doc.xpath("td[@class='remarcado' and text()='Colegiado núm.:']/following-sibling::td")).join(",").pretty
      r["PROVINCE"] = text(doc.xpath("td[@class='remarcado' and text()='Colegio(s):']/following-sibling::td")).join(",").pretty
      r["SPECIALITY"] = text(doc.xpath("td[@class='remarcado' and text()='Especialidad/es:']/following-sibling::td")).join(",").pretty
      r["WEBPAGE"] = text(doc.xpath("td[@class='remarcado' and text()='Página WEB:']/following-sibling::td")).join(",").pretty
      r["REMARKS"] = text(doc.xpath("td[@class='remarcado' and text()='Observaciones:']/following-sibling::td")).join(",").pretty
    end
    records << r unless r['NAME'].nil? or r['NAME'].empty? 
  end
  ScraperWiki.save_sqlite(unique_keys=['ID'],records,table_name='swdata',verbose=2) unless records.length == 0
  return records.length
end

def action(srch)
  br = Mechanize.new { |b|
    b.user_agent_alias = 'Linux Firefox'
    b.read_timeout = 1200
    b.max_history=0
    b.retry_change_requests = true
    b.verify_mode = OpenSSL::SSL::VERIFY_NONE
  }
  begin
  s_url = BASE_URL + "rsl_abogado.php?COLEGIO=#{srch}"
  pg = br.get(s_url)
  urls = scrape(pg.body,"list",nil)
  urls.each{|url|
    a_url = BASE_URL + url
    pg_tmp = br.get(a_url)
    scrape(pg_tmp.body,"details",{"ID"=>url.split(/=/).last,"URL"=>a_url})
  }
  rescue Exception => e
   raise e
  end
end

#save_metadata("OFFSET",0)
provinces = {""=>"0","A Coruña"=>"0015001", "Alava"=>"0001001", "Albacete"=>"0002001", "Alcala de Henares"=>"0028002", "Alcoi"=>"0003003", "Alicante"=>"0003001", "Almeria"=>"0004011", "Alzira"=>"0016002", "Antequera"=>"0029001", "Ávila"=>"0005001", "Badajoz"=>"0006001", "Barcelona"=>"0008001", "Burgos"=>"0009001", "Caceres"=>"0010001", "Cádiz"=>"0011001", "Cartagena"=>"0030003", "Castellón"=>"0012001", "Ceuta"=>"0051001", "Ciudad Real"=>"0013001", "Córdoba"=>"0014001", "Cuenca"=>"0016001", "Elche"=>"0003002", "Estella"=>"0031004", "Ferrol"=>"0015003", "Figueres"=>"0017002", "Gijón"=>"0033200", "Girona"=>"0017001", "Granada"=>"0018001", "Granollers"=>"0008007", "Guadalajara"=>"0019001", "Huelva"=>"0021001", "Huesca"=>"0022001", "Jaén"=>"0023001", "Jerez de la frontera"=>"0011002", "Lanzarote"=>"0038004", "Las Palmas de Gran Canaria"=>"0038003", "León"=>"0024001", "Lleida"=>"0025001", "Logroño"=>"0026001", "Lorca"=>"0030002", "Lucena"=>"0014002", "Lugo"=>"0027001", "Madrid"=>"0028001", "Málaga"=>"0029002", "Manresa"=>"0008006", "Mataró"=>"0008005", "Melilla"=>"0052001", "Murcia"=>"0030001", "Oriola"=>"0046004", "Ourense"=>"0032001", "Oviedo"=>"0033001", "Palencia"=>"0034001", "Palma de Mallorca"=>"0007001", "Pamplona"=>"0031001", "Pontevedra"=>"0036002", "Reus"=>"0043002", "Sabadell"=>"0008003", "Salamanca"=>"0037001", "San Sebastian"=>"0020001", "Sant Feliu de Llobregat"=>"0008002", "Santander"=>"0039001", "Santiago de Compostela"=>"0015002", "Segovia"=>"0040001", "Sevilla"=>"0041000", "Soria"=>"0042001", "Sta. Cruz de La Palma"=>"0038002", "Sta. Cruz de Tenerife"=>"0038001", "Sueca"=>"0046003", "Tafalla"=>"0031003", "Talavera de la Reina"=>"0045002", "Tarragona"=>"0043001", "Terrassa"=>"0008004", "Teruel"=>"0044001", "Toledo"=>"0045001", "Tortosa"=>"0043003", "Tudela"=>"0031002", "Valencia"=>"0046001", "Valladolid"=>"0047001", "Vic"=>"0008009", "Vigo"=>"0036001", "Vizcaya"=>"0048001", "Zamora"=>"0049001", "Zaragoza"=>"0050280"}
offset = get_metadata("OFFSET",0)
provinces.each_with_index{|province,idx|
  next if idx < offset
  action(province.last)
  save_metadata("OFFSET",idx.next)

}
delete_metadata("OFFSET")
