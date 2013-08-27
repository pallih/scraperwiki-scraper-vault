# Blank Ruby

$concierto={}, $location={}, $performer={}, $fecha={}
$mes={}
$mes=["01","02","03","04", "05", "06","07","08","09","10","11","12"]
$agno=["2012"]

for l in 2..11
    num_concierto=0
    
    url= "http://www.cbso.co.uk/?page=concerts&m="+ $mes[l]+"&y=2012&s.x=15&s.y=11&s=Go"
    html= ScraperWiki.scrape(url)
    puts html
    
    require 'nokogiri'
    
    doc = Nokogiri::HTML(html)
    doc.search('h2> a').each do |fecha|
      $fecha[num_concierto]= fecha.inner_html
      num_concierto=num_concierto+1
    end
    puts "fechas done: "+ $fechas.to_s()
    
    num_concierto=0
    doc.search('p[@class="title"]').each do |concierto|
      ic = Iconv.new('windows-1252//IGNORE', 'windows-1252')
      temp = ic.iconv(concierto.inner_html)
      $concierto [num_concierto]= temp
      num_concierto=num_concierto+1
    end
    puts "concierto done: "+ $concierto.to_s() 

    num_concierto=0
    doc.search('p[@class="location"]').each do |location|
      ic = Iconv.new('windows-1252//IGNORE', 'windows-1252')
      temp = ic.iconv(location.inner_html)
      $location[num_concierto]= temp
      num_concierto=num_concierto+1
    end
    puts "location done: "+ $location.to_s()

    num_concierto=0
    doc.search('p[@class="performers"]').each do |performer|
      ic = Iconv.new('iso-8859-1//IGNORE', 'iso-8859-1')
      temp = ic.iconv(performer.inner_html)
      $performer[num_concierto]= temp
      num_concierto=num_concierto+1
    end
    puts "performer done: "+ $performer.to_s()
    puts "numero concierto: "+ num_concierto.to_s()
    
    for j in 0..num_concierto-1
                
        record={}
        
        puts $mes[l]
        record ['ID']=  "2012_"+ $mes[l] +"_"+ j.to_s()
        record ['fecha']= $fecha[j]
        record ['year']= "2012"
        record ['Concierto']= $concierto[j]
        record ['Location']= $location[j]
        puts record ['Location']
        record ['Performer']= $performer[j]
        puts "record: "+ record.to_s()
        ScraperWiki.save_sqlite(["ID"], record)
        puts "Luis"
    end
end# Blank Ruby

$concierto={}, $location={}, $performer={}, $fecha={}
$mes={}
$mes=["01","02","03","04", "05", "06","07","08","09","10","11","12"]
$agno=["2012"]

for l in 2..11
    num_concierto=0
    
    url= "http://www.cbso.co.uk/?page=concerts&m="+ $mes[l]+"&y=2012&s.x=15&s.y=11&s=Go"
    html= ScraperWiki.scrape(url)
    puts html
    
    require 'nokogiri'
    
    doc = Nokogiri::HTML(html)
    doc.search('h2> a').each do |fecha|
      $fecha[num_concierto]= fecha.inner_html
      num_concierto=num_concierto+1
    end
    puts "fechas done: "+ $fechas.to_s()
    
    num_concierto=0
    doc.search('p[@class="title"]').each do |concierto|
      ic = Iconv.new('windows-1252//IGNORE', 'windows-1252')
      temp = ic.iconv(concierto.inner_html)
      $concierto [num_concierto]= temp
      num_concierto=num_concierto+1
    end
    puts "concierto done: "+ $concierto.to_s() 

    num_concierto=0
    doc.search('p[@class="location"]').each do |location|
      ic = Iconv.new('windows-1252//IGNORE', 'windows-1252')
      temp = ic.iconv(location.inner_html)
      $location[num_concierto]= temp
      num_concierto=num_concierto+1
    end
    puts "location done: "+ $location.to_s()

    num_concierto=0
    doc.search('p[@class="performers"]').each do |performer|
      ic = Iconv.new('iso-8859-1//IGNORE', 'iso-8859-1')
      temp = ic.iconv(performer.inner_html)
      $performer[num_concierto]= temp
      num_concierto=num_concierto+1
    end
    puts "performer done: "+ $performer.to_s()
    puts "numero concierto: "+ num_concierto.to_s()
    
    for j in 0..num_concierto-1
                
        record={}
        
        puts $mes[l]
        record ['ID']=  "2012_"+ $mes[l] +"_"+ j.to_s()
        record ['fecha']= $fecha[j]
        record ['year']= "2012"
        record ['Concierto']= $concierto[j]
        record ['Location']= $location[j]
        puts record ['Location']
        record ['Performer']= $performer[j]
        puts "record: "+ record.to_s()
        ScraperWiki.save_sqlite(["ID"], record)
        puts "Luis"
    end
end# Blank Ruby

$concierto={}, $location={}, $performer={}, $fecha={}
$mes={}
$mes=["01","02","03","04", "05", "06","07","08","09","10","11","12"]
$agno=["2012"]

for l in 2..11
    num_concierto=0
    
    url= "http://www.cbso.co.uk/?page=concerts&m="+ $mes[l]+"&y=2012&s.x=15&s.y=11&s=Go"
    html= ScraperWiki.scrape(url)
    puts html
    
    require 'nokogiri'
    
    doc = Nokogiri::HTML(html)
    doc.search('h2> a').each do |fecha|
      $fecha[num_concierto]= fecha.inner_html
      num_concierto=num_concierto+1
    end
    puts "fechas done: "+ $fechas.to_s()
    
    num_concierto=0
    doc.search('p[@class="title"]').each do |concierto|
      ic = Iconv.new('windows-1252//IGNORE', 'windows-1252')
      temp = ic.iconv(concierto.inner_html)
      $concierto [num_concierto]= temp
      num_concierto=num_concierto+1
    end
    puts "concierto done: "+ $concierto.to_s() 

    num_concierto=0
    doc.search('p[@class="location"]').each do |location|
      ic = Iconv.new('windows-1252//IGNORE', 'windows-1252')
      temp = ic.iconv(location.inner_html)
      $location[num_concierto]= temp
      num_concierto=num_concierto+1
    end
    puts "location done: "+ $location.to_s()

    num_concierto=0
    doc.search('p[@class="performers"]').each do |performer|
      ic = Iconv.new('iso-8859-1//IGNORE', 'iso-8859-1')
      temp = ic.iconv(performer.inner_html)
      $performer[num_concierto]= temp
      num_concierto=num_concierto+1
    end
    puts "performer done: "+ $performer.to_s()
    puts "numero concierto: "+ num_concierto.to_s()
    
    for j in 0..num_concierto-1
                
        record={}
        
        puts $mes[l]
        record ['ID']=  "2012_"+ $mes[l] +"_"+ j.to_s()
        record ['fecha']= $fecha[j]
        record ['year']= "2012"
        record ['Concierto']= $concierto[j]
        record ['Location']= $location[j]
        puts record ['Location']
        record ['Performer']= $performer[j]
        puts "record: "+ record.to_s()
        ScraperWiki.save_sqlite(["ID"], record)
        puts "Luis"
    end
end