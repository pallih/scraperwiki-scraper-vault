# encoding: UTF-8
require 'faraday'
require 'net/http'
require 'uri'
require 'json'

start_x = 10222*2
end_x = 10224*2

start_y = 6026*2
end_y = 6034*2

zoom = 14+1

# функция для получения геометрии объекта в виде строки
def get_geometry data

  if data[0][0].kind_of?(Array)
    data[0][0].map{|i| i.join(',')}.join(';')
  else
    data.map{|i| i.join(',')}.join(';')
  end

end

# обходим заданный участок и собираем id объектов в массив $data
$data = []
(start_x..end_x).each do |x|
  (start_y..end_y).each do |y|
  uri = URI "http://n.maps.yandex.ru/actions/get-geoobjects-by-tile.xml?x=#{x}&y=#{y}&zoom=#{zoom}"
  res = Net::HTTP.get uri
  $data += JSON.parse(res)['response']
  end
end



p $data.length

# собираем данные
$data.each do |object|

  uri = URI "http://n.maps.yandex.ru/actions/get-geoobject.xml?id=#{object['id']}"
  res = JSON.parse(Net::HTTP.get uri)['response']
  if res['id']
    data = {
      :id => res['id'], :revision => res['revision'], :category => res['categoryId'],
      :center => res['center'].join(','), :title => res['title'], :attributes => res['attrs'].to_json,
      :geometry => get_geometry(res['geometry']['data']), :geometry_type => res['geometry']['type']
    }
    # записываем в бд
    #ScraperWiki::save_sqlite(['id'], data)
    p data
  else
    # по каким-то причинам на некоторые объекты сервер возврашает ошибку
    p "Error:#{object}"
    p res
  end

end


