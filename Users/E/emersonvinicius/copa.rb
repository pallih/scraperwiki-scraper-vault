# encoding: utf-8

require 'nokogiri'
Encoding.default_internal = 'UTF-8'
class Copa
  URL_BASE = "http://www.copatransparente.gov.br/portalCopa"
  
  def parser(url)
     Nokogiri::HTML ScraperWiki.scrape(url)
  end
  
  def clear_field(value)
    value.gsub /^\s*|\s*$/, ''
  end
end

class Action < Copa  
  def initialize(id)
    @id = id
    search_field
  end
  
  def action_url
    "#{URL_BASE}/acoes/#{@id}" 
  end
  
  def type
    clear_field @data.search("#parent-fieldname-tipo").text
  end

  protected
  
  def search_field
    scraper = parser(action_url)
    @data = scraper.search(".field")
  end
   
end

def test(value, expected)
  if value == expected
    return "[passed] '#{value}' is equal '#{expected}'"
  else
    return "[falied] '#{value}' isnt equal '#{expected}'"
  end
  
end

# http://www.copatransparente.gov.br/portalCopa/acoes/estadio-nacional-de-brasilia-obras-civis
# http://www.copatransparente.gov.br/portalCopa/acoes/sistema-scats-av.-antonio-carlos-belo-horizonte

estadio_brasilia = Action.new("estadio-nacional-de-brasilia-obras-civis")
puts test(estadio_brasilia.type, "Obras / Serviços de engenharia")
puts test(estadio_brasilia.justification, "")# encoding: utf-8

require 'nokogiri'
Encoding.default_internal = 'UTF-8'
class Copa
  URL_BASE = "http://www.copatransparente.gov.br/portalCopa"
  
  def parser(url)
     Nokogiri::HTML ScraperWiki.scrape(url)
  end
  
  def clear_field(value)
    value.gsub /^\s*|\s*$/, ''
  end
end

class Action < Copa  
  def initialize(id)
    @id = id
    search_field
  end
  
  def action_url
    "#{URL_BASE}/acoes/#{@id}" 
  end
  
  def type
    clear_field @data.search("#parent-fieldname-tipo").text
  end

  protected
  
  def search_field
    scraper = parser(action_url)
    @data = scraper.search(".field")
  end
   
end

def test(value, expected)
  if value == expected
    return "[passed] '#{value}' is equal '#{expected}'"
  else
    return "[falied] '#{value}' isnt equal '#{expected}'"
  end
  
end

# http://www.copatransparente.gov.br/portalCopa/acoes/estadio-nacional-de-brasilia-obras-civis
# http://www.copatransparente.gov.br/portalCopa/acoes/sistema-scats-av.-antonio-carlos-belo-horizonte

estadio_brasilia = Action.new("estadio-nacional-de-brasilia-obras-civis")
puts test(estadio_brasilia.type, "Obras / Serviços de engenharia")
puts test(estadio_brasilia.justification, "")