import scraperwiki

import os
for root, dirs, files in os.walk('.'):
    for i, name in enumerate(files):
        n = os.path.join(root, name)
        scraperwiki.sqlite.save(['line'], dict(line=i,text=n))
import scraperwiki

import os
for root, dirs, files in os.walk('.'):
    for i, name in enumerate(files):
        n = os.path.join(root, name)
        scraperwiki.sqlite.save(['line'], dict(line=i,text=n))
