require 'rubygems'
require 'spreadsheet'
require 'open-uri'

xls_2010='http://www.justice.gov.sk/Stranky/Sudy/Statistika%20sudy%20a%20sudcovia/dlzka_konania_okresne%20sudy_2010.xls'
xls_2011='http://www.justice.gov.sk/Stranky/Sudy/Statistika%20sudy%20a%20sudcovia/dlzka%20konania_okresne%20sudy_I%20%20p%20%202011.xls'

id = 0

open xls_2010 do |f|
  book = Spreadsheet.open f
  sheet = book.worksheet 0
  # A6 - I59
  (5..58).each{ |r|
    row = sheet.row(r)
    data = {
      :id => id,
      :rok => 2010,
      :okres => row[0], # A
      :trestne => row[1], # B
      :obcianskopravne => row[3], # D
      :obchodne => row[5], # F
      :maloleti => row[7] # H
    }
    id += 1
    ScraperWiki.save_sqlite(unique_keys=[:id], data=data)
  }
end

open xls_2011 do |f|
  book = Spreadsheet.open f
  sheet = book.worksheet 0
  # A6 - E59
  (5..58).each{ |r|
    row = sheet.row(r)
    data = {
      :id => id,
      :rok => 2011,
      :okres => row[0], # A
      :trestne => row[1], # B
      :obcianskopravne => row[2], # C
      :obchodne => row[3], # D
      :maloleti => row[4] # E
    }
    id += 1
    ScraperWiki.save_sqlite(unique_keys=[:id], data=data)
  }
end
require 'rubygems'
require 'spreadsheet'
require 'open-uri'

xls_2010='http://www.justice.gov.sk/Stranky/Sudy/Statistika%20sudy%20a%20sudcovia/dlzka_konania_okresne%20sudy_2010.xls'
xls_2011='http://www.justice.gov.sk/Stranky/Sudy/Statistika%20sudy%20a%20sudcovia/dlzka%20konania_okresne%20sudy_I%20%20p%20%202011.xls'

id = 0

open xls_2010 do |f|
  book = Spreadsheet.open f
  sheet = book.worksheet 0
  # A6 - I59
  (5..58).each{ |r|
    row = sheet.row(r)
    data = {
      :id => id,
      :rok => 2010,
      :okres => row[0], # A
      :trestne => row[1], # B
      :obcianskopravne => row[3], # D
      :obchodne => row[5], # F
      :maloleti => row[7] # H
    }
    id += 1
    ScraperWiki.save_sqlite(unique_keys=[:id], data=data)
  }
end

open xls_2011 do |f|
  book = Spreadsheet.open f
  sheet = book.worksheet 0
  # A6 - E59
  (5..58).each{ |r|
    row = sheet.row(r)
    data = {
      :id => id,
      :rok => 2011,
      :okres => row[0], # A
      :trestne => row[1], # B
      :obcianskopravne => row[2], # C
      :obchodne => row[3], # D
      :maloleti => row[4] # E
    }
    id += 1
    ScraperWiki.save_sqlite(unique_keys=[:id], data=data)
  }
end
