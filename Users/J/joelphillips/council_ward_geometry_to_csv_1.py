import scraperwiki
import scraperwiki.sqlite as db
import cgi, os
import sys        

params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
scraper = scraperwiki.utils.swimport('council_ward_geometry' ) 
db.execute('create table if not exists swdata (parent_area, id, name, kml)')
db.execute('create table if not exists counts (parent_area, count int)')



# ajax handler
if 'parent_area' in params:
    parent = int(params['parent_area'])
    count = db.select('count() from swdata where parent_area=?', parent)[0]['count()']
    if not count:
        count = scraper.save_kml_for_children_of(parent)
        print '<p>Scraped new data</p>'
    total_count = count
    rows = db.select('count from counts where parent_area=?', parent)
    if rows:
        total_count = rows[0]['count']

    print '<p>There is {0} of {1} records for id {2}</p>'.format(count, total_count, parent)
    if count < total_count:
        print '<p>Please wait and resubmit form to get all results</p>'
    print  '<a href="https://api.scraperwiki.com/api/1.0/datastore/sqlite?'\
           'format=csv&name=council_ward_geometry_to_csv&query=select%20*%20from%20%60swdata%60%20'\
           'where%20parent_area%3D{0}">Download as CSV</a>'.format(parent)
    sys.exit()

# main form
print """
<html>
<head>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $('.button').click(function(){
        var url = window.location.href;
        console.log(url);
        $('#results').html('Loading...');
        var loader = function(){
            $.ajax({
                url: url,
                data: {parent_area: $('input#parent_area').val()},
                success: function(data){$('#results').html(data);},
                error: function(){
                    setTimeout(loader, 10000);
                    $('#results').html('Scraping data, please wait...');
                },
            });
        }
        loader();
        return false;
    });
});
</script>
</head>
<body>
    <form method="get" action="">
    Parent area id: <input type="text" name="parent_area" id="parent_area" value=></input>
    <input type="submit" class="button">
    </form>
    <hr></hr>
    <div id="results">
    </div>
</body>
</html>
"""

import scraperwiki
import scraperwiki.sqlite as db
import cgi, os
import sys        

params = dict(cgi.parse_qsl(os.getenv("QUERY_STRING", "")))
scraper = scraperwiki.utils.swimport('council_ward_geometry' ) 
db.execute('create table if not exists swdata (parent_area, id, name, kml)')
db.execute('create table if not exists counts (parent_area, count int)')



# ajax handler
if 'parent_area' in params:
    parent = int(params['parent_area'])
    count = db.select('count() from swdata where parent_area=?', parent)[0]['count()']
    if not count:
        count = scraper.save_kml_for_children_of(parent)
        print '<p>Scraped new data</p>'
    total_count = count
    rows = db.select('count from counts where parent_area=?', parent)
    if rows:
        total_count = rows[0]['count']

    print '<p>There is {0} of {1} records for id {2}</p>'.format(count, total_count, parent)
    if count < total_count:
        print '<p>Please wait and resubmit form to get all results</p>'
    print  '<a href="https://api.scraperwiki.com/api/1.0/datastore/sqlite?'\
           'format=csv&name=council_ward_geometry_to_csv&query=select%20*%20from%20%60swdata%60%20'\
           'where%20parent_area%3D{0}">Download as CSV</a>'.format(parent)
    sys.exit()

# main form
print """
<html>
<head>
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
<script>
$(document).ready(function(){
    $('.button').click(function(){
        var url = window.location.href;
        console.log(url);
        $('#results').html('Loading...');
        var loader = function(){
            $.ajax({
                url: url,
                data: {parent_area: $('input#parent_area').val()},
                success: function(data){$('#results').html(data);},
                error: function(){
                    setTimeout(loader, 10000);
                    $('#results').html('Scraping data, please wait...');
                },
            });
        }
        loader();
        return false;
    });
});
</script>
</head>
<body>
    <form method="get" action="">
    Parent area id: <input type="text" name="parent_area" id="parent_area" value=></input>
    <input type="submit" class="button">
    </form>
    <hr></hr>
    <div id="results">
    </div>
</body>
</html>
"""

