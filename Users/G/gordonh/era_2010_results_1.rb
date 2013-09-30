# ERA 2010 Results Scraper

require 'nokogiri'
require 'open-uri'
 
ARC_DOMAIN = 'http://www.arc.gov.au/'
INDEX_URL = ARC_DOMAIN + 'era/outcomes_2010/institutionindex'
MAX_INST = 50



CLUSTER_FORS = [ '10', '12', '11' ]

def scrape_index(page)
  puts "Reading index..."
  urls = {}
  count = 0
  page.css('tr').collect{|x| x.css('td')}.reject{|x| x.length == 0}.collect do |row|
    link = row.at_css('a')
    if link and ( MAX_INST and count < MAX_INST )
      puts "Index: " + link.inner_text
      urls[link.inner_text] = link['href']
      count += 1
    end
  end
  urls
end

def force_string(str)
  cooked = ''  
  if str 
    cooked = '="' + str + '"'
  end
  cooked
end


index_html = ScraperWiki.scrape(INDEX_URL)
index_page = Nokogiri::HTML(index_html)
inst_links = scrape_index(index_page)

totals = {}

inst_links.each do |institution,inst_url|
  inst_html = ScraperWiki.scrape(ARC_DOMAIN + inst_url)
  puts "Reading data for " + institution
  page = Nokogiri::HTML(inst_html)
  page.css('tr').collect {|x| x.css('td')}.reject{ |x| x.length == 0}.collect do |row|
    record = {}
    record['Institution'] = institution.rstrip
    record['Cluster']   = row.css('td')[0].inner_text.rstrip
    record['FORName']   = row.css('td')[2].inner_text.rstrip
    record['Rating']    = row.css('td')[3].inner_text.rstrip
    rawfor              = row.css('td')[1].inner_text.rstrip

    record['Cluster'] = record['Cluster'][/^[A-Z]+/]
    record['FOR']     = rawfor[/^[0-9]+/]
    record['FOR2']    = rawfor[/^[0-9][0-9]/]
    if rawfor.length > 2
      record['FOR4']  = rawfor[/^[0-9][0-9][0-9][0-9]/]
    else
      record['FOR4'] = ''
    end

    if CLUSTER_FORS.include?(record['FOR2'])
      record['FOR2'] = record['FOR2'] + record['Cluster']
      record['FOR'] = record['FOR'] + record['Cluster']
    end

    record['FOR2'] = force_string(record['FOR2'])
    record['FOR4'] = force_string(record['FOR4'])

    if record['Rating'][/[1-5]/]
      rating = Integer record['Rating'][/[1-5]/]
      if totals.has_key?(record['FOR'])
        totals[record['FOR']]['total'] += rating
        totals[record['FOR']]['count'] += 1
      else
        totals[record['FOR']] = {
          'count' => 1,
          'total' => rating,
          'Cluster' => record['Cluster'],
          'FORName' => record['FORName'],
          # 'FOR' =>     record['FOR'],
          'FOR2' =>    record['FOR2'],
          'FOR4' =>    record['FOR4'],
          'Cluster' => record['Cluster']
        }
      end
    else
      record['Rating'] = ''
    end
    record.delete('FOR')
    ScraperWiki.save(['Institution', 'FOR2', 'FOR4' ], record)    
  end
end

totals.each do |f, t|
  if t['count'] > 0
    average = (Float t['total']) / (Float t['count'])
    record = {
      'FOR2' =>    t['FOR2'],
      'FOR4' =>    t['FOR4'],
      'Rating' =>  sprintf("%.2f", average),
      'Institution' => 'Average',
      'FORName' => t['FORName'],
      'Cluster' => t['Cluster']
    }
    ScraperWiki.save(['Institution', 'FOR2', 'FOR4'], record)
  end
end


# ERA 2010 Results Scraper

require 'nokogiri'
require 'open-uri'
 
ARC_DOMAIN = 'http://www.arc.gov.au/'
INDEX_URL = ARC_DOMAIN + 'era/outcomes_2010/institutionindex'
MAX_INST = 50



CLUSTER_FORS = [ '10', '12', '11' ]

def scrape_index(page)
  puts "Reading index..."
  urls = {}
  count = 0
  page.css('tr').collect{|x| x.css('td')}.reject{|x| x.length == 0}.collect do |row|
    link = row.at_css('a')
    if link and ( MAX_INST and count < MAX_INST )
      puts "Index: " + link.inner_text
      urls[link.inner_text] = link['href']
      count += 1
    end
  end
  urls
end

def force_string(str)
  cooked = ''  
  if str 
    cooked = '="' + str + '"'
  end
  cooked
end


index_html = ScraperWiki.scrape(INDEX_URL)
index_page = Nokogiri::HTML(index_html)
inst_links = scrape_index(index_page)

totals = {}

inst_links.each do |institution,inst_url|
  inst_html = ScraperWiki.scrape(ARC_DOMAIN + inst_url)
  puts "Reading data for " + institution
  page = Nokogiri::HTML(inst_html)
  page.css('tr').collect {|x| x.css('td')}.reject{ |x| x.length == 0}.collect do |row|
    record = {}
    record['Institution'] = institution.rstrip
    record['Cluster']   = row.css('td')[0].inner_text.rstrip
    record['FORName']   = row.css('td')[2].inner_text.rstrip
    record['Rating']    = row.css('td')[3].inner_text.rstrip
    rawfor              = row.css('td')[1].inner_text.rstrip

    record['Cluster'] = record['Cluster'][/^[A-Z]+/]
    record['FOR']     = rawfor[/^[0-9]+/]
    record['FOR2']    = rawfor[/^[0-9][0-9]/]
    if rawfor.length > 2
      record['FOR4']  = rawfor[/^[0-9][0-9][0-9][0-9]/]
    else
      record['FOR4'] = ''
    end

    if CLUSTER_FORS.include?(record['FOR2'])
      record['FOR2'] = record['FOR2'] + record['Cluster']
      record['FOR'] = record['FOR'] + record['Cluster']
    end

    record['FOR2'] = force_string(record['FOR2'])
    record['FOR4'] = force_string(record['FOR4'])

    if record['Rating'][/[1-5]/]
      rating = Integer record['Rating'][/[1-5]/]
      if totals.has_key?(record['FOR'])
        totals[record['FOR']]['total'] += rating
        totals[record['FOR']]['count'] += 1
      else
        totals[record['FOR']] = {
          'count' => 1,
          'total' => rating,
          'Cluster' => record['Cluster'],
          'FORName' => record['FORName'],
          # 'FOR' =>     record['FOR'],
          'FOR2' =>    record['FOR2'],
          'FOR4' =>    record['FOR4'],
          'Cluster' => record['Cluster']
        }
      end
    else
      record['Rating'] = ''
    end
    record.delete('FOR')
    ScraperWiki.save(['Institution', 'FOR2', 'FOR4' ], record)    
  end
end

totals.each do |f, t|
  if t['count'] > 0
    average = (Float t['total']) / (Float t['count'])
    record = {
      'FOR2' =>    t['FOR2'],
      'FOR4' =>    t['FOR4'],
      'Rating' =>  sprintf("%.2f", average),
      'Institution' => 'Average',
      'FORName' => t['FORName'],
      'Cluster' => t['Cluster']
    }
    ScraperWiki.save(['Institution', 'FOR2', 'FOR4'], record)
  end
end


