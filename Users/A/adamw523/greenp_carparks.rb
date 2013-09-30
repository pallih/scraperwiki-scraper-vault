require "hpricot"

summary_div_re = Regexp.new("h1\>(.*)\<\/h1.*ess:\<\/strong\>(.*)\<\/p\>.*ype:\<\/strong>(.*)\<\/p\>.*Capacity:<\/strong>(.*)<\/p>.*tions:<\/strong\>(.*)<\/p>.*ayment:<\/strong\>(.*)\<\/p\>", Regexp::MULTILINE)
lat_lng_re = Regexp.new('.*var\ point.*Lng\(\'(.*)\'\,\'(.*)\'\).*', Regexp::MULTILINE)

ScraperWiki.attach('greenp_carparks_links')
carparks = ScraperWiki.select('* from `greenp_carparks_links`.swdata')

# pp carparks

if carparks
  carparks.each do |carpark|
    carpark_url = carpark['url']
  
    if html = ScraperWiki.scrape(carpark_url)
      doc = Hpricot(html)
            
      lot_summary_div = doc.search("div#lot-summary")
      tab_rates_div = doc.search("div#tab-rates")
      
      summary_div_match = lot_summary_div.inner_html.match(summary_div_re)
      lat_lng_match = doc.inner_html.match(lat_lng_re)
      
      item = {}
      # item['html'] = html
      item['url'] = carpark_url
      # item['summary_div_matches'] = summary_div_match ? summary_div_match.to_a.join(',').force_encoding('UTF-8') : nil
      # item['htmllat_lng_matches'] = lat_lng_match ? lat_lng_match.to_a.join(',').force_encoding('UTF-8') : nil
      item['updated_at'] = Time.now

      if summary_div_match && lat_lng_match
        item['lat'] = lat_lng_match[1]
        item['lng'] = lat_lng_match[2]

        item['title'] = summary_div_match[1].strip
        item['street_address'] = summary_div_match[2].strip
        item['facility_type'] = summary_div_match[3].strip
        item['capacity'] = summary_div_match[4].strip
        item['payment_options'] = summary_div_match[5].strip
        item['payment_types'] = summary_div_match[6].strip
      
        tab_rates_p_elements = tab_rates_div.search("p")
        item['rate'] = tab_rates_p_elements[0].inner_text
        item['rate_details'] = []
        tab_rates_p_elements.values_at(1..-1).each do |rate_details|
          item['rate_details'].push(rate_details.inner_text)
        end
      end
      # puts item
      ScraperWiki.save(['url'], item)
    end
  end
end

# lot_summary_div
#<h1>Carpark 55</h1>
#                <p><strong>Address:</strong> 23 Bedford Park Avenue West</p>
#                <p><strong>Facility Type:</strong> Surface</p>
#                                  <p><strong>Capacity:</strong> 42 Spaces</p>
#                                                <p><strong>Payment Options:</strong> </p>
#                <p><strong>Accepted Forms of Payment:</strong> </p>
#                
#                <div class="clear"><!-- --></div>
              require "hpricot"

summary_div_re = Regexp.new("h1\>(.*)\<\/h1.*ess:\<\/strong\>(.*)\<\/p\>.*ype:\<\/strong>(.*)\<\/p\>.*Capacity:<\/strong>(.*)<\/p>.*tions:<\/strong\>(.*)<\/p>.*ayment:<\/strong\>(.*)\<\/p\>", Regexp::MULTILINE)
lat_lng_re = Regexp.new('.*var\ point.*Lng\(\'(.*)\'\,\'(.*)\'\).*', Regexp::MULTILINE)

ScraperWiki.attach('greenp_carparks_links')
carparks = ScraperWiki.select('* from `greenp_carparks_links`.swdata')

# pp carparks

if carparks
  carparks.each do |carpark|
    carpark_url = carpark['url']
  
    if html = ScraperWiki.scrape(carpark_url)
      doc = Hpricot(html)
            
      lot_summary_div = doc.search("div#lot-summary")
      tab_rates_div = doc.search("div#tab-rates")
      
      summary_div_match = lot_summary_div.inner_html.match(summary_div_re)
      lat_lng_match = doc.inner_html.match(lat_lng_re)
      
      item = {}
      # item['html'] = html
      item['url'] = carpark_url
      # item['summary_div_matches'] = summary_div_match ? summary_div_match.to_a.join(',').force_encoding('UTF-8') : nil
      # item['htmllat_lng_matches'] = lat_lng_match ? lat_lng_match.to_a.join(',').force_encoding('UTF-8') : nil
      item['updated_at'] = Time.now

      if summary_div_match && lat_lng_match
        item['lat'] = lat_lng_match[1]
        item['lng'] = lat_lng_match[2]

        item['title'] = summary_div_match[1].strip
        item['street_address'] = summary_div_match[2].strip
        item['facility_type'] = summary_div_match[3].strip
        item['capacity'] = summary_div_match[4].strip
        item['payment_options'] = summary_div_match[5].strip
        item['payment_types'] = summary_div_match[6].strip
      
        tab_rates_p_elements = tab_rates_div.search("p")
        item['rate'] = tab_rates_p_elements[0].inner_text
        item['rate_details'] = []
        tab_rates_p_elements.values_at(1..-1).each do |rate_details|
          item['rate_details'].push(rate_details.inner_text)
        end
      end
      # puts item
      ScraperWiki.save(['url'], item)
    end
  end
end

# lot_summary_div
#<h1>Carpark 55</h1>
#                <p><strong>Address:</strong> 23 Bedford Park Avenue West</p>
#                <p><strong>Facility Type:</strong> Surface</p>
#                                  <p><strong>Capacity:</strong> 42 Spaces</p>
#                                                <p><strong>Payment Options:</strong> </p>
#                <p><strong>Accepted Forms of Payment:</strong> </p>
#                
#                <div class="clear"><!-- --></div>
              