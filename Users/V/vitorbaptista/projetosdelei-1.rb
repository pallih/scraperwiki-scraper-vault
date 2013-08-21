###############################################################################
# projetosdelei.com.br
###############################################################################

require 'nokogiri'

BASE_URL = 'http://www.projetosdelei.com.br/setor/'
CATEGORIAS = {'Agricultura' => 'agricult', 'Assistência Social' => 'ass_social',
              'Criança e Adolescente' => 'crianca', 'Deficientes' => 'deficient',
              'Educação e Cultura' => 'educult', 'Entidades' => 'entidad',
              'Esportes/Lazer/Turismo' => 'esplaztur', 'Idoso' => 'idoso',
              'Indústria e Comércio' => 'indcom', 'Legislação' => 'legislac',
              'Meio Ambiente' => 'meioamb', 'Mulher' => 'mulher',
              'Obras' => 'obras', 'Saúde' => 'saude', 'Segurança' => 'seguranc',
              'Trabalho' => 'trabalho', 'Transporte' => 'transport',
              'Tributação' => 'tributac', 'Temas Diversos' => 'temasdiv',
              'Projetos de Resoluções' => 'presoluc'}

# raspando cada categoria
CATEGORIAS.each_pair { |key, page|
  url = "#{BASE_URL}#{page}.shtml"
  puts url
  # o html tem várias tags <html> e </html>. Nós as tiramos.
  html_malformatted = ScraperWiki.scrape(url)
  html = "<html>#{html_malformatted.gsub(/<\/?html>/, '')}</html>"

  # variável de controle, usada para saber se a linha atual é
  # um código ou não
  codigo = false

  doc = Nokogiri::HTML(html)
  doc.search('//tr[@valign="TOP"]/td/text()').each do |content|
    content = content.to_s.strip
    
    if codigo
      # tirando . e \n do nome do projeto
      nome = content.gsub(".", "").gsub("\n", "").gsub(/  +/, " ").gsub("\302\223", '"').gsub("\302\224", '"')

      ScraperWiki.save(['id'], {'categoria' => key, 'id' => codigo, 'nome' => nome})

      codigo = false
    else
      codigo = content.to_i
    end
  end
}