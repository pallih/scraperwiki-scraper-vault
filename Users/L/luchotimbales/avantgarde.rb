# Blank Ruby


for j in 11..12
  for i in 1..31
    html="http://hemeroteca.lavanguardia.com/edition.html?bd="+i.to_s()+"&bm="+ j.to_s() +"&by=1987"
    puts html
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html)
    #puts doc
    doc.search('ul > li').each do |portada|
      puts portada
    end


  end

end


# Blank Ruby


for j in 11..12
  for i in 1..31
    html="http://hemeroteca.lavanguardia.com/edition.html?bd="+i.to_s()+"&bm="+ j.to_s() +"&by=1987"
    puts html
    
    require 'nokogiri'
    doc = Nokogiri::HTML(html)
    #puts doc
    doc.search('ul > li').each do |portada|
      puts portada
    end


  end

end


