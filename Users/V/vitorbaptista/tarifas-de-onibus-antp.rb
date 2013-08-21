DATAS = ['2005-06-01', '2006-09-01', '2006-12-01', '2007-05-01', '2007-09-01',
         '2008-01-01', '2008-04-01', '2008-07-01', '2008-10-01', '2009-01-01',
         '2009-04-01', '2009-07-01', '2009-10-01', '2010-01-01', '2010-04-01',
         '2010-07-01', '2010-10-01']

class Cidade
  attr_accessor :nome, :uf, :populacao, :tarifas

  def initialize(nodeset, datas)
    @nome = nodeset.shift.content
    @uf = nodeset.shift.content
    @populacao = nodeset.shift.content.to_i
    @tarifas = Hash.new
    tarifas = nodeset.collect { |node| node.content.gsub(",", ".").to_f if not node.content.nil? }
    tarifas.each_with_index { |tarifa, index|
      @tarifas[DATAS[index]] = tarifa
    }
  end

  def to_s
    "#{@nome} #{@uf} #{@populacao} #{@tarifas.join(' ')}"
  end
end

def str_to_date(str)
  mes, ano = str.split("_")

  mes = case mes
          when "jan"
            "01"
          when "fev"
            "02"
          when "mar"
            "03"
          when "abr"
            "04"
          when "mai"
            "05"
          when "jun"
            "06"
          when "jul"
            "07"
          when "ago"
            "08"
          when "set"
            "09"
          when "out"
            "10"
          when "nov"
            "11"
          when "dez"
            "12"
        end

  "20#{ano}-#{mes}-01"
end


html = ScraperWiki.scrape("http://portal1.antp.net/site/simob/Lists/trfs/tarifas.aspx")

require 'nokogiri'
doc = Nokogiri::HTML(html)
cidades = Array.new
datas = ''
doc.xpath("//div[@id='WebPartWPQ1']/table/tr").each_with_index  do |node, index|
  if index.zero? 
    datas = node.children[3..-1].collect { |child| str_to_date(child.content) }
    next
  end
  cidades << Cidade.new(node.children, datas)
end

cidades.each do |cidade|
  ScraperWiki.save('cidade', {'cidade' => cidade.nome, 'uf' => cidade.uf}.merge(cidade.tarifas)) 
end

