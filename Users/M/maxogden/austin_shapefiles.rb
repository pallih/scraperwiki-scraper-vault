require 'net/ftp'
require 'nokogiri'

Net::FTP.open('ftp.ci.austin.tx.us') do |ftp|
 ftp.login
 files = ftp.chdir('GIS-Data/Regional')
 ftp.getbinaryfile('coa_gis.html', 'coa_gis.html')
end

doc = Nokogiri::HTML.parse(File.read('coa_gis.html'))

shps = doc.css('a').map{|a| a.attr('href') if a.attr('href') =~ /\.zip/ }.compact

p shps