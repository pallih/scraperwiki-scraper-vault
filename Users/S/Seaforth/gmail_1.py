from lxml.html import fromstring
from requests import session
from scraperwiki.sqlite import save_var, get_var
import re

class Gmail:
    def __init__(self, emailaddress, password):
        self.emailaddress = emailaddress
        self.password = password
        self.s = session()
        self.login()

    def login(self):
        "log in and go to the inbox"
        # Gmail.com
        r = self.s.get('http://gmail.com', verify = False)
        
        # Fill form
        inputs = fromstring(r.text).xpath('id("gaia_loginform")/descendant::input')
        params = {input.attrib['name']: input.get('value', '') for input in inputs}
        params.update({'Email': self.emailaddress, 'Passwd': self.password})
        r = self.s.post("https://accounts.google.com/ServiceLoginAuth", params, verify = False)
        r = self.s.get('https://mail.google.com/mail/u/0', verify = False)
        print(r.text)
        #r = self.s.get(r.headers['location'], verify = False)
        self.inbox = r.text
        print(self.inbox)
        self.inbox_href = r.url
        print("logged in")

    def urls_of_emails_with_attachments(self):
        "returns a list of the urls of emails with attachments"
        html = fromstring(self.inbox)
        message_link_nodes = html.xpath('//img[@src="/mail/u/0/images/paperclip.gif"]/following-sibling::a')
        for m in message_link_nodes:
            m.make_links_absolute(self.inbox_href)
        message_urls = [m.attrib['href'] for m in message_link_nodes]
        return message_urls

    def urls_of_all_emails(self):
        print(fromstring(self.inbox))
        html = fromstring(self.inbox)
        message_link_nodes = html.xpath('//form[@name="f"]/descendant::td[@width="73%"]/a')
        print(message_link_nodes )
        for m in message_link_nodes:
            print("1")
            m.make_links_absolute(self.inbox_href)
        message_urls = [m.attrib['href'] for m in message_link_nodes]
        return message_urls

    def get_first_pdf_attachment(self, message_url):
        r = self.s.get(message_url, verify = False)
        html = fromstring(r.text)
        attachment_link_nodes = html.xpath('//a[@target="_blank"][img[@src="/mail/u/0/images/pdf.gif"]]')
        for a in attachment_link_nodes:
            a.make_links_absolute(r.url)
        attachment_urls = [a.attrib['href'] for a in attachment_link_nodes]
        r = self.s.get(attachment_urls[0], verify = False)
        filename = re.match('attachment; filename="([^"]+)"', r.headers['content-disposition']).group(1)
        return filename, r.content

gm = Gmail("annontmousmra.test@gmail.com." , "testtesty")

lsURLs = gm.urls_of_all_emails()


print(lsURLs)
for a in lsURLs:
    print(a)



from lxml.html import fromstring
from requests import session
from scraperwiki.sqlite import save_var, get_var
import re

class Gmail:
    def __init__(self, emailaddress, password):
        self.emailaddress = emailaddress
        self.password = password
        self.s = session()
        self.login()

    def login(self):
        "log in and go to the inbox"
        # Gmail.com
        r = self.s.get('http://gmail.com', verify = False)
        
        # Fill form
        inputs = fromstring(r.text).xpath('id("gaia_loginform")/descendant::input')
        params = {input.attrib['name']: input.get('value', '') for input in inputs}
        params.update({'Email': self.emailaddress, 'Passwd': self.password})
        r = self.s.post("https://accounts.google.com/ServiceLoginAuth", params, verify = False)
        r = self.s.get('https://mail.google.com/mail/u/0', verify = False)
        print(r.text)
        #r = self.s.get(r.headers['location'], verify = False)
        self.inbox = r.text
        print(self.inbox)
        self.inbox_href = r.url
        print("logged in")

    def urls_of_emails_with_attachments(self):
        "returns a list of the urls of emails with attachments"
        html = fromstring(self.inbox)
        message_link_nodes = html.xpath('//img[@src="/mail/u/0/images/paperclip.gif"]/following-sibling::a')
        for m in message_link_nodes:
            m.make_links_absolute(self.inbox_href)
        message_urls = [m.attrib['href'] for m in message_link_nodes]
        return message_urls

    def urls_of_all_emails(self):
        print(fromstring(self.inbox))
        html = fromstring(self.inbox)
        message_link_nodes = html.xpath('//form[@name="f"]/descendant::td[@width="73%"]/a')
        print(message_link_nodes )
        for m in message_link_nodes:
            print("1")
            m.make_links_absolute(self.inbox_href)
        message_urls = [m.attrib['href'] for m in message_link_nodes]
        return message_urls

    def get_first_pdf_attachment(self, message_url):
        r = self.s.get(message_url, verify = False)
        html = fromstring(r.text)
        attachment_link_nodes = html.xpath('//a[@target="_blank"][img[@src="/mail/u/0/images/pdf.gif"]]')
        for a in attachment_link_nodes:
            a.make_links_absolute(r.url)
        attachment_urls = [a.attrib['href'] for a in attachment_link_nodes]
        r = self.s.get(attachment_urls[0], verify = False)
        filename = re.match('attachment; filename="([^"]+)"', r.headers['content-disposition']).group(1)
        return filename, r.content

gm = Gmail("annontmousmra.test@gmail.com." , "testtesty")

lsURLs = gm.urls_of_all_emails()


print(lsURLs)
for a in lsURLs:
    print(a)



