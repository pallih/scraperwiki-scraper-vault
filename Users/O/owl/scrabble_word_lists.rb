require 'spreadsheet'           
require 'open-uri'
require 'mechanize'

BASE_URL = "http://dictionary-thesaurus.com/"
page = Mechanize.new().get(BASE_URL+"ScrabbleWords.html")
page.links_with(:href=>/xls/).each{|link|
  book = nil
  open BASE_URL+link.href do |f|
    book = Spreadsheet.open f
  end
  records = []
  sheet = book.worksheet 0
  sheet.each_with_index{|row,row_num|
    next if row_num < 5
    keys = []
    row.collect{|v| keys << v  unless v.nil? } 
    records << {"WORD"=>keys[0]} unless keys.empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['WORD'],records,table_name='swdata',verbose=2) unless records.length == 0
}


require 'spreadsheet'           
require 'open-uri'
require 'mechanize'

BASE_URL = "http://dictionary-thesaurus.com/"
page = Mechanize.new().get(BASE_URL+"ScrabbleWords.html")
page.links_with(:href=>/xls/).each{|link|
  book = nil
  open BASE_URL+link.href do |f|
    book = Spreadsheet.open f
  end
  records = []
  sheet = book.worksheet 0
  sheet.each_with_index{|row,row_num|
    next if row_num < 5
    keys = []
    row.collect{|v| keys << v  unless v.nil? } 
    records << {"WORD"=>keys[0]} unless keys.empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['WORD'],records,table_name='swdata',verbose=2) unless records.length == 0
}


require 'spreadsheet'           
require 'open-uri'
require 'mechanize'

BASE_URL = "http://dictionary-thesaurus.com/"
page = Mechanize.new().get(BASE_URL+"ScrabbleWords.html")
page.links_with(:href=>/xls/).each{|link|
  book = nil
  open BASE_URL+link.href do |f|
    book = Spreadsheet.open f
  end
  records = []
  sheet = book.worksheet 0
  sheet.each_with_index{|row,row_num|
    next if row_num < 5
    keys = []
    row.collect{|v| keys << v  unless v.nil? } 
    records << {"WORD"=>keys[0]} unless keys.empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['WORD'],records,table_name='swdata',verbose=2) unless records.length == 0
}


require 'spreadsheet'           
require 'open-uri'
require 'mechanize'

BASE_URL = "http://dictionary-thesaurus.com/"
page = Mechanize.new().get(BASE_URL+"ScrabbleWords.html")
page.links_with(:href=>/xls/).each{|link|
  book = nil
  open BASE_URL+link.href do |f|
    book = Spreadsheet.open f
  end
  records = []
  sheet = book.worksheet 0
  sheet.each_with_index{|row,row_num|
    next if row_num < 5
    keys = []
    row.collect{|v| keys << v  unless v.nil? } 
    records << {"WORD"=>keys[0]} unless keys.empty? 
  }
  ScraperWiki.save_sqlite(unique_keys=['WORD'],records,table_name='swdata',verbose=2) unless records.length == 0
}


