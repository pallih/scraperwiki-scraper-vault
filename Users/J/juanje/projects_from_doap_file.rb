# GNOME Projects from doap file
require 'open-uri'
require 'nokogiri'

url = 'http://git.gnome.org/repositories.doap'
doc = Nokogiri::XML(open url)

doc.xpath('//doap:Project').each do |node|
  next if node.xpath('./doap:name').text.empty? 
  next if node.at_xpath('./doap:category').nil? 
 
  category = node.at_xpath('./doap:category')['resource'].split('#').last
  homepage = node.at_xpath('./doap:homepage') || {}
  description = node.at_xpath('./doap:description') ? node.at_xpath('./doap:description').text : ''
  sortdesc = node.xpath('./doap:name').text
  repository = node.at_xpath('./doap:repository/doap:GitRepository/doap:location')['resource']

  data = {
    :name        => repository.split('/').last,
    :sortdesc    => sortdesc.empty? ? "#{name}'s repository" : sortdesc,
    :description => description,
    :homepage    => homepage['resource'] || '',
    :category    => category,
    :repository  => repository
  }
  ScraperWiki.save(unique_keys=[:name], data=data)

end
