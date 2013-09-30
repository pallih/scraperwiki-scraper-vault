require 'cgi'

ScraperWiki.attach('australian_post_offices')

# Counts type of office, and accommodates an asterisk in the data
def percent_of(type)
  type = ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata WHERE type LIKE '#{type}%'" )[0]['COUNT(*)']
  total = ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata" )[0]['COUNT(*)']
  type.to_f/total.to_f*100
end

def number_of(type)
  ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata WHERE type LIKE '#{type}%'" )[0]['COUNT(*)']
end

def render_chart(params)
  chart_url = 'http://chart.googleapis.com/chart?'
  params.each_pair do |k, v|
    chart_url = "#{chart_url}#{k}=#{v}&"
  end
  chart_url[0..-2]
end

type_chart = {
  'cht'  => 'p',
  'chs'  => '550x220',
  'chtt' => 'Types%20of%20Post%20Offices%20in%20Australia',
  'chl'  => CGI.escape(
              "Community Postal Agency (#{number_of('Community Postal Agency')})|Business Centre (#{number_of('Business Centre')})|Post Office (#{number_of('Post Office')})"
            ),
  'chd'  => "t:#{percent_of('Community Postal Agency')},#{percent_of('Business Centre')},#{percent_of('Post Office')}",
  'chco' => 'FFFF00,FF0010'
}

puts "<img src='#{render_chart(type_chart)}'>"
require 'cgi'

ScraperWiki.attach('australian_post_offices')

# Counts type of office, and accommodates an asterisk in the data
def percent_of(type)
  type = ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata WHERE type LIKE '#{type}%'" )[0]['COUNT(*)']
  total = ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata" )[0]['COUNT(*)']
  type.to_f/total.to_f*100
end

def number_of(type)
  ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata WHERE type LIKE '#{type}%'" )[0]['COUNT(*)']
end

def render_chart(params)
  chart_url = 'http://chart.googleapis.com/chart?'
  params.each_pair do |k, v|
    chart_url = "#{chart_url}#{k}=#{v}&"
  end
  chart_url[0..-2]
end

type_chart = {
  'cht'  => 'p',
  'chs'  => '550x220',
  'chtt' => 'Types%20of%20Post%20Offices%20in%20Australia',
  'chl'  => CGI.escape(
              "Community Postal Agency (#{number_of('Community Postal Agency')})|Business Centre (#{number_of('Business Centre')})|Post Office (#{number_of('Post Office')})"
            ),
  'chd'  => "t:#{percent_of('Community Postal Agency')},#{percent_of('Business Centre')},#{percent_of('Post Office')}",
  'chco' => 'FFFF00,FF0010'
}

puts "<img src='#{render_chart(type_chart)}'>"
require 'cgi'

ScraperWiki.attach('australian_post_offices')

# Counts type of office, and accommodates an asterisk in the data
def percent_of(type)
  type = ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata WHERE type LIKE '#{type}%'" )[0]['COUNT(*)']
  total = ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata" )[0]['COUNT(*)']
  type.to_f/total.to_f*100
end

def number_of(type)
  ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata WHERE type LIKE '#{type}%'" )[0]['COUNT(*)']
end

def render_chart(params)
  chart_url = 'http://chart.googleapis.com/chart?'
  params.each_pair do |k, v|
    chart_url = "#{chart_url}#{k}=#{v}&"
  end
  chart_url[0..-2]
end

type_chart = {
  'cht'  => 'p',
  'chs'  => '550x220',
  'chtt' => 'Types%20of%20Post%20Offices%20in%20Australia',
  'chl'  => CGI.escape(
              "Community Postal Agency (#{number_of('Community Postal Agency')})|Business Centre (#{number_of('Business Centre')})|Post Office (#{number_of('Post Office')})"
            ),
  'chd'  => "t:#{percent_of('Community Postal Agency')},#{percent_of('Business Centre')},#{percent_of('Post Office')}",
  'chco' => 'FFFF00,FF0010'
}

puts "<img src='#{render_chart(type_chart)}'>"
require 'cgi'

ScraperWiki.attach('australian_post_offices')

# Counts type of office, and accommodates an asterisk in the data
def percent_of(type)
  type = ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata WHERE type LIKE '#{type}%'" )[0]['COUNT(*)']
  total = ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata" )[0]['COUNT(*)']
  type.to_f/total.to_f*100
end

def number_of(type)
  ScraperWiki.select( "COUNT(*) FROM australian_post_offices.swdata WHERE type LIKE '#{type}%'" )[0]['COUNT(*)']
end

def render_chart(params)
  chart_url = 'http://chart.googleapis.com/chart?'
  params.each_pair do |k, v|
    chart_url = "#{chart_url}#{k}=#{v}&"
  end
  chart_url[0..-2]
end

type_chart = {
  'cht'  => 'p',
  'chs'  => '550x220',
  'chtt' => 'Types%20of%20Post%20Offices%20in%20Australia',
  'chl'  => CGI.escape(
              "Community Postal Agency (#{number_of('Community Postal Agency')})|Business Centre (#{number_of('Business Centre')})|Post Office (#{number_of('Post Office')})"
            ),
  'chd'  => "t:#{percent_of('Community Postal Agency')},#{percent_of('Business Centre')},#{percent_of('Post Office')}",
  'chco' => 'FFFF00,FF0010'
}

puts "<img src='#{render_chart(type_chart)}'>"
