# Blank Ruby

require 'hpricot'

state_abbr = {
  'AL' => 'Alabama',
  'AK' => 'Alaska',
  'AZ' => 'Arizona',
  'AR' => 'Arkansas',
  'CA' => 'California',
  'CO' => 'Colorado',
  'CT' => 'Connecticut',
  'DE' => 'Delaware',
  'DC' => 'District of Columbia',
  'FM' => 'Micronesia1',
  'FL' => 'Florida',
  'GA' => 'Georgia',
  'GU' => 'Guam',
  'HI' => 'Hawaii',
  'ID' => 'Idaho',
  'IL' => 'Illinois',
  'IN' => 'Indiana',
  'IA' => 'Iowa',
  'KS' => 'Kansas',
  'KY' => 'Kentucky',
  'LA' => 'Louisiana',
  'ME' => 'Maine',
  'MH' => 'Islands1',
  'MD' => 'Maryland',
  'MA' => 'Massachusetts',
  'MI' => 'Michigan',
  'MN' => 'Minnesota',
  'MS' => 'Mississippi',
  'MO' => 'Missouri',
  'MT' => 'Montana',
  'NE' => 'Nebraska',
  'NV' => 'Nevada',
  'NH' => 'New Hampshire',
  'NJ' => 'New Jersey',
  'NM' => 'New Mexico',
  'NY' => 'New York',
  'NC' => 'North Carolina',
  'ND' => 'North Dakota',
  'OH' => 'Ohio',
  'OK' => 'Oklahoma',
  'OR' => 'Oregon',
  'PW' => 'Palau',
  'PA' => 'Pennsylvania',
  'PR' => 'Puerto Rico',
  'RI' => 'Rhode Island',
  'SC' => 'South Carolina',
  'SD' => 'South Dakota',
  'TN' => 'Tennessee',
  'TX' => 'Texas',
  'UT' => 'Utah',
  'VT' => 'Vermont',
  'VI' => 'Virgin Island',
  'VA' => 'Virginia',
  'WA' => 'Washington',
  'WV' => 'West Virginia',
  'WI' => 'Wisconsin',
  'WY' => 'Wyoming'
}

wh = state_abbr.keys.collect do |state|
  puts state
  url = "http://hosted.where2getit.com/wafflehouse/ajax?&xml_request=%3Crequest%3E%3C"
  url += "appkey%3EF03D90F4-9858-11DC-86A8-AD9B145F7BC8%3C%2Fappkey%3E%3Cformdata%20id"
  url += "%3D%22locatorsearch%22%3E%3Climit%3E16%3C%2Flimit%3E%3Cdataview%3Estore_defau"
  url += "lt%3C%2Fdataview%3E%3Cgeolocs%3E%3Cgeoloc%3E%3Caddressline%3E#{state}%3C%2Faddres"
  url += "sline%3E%3Clatitude%3E%3C%2Flatitude%3E%3Clongitude%3E%3C%2Flongitude%3E%3C%2"
  url += "Fgeoloc%3E%3C%2Fgeolocs%3E%3Csearchradius%3E20%7C50%7C100%7C200%7C400%3C%2Fse"
  url += "archradius%3E%3C%2Fformdata%3E%3C%2Frequest%3E"
  html = Net::HTTP.get(URI::parse(url))
  doc = Hpricot.parse html
  puts "\t"+(doc.search("poi")).length.to_s
  z = (doc.search("poi")).collect do |wh|
    puts "\t"+(wh.search :city).innerHTML
    a= {
      "uid"     => (wh.search :uid).innerHTML.to_s,
      "address" => (wh.search :address1).innerHTML.downcase.split.collect{ |k| k.capitalize }.join(" "),
      "city" => (wh.search :city).innerHTML.downcase.split.collect{ |k| k.capitalize }.join(" "),
      "phone" => (wh.search :phone).innerHTML,
      "postalcode" => (wh.search :postalcode).innerHTML,
      "state" => state
    }
    ScraperWiki.save_sqlite(["uid"], a,"waffleHouseLocations")
  end
end
