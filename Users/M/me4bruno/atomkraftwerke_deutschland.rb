require 'nokogiri'

# Create a content string from the content of the node and its subnodes. 
# Content of empty subnodes will be replaced by ' '.
def extractContentOfXmlElement xmlElement
   xmlElementContent = ''
   xmlElement.children.each do |xmlElementChild|
     xmlElementContentPart = ' '
     if !xmlElementChild.content.empty? 
       xmlElementContentPart = xmlElementChild.content
     end
     xmlElementContent = xmlElementContent + xmlElementContentPart
   end
   return xmlElementContent  
end

wikipediaUrl = 'http://de.wikipedia.org'

listAkwHtml = ScraperWiki.scrape(wikipediaUrl + "/wiki/Liste_der_Kernreaktoren_in_Deutschland")
listAkwDoc = Nokogiri::XML(listAkwHtml)

listAkwDoc.css('body * table:nth-of-type(2) tr').each do |singleAkwRow|    
    singleAkwCells = singleAkwRow.css('td')
    
    if (!singleAkwCells.empty?)
      singleAkwLink = singleAkwCells[0].search('a')[1]
      singleAkwUrl = wikipediaUrl + singleAkwLink.attribute('href')
      singleAkwHtml = ScraperWiki.scrape(singleAkwUrl)
      singleAkwDoc = Nokogiri::XML(singleAkwHtml)

      singleAkwLongitude = Float(singleAkwDoc.css('#Infobox_Kernkraftwerk .longitude')[0].child.content)
      singleAkwLatitude = Float(singleAkwDoc.css('#Infobox_Kernkraftwerk .latitude')[0].child.content)

      singleAkwBezeichnung = singleAkwLink.content
      if singleAkwCells[0].children.size == 6
        singleAkwBezeichnungAppendix = singleAkwCells[0].children[5]
        singleAkwBezeichnung = singleAkwBezeichnung + singleAkwBezeichnungAppendix.content
      end

      singleAkwStatus = extractContentOfXmlElement(singleAkwCells[13]) 
      
      singleAkwImageTag = singleAkwDoc.css('#Infobox_Kernkraftwerk a.image img')[0]
      singleAkwImageUrl = wikipediaUrl + singleAkwImageTag.attribute('src')
  
      akwData = {
        'kuerzel' => singleAkwCells[1].child.content,
        'standort' => singleAkwLink.content,
        'bezeichnung' => singleAkwBezeichnung,
        'wikipedia_url' => singleAkwUrl,
        'bundesland' => singleAkwCells[0].search('a img').attribute('alt'),
        'latitude' => singleAkwLatitude,
        'longitude' => singleAkwLongitude,
        'typ' => singleAkwCells[2].child.content,
        'betreiber' => singleAkwCells[3].content.gsub('-', ''),
        'ausser_betrieb' => singleAkwCells[11].child.content.gsub('!', ''),
        'status' => singleAkwStatus,
        'image_url' => singleAkwImageUrl
      }

      unique_keys = ['kuerzel']
      ScraperWiki.save_sqlite(unique_keys, akwData)
    end
end
require 'nokogiri'

# Create a content string from the content of the node and its subnodes. 
# Content of empty subnodes will be replaced by ' '.
def extractContentOfXmlElement xmlElement
   xmlElementContent = ''
   xmlElement.children.each do |xmlElementChild|
     xmlElementContentPart = ' '
     if !xmlElementChild.content.empty? 
       xmlElementContentPart = xmlElementChild.content
     end
     xmlElementContent = xmlElementContent + xmlElementContentPart
   end
   return xmlElementContent  
end

wikipediaUrl = 'http://de.wikipedia.org'

listAkwHtml = ScraperWiki.scrape(wikipediaUrl + "/wiki/Liste_der_Kernreaktoren_in_Deutschland")
listAkwDoc = Nokogiri::XML(listAkwHtml)

listAkwDoc.css('body * table:nth-of-type(2) tr').each do |singleAkwRow|    
    singleAkwCells = singleAkwRow.css('td')
    
    if (!singleAkwCells.empty?)
      singleAkwLink = singleAkwCells[0].search('a')[1]
      singleAkwUrl = wikipediaUrl + singleAkwLink.attribute('href')
      singleAkwHtml = ScraperWiki.scrape(singleAkwUrl)
      singleAkwDoc = Nokogiri::XML(singleAkwHtml)

      singleAkwLongitude = Float(singleAkwDoc.css('#Infobox_Kernkraftwerk .longitude')[0].child.content)
      singleAkwLatitude = Float(singleAkwDoc.css('#Infobox_Kernkraftwerk .latitude')[0].child.content)

      singleAkwBezeichnung = singleAkwLink.content
      if singleAkwCells[0].children.size == 6
        singleAkwBezeichnungAppendix = singleAkwCells[0].children[5]
        singleAkwBezeichnung = singleAkwBezeichnung + singleAkwBezeichnungAppendix.content
      end

      singleAkwStatus = extractContentOfXmlElement(singleAkwCells[13]) 
      
      singleAkwImageTag = singleAkwDoc.css('#Infobox_Kernkraftwerk a.image img')[0]
      singleAkwImageUrl = wikipediaUrl + singleAkwImageTag.attribute('src')
  
      akwData = {
        'kuerzel' => singleAkwCells[1].child.content,
        'standort' => singleAkwLink.content,
        'bezeichnung' => singleAkwBezeichnung,
        'wikipedia_url' => singleAkwUrl,
        'bundesland' => singleAkwCells[0].search('a img').attribute('alt'),
        'latitude' => singleAkwLatitude,
        'longitude' => singleAkwLongitude,
        'typ' => singleAkwCells[2].child.content,
        'betreiber' => singleAkwCells[3].content.gsub('-', ''),
        'ausser_betrieb' => singleAkwCells[11].child.content.gsub('!', ''),
        'status' => singleAkwStatus,
        'image_url' => singleAkwImageUrl
      }

      unique_keys = ['kuerzel']
      ScraperWiki.save_sqlite(unique_keys, akwData)
    end
end
