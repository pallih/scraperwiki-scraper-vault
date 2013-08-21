# Blank Python
import scraperwiki, random, math
import numpy as np
import scipy as sp
import pylab
import cStringIO
from scipy import spatial
from scipy import cluster

sourcescraper = 'clustertenderpy'
scraperwiki.sqlite.attach('clustertenderpy')

lm = scraperwiki.sqlite.select("* from swdata")
print lm[0]['linkageMatrix']

linkageMatrix = np.array(lm[0]['linkageMatrix'],dtype=np.float64)
print type(linkageMatrix[0])

cluster.hierarchy.dendrogram(linkageMatrix[0]['linkageMatrix'])


from matplotlib.pyplot import show


fig, ax = plt.subplots(1,1)

dendrogram=cluster.hierarchy.dendrogram(linkageMatrix)

ax.plot(dendrogram)

# Save the generated figure to a file
stream = cStringIO.StringIO()
fig.savefig(stream,format='png')

# Some http stuff..
scraperwiki.utils.httpresponseheader("Content-Type", "image/png")
scraperwiki.dumpMessage({"content":base64.encodestring(stream.getvalue()), "message_type":"console", "encoding":"base64"})