from cStringIO import StringIO

from scraperwiki import dumpMessage, sqlite, utils

sourcescraper = 'solid_state_drives'

sqlite.attach(sourcescraper, "src")
data = sqlite.select('* from src.swdata')

from pprint import pprint

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

xs, ys, ys_div = [], [], []
for element in data:
    if not element["size"]: continue
    xs.append(float(element["price"]))
    ys.append(float(element["size"][:-2]))
    ys_div.append(xs[-1] / ys[-1])

subplot = plt.subplot(211)
plt.xlabel(u"Price (GBP)")
plt.ylabel(u"Size (GB)")
subplot.scatter(xs, ys)

subplot = plt.subplot(212)
plt.xlabel(u"Price (GBP)")
plt.ylabel(u"Price / Size (GB)")
subplot.scatter(xs, ys_div)

format = "png"
imagedata = StringIO()
plt.savefig(imagedata, format=format, dpi=96)
utils.httpresponseheader("Content-Type", "image/%s" % format)
dumpMessage({"content": imagedata.getvalue().encode("base64"), "message_type": "console", "encoding":"base64"})
from cStringIO import StringIO

from scraperwiki import dumpMessage, sqlite, utils

sourcescraper = 'solid_state_drives'

sqlite.attach(sourcescraper, "src")
data = sqlite.select('* from src.swdata')

from pprint import pprint

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

xs, ys, ys_div = [], [], []
for element in data:
    if not element["size"]: continue
    xs.append(float(element["price"]))
    ys.append(float(element["size"][:-2]))
    ys_div.append(xs[-1] / ys[-1])

subplot = plt.subplot(211)
plt.xlabel(u"Price (GBP)")
plt.ylabel(u"Size (GB)")
subplot.scatter(xs, ys)

subplot = plt.subplot(212)
plt.xlabel(u"Price (GBP)")
plt.ylabel(u"Price / Size (GB)")
subplot.scatter(xs, ys_div)

format = "png"
imagedata = StringIO()
plt.savefig(imagedata, format=format, dpi=96)
utils.httpresponseheader("Content-Type", "image/%s" % format)
dumpMessage({"content": imagedata.getvalue().encode("base64"), "message_type": "console", "encoding":"base64"})
