require 'open-uri'
require 'uri'
require 'nokogiri'
require 'digest/md5'

BASE_URL = 'http://votacoes.camarapoa.rs.gov.br/'

def wait!
  $wait ||= 10
  $wait > 600 ? $wait = 600 : $wait += 10
end

def presencas_da(votacao_detalhes, votacao, sessao)
  table = votacao_detalhes.css('table.list tr')
  table.shift # discarta header
  table.map {|tr| tr.text.split(/\n/)[0,3].map &:strip }.inject([]) do |a, e|
    a << {
      data_sessao: sessao[:data],
      tipo_sessao: sessao[:tipo],
      numero_sessao: sessao[:numero],

      horario_inicio_votacao: votacao[:horario_inicio],
      parlamentar: e[0],
      partido: e[1],
      voto: e[2],
    }
  end
end

def detalhes_da(votacao, sessao)
  votacao_detalhes = begin
    Nokogiri::HTML open(URI.join(BASE_URL, votacao[:detalhes_link]).to_s).read.force_encoding('UTF-8')
  rescue => e
    puts "Got exception #{e}, retrying in #{wait!}..."
    sleep $wait
    retry
  end

  text = votacao_detalhes.xpath('//div[@class="box no-box"]').text

  {
    sessao_uuid: sessao[:sessao_uuid],
    data: sessao[:data],
    horario_inicio: votacao[:horario],
    horario_encerramento: text.match(/Encerramento:\s+((\d{2}:?){3})/)[1],
    proposicao: votacao[:proposicao],
    tipo: votacao[:tipo],
    situacao: votacao[:situacao],
    item_pauta: text.match(/Item pauta:\s+([^\n]+)\n/)[1],
    ordem_dia: text.match(/Ordem dia:\s+([^\n]+) Resultado/)[1],
  }.tap do |votacao|
    data = presencas_da(votacao_detalhes, votacao, sessao)
    ScraperWiki::save_sqlite(%w[data_sessao tipo_sessao numero_sessao horario_inicio_votacao parlamentar], data, 'presencas')
  end
end

def votacoes_da(sessao, sessao_hash)
  tabela = sessao.css('table tr').map(&:text).reject {|x| x == "" }.map {|x| x.split(/\t\t/).map &:strip }
  detalhes_links = sessao.css('table tr a @href').map(&:text).uniq
  _ = tabela.shift # discarta headers

  i = 0
  votacoes = tabela.inject([]) do |a, e|
    a << {
      horario: e[0],
      proposicao: e[1],
      tipo: e[2],
      situacao: e[4],
      detalhes_link: detalhes_links[i].gsub(/parlamentares\?/, 'parlamentares_nome?')
    }
    i += 1
    a
  end

  Thread.new do
    data = votacoes.map {|votacao| detalhes_da votacao, sessao_hash }
    ScraperWiki::save_sqlite(%w[sessao_uuid horario_inicio], data, 'votacoes')
  end
end

def processa_sessao(link)
  sessao = begin
    Nokogiri::HTML open(URI.join(BASE_URL, link).to_s).read.force_encoding('UTF-8')
  rescue => e
    puts "Got exception #{e}, retrying in #{wait!}..."
    sleep $wait
    retry
  end

  titulo = sessao.css('#sessao_mais_recente').text.split(/\n/)[2].strip.split

  {
    sessao_uuid: Digest::MD5.hexdigest("#{titulo[0]}-#{titulo[4]}-#{titulo[2].gsub(/[^\d]/, '')}"),
    data: titulo[0],
    tipo: titulo[4],
    numero: titulo[2].gsub(/[^\d]/, ''),
  }.tap do |result|
    ScraperWiki::save_sqlite(%w[data tipo numero], result, 'sessoes')
    votacoes_da(sessao, result)
  end
end

def processa_sessoes(index)
  links = index.css('a.sessoes @href').map &:text

  links.map do |link|
    processa_sessao(link)
  end
end

def sessoes
  index = Nokogiri::HTML open(BASE_URL).read.force_encoding('UTF-8')
  threads = []

  threads << Thread.new { processa_sessoes(index.dup) }

  while next_link = index.css('a.next_page @href').first
    puts next_link.text
    index = begin
      Nokogiri::HTML open(URI.join(BASE_URL, next_link.text).to_s).read.force_encoding('UTF-8')
    rescue => e
      puts "Got exception #{e}, retrying in #{wait!}..."
      sleep $wait
      retry
    end

    threads << Thread.new { processa_sessoes(index.dup) }
  end

  threads.map(&:join)
end

sessoes
require 'open-uri'
require 'uri'
require 'nokogiri'
require 'digest/md5'

BASE_URL = 'http://votacoes.camarapoa.rs.gov.br/'

def wait!
  $wait ||= 10
  $wait > 600 ? $wait = 600 : $wait += 10
end

def presencas_da(votacao_detalhes, votacao, sessao)
  table = votacao_detalhes.css('table.list tr')
  table.shift # discarta header
  table.map {|tr| tr.text.split(/\n/)[0,3].map &:strip }.inject([]) do |a, e|
    a << {
      data_sessao: sessao[:data],
      tipo_sessao: sessao[:tipo],
      numero_sessao: sessao[:numero],

      horario_inicio_votacao: votacao[:horario_inicio],
      parlamentar: e[0],
      partido: e[1],
      voto: e[2],
    }
  end
end

def detalhes_da(votacao, sessao)
  votacao_detalhes = begin
    Nokogiri::HTML open(URI.join(BASE_URL, votacao[:detalhes_link]).to_s).read.force_encoding('UTF-8')
  rescue => e
    puts "Got exception #{e}, retrying in #{wait!}..."
    sleep $wait
    retry
  end

  text = votacao_detalhes.xpath('//div[@class="box no-box"]').text

  {
    sessao_uuid: sessao[:sessao_uuid],
    data: sessao[:data],
    horario_inicio: votacao[:horario],
    horario_encerramento: text.match(/Encerramento:\s+((\d{2}:?){3})/)[1],
    proposicao: votacao[:proposicao],
    tipo: votacao[:tipo],
    situacao: votacao[:situacao],
    item_pauta: text.match(/Item pauta:\s+([^\n]+)\n/)[1],
    ordem_dia: text.match(/Ordem dia:\s+([^\n]+) Resultado/)[1],
  }.tap do |votacao|
    data = presencas_da(votacao_detalhes, votacao, sessao)
    ScraperWiki::save_sqlite(%w[data_sessao tipo_sessao numero_sessao horario_inicio_votacao parlamentar], data, 'presencas')
  end
end

def votacoes_da(sessao, sessao_hash)
  tabela = sessao.css('table tr').map(&:text).reject {|x| x == "" }.map {|x| x.split(/\t\t/).map &:strip }
  detalhes_links = sessao.css('table tr a @href').map(&:text).uniq
  _ = tabela.shift # discarta headers

  i = 0
  votacoes = tabela.inject([]) do |a, e|
    a << {
      horario: e[0],
      proposicao: e[1],
      tipo: e[2],
      situacao: e[4],
      detalhes_link: detalhes_links[i].gsub(/parlamentares\?/, 'parlamentares_nome?')
    }
    i += 1
    a
  end

  Thread.new do
    data = votacoes.map {|votacao| detalhes_da votacao, sessao_hash }
    ScraperWiki::save_sqlite(%w[sessao_uuid horario_inicio], data, 'votacoes')
  end
end

def processa_sessao(link)
  sessao = begin
    Nokogiri::HTML open(URI.join(BASE_URL, link).to_s).read.force_encoding('UTF-8')
  rescue => e
    puts "Got exception #{e}, retrying in #{wait!}..."
    sleep $wait
    retry
  end

  titulo = sessao.css('#sessao_mais_recente').text.split(/\n/)[2].strip.split

  {
    sessao_uuid: Digest::MD5.hexdigest("#{titulo[0]}-#{titulo[4]}-#{titulo[2].gsub(/[^\d]/, '')}"),
    data: titulo[0],
    tipo: titulo[4],
    numero: titulo[2].gsub(/[^\d]/, ''),
  }.tap do |result|
    ScraperWiki::save_sqlite(%w[data tipo numero], result, 'sessoes')
    votacoes_da(sessao, result)
  end
end

def processa_sessoes(index)
  links = index.css('a.sessoes @href').map &:text

  links.map do |link|
    processa_sessao(link)
  end
end

def sessoes
  index = Nokogiri::HTML open(BASE_URL).read.force_encoding('UTF-8')
  threads = []

  threads << Thread.new { processa_sessoes(index.dup) }

  while next_link = index.css('a.next_page @href').first
    puts next_link.text
    index = begin
      Nokogiri::HTML open(URI.join(BASE_URL, next_link.text).to_s).read.force_encoding('UTF-8')
    rescue => e
      puts "Got exception #{e}, retrying in #{wait!}..."
      sleep $wait
      retry
    end

    threads << Thread.new { processa_sessoes(index.dup) }
  end

  threads.map(&:join)
end

sessoes
