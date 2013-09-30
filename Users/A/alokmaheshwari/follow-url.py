import mechanize 
import lxml.html
import scraperwiki  

surl = "http://main.exoclick.com/click.php?data=eGhhbXN0ZXJ8MjQxMjQ3fDB8aHR0cCUzQSUyRiUyRnRyay5rbGlja3RyZWsuY29tJTJGYmFzZS5waHAlM0ZjJTNEODMlMjZrZXklM0Q4NzNkNTA5YWZiNTRjM2RiZjNiMjFiYTFjOGQyMzAxZiUyNnNvdXJjZSUzRHhoYW1zdGVyLmNvbXwzNDk1NHx8MHwxMDB8MTM1MDA3MDUxM3x4aGFtc3Rlci5jb218NDYuNDMuNTUuODd8MjQxMjQ3LTUyMDgxODR8NTIwODE4NHwxMDA2MzN8Mnw3fGE5MjgzZjg2MDBhMjJmNDc1NDI1NDVmODBlNDhmN2Ux&js=1"

br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(True)  # can sometimes hang without this 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 

response = br.open(surl)

print response.read()

br.form = list(br.forms())[0] 

response = br.submit()


print response.geturl()
print response.read() 

#br.set_handle_refresh(True)  # can sometimes hang without this  

#response1 = br.response()  # get the response again
#print response1.read()     # can apply lxml.html.fromstring() 


import mechanize 
import lxml.html
import scraperwiki  

surl = "http://main.exoclick.com/click.php?data=eGhhbXN0ZXJ8MjQxMjQ3fDB8aHR0cCUzQSUyRiUyRnRyay5rbGlja3RyZWsuY29tJTJGYmFzZS5waHAlM0ZjJTNEODMlMjZrZXklM0Q4NzNkNTA5YWZiNTRjM2RiZjNiMjFiYTFjOGQyMzAxZiUyNnNvdXJjZSUzRHhoYW1zdGVyLmNvbXwzNDk1NHx8MHwxMDB8MTM1MDA3MDUxM3x4aGFtc3Rlci5jb218NDYuNDMuNTUuODd8MjQxMjQ3LTUyMDgxODR8NTIwODE4NHwxMDA2MzN8Mnw3fGE5MjgzZjg2MDBhMjJmNDc1NDI1NDVmODBlNDhmN2Ux&js=1"

br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # no robots
br.set_handle_refresh(True)  # can sometimes hang without this 
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')] 

response = br.open(surl)

print response.read()

br.form = list(br.forms())[0] 

response = br.submit()


print response.geturl()
print response.read() 

#br.set_handle_refresh(True)  # can sometimes hang without this  

#response1 = br.response()  # get the response again
#print response1.read()     # can apply lxml.html.fromstring() 


