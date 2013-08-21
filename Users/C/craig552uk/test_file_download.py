from datetime import datetime as dt
import scraperwiki


# Define the file name
timestamp = dt.now().strftime("%Y-%m-%d-%H-%M-%S")
FILE_NAME="downloaded_file_%s.txt" % timestamp


# Set the headers to force download of the file
scraperwiki.utils.httpresponseheader("Content-Type", "application/octet-stream")
scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment; filename=%s" % FILE_NAME)


# Construct the file content
print "Hello world"
print "How are you today?"