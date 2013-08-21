# http://ironmanlanzarote.com/index.php?option=com_docman&task=doc_download&gid=72

require 'pdf-reader'
require 'open-uri'

class String
  def escape_single_quotes
    self.gsub(/'/, "\\\\'")
  end
end

class PageTextReceiver
  attr_accessor :content

  def initialize
    @content = []
  end

  # Called when page parsing starts
  def begin_page(arg = nil)
    @content << ""
  end

  # record text that is drawn on the page
  def show_text(string, *params)
    @content.last << string
  end

  # there's a few text callbacks, so make sure we process them all
  alias :super_show_text :show_text
  alias :move_to_next_line_and_show_text :show_text
  alias :set_spacing_next_line_show_text :show_text

  # this final text callback takes slightly different arguments
  def show_text_with_positioning(*params)
    params = params.first
    params.each { |str| show_text(str) if str.kind_of?(String)}
  end
end

pdf = open('http://ironmanlanzarote.com/index.php?option=com_docman&task=doc_download&gid=72')

receiver = PageTextReceiver.new
pdf_reader = PDF::Reader.new

pdf_reader.parse(pdf, receiver)
men = receiver.content.inject("") do |result, element|
  result + element
end

place=1
mensql = men.scan(/(\d+?)(\D+?)(\w{3})(\w{3}|\d{2}-\d{2})\d+?(\d{2}:\d{2}:\d{2})(\d{2}:\d{2})\d+?(\d{2}:\d{2}:\d{2})(\d{2}:\d{2})\d+?(\d{2}:\d{2}:\d{2})(\d{2}:\d{2}:\d{2})/).inject("") do |result, element|
  bib = element[0].sub!(place.to_s, '')
  name = element[1].escape_single_quotes
  country = element[2]
  agegroup = element[3]
  swim = element[4]
  t1 = "00:#{element[5]}"
  bike = element[6]
  t2 = "00:#{element[7]}"
  run = element[8]
  total = element[9]
  #result[place] = {:name => name, :country => country, :agegroup => agegroup, :swim => swim, :t1 => t1, :bike => bike, :t2 => t2, :run => run, :total => total}
  place += 1
  sql = "result_id = DB[:results].insert(:race_id => race_id, :bib => #{bib}, :name => '#{name}', :country => '#{country}', :agegroup => '#{agegroup}')\n"
  sql << "DB[:legs].insert(:result_id => result_id, :type => 'swim', :order => 1, :time => '#{swim}')\n"
  sql << "DB[:legs].insert(:result_id => result_id, :type => 't1', :order => 2, :time => '#{t1}')\n"
  sql << "DB[:legs].insert(:result_id => result_id, :type => 'bike', :order => 3, :time => '#{bike}')\n"
  sql << "DB[:legs].insert(:result_id => result_id, :type => 't2', :order => 4, :time => '#{t2}')\n"
  sql << "DB[:legs].insert(:result_id => result_id, :type => 'run', :order => 5, :time => '#{run}')\n"
  result + sql
end

puts mensql
