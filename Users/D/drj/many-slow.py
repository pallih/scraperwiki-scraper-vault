open('shcript', 'w').write(
"""#!/bin/sh
# Launch many slow ScraperWiki views.

for a in 1 2 3 4 5 6 7 8 9 10 11 12 13
do
    echo $a
    curl --insecure https://views.scraperwiki.com/run/slow-view/? &
done
""")

import os
os.system("sh shcript")