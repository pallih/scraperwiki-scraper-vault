# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

  table = doc.xpath('/html/body/table//table')[1]

  # Note tr[1] is actually a table header
  table.xpath('tr[position() > 1]').each do |tr|
    fields = tr.xpath('td').map do |td|
      field = td.text 
      field.gsub!(/(?:\s|\xe3\x80\x80)+/, ' ') # Shrink spaces (\xe3... == full-width space)
      field.gsub!(/\s?$/, '')                  # Chop off trailing space
      field
    end
    jikoku, meigaracode, kaishamei, hyodai, xbrlumu, torihikijo, rireki _ = fields
    
#    name.gsub!(/.$/, '') # Chop off "-kun"

    result << {
      'jikoku'     => jikoku,
      'meigaracode' => meigaracode,
      'kaishamei'    => kaishamei,
      'hyodai' => hyodai,
      'xbrlumu' => xbrlumu,
      'torihikijo' => torihikijo,
      'rireki' => rireki
    }
  end

  result
end



urls = (1..10).map {|i| "https://www.release.tdnet.info/inbs/I_list_00#{i}_20120801.html" }

urls.each do |url|
  puts "Fetching #{url}"
  doc = Nokogiri::HTML.parse(open(url), 'Shift_JIS')
  data = parse_doc(doc)
  # (jikoku, meigaracode, kaishamei,) is not unique indeed
  ScraperWiki.save(['jikoku', 'meigaracode', 'kaishamei'], data)
end# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def parse_doc(doc)
  result = []

  table = doc.xpath('/html/body/table//table')[1]

  # Note tr[1] is actually a table header
  table.xpath('tr[position() > 1]').each do |tr|
    fields = tr.xpath('td').map do |td|
      field = td.text 
      field.gsub!(/(?:\s|\xe3\x80\x80)+/, ' ') # Shrink spaces (\xe3... == full-width space)
      field.gsub!(/\s?$/, '')                  # Chop off trailing space
      field
    end
    jikoku, meigaracode, kaishamei, hyodai, xbrlumu, torihikijo, rireki _ = fields
    
#    name.gsub!(/.$/, '') # Chop off "-kun"

    result << {
      'jikoku'     => jikoku,
      'meigaracode' => meigaracode,
      'kaishamei'    => kaishamei,
      'hyodai' => hyodai,
      'xbrlumu' => xbrlumu,
      'torihikijo' => torihikijo,
      'rireki' => rireki
    }
  end

  result
end



urls = (1..10).map {|i| "https://www.release.tdnet.info/inbs/I_list_00#{i}_20120801.html" }

urls.each do |url|
  puts "Fetching #{url}"
  doc = Nokogiri::HTML.parse(open(url), 'Shift_JIS')
  data = parse_doc(doc)
  # (jikoku, meigaracode, kaishamei,) is not unique indeed
  ScraperWiki.save(['jikoku', 'meigaracode', 'kaishamei'], data)
end