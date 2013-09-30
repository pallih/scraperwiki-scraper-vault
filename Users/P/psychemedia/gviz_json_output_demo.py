import scraperwiki
import gviz_api

#Example of:
##how to use the Google gviz Python library to cast Scraperwiki data into the Gviz format and export it as JSON

#Based on the code example at:
#http://code.google.com/apis/chart/interactive/docs/dev/gviz_api_lib.html


scraperwiki.sqlite.attach( 'openlearn-units' )
q = 'parentCourseCode,name,topic,unitcode FROM "swdata" LIMIT 20'
data = scraperwiki.sqlite.select(q)

description = {"parentCourseCode": ("string", "Parent Course"),"name": ("string", "Unit name"),"unitcode": ("string", "Unit Code"),"topic":("string","Topic")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("unitcode","name", "topic","parentCourseCode" ),order_by="unitcode")

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print 'ousefulHack('+json+')'
import scraperwiki
import gviz_api

#Example of:
##how to use the Google gviz Python library to cast Scraperwiki data into the Gviz format and export it as JSON

#Based on the code example at:
#http://code.google.com/apis/chart/interactive/docs/dev/gviz_api_lib.html


scraperwiki.sqlite.attach( 'openlearn-units' )
q = 'parentCourseCode,name,topic,unitcode FROM "swdata" LIMIT 20'
data = scraperwiki.sqlite.select(q)

description = {"parentCourseCode": ("string", "Parent Course"),"name": ("string", "Unit name"),"unitcode": ("string", "Unit Code"),"topic":("string","Topic")}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("unitcode","name", "topic","parentCourseCode" ),order_by="unitcode")

scraperwiki.utils.httpresponseheader("Content-Type", "application/json")
print 'ousefulHack('+json+')'
