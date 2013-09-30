import mechanize

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)
response = br.open("http://www.indiapost.gov.in/Pin/")
response.set_data(response.get_data()[3985:])
br.set_response(response)
assert br.viewing_html()
 



br.select_form(nr=0)
br["ddl_dist"] = ["432"]
r2 = br.submit()
print r2.read()
import mechanize

br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_robots(False)
response = br.open("http://www.indiapost.gov.in/Pin/")
response.set_data(response.get_data()[3985:])
br.set_response(response)
assert br.viewing_html()
 



br.select_form(nr=0)
br["ddl_dist"] = ["432"]
r2 = br.submit()
print r2.read()
