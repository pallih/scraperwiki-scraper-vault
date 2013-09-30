import Image
a = Image.new("RGB",(10,10))
import StringIO
b = StringIO.StringIO()
a.save(b, "jpeg")


scraperwiki.utils.httpresponseheader("Content-Type", "image/jpg")
print b.getvalue()
import Image
a = Image.new("RGB",(10,10))
import StringIO
b = StringIO.StringIO()
a.save(b, "jpeg")


scraperwiki.utils.httpresponseheader("Content-Type", "image/jpg")
print b.getvalue()
