# encoding: UTF-8
require 'csv'
require "open-uri"

BASE_URL="ftp://ftp.sec.state.vt.us/corporations/"
def get_metadata(key, default)
  begin
    ScraperWiki.get_var(key, default)
  rescue Exception => e
    puts "ERROR: #{e.inspect} during get_metadata(#{key}, #{default})"
  end
end

def save_metadata(key, value)
  begin
   ScraperWiki.save_var(key, value)
  rescue Exception => e
   puts "ERROR: #{e.inspect} during save_metadata(#{key}, #{value})"
   retry
  end
end

files = [["corpscsv.zip",["corpcsv/CORPS.CSV","corpcsv/CORPSCSV.CSV"],"CORP",[["FN_PREFIX","FN_SERIAL","FN_SUFFIX"]]],["gpcsv.zip",["GPCSV.CSV"],"GP",["fn_prefix","file_no"]],
["llpcsv.zip",["LLPCSV.CSV"],"LLP",["fn_prefix","file_no"]],["lpdcsv.zip",["LPDCSV.CSV"],"LPD",["fn_prefix","file_no"]]]

offset = get_metadata("OFFSET",0)
offset = 0 if offset >= files.length
files.each_with_index{|file,idx|
  next if idx < offset
  open(BASE_URL+file[0],{:read_timeout => 1200}) do |o|
    File.open(file[0], "w") { |f| f << o.read }
    %x[unzip #{file[0]}]
  end unless File.exists?(file[0])
  records = []
  file[1].each{|fi|
    CSV.foreach(fi, :quote_char => '"', :col_sep =>',', :row_sep =>:auto, :headers => true,:encoding=>"ISO-8859-1") do |row|
      h = row.to_hash
      h.delete_if {|key, value| key.nil?}
      records << h
    end
  }
  #puts records.inspect
  ScraperWiki.save_sqlite(unique_keys=file[3],records,table_name=file[2],verbose=2) unless records.length == 0
  get_metadata("OFFSET",idx.next)
}

