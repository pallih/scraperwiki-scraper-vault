require 'nokogiri'
require 'mechanize'
require 'open-uri'


url = "https://web.barclayscyclehire.tfl.gov.uk"
agent = Mechanize.new
page = agent.get(url)

cookie_string = ""

agent.cookies.each do |c|
  puts cookie_string << "#{c.to_s}; "
end

cookie_string

puts cookie_string


page.forms.each_with_index do |f, index|
  puts "-------------------- #{index}"
  # loop through the controls in the form
  puts "Controls:"
  f.fields.each do |field|
    if field.node["type"]
      puts " - (name, type, value) = ('#{field.node["name"]}', '#{field.node["type"]}', '#{field.node["value"]}')"
    elsif field.node.name == 'select'
      puts " - (name, type, value) = ('#{field.node["name"]}', '#{field.node.name}', '#{field.options[0]}')"
      # loop through all the options in any select (drop-down) controls
      field.options.each do |opt|
         puts " - - - (value) = #{opt}"
      end
    else
      puts " - (type) ="
    end
  end
end

# this is the cookies header provide when I look at the response in firefox
# Cookie:lchssession=isb85id8nr4e0m8g64vo4450u7; lchscookie=+J/zmYJMHM/59wnFNJe2QPYfpmGygUPNLwEbQ3k1Xa5F0lbsGkpoTU/egphI/Tl2fHm0GMy8mMmiyA==; TS7a8c97=fdbe23853e039d1b3f349257329157a232c66b2fbfc1e2e54f175ee9d8ab2530bc2922a5ea3035484895a03e; CP=null*; ccokieenable

post_page = agent.post(url, { 
"login[Email]" => "wave@chrisadams.me.uk",
"login[Password]" => "Bacon12345",
'login[_csrf_token]' => 'ace80392de1d61ae5937868eff694ba6'
}, 
'Cookie' => cookie_string
)

puts post_page.body


## what's this? the site is checking for cookies with javascript? GGAARRRRRGGGHHHHH!!!!!

#   <script language="javascript" type="text/javascript">
#         function detectCookieActivation()
#         {
#       document.cookie="ccokieenable"
#         cookieEnabled=(document.cookie.indexOf("ccokieenable")!=-1);
#       var elem = document.getElementById("cookiesmessage");  
#             if(!cookieEnabled){
#         elem.innerHTML =  "<div class='info-panel info-panel-full-width test-validation validation-message'><div class='errorWSDL'>We need to use a cookie to manage your secure session.  <br/>Please enable cookies in your browser settings and try again.</div></div>";  
#             }
#             else
#             {
#                elem.innerHTML = "";
#             }
#         }
#     detectCookieActivation();
#     </script>

    

require 'nokogiri'
require 'mechanize'
require 'open-uri'


url = "https://web.barclayscyclehire.tfl.gov.uk"
agent = Mechanize.new
page = agent.get(url)

cookie_string = ""

agent.cookies.each do |c|
  puts cookie_string << "#{c.to_s}; "
end

cookie_string

puts cookie_string


page.forms.each_with_index do |f, index|
  puts "-------------------- #{index}"
  # loop through the controls in the form
  puts "Controls:"
  f.fields.each do |field|
    if field.node["type"]
      puts " - (name, type, value) = ('#{field.node["name"]}', '#{field.node["type"]}', '#{field.node["value"]}')"
    elsif field.node.name == 'select'
      puts " - (name, type, value) = ('#{field.node["name"]}', '#{field.node.name}', '#{field.options[0]}')"
      # loop through all the options in any select (drop-down) controls
      field.options.each do |opt|
         puts " - - - (value) = #{opt}"
      end
    else
      puts " - (type) ="
    end
  end
end

# this is the cookies header provide when I look at the response in firefox
# Cookie:lchssession=isb85id8nr4e0m8g64vo4450u7; lchscookie=+J/zmYJMHM/59wnFNJe2QPYfpmGygUPNLwEbQ3k1Xa5F0lbsGkpoTU/egphI/Tl2fHm0GMy8mMmiyA==; TS7a8c97=fdbe23853e039d1b3f349257329157a232c66b2fbfc1e2e54f175ee9d8ab2530bc2922a5ea3035484895a03e; CP=null*; ccokieenable

post_page = agent.post(url, { 
"login[Email]" => "wave@chrisadams.me.uk",
"login[Password]" => "Bacon12345",
'login[_csrf_token]' => 'ace80392de1d61ae5937868eff694ba6'
}, 
'Cookie' => cookie_string
)

puts post_page.body


## what's this? the site is checking for cookies with javascript? GGAARRRRRGGGHHHHH!!!!!

#   <script language="javascript" type="text/javascript">
#         function detectCookieActivation()
#         {
#       document.cookie="ccokieenable"
#         cookieEnabled=(document.cookie.indexOf("ccokieenable")!=-1);
#       var elem = document.getElementById("cookiesmessage");  
#             if(!cookieEnabled){
#         elem.innerHTML =  "<div class='info-panel info-panel-full-width test-validation validation-message'><div class='errorWSDL'>We need to use a cookie to manage your secure session.  <br/>Please enable cookies in your browser settings and try again.</div></div>";  
#             }
#             else
#             {
#                elem.innerHTML = "";
#             }
#         }
#     detectCookieActivation();
#     </script>

    

