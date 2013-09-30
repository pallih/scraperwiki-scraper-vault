import scraperwiki

# Blank Python

certid='c7a90eb5-9e30-41fa-bbdc-f7af9293d655'
appid='ScraperW-bbc3-4251-bd57-30dd7b39e5ac'
devid='4b2b2096-feba-4efe-b245-bec234b788c5'
token_raw='''
AgAAAA**AQAAAA**aAAAAA**Cr8OUA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AFkoCpCJGGpwqdj6x9nY+seQ
**qIYBAA**AAMAAA**otY9Y91Gh6pJVJowbj7aBf8SgzKk7nRX8relbYSKLD6qlcDYg/1nvFYRn5imzjvCVQUu
zQouOxrBuB7Us10AWPQ9AfkszP2rppfyM0eW+YZ6uz0DKkykU+VUeipqU/1xW8bqkVGBcku24Smgg5LkJFm04B
kUxKgyN2UfZqEGs6JT/HlzY9lER8nJd0dRW85Gi+Sb3hV7j8zXttfI7fXXtvl85Xbhp37+Sm6G+hdACw6oYLF9
vbQDhy+PWJIFikRmQHQonP3knkMpU3vIW0Qj9eIvFZeJdHJDSRvzUuKskvZyjMreUnRYpLY3FJNa8wTc7jF//m
XU8sMkrvA7ISpkTXkNwp2dK94HK6KLpBbqArfFgR8p/kaRvEQ8akLdt8rL00ctvCu8ypd+C7Btb9VEsqLm5VG7
ZFqUmCAYapKF7mmaAOaLeLNCm5IWb93XmUa1bnuNk/xJ6fUMGhh5fDXU7HQUnIDcIPnPGboWf/t+yDAZYbHKoF
2rm7911wvIGCHGY81pDqdXN+QXaP/1cWN2vekZyq0iMH7mlhfN/Mq+WvQm+Gl/TiBMRG9SPwm43qWqru19fvOu
c8naKumPKD23vAUxKJ76O7rBXmzERw0vPcSO+pg09dFRm1JTlNsTFWcBvGGSd2EanSCERQmm6cIopjMdfj5v01
qNj0yuJ6cF13qykKoYYhNDS7KAlKBz2d6X3dBp5PskezuPItali0qy7s+V/FIqxeA9zAlkoNCb4k0rVy4685+h
OV3q0kvP1GEZ'''
token=''.join(token_raw.strip().split('\n'))

ebaysdk=scraperwiki.swimport('ebay-api')

f = ebaysdk.finding(iaf_token=token, certid=certid, appid=appid, devid=devid)
f.execute('findItemsAdvanced', {'keywords': 'shoes'})

dom    = f.response_dom()
mydict = f.response_dict()
myobj  = f.response_obj()

print myobj.itemSearchURL

# process the response via DOM
items = dom.getElementsByTagName('item')

for item in items:
    print nodeText(item.getElementsByTagName('title')[0])
import scraperwiki

# Blank Python

certid='c7a90eb5-9e30-41fa-bbdc-f7af9293d655'
appid='ScraperW-bbc3-4251-bd57-30dd7b39e5ac'
devid='4b2b2096-feba-4efe-b245-bec234b788c5'
token_raw='''
AgAAAA**AQAAAA**aAAAAA**Cr8OUA**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AFkoCpCJGGpwqdj6x9nY+seQ
**qIYBAA**AAMAAA**otY9Y91Gh6pJVJowbj7aBf8SgzKk7nRX8relbYSKLD6qlcDYg/1nvFYRn5imzjvCVQUu
zQouOxrBuB7Us10AWPQ9AfkszP2rppfyM0eW+YZ6uz0DKkykU+VUeipqU/1xW8bqkVGBcku24Smgg5LkJFm04B
kUxKgyN2UfZqEGs6JT/HlzY9lER8nJd0dRW85Gi+Sb3hV7j8zXttfI7fXXtvl85Xbhp37+Sm6G+hdACw6oYLF9
vbQDhy+PWJIFikRmQHQonP3knkMpU3vIW0Qj9eIvFZeJdHJDSRvzUuKskvZyjMreUnRYpLY3FJNa8wTc7jF//m
XU8sMkrvA7ISpkTXkNwp2dK94HK6KLpBbqArfFgR8p/kaRvEQ8akLdt8rL00ctvCu8ypd+C7Btb9VEsqLm5VG7
ZFqUmCAYapKF7mmaAOaLeLNCm5IWb93XmUa1bnuNk/xJ6fUMGhh5fDXU7HQUnIDcIPnPGboWf/t+yDAZYbHKoF
2rm7911wvIGCHGY81pDqdXN+QXaP/1cWN2vekZyq0iMH7mlhfN/Mq+WvQm+Gl/TiBMRG9SPwm43qWqru19fvOu
c8naKumPKD23vAUxKJ76O7rBXmzERw0vPcSO+pg09dFRm1JTlNsTFWcBvGGSd2EanSCERQmm6cIopjMdfj5v01
qNj0yuJ6cF13qykKoYYhNDS7KAlKBz2d6X3dBp5PskezuPItali0qy7s+V/FIqxeA9zAlkoNCb4k0rVy4685+h
OV3q0kvP1GEZ'''
token=''.join(token_raw.strip().split('\n'))

ebaysdk=scraperwiki.swimport('ebay-api')

f = ebaysdk.finding(iaf_token=token, certid=certid, appid=appid, devid=devid)
f.execute('findItemsAdvanced', {'keywords': 'shoes'})

dom    = f.response_dom()
mydict = f.response_dict()
myobj  = f.response_obj()

print myobj.itemSearchURL

# process the response via DOM
items = dom.getElementsByTagName('item')

for item in items:
    print nodeText(item.getElementsByTagName('title')[0])
