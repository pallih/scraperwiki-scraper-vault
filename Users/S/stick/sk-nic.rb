#!/usr/bin/ruby

require 'rubygems'
require 'open-uri'
require 'zlib'
require 'openssl'
require 'scraperwiki'

# sk-nic has wrong certificate -> workaround it
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

url_domains = 'https://www.sk-nic.sk/documents/domeny_1.txt.gz'
url_registrators = 'https://www.sk-nic.sk/documents/registratori.txt.gz'

open url_registrators do |f|

  gz = Zlib::GzipReader.new(f)
  gz.each do |line|
    line = line.strip
    next if line.start_with?('--') or line.start_with?('Reg ID') or line.empty? 
    line = line.encode('UTF-8', 'ISO-8859-2').split(';')
#    line = line.split(';')
    data = {
      :id => line[0],
      :name => line[1],
      :street => line[2],
      :city => line[3],
      :phone => line[4],
      :email => line[5]
    }
    ScraperWiki.save_sqlite(unique_keys=[:id], data = data, table_name = 'registrars')
  end
  gz.close

end

open url_domains do |f|

  gz = Zlib::GzipReader.new(f)
  gz.each do |line|
    line = line.strip
    next if line.start_with?('--') or line.start_with?('domena') or line.empty? 
    line = line.encode('UTF-8', 'ISO-8859-2').split(';')
#    line = line.split(';')
    data = {
      :domain => line[0],
      :reg_id => line[1],
      :owner_id => line[2],
      :status => line[4],
      :ns1 => line[5],
      :ns2 => line[6],
      :ns3 => line[7],
      :ns4 => line[8],
      :ico => line[9],
      :valid_until => line[10]
    }
    ScraperWiki.save_sqlite(unique_keys=[:domain], data = data, table_name = 'domeny')
  end
  gz.close

end