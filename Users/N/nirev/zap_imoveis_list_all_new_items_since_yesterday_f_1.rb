require 'rubygems'
require 'active_support/time'
require 'nokogiri' 

base_url = 'http://www.zap.com.br/imoveis/sao-paulo+sao-paulo+%s/casa-padrao/aluguel/?tipobusca=rapida&rangeValor=0-1700&foto=1&ord=dataatualizacao'
bairros = [
            'vl-mariana', 
            'vl-madalena', 
            'saude',
            'jardins',
            'paraiso',
            'vl-clementino',
            'pc-da-arvore',
            'perdizes',
            'pinheiros',
            'sumare',
            'sumarezinho'
          ]

datelimit = Date.today - 1.days

bairros.each do |bairro|
  url = base_url % bairro
  
  html = ScraperWiki::scrape(url)
  doc = Nokogiri::HTML(html, nil, 'ISO-8859-1')
  page = 1

  doc.css('.itemOf').each do |item|
    date_str = item.css('div.itemData span').text.strip.split.last
    date = Date.strptime date_str, '%d/%m/%Y'
    break if date < datelimit
    
    data = {}
    data['url'] = item.at_css('div.full a')['href']
    data['bairro'] = bairro
    data['data'] = date.to_s
    
    itempage = Nokogiri::HTML(ScraperWiki::scrape(data['url']), nil, 'ISO-8859-1')
    data['rua'] = itempage.at_css('span.street-address').text if itempage.at_css('span.street-address')
    itempage.css('ul.fc-detalhes li').each do |attr|
      case attr.css('span').first
        when /dormit.rios/
          data['dorms'] = attr.css('span').last.text.split.first
        when /.rea.*til/
          data['area'] = attr.css('span').last.text.gsub(/\s+/, "")
        when /condom.*/
          data['cond'] = attr.css('span').last.text.strip
        when /IPTU.*/
          data['iptu'] = attr.css('span').last.text.strip
        when /pre.* de aluguel.*/
          data['aluguel'] = attr.css('span').last.text.strip
      end
    end
    data['total'] = 0
    ['aluguel', 'cond', 'iptu'].each {|x| data['total'] += data[x].split.last.gsub('.', '').to_i if data[x]}
    ScraperWiki::save_sqlite(['url'], data)
  end
end
require 'rubygems'
require 'active_support/time'
require 'nokogiri' 

base_url = 'http://www.zap.com.br/imoveis/sao-paulo+sao-paulo+%s/casa-padrao/aluguel/?tipobusca=rapida&rangeValor=0-1700&foto=1&ord=dataatualizacao'
bairros = [
            'vl-mariana', 
            'vl-madalena', 
            'saude',
            'jardins',
            'paraiso',
            'vl-clementino',
            'pc-da-arvore',
            'perdizes',
            'pinheiros',
            'sumare',
            'sumarezinho'
          ]

datelimit = Date.today - 1.days

bairros.each do |bairro|
  url = base_url % bairro
  
  html = ScraperWiki::scrape(url)
  doc = Nokogiri::HTML(html, nil, 'ISO-8859-1')
  page = 1

  doc.css('.itemOf').each do |item|
    date_str = item.css('div.itemData span').text.strip.split.last
    date = Date.strptime date_str, '%d/%m/%Y'
    break if date < datelimit
    
    data = {}
    data['url'] = item.at_css('div.full a')['href']
    data['bairro'] = bairro
    data['data'] = date.to_s
    
    itempage = Nokogiri::HTML(ScraperWiki::scrape(data['url']), nil, 'ISO-8859-1')
    data['rua'] = itempage.at_css('span.street-address').text if itempage.at_css('span.street-address')
    itempage.css('ul.fc-detalhes li').each do |attr|
      case attr.css('span').first
        when /dormit.rios/
          data['dorms'] = attr.css('span').last.text.split.first
        when /.rea.*til/
          data['area'] = attr.css('span').last.text.gsub(/\s+/, "")
        when /condom.*/
          data['cond'] = attr.css('span').last.text.strip
        when /IPTU.*/
          data['iptu'] = attr.css('span').last.text.strip
        when /pre.* de aluguel.*/
          data['aluguel'] = attr.css('span').last.text.strip
      end
    end
    data['total'] = 0
    ['aluguel', 'cond', 'iptu'].each {|x| data['total'] += data[x].split.last.gsub('.', '').to_i if data[x]}
    ScraperWiki::save_sqlite(['url'], data)
  end
end
