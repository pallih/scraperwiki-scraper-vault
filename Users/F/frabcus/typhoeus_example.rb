require 'typhoeus'

response = Typhoeus::Request.get("http://www.pauldix.net")

puts response

