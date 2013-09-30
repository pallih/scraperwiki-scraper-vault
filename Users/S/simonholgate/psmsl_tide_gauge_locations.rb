# encoding: utf-8
require 'nokogiri' 

    html = ScraperWiki.scrape("http://www.psmsl.org/data/obtaining/")
## Get around problems with page encoding
    html.force_encoding('utf-8')
    
    doc = Nokogiri::HTML(html)
    

    for v in doc.search("tbody tr")
      cells = v.search('td')
 
      data = {
        'name' => cells[0].inner_html,
        'id' => cells[1].search('a').inner_html.to_i,
        'lat' => cells[2].search('p').inner_html.to_f,
        'lon' => cells[3].search('p').inner_html.to_f,
        'gloss_id' => cells[4].inner_html.to_i,
        'ctry' => cells[5].search('abbr').first.attributes["title"].value,
        'ctry3' => cells[5].search('abbr').inner_html,
        'updated' => cells[6].inner_html,
        'ctry_code' => cells[7].inner_html.to_i,
        'stn_code' => cells[8].inner_html.to_i
        }


      ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
    end


# encoding: utf-8
require 'nokogiri' 

    html = ScraperWiki.scrape("http://www.psmsl.org/data/obtaining/")
## Get around problems with page encoding
    html.force_encoding('utf-8')
    
    doc = Nokogiri::HTML(html)
    

    for v in doc.search("tbody tr")
      cells = v.search('td')
 
      data = {
        'name' => cells[0].inner_html,
        'id' => cells[1].search('a').inner_html.to_i,
        'lat' => cells[2].search('p').inner_html.to_f,
        'lon' => cells[3].search('p').inner_html.to_f,
        'gloss_id' => cells[4].inner_html.to_i,
        'ctry' => cells[5].search('abbr').first.attributes["title"].value,
        'ctry3' => cells[5].search('abbr').inner_html,
        'updated' => cells[6].inner_html,
        'ctry_code' => cells[7].inner_html.to_i,
        'stn_code' => cells[8].inner_html.to_i
        }


      ScraperWiki.save_sqlite(unique_keys=['id'], data=data)
    end


