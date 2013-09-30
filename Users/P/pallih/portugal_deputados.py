import scraperwiki
import mechanize
import lxml.html
import re
import urllib
import urllib2



b = mechanize.Browser()
b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
b.set_handle_robots(False) #just to speed it up - the robots.txt is empty anyway

def extract(text, sub1, sub2):
    """extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]

regex = re.compile(".*BID=(\d.*)")

b.open("http://www.parlamento.pt/DeputadoGP/Paginas/Deputados.aspx")
response = b.response().read()
root = lxml.html.fromstring(response)
results = root.xpath('//tr[contains(@class,"ARTabResultadosLinhaImpar")]/. | //tr[contains(@class,"ARTabResultadosLinhaPar")]/.')

current_page = root.xpath('//tr[contains(@class, "ARLabel")]//td[1]')
next_page = root.xpath('//tr[contains(@class, "ARLabel")]//a')
next_page_number = int(current_page[1].text_content())+1
next_page_string = "','Page$" + str(next_page_number) + "')"
print next_page_string
print 'next page number?: ', next_page_number
print 'current page: ', current_page[1].text_content()

print 'next page: ', next_page[0].get('href')

for link in b.links(url_regex ='javascript:'): 
    #print link.attrs, ' - ', link.text        
    if re.search(str(next_page_number), str(link.text)):
#   next_page_to_do = int(link.text) + 1
        print 'there is a next page - ',  next_page[0].get('href')
        next_link_to_do = str(next_page[0].get('href'))
        print next_link_to_do
        special_form_element = extract(next_link_to_do, "javascript:__doPostBack('",str(next_page_string))
        #ctl00$ctl22 = ''
        for form in b.forms():
            print form
            print 'thats'
        b.select_form(name="aspnetForm")
        b.form.set_all_readonly(False)
        print b.form
        b.form.new_control('hidden','ctl00$ctl22',{'value':''})
        b.form.fixup()
        b.form.set_all_readonly(False)
        print b.form
        #b.form['ctl00$ctl22'] = 'ctl00$ctl13$g_4090e9c6_d794_4506_9ff9_3e6f8d30ec2d$ctl00$pnlUpdate|ctl00$ctl13$g_4090e9c6_d794_4506_9ff9_3e6f8d30ec2d$ctl00$gvResultsByDate'
        b.form['__EVENTTARGET'] = special_form_element
        b.form['__EVENTARGUMENT'] = 'Page$' + str(next_page_number)

        b.form['ctl00$ctl22'] = ''
        print b.form

        response = b.submit().read()
        print response
        root = lxml.html.fromstring(response)
        current_page = root.xpath('//tr[contains(@class, "ARLabel")]//td[1]')
        next_page = root.xpath('//tr[contains(@class, "ARLabel")]//a')
        next_page_number = int(current_page[1].text_content())+1
        next_page_string = "','Page$" + str(next_page_number) + "')"
        print next_page_string
        print 'next page number?: ', next_page_number
        print 'current page: ', current_page[1].text_content()

        print 'next page: ', next_page[0].get('href')

        


def process(results):
    for r in results:
        record = {}
        record['nome'] = r[0].text_content().strip()
        record ['bid'] = regex.findall(r[5][0].get('href'))[0]
        print record
        #scraperwiki.sqlite.save(['bid'], data=record, table_name='portugal_deputados')

import scraperwiki
import mechanize
import lxml.html
import re
import urllib
import urllib2



b = mechanize.Browser()
b.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')]
b.set_handle_robots(False) #just to speed it up - the robots.txt is empty anyway

def extract(text, sub1, sub2):
    """extract a substring between two substrings sub1 and sub2 in text"""
    return text.split(sub1)[-1].split(sub2)[0]

regex = re.compile(".*BID=(\d.*)")

b.open("http://www.parlamento.pt/DeputadoGP/Paginas/Deputados.aspx")
response = b.response().read()
root = lxml.html.fromstring(response)
results = root.xpath('//tr[contains(@class,"ARTabResultadosLinhaImpar")]/. | //tr[contains(@class,"ARTabResultadosLinhaPar")]/.')

current_page = root.xpath('//tr[contains(@class, "ARLabel")]//td[1]')
next_page = root.xpath('//tr[contains(@class, "ARLabel")]//a')
next_page_number = int(current_page[1].text_content())+1
next_page_string = "','Page$" + str(next_page_number) + "')"
print next_page_string
print 'next page number?: ', next_page_number
print 'current page: ', current_page[1].text_content()

print 'next page: ', next_page[0].get('href')

for link in b.links(url_regex ='javascript:'): 
    #print link.attrs, ' - ', link.text        
    if re.search(str(next_page_number), str(link.text)):
#   next_page_to_do = int(link.text) + 1
        print 'there is a next page - ',  next_page[0].get('href')
        next_link_to_do = str(next_page[0].get('href'))
        print next_link_to_do
        special_form_element = extract(next_link_to_do, "javascript:__doPostBack('",str(next_page_string))
        #ctl00$ctl22 = ''
        for form in b.forms():
            print form
            print 'thats'
        b.select_form(name="aspnetForm")
        b.form.set_all_readonly(False)
        print b.form
        b.form.new_control('hidden','ctl00$ctl22',{'value':''})
        b.form.fixup()
        b.form.set_all_readonly(False)
        print b.form
        #b.form['ctl00$ctl22'] = 'ctl00$ctl13$g_4090e9c6_d794_4506_9ff9_3e6f8d30ec2d$ctl00$pnlUpdate|ctl00$ctl13$g_4090e9c6_d794_4506_9ff9_3e6f8d30ec2d$ctl00$gvResultsByDate'
        b.form['__EVENTTARGET'] = special_form_element
        b.form['__EVENTARGUMENT'] = 'Page$' + str(next_page_number)

        b.form['ctl00$ctl22'] = ''
        print b.form

        response = b.submit().read()
        print response
        root = lxml.html.fromstring(response)
        current_page = root.xpath('//tr[contains(@class, "ARLabel")]//td[1]')
        next_page = root.xpath('//tr[contains(@class, "ARLabel")]//a')
        next_page_number = int(current_page[1].text_content())+1
        next_page_string = "','Page$" + str(next_page_number) + "')"
        print next_page_string
        print 'next page number?: ', next_page_number
        print 'current page: ', current_page[1].text_content()

        print 'next page: ', next_page[0].get('href')

        


def process(results):
    for r in results:
        record = {}
        record['nome'] = r[0].text_content().strip()
        record ['bid'] = regex.findall(r[5][0].get('href'))[0]
        print record
        #scraperwiki.sqlite.save(['bid'], data=record, table_name='portugal_deputados')

