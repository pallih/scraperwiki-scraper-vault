require 'open-uri'
require 'nokogiri'
require 'uri'

class Vereadores

  MAIN_URL = 'http://www.camarapoa.rs.gov.br/frames/veread/acessor/veralf.htm'

  def perform
    data = rows.inject([]) do |a, e|
      if e[0]
        a << { nome: e[0], email: e[1], ramais: e[2], partido: e[3] }
      else
        a
      end
    end

    data.each do |row|
      fix_telefones_in row
      fix_links_in row
    end

    ScraperWiki::save_sqlite([:nome], data, 'vereadores')
  end

  def fix_links_in(row)
    nome, href = row.delete(:nome)
    row[:nome] = nome
    row[:href] = URI.join(MAIN_URL, href.to_s).to_s if href

    email, href = row.delete(:email)
    row[:email] = email
  end

  def fix_telefones_in(row)
    row.delete(:ramais).split('/').map {|r| "3220-#{r}" }.each_with_index do |tel, i|
      row[:"telefone_#{i}"] = tel
    end
  end

  def rows
    @rows ||= html.xpath('//table')[1].xpath('./tr').map do |tr|
      tr.xpath('.//td[@bgcolor="#FFFFFF"]').map do |td|
        text = td.text.split.join(' ')
        href = (td / 'a/@href').text

        if href.empty? 
          text
        else
          [ text, href ]
        end
      end
    end
  end

  def html
    @html ||= Nokogiri::HTML(raw_data)
  end

  def raw_data
    open(MAIN_URL)
  end

end

Vereadores.new.perform