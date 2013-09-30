# Download images
# Add images to zip file
# Download zip file

import urllib
import zipfile
import base64
from scraperwiki import dumpMessage as dump_message
from scraperwiki.utils import httpresponseheader as http_header


# Images to download and the file names to save them as
IMAGES = [
    ('img-1.jpeg', 'http://lorempixel.com/200/200/animals/1/'),
    ('img-2.jpeg', 'http://lorempixel.com/200/200/animals/2/'),
    ('img-3.jpeg', 'http://lorempixel.com/200/200/animals/3/'),
    ('img-4.jpeg', 'http://lorempixel.com/200/200/animals/4/'),
    ('img-5.jpeg', 'http://lorempixel.com/200/200/animals/5/'),
]


# Name of the zip file
ZIP_FILE = 'files.zip'


# Open a new zip file for writing
zip = zipfile.ZipFile(ZIP_FILE, 'w')


for filename, url in IMAGES:

    # Download each image and save to tmp directory
    urllib.urlretrieve(url, filename)

    # Add each image to the zip file
    zip.write(filename)


# Close the zip file for writing
zip.close()


# Set the headers to force download of the file
http_header("Content-Type", "application/octet-stream")
http_header("Content-Disposition", "attachment;filename=%s" % ZIP_FILE)


# Return zip file content base64 encoded
# Note that the file is opened in binary read mode (rb)
dump_message({"content":base64.encodestring(open(ZIP_FILE, 'rb').read()), 
              "message_type":"console", 
              "encoding":"base64"})






# Download images
# Add images to zip file
# Download zip file

import urllib
import zipfile
import base64
from scraperwiki import dumpMessage as dump_message
from scraperwiki.utils import httpresponseheader as http_header


# Images to download and the file names to save them as
IMAGES = [
    ('img-1.jpeg', 'http://lorempixel.com/200/200/animals/1/'),
    ('img-2.jpeg', 'http://lorempixel.com/200/200/animals/2/'),
    ('img-3.jpeg', 'http://lorempixel.com/200/200/animals/3/'),
    ('img-4.jpeg', 'http://lorempixel.com/200/200/animals/4/'),
    ('img-5.jpeg', 'http://lorempixel.com/200/200/animals/5/'),
]


# Name of the zip file
ZIP_FILE = 'files.zip'


# Open a new zip file for writing
zip = zipfile.ZipFile(ZIP_FILE, 'w')


for filename, url in IMAGES:

    # Download each image and save to tmp directory
    urllib.urlretrieve(url, filename)

    # Add each image to the zip file
    zip.write(filename)


# Close the zip file for writing
zip.close()


# Set the headers to force download of the file
http_header("Content-Type", "application/octet-stream")
http_header("Content-Disposition", "attachment;filename=%s" % ZIP_FILE)


# Return zip file content base64 encoded
# Note that the file is opened in binary read mode (rb)
dump_message({"content":base64.encodestring(open(ZIP_FILE, 'rb').read()), 
              "message_type":"console", 
              "encoding":"base64"})






