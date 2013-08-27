# Ruby for collection of concerts

$Fecha =""
$Concierto=""
$URL=""
$Reviewer=""

html = ScraperWiki.scrape("http://www.bachtrack.com/reviews/list/concert")
puts html
counter=1
  
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('td[@valign="top"]').each do |row|
    #puts row
    case counter
      when counter=1
        $Fecha=row.text
        counter=counter+1
      when counter=2
       $Concierto=row.text
       $URL=row.css('a').attr('href')
        counter=counter+1
      when counter=3
        $Reviewer=row.text
        counter=counter+1
      when counter=4
         record={}
        record ['ID']= $URL
        record ['Fecha/Localizacion']=$Fecha
        record ['Concierto']=$Concierto
        record ['URL']="http://www.bachtrack.com/"+ $URL
        record ['Reviewer']= $Reviewer
        ScraperWiki.save_sqlite(["ID"], record)
        counter=1
    end
  puts counter.to_s() 

  end

  for t in 21..56
  counter_page= t*50
  
  html = ScraperWiki.scrape("http://www.bachtrack.com/reviews/list/all/"+counter_page.to_s())
  puts html
  counter=1
      
      require 'nokogiri'
      doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@valign="top"]').each do |row|
        #puts row
        case counter
          when counter=1
            $Fecha=row.text
            counter=counter+1
          when counter=2
           $Concierto=row.text
           $URL=row.css('a').attr('href')
            counter=counter+1
          when counter=3
            $Reviewer=row.text
            counter=counter+1
          when counter=4
             record={}
            record ['ID']= $URL
            record ['Fecha/Localizacion']=$Fecha
            record ['Concierto']=$Concierto
            record ['URL']="http://www.bachtrack.com/"+ $URL
            record ['Reviewer']= $Reviewer
            ScraperWiki.save_sqlite(["ID"], record)
            counter=1
        end
      puts counter.to_s() 
  
     end
  end


# Ruby for collection of concerts

$Fecha =""
$Concierto=""
$URL=""
$Reviewer=""

html = ScraperWiki.scrape("http://www.bachtrack.com/reviews/list/concert")
puts html
counter=1
  
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('td[@valign="top"]').each do |row|
    #puts row
    case counter
      when counter=1
        $Fecha=row.text
        counter=counter+1
      when counter=2
       $Concierto=row.text
       $URL=row.css('a').attr('href')
        counter=counter+1
      when counter=3
        $Reviewer=row.text
        counter=counter+1
      when counter=4
         record={}
        record ['ID']= $URL
        record ['Fecha/Localizacion']=$Fecha
        record ['Concierto']=$Concierto
        record ['URL']="http://www.bachtrack.com/"+ $URL
        record ['Reviewer']= $Reviewer
        ScraperWiki.save_sqlite(["ID"], record)
        counter=1
    end
  puts counter.to_s() 

  end

  for t in 21..56
  counter_page= t*50
  
  html = ScraperWiki.scrape("http://www.bachtrack.com/reviews/list/all/"+counter_page.to_s())
  puts html
  counter=1
      
      require 'nokogiri'
      doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@valign="top"]').each do |row|
        #puts row
        case counter
          when counter=1
            $Fecha=row.text
            counter=counter+1
          when counter=2
           $Concierto=row.text
           $URL=row.css('a').attr('href')
            counter=counter+1
          when counter=3
            $Reviewer=row.text
            counter=counter+1
          when counter=4
             record={}
            record ['ID']= $URL
            record ['Fecha/Localizacion']=$Fecha
            record ['Concierto']=$Concierto
            record ['URL']="http://www.bachtrack.com/"+ $URL
            record ['Reviewer']= $Reviewer
            ScraperWiki.save_sqlite(["ID"], record)
            counter=1
        end
      puts counter.to_s() 
  
     end
  end


# Ruby for collection of concerts

$Fecha =""
$Concierto=""
$URL=""
$Reviewer=""

html = ScraperWiki.scrape("http://www.bachtrack.com/reviews/list/concert")
puts html
counter=1
  
  require 'nokogiri'
  doc = Nokogiri::HTML(html, nil, 'utf-8')
  doc.search('td[@valign="top"]').each do |row|
    #puts row
    case counter
      when counter=1
        $Fecha=row.text
        counter=counter+1
      when counter=2
       $Concierto=row.text
       $URL=row.css('a').attr('href')
        counter=counter+1
      when counter=3
        $Reviewer=row.text
        counter=counter+1
      when counter=4
         record={}
        record ['ID']= $URL
        record ['Fecha/Localizacion']=$Fecha
        record ['Concierto']=$Concierto
        record ['URL']="http://www.bachtrack.com/"+ $URL
        record ['Reviewer']= $Reviewer
        ScraperWiki.save_sqlite(["ID"], record)
        counter=1
    end
  puts counter.to_s() 

  end

  for t in 21..56
  counter_page= t*50
  
  html = ScraperWiki.scrape("http://www.bachtrack.com/reviews/list/all/"+counter_page.to_s())
  puts html
  counter=1
      
      require 'nokogiri'
      doc = Nokogiri::HTML(html, nil, 'utf-8')
      doc.search('td[@valign="top"]').each do |row|
        #puts row
        case counter
          when counter=1
            $Fecha=row.text
            counter=counter+1
          when counter=2
           $Concierto=row.text
           $URL=row.css('a').attr('href')
            counter=counter+1
          when counter=3
            $Reviewer=row.text
            counter=counter+1
          when counter=4
             record={}
            record ['ID']= $URL
            record ['Fecha/Localizacion']=$Fecha
            record ['Concierto']=$Concierto
            record ['URL']="http://www.bachtrack.com/"+ $URL
            record ['Reviewer']= $Reviewer
            ScraperWiki.save_sqlite(["ID"], record)
            counter=1
        end
      puts counter.to_s() 
  
     end
  end


