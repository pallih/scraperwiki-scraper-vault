# GNOME git projects
require 'open-uri'
require 'nokogiri'
require 'openssl'

OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

url = 'https://git.gnome.org/repositories.doap'
doc = Nokogiri::XML(open url)

doc.xpath('//doap:Project').each do |node|
  next if node.xpath('./doap:name').text.empty? 
 
  category_ref = node.at_xpath('./doap:category').nil? ? 'Other' : node.at_xpath('./doap:category')['resource']
  category = category_ref.include?('#') ? category_ref.split('#').last.capitalize : 'Other'
  homepage = node.at_xpath('./doap:homepage') || {}
  description = node.at_xpath('./doap:description') ? node.at_xpath('./doap:description').text : ''
  shortdesc = node.xpath('./doap:name').text
  shortdesc = shortdesc.empty? ? "#{name}'s repository" : shortdesc
  repository = node.at_xpath('./doap:repository/doap:GitRepository/doap:location')['resource']

  data = {
    :name        => repository.split('/').last,
    :description => description.empty? ? shortdesc : description ,
    :homepage    => homepage['resource'] || 'http://projects.gnome.org/',
    :category    => category,
    :repository  => repository
  }
  ScraperWiki::save_sqlite(unique_keys=[:name], data=data)

end




# GNOME git projects
require 'open-uri'
require 'nokogiri'
require 'openssl'

OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

url = 'https://git.gnome.org/repositories.doap'
doc = Nokogiri::XML(open url)

doc.xpath('//doap:Project').each do |node|
  next if node.xpath('./doap:name').text.empty? 
 
  category_ref = node.at_xpath('./doap:category').nil? ? 'Other' : node.at_xpath('./doap:category')['resource']
  category = category_ref.include?('#') ? category_ref.split('#').last.capitalize : 'Other'
  homepage = node.at_xpath('./doap:homepage') || {}
  description = node.at_xpath('./doap:description') ? node.at_xpath('./doap:description').text : ''
  shortdesc = node.xpath('./doap:name').text
  shortdesc = shortdesc.empty? ? "#{name}'s repository" : shortdesc
  repository = node.at_xpath('./doap:repository/doap:GitRepository/doap:location')['resource']

  data = {
    :name        => repository.split('/').last,
    :description => description.empty? ? shortdesc : description ,
    :homepage    => homepage['resource'] || 'http://projects.gnome.org/',
    :category    => category,
    :repository  => repository
  }
  ScraperWiki::save_sqlite(unique_keys=[:name], data=data)

end




