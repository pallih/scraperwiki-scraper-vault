require 'nokogiri'
require 'mechanize'
require 'cgi'  

params = CGI::parse( ENV['QUERY_STRING'] )

url = "http://www.barrowbc.gov.uk/papps/search.aspx"

ref = params['id']

a = Mechanize.new
a.get(url) do |page|
doc = Nokogiri.HTML(page.body)

viewstate = doc.search('#__VIEWSTATE')[0][:value]
eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]

p = a.post(url, {
  "__EVENTTARGET" => "",
  "__EVENTARGUMENT" => "",
  "__LASTFOCUS" => "",
  "__VIEWSTATE" => viewstate,
  "__EVENTVALIDATION" => eventvalidation,
  "txtSearch" => ref,
  "txtSearch2" => "",
  "btnSearch" => "Ref No: Search",
})

doc = Nokogiri.HTML(p.body)

viewstate = doc.search('#__VIEWSTATE')[0][:value]
eventvalidation = doc.search('#__EVENTVALIDATION')[0][:value]

puts "<!DOCTYPE html>
<html>
  <head>
    <title>Redirecting to application...</title>
    <script type='text/javascript' src='http://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js'></script>
    <script type='text/javascript'>
      $(document).ready(function(){
        $('#planningform').submit();
      });
    </script>
  </head>
  <body>"

puts "Redirecting to application..."

puts "<form action='#{url}' method='post' id='planningform'>"
puts "<input type='hidden' name='__VIEWSTATE' value='#{viewstate}' />"
puts "<input type='hidden' name='__EVENTVALIDATION' value='#{eventvalidation}' />"
puts "<input type='hidden' name='txtSearch' value='ref' />"
puts "<input type='hidden' name='JumpPage' value='1' />"
puts "<input type='hidden' name='myRepeater$ctl01$btnDetails1' value='Details of #{ref}' />"
puts "<noscript><input type='submit' value='Click me to view the application on the Barrow website' /></script>"
puts "</form>"

end

puts "</body>"
