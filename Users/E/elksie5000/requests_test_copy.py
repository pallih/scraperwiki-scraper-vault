
import scraperwiki
import requests
import lxml.html
import re

#Staffs
#http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0r_PNVmZdJRr416ajTQptALCe0mm-VPKJ/HAHTpage/cl_search.Hsresults.run?cboCourse=-&cboInst=S72&cboRegion=0&cboLevel=0&stype=H&Submit=search&scotSearch=0
#Submit    search
#cboCourse    -
#cboInst    S72
#cboLevel    0
#cboRegion    0
#scotSearch    0
#stype    H



url = "http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run"

#http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0rsG9VmXr2RrU1EajTL-KS1ChDPA-Vz5r/HAHTpage/cl_search.Hssearchh.run

#http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0r_PNVmZdJRr416ajTQptALCe0mm-VPKJ/HAHTpage/cl_search.Hsresults.run?cboCourse=-&cboInst=S72&cboRegion=0&cboLevel=0&stype=H&Submit=search&scotSearch=0

staffs_uni_search = {'Submit' : 'search',
                    'cboCourse' : '-',
                    'cboInst': 'S72',
                    'cboLevel': '0',
                    'cboRegion': '0',
                    'scotSearch':'0',
                    'stype': 'H',}

s = requests.session()
c = requests.request(cookies, url)
print c.text

r = s.get(url)

print r.text


#print r.headers

#cookies = r.cookies

#print cookies.text

#s = requests.get(url, params=staffs_uni_search)


import scraperwiki
import requests
import lxml.html
import re

#Staffs
#http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0r_PNVmZdJRr416ajTQptALCe0mm-VPKJ/HAHTpage/cl_search.Hsresults.run?cboCourse=-&cboInst=S72&cboRegion=0&cboLevel=0&stype=H&Submit=search&scotSearch=0
#Submit    search
#cboCourse    -
#cboInst    S72
#cboLevel    0
#cboRegion    0
#scotSearch    0
#stype    H



url = "http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/cl_search.hjx;start=cl_search.Hspresearch.run"

#http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0rsG9VmXr2RrU1EajTL-KS1ChDPA-Vz5r/HAHTpage/cl_search.Hssearchh.run

#http://clearing.ucas.com/cgi-bin/hsrun/clv02/cl_search12/StateId/E0r_PNVmZdJRr416ajTQptALCe0mm-VPKJ/HAHTpage/cl_search.Hsresults.run?cboCourse=-&cboInst=S72&cboRegion=0&cboLevel=0&stype=H&Submit=search&scotSearch=0

staffs_uni_search = {'Submit' : 'search',
                    'cboCourse' : '-',
                    'cboInst': 'S72',
                    'cboLevel': '0',
                    'cboRegion': '0',
                    'scotSearch':'0',
                    'stype': 'H',}

s = requests.session()
c = requests.request(cookies, url)
print c.text

r = s.get(url)

print r.text


#print r.headers

#cookies = r.cookies

#print cookies.text

#s = requests.get(url, params=staffs_uni_search)

