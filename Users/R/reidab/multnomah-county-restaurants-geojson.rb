# GeoJSON
require 'json'

sourcescraper = 'multnomah-county-restaurants'
ScraperWiki.attach(sourcescraper)
ScraperWiki.httpresponseheader("Content-Type", "text/json")

restaurants = ScraperWiki.select("* from `multnomah-county-restaurants`.restaurants where latitude is not null")

restaurants_with_geometry = restaurants.map do |restaurant|
  latitude = restaurant.delete('latitude')
  longitude = restaurant.delete('longitude')

  restaurant.merge(:geometry => {
   :type => 'Point',
   :coordinates => [longitude, latitude]
  })
end

puts restaurants_with_geometry.to_json