import scraperwiki
import mechanize

# https://views.scraperwiki.com/run/python_mechanize_cheat_sheet/

br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

url = 'http://google.com'

response = br.open(url)
# print response.read()

for form in br.forms():
    print "Form name:", form.name
    print form

#form = br.select_form("gbqf")
form = list(br.forms())[0]

for control in form.controls:
    print control
    try: 
        print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
    except TypeError: 
        print "control name must be string-like"
import scraperwiki
import mechanize

# https://views.scraperwiki.com/run/python_mechanize_cheat_sheet/

br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

url = 'http://google.com'

response = br.open(url)
# print response.read()

for form in br.forms():
    print "Form name:", form.name
    print form

#form = br.select_form("gbqf")
form = list(br.forms())[0]

for control in form.controls:
    print control
    try: 
        print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
    except TypeError: 
        print "control name must be string-like"
