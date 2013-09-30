ScraperWiki.save_metadata('data_columns', ['Route', 'StartDate', 'Section', 'EndDate', 'Region'])

html = ScraperWiki.scrape('http://www.cd.cz/cd-online/vyluky/')

require 'nokogiri'

doc = Nokogiri::HTML(html)
doc.css('div.underline').each { |mainblock|
  record = Hash.new

  route = mainblock.xpath('h5/text()').to_s.gsub('|', '')
  mainblock.css('table.nostyle').each { |attrblock|
    r1, r2 = attrblock.css('tr')[0], attrblock.css('tr')[1]
    startdate, section, enddate, region = 
      r1.css('td')[0].to_str, r1.css('td')[1].to_str, r2.css('td')[0].to_str, r2.css('td')[1].to_str

    record['Route'] = route
    record['StartDate'] = startdate[11, startdate.length]
    record['Section'] = section[6, section.length]
    record['EndDate'] = enddate[19, enddate.length]
    record['Region'] = region[6, region.length]

    #record.each { |key, value| puts "#{key}: #{value}" }
    #puts
    
    ScraperWiki.save('Route', record)
  }
}ScraperWiki.save_metadata('data_columns', ['Route', 'StartDate', 'Section', 'EndDate', 'Region'])

html = ScraperWiki.scrape('http://www.cd.cz/cd-online/vyluky/')

require 'nokogiri'

doc = Nokogiri::HTML(html)
doc.css('div.underline').each { |mainblock|
  record = Hash.new

  route = mainblock.xpath('h5/text()').to_s.gsub('|', '')
  mainblock.css('table.nostyle').each { |attrblock|
    r1, r2 = attrblock.css('tr')[0], attrblock.css('tr')[1]
    startdate, section, enddate, region = 
      r1.css('td')[0].to_str, r1.css('td')[1].to_str, r2.css('td')[0].to_str, r2.css('td')[1].to_str

    record['Route'] = route
    record['StartDate'] = startdate[11, startdate.length]
    record['Section'] = section[6, section.length]
    record['EndDate'] = enddate[19, enddate.length]
    record['Region'] = region[6, region.length]

    #record.each { |key, value| puts "#{key}: #{value}" }
    #puts
    
    ScraperWiki.save('Route', record)
  }
}