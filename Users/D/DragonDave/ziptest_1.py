# Blank Python
import StringIO
import scraperwiki
import zipfile
import random

scraperwiki.utils.httpresponseheader("Content-Type", "application/zip")

zio=StringIO.StringIO()
zfile=zipfile.ZipFile(zio, 'w', zipfile.ZIP_DEFLATED)
i='0'*10000 # 10kb

for j in range(1,10000): # number of files
    x=str(random.randint(0,1e9))
    zfile.writestr(x,i)

print zio.getvalue()
