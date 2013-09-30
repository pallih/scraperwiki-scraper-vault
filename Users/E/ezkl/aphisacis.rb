require 'nokogiri'
require 'typhoeus'

@uri = "http://acissearch.aphis.usda.gov/LPASearch/faces/Detail.jspx"

response = Typhoeus::Request.post(@uri, params: { addressstatelist: 43, value: "all", partial: false })
puts response.bodyrequire 'nokogiri'
require 'typhoeus'

@uri = "http://acissearch.aphis.usda.gov/LPASearch/faces/Detail.jspx"

response = Typhoeus::Request.post(@uri, params: { addressstatelist: 43, value: "all", partial: false })
puts response.body