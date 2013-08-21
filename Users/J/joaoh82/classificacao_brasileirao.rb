# Blank Ruby

require 'nokogiri'           
html = ScraperWiki::scrape("http://globoesporte.globo.com/futebol/brasileirao-serie-a/#/classificacao-e-jogos")
doc = Nokogiri::HTML(html)

p html

el = doc.css("tr.linha-classificacao td.coluna-p div")[0]
puts el