# Count how many crimes there were in a particular area

require 'json'
require 'open-uri'

def countCrimesInArea(lat,lng)

  count = 0
  
  for i in 1..12
    sleep 1.5
    url = "http://data.police.uk/api/crimes-street/all-crime?lat=" + lat + "&lng=" + lng + "&date=2012-" + i.to_s
    output = JSON.parse(open(url).read) 
    count = count + output.length
  end

  return count
end



stops = ['Eccles',
         'Ladywell',
         'Weaste',
         'Langworthy',
         'Broadway',
         'Mediacity',
         'Harbour City',
         'Anchorage',
         'Salford Quays',
         'Exchange Quay',
         'Pomona']

lat = {'Eccles' => '53.4834634',
        'Ladywell' => '53.4875447',
        'Weaste' => '53.4806745',
        'Langworthy' => '53.4793777',
        'Broadway' => '53.4694265',
        'Mediacity' => '53.4741021',
        'Harbour City' => '53.4694265',
        'Anchorage' => '53.4737792',
        'Salford Quays' => '53.4704610',
        'Exchange Quay' => '53.4661202',
        'Pomona' => '53.4656300'}

lng = {'Eccles' => '-2.3334294',
        'Ladywell' => '-2.3234243',
        'Weaste' => '-2.2896039',
        'Langworthy' => '-2.2868678',
        'Broadway' => '-2.2997521',
        'Mediacity' => '-2.2976345',
        'Harbour City' => '-2.2997521',
        'Anchorage' => '-2.2863479',
        'Salford Quays' => '-2.2831920',
        'Exchange Quay' => '-2.2828920',
        'Pomona' => '-2.2828920'}

stops.each do |stop|
  numberCrimes = countCrimesInArea(lat[stop],lng[stop])
  p stop + " has " + numberCrimes.to_s + "\n"
end


