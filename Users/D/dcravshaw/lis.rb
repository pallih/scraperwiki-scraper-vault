#encoding: utf-8 
require 'nokogiri'
require 'typhoeus'

def save_to_whereever(group_id, html)
  doc = Nokogiri::HTML(html)
  name = doc.css('.group-name').inner_text

  stats = {"group" => group_id, "name" => name}

  return if name.nil? or name == ""
  puts "Processing #{group_id}: #{name}"

  doc.css('div .stat').each do |stat|
    next if stat.css('span').inner_text== ""
    name = stat.css('h2').inner_text
    value = stat.css('span').inner_text  
    # puts "#{name}: #{value}"
    stats[name] = value
  end

  ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  temp = ic.iconv(html)
  graphs = temp.scan(/chartId: '(?<chartid>\w+)', dataXML: (?<dataxml>'.*chart>\\n'),/)
  graphs.each{|chart|
    # puts "#{chart[0]}: #{chart[1]}"
    frag =  Nokogiri::XML.fragment(eval %Q{#{chart[1]}})
    labels =frag.css("category").collect{|c| c.attributes['label'].value rescue 'wtf'}
    if labels.empty? 
      labels = frag.css("set").collect{|c| c.attributes['label'].value rescue 'wtf'}
    end
    values = frag.css("set").collect{|c| c.attributes['value'].value rescue 'wtf'}
    # puts labels.inspect
    # puts values.inspect
    stats[chart[0]] =  {"values" => values, "labels" => labels}
  }
 
  ScraperWiki::save_sqlite(["group"], stats) unless stats.keys.length == 2
end

Typhoeus::Hydra.new(max_concurrency: 200)

start = 84000
until start >= 5000000
  start_time = Time.now
  hydra = Typhoeus::Hydra.new
  999.times.map{|i| 
    request = Typhoeus::Request.new("http://www.linkedin.com/groups?groupDashboard=&gid=#{start+i}", followlocation: false)
    request.on_complete do |response|
      save_to_whereever(start + i, response.body)
    end
    hydra.queue(request)
  }
  hydra.run
  end_time = Time.now

  puts "#{start}: Took #{end_time - start_time} seconds"
  start += 1000
end

#encoding: utf-8 
require 'nokogiri'
require 'typhoeus'

def save_to_whereever(group_id, html)
  doc = Nokogiri::HTML(html)
  name = doc.css('.group-name').inner_text

  stats = {"group" => group_id, "name" => name}

  return if name.nil? or name == ""
  puts "Processing #{group_id}: #{name}"

  doc.css('div .stat').each do |stat|
    next if stat.css('span').inner_text== ""
    name = stat.css('h2').inner_text
    value = stat.css('span').inner_text  
    # puts "#{name}: #{value}"
    stats[name] = value
  end

  ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  temp = ic.iconv(html)
  graphs = temp.scan(/chartId: '(?<chartid>\w+)', dataXML: (?<dataxml>'.*chart>\\n'),/)
  graphs.each{|chart|
    # puts "#{chart[0]}: #{chart[1]}"
    frag =  Nokogiri::XML.fragment(eval %Q{#{chart[1]}})
    labels =frag.css("category").collect{|c| c.attributes['label'].value rescue 'wtf'}
    if labels.empty? 
      labels = frag.css("set").collect{|c| c.attributes['label'].value rescue 'wtf'}
    end
    values = frag.css("set").collect{|c| c.attributes['value'].value rescue 'wtf'}
    # puts labels.inspect
    # puts values.inspect
    stats[chart[0]] =  {"values" => values, "labels" => labels}
  }
 
  ScraperWiki::save_sqlite(["group"], stats) unless stats.keys.length == 2
end

Typhoeus::Hydra.new(max_concurrency: 200)

start = 84000
until start >= 5000000
  start_time = Time.now
  hydra = Typhoeus::Hydra.new
  999.times.map{|i| 
    request = Typhoeus::Request.new("http://www.linkedin.com/groups?groupDashboard=&gid=#{start+i}", followlocation: false)
    request.on_complete do |response|
      save_to_whereever(start + i, response.body)
    end
    hydra.queue(request)
  }
  hydra.run
  end_time = Time.now

  puts "#{start}: Took #{end_time - start_time} seconds"
  start += 1000
end

