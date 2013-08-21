from rpy2 import robjects
from rpy2.robjects.lib import grid
from rpy2.robjects.packages import importr

from cStringIO import StringIO

# The R 'print' function
rprint = robjects.globalenv.get("print")
stats = importr('stats')
grdevices = importr('grDevices')
base = importr('base')

ggplot2 = importr('ggplot2')

lattice = importr('lattice')
xyplot = lattice.xyplot
datasets = importr('datasets')
mtcars = datasets.mtcars
formula = robjects.Formula('mpg ~ wt')
formula.getenvironment()['mpg'] = mtcars.rx2('mpg')
formula.getenvironment()['wt'] = mtcars.rx2('wt')

from scraperwiki import dumpMessage,utils

format = "png"
imagedata = StringIO()

r = robjects.r
#r.png doesn't seem willing to write to StringIO(), maybe becuase we donlt have chart data yet?
r.png(imagedata)

lattice.xyplot(formula)

r('dev.off()')
#plt.savefig(imagedata, format=format, dpi=96)
utils.httpresponseheader("Content-Type", "image/%s" % format)
dumpMessage({"content": imagedata.getvalue().encode("base64"), "message_type": "console", "encoding":"base64"})

