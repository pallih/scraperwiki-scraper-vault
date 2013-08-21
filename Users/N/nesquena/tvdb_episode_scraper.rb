# coding: utf-8

tvdb_id = 71256
untrusted_string = ScraperWiki::scrape("http://thetvdb.com/?tab=seasonall&id=#{tvdb_id}&lid=7")
ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
html = ic.iconv(untrusted_string + ' ')[0..-2]      
require 'nokogiri'           
doc = Nokogiri::HTML html
doc.search("#maincontent .section tr").each do |v|
  rows = v.search('td')
  next unless rows[0].inner_html =~ /\d/
  season, episode = rows[0].search("a")[0].inner_html.split(" - ").map { |s| s.to_i rescue s }
  title = rows[1].search("a")[0].inner_html.gsub(/&amp;/, '&')
  tvdb_episode_id = rows[1].search("a")[0]['href'][/\&id\=(\d+)/, 1]
  airdate = Time.parse(rows[2].inner_html) rescue nil if rows[2].inner_html.size > 0
  if season && episode && title && airdate
    data = { :title => title, :airdate => airdate, :season => season, :episode => episode, :tvdb_media_id => tvdb_id, :tvdb_episode_id => tvdb_episode_id }
    ScraperWiki::save_sqlite(['title', 'airdate', 'season', 'episode', 'tvdb_media_id', 'tvdb_episode_id'], data)
  end
end