import gviz_api
import tweepy


#--via @mhawksey
# query string crib https://views.scraperwiki.com/run/python_querystring_cheat_sheet/?
import cgi, os
qstring=os.getenv("QUERY_STRING")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'user' in get:
        user=get['user']
else:
    user = '@billfrasermla'
#---


data=[]
for fo in tweepy.api.followers(user):
    #print fo.screen_name,fo.friends_count,fo.followers_count,fo.statuses_count,fo.created_at,fo.profile_image_url,fo.description,(1.0*fo.friends_count)/(1.0*fo.followers_count),(1.0*fo.statuses_count)/(1.0*fo.followers_count)
    dataLine={'screen_name':fo.screen_name,'fr_count':fo.friends_count,'fo_count':fo.followers_count, "stat_count":fo.statuses_count, "created":fo.created_at, "profile_img":fo.profile_image_url, "desc":fo.description }
    if fo.followers_count>0:
        dataLine["fr_fo_ratio"]=(1.0*fo.friends_count)/(1.0*fo.followers_count)
        dataLine["st_fo_ratio"]=(1.0*fo.statuses_count)/(1.0*fo.followers_count)
    else:
        dataLine["fr_fo_ratio"]=-1
        dataLine["st_fo_ratio"]=-1
    data.append(dataLine)

page_template = """
<html><head><title>Twitter Gardening</title>
  <script src="https://www.google.com/jsapi" type="text/javascript"></script>
  <script>
    google.load('visualization', '1.1', {packages:['controls']});
   google.setOnLoadCallback(drawTable);

    function drawTable() {

      var json_data = new google.visualization.DataTable(%(json)s, 0.6);
    var  formatter = new google.visualization.PatternFormat('<img height=73 width=73 src="{0}" />');
    formatter.format(json_data, [1]); // Apply formatter and set the formatted value of the first column.


formatter = new google.visualization.PatternFormat('<a href="http://twitter.com/{0}">{0}</a>');
    formatter.format(json_data, [0,0]); // Apply formatter and set the formatted value of the first column.

formatter = new google.visualization.NumberFormat({pattern:'#.##'});
  formatter.format(json_data, 7); 
formatter = new google.visualization.NumberFormat({pattern:'#.##'});
  formatter.format(json_data, 8); 

 
var json_table = new google.visualization.ChartWrapper({'chartType': 'Table','containerId':'table_div_json','options': {allowHtml: true}});
//var view = new google.visualization.DataView(json_data);
//    view.setColumns([0,6,1,2,3,4,5])

/*
var stringFilter = new google.visualization.ControlWrapper({
      'controlType': 'StringFilter',
      'containerId': 'control1',
      'options': {
        'filterColumnLabel': 'User',
        'matchType': 'any'
      }
    });
*/
var rangeFilter = new google.visualization.ControlWrapper({
'controlType': 'NumberRangeFilter',
      'containerId': 'control1',
    options:{'filterColumnLabel': 'Followers'}
});
var rangeFilter2 = new google.visualization.ControlWrapper({
'controlType': 'NumberRangeFilter',
      'containerId': 'control2',
    options:{'filterColumnLabel': 'Friends'}
});

  var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard')).bind([rangeFilter,rangeFilter2], json_table).draw(json_data);
 
    }
  </script></head>
  <body><h1>Twitter Gardening</h1>
<p>Twitter gardening tool - most recent 100 or so followers for briankelly (default). Click on column headers to sort table by that column.</p>
<p>To view followers of your own account, use the following URL format:<br/>
https://views.scraperwiki.com/run/twitter_gardening/?user=YOUR_USERNAME_HERE</p>
<div id="dashboard">
    <div><span id="control1"></span> <span id="control2"></span></div>
    <div id="table_div_json"></div>
</div>
  </body>
</html>
"""

description = {"screen_name": ("string", "User"),"profile_img":("string","Icon"),"fr_count": ("number", "Friends"),"fo_count": ("number", "Followers"), "stat_count":("number","Statuses"),"created": ("date", "Created"),"fr_fo_ratio": ("number", "Friends/Followers Ratio"),"st_fo_ratio":("number","Statuses/Followers Ratio"),"desc":('string','Description')}

data_table = gviz_api.DataTable(description)
data_table.LoadData(data)

json = data_table.ToJSon(columns_order=("screen_name","profile_img","desc","fr_count","fo_count","stat_count","created","fr_fo_ratio","st_fo_ratio"),order_by="fr_count")
print page_template % vars()