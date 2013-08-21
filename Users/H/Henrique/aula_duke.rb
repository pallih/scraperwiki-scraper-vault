# biblioteca que irá passar os dados
require 'nokogiri'

#definindo primeiro alvo
primeiro_alvo = "http://www.marxists.org/archive/peng/1982/oncubavswp.htm"

# armazenar o conteúdo do primeiro alvo
tema = ScraperWiki.scrape(primeiro_alvo)

#parser do conteúdo
parser = Nokogiri::HTML(tema)

#criando um container temporario para os dados
dados_para_serem_salvos = {}

#armazenando titulo
dados_para_serem_salvos["titulo"] = parser.search("h4")[0].text

#armazenando conteudo
dados_para_serem_salvos["conteudo"] = parser.search("p").text

#armazenando links
dados_para_serem_salvos["links"] = parser.search("a")

#salvando no banco de dados
ScraperWiki.save(["titulo"], dados_para_serem_salvos)



segundo_alvo = "http://www.realcubablog.com/post/2011/02/09/WikiLeaks-Us-opinion-about-Cubas-economy-and-Rauls-reforms.aspx"
segundo_tema = ScraperWiki.scrape(segundo_alvo)
parser = Nokogiri::HTML(segundo_tema)
dados_para_serem_salvos = {}
dados_para_serem_salvos["titulo"] = parser.search("div#post0 h1").text
dados_para_serem_salvos["conteudo"] = parser.search("div#post0 div.text").text
dados_para_serem_salvos["link"] = parser.search("div#post0 h1 a.taggedlink").attr("href")
ScraperWiki.save(["titulo"], dados_para_serem_salvos) 


