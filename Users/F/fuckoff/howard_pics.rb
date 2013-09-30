###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://scraperwiki.com/hello_world.html'
html = '<td height="152" colspan="2" valign="top"><table width="30%" height="124" border="0">

        <tr>

          <td width="30%" height="120"><img src="IMAGES/ANT2.JPG" width="178" height="118"></td>

          <td width="70%" valign="top"><em>Atta cephalotes</em> worker ant cutting 

            a leaf in the lab</td>

        </tr>

      </table>

      <table width="62%" height="173" border="0">

        <tr> 

          <td width="15%" height="169"><img src="IMAGES/BCI.jpg" width="250" height="167"></td>

          <td width="85%" valign="top">Arial photograph of Barro Colorado Island, 

            Panama. Site of field work on leaf cutter ants.</td>

        </tr>

      </table>

      <table width="75%" height="213" border="0">

        <tr> 

          <td width="15%" height="209"><img src="IMAGES/bigtree01.jpg" width="200" height="207"></td>

          <td width="85%" valign="top"><em>Huberodendron</em> tree in Corcovado 

            National Park, Costa Rica with 1980 OTS course members. Left to Right: 

            Bill Busby, Sandy Knapp, Lloyd Goldwasser, Jonathan Coddington. Corcovado 

            is the site for research on leafcutter ants and forest regeneration.</td>

        </tr>

      </table>

      

    </td>
'

# use Nokogiri to get all <td> tags

doc = Nokogiri::HTML(html)
out_text = ''

doc.xpath('//table/tr').each do |node|
  out_text += '<div class="page_item">'
  node.css('img').each do |imgTag|
    imgTag['class'] = "gallerypic"
    out_text += imgTag.to_s.gsub('%20','').gsub('IMAGES','/people/images')
    imgTag.remove
  end

  node.css('td').each do |row|
    out_text += row.inner_html
  end
  out_text += '</div>'
end



out_text = out_text.gsub('"','\"').gsub('\n','') 
puts out_text
record = {"tropical" => out_text}
ScraperWiki.save(['tropical'], record)

#doc.xpath('//td/img').each do |node|
#  puts (node['src']).gsub('%20','')
#  puts  node.parent.parent.text
#  puts '--'
#end

#doc.search('td').each do |td|
#    puts td.inner_html
#    record = {'td' => td.inner_html}
#    ScraperWiki.save(['td'], record)
#end
###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://scraperwiki.com/hello_world.html'
html = '<td height="152" colspan="2" valign="top"><table width="30%" height="124" border="0">

        <tr>

          <td width="30%" height="120"><img src="IMAGES/ANT2.JPG" width="178" height="118"></td>

          <td width="70%" valign="top"><em>Atta cephalotes</em> worker ant cutting 

            a leaf in the lab</td>

        </tr>

      </table>

      <table width="62%" height="173" border="0">

        <tr> 

          <td width="15%" height="169"><img src="IMAGES/BCI.jpg" width="250" height="167"></td>

          <td width="85%" valign="top">Arial photograph of Barro Colorado Island, 

            Panama. Site of field work on leaf cutter ants.</td>

        </tr>

      </table>

      <table width="75%" height="213" border="0">

        <tr> 

          <td width="15%" height="209"><img src="IMAGES/bigtree01.jpg" width="200" height="207"></td>

          <td width="85%" valign="top"><em>Huberodendron</em> tree in Corcovado 

            National Park, Costa Rica with 1980 OTS course members. Left to Right: 

            Bill Busby, Sandy Knapp, Lloyd Goldwasser, Jonathan Coddington. Corcovado 

            is the site for research on leafcutter ants and forest regeneration.</td>

        </tr>

      </table>

      

    </td>
'

# use Nokogiri to get all <td> tags

doc = Nokogiri::HTML(html)
out_text = ''

doc.xpath('//table/tr').each do |node|
  out_text += '<div class="page_item">'
  node.css('img').each do |imgTag|
    imgTag['class'] = "gallerypic"
    out_text += imgTag.to_s.gsub('%20','').gsub('IMAGES','/people/images')
    imgTag.remove
  end

  node.css('td').each do |row|
    out_text += row.inner_html
  end
  out_text += '</div>'
end



out_text = out_text.gsub('"','\"').gsub('\n','') 
puts out_text
record = {"tropical" => out_text}
ScraperWiki.save(['tropical'], record)

#doc.xpath('//td/img').each do |node|
#  puts (node['src']).gsub('%20','')
#  puts  node.parent.parent.text
#  puts '--'
#end

#doc.search('td').each do |td|
#    puts td.inner_html
#    record = {'td' => td.inner_html}
#    ScraperWiki.save(['td'], record)
#end
