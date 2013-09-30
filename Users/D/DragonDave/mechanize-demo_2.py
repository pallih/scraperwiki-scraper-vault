import re
import mechanize

br = mechanize.Browser()
br.open("https://secure.citysocialising.com/user/user_login.html?dest=http%3A%2F%2Fliverpool.citysocialising.com%2Fhome.html") # login page

br.select_form(nr=0)
br["user_login_username"] = "username" 
br["user_login_password"] = "password"
print br.form
response2 = br.submit()

print response2.read()import re
import mechanize

br = mechanize.Browser()
br.open("https://secure.citysocialising.com/user/user_login.html?dest=http%3A%2F%2Fliverpool.citysocialising.com%2Fhome.html") # login page

br.select_form(nr=0)
br["user_login_username"] = "username" 
br["user_login_password"] = "password"
print br.form
response2 = br.submit()

print response2.read()