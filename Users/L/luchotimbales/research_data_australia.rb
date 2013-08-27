# Curso web scraping avanzado
# sacar datos de varias páginas web http://www.izbori.ba/rezultati/konacni/parlament_bih/index.htm

def crawlsite(link)

  html = ScraperWiki.scrape(link)
  puts html
  
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('a').each do |row|  
    puts row.attr('href')
  
    if row.attr('href')[0]=="/" then    
      link="http://ands.org.au"+ row.attr('href').to_s()
      puts link
    else
      link=row.attr('href')
    end
  
    record={}
    record ['URL']= link
    record ['Visited']= "True"
    record ['Words']=""
    ScraperWiki.save_sqlite(["URL"], record) 
  end
  
  return "done"
end


URL="http://ands.org.au/"
html = ScraperWiki.scrape(URL)
puts html

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('a').each do |row|  
  puts row.attr('href')

  if row.attr('href')[0]=="/" then    
    link="http://ands.org.au"+ row.attr('href').to_s()
    puts link
    crawlsite(link)
  else
    link=row.attr('href')
  end

  
  
  record={}
  record ['URL']= link
  record ['Visited']= "True"
  record ['Words']=""
  ScraperWiki.save_sqlite(["URL"], record) 

end





# Curso web scraping avanzado
# sacar datos de varias páginas web http://www.izbori.ba/rezultati/konacni/parlament_bih/index.htm

def crawlsite(link)

  html = ScraperWiki.scrape(link)
  puts html
  
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('a').each do |row|  
    puts row.attr('href')
  
    if row.attr('href')[0]=="/" then    
      link="http://ands.org.au"+ row.attr('href').to_s()
      puts link
    else
      link=row.attr('href')
    end
  
    record={}
    record ['URL']= link
    record ['Visited']= "True"
    record ['Words']=""
    ScraperWiki.save_sqlite(["URL"], record) 
  end
  
  return "done"
end


URL="http://ands.org.au/"
html = ScraperWiki.scrape(URL)
puts html

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('a').each do |row|  
  puts row.attr('href')

  if row.attr('href')[0]=="/" then    
    link="http://ands.org.au"+ row.attr('href').to_s()
    puts link
    crawlsite(link)
  else
    link=row.attr('href')
  end

  
  
  record={}
  record ['URL']= link
  record ['Visited']= "True"
  record ['Words']=""
  ScraperWiki.save_sqlite(["URL"], record) 

end





# Curso web scraping avanzado
# sacar datos de varias páginas web http://www.izbori.ba/rezultati/konacni/parlament_bih/index.htm

def crawlsite(link)

  html = ScraperWiki.scrape(link)
  puts html
  
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('a').each do |row|  
    puts row.attr('href')
  
    if row.attr('href')[0]=="/" then    
      link="http://ands.org.au"+ row.attr('href').to_s()
      puts link
    else
      link=row.attr('href')
    end
  
    record={}
    record ['URL']= link
    record ['Visited']= "True"
    record ['Words']=""
    ScraperWiki.save_sqlite(["URL"], record) 
  end
  
  return "done"
end


URL="http://ands.org.au/"
html = ScraperWiki.scrape(URL)
puts html

require 'nokogiri'
doc = Nokogiri::HTML(html, nil, 'utf-8')
doc.search('a').each do |row|  
  puts row.attr('href')

  if row.attr('href')[0]=="/" then    
    link="http://ands.org.au"+ row.attr('href').to_s()
    puts link
    crawlsite(link)
  else
    link=row.attr('href')
  end

  
  
  record={}
  record ['URL']= link
  record ['Visited']= "True"
  record ['Words']=""
  ScraperWiki.save_sqlite(["URL"], record) 

end





