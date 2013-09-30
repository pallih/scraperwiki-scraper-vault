require 'net/http'

# This crashes with a stack trace ending like this on ScraperWiki:
# /usr/lib/ruby/1.8/net/protocol.rb -- in `rbuf_fill'
# /usr/lib/ruby/1.8/net/protocol.rb:135:in `sysread': Connection reset by peer

# But works fine locally
# works for me when I run it on the site.  should there be some http:// before the www?

@http = Net::HTTP.new("www.sos.wa.gov")
@path = "/corps/search_detail201002.asmx/GetNext"
@headers = { 'Accept' => '*/*', 'Content-Type' => 'application/json;charset=utf-8' }
i = 21
json_data = '{"Start":"' + i.to_s +
'","Name":"A","Criteria":"all","NameType":"starts_with","UBI":"","Active":"",
"AgentName":"","City":"","Zip":"","Domestic":"","Category":"","Now":'+(Time.now.to_f*1000).to_i.to_s + ',"StartDate":"","EndDate":""}'


resp, data = @http.post(@path, json_data, @headers)
puts data

require 'net/http'

# This crashes with a stack trace ending like this on ScraperWiki:
# /usr/lib/ruby/1.8/net/protocol.rb -- in `rbuf_fill'
# /usr/lib/ruby/1.8/net/protocol.rb:135:in `sysread': Connection reset by peer

# But works fine locally
# works for me when I run it on the site.  should there be some http:// before the www?

@http = Net::HTTP.new("www.sos.wa.gov")
@path = "/corps/search_detail201002.asmx/GetNext"
@headers = { 'Accept' => '*/*', 'Content-Type' => 'application/json;charset=utf-8' }
i = 21
json_data = '{"Start":"' + i.to_s +
'","Name":"A","Criteria":"all","NameType":"starts_with","UBI":"","Active":"",
"AgentName":"","City":"","Zip":"","Domestic":"","Category":"","Now":'+(Time.now.to_f*1000).to_i.to_s + ',"StartDate":"","EndDate":""}'


resp, data = @http.post(@path, json_data, @headers)
puts data

