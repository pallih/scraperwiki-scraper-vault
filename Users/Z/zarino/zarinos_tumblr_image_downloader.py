import scraperwiki
import zipfile
import re

scraperwiki.utils.httpresponseheader("Content-Type", "application/octet-stream")
scraperwiki.utils.httpresponseheader("Content-Disposition", 'attachment;filename="photos.zip"')

scraperwiki.sqlite.attach("zarinos_tumblr_image_scraper")
photos = scraperwiki.sqlite.select('* from photos')

with zipfile.ZipFile('photos.zip', mode='w') as z:
    for photo in photos:
        z.writestr(re.sub(r'.+/', '', photo['url']), photo['bin'])

print open('photos.zip', 'r').read()