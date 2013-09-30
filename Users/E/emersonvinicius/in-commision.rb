require 'nokogiri'

mdc = SW_MetadataClient.new
mdc.save('data_columns', ['project_name', 'stoped_day', 'last_stopped', 'last_commission']) 


#adicione no array o id das matérias para acompanhamento
ids = [96674, 81614]

URL_SENADO = "http://www.senado.gov.br/atividade/materia/"

def date(date)
  date = date.split("/")
  Date.new(date[2].to_i, date[1].to_i, date[0].to_i)
end


def save_project(id)
  
  stoped = 0
  tramitacoes = []

  sort = "&p_sort2=D&cmd=sort&p_sort=DESC"


  html = ScraperWiki.scrape(URL_SENADO + "detalhes.asp?p_cod_mate=#{id}#{sort}")
  target = "//*[@id='DIV_TRAMITACAO']/form/div/div/div/div/div[3]/div"
  
  parser = Nokogiri::HTML(html)
  container = parser.search(target)
  
  name = parser.search(".titulocaixa_abas").first.text

  container.each_with_index do |data, i|
  
    tramitacao = {}
    tramitacao['date']  = (data/"div[1]/div[1]").first.text
    #"

    tramitacao['commision'] = (data/"div[1]/div[2]").first.text
    #"

    current_date = date(tramitacao['date'])
    previous_date = current_date
  
    if tramitacoes[i-1]
      previous_date = date(tramitacoes[i-1]['date'])
    end
  
    stoped += previous_date - current_date
    
    tramitacoes << tramitacao
  end
  
  _last_stopped = date(tramitacoes.first['date'])
  _now = date("#{Time.now.day}/#{Time.now.month}/#{Time.now.year}")
  
  last_stopped = _now - _last_stopped 

  project = {}
  project['id'] = id
  project['project_name'] = name
  project['stoped_day'] = stoped
  project['last_stopped'] =  last_stopped
  project['last_commission'] = tramitacoes.first['commision']
  
  ScraperWiki.save(['id'], project)
end

ids.each do |id|
  save_project(id)
endrequire 'nokogiri'

mdc = SW_MetadataClient.new
mdc.save('data_columns', ['project_name', 'stoped_day', 'last_stopped', 'last_commission']) 


#adicione no array o id das matérias para acompanhamento
ids = [96674, 81614]

URL_SENADO = "http://www.senado.gov.br/atividade/materia/"

def date(date)
  date = date.split("/")
  Date.new(date[2].to_i, date[1].to_i, date[0].to_i)
end


def save_project(id)
  
  stoped = 0
  tramitacoes = []

  sort = "&p_sort2=D&cmd=sort&p_sort=DESC"


  html = ScraperWiki.scrape(URL_SENADO + "detalhes.asp?p_cod_mate=#{id}#{sort}")
  target = "//*[@id='DIV_TRAMITACAO']/form/div/div/div/div/div[3]/div"
  
  parser = Nokogiri::HTML(html)
  container = parser.search(target)
  
  name = parser.search(".titulocaixa_abas").first.text

  container.each_with_index do |data, i|
  
    tramitacao = {}
    tramitacao['date']  = (data/"div[1]/div[1]").first.text
    #"

    tramitacao['commision'] = (data/"div[1]/div[2]").first.text
    #"

    current_date = date(tramitacao['date'])
    previous_date = current_date
  
    if tramitacoes[i-1]
      previous_date = date(tramitacoes[i-1]['date'])
    end
  
    stoped += previous_date - current_date
    
    tramitacoes << tramitacao
  end
  
  _last_stopped = date(tramitacoes.first['date'])
  _now = date("#{Time.now.day}/#{Time.now.month}/#{Time.now.year}")
  
  last_stopped = _now - _last_stopped 

  project = {}
  project['id'] = id
  project['project_name'] = name
  project['stoped_day'] = stoped
  project['last_stopped'] =  last_stopped
  project['last_commission'] = tramitacoes.first['commision']
  
  ScraperWiki.save(['id'], project)
end

ids.each do |id|
  save_project(id)
end