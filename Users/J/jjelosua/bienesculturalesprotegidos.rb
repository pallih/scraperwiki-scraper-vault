# encoding: utf-8
require 'mechanize'
TOTAL = 16146
COOKIE_URL = 'http://www.mcu.es/patrimonio/CE/BienesCulturales.html'
FORM_URL = 'http://www.mcu.es/bienes/cargarFiltroBienesInmuebles.do?layout=bienesInmuebles&cache=init&language=es'
DETAIL_URL = 'http://www.mcu.es/bienes/buscarDetalleBienesInmuebles.do?'\
             'language=es&prev_layout=bienesInmueblesResultado&layout=bienesInmueblesDetalle&brscgi_DOCN='

#method to determine if the field is needed in DB
def save_field(header)
  if (header =~ /^(Bien|Comunidad Autónoma|Provincia|Municipio|Categoría|Fecha de Incoación|Fecha de Declaración):\s*$/)
    return true
  else
    return false
  end
end

#Create the mechanize agent
agent = Mechanize.new { |agent| agent.user_agent_alias = 'Mac Safari'}

#First we obtain the session cookie needed for the following scraping process
agent.get(COOKIE_URL)
formPage = agent.get(FORM_URL)

# get the form
form = formPage.form_with(:id => "busquedaBienesInmueblesForm")
# get the button you want from the form
button = form.button_with(:value => "Buscar")
# submit the form using that button
agent.submit(form, button)
#Get the stored variable in case the run has been cutted out
start = ScraperWiki::get_var("index",1)
puts start
for i in start..TOTAL
  begin
    doc_num = "%09d" % (i)
    url = "#{DETAIL_URL}#{doc_num}"
    detailPage = agent.get(url)
    nokogiriDoc= detailPage.parser
    table = nokogiriDoc.css('div#fichaSinPest table')
    rows = table.css('tr')
    data = {}
    data["id"] = doc_num
    for j in 0..rows.length()-1
      header = rows[j].css('th').text
      if save_field(header)
        header.gsub!(/:\s*$/,"")
        data[header] = rows[j].css('td').text.strip
      end
    end
    ScraperWiki::save_sqlite(['id'], data)
    sleep(1)
  rescue Exception => ex
    ScraperWiki::save_var("index", i)
  end
end

# encoding: utf-8
require 'mechanize'
TOTAL = 16146
COOKIE_URL = 'http://www.mcu.es/patrimonio/CE/BienesCulturales.html'
FORM_URL = 'http://www.mcu.es/bienes/cargarFiltroBienesInmuebles.do?layout=bienesInmuebles&cache=init&language=es'
DETAIL_URL = 'http://www.mcu.es/bienes/buscarDetalleBienesInmuebles.do?'\
             'language=es&prev_layout=bienesInmueblesResultado&layout=bienesInmueblesDetalle&brscgi_DOCN='

#method to determine if the field is needed in DB
def save_field(header)
  if (header =~ /^(Bien|Comunidad Autónoma|Provincia|Municipio|Categoría|Fecha de Incoación|Fecha de Declaración):\s*$/)
    return true
  else
    return false
  end
end

#Create the mechanize agent
agent = Mechanize.new { |agent| agent.user_agent_alias = 'Mac Safari'}

#First we obtain the session cookie needed for the following scraping process
agent.get(COOKIE_URL)
formPage = agent.get(FORM_URL)

# get the form
form = formPage.form_with(:id => "busquedaBienesInmueblesForm")
# get the button you want from the form
button = form.button_with(:value => "Buscar")
# submit the form using that button
agent.submit(form, button)
#Get the stored variable in case the run has been cutted out
start = ScraperWiki::get_var("index",1)
puts start
for i in start..TOTAL
  begin
    doc_num = "%09d" % (i)
    url = "#{DETAIL_URL}#{doc_num}"
    detailPage = agent.get(url)
    nokogiriDoc= detailPage.parser
    table = nokogiriDoc.css('div#fichaSinPest table')
    rows = table.css('tr')
    data = {}
    data["id"] = doc_num
    for j in 0..rows.length()-1
      header = rows[j].css('th').text
      if save_field(header)
        header.gsub!(/:\s*$/,"")
        data[header] = rows[j].css('td').text.strip
      end
    end
    ScraperWiki::save_sqlite(['id'], data)
    sleep(1)
  rescue Exception => ex
    ScraperWiki::save_var("index", i)
  end
end

