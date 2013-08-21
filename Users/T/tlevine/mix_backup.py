from scraperwiki.utils import httpresponseheader
import os
slugs = ['mix_backup', 'mix_scraper_spreadsheets']
curls = ['curl --insecure https://scraperwiki.com/editor/raw/{0} > {0}.py 2> /dev/null'.format(slug) for slug in slugs]

# Download and put in a directory
os.system('rm -R mix_backup 2>/dev/null; mkdir mix_backup 2> /dev/null; cd mix_backup 2> /dev/null;' + ';'.join(curls))

# Tar and gzip
os.system('tar czf mix_backup.tar.gz mix_backup 2> /dev/null')

# Print
httpresponseheader('Content-Type', 'application/x-gzip')
print open('mix_backup.tar.gz').read()