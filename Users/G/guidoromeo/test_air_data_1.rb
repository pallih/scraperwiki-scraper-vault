# Blank Ruby
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'pp'

resp = open('http://www.brace.sinanet.apat.it/web/area_download.inizio')
page = Nokogiri.HTML(resp)

results = page.search('select[@name="p_reg"] option').collect{|o| o.inner_text}.delete_if{|t| t=='' }
#'http://www.brace.sinanet.apat.it/zipper/download/ABRUZZO_BAP_2009.zip'
#puts results
pollutants = page.search('select[@name="p_comp"] option').collect{|o| o.inner_text.sub(/\s\(.*\)?$/,'')}.delete_if{|t| t=='' }
results = results.collect{|r| pollutants.collect{|p| "http://www.brace.sinanet.apat.it/zipper/download/#{r}_#{p}"}}.flatten
#puts pollutants
years = page.search('select[@name="p_anno"] option').collect{|o| o.inner_text}
results = results.collect{|r| {'download_link' => years.collect{|p| "#{r}_#{p}"}}}.flatten
ScraperWiki.save(['download_link'], results)
#pp results

#areas.collect do


# Blank Ruby
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'pp'

resp = open('http://www.brace.sinanet.apat.it/web/area_download.inizio')
page = Nokogiri.HTML(resp)

results = page.search('select[@name="p_reg"] option').collect{|o| o.inner_text}.delete_if{|t| t=='' }
#'http://www.brace.sinanet.apat.it/zipper/download/ABRUZZO_BAP_2009.zip'
#puts results
pollutants = page.search('select[@name="p_comp"] option').collect{|o| o.inner_text.sub(/\s\(.*\)?$/,'')}.delete_if{|t| t=='' }
results = results.collect{|r| pollutants.collect{|p| "http://www.brace.sinanet.apat.it/zipper/download/#{r}_#{p}"}}.flatten
#puts pollutants
years = page.search('select[@name="p_anno"] option').collect{|o| o.inner_text}
results = results.collect{|r| {'download_link' => years.collect{|p| "#{r}_#{p}"}}}.flatten
ScraperWiki.save(['download_link'], results)
#pp results

#areas.collect do


