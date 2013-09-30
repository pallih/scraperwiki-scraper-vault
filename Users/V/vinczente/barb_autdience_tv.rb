# Blank Ruby
# ScraperWiki CPU time exceeded is runned as normal

require 'rubygems'
require 'mechanize'
require 'date'
require 'digest/md5'

url = 'http://www.barb.co.uk/report/weeklyViewing'
years = [2012] # should be : (2010..Time.now.year)
weeks = [Date.today.cweek-2] # should be :(1..52)

def end_week_date(week_num, year)
  return Date.commercial( year, week_num, 7 )
end

def construct_url(year, month, week, day)
  return '?period_year[]='+year.to_s+'&period_month[]='+month.to_s.rjust(2, '0')+'&period_week[]='+week.to_s.rjust(2, '0')+'&button_submit=View Figures&period[]='+year.to_s+month.to_s.rjust(2, '0')+'0601'+day.to_s.rjust(2, '0')
end

def parse_url(url, date)
  agent = Mechanize.new
  agent.user_agent_alias = 'Mac Safari'
  page = agent.get(url)
  if(page.at("table.datagrid")!=nil)
  record = {}
      page.at("table.datagrid").search('tr')[1..-1].each do |r|
        if(r.search('td')[0]!=nil)
        record = {
           'channel' => r.search('td')[0].inner_html,
           'avg_daily_reach_number' => r.search('td')[1].inner_html,
           'avg_daily_reach_percanetage' => r.search('td')[2].inner_html,
           'weekly_reach_number' => r.search('td')[3].inner_html,
           'weekly_reach_percentage' => r.search('td')[4].inner_html,
           'avg_week_viewing_time_per_person' => r.search('td')[5].inner_html,
           'share' => r.search('td')[6].inner_html,
           'date' => date.to_s,
           'key' => Digest::MD5.hexdigest(r.search('td')[0].inner_html + '-' + date.to_s)
         }
         ScraperWiki.save_sqlite(['key'], record)
        end
      end
  end
end

years.each do |year|
  weeks.each do |week|
    if(end_week_date(week, year).year <= year && end_week_date(week, year)<= Date.parse(Time.now.strftime('%Y/%m/%d')))
      last_day_of_week = end_week_date(week, year)
      parse_url(url+construct_url(year, last_day_of_week.month, week, last_day_of_week.day),last_day_of_week)
    end
  end
end# Blank Ruby
# ScraperWiki CPU time exceeded is runned as normal

require 'rubygems'
require 'mechanize'
require 'date'
require 'digest/md5'

url = 'http://www.barb.co.uk/report/weeklyViewing'
years = [2012] # should be : (2010..Time.now.year)
weeks = [Date.today.cweek-2] # should be :(1..52)

def end_week_date(week_num, year)
  return Date.commercial( year, week_num, 7 )
end

def construct_url(year, month, week, day)
  return '?period_year[]='+year.to_s+'&period_month[]='+month.to_s.rjust(2, '0')+'&period_week[]='+week.to_s.rjust(2, '0')+'&button_submit=View Figures&period[]='+year.to_s+month.to_s.rjust(2, '0')+'0601'+day.to_s.rjust(2, '0')
end

def parse_url(url, date)
  agent = Mechanize.new
  agent.user_agent_alias = 'Mac Safari'
  page = agent.get(url)
  if(page.at("table.datagrid")!=nil)
  record = {}
      page.at("table.datagrid").search('tr')[1..-1].each do |r|
        if(r.search('td')[0]!=nil)
        record = {
           'channel' => r.search('td')[0].inner_html,
           'avg_daily_reach_number' => r.search('td')[1].inner_html,
           'avg_daily_reach_percanetage' => r.search('td')[2].inner_html,
           'weekly_reach_number' => r.search('td')[3].inner_html,
           'weekly_reach_percentage' => r.search('td')[4].inner_html,
           'avg_week_viewing_time_per_person' => r.search('td')[5].inner_html,
           'share' => r.search('td')[6].inner_html,
           'date' => date.to_s,
           'key' => Digest::MD5.hexdigest(r.search('td')[0].inner_html + '-' + date.to_s)
         }
         ScraperWiki.save_sqlite(['key'], record)
        end
      end
  end
end

years.each do |year|
  weeks.each do |week|
    if(end_week_date(week, year).year <= year && end_week_date(week, year)<= Date.parse(Time.now.strftime('%Y/%m/%d')))
      last_day_of_week = end_week_date(week, year)
      parse_url(url+construct_url(year, last_day_of_week.month, week, last_day_of_week.day),last_day_of_week)
    end
  end
end