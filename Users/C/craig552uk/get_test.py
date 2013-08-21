#
# Test to handle query string params
# 


from scraperwiki.utils import httpresponseheader as http_header
from scraperwiki.utils import GET as query_string

# Get query string parameters
qs = query_string()


# Download file if value submitted
if 'id' in qs:

    http_header("Content-Type", "application/octet-stream")
    http_header("Content-Disposition", "attachment; filename=file.txt")
    print "Hello world"
    print "Your id is %s" % qs['id']

else:
    # Form to submit value
    print """
    <form>
        <p><input type="text" name="id"/></p>
        <p><input type="submit" value="Download File"></p>
    </form>
    """