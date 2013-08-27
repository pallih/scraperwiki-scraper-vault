# encoding: UTF-8
require 'nokogiri'
require 'typhoeus'
require 'csv'

BASE_URL = 'http://www.goodsmatrix.ru'
POSTFIX = '/goods/'
EXT = '.html'
BCODES = [4034229008833,4044996007038,4607084414073,
          4041811018453,4607084411164,4607084411157,
          4607067553171,4008638120103
         ]

  BCODES.each do |row|

    html = Typhoeus::Request.get BASE_URL + POSTFIX + row.to_s + EXT
    #p html.body.force_encoding('').encode!('windows-1251')
    doc = Nokogiri::HTML html.body.force_encoding('cp1251').encode('utf-8')
    p doc
      p 'Processing: ' + "#{row}"
      p doc.css('span[id*="_ContentPH_GoodsName"]')
      [
        doc.css('span[id*="_ContentPH_GoodsName"]').text,
        doc.css('span[id*="_ContentPH_Composition"]').text,
        doc.css('span[id*="_ContentPH_Comment"]').text,
        doc.css('span[id*="_ContentPH_Gost"]').text,
        doc.css('span[id*="_ContentPH_Net"]').text,
        doc.css('span[id*="_ContentPH_KeepingTime"]').text,
        doc.css('span[id*="_ContentPH_StoreCond"]').text,
        doc.css('span[id*="_ContentPH_GmoL"]').text,
        doc.css('span[id*="_ContentPH_ESL"]').text,
        doc.css('span[id*="_ContentPH_QuantityInBox"]').text,
        doc.css('img[id*="_ctl0_ContentPH_LSGoodPicture_GoodImg"]').text
     ]


  end

# encoding: UTF-8
require 'nokogiri'
require 'typhoeus'
require 'csv'

BASE_URL = 'http://www.goodsmatrix.ru'
POSTFIX = '/goods/'
EXT = '.html'
BCODES = [4034229008833,4044996007038,4607084414073,
          4041811018453,4607084411164,4607084411157,
          4607067553171,4008638120103
         ]

  BCODES.each do |row|

    html = Typhoeus::Request.get BASE_URL + POSTFIX + row.to_s + EXT
    #p html.body.force_encoding('').encode!('windows-1251')
    doc = Nokogiri::HTML html.body.force_encoding('cp1251').encode('utf-8')
    p doc
      p 'Processing: ' + "#{row}"
      p doc.css('span[id*="_ContentPH_GoodsName"]')
      [
        doc.css('span[id*="_ContentPH_GoodsName"]').text,
        doc.css('span[id*="_ContentPH_Composition"]').text,
        doc.css('span[id*="_ContentPH_Comment"]').text,
        doc.css('span[id*="_ContentPH_Gost"]').text,
        doc.css('span[id*="_ContentPH_Net"]').text,
        doc.css('span[id*="_ContentPH_KeepingTime"]').text,
        doc.css('span[id*="_ContentPH_StoreCond"]').text,
        doc.css('span[id*="_ContentPH_GmoL"]').text,
        doc.css('span[id*="_ContentPH_ESL"]').text,
        doc.css('span[id*="_ContentPH_QuantityInBox"]').text,
        doc.css('img[id*="_ctl0_ContentPH_LSGoodPicture_GoodImg"]').text
     ]


  end

# encoding: UTF-8
require 'nokogiri'
require 'typhoeus'
require 'csv'

BASE_URL = 'http://www.goodsmatrix.ru'
POSTFIX = '/goods/'
EXT = '.html'
BCODES = [4034229008833,4044996007038,4607084414073,
          4041811018453,4607084411164,4607084411157,
          4607067553171,4008638120103
         ]

  BCODES.each do |row|

    html = Typhoeus::Request.get BASE_URL + POSTFIX + row.to_s + EXT
    #p html.body.force_encoding('').encode!('windows-1251')
    doc = Nokogiri::HTML html.body.force_encoding('cp1251').encode('utf-8')
    p doc
      p 'Processing: ' + "#{row}"
      p doc.css('span[id*="_ContentPH_GoodsName"]')
      [
        doc.css('span[id*="_ContentPH_GoodsName"]').text,
        doc.css('span[id*="_ContentPH_Composition"]').text,
        doc.css('span[id*="_ContentPH_Comment"]').text,
        doc.css('span[id*="_ContentPH_Gost"]').text,
        doc.css('span[id*="_ContentPH_Net"]').text,
        doc.css('span[id*="_ContentPH_KeepingTime"]').text,
        doc.css('span[id*="_ContentPH_StoreCond"]').text,
        doc.css('span[id*="_ContentPH_GmoL"]').text,
        doc.css('span[id*="_ContentPH_ESL"]').text,
        doc.css('span[id*="_ContentPH_QuantityInBox"]').text,
        doc.css('img[id*="_ctl0_ContentPH_LSGoodPicture_GoodImg"]').text
     ]


  end

