  #check i'm running
  puts "wooo"
  
  #this is the for loop. i=page number. 1..62 means iterate over pages 1 to 62
  for i in 1..62
  
    #download the html
html = ScraperWiki.scrape("http://www.lloydstsblondon2012.co.uk/en/carrytheflame/search/?pg=#{i}")

    
    #parse the html
    require 'nokogiri'
    doc = Nokogiri::HTML(html)
    for v in doc.search("table.searchresults tbody tr")
      cells = v.search('td')
      data = {
        'image name' => cells[0].inner_html,
        'county' => cells[1].inner_html,
        'reason' => cells[2].inner_html,
        'age' => cells[3].inner_html
}


      ScraperWiki.save_sqlite(unique_keys=['image name'], data=data)
    
    end 
  end    
    
    
    
  #check i'm running
  puts "wooo"
  
  #this is the for loop. i=page number. 1..62 means iterate over pages 1 to 62
  for i in 1..62
  
    #download the html
html = ScraperWiki.scrape("http://www.lloydstsblondon2012.co.uk/en/carrytheflame/search/?pg=#{i}")

    
    #parse the html
    require 'nokogiri'
    doc = Nokogiri::HTML(html)
    for v in doc.search("table.searchresults tbody tr")
      cells = v.search('td')
      data = {
        'image name' => cells[0].inner_html,
        'county' => cells[1].inner_html,
        'reason' => cells[2].inner_html,
        'age' => cells[3].inner_html
}


      ScraperWiki.save_sqlite(unique_keys=['image name'], data=data)
    
    end 
  end    
    
    
    
