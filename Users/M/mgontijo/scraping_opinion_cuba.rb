# requerendo a biblioteca que irá parsear os dados
require 'nokogiri'
# definir o alvo
primeiro_alvo = "http://www.marxists.org/archive/peng/1982/oncubavswp.htm"
# armazenar conteudo do primeiro_alvo
tema= ScraperWiki.scrape(primeiro_alvo)
#parsear conteudo
parser=Nokogiri::HTML(tema)
#criando container temporario
dadosparasersalvos={}
dadosparasersalvos["titulo"]=parser.search("h4")[0].text
#armazenando título
dadosparasersalvos["conteudo"]=parser.search("p")
dadosparasersalvos["links"]=parser.search("a")
#verificar
#titulos= [0 => "titulo1", 1=. "titulo2", 2=> "titulo3"]

#salvando no banc=o de dados
ScraperWiki.save(["titulo"],dadosparasersalvos)

segundo_alvo="http://www.realcubablog.com/post/2011/02/09/WikiLeaks-US-opinion-about-Cubas-economy-and-Rauls-reforms.aspx"
segundo_tema= ScraperWiki.scrape(segundo_alvo)
parser=Nokogiri::HTML(segundo_tema)
dadosparasersalvos={}
dadosparasersalvos["titulo"]=parser.search("div#post0 h1").text
puts dadosparasersalvos["titulo"]
dadosparasersalvos["conteudo"]=parser.search("div#post0 div.text p").text
dadosparasersalvos["links"]=parser.search("div#content a")
puts dadosparasersalvos["links"]
ScraperWiki.save(["titulo"],dadosparasersalvos)