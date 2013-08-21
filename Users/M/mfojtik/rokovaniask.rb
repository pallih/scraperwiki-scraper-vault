require 'rubygems'
require 'mechanize'
require 'nokogiri'

BASE_URL="http://www.rokovania.sk/Rokovanie.aspx"

@agent = Mechanize.new { |agent|
  agent.user_agent_alias = 'Mac Safari'
}

def is_header?(div)
  div.attr('class') and div.attr('class').text.script == 'categoryMaterial'
end

def parse_program(materials)
  materials.at('div#contentDR').search('div div span.column_r a').collect do |material_name|
    next if is_header? material_name.parent.parent
    { 
      :title => material_name.text.strip,
      :unique_id => material_name.parent.parent.search('span.column_r')[2].text.strip,
      :proposed_by => material_name.parent.parent.search('span.column_r')[4].text.strip,
      :status => material_name.parent.parent.search('span.column_r')[6].text.strip,
    }
  end
end

def scrap_list
  @agent.get(BASE_URL) do |page|
    page.at('div#rokovanie table.grid').search('tbody tr').each do |r|
      rokovanie = {
        :agenda_num => r.search('td')[0].text.strip.to_i.to_s,
        :date => r.search('td')[2].text.strip
      }
      @agent.get(r.search('td')[3].search('div a').attr('href').text) do |program|
        yield rokovanie.merge(:materials => parse_program(program))
      end
    end
  end
end

scrap_list do |list_item|
  meta_data = {:date => list_item[:date], :num => list_item[:num]}
  list_item[:materials].each do |material|
    ScraperWiki.save(['unique_id'], material.merge(meta_data))
  end
end
