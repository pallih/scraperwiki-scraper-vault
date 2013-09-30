#encoding: utf-8
sourcescraper = 'konstrundan_2012'

ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select( "* from konstrundan_2012.deltagare order by uri" )

ScraperWiki.httpresponseheader('Content-Type', 'text/xml; charset=utf-8')

puts %Q|<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>|

folders = Hash.new {|h,k| h[k] = []}

data.select {|x| x['longitude'] != nil && x['longitude'].strip.size > 0 }.each do |item|
  types = item.keys.select {|type| item[type] == 1 || item[type] == '1' || item[type] == true}

  if types.include? 'måleri'
   folders['måleri'] << item
  elsif types.include? 'skulptur'
   folders['skulptur'] << item
  elsif types.include? 'grafik'
   folders['grafik'] << item
  elsif types.include? 'teckning'
   folders['teckning'] << item
  elsif types.include? 'keramik'
   folders['keramik'] << item
  elsif types.include? 'textil'
   folders['textil'] << item
  elsif types.include? 'fotokonst'
   folders['fotokonst'] << item
  else
   folders['other'] << item
  end  
end

folders.each do |folder, items|
  puts "<Folder>
  <name>#{folder}</name>
  <open>0</open>"

  items.each do |item|

    types = item.keys.select {|type| item[type] == 1 || item[type] == '1' || item[type] == true}
  
    colour = if types.include? 'måleri'
     'pink'
    elsif types.include? 'skulptur'
     'blue'
    elsif types.include? 'grafik'
     'green'
    elsif types.include? 'teckning'
     'lightblue'
    elsif types.include? 'keramik'
     'orange'
    elsif types.include? 'textil'
     'pink'
    elsif types.include? 'fotokonst'
     'purple'
    else
     'red'
    end
    
    dot = types.size > 1 ? '-dot' : ''
    
    icon = "http://google.com/mapfiles/ms/micons/#{colour}#{dot}.png"
    
    puts %Q|    <Placemark>
          <name>#{item['name']}</name>
          <description>
            <![CDATA[
              <h1>#{item['name']}</h1>
              <p><a href="#{item['map_uri']}">#{item['address_1']}</a></p>
              <p>#{item['address_2']}</p>
              <p>#{types.join(', ')}</p>
              <img src="#{item['image_uri']}" width="128" height="128" />
            ]]>
          </description>
          <Style>
            <IconStyle>
              <Icon>
                <href>#{icon}</href>
              </Icon>
            </IconStyle>
          </Style>
          <Point>
            <coordinates>#{item['longitude']},#{item['latitude']}</coordinates>
          </Point>
        </Placemark>|
  end

  puts "</Folder>"

end



puts %Q|  </Document>
</kml>|
#encoding: utf-8
sourcescraper = 'konstrundan_2012'

ScraperWiki.attach(sourcescraper)

data = ScraperWiki.select( "* from konstrundan_2012.deltagare order by uri" )

ScraperWiki.httpresponseheader('Content-Type', 'text/xml; charset=utf-8')

puts %Q|<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>|

folders = Hash.new {|h,k| h[k] = []}

data.select {|x| x['longitude'] != nil && x['longitude'].strip.size > 0 }.each do |item|
  types = item.keys.select {|type| item[type] == 1 || item[type] == '1' || item[type] == true}

  if types.include? 'måleri'
   folders['måleri'] << item
  elsif types.include? 'skulptur'
   folders['skulptur'] << item
  elsif types.include? 'grafik'
   folders['grafik'] << item
  elsif types.include? 'teckning'
   folders['teckning'] << item
  elsif types.include? 'keramik'
   folders['keramik'] << item
  elsif types.include? 'textil'
   folders['textil'] << item
  elsif types.include? 'fotokonst'
   folders['fotokonst'] << item
  else
   folders['other'] << item
  end  
end

folders.each do |folder, items|
  puts "<Folder>
  <name>#{folder}</name>
  <open>0</open>"

  items.each do |item|

    types = item.keys.select {|type| item[type] == 1 || item[type] == '1' || item[type] == true}
  
    colour = if types.include? 'måleri'
     'pink'
    elsif types.include? 'skulptur'
     'blue'
    elsif types.include? 'grafik'
     'green'
    elsif types.include? 'teckning'
     'lightblue'
    elsif types.include? 'keramik'
     'orange'
    elsif types.include? 'textil'
     'pink'
    elsif types.include? 'fotokonst'
     'purple'
    else
     'red'
    end
    
    dot = types.size > 1 ? '-dot' : ''
    
    icon = "http://google.com/mapfiles/ms/micons/#{colour}#{dot}.png"
    
    puts %Q|    <Placemark>
          <name>#{item['name']}</name>
          <description>
            <![CDATA[
              <h1>#{item['name']}</h1>
              <p><a href="#{item['map_uri']}">#{item['address_1']}</a></p>
              <p>#{item['address_2']}</p>
              <p>#{types.join(', ')}</p>
              <img src="#{item['image_uri']}" width="128" height="128" />
            ]]>
          </description>
          <Style>
            <IconStyle>
              <Icon>
                <href>#{icon}</href>
              </Icon>
            </IconStyle>
          </Style>
          <Point>
            <coordinates>#{item['longitude']},#{item['latitude']}</coordinates>
          </Point>
        </Placemark>|
  end

  puts "</Folder>"

end



puts %Q|  </Document>
</kml>|
