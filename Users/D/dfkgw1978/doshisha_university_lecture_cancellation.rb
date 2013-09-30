# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def find_target_table(doc)
  tables = doc.xpath('/html/body//table//table')
  i = 0
  while i < tables.size
    s = tables[i].inner_text.strip.encode('utf-8').gsub(/[\s　]/, '')
    break if s =~ /科目名教員名/
    i += 1
  end
  tables[i]
end 

def parse_doc(doc)
  result = []

  table = find_target_table(doc)
  table.css('tr')[1..-1].each do |tr|
    subject, teacher, reason = tr.css('td').map{|td|td.inner_text}
    puts subject
    result << {
      'subject' => subject,
      'teacher' => teacher,
      'reason' => reason
    }
  end
  result
end


url = "http://duet.doshisha.ac.jp/info/KK1000.jsp?katei=1&youbi=1&kouchi=2"
puts "Fetching #{url}"
doc = Nokogiri::HTML.parse(open(url))
data = parse_doc(doc)
ScraperWiki.save(['subject', 'teacher'], data)
# -*- coding: utf-8 -*-

require 'rubygems'
require 'open-uri'
require 'nokogiri'

if RUBY_VERSION < '1.9.0'
  $KCODE = 'UTF8'
end

def find_target_table(doc)
  tables = doc.xpath('/html/body//table//table')
  i = 0
  while i < tables.size
    s = tables[i].inner_text.strip.encode('utf-8').gsub(/[\s　]/, '')
    break if s =~ /科目名教員名/
    i += 1
  end
  tables[i]
end 

def parse_doc(doc)
  result = []

  table = find_target_table(doc)
  table.css('tr')[1..-1].each do |tr|
    subject, teacher, reason = tr.css('td').map{|td|td.inner_text}
    puts subject
    result << {
      'subject' => subject,
      'teacher' => teacher,
      'reason' => reason
    }
  end
  result
end


url = "http://duet.doshisha.ac.jp/info/KK1000.jsp?katei=1&youbi=1&kouchi=2"
puts "Fetching #{url}"
doc = Nokogiri::HTML.parse(open(url))
data = parse_doc(doc)
ScraperWiki.save(['subject', 'teacher'], data)
