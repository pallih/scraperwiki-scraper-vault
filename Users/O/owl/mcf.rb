# encoding: UTF-8

class Array
  def strip
    self.collect{|a|a.strip}
  end
  def to_i
    self.collect{|a|a.to_i}
  end
end


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

def s_text(str)
  return str.text.strip.gsub(/\u00A0/,' ').pretty
end


def a_text(str)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      tmp << a_text(st)
    }
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

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def append_base(uri,surl)
  return nil if surl.nil? or surl.empty? or surl == "/"
  return surl if surl =~ /^http/
  return uri.strip + ("/"+surl.strip).gsub(/(\/)+/,"/").strip
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

def csv_arr(fn,rec)
  csv_data = CSV.read fn
  headers = csv_data.shift.map {|i| i.gsub(' ','_').strip.downcase unless i.nil? }
  string_data = csv_data.map {|row| row.map {|cell| cell.to_s } }
  list = string_data.map {|row| Hash[*headers.zip(row).flatten]}
  list.collect{|a| 
    a.delete_if{|k,v| v.empty?}
    a.merge(rec) unless rec.empty? 
  }
end

def csv_arr(fn)
  csv_data = CSV.read fn
  headers = csv_data.shift.map {|i| i.to_s }
  string_data = csv_data.map {|row| row.map {|cell| cell.to_s } }
  array_of_hashes = string_data.map {|row| Hash[*headers.zip(row).flatten] }
end


def s_key(str)
  return str.gsub(/\'|’|\+/,"").gsub(/\s+/," ").strip.gsub(" ","_").downcase
end

class RomanNumerals
  @base_digits = {
    1    => 'I',
    4    => 'IV',
    5    => 'V',
    9    => 'IX',
    10   => 'X',
    40   => 'XL',
    50   => 'L',
    90   => 'XC',
    100  => 'C',
    400  => 'CD',
    500  => 'D',
    900  => 'CM',
    1000 => 'M'
  }

  def self.to_roman(value)
    result = ''
    @base_digits.keys.reverse.each do |decimal|
      while value >= decimal
        value -= decimal
        result += @base_digits[decimal]
      end
    end
    result
  end

  def self.to_decimal(value)
    value.upcase!
    result = 0
    @base_digits.values.reverse.each do |roman|
      while value.start_with? roman
        value = value.slice(roman.length, value.length)
        result += @base_digits.key roman
      end
    end
    result
  end
end

def p1(c)
  var_arr = c.to_s.split("").to_i
  lastDig = var_arr.reverse[0]
  minDig = var_arr.sort[0]
  subvar1 = (2 * (var_arr[2])) + (var_arr[1]*1)
  subvar2 = (2 * var_arr[2])+var_arr[1]
  my_pow= ((var_arr[0]*1)+2) ** var_arr[1]
  x=(c*3+subvar1)*1
  y=Math.cos(Math::PI*subvar2)
  answer=x*y
  answer-=my_pow*1
  answer+=(minDig*1)-(lastDig*1)
  answer=answer+subvar2
  return answer.to_i
end
# encoding: UTF-8

class Array
  def strip
    self.collect{|a|a.strip}
  end
  def to_i
    self.collect{|a|a.to_i}
  end
end


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

def s_text(str)
  return str.text.strip.gsub(/\u00A0/,' ').pretty
end


def a_text(str)
  ret = []
  if str.kind_of? (Nokogiri::XML::Element)
    tmp = []
    str.children().each{|st|
      tmp << a_text(st)
    }
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

def attributes(t,attr)
  return (t.nil? or t.first.nil? or t.first.attributes.nil? or t.first.attributes[attr].nil?) ? "" : t.first.attributes[attr].value
end

def append_base(uri,surl)
  return nil if surl.nil? or surl.empty? or surl == "/"
  return surl if surl =~ /^http/
  return uri.strip + ("/"+surl.strip).gsub(/(\/)+/,"/").strip
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

def csv_arr(fn,rec)
  csv_data = CSV.read fn
  headers = csv_data.shift.map {|i| i.gsub(' ','_').strip.downcase unless i.nil? }
  string_data = csv_data.map {|row| row.map {|cell| cell.to_s } }
  list = string_data.map {|row| Hash[*headers.zip(row).flatten]}
  list.collect{|a| 
    a.delete_if{|k,v| v.empty?}
    a.merge(rec) unless rec.empty? 
  }
end

def csv_arr(fn)
  csv_data = CSV.read fn
  headers = csv_data.shift.map {|i| i.to_s }
  string_data = csv_data.map {|row| row.map {|cell| cell.to_s } }
  array_of_hashes = string_data.map {|row| Hash[*headers.zip(row).flatten] }
end


def s_key(str)
  return str.gsub(/\'|’|\+/,"").gsub(/\s+/," ").strip.gsub(" ","_").downcase
end

class RomanNumerals
  @base_digits = {
    1    => 'I',
    4    => 'IV',
    5    => 'V',
    9    => 'IX',
    10   => 'X',
    40   => 'XL',
    50   => 'L',
    90   => 'XC',
    100  => 'C',
    400  => 'CD',
    500  => 'D',
    900  => 'CM',
    1000 => 'M'
  }

  def self.to_roman(value)
    result = ''
    @base_digits.keys.reverse.each do |decimal|
      while value >= decimal
        value -= decimal
        result += @base_digits[decimal]
      end
    end
    result
  end

  def self.to_decimal(value)
    value.upcase!
    result = 0
    @base_digits.values.reverse.each do |roman|
      while value.start_with? roman
        value = value.slice(roman.length, value.length)
        result += @base_digits.key roman
      end
    end
    result
  end
end

def p1(c)
  var_arr = c.to_s.split("").to_i
  lastDig = var_arr.reverse[0]
  minDig = var_arr.sort[0]
  subvar1 = (2 * (var_arr[2])) + (var_arr[1]*1)
  subvar2 = (2 * var_arr[2])+var_arr[1]
  my_pow= ((var_arr[0]*1)+2) ** var_arr[1]
  x=(c*3+subvar1)*1
  y=Math.cos(Math::PI*subvar2)
  answer=x*y
  answer-=my_pow*1
  answer+=(minDig*1)-(lastDig*1)
  answer=answer+subvar2
  return answer.to_i
end
