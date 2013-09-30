#encoding: UTF-8
require 'json'

[0,1,2,3,4,5].each{ |score|

  page = 1
  finished = false
  while finished == false
    ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
    html = ic.iconv(ScraperWiki::scrape("http://fancyapint.com/Pub/rating/#{score}/?&doFilter=0&perPage=10&page=#{page}"))
    
    puts html.encoding
    html.gsub(/\u00a0/," ")    


    if html.match('var pubs = (.*?\])\;.*?\n')
      pub_json = $~[1]
      puts pub_json
      pubs = JSON::parse(pub_json)
      puts pubs[0]
      
      pubs.each{|pub| 
      
        pub.delete('addressId')
        pub.delete('locationId')
        pub.delete('last_review')
        pub['lat'] = pub['pubLatLng']['lat']
        pub['lng'] = pub['pubLatLng']['lng']
        pub.delete('pubLatLng')
        pub['addr1'] = pub['address']['addr1']
        pub['addr2'] = pub['address']['addr2']
        pub['addr3'] = pub['address']['addr3']
        pub['town_city'] = pub['address']['town_city']
        pub['county'] = pub['address']['county']
        pub['postcode'] = pub['address']['postcode']
        pub.delete('address')
        pub.delete('imageLocation')
        pub.delete('mainimageLocation')
      
        ScraperWiki::save_sqlite(['pubId'],pub)
      }
    else
      finished = true
    end
    page=page+1
  end
}


#{"name"=>"Beeses Riverside Bar &amp; Tea Gardens", "addressId"=>"4251", "location_name"=>"Bristol", "locationId"=>"269", "last_review"=>"", "pubLatLng"=>{"pubId"=>"4990", "lat"=>"51.441742", "lng"=>"-2.534057", "pubLatLngId"=>""}, "address"=>{"countryId"=>"225", "addr1"=>"Wyndham Crescent", "addr2"=>" Bristol", "addr3"=>"", "town_city"=>"Bristol", "county"=>"Avon", "postcode"=>"BS4 4SX", "addressId"=>"4251"}, "communityAvg"=>"0.00", "fapAvg"=>"5.00", "communityCount"=>"0", "fapCount"=>"1", "reviewCount"=>"1", "imageLocation"=>"", "mainimageLocation"=>"", "pubId"=>"4990"}

#encoding: UTF-8
require 'json'

[0,1,2,3,4,5].each{ |score|

  page = 1
  finished = false
  while finished == false
    ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
    html = ic.iconv(ScraperWiki::scrape("http://fancyapint.com/Pub/rating/#{score}/?&doFilter=0&perPage=10&page=#{page}"))
    
    puts html.encoding
    html.gsub(/\u00a0/," ")    


    if html.match('var pubs = (.*?\])\;.*?\n')
      pub_json = $~[1]
      puts pub_json
      pubs = JSON::parse(pub_json)
      puts pubs[0]
      
      pubs.each{|pub| 
      
        pub.delete('addressId')
        pub.delete('locationId')
        pub.delete('last_review')
        pub['lat'] = pub['pubLatLng']['lat']
        pub['lng'] = pub['pubLatLng']['lng']
        pub.delete('pubLatLng')
        pub['addr1'] = pub['address']['addr1']
        pub['addr2'] = pub['address']['addr2']
        pub['addr3'] = pub['address']['addr3']
        pub['town_city'] = pub['address']['town_city']
        pub['county'] = pub['address']['county']
        pub['postcode'] = pub['address']['postcode']
        pub.delete('address')
        pub.delete('imageLocation')
        pub.delete('mainimageLocation')
      
        ScraperWiki::save_sqlite(['pubId'],pub)
      }
    else
      finished = true
    end
    page=page+1
  end
}


#{"name"=>"Beeses Riverside Bar &amp; Tea Gardens", "addressId"=>"4251", "location_name"=>"Bristol", "locationId"=>"269", "last_review"=>"", "pubLatLng"=>{"pubId"=>"4990", "lat"=>"51.441742", "lng"=>"-2.534057", "pubLatLngId"=>""}, "address"=>{"countryId"=>"225", "addr1"=>"Wyndham Crescent", "addr2"=>" Bristol", "addr3"=>"", "town_city"=>"Bristol", "county"=>"Avon", "postcode"=>"BS4 4SX", "addressId"=>"4251"}, "communityAvg"=>"0.00", "fapAvg"=>"5.00", "communityCount"=>"0", "fapCount"=>"1", "reviewCount"=>"1", "imageLocation"=>"", "mainimageLocation"=>"", "pubId"=>"4990"}

