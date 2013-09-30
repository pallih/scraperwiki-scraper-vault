# get http://www.bmreports.com/bsp/additional/soapfunctions.php?element=INDO&zT=N&dT=2010-10-29
require 'open-uri'
require 'hpricot'

BASE_URL = 'http://www.bmreports.com/bsp/additional/soapfunctions.php?element=INDO&zT=N&dT='

def total_for_day(date=nil)
  puts "getting data for #{date} from #{BASE_URL + date.to_s}"
  date_data = Hpricot.XML(open(BASE_URL + date.to_s))
  date_data.search('PAGES>SD>SP>SERIES[@ID="INDO"]').inject(0) { |sum, e| sum + e[:VAL].to_i }
end

def sum_of_week_up_to_date(date)
  begin
    (0..6).inject(0)  do |sum, i|
      next_date = date - i
      sum + total_for_day(next_date)
    end
  rescue Exception => e
    return nil
  end
end

def as_percentage number
  one_dp = ((number * 1000).to_i / 10.to_f)
  "#{one_dp}%"
end

results = []

yesterday = Date.today - 1
a_year_ago = Date.today - 366

indo = total_for_day(yesterday)
week_indo = sum_of_week_up_to_date(yesterday)

last_year_indo = total_for_day(a_year_ago)
last_year_week_indo = sum_of_week_up_to_date(a_year_ago)

change = (indo - last_year_indo).to_f / last_year_indo
week_change = (week_indo - last_year_week_indo).to_f / last_year_week_indo

record = { 'date' => yesterday.to_s, 'last_year_date' => a_year_ago.to_s, 'indo' => total_for_day(yesterday), 'indo_percent_change' => as_percentage(change), 'week_indo' => week_indo, 'week_indo_percent_change' => as_percentage(week_change), 'last_year_indo' => last_year_indo, 'last_year_week_indo' => last_year_week_indo }

ScraperWiki.save(['date','last_year_date','indo','indo_percent_change','week_indo','week_indo_percent_change','last_year_indo','last_year_week_indo'], record)
# get http://www.bmreports.com/bsp/additional/soapfunctions.php?element=INDO&zT=N&dT=2010-10-29
require 'open-uri'
require 'hpricot'

BASE_URL = 'http://www.bmreports.com/bsp/additional/soapfunctions.php?element=INDO&zT=N&dT='

def total_for_day(date=nil)
  puts "getting data for #{date} from #{BASE_URL + date.to_s}"
  date_data = Hpricot.XML(open(BASE_URL + date.to_s))
  date_data.search('PAGES>SD>SP>SERIES[@ID="INDO"]').inject(0) { |sum, e| sum + e[:VAL].to_i }
end

def sum_of_week_up_to_date(date)
  begin
    (0..6).inject(0)  do |sum, i|
      next_date = date - i
      sum + total_for_day(next_date)
    end
  rescue Exception => e
    return nil
  end
end

def as_percentage number
  one_dp = ((number * 1000).to_i / 10.to_f)
  "#{one_dp}%"
end

results = []

yesterday = Date.today - 1
a_year_ago = Date.today - 366

indo = total_for_day(yesterday)
week_indo = sum_of_week_up_to_date(yesterday)

last_year_indo = total_for_day(a_year_ago)
last_year_week_indo = sum_of_week_up_to_date(a_year_ago)

change = (indo - last_year_indo).to_f / last_year_indo
week_change = (week_indo - last_year_week_indo).to_f / last_year_week_indo

record = { 'date' => yesterday.to_s, 'last_year_date' => a_year_ago.to_s, 'indo' => total_for_day(yesterday), 'indo_percent_change' => as_percentage(change), 'week_indo' => week_indo, 'week_indo_percent_change' => as_percentage(week_change), 'last_year_indo' => last_year_indo, 'last_year_week_indo' => last_year_week_indo }

ScraperWiki.save(['date','last_year_date','indo','indo_percent_change','week_indo','week_indo_percent_change','last_year_indo','last_year_week_indo'], record)
