import requests
from lxml.html import fromstring

url = "http://www.opensecrets.org/politicians/summary.php?cid=N00004118&cycle=2012"


r = requests.get(url)
#print r.content
x = fromstring(r.content)
a_nodes = x.cssselect('a')
#assert len(a_nodes[2]) == 1, a_nodes
href = a_nodes[45].attrib['href']
print href

for element in a_nodes:
  print element.get('href')

url1='www.opensecrets.org/usearch/index.php?q=debbie+stabenow'
r1 = requests.get(url)
#print r1.content
x1 = fromstring(r1.content)
a_nodes1 = x1.cssselect('a')
#assert len(a_nodes[2]) == 1, a_nodes

print '************* search ***************'
for element in a_nodes1:
  print element.get('href')

import requests
from lxml.html import fromstring

url = "http://www.opensecrets.org/politicians/summary.php?cid=N00004118&cycle=2012"


r = requests.get(url)
#print r.content
x = fromstring(r.content)
a_nodes = x.cssselect('a')
#assert len(a_nodes[2]) == 1, a_nodes
href = a_nodes[45].attrib['href']
print href

for element in a_nodes:
  print element.get('href')

url1='www.opensecrets.org/usearch/index.php?q=debbie+stabenow'
r1 = requests.get(url)
#print r1.content
x1 = fromstring(r1.content)
a_nodes1 = x1.cssselect('a')
#assert len(a_nodes[2]) == 1, a_nodes

print '************* search ***************'
for element in a_nodes1:
  print element.get('href')

