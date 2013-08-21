# encoding: UTF-8
require 'mechanize'
require 'nokogiri'

#KY="27cedd1f8bd73bcfca715cb8eb0500d813e4b5d2" # S
#KY="43672daa5983e218e41281f06f8e28eb207cd4b0" # M
KY="c6cbf833716dc7760eb83507a858e278b5e84264" #A_B

@convs = {}

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    raise e unless e.inspect =~ /no such table/i    
  end
end
def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   raise e unless e.inspect =~ /no such table/i
  end
end
def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   raise e unless e.inspect =~ /no such table/i
  end
end


class String
  def pretty
    self.gsub(/\s+/,' ').strip
  end
end

def i_text(str,ign)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      tmp << a_text(st)
    } unless str.name =~ /"script"|#{ign}/
    ret << tmp
  elsif str.kind_of? (Nokogiri::XML::NodeSet)
    str.collect().each{|st|
      ret << a_text(st)
    }
  elsif str.kind_of? (Nokogiri::XML::Text)
    ret << s_text(str)
  end
  return ret.flatten
end

def a_text(str)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      tmp << a_text(st)
    } unless str.name == "script"
    ret << tmp
  elsif str.kind_of? (Nokogiri::XML::NodeSet)
    str.collect().each{|st|
      ret << a_text(st)
    }
  elsif str.kind_of? (Nokogiri::XML::Text)
    ret << s_text(str)
  end
  return ret.flatten
end

def s_text(str)
  return str.text.strip.gsub(/\u00A0/,' ').pretty
end

def c_text(str,con)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      tmp << c_text(st,con)
    }
    ret << tmp
  elsif str.kind_of? (Nokogiri::XML::NodeSet)
    str.collect().each{|st|
      break if st.name =~ /#{con}/
      ret << c_text(st,con)
    }
  elsif str.kind_of? (Nokogiri::XML::Text)
    ret << s_text(str)
  end
  return ret.flatten
end

def cc_text(str,con)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      #puts st.name

      break if st.name == con
      tmp << cc_text(st,con)
    }
    ret << tmp
  elsif str.kind_of? (Nokogiri::XML::NodeSet)
    str.collect().each{|st|
      ret << cc_text(st,con)
    }
  elsif str.kind_of? (Nokogiri::XML::Text)
    ret << s_text(str)
  end
  return ret.flatten
end

def r_c_text(str,c)
  ret= []
  b = true
  str.collect{|ss|
    tmp = []
    ss.children().collect{|st|
      t = st.text.gsub(/\u00A0/,'').strip
      b = false if st.name == c
      next if b == true
      tmp << t
    }
    if ss.name == "ul"
      ret << tmp.join(",").pretty
    else
      ret << tmp.join(" ").pretty
    end
  }
  return ret
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def s_key(str)
  return str.gsub(/\'|’|\+/,"").gsub(/\s+/," ").strip.gsub(" ","_").downcase
end

def prune(tbl)
  begin
    ScraperWiki.sqliteexecute("drop table #{tbl}")
    ScraperWiki.commit()
  rescue Exception => e
    puts [tbl,e,e.backtrace].inspect
  end
end

def exists(val,tbl,col)
  begin
    return ScraperWiki.sqliteexecute("select count(*) from #{tbl} where #{col}=?",[val])['data'][0][0]
  rescue Exception => e
    puts [val,e,e.backtrace].inspect
    return 0
  end
end

def append_base(uri,surl)
  return nil if surl.nil? or surl.empty? or surl == "/"
  return surl if surl =~ /^http/
  return uri.strip + ("/"+surl.strip).gsub(/(\/)+/,"/").strip
end

def parse(pg,act)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"  

  if act == "ranked_concepts"
    doc = Nokogiri::XML(data).xpath(".")
    r = {}
    r["language"] = s_text(doc.xpath(".//language/text()"))
    tmp = []
    doc.xpath(".//concepts/concept").each{|ent|
      tmp << {
        "text" => s_text(ent.xpath("./text/text()")),
        "relevance" => s_text(ent.xpath("./relevance/text()")),
      }
    }
    r["concepts"] = tmp
    return r
  elsif act == "ranked_keywords"
    doc = Nokogiri::XML(data).xpath(".")
    r = {}
    r["language"] = s_text(doc.xpath(".//language/text()"))
    tmp = []
    doc.xpath(".//keywords/keyword").each{|ent|
      tmp << {
        "text" => s_text(ent.xpath("./text/text()")),
        "relevance" => s_text(ent.xpath("./relevance/text()")),
      }
    }
    r["keywords"] = tmp
    return r
  elsif act == "named_entities"
    doc = Nokogiri::XML(data).xpath(".")
    r = {}
    r["language"] = s_text(doc.xpath(".//language/text()"))
    tmp = []
    doc.xpath(".//entities/entity").each{|ent|
      tmp << {
        "relevance" => s_text(ent.xpath("./relevance/text()")),
        "count" => s_text(ent.xpath("./count/text()")),
        "text" => s_text(ent.xpath("./text/text()")),
        "type" => s_text(ent.xpath("./type/text()")),
      }
    }
    r["entities"] =  tmp
    return r
  end
end

def ttm(str)
  begin
    h,m,s = 0,0,0
    sep = "." if str =~ /\./
    sep = ":" if str =~ /\./
    h,m,s = str.split(sep).map{|t| t.to_i}
    return h * 60 + m + s / 60.0
  rescue 
    str
  end
end


def get_analysis(val,col1,col2,tbl)
  begin
    begin
      ScraperWiki.sqliteexecute('delete from '+tbl+' where analysis like \'%"language":""%\' or analysis like \'%"keywords":[]%\' or analysis is null')#or  analysis like \'%"entities":[]%\'')
      ScraperWiki.commit()
      @toggle = 1
    end if @toggle.nil? or @toggle == 0

    return ScraperWiki.sqliteexecute("select #{col2} from #{tbl} where #{col1}=?",[val])['data'].flatten.first
  rescue Exception => e
    puts [e.inspect,e.backtrace].inspect
    return nil
  end
end

def get_by_text(data)
  #puts [@limit_reached,@limit_reached==true].inspect
  return nil unless @limit_reached.nil? if @limit_reached == true
  if data.nil? or data.empty? #or data.strip.length < 100
    puts "null / insufficient feed"
    return nil 
  end
  base_uri = "http://access.alchemyapi.com/calls/text/"
  hdrs = {
      "X-Requested-With"=>"XMLHttpRequest",
      "Referer"=>"http://access.alchemyapi.com/demo/entities_int.html",
      "Cookie"=>"__utma=191335290.937107543.1334691427.1334691427.1334691427.1; __utmb=191335290.2.10.1334691427; __utmc=191335290; __utmz=191335290.1334691427.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
  }
  params = {"apikey"=>KY,"text"=>data}
  named_entities = parse(Mechanize.new().post(base_uri+"TextGetRankedNamedEntities",params,hdrs),"named_entities")
  ranked_concepts = parse(Mechanize.new().post(base_uri+"TextGetRankedConcepts?showSourceText=1",params,hdrs),"ranked_concepts")
  pg = Mechanize.new().post(base_uri+"TextGetRankedKeywords?showSourceText=1",params,hdrs)
  ranked_keywords = parse(pg,"ranked_keywords")
  if ranked_keywords["keywords"].nil? or ranked_keywords["keywords"].empty? 
    puts "Invalid analysis results for #{data} - #{data.length} :: #{pg.body}"
    @limit_reached = true if pg.body =~ /limit/i
  end
  return JSON.generate({"named_entities"=>named_entities,"ranked_keywords"=>ranked_keywords,"ranked_concepts"=>ranked_concepts}) #unless ranked_keywords.nil? 
  #return JSON.generate("ranked_keywords"=>ranked_keywords) #unless ranked_keywords.nil? 
end


def get_by_url(url)
  return nil unless @limit_reached.nil? if @limit_reached == true
  raise "Null value" if url.nil? or url.empty? 
  base_uri = "http://access.alchemyapi.com/calls/url/"
  hdrs = {
      "X-Requested-With"=>"XMLHttpRequest",
      "Referer"=>"http://access.alchemyapi.com/demo/entities_int.html",
      "Cookie"=>"__utma=191335290.937107543.1334691427.1334691427.1334691427.1; __utmb=191335290.2.10.1334691427; __utmc=191335290; __utmz=191335290.1334691427.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
  }
  named_entities = parse(Mechanize.new().get(base_uri+"URLGetRankedNamedEntities?apikey=#{KY}&url=#{url}",[],base_uri,hdrs),"named_entities")
  ranked_concepts = parse(Mechanize.new().get(base_uri+"URLGetRankedConcepts?apikey=#{KY}&url=#{url}",[],base_uri,hdrs),"ranked_concepts")
  pg = Mechanize.new().get(base_uri+"URLGetRankedKeywords?apikey=#{KY}&url=#{url}",[],base_uri,hdrs)
  ranked_keywords = parse(pg,"ranked_keywords")
  if ranked_keywords["keywords"].nil? or ranked_keywords["keywords"].empty?   
    puts "Invalid analysis results for #{url} :: #{pg.body}" 
    @limit_reached = true if pg.body =~ /limit/i
  end
  return JSON.generate({"named_entities"=>named_entities,"ranked_keywords"=>ranked_keywords,"ranked_concepts"=>ranked_concepts}) #unless ranked_keywords.nil? 
  #return JSON.generate("ranked_keywords"=>ranked_keywords) #unless ranked_keywords.nil? 
end


def dur(arr)
  d = {}
  arr.each{|a|
    if a =~ /day$/i or a =~ /days$/i
      d["days"] = a.scan(/([\d.]+)/).flatten.first
    elsif a =~ /week$/i or a =~ /weeks$/i
      d["weeks"] = a.scan(/([\d.]+)/).flatten.first
    elsif a =~ /month$/i or a =~ /months$/i or a =~ /month\(s\)$/i
      d["months"] = a.scan(/([\d.]+)/).flatten.first
    elsif a =~ /year$/i or a =~ /years$/i
      d["years"] = a.scan(/([\d.]+)/).flatten.first
    elsif a=~ /h$/i or a =~ /hours$/i or a =~ /hour$/i or a =~ /hrs/ or a =~ /hr$/
      d["hours"] = a.scan(/([\d.]+)/).flatten.first
    elsif a =~ /m$/i or a =~ /minutes$/i or a =~ /minute$/i or a =~ /min$/ or a =~ /mins$/
      d["minutes"] = a.scan(/([\d.]+)/).flatten.first
    elsif (a =~ /s$/i or a =~ /seconds$/i or a =~ /second$/i)
      tmp = a.scan(/([\d.]+)/).flatten.first
      d["seconds"] = tmp unless tmp == "0"
    end
  }
  return d
end

def gbp_usd(v1)
  pg = Mechanize.new().get("http://www.google.com/finance/converter?a=#{v1}&from=GBP&to=USD")
  v = s_text(Nokogiri::HTML(pg.body).xpath(".//span[@class='bld']")).gsub("USD","").strip
  return "$#{v}"
end

def csv_hash(fn)
  cd = CSV.read fn
  hdrs = cd.shift.map {|i| i.to_s }
  da = cd.map {|row| row.map {|cell| cell.to_s } }
  return da.map {|row| Hash[*hdrs.zip(row).flatten] }
end

# LICENSE:
# 
# (The MIT License)
# 
# Copyright © 2008 Tom Preston-Werner
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

require 'strscan'

class Numerizer

  DIRECT_NUMS = [
    ['eleven', '11'],
    ['twelve', '12'],
    ['thirteen', '13'],
    ['fourteen', '14'],
    ['fifteen', '15'],
    ['sixteen', '16'],
    ['seventeen', '17'],
    ['eighteen', '18'],
    ['nineteen', '19'],
    ['ninteen', '19'], # Common mis-spelling
    ['zero', '0'],
    ['ten', '10'],
    ['\ba[\b^$]', '1'] # doesn't make sense for an 'a' at the end to be a 1
  ]
  
  SINGLE_NUMS = [
    ['one', 1],
    ['two', 2],
    ['three', 3],
    #['four(\W|$)', '4\1'],  # The weird regex is so that it matches four but not fourty
    ['four', 4],
    ['five', 5],
    ['six', 6],
    ['seven', 7],
    ['eight', 8],
    ['nine', 9]
  ]

  TEN_PREFIXES = [ ['twenty', 20],
    ['thirty', 30],
    ['forty', 40],
    ['fourty', 40], # Common misspelling
    ['fifty', 50],
    ['sixty', 60],
    ['seventy', 70],
    ['eighty', 80],
    ['ninety', 90]
  ]

  BIG_PREFIXES = [ ['hundred', 100],
    ['thousand', 1000],
    ['million', 1_000_000],
    ['billion', 1_000_000_000],
    ['trillion', 1_000_000_000_000],
  ]
  
  FRACTIONS = [ ['half', 2],
    ['third(s)?', 3],
    ['fourth(s)?', 4],
    ['quarter(s)?', 4],
    ['fifth(s)?', 5],
    ['sixth(s)?', 6],
    ['seventh(s)?', 7],
    ['eighth(s)?', 8],
    ['nineth(s)?', 9],
  ]

  def self.numerize(string)
    string = string.dup

    # preprocess
    string.gsub!(/ +|([^\d])-([^\d])/, '\1 \2') # will mutilate hyphenated-words

    # easy/direct replacements

    (DIRECT_NUMS + SINGLE_NUMS).each do |dn|
      # string.gsub!(/#{dn[0]}/i, '<num>' + dn[1])
      string.gsub!(/(^|\W+)#{dn[0]}($|\W+)/i) {"#{$1}<num>" + dn[1].to_s + $2}
    end

    # ten, twenty, etc.
    # TEN_PREFIXES.each do |tp|
    #   string.gsub!(/(?:#{tp[0]}) *<num>(\d(?=[^\d]|$))*/i) {'<num>' + (tp[1] + $1.to_i).to_s}
    # end
    TEN_PREFIXES.each do |tp|
      SINGLE_NUMS.each do |dn|
        string.gsub!(/(^|\W+)#{tp[0]}#{dn[0]}($|\W+)/i) { 
          "#{$1}<num>" + (tp[1] + dn[1]).to_s + $2
        }
      end
      string.gsub!(/(^|\W+)#{tp[0]}($|\W+)/i) { "#{$1}<num>" + tp[1].to_s + $2 }
    end
    
    # handle fractions
    FRACTIONS.each do |tp|
      string.gsub!(/a #{tp[0]}/i) { '<num>1/' + tp[1].to_s }
      string.gsub!(/\s#{tp[0]}/i) { '/' + tp[1].to_s }
    end
    
    # evaluate fractions when preceded by another number
    string.gsub!(/(\d+)(?: | and |-)+(<num>|\s)*(\d+)\s*\/\s*(\d+)/i) { ($1.to_f + ($3.to_f/$4.to_f)).to_s }
    
    # hundreds, thousands, millions, etc.
    BIG_PREFIXES.each do |bp|
      string.gsub!(/(?:<num>)?(\d*) *#{bp[0]}/i) { '<num>' + (bp[1] * $1.to_i).to_s}
        andition(string)
    end

    andition(string)

    string.gsub(/<num>/, '')
  end

  private

  def self.andition(string)
    sc = StringScanner.new(string)
    while(sc.scan_until(/<num>(\d+)( | and )<num>(\d+)(?=[^\w]|$)/i))
      if sc[2] =~ /and/ || sc[1].size > sc[3].size
        string[(sc.pos - sc.matched_size)..(sc.pos-1)] = '<num>' + (sc[1].to_i + sc[3].to_i).to_s
        sc.reset
      end
    end
  end
end

require 'numerizer' unless defined?(Numerizer)

module ChronicDuration

  extend self

  class DurationParseError < StandardError
  end

  @@raise_exceptions = false

  def self.raise_exceptions
    !!@@raise_exceptions
  end

  def self.raise_exceptions=(value)
    @@raise_exceptions = !!value
  end

  # Given a string representation of elapsed time,
  # return an integer (or float, if fractions of a
  # second are input)
  def parse(string, opts = {})
    result = calculate_from_words(cleanup(string), opts)
    (!opts[:keep_zero] and result == 0) ? nil : result
  end

  # Given an integer and an optional format,
  # returns a formatted string representing elapsed time
  def output(seconds, opts = {})
    int = seconds.to_i
    seconds = int if seconds - int == 0 # if seconds end with .0

    opts[:format] ||= :default
    opts[:keep_zero] ||= false

    years = months = weeks = days = hours = minutes = 0

    decimal_places = seconds.to_s.split('.').last.length if seconds.is_a?(Float)

    minute = 60
    hour = 60 * minute
    day = 24 * hour
    month = 30 * day
    year = 31557600

    if seconds >= 31557600 && seconds%year < seconds%month
      years = seconds / year
      months = seconds % year / month
      days = seconds % year % month / day
      hours = seconds % year % month % day / hour
      minutes = seconds % year % month % day % hour / minute
      seconds = seconds % year % month % day % hour % minute
    elsif seconds >= 60
      minutes = (seconds / 60).to_i
      seconds = seconds % 60
      if minutes >= 60
        hours = (minutes / 60).to_i
        minutes = (minutes % 60).to_i
        if hours >= 24
          days = (hours / 24).to_i
          hours = (hours % 24).to_i
          if opts[:weeks]
            if days >= 7
              weeks = (days / 7).to_i
              days = (days % 7).to_i
              if weeks >= 4
                months = (weeks / 4).to_i
                weeks = (weeks % 4).to_i
              end
            end
          else
            if days >= 30
              months = (days / 30).to_i
              days = (days % 30).to_i
            end
          end
        end
      end
    end

    joiner = ' '
    process = nil

    case opts[:format]
    when :micro
      dividers = {
        :years => 'y', :months => 'mo', :weeks => 'w', :days => 'd', :hours => 'h', :minutes => 'm', :seconds => 's' }
      joiner = ''
    when :short
      dividers = {
        :years => 'y', :months => 'mo', :weeks => 'w', :days => 'd', :hours => 'h', :minutes => 'm', :seconds => 's' }
    when :default
      dividers = {
        :years => ' yr', :months => ' mo', :weeks => ' wk', :days => ' day', :hours => ' hr', :minutes => ' min', :seconds => ' sec',
        :pluralize => true }
    when :long
      dividers = {
        :years => ' year', :months => ' month', :weeks => ' week', :days => ' day', :hours => ' hour', :minutes => ' minute', :seconds => ' second',
        :pluralize => true }
    when :chrono
      dividers = {
        :years => ':', :months => ':', :weeks => ':', :days => ':', :hours => ':', :minutes => ':', :seconds => ':', :keep_zero => true }
      process = lambda do |str|
        # Pad zeros
        # Get rid of lead off times if they are zero
        # Get rid of lead off zero
        # Get rid of trailing :
        divider = ':'
        str.split(divider).map { |n|
          # add zeros only if n is an integer
          n.include?('.') ? ("%04.#{decimal_places}f" % n) : ("%02d" % n)
        }.join(divider).gsub(/^(00:)+/, '').gsub(/^0/, '').gsub(/:$/, '')
      end
      joiner = ''
    end

    result = [:years, :months, :weeks, :days, :hours, :minutes, :seconds].map do |t|
      next if t == :weeks && !opts[:weeks]
      num = eval(t.to_s)
      num = ("%.#{decimal_places}f" % num) if num.is_a?(Float) && t == :seconds
      keep_zero = dividers[:keep_zero]
      keep_zero ||= opts[:keep_zero] if t == :seconds
      humanize_time_unit( num, dividers[t], dividers[:pluralize], keep_zero )
    end.compact!

    result = result[0...opts[:units]] if opts[:units]

    result = result.join(joiner)

    if process
      result = process.call(result)
    end

    result.length == 0 ? nil : result

  end

private

  def humanize_time_unit(number, unit, pluralize, keep_zero)
    return nil if number == 0 && !keep_zero
    res = "#{number}#{unit}"
    # A poor man's pluralizer
    res << 's' if !(number == 1) && pluralize
    res
  end

  def calculate_from_words(string, opts)
    val = 0
    words = string.split(' ')
    words.each_with_index do |v, k|
      if v =~ float_matcher
        val += (convert_to_number(v) * duration_units_seconds_multiplier(words[k + 1] || (opts[:default_unit] || 'seconds')))
      end
    end
    val
  end

  def cleanup(string)
    res = string.downcase
    res = filter_by_type(Numerizer.numerize(res))
    res = res.gsub(float_matcher) {|n| " #{n} "}.squeeze(' ').strip
    res = filter_through_white_list(res)
  end

  def convert_to_number(string)
    string.to_f % 1 > 0 ? string.to_f : string.to_i
  end

  def duration_units_list
    %w(seconds minutes hours days weeks months years)
  end
  def duration_units_seconds_multiplier(unit)
    return 0 unless duration_units_list.include?(unit)
    case unit
    when 'years';   31557600
    when 'months';  3600 * 24 * 30
    when 'weeks';   3600 * 24 * 7
    when 'days';    3600 * 24
    when 'hours';   3600
    when 'minutes'; 60
    when 'seconds'; 1
    end
  end

  # Parse 3:41:59 and return 3 hours 41 minutes 59 seconds
  def filter_by_type(string)
    chrono_units_list = duration_units_list.reject {|v| v == "weeks"}
    if string.gsub(' ', '') =~ /#{float_matcher}(:#{float_matcher})+/
      res = []
      string.gsub(' ', '').split(':').reverse.each_with_index do |v,k|
        return unless chrono_units_list[k]
        res << "#{v} #{chrono_units_list[k]}"
      end
      res = res.reverse.join(' ')
    else
      res = string
    end
    res
  end

  def float_matcher
    /[0-9]*\.?[0-9]+/
  end

  # Get rid of unknown words and map found
  # words to defined time units
  def filter_through_white_list(string)
    res = []
    string.split(' ').each do |word|
      if word =~ float_matcher
        res << word.strip
        next
      end
      stripped_word = word.strip.gsub(/^,/, '').gsub(/,$/, '')
      if mappings.has_key?(stripped_word)
        res << mappings[stripped_word]
      elsif !join_words.include?(stripped_word) and ChronicDuration.raise_exceptions
        raise DurationParseError, "An invalid word #{word.inspect} was used in the string to be parsed."
      end
    end
    # add '1' at front if string starts with something recognizable but not with a number, like 'day' or 'minute 30sec' 
    res.unshift(1) if res.length > 0 && mappings[res[0]]  
    res.join(' ')
  end

  def mappings
    {
      'seconds' => 'seconds',
      'second'  => 'seconds',
      'secs'    => 'seconds',
      'sec'     => 'seconds',
      's'       => 'seconds',
      'minutes' => 'minutes',
      'minute'  => 'minutes',
      'mins'    => 'minutes',
      'min'     => 'minutes',
      'm'       => 'minutes',
      'hours'   => 'hours',
      'hour'    => 'hours',
      'hrs'     => 'hours',
      'hr'      => 'hours',
      'h'       => 'hours',
      'days'    => 'days',
      'day'     => 'days',
      'dy'      => 'days',
      'd'       => 'days',
      'weeks'   => 'weeks',
      'week'    => 'weeks',
      'w'       => 'weeks',
      'months'  => 'months',
      'mo'      => 'months',
      'mos'     => 'months',
      'month'   => 'months',
      'years'   => 'years',
      'year'    => 'years',
      'yrs'     => 'years',
      'yr'      => 'years',
      'y'       => 'years'
    }
  end

  def join_words
    ['and', 'with', 'plus']
  end
end# encoding: UTF-8
require 'mechanize'
require 'nokogiri'

#KY="27cedd1f8bd73bcfca715cb8eb0500d813e4b5d2" # S
#KY="43672daa5983e218e41281f06f8e28eb207cd4b0" # M
KY="c6cbf833716dc7760eb83507a858e278b5e84264" #A_B

@convs = {}

def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
    raise e unless e.inspect =~ /no such table/i    
  end
end
def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e 
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   raise e unless e.inspect =~ /no such table/i
  end
end
def delete_metadata(name)
  begin
   ScraperWiki.sqliteexecute("delete from swvariables where name=?",[name])
   ScraperWiki.commit()
  rescue Exception => e
   puts "ERROR: #{e.inspect} during delete_metadata(#{name})"
   raise e unless e.inspect =~ /no such table/i
  end
end


class String
  def pretty
    self.gsub(/\s+/,' ').strip
  end
end

def i_text(str,ign)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      tmp << a_text(st)
    } unless str.name =~ /"script"|#{ign}/
    ret << tmp
  elsif str.kind_of? (Nokogiri::XML::NodeSet)
    str.collect().each{|st|
      ret << a_text(st)
    }
  elsif str.kind_of? (Nokogiri::XML::Text)
    ret << s_text(str)
  end
  return ret.flatten
end

def a_text(str)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      tmp << a_text(st)
    } unless str.name == "script"
    ret << tmp
  elsif str.kind_of? (Nokogiri::XML::NodeSet)
    str.collect().each{|st|
      ret << a_text(st)
    }
  elsif str.kind_of? (Nokogiri::XML::Text)
    ret << s_text(str)
  end
  return ret.flatten
end

def s_text(str)
  return str.text.strip.gsub(/\u00A0/,' ').pretty
end

def c_text(str,con)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      tmp << c_text(st,con)
    }
    ret << tmp
  elsif str.kind_of? (Nokogiri::XML::NodeSet)
    str.collect().each{|st|
      break if st.name =~ /#{con}/
      ret << c_text(st,con)
    }
  elsif str.kind_of? (Nokogiri::XML::Text)
    ret << s_text(str)
  end
  return ret.flatten
end

def cc_text(str,con)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      #puts st.name

      break if st.name == con
      tmp << cc_text(st,con)
    }
    ret << tmp
  elsif str.kind_of? (Nokogiri::XML::NodeSet)
    str.collect().each{|st|
      ret << cc_text(st,con)
    }
  elsif str.kind_of? (Nokogiri::XML::Text)
    ret << s_text(str)
  end
  return ret.flatten
end

def r_c_text(str,c)
  ret= []
  b = true
  str.collect{|ss|
    tmp = []
    ss.children().collect{|st|
      t = st.text.gsub(/\u00A0/,'').strip
      b = false if st.name == c
      next if b == true
      tmp << t
    }
    if ss.name == "ul"
      ret << tmp.join(",").pretty
    else
      ret << tmp.join(" ").pretty
    end
  }
  return ret
end

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end


def s_key(str)
  return str.gsub(/\'|’|\+/,"").gsub(/\s+/," ").strip.gsub(" ","_").downcase
end

def prune(tbl)
  begin
    ScraperWiki.sqliteexecute("drop table #{tbl}")
    ScraperWiki.commit()
  rescue Exception => e
    puts [tbl,e,e.backtrace].inspect
  end
end

def exists(val,tbl,col)
  begin
    return ScraperWiki.sqliteexecute("select count(*) from #{tbl} where #{col}=?",[val])['data'][0][0]
  rescue Exception => e
    puts [val,e,e.backtrace].inspect
    return 0
  end
end

def append_base(uri,surl)
  return nil if surl.nil? or surl.empty? or surl == "/"
  return surl if surl =~ /^http/
  return uri.strip + ("/"+surl.strip).gsub(/(\/)+/,"/").strip
end

def parse(pg,act)
  data = pg.body
  uri = URI.parse(pg.uri.to_s)
  base_uri = "#{uri.scheme}://#{uri.host}"  

  if act == "ranked_concepts"
    doc = Nokogiri::XML(data).xpath(".")
    r = {}
    r["language"] = s_text(doc.xpath(".//language/text()"))
    tmp = []
    doc.xpath(".//concepts/concept").each{|ent|
      tmp << {
        "text" => s_text(ent.xpath("./text/text()")),
        "relevance" => s_text(ent.xpath("./relevance/text()")),
      }
    }
    r["concepts"] = tmp
    return r
  elsif act == "ranked_keywords"
    doc = Nokogiri::XML(data).xpath(".")
    r = {}
    r["language"] = s_text(doc.xpath(".//language/text()"))
    tmp = []
    doc.xpath(".//keywords/keyword").each{|ent|
      tmp << {
        "text" => s_text(ent.xpath("./text/text()")),
        "relevance" => s_text(ent.xpath("./relevance/text()")),
      }
    }
    r["keywords"] = tmp
    return r
  elsif act == "named_entities"
    doc = Nokogiri::XML(data).xpath(".")
    r = {}
    r["language"] = s_text(doc.xpath(".//language/text()"))
    tmp = []
    doc.xpath(".//entities/entity").each{|ent|
      tmp << {
        "relevance" => s_text(ent.xpath("./relevance/text()")),
        "count" => s_text(ent.xpath("./count/text()")),
        "text" => s_text(ent.xpath("./text/text()")),
        "type" => s_text(ent.xpath("./type/text()")),
      }
    }
    r["entities"] =  tmp
    return r
  end
end

def ttm(str)
  begin
    h,m,s = 0,0,0
    sep = "." if str =~ /\./
    sep = ":" if str =~ /\./
    h,m,s = str.split(sep).map{|t| t.to_i}
    return h * 60 + m + s / 60.0
  rescue 
    str
  end
end


def get_analysis(val,col1,col2,tbl)
  begin
    begin
      ScraperWiki.sqliteexecute('delete from '+tbl+' where analysis like \'%"language":""%\' or analysis like \'%"keywords":[]%\' or analysis is null')#or  analysis like \'%"entities":[]%\'')
      ScraperWiki.commit()
      @toggle = 1
    end if @toggle.nil? or @toggle == 0

    return ScraperWiki.sqliteexecute("select #{col2} from #{tbl} where #{col1}=?",[val])['data'].flatten.first
  rescue Exception => e
    puts [e.inspect,e.backtrace].inspect
    return nil
  end
end

def get_by_text(data)
  #puts [@limit_reached,@limit_reached==true].inspect
  return nil unless @limit_reached.nil? if @limit_reached == true
  if data.nil? or data.empty? #or data.strip.length < 100
    puts "null / insufficient feed"
    return nil 
  end
  base_uri = "http://access.alchemyapi.com/calls/text/"
  hdrs = {
      "X-Requested-With"=>"XMLHttpRequest",
      "Referer"=>"http://access.alchemyapi.com/demo/entities_int.html",
      "Cookie"=>"__utma=191335290.937107543.1334691427.1334691427.1334691427.1; __utmb=191335290.2.10.1334691427; __utmc=191335290; __utmz=191335290.1334691427.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
  }
  params = {"apikey"=>KY,"text"=>data}
  named_entities = parse(Mechanize.new().post(base_uri+"TextGetRankedNamedEntities",params,hdrs),"named_entities")
  ranked_concepts = parse(Mechanize.new().post(base_uri+"TextGetRankedConcepts?showSourceText=1",params,hdrs),"ranked_concepts")
  pg = Mechanize.new().post(base_uri+"TextGetRankedKeywords?showSourceText=1",params,hdrs)
  ranked_keywords = parse(pg,"ranked_keywords")
  if ranked_keywords["keywords"].nil? or ranked_keywords["keywords"].empty? 
    puts "Invalid analysis results for #{data} - #{data.length} :: #{pg.body}"
    @limit_reached = true if pg.body =~ /limit/i
  end
  return JSON.generate({"named_entities"=>named_entities,"ranked_keywords"=>ranked_keywords,"ranked_concepts"=>ranked_concepts}) #unless ranked_keywords.nil? 
  #return JSON.generate("ranked_keywords"=>ranked_keywords) #unless ranked_keywords.nil? 
end


def get_by_url(url)
  return nil unless @limit_reached.nil? if @limit_reached == true
  raise "Null value" if url.nil? or url.empty? 
  base_uri = "http://access.alchemyapi.com/calls/url/"
  hdrs = {
      "X-Requested-With"=>"XMLHttpRequest",
      "Referer"=>"http://access.alchemyapi.com/demo/entities_int.html",
      "Cookie"=>"__utma=191335290.937107543.1334691427.1334691427.1334691427.1; __utmb=191335290.2.10.1334691427; __utmc=191335290; __utmz=191335290.1334691427.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)"
  }
  named_entities = parse(Mechanize.new().get(base_uri+"URLGetRankedNamedEntities?apikey=#{KY}&url=#{url}",[],base_uri,hdrs),"named_entities")
  ranked_concepts = parse(Mechanize.new().get(base_uri+"URLGetRankedConcepts?apikey=#{KY}&url=#{url}",[],base_uri,hdrs),"ranked_concepts")
  pg = Mechanize.new().get(base_uri+"URLGetRankedKeywords?apikey=#{KY}&url=#{url}",[],base_uri,hdrs)
  ranked_keywords = parse(pg,"ranked_keywords")
  if ranked_keywords["keywords"].nil? or ranked_keywords["keywords"].empty?   
    puts "Invalid analysis results for #{url} :: #{pg.body}" 
    @limit_reached = true if pg.body =~ /limit/i
  end
  return JSON.generate({"named_entities"=>named_entities,"ranked_keywords"=>ranked_keywords,"ranked_concepts"=>ranked_concepts}) #unless ranked_keywords.nil? 
  #return JSON.generate("ranked_keywords"=>ranked_keywords) #unless ranked_keywords.nil? 
end


def dur(arr)
  d = {}
  arr.each{|a|
    if a =~ /day$/i or a =~ /days$/i
      d["days"] = a.scan(/([\d.]+)/).flatten.first
    elsif a =~ /week$/i or a =~ /weeks$/i
      d["weeks"] = a.scan(/([\d.]+)/).flatten.first
    elsif a =~ /month$/i or a =~ /months$/i or a =~ /month\(s\)$/i
      d["months"] = a.scan(/([\d.]+)/).flatten.first
    elsif a =~ /year$/i or a =~ /years$/i
      d["years"] = a.scan(/([\d.]+)/).flatten.first
    elsif a=~ /h$/i or a =~ /hours$/i or a =~ /hour$/i or a =~ /hrs/ or a =~ /hr$/
      d["hours"] = a.scan(/([\d.]+)/).flatten.first
    elsif a =~ /m$/i or a =~ /minutes$/i or a =~ /minute$/i or a =~ /min$/ or a =~ /mins$/
      d["minutes"] = a.scan(/([\d.]+)/).flatten.first
    elsif (a =~ /s$/i or a =~ /seconds$/i or a =~ /second$/i)
      tmp = a.scan(/([\d.]+)/).flatten.first
      d["seconds"] = tmp unless tmp == "0"
    end
  }
  return d
end

def gbp_usd(v1)
  pg = Mechanize.new().get("http://www.google.com/finance/converter?a=#{v1}&from=GBP&to=USD")
  v = s_text(Nokogiri::HTML(pg.body).xpath(".//span[@class='bld']")).gsub("USD","").strip
  return "$#{v}"
end

def csv_hash(fn)
  cd = CSV.read fn
  hdrs = cd.shift.map {|i| i.to_s }
  da = cd.map {|row| row.map {|cell| cell.to_s } }
  return da.map {|row| Hash[*hdrs.zip(row).flatten] }
end

# LICENSE:
# 
# (The MIT License)
# 
# Copyright © 2008 Tom Preston-Werner
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

require 'strscan'

class Numerizer

  DIRECT_NUMS = [
    ['eleven', '11'],
    ['twelve', '12'],
    ['thirteen', '13'],
    ['fourteen', '14'],
    ['fifteen', '15'],
    ['sixteen', '16'],
    ['seventeen', '17'],
    ['eighteen', '18'],
    ['nineteen', '19'],
    ['ninteen', '19'], # Common mis-spelling
    ['zero', '0'],
    ['ten', '10'],
    ['\ba[\b^$]', '1'] # doesn't make sense for an 'a' at the end to be a 1
  ]
  
  SINGLE_NUMS = [
    ['one', 1],
    ['two', 2],
    ['three', 3],
    #['four(\W|$)', '4\1'],  # The weird regex is so that it matches four but not fourty
    ['four', 4],
    ['five', 5],
    ['six', 6],
    ['seven', 7],
    ['eight', 8],
    ['nine', 9]
  ]

  TEN_PREFIXES = [ ['twenty', 20],
    ['thirty', 30],
    ['forty', 40],
    ['fourty', 40], # Common misspelling
    ['fifty', 50],
    ['sixty', 60],
    ['seventy', 70],
    ['eighty', 80],
    ['ninety', 90]
  ]

  BIG_PREFIXES = [ ['hundred', 100],
    ['thousand', 1000],
    ['million', 1_000_000],
    ['billion', 1_000_000_000],
    ['trillion', 1_000_000_000_000],
  ]
  
  FRACTIONS = [ ['half', 2],
    ['third(s)?', 3],
    ['fourth(s)?', 4],
    ['quarter(s)?', 4],
    ['fifth(s)?', 5],
    ['sixth(s)?', 6],
    ['seventh(s)?', 7],
    ['eighth(s)?', 8],
    ['nineth(s)?', 9],
  ]

  def self.numerize(string)
    string = string.dup

    # preprocess
    string.gsub!(/ +|([^\d])-([^\d])/, '\1 \2') # will mutilate hyphenated-words

    # easy/direct replacements

    (DIRECT_NUMS + SINGLE_NUMS).each do |dn|
      # string.gsub!(/#{dn[0]}/i, '<num>' + dn[1])
      string.gsub!(/(^|\W+)#{dn[0]}($|\W+)/i) {"#{$1}<num>" + dn[1].to_s + $2}
    end

    # ten, twenty, etc.
    # TEN_PREFIXES.each do |tp|
    #   string.gsub!(/(?:#{tp[0]}) *<num>(\d(?=[^\d]|$))*/i) {'<num>' + (tp[1] + $1.to_i).to_s}
    # end
    TEN_PREFIXES.each do |tp|
      SINGLE_NUMS.each do |dn|
        string.gsub!(/(^|\W+)#{tp[0]}#{dn[0]}($|\W+)/i) { 
          "#{$1}<num>" + (tp[1] + dn[1]).to_s + $2
        }
      end
      string.gsub!(/(^|\W+)#{tp[0]}($|\W+)/i) { "#{$1}<num>" + tp[1].to_s + $2 }
    end
    
    # handle fractions
    FRACTIONS.each do |tp|
      string.gsub!(/a #{tp[0]}/i) { '<num>1/' + tp[1].to_s }
      string.gsub!(/\s#{tp[0]}/i) { '/' + tp[1].to_s }
    end
    
    # evaluate fractions when preceded by another number
    string.gsub!(/(\d+)(?: | and |-)+(<num>|\s)*(\d+)\s*\/\s*(\d+)/i) { ($1.to_f + ($3.to_f/$4.to_f)).to_s }
    
    # hundreds, thousands, millions, etc.
    BIG_PREFIXES.each do |bp|
      string.gsub!(/(?:<num>)?(\d*) *#{bp[0]}/i) { '<num>' + (bp[1] * $1.to_i).to_s}
        andition(string)
    end

    andition(string)

    string.gsub(/<num>/, '')
  end

  private

  def self.andition(string)
    sc = StringScanner.new(string)
    while(sc.scan_until(/<num>(\d+)( | and )<num>(\d+)(?=[^\w]|$)/i))
      if sc[2] =~ /and/ || sc[1].size > sc[3].size
        string[(sc.pos - sc.matched_size)..(sc.pos-1)] = '<num>' + (sc[1].to_i + sc[3].to_i).to_s
        sc.reset
      end
    end
  end
end

require 'numerizer' unless defined?(Numerizer)

module ChronicDuration

  extend self

  class DurationParseError < StandardError
  end

  @@raise_exceptions = false

  def self.raise_exceptions
    !!@@raise_exceptions
  end

  def self.raise_exceptions=(value)
    @@raise_exceptions = !!value
  end

  # Given a string representation of elapsed time,
  # return an integer (or float, if fractions of a
  # second are input)
  def parse(string, opts = {})
    result = calculate_from_words(cleanup(string), opts)
    (!opts[:keep_zero] and result == 0) ? nil : result
  end

  # Given an integer and an optional format,
  # returns a formatted string representing elapsed time
  def output(seconds, opts = {})
    int = seconds.to_i
    seconds = int if seconds - int == 0 # if seconds end with .0

    opts[:format] ||= :default
    opts[:keep_zero] ||= false

    years = months = weeks = days = hours = minutes = 0

    decimal_places = seconds.to_s.split('.').last.length if seconds.is_a?(Float)

    minute = 60
    hour = 60 * minute
    day = 24 * hour
    month = 30 * day
    year = 31557600

    if seconds >= 31557600 && seconds%year < seconds%month
      years = seconds / year
      months = seconds % year / month
      days = seconds % year % month / day
      hours = seconds % year % month % day / hour
      minutes = seconds % year % month % day % hour / minute
      seconds = seconds % year % month % day % hour % minute
    elsif seconds >= 60
      minutes = (seconds / 60).to_i
      seconds = seconds % 60
      if minutes >= 60
        hours = (minutes / 60).to_i
        minutes = (minutes % 60).to_i
        if hours >= 24
          days = (hours / 24).to_i
          hours = (hours % 24).to_i
          if opts[:weeks]
            if days >= 7
              weeks = (days / 7).to_i
              days = (days % 7).to_i
              if weeks >= 4
                months = (weeks / 4).to_i
                weeks = (weeks % 4).to_i
              end
            end
          else
            if days >= 30
              months = (days / 30).to_i
              days = (days % 30).to_i
            end
          end
        end
      end
    end

    joiner = ' '
    process = nil

    case opts[:format]
    when :micro
      dividers = {
        :years => 'y', :months => 'mo', :weeks => 'w', :days => 'd', :hours => 'h', :minutes => 'm', :seconds => 's' }
      joiner = ''
    when :short
      dividers = {
        :years => 'y', :months => 'mo', :weeks => 'w', :days => 'd', :hours => 'h', :minutes => 'm', :seconds => 's' }
    when :default
      dividers = {
        :years => ' yr', :months => ' mo', :weeks => ' wk', :days => ' day', :hours => ' hr', :minutes => ' min', :seconds => ' sec',
        :pluralize => true }
    when :long
      dividers = {
        :years => ' year', :months => ' month', :weeks => ' week', :days => ' day', :hours => ' hour', :minutes => ' minute', :seconds => ' second',
        :pluralize => true }
    when :chrono
      dividers = {
        :years => ':', :months => ':', :weeks => ':', :days => ':', :hours => ':', :minutes => ':', :seconds => ':', :keep_zero => true }
      process = lambda do |str|
        # Pad zeros
        # Get rid of lead off times if they are zero
        # Get rid of lead off zero
        # Get rid of trailing :
        divider = ':'
        str.split(divider).map { |n|
          # add zeros only if n is an integer
          n.include?('.') ? ("%04.#{decimal_places}f" % n) : ("%02d" % n)
        }.join(divider).gsub(/^(00:)+/, '').gsub(/^0/, '').gsub(/:$/, '')
      end
      joiner = ''
    end

    result = [:years, :months, :weeks, :days, :hours, :minutes, :seconds].map do |t|
      next if t == :weeks && !opts[:weeks]
      num = eval(t.to_s)
      num = ("%.#{decimal_places}f" % num) if num.is_a?(Float) && t == :seconds
      keep_zero = dividers[:keep_zero]
      keep_zero ||= opts[:keep_zero] if t == :seconds
      humanize_time_unit( num, dividers[t], dividers[:pluralize], keep_zero )
    end.compact!

    result = result[0...opts[:units]] if opts[:units]

    result = result.join(joiner)

    if process
      result = process.call(result)
    end

    result.length == 0 ? nil : result

  end

private

  def humanize_time_unit(number, unit, pluralize, keep_zero)
    return nil if number == 0 && !keep_zero
    res = "#{number}#{unit}"
    # A poor man's pluralizer
    res << 's' if !(number == 1) && pluralize
    res
  end

  def calculate_from_words(string, opts)
    val = 0
    words = string.split(' ')
    words.each_with_index do |v, k|
      if v =~ float_matcher
        val += (convert_to_number(v) * duration_units_seconds_multiplier(words[k + 1] || (opts[:default_unit] || 'seconds')))
      end
    end
    val
  end

  def cleanup(string)
    res = string.downcase
    res = filter_by_type(Numerizer.numerize(res))
    res = res.gsub(float_matcher) {|n| " #{n} "}.squeeze(' ').strip
    res = filter_through_white_list(res)
  end

  def convert_to_number(string)
    string.to_f % 1 > 0 ? string.to_f : string.to_i
  end

  def duration_units_list
    %w(seconds minutes hours days weeks months years)
  end
  def duration_units_seconds_multiplier(unit)
    return 0 unless duration_units_list.include?(unit)
    case unit
    when 'years';   31557600
    when 'months';  3600 * 24 * 30
    when 'weeks';   3600 * 24 * 7
    when 'days';    3600 * 24
    when 'hours';   3600
    when 'minutes'; 60
    when 'seconds'; 1
    end
  end

  # Parse 3:41:59 and return 3 hours 41 minutes 59 seconds
  def filter_by_type(string)
    chrono_units_list = duration_units_list.reject {|v| v == "weeks"}
    if string.gsub(' ', '') =~ /#{float_matcher}(:#{float_matcher})+/
      res = []
      string.gsub(' ', '').split(':').reverse.each_with_index do |v,k|
        return unless chrono_units_list[k]
        res << "#{v} #{chrono_units_list[k]}"
      end
      res = res.reverse.join(' ')
    else
      res = string
    end
    res
  end

  def float_matcher
    /[0-9]*\.?[0-9]+/
  end

  # Get rid of unknown words and map found
  # words to defined time units
  def filter_through_white_list(string)
    res = []
    string.split(' ').each do |word|
      if word =~ float_matcher
        res << word.strip
        next
      end
      stripped_word = word.strip.gsub(/^,/, '').gsub(/,$/, '')
      if mappings.has_key?(stripped_word)
        res << mappings[stripped_word]
      elsif !join_words.include?(stripped_word) and ChronicDuration.raise_exceptions
        raise DurationParseError, "An invalid word #{word.inspect} was used in the string to be parsed."
      end
    end
    # add '1' at front if string starts with something recognizable but not with a number, like 'day' or 'minute 30sec' 
    res.unshift(1) if res.length > 0 && mappings[res[0]]  
    res.join(' ')
  end

  def mappings
    {
      'seconds' => 'seconds',
      'second'  => 'seconds',
      'secs'    => 'seconds',
      'sec'     => 'seconds',
      's'       => 'seconds',
      'minutes' => 'minutes',
      'minute'  => 'minutes',
      'mins'    => 'minutes',
      'min'     => 'minutes',
      'm'       => 'minutes',
      'hours'   => 'hours',
      'hour'    => 'hours',
      'hrs'     => 'hours',
      'hr'      => 'hours',
      'h'       => 'hours',
      'days'    => 'days',
      'day'     => 'days',
      'dy'      => 'days',
      'd'       => 'days',
      'weeks'   => 'weeks',
      'week'    => 'weeks',
      'w'       => 'weeks',
      'months'  => 'months',
      'mo'      => 'months',
      'mos'     => 'months',
      'month'   => 'months',
      'years'   => 'years',
      'year'    => 'years',
      'yrs'     => 'years',
      'yr'      => 'years',
      'y'       => 'years'
    }
  end

  def join_words
    ['and', 'with', 'plus']
  end
end