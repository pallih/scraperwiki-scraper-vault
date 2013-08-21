require 'nokogiri'
require 'open-uri'
require 'uri'

today = Date.today

permalinks = {}

2010.upto(today.year) do |year|
  start_month = (year == 2010) ? 10 : 1
  end_month = (year == today.year) ? today.month : 12

  start_month.upto(end_month) do |month|

    url = "http://www.homeoffice.gov.uk/media-centre/speeches/?view=Search+results&simpleOrAdvanced=advanced&type=news&contentType=All&itemTypes=News&searchTerm=&wordLogic=and&searchDateOption=dateRange&fromDay=1&fromMonth=#{month}&fromYear=#{year}&toDay=31&toMonth=#{month}&toYear=#{year}&d-7095067-s=1&d-7095067-p=1&d-7095067-o=1"
    base_url = URI.parse(url)
    
    doc = nil
    begin
      html = open(url).read
      doc = Nokogiri::HTML(html.inspect)
    rescue Exception => e
      puts url
      puts e.to_s
      puts e.backtrace.join("\n")
    end

    if doc
      doc.search('a').each do |a|
        if a['href'].include?('speeches')
          permalink = base_url.merge( a['href'].gsub('\"','') ).to_s.gsub(/\?version=\d+/,'')
          permalinks[permalink] = true        
        end
      end
    end
  end

end

permalinks.delete('http://www.homeoffice.gov.uk/media-centre/speeches/')

ministers = ['Damian Green',
'Nick Herbert',
'Baroness Neville-Jones',
'Baroness Neville Jones',
'Pauline Neville Jones',
'Pauline Neville-Jones',
'James Brokenshire',
'Theresa May',
'Lynne Featherstone']

puts permalinks.size

permalinks.keys.each do |permalink|
  doc = nil
  begin
    html = open(permalink).read
    doc = Nokogiri::HTML(html)
  rescue Exception => e
    puts permalink
    puts e.to_s
    puts e.backtrace.join("\n")
  end

  if doc
    title = (doc.at('h1.article') || doc.at('header h1') ).inner_text
    date = doc.at('.date.article').inner_text
    body = doc.at('.date.article + div').inner_html
    minister_name = nil
  
    minister_name = 'unknown'
    ministers.each do |minister|
      minister_name = minister if title[/#{minister}/]
    end

    if minister_name == 'unknown'
      ministers.each do |minister|      
        minister_name = minister if body[/#{minister}/]
      end
    end

    if minister_name == 'unknown'
      minister_name = 'Home Secretary' if body[/Home Secretary/]
    end
 
    if ['Baroness Neville Jones', 'Pauline Neville Jones', 'Pauline Neville-Jones'].include?(minister_name)
      minister_name = 'Baroness Neville-Jones'
    end

    description = doc.at('.date.article').parent.search('div').first.search('p').first.inner_text

    where = case description
    when /\sat (.+) (on|in)/
      $1.split('.').first.split(' by ').first.strip
    when /\sto (.+) (on|in)/
      $1.split('.').first.split(' by ').first.strip
    when /\sat ([^\.]+)/
      $1.split(' by ').first.strip
    when /\sto ([^\.]+)/
      $1.split(' by ').first.strip
    when /\sin ([^\.]+)/
      $1.split(' by ').first.strip
    else
      'unknown'
    end
    where.sub!(/^the /, '')

    puts "where: " + where
    puts description

    record = {'title' => title, 'permalink' => permalink, 'minister_name' => minister_name, 'given_on' => date, 'body' => body, 'department' => 'Home Office', 'where' => where}

    ScraperWiki.save(['permalink'], record)
  end
end

