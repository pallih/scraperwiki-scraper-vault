require 'rubygems'
require 'spreadsheet'
require 'open-uri'

data_tv='http://www.teleoff.gov.sk/data/files/707.xls'
data_rozhlas='http://www.teleoff.gov.sk/data/files/17561.xls'

id = 0

# rozhlas is disabled because spreadsheet gem throws:
# Unknown Codepage 0x2a05 exception :-(

=begin

open data_rozhlas do |f|
  book = Spreadsheet.open f
  sheet = book.worksheet 0
  sheet.each(4) { |r|
    lon = r[5].nil? ? nil : r[5].split(' ').collect{ |x| x.to_f } # E
    lat = r[6].nil? ? nil : r[6].split(' ').collect{ |x| x.to_f } # F
    data = {
      :id => id,
      :type => 'rozhlas',
      :name => r[4], # E
      :freq => r[1], # B
      :prog => r[2], # C
      :pi => r[3], # D
      :lon => lon.nil? ? nil : lon[0] + lon[1]/60 + lon[2]/3600,
      :lat => lat.nil? ? nil : lat[0] + lon[1]/60 + lon[2]/3600,
      :alt => r[7], # H
      :erp => r[8], # I
      :ant_diagram => r[9], # J
      :haat => r[10], # K
      :polar => r[11], # L
      :ant_height => r[12] # M
    }
    # N - AW
    (0..35).each { |x|
      data[ "sup#{x*10}".to_sym ] = r[13+x]
    }
    id += 1
    ScraperWiki.save_sqlite(unique_keys=[:id], data=data)
  }
end

=end

open data_tv do |f|
  book = Spreadsheet.open f
  sheet = book.worksheet 0
  sheet.each(4) { |r|
    lon = r[4].nil? ? nil : r[4].split(' ').collect{ |x| x.to_f } # E
    lat = r[5].nil? ? nil : r[5].split(' ').collect{ |x| x.to_f } # F
    data = {
      :id => id,
      :type => 'tv',
      :name => r[0], # A
      :chan => r[1].to_i, # B
      :prog => r[2], # C
      :erp_db => r[3], # D
      :lon => lon.nil? ? nil : lon[0] + lon[1]/60 + lon[2]/3600,
      :lat => lat.nil? ? nil : lat[0] + lon[1]/60 + lon[2]/3600,
      :alt => r[6], # G
      :offset => r[7], # H
      :erp => r[8], # I
      :ant_diagram => r[9], # J
      :polar => r[10], # K
      :ant_height => r[11] # L
    }
    # M - AV
    (0..35).each { |x|
      data[ "sup#{x*10}".to_sym ] = r[12+x]
    }
    id += 1
    ScraperWiki.save_sqlite(unique_keys=[:id], data=data) if data[:chan] > 0
  }
end