require 'rubygems'
require 'mechanize'
require 'json'
require 'nokogiri'
require 'pp'

BASE_URL='http://www.nrsr.sk/web/Default.aspx?sid=poslanci/ospravedlnenia_result'

BASE_CAL_URL='http://www.nrsr.sk/web/Services/CalendarService.asmx/RenderCalendar?month=10&year=2011&app="nrdvp"&lang=""'


@agent = Mechanize.new { |agent|
  agent.user_agent_alias = 'Mac Safari'
}

def excuse_url(m)
  (1..5).each { |meeting_num|
    yield :name => m[:name],
          :url => "http://www.nrsr.sk/web/Default.aspx?sid=poslanci/ospravedlnenia_result&PoslanecMasterID="+m[:id]+
            "&CisObdobia=#{meeting_num}&DatumOd=1900-1-1%200:0:0&DatumDo=2100-1-1%200:0:0&CisSchodze="
  }
end

def mop_list
  list = []
  @agent.get(BASE_URL) do |page|
    page.at('div#_sectionLayoutContainer__panelContent').search('select#_sectionLayoutContainer_ctl00_PoslanecMasterID option').each do |opt|
      next if opt.attr('value') == '-1'
      yield :id => opt.attr('value'), :name => opt.text
    end
  end
  list
end

def list_excuses
  mop_list do |mop|
    excuse_url(mop) do |url|
      @agent.get(url[:url]) do |page|
        next unless page.at('table.tab_zoznam')
        page.at('table.tab_zoznam').search('tr').each do |r|
          next if r.attr('class') == 'tab_zoznam_header'
          yield :name => url[:name], :date => r.search('td')[2].text.strip, :party => r.search('td')[1].text.strip, :reason => r.search('td')[3].text.strip
        end
      end
    end
  end
end

def make_uuid(i)
  { :unique_id => "#{i[:name].downcase.gsub(/\W/, '-')}-#{i[:date].gsub(/(\W|\.)/, '-')}" }
end

list_excuses do |item|
  pp item.merge(make_uuid(item))
  ScraperWiki.save(['unique_id'],  item.merge(make_uuid(item)))
end
