# encoding: UTF-8
# https://scraperwiki.com/docs/ruby/ruby_datastore_guide/
require 'nokogiri'
require 'json'
require 'open-uri'
require 'uri'


def html_doc(url) 
  html = ScraperWiki::scrape(url)   
  html.force_encoding("UTF-8") 
  
  #doc = Nokogiri::HTML(html)  
  doc = Nokogiri::HTML(html, nil, 'ISO-8859-1')
  doc.encoding = 'UTF-8'
  doc
end
     
def get_imovel_info (id)
  url = "http://www.infoimoveis.com.br/pop_view.htm?id=#{id}"
  puts "tratando id = #{id} , #{url}"
  document = html_doc(url)
  nao_informado = 'nao informado'
  preco = '0,00' 

  begin
   #todo: nem todos tem preco!
    document.xpath('/html/body/table[2]/tr/td/table[5]/tr/td/b').each{|node|
    str = node.text().to_s
    preco = str if (str != 'Descrição do imóvel')
    }
    

  rescue
    print "error id={id}"
  end

  preco = preco.gsub("R$ ", "")

  nao_informado = 'nao informado'
  h = {'Descricao' => nao_informado, 'Área total' => nao_informado, 'Área construída' => nao_informado, 'Endereço' => nao_informado}
  h1 = {}
  document.xpath('/html/body/table[2]/tr/td/table[3]/tr[2]/td/table/tr').each do |node|
    k = node.css('.t_bege').text().sub(':', '')
    v = node.css('.t_marrom').text()
    k = "descricao" if k == ""
    h1[k] = v
  end
  
  h.merge!(h1)

  descricao = h['Descricao']
  finalidade = h['Finalidade']
  tipo = h['Tipo']
  cidade = h['Cidade']
  bairro = h['Bairro']
  endereco = h['Endereço']
  area_total = h['Área total'].gsub("m²","");
  area_construida = h['Área construída'].gsub("m²","");

  #informacoes
  #a = []
  #a = document.xpath('/html/body/table[2]/tr/td/table[5]/tr[2]/td/table/tr/td/img').map { |node| node.next.text() }  #informacoes 1
  #a << document.xpath('/html/body/table[2]/tr/td/table[5]/tr[2]/td/table/tr/td[2]/img').map { |node| node.next.text() }  #informacoes 2
  #print a.size.to_s
  #print a.to_s
  # -----
  
  details = {
     :id => id,
     :preco => preco, 
     :descricao => descricao,
     :finalidade => finalidade,
     :tipo => tipo,
     :cidade => cidade,
     :bairro => bairro,
     :endereco => endereco,
     :area_total => area_total,
     :area_construida => area_construida
  }

  #todo: se a finalidade for '', o registro do imovel foi removido
  print "details = #{details.to_s}"

  details
end


def get_imoveis (uf, cidade, finalidade, tipo)
    result = []
  pagina= 1
  while true do
    url = "http://www.infoimoveis.com.br/busca.htm?uf=#{uf}&finalidade=#{finalidade}&tipo=#{tipo}&cidade=#{cidade}&pagina=#{pagina}"
    document = html_doc(url)
    imoveis = document.xpath("//a[@data-id]")

    if imoveis.size > 0 
      pagina+= 1
      imoveis.each do |i|
        id = (i.attr "data-id")        
        result << id
      end
    else
      break
    end
  end
  
  #result.uniq
  result
end

def salva_imoveis(ids)
  ids.each do |e|  
    data = get_imovel_info(e)
    ScraperWiki::save_sqlite(['id', 'preco', 'descricao', 'finalidade', 'tipo', 'cidade', 
     'bairro', 'endereco', 'area_total', 'area_construida'], data, 'info_data');
  end
end  

def save_ids ids
  print "Inserindo #{ids.size} novos ID's"
  ids.each do |id|
    ScraperWiki::save_sqlite(['id'], {:id => id}, 'info_id');
  end
end


def get_ids_from_infoi
  cod_uf = 1  #ms
  cod_cidade = 1 #campo grande
  cod_finalidades = ['1', '2', '3']
  cod_tipos = ['15', '1', '14', '11', '2', '5', '6', '13', '4', '12']

  ids = []
  cod_finalidades.each do |f|
    cod_tipos.each do |t|
     ids += get_imoveis(cod_uf, cod_cidade, f, t)
    end
  end
  ids
end

def get_ids_teste
  get_imoveis(1, 1, 1, 1).each {|id| print "id=#{id} \n"}
end

def get_ids_novos
  ScraperWiki::select('ii.id from info_id ii left join info_data id on ii.id = id.id where id.id is null').map {|e| e['id'] }
end

def get_ids_from_datastore
  ScraperWiki::select('id from info_id').map {|e| e['id'] }
end

def scrap_ids 
  ids = get_ids_from_infoi
  ids_local = get_ids_from_datastore
  ids_novos = ids - ids_local
  save_ids ids_novos
end

def scrap_data(limit = -1)
  ids = get_ids_novos

  if limit != -1
   ids = ids.take(limit)
  end

  print "Processando #{ids.size} novos registros\n"
  salva_imoveis ids
end

def execute_sql(sql)
  ScraperWiki::sqliteexecute(sql);
  ScraperWiki::commit();
  print "command \"#{sql}\" executed with success. \n"
end

def format_data
 execute_sql "delete from info_data where finalidade = ''";
 #execute_sql "update info_data set preco = trim(replace(preco, 'R$', ''));"
 #execute_sql "update info_data set area_construida = trim(replace(area_construida, 'm²', ''));"
 #execute_sql "update info_data set area_total = trim(replace(area_total, 'm²', ''));"
 #execute_sql "update info_data set preco = '0,00' where preco like '%nao%' or preco = '0'";
end

def scrap_setup
  #execute_sql "alter table info_data add latitude varchar(15)"
  #execute_sql "alter table info_data add longitude varchar(15)"
  #execute_sql "alter table info_data add geo_status varchar(15)"
  #execute_sql "update info_data set geo_status = null"  # zero_results/ ok

end


def view_novos
 get_ids_novos.each{|id| print "http://www.infoimoveis.com.br/pop_view.htm?id=#{id}\n"}
end

# rodizio = ['ids', 'data', 'geocode']
def scrap_routine
 nxt = ScraperWiki::get_var('next') || 'ids'

 if (nxt == 'ids')
   ScraperWiki::save_var('next', 'data');
   scrap_ids 
 elsif (nxt == 'data')
   ScraperWiki::save_var('next', 'ids');
   scrap_data 1000
   #format_data
 end 
end


def quote_plus(str)
  URI.escape(str).split(' ').join('+')
end

def get_json(url)
  JSON.parse(open(url).read)
end

# get_geocode "Campo+Grande/MS Rua liberdade 990"
def get_geocode(address) 
  result = {:lat => 0, :lng => 0, :status => ""}
  url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+quote_plus(address)+'&sensor=false&output=json'
  resp = get_json(url)

  if resp 
    result["status"] = resp["status"] # == OVER_QUERY_LIMIT, ZERO_RESULTS

    if resp["status"] == "ok"
      location = resp['results'][0]['geometry']['location']
      result = {"lat" => location['lat'], "lng" => location['lng'], "status" => "ok"}
    end
  end

  result
end 

def process_geo_code
  # max of 2500 day
  ScraperWiki::select('id, endereco from info_data where geo_status is null limit 1').each do |data|
    id = data["id"]    
    full_address = 'Campo Grande/MS, ' + data['endereco']
    print "processig #{id} , #{full_address}\n"
    gcode = get_geocode(full_address) 
    print gcode.to_s
    geo_status = gcode["status"]

    if (geo_status == "ok")
      lat = gcode["lat"]
      lng = gcode["lng"]
      sql = "update info_data set latitude = \"#{lat}\", longitude=\"#{lng}\", geo_status=\"#{geo_status}\" where id = \"#{id}\""
      execute_sql(sql)
    elsif (geo_status == "ZERO_RESULTS")
      sql = "update info_data set geo_status=\"#{geo_status}\" where id = \"#{id}\""
      execute_sql(sql)
    else
      sql = nil
      break
    end

    
  end  
end


#scrap_setup
#format_data
scrap_routine
#scrap_ids 
#get_ids_teste
#scrap_data 1000
#view_novos
#process_geo_code

# encoding: UTF-8
# https://scraperwiki.com/docs/ruby/ruby_datastore_guide/
require 'nokogiri'
require 'json'
require 'open-uri'
require 'uri'


def html_doc(url) 
  html = ScraperWiki::scrape(url)   
  html.force_encoding("UTF-8") 
  
  #doc = Nokogiri::HTML(html)  
  doc = Nokogiri::HTML(html, nil, 'ISO-8859-1')
  doc.encoding = 'UTF-8'
  doc
end
     
def get_imovel_info (id)
  url = "http://www.infoimoveis.com.br/pop_view.htm?id=#{id}"
  puts "tratando id = #{id} , #{url}"
  document = html_doc(url)
  nao_informado = 'nao informado'
  preco = '0,00' 

  begin
   #todo: nem todos tem preco!
    document.xpath('/html/body/table[2]/tr/td/table[5]/tr/td/b').each{|node|
    str = node.text().to_s
    preco = str if (str != 'Descrição do imóvel')
    }
    

  rescue
    print "error id={id}"
  end

  preco = preco.gsub("R$ ", "")

  nao_informado = 'nao informado'
  h = {'Descricao' => nao_informado, 'Área total' => nao_informado, 'Área construída' => nao_informado, 'Endereço' => nao_informado}
  h1 = {}
  document.xpath('/html/body/table[2]/tr/td/table[3]/tr[2]/td/table/tr').each do |node|
    k = node.css('.t_bege').text().sub(':', '')
    v = node.css('.t_marrom').text()
    k = "descricao" if k == ""
    h1[k] = v
  end
  
  h.merge!(h1)

  descricao = h['Descricao']
  finalidade = h['Finalidade']
  tipo = h['Tipo']
  cidade = h['Cidade']
  bairro = h['Bairro']
  endereco = h['Endereço']
  area_total = h['Área total'].gsub("m²","");
  area_construida = h['Área construída'].gsub("m²","");

  #informacoes
  #a = []
  #a = document.xpath('/html/body/table[2]/tr/td/table[5]/tr[2]/td/table/tr/td/img').map { |node| node.next.text() }  #informacoes 1
  #a << document.xpath('/html/body/table[2]/tr/td/table[5]/tr[2]/td/table/tr/td[2]/img').map { |node| node.next.text() }  #informacoes 2
  #print a.size.to_s
  #print a.to_s
  # -----
  
  details = {
     :id => id,
     :preco => preco, 
     :descricao => descricao,
     :finalidade => finalidade,
     :tipo => tipo,
     :cidade => cidade,
     :bairro => bairro,
     :endereco => endereco,
     :area_total => area_total,
     :area_construida => area_construida
  }

  #todo: se a finalidade for '', o registro do imovel foi removido
  print "details = #{details.to_s}"

  details
end


def get_imoveis (uf, cidade, finalidade, tipo)
    result = []
  pagina= 1
  while true do
    url = "http://www.infoimoveis.com.br/busca.htm?uf=#{uf}&finalidade=#{finalidade}&tipo=#{tipo}&cidade=#{cidade}&pagina=#{pagina}"
    document = html_doc(url)
    imoveis = document.xpath("//a[@data-id]")

    if imoveis.size > 0 
      pagina+= 1
      imoveis.each do |i|
        id = (i.attr "data-id")        
        result << id
      end
    else
      break
    end
  end
  
  #result.uniq
  result
end

def salva_imoveis(ids)
  ids.each do |e|  
    data = get_imovel_info(e)
    ScraperWiki::save_sqlite(['id', 'preco', 'descricao', 'finalidade', 'tipo', 'cidade', 
     'bairro', 'endereco', 'area_total', 'area_construida'], data, 'info_data');
  end
end  

def save_ids ids
  print "Inserindo #{ids.size} novos ID's"
  ids.each do |id|
    ScraperWiki::save_sqlite(['id'], {:id => id}, 'info_id');
  end
end


def get_ids_from_infoi
  cod_uf = 1  #ms
  cod_cidade = 1 #campo grande
  cod_finalidades = ['1', '2', '3']
  cod_tipos = ['15', '1', '14', '11', '2', '5', '6', '13', '4', '12']

  ids = []
  cod_finalidades.each do |f|
    cod_tipos.each do |t|
     ids += get_imoveis(cod_uf, cod_cidade, f, t)
    end
  end
  ids
end

def get_ids_teste
  get_imoveis(1, 1, 1, 1).each {|id| print "id=#{id} \n"}
end

def get_ids_novos
  ScraperWiki::select('ii.id from info_id ii left join info_data id on ii.id = id.id where id.id is null').map {|e| e['id'] }
end

def get_ids_from_datastore
  ScraperWiki::select('id from info_id').map {|e| e['id'] }
end

def scrap_ids 
  ids = get_ids_from_infoi
  ids_local = get_ids_from_datastore
  ids_novos = ids - ids_local
  save_ids ids_novos
end

def scrap_data(limit = -1)
  ids = get_ids_novos

  if limit != -1
   ids = ids.take(limit)
  end

  print "Processando #{ids.size} novos registros\n"
  salva_imoveis ids
end

def execute_sql(sql)
  ScraperWiki::sqliteexecute(sql);
  ScraperWiki::commit();
  print "command \"#{sql}\" executed with success. \n"
end

def format_data
 execute_sql "delete from info_data where finalidade = ''";
 #execute_sql "update info_data set preco = trim(replace(preco, 'R$', ''));"
 #execute_sql "update info_data set area_construida = trim(replace(area_construida, 'm²', ''));"
 #execute_sql "update info_data set area_total = trim(replace(area_total, 'm²', ''));"
 #execute_sql "update info_data set preco = '0,00' where preco like '%nao%' or preco = '0'";
end

def scrap_setup
  #execute_sql "alter table info_data add latitude varchar(15)"
  #execute_sql "alter table info_data add longitude varchar(15)"
  #execute_sql "alter table info_data add geo_status varchar(15)"
  #execute_sql "update info_data set geo_status = null"  # zero_results/ ok

end


def view_novos
 get_ids_novos.each{|id| print "http://www.infoimoveis.com.br/pop_view.htm?id=#{id}\n"}
end

# rodizio = ['ids', 'data', 'geocode']
def scrap_routine
 nxt = ScraperWiki::get_var('next') || 'ids'

 if (nxt == 'ids')
   ScraperWiki::save_var('next', 'data');
   scrap_ids 
 elsif (nxt == 'data')
   ScraperWiki::save_var('next', 'ids');
   scrap_data 1000
   #format_data
 end 
end


def quote_plus(str)
  URI.escape(str).split(' ').join('+')
end

def get_json(url)
  JSON.parse(open(url).read)
end

# get_geocode "Campo+Grande/MS Rua liberdade 990"
def get_geocode(address) 
  result = {:lat => 0, :lng => 0, :status => ""}
  url = 'http://maps.googleapis.com/maps/api/geocode/json?address='+quote_plus(address)+'&sensor=false&output=json'
  resp = get_json(url)

  if resp 
    result["status"] = resp["status"] # == OVER_QUERY_LIMIT, ZERO_RESULTS

    if resp["status"] == "ok"
      location = resp['results'][0]['geometry']['location']
      result = {"lat" => location['lat'], "lng" => location['lng'], "status" => "ok"}
    end
  end

  result
end 

def process_geo_code
  # max of 2500 day
  ScraperWiki::select('id, endereco from info_data where geo_status is null limit 1').each do |data|
    id = data["id"]    
    full_address = 'Campo Grande/MS, ' + data['endereco']
    print "processig #{id} , #{full_address}\n"
    gcode = get_geocode(full_address) 
    print gcode.to_s
    geo_status = gcode["status"]

    if (geo_status == "ok")
      lat = gcode["lat"]
      lng = gcode["lng"]
      sql = "update info_data set latitude = \"#{lat}\", longitude=\"#{lng}\", geo_status=\"#{geo_status}\" where id = \"#{id}\""
      execute_sql(sql)
    elsif (geo_status == "ZERO_RESULTS")
      sql = "update info_data set geo_status=\"#{geo_status}\" where id = \"#{id}\""
      execute_sql(sql)
    else
      sql = nil
      break
    end

    
  end  
end


#scrap_setup
#format_data
scrap_routine
#scrap_ids 
#get_ids_teste
#scrap_data 1000
#view_novos
#process_geo_code

