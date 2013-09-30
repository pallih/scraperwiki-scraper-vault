require 'rubygems'
require 'open-uri'
require 'roo'

transmitters = ['http://www.rada-rtv.sk/_cms/data/modules/download/1244028058_Prehlad_vlastnickych_struktur_televiznych_vysielatelov.xls','http://www.rada-rtv.sk/_cms/data/modules/download/1244028475_Prehlad_vlastnickych_struktur_rozhlasovych_vysielatelov.xls']

id = 1

transmitters.each do |transmitter|
  sheet = Excel.new(transmitter)
  sheet.default_sheet = sheet.sheets.first

  4.upto(sheet.last_row) do |line|
    if sheet.cell(line,'D').is_a?(Numeric)
      licence = sheet.cell(line,'D').to_i
    else
      licence = sheet.cell(line,'D')
    end
    data = {
      :id => id,
      :company => sheet.cell(line,'B'),
      :city => sheet.cell(line,'C'),
      :licence_number => licence,
      :basic_capital => sheet.cell(line,'E').to_i,
      :corporators => sheet.cell(line,'F'),
      :statutory_body => sheet.cell(line,'G')
    }
    ScraperWiki.save_sqlite(unique_keys=[:id], data=data)
    id += 1
  end
end
require 'rubygems'
require 'open-uri'
require 'roo'

transmitters = ['http://www.rada-rtv.sk/_cms/data/modules/download/1244028058_Prehlad_vlastnickych_struktur_televiznych_vysielatelov.xls','http://www.rada-rtv.sk/_cms/data/modules/download/1244028475_Prehlad_vlastnickych_struktur_rozhlasovych_vysielatelov.xls']

id = 1

transmitters.each do |transmitter|
  sheet = Excel.new(transmitter)
  sheet.default_sheet = sheet.sheets.first

  4.upto(sheet.last_row) do |line|
    if sheet.cell(line,'D').is_a?(Numeric)
      licence = sheet.cell(line,'D').to_i
    else
      licence = sheet.cell(line,'D')
    end
    data = {
      :id => id,
      :company => sheet.cell(line,'B'),
      :city => sheet.cell(line,'C'),
      :licence_number => licence,
      :basic_capital => sheet.cell(line,'E').to_i,
      :corporators => sheet.cell(line,'F'),
      :statutory_body => sheet.cell(line,'G')
    }
    ScraperWiki.save_sqlite(unique_keys=[:id], data=data)
    id += 1
  end
end
