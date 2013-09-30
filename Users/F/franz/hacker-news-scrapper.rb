require 'nokogiri'
require 'open-uri'

seedUrl='http://news.ycombinator.com/news'

def fetchHackerNews(url)
    puts '---------------'
    puts url
    html = ScraperWiki.scrape(url)
    puts html
    doc = Nokogiri::HTML(html)
   
    dataA = Array.new
    
 
    i = 0
    doc.search('td.subtext').each do |d|
    dataA[i]={}
    dataA[i]['time']=Time.now
      a=d.search('a')
      #puts a
      dataA[i]['user']=a[0].text
      dataA[i]['comment']='http://news.ycombinator.com/'+a[1].attribute('href').text
      
      dataA[i]['points']=d.search('span').text.gsub(/\spoints/,'')
  
    #puts i 
     #puts d
    i = i+1
    end
    
    j = 0
    doc.search('td.title').each do |d|
      puts d
      if d
        puts d
        d.search('a').each do |anchor|
          #puts anchor
          if anchor
if anchor.attribute('href') && (anchor.attribute('href').text[0,7] == 'http://' || anchor.attribute('href').text[0,8] == 'https://')
             dataA[j]['url'] = anchor.attribute('href').text
             dataA[j]['title'] = anchor.text
             dataA[j]['entrydomain'] = d.search('.comhead').text.gsub(/\(/,'').gsub(/\)/,'')
          # puts entrydomain
             puts dataA[j]
             j = j +1
            else
             
            # nextpage = 'http://news.ycombinator.com'+anchor.attribute('href').text
            # puts nextpage
            # newData = fetchHackerNews(nextpage)
            # dataA.push(newData)
            end
           end
        end
      end
      
        end
    return dataA
end

da = fetchHackerNews(seedUrl)
da.each do |d|
  ScraperWiki.save(['user','comment','points', 'url',  'title','entrydomain','time'], d)
      
endrequire 'nokogiri'
require 'open-uri'

seedUrl='http://news.ycombinator.com/news'

def fetchHackerNews(url)
    puts '---------------'
    puts url
    html = ScraperWiki.scrape(url)
    puts html
    doc = Nokogiri::HTML(html)
   
    dataA = Array.new
    
 
    i = 0
    doc.search('td.subtext').each do |d|
    dataA[i]={}
    dataA[i]['time']=Time.now
      a=d.search('a')
      #puts a
      dataA[i]['user']=a[0].text
      dataA[i]['comment']='http://news.ycombinator.com/'+a[1].attribute('href').text
      
      dataA[i]['points']=d.search('span').text.gsub(/\spoints/,'')
  
    #puts i 
     #puts d
    i = i+1
    end
    
    j = 0
    doc.search('td.title').each do |d|
      puts d
      if d
        puts d
        d.search('a').each do |anchor|
          #puts anchor
          if anchor
if anchor.attribute('href') && (anchor.attribute('href').text[0,7] == 'http://' || anchor.attribute('href').text[0,8] == 'https://')
             dataA[j]['url'] = anchor.attribute('href').text
             dataA[j]['title'] = anchor.text
             dataA[j]['entrydomain'] = d.search('.comhead').text.gsub(/\(/,'').gsub(/\)/,'')
          # puts entrydomain
             puts dataA[j]
             j = j +1
            else
             
            # nextpage = 'http://news.ycombinator.com'+anchor.attribute('href').text
            # puts nextpage
            # newData = fetchHackerNews(nextpage)
            # dataA.push(newData)
            end
           end
        end
      end
      
        end
    return dataA
end

da = fetchHackerNews(seedUrl)
da.each do |d|
  ScraperWiki.save(['user','comment','points', 'url',  'title','entrydomain','time'], d)
      
end