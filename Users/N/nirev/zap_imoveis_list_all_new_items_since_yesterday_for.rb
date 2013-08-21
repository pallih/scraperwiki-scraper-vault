require 'rubygems'
require 'active_support/time'
require 'nokogiri' 

base_url = 'http://www.zap.com.br/imoveis/sao-paulo+sao-paulo+%s/apartamento-padrao/aluguel/?tipobusca=rapida&rangeValor=0-2300&foto=1&ord=dataatualizacao'
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
price_limit = 2300

if false
  ScraperWiki::sqliteexecute("CREATE TABLE `swdata` (`url` text, `data` text, `total` integer, `bairro` text, `rua` text, `area` text, `dorms` text, `aluguel` text, `cond` text, `iptu` text)")
end

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
    data['data'] = date_str
    
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
    data['total'] = 0
    ['aluguel', 'cond', 'iptu'].each {|x| data['total'] += data[x].split.last.gsub('.','').to_i if data[x]}
    end

    ScraperWiki::save_sqlite(['url'], data) if (data['total'] < price_limit)
  end
end
