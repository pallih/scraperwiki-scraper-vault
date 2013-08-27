<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <title>Dynamic Form Population With jQuery</title>
    <script type="text/javascript" src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
    <script type="text/javascript">
var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsonlist&name=irish_president_engagementsjson&query=select%20*%20from%20%60swdata%60%20limit%2010";            
var srcname = "irish_president_engagementsjson"; 
var sqlselect = "select * from swdata limit 10"; 
$.ajax({
    url: apiurl, 
    dataType: "jsonp", 
    data:{
        name: srcname, 
        query: sqlselect, 
        format: "jsonlist"
    }, 
    success: function(data){
        alert(data);
    }
});


 </script></head><body><div></div></body></html><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <title>Dynamic Form Population With jQuery</title>
    <script type="text/javascript" src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
    <script type="text/javascript">
var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsonlist&name=irish_president_engagementsjson&query=select%20*%20from%20%60swdata%60%20limit%2010";            
var srcname = "irish_president_engagementsjson"; 
var sqlselect = "select * from swdata limit 10"; 
$.ajax({
    url: apiurl, 
    dataType: "jsonp", 
    data:{
        name: srcname, 
        query: sqlselect, 
        format: "jsonlist"
    }, 
    success: function(data){
        alert(data);
    }
});


 </script></head><body><div></div></body></html><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <title>Dynamic Form Population With jQuery</title>
    <script type="text/javascript" src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
    <script type="text/javascript">
var apiurl = "https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsonlist&name=irish_president_engagementsjson&query=select%20*%20from%20%60swdata%60%20limit%2010";            
var srcname = "irish_president_engagementsjson"; 
var sqlselect = "select * from swdata limit 10"; 
$.ajax({
    url: apiurl, 
    dataType: "jsonp", 
    data:{
        name: srcname, 
        query: sqlselect, 
        format: "jsonlist"
    }, 
    success: function(data){
        alert(data);
    }
});


 </script></head><body><div></div></body></html>