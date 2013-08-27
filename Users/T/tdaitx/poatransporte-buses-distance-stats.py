# Blank Python
sourcescraper = 'poatransporte-buses-distance'

import scraperwiki
import math

# avg and variance from http://www.calebmadrigal.com/standard-deviation-in-python/

def average(s, correction=0): return sum(s) * 1.0 / (len(s)+correction)
        
scraperwiki.sqlite.attach("poatransporte-buses-distance", "dist")

distances = scraperwiki.sqlite.select("distance from dist.swdata")
distances = [d['distance'] for d in distances]

total = sum(distances)
avg = average(distances)
variance = map(lambda x: (x - avg)**2, distances)
std_dev_bias = math.sqrt(average(variance))
std_dev_unbias = math.sqrt(average(variance,1))

print u"%d linhas</br>Total: %f quil\u00F4metros</br>M\u00E9dia: %f</br>biased \u03C3: %f</br>unbiased \u03C3: %f" % (len(distances), total, avg, std_dev_bias, std_dev_unbias)
# Blank Python
sourcescraper = 'poatransporte-buses-distance'

import scraperwiki
import math

# avg and variance from http://www.calebmadrigal.com/standard-deviation-in-python/

def average(s, correction=0): return sum(s) * 1.0 / (len(s)+correction)
        
scraperwiki.sqlite.attach("poatransporte-buses-distance", "dist")

distances = scraperwiki.sqlite.select("distance from dist.swdata")
distances = [d['distance'] for d in distances]

total = sum(distances)
avg = average(distances)
variance = map(lambda x: (x - avg)**2, distances)
std_dev_bias = math.sqrt(average(variance))
std_dev_unbias = math.sqrt(average(variance,1))

print u"%d linhas</br>Total: %f quil\u00F4metros</br>M\u00E9dia: %f</br>biased \u03C3: %f</br>unbiased \u03C3: %f" % (len(distances), total, avg, std_dev_bias, std_dev_unbias)
