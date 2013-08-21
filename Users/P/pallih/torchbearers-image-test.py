import scraperwiki

url = 'http://www.london2012.com/imgml/torchbearers/%s/1D94-C5DD-593F-494A.jpg'

import string 


alpha = string.lowercase

for i in alpha:
    print '<img src="'+ url %  i+'">'