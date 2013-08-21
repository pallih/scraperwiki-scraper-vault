import scraperwiki
import mechanize
import lxml.html
import cgi
import time

def select_form():
    br.select_form('aspnetForm')    # works when form has a name
    br.form.set_all_readonly(False)

def loop_control_and_read_text_output():
    select_form()
    control = br.form.find_control('ctl00$cphMainContent$cboMetalCaster')
    record = {}

    for item in control.items:
        print item
        select_form()
        br['ctl00$cphMainContent$cboMetalCaster'] = [str(item)]  #We're selecting from the MetalCaster drop down
        response1 = br.submit('ctl00$cphMainContent$btnShowMetalCasterInfo')
        print item, response1.read()
        time.sleep(4)
        select_form()
        br['__EVENTTARGET'] = 'ctl00$cphMainContent$gvNonMemberResults'
        br['__EVENTARGUMENT'] = 'Select$0'

        # disable all the submit buttons (otherwise br.submit picks one for you (eg btnHelp) and the server responds to it)
        for control in br.form.controls:
            if control.type == "submit":
                control.disabled = True

            try:
                request = br.click()
            except mechanize.HTTPError, request:
                continue
            else:
                response = br.open(request)
                htmlread = response.read()
                root = lxml.html.fromstring(htmlread)
        
                #Save the textarea data
                record['ID'] = str(item)
                record['Data'] = root.cssselect("textarea")[0].text.partition("====")[0]
                print record['Data']
                scraperwiki.sqlite.save(['ID'], record)

print "starting"

br = mechanize.Browser()
br.set_handle_robots(True)   # no robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

# Open a webpage and inspect its contents
url = "http://www.metalcastingvirtuallibrary.com/foundry/foundry.aspx"
response = br.open(url)
loop_control_and_read_text_output()
