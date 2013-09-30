# Blank Ruby
#encoding: UTF-8 

require 'mechanize'
require 'date'
require 'digest/md5'

require 'cgi'
require 'nokogiri'

require 'iconv'

def remove_tags(html_stuff)
return html_stuff.inner_html.gsub(/<\/?[^>]*>/, "")
end
days = [-1,0,1,2,3,4,5,6]

days.each do |day|
  now = Time.now
  date_now = Time.utc(now.year,now.month,now.day) + (day*60*60*24)
  url = 'http://football-data.enetpulse.com/getContent.php?d='+day.to_s+'&showLeagues=top'
  html = ScraperWiki.scrape(url)
  ic_ignore = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  html = ic_ignore.iconv(html)
  page = Nokogiri::HTML(html)
  
  page.at("table.livetableA").search('tr')[1..-1].each do |r|
  if r.search('span')[0]!=nil
    time = remove_tags(r.search('td')[0])
    if time == 'FT'
      start_at = nil
      status = 'ended'
    elsif time == 'CAN'
      start_at = nil
      status = 'cancelled'
    elsif time.include? ':'
      hours_array = time.split(':')
      starts_at = Time.utc(date_now.year,date_now.month,date_now.day,hours_array[0],hours_array[1])
      status = 'scheduled'
    elsif time.include? "'"
      minutes_diff = time.gsub("'","").to_i
      calculated_date = Time.new - (minutes_diff*60)
      starts_at = Time.utc(calculated_date.year,calculated_date.month,calculated_date.day,calculated_date.hour,calculated_date.min)
      status = 'playing'
    end
    puts r.search('td')
    team1 = remove_tags(r.search('td')[1])
    team2 = remove_tags(r.search('td')[3])
    score = remove_tags(r.search('td')[2]).strip

    if time == 'CAN'
      print score
    end

    if score ==nil || (score !=nil && score.split('-').length < 2)
      score_array = [0,0]
    else
      score_array = score.split('-')
    end

    score_team_1 = score_array[0].to_s.strip
    score_team_2 = score_array[1].to_s.strip

    link = r.search('td')[4].search('a').attribute('href').to_s.split('?')[1]
    link_args = CGI::parse(link)
    if starts_at.nil? 
      starts_at = ''
    else
      starts_at = starts_at.strftime('%Y-%m-%d %H:%M:%S')
    end   
    record = {
       'status' => status,
       'starts_at' => starts_at,
       'team1' => team1,
       'team1_id' => link_args['participant1'][0],
       'score_team_1'=> score_team_1,
       'team2' => team2,
       'team2_id' => link_args['participant2'][0],
       'score_team_2'=> score_team_2,
       'country'=> link_args['country'][0],
       'listing_date' => date_now.strftime('%Y-%m-%d'),
       'key' => Digest::MD5.hexdigest(date_now.to_s + '-' + link_args['participant1'][0] + '-' + link_args['participant2'][0])
     }
    ScraperWiki.save_sqlite(['key'], record)
  end
  end
end# Blank Ruby
#encoding: UTF-8 

require 'mechanize'
require 'date'
require 'digest/md5'

require 'cgi'
require 'nokogiri'

require 'iconv'

def remove_tags(html_stuff)
return html_stuff.inner_html.gsub(/<\/?[^>]*>/, "")
end
days = [-1,0,1,2,3,4,5,6]

days.each do |day|
  now = Time.now
  date_now = Time.utc(now.year,now.month,now.day) + (day*60*60*24)
  url = 'http://football-data.enetpulse.com/getContent.php?d='+day.to_s+'&showLeagues=top'
  html = ScraperWiki.scrape(url)
  ic_ignore = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  html = ic_ignore.iconv(html)
  page = Nokogiri::HTML(html)
  
  page.at("table.livetableA").search('tr')[1..-1].each do |r|
  if r.search('span')[0]!=nil
    time = remove_tags(r.search('td')[0])
    if time == 'FT'
      start_at = nil
      status = 'ended'
    elsif time == 'CAN'
      start_at = nil
      status = 'cancelled'
    elsif time.include? ':'
      hours_array = time.split(':')
      starts_at = Time.utc(date_now.year,date_now.month,date_now.day,hours_array[0],hours_array[1])
      status = 'scheduled'
    elsif time.include? "'"
      minutes_diff = time.gsub("'","").to_i
      calculated_date = Time.new - (minutes_diff*60)
      starts_at = Time.utc(calculated_date.year,calculated_date.month,calculated_date.day,calculated_date.hour,calculated_date.min)
      status = 'playing'
    end
    puts r.search('td')
    team1 = remove_tags(r.search('td')[1])
    team2 = remove_tags(r.search('td')[3])
    score = remove_tags(r.search('td')[2]).strip

    if time == 'CAN'
      print score
    end

    if score ==nil || (score !=nil && score.split('-').length < 2)
      score_array = [0,0]
    else
      score_array = score.split('-')
    end

    score_team_1 = score_array[0].to_s.strip
    score_team_2 = score_array[1].to_s.strip

    link = r.search('td')[4].search('a').attribute('href').to_s.split('?')[1]
    link_args = CGI::parse(link)
    if starts_at.nil? 
      starts_at = ''
    else
      starts_at = starts_at.strftime('%Y-%m-%d %H:%M:%S')
    end   
    record = {
       'status' => status,
       'starts_at' => starts_at,
       'team1' => team1,
       'team1_id' => link_args['participant1'][0],
       'score_team_1'=> score_team_1,
       'team2' => team2,
       'team2_id' => link_args['participant2'][0],
       'score_team_2'=> score_team_2,
       'country'=> link_args['country'][0],
       'listing_date' => date_now.strftime('%Y-%m-%d'),
       'key' => Digest::MD5.hexdigest(date_now.to_s + '-' + link_args['participant1'][0] + '-' + link_args['participant2'][0])
     }
    ScraperWiki.save_sqlite(['key'], record)
  end
  end
end