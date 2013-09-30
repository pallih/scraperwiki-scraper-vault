# Blank Ruby

require 'nokogiri'           
require 'open-uri'

def leboncoin_parse_page(url)
  html = open(url)
  doc = Nokogiri::HTML(html.read)

  # parse page content
  leboncoin_parse_doc_contents(doc)

  # follow next page (FIXME if not done ?)
  if false
  next_page_url = leboncoin_find_next_page_url_in_doc(doc)
  while !next_page_url.nil? 
     p next_page_url
     next_page_url = leboncoin_parse_page(next_page_url)
  end
  end
end
 
def leboncoin_find_next_page_url_in_doc(doc)
  selectedFound = false

  doc.at_css("ul#paging").children().each do |li|
    a = li.at_css('a')
    if selectedFound && !a.nil? 
      return a.attr('href')
    else 
      if li.attr('class') == 'selected'
        selectedFound = true
      end
    end    
  end

  return nil
end

def leboncoin_parse_doc_contents(doc)
  doc.at_css('div.list-lbc').css("a").each do |classified|
    p classified.attr("href")
  end
end
       
leboncoin_parse_page('http://www.leboncoin.fr/ventes_immobilieres/offres/midi_pyrenees/haute_garonne/?f=a&th=1&ps=3&pe=4&sqs=4&ros=1&roe=3&ret=2&location=Toulouse')



if false
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr").each do |v|
  cells = v.search 'td'
  if cells.count == 12
    data = {
      country: cells[0].inner_html,
      years_in_school: cells[4].inner_html.to_i
    }
    ScraperWiki::save_sqlite(['country'], data)
    #puts data.to_json
  end
end
end# Blank Ruby

require 'nokogiri'           
require 'open-uri'

def leboncoin_parse_page(url)
  html = open(url)
  doc = Nokogiri::HTML(html.read)

  # parse page content
  leboncoin_parse_doc_contents(doc)

  # follow next page (FIXME if not done ?)
  if false
  next_page_url = leboncoin_find_next_page_url_in_doc(doc)
  while !next_page_url.nil? 
     p next_page_url
     next_page_url = leboncoin_parse_page(next_page_url)
  end
  end
end
 
def leboncoin_find_next_page_url_in_doc(doc)
  selectedFound = false

  doc.at_css("ul#paging").children().each do |li|
    a = li.at_css('a')
    if selectedFound && !a.nil? 
      return a.attr('href')
    else 
      if li.attr('class') == 'selected'
        selectedFound = true
      end
    end    
  end

  return nil
end

def leboncoin_parse_doc_contents(doc)
  doc.at_css('div.list-lbc').css("a").each do |classified|
    p classified.attr("href")
  end
end
       
leboncoin_parse_page('http://www.leboncoin.fr/ventes_immobilieres/offres/midi_pyrenees/haute_garonne/?f=a&th=1&ps=3&pe=4&sqs=4&ros=1&roe=3&ret=2&location=Toulouse')



if false
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr").each do |v|
  cells = v.search 'td'
  if cells.count == 12
    data = {
      country: cells[0].inner_html,
      years_in_school: cells[4].inner_html.to_i
    }
    ScraperWiki::save_sqlite(['country'], data)
    #puts data.to_json
  end
end
end