# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://www.march.es/ceacs/publicaciones/working/working.asp?All=1#tablaregistros")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
doc = Nokogiri::HTML(html)

array_id={}
doc.css('table').each do |pub|
    puts pub.content
end

# j=0
# ref={}
# for i in 0..15
#     html2= ScraperWiki.scrape("http://www.march.es/ceacs/publicaciones/working/working.asp?Orden=1&All=1&page="+array_id[i]+"#tablaregistros")
#     doc2 = Nokogiri::HTML(html2)
    
#     doc2.search('table[@summary=Títulos publicados] > tr').each do |refer|
#         ref["Cita"]=refer.inner_html
#         puts refer.inner_html
#         ref["StudyId"]=array_id[i]
#         puts array_id[i]
#         ref["Clave"]=j.to_s()
#         puts j
#         j=j+1
#         ScraperWiki.save(["Clave"], ref)
#     end    
# end



# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://www.march.es/ceacs/publicaciones/working/working.asp?All=1#tablaregistros")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
doc = Nokogiri::HTML(html)

array_id={}
doc.css('table').each do |pub|
    puts pub.content
end

# j=0
# ref={}
# for i in 0..15
#     html2= ScraperWiki.scrape("http://www.march.es/ceacs/publicaciones/working/working.asp?Orden=1&All=1&page="+array_id[i]+"#tablaregistros")
#     doc2 = Nokogiri::HTML(html2)
    
#     doc2.search('table[@summary=Títulos publicados] > tr').each do |refer|
#         ref["Cita"]=refer.inner_html
#         puts refer.inner_html
#         ref["StudyId"]=array_id[i]
#         puts array_id[i]
#         ref["Clave"]=j.to_s()
#         puts j
#         j=j+1
#         ScraperWiki.save(["Clave"], ref)
#     end    
# end



# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://www.march.es/ceacs/publicaciones/working/working.asp?All=1#tablaregistros")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
doc = Nokogiri::HTML(html)

array_id={}
doc.css('table').each do |pub|
    puts pub.content
end

# j=0
# ref={}
# for i in 0..15
#     html2= ScraperWiki.scrape("http://www.march.es/ceacs/publicaciones/working/working.asp?Orden=1&All=1&page="+array_id[i]+"#tablaregistros")
#     doc2 = Nokogiri::HTML(html2)
    
#     doc2.search('table[@summary=Títulos publicados] > tr').each do |refer|
#         ref["Cita"]=refer.inner_html
#         puts refer.inner_html
#         ref["StudyId"]=array_id[i]
#         puts array_id[i]
#         ref["Clave"]=j.to_s()
#         puts j
#         j=j+1
#         ScraperWiki.save(["Clave"], ref)
#     end    
# end



# Welcome to the second ScraperWiki Ruby tutorial

# At the end of the last tutorial we had downloaded the text of
# a webpage. We will do that again ready to process the contents
# of the page

html = ScraperWiki.scrape("http://www.march.es/ceacs/publicaciones/working/working.asp?All=1#tablaregistros")
puts html

# Next we use Nokogiri to extract the values from the HTML source.
# Uncomment the next five lines (i.e. delete the # at the start of the lines)
# and run the scraper again. There should be output in the console.

require 'nokogiri'
doc = Nokogiri::HTML(html)

array_id={}
doc.css('table').each do |pub|
    puts pub.content
end

# j=0
# ref={}
# for i in 0..15
#     html2= ScraperWiki.scrape("http://www.march.es/ceacs/publicaciones/working/working.asp?Orden=1&All=1&page="+array_id[i]+"#tablaregistros")
#     doc2 = Nokogiri::HTML(html2)
    
#     doc2.search('table[@summary=Títulos publicados] > tr').each do |refer|
#         ref["Cita"]=refer.inner_html
#         puts refer.inner_html
#         ref["StudyId"]=array_id[i]
#         puts array_id[i]
#         ref["Clave"]=j.to_s()
#         puts j
#         j=j+1
#         ScraperWiki.save(["Clave"], ref)
#     end    
# end



