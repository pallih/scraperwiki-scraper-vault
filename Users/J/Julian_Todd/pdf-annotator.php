<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>PDF Cropper</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery.autoheight.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com//js/jquery.Jcrop.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <style type="text/css">
        .dpdfpagediv { border: thick red solid; width:800px }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #annottext { clear:both; width: 100%; height: 100px; overflow: auto}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var cropperapi; 
function setCrop(c)
{
    var dlk = c.x + " " + c.y + " " + c.x2 + " " + c.y2; 
    $('#consolidatelink').text(dlk); 
};


function appendannotation(lid, rectstring, txt)
{
    $('ul#goingnotes').append($('<li id="'+lid+'"><b>'+rectstring+'</b> <span>'+txt+'</span></li>')); 
    $('#annottext').val(""); 
    // apply the click link to it
    $('#'+lid + " b").click(function() 
    {
        var txt = $(this).next('span').text(); 
        $('#annottext').val(txt); 
        var rect = $(this).text().split(" "); 
        if (cropperapi)
            cropperapi.animateTo([parseInt(rect[0]), parseInt(rect[1]), parseInt(rect[2]), parseInt(rect[3])]);
    }); 
}

var trowid = 10; 
var pagebasereq = ""; 
function commit()
{
    // add the new text into our list
    var txt = $('#annottext').val(); 
    if (txt == "")
        return; 

    var username = $.trim($('#username').val()); 
    if (username == "")
        { alert("Please enter a username"); return }

    var lid = 'g'+trowid; 
    trowid++; 
    appendannotation(lid, $('#consolidatelink').text(), txt); 

    // send the value up to the server
    var values = [ ]; 
    values.push("user="+escape(username)); 
    var rect = $('#consolidatelink').text().split(" "); 
    values.push("x="+rect[0]+"&y="+rect[1]+"&x2="+rect[2]+"&y2="+rect[3]); 
    values.push("imgwidth=800&imgheight=1200"); 
    values.push("content="+escape(txt)); 
    //alert(pagebasereq+"&"+values.join("&")); 

    $.ajax({url:pagebasereq+"&"+values.join("&"), success: function(sdata)
    {
        var data = $.evalJSON(sdata);
        if (data["status"] != "Okay")
            alert(sdata); // would be better with rowid
    }}); 
}

$(document).ready(function() 
{ 
    pagebasereq = "http://scraperwikiviews.com/run/pdf-annotator-database/?pdfurl="+escape($("#pdfurl").attr("href"))+
                  "&pagenumber="+escape($("#pagenumber").text()); 

    $('#pdfpageid').load(function() 
    { 
        // consider boxWidth:800 of setting the real width so it handles its own scaling
        cropperapi = $.Jcrop('#pdfpageid', { onSelect: setCrop, onChange: setCrop, keySupport: false } ); 

        $.ajax({url:pagebasereq, success: function(sdata)
        {
            var data = $.evalJSON(sdata);
            for (var i=0; i < data.length; i++)
                appendannotation("u"+data[i].rowid, data[i].x+" "+data[i].y+" "+data[i].x2+" "+data[i].y2, data[i].content); 
        }}); 
        $("#commitbutton").click(commit); 
    }); 
});

    </script>
</head>
<body class="fullscreen">

<div>
<?php 
  parse_str(getenv("URLQUERY"), $output); 
  $pagenumber = intval(array_key_exists("pagenumber", $output) ? $output["pagenumber"] : "1"); 
  $pdfurl = (array_key_exists("pdfurl", $output) ? $output["pdfurl"] : "http://www.kytreasury.com/NR/rdonlyres/F5AF58E8-7F9E-4067-B31C-AE68EC9F1AE0/0/CaseyCounty.pdf"); 
  $imgsrc = "http://scraperwiki.com/cropper/png/u/page_$pagenumber?".http_build_query(array('url'=>$pdfurl)); 
?>
  <h2>Page <span id="pagenumber"><?php echo $pagenumber; ?></span> of 
    <a id="pdfurl" href="<?php echo $pdfurl; ?>"><?php echo $pdfurl; ?></a> 
  </h2>
  <p>
    <?php if ($pagenumber > 1) { ?>
      <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber-1)); ?>">prev page</a> 
    <?php } ?>
    <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber+1)); ?>">next page</a> 
    <a href="http://scraperwikiviews.com/run/pdf-annotator-database/">Main index</a>
    </p>
</div> 

<div id="annotate">
  Location rectangle <b id="consolidatelink">...</b>
  <textarea id="annottext" title="Put your annotation here"></textarea>
  Username: <input type="text" id="username"/>
  <input type="button" id="commitbutton" value="commit"/>
  <ul id="goingnotes"></ul>
</div>

<div class="pdfpagediv">
  <div class="dpdfpagediv">
    <img id="pdfpageid" src="<?php echo $imgsrc ?>">
  </div>
</div>


</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>PDF Cropper</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery.autoheight.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com//js/jquery.Jcrop.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <style type="text/css">
        .dpdfpagediv { border: thick red solid; width:800px }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #annottext { clear:both; width: 100%; height: 100px; overflow: auto}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var cropperapi; 
function setCrop(c)
{
    var dlk = c.x + " " + c.y + " " + c.x2 + " " + c.y2; 
    $('#consolidatelink').text(dlk); 
};


function appendannotation(lid, rectstring, txt)
{
    $('ul#goingnotes').append($('<li id="'+lid+'"><b>'+rectstring+'</b> <span>'+txt+'</span></li>')); 
    $('#annottext').val(""); 
    // apply the click link to it
    $('#'+lid + " b").click(function() 
    {
        var txt = $(this).next('span').text(); 
        $('#annottext').val(txt); 
        var rect = $(this).text().split(" "); 
        if (cropperapi)
            cropperapi.animateTo([parseInt(rect[0]), parseInt(rect[1]), parseInt(rect[2]), parseInt(rect[3])]);
    }); 
}

var trowid = 10; 
var pagebasereq = ""; 
function commit()
{
    // add the new text into our list
    var txt = $('#annottext').val(); 
    if (txt == "")
        return; 

    var username = $.trim($('#username').val()); 
    if (username == "")
        { alert("Please enter a username"); return }

    var lid = 'g'+trowid; 
    trowid++; 
    appendannotation(lid, $('#consolidatelink').text(), txt); 

    // send the value up to the server
    var values = [ ]; 
    values.push("user="+escape(username)); 
    var rect = $('#consolidatelink').text().split(" "); 
    values.push("x="+rect[0]+"&y="+rect[1]+"&x2="+rect[2]+"&y2="+rect[3]); 
    values.push("imgwidth=800&imgheight=1200"); 
    values.push("content="+escape(txt)); 
    //alert(pagebasereq+"&"+values.join("&")); 

    $.ajax({url:pagebasereq+"&"+values.join("&"), success: function(sdata)
    {
        var data = $.evalJSON(sdata);
        if (data["status"] != "Okay")
            alert(sdata); // would be better with rowid
    }}); 
}

$(document).ready(function() 
{ 
    pagebasereq = "http://scraperwikiviews.com/run/pdf-annotator-database/?pdfurl="+escape($("#pdfurl").attr("href"))+
                  "&pagenumber="+escape($("#pagenumber").text()); 

    $('#pdfpageid').load(function() 
    { 
        // consider boxWidth:800 of setting the real width so it handles its own scaling
        cropperapi = $.Jcrop('#pdfpageid', { onSelect: setCrop, onChange: setCrop, keySupport: false } ); 

        $.ajax({url:pagebasereq, success: function(sdata)
        {
            var data = $.evalJSON(sdata);
            for (var i=0; i < data.length; i++)
                appendannotation("u"+data[i].rowid, data[i].x+" "+data[i].y+" "+data[i].x2+" "+data[i].y2, data[i].content); 
        }}); 
        $("#commitbutton").click(commit); 
    }); 
});

    </script>
</head>
<body class="fullscreen">

<div>
<?php 
  parse_str(getenv("URLQUERY"), $output); 
  $pagenumber = intval(array_key_exists("pagenumber", $output) ? $output["pagenumber"] : "1"); 
  $pdfurl = (array_key_exists("pdfurl", $output) ? $output["pdfurl"] : "http://www.kytreasury.com/NR/rdonlyres/F5AF58E8-7F9E-4067-B31C-AE68EC9F1AE0/0/CaseyCounty.pdf"); 
  $imgsrc = "http://scraperwiki.com/cropper/png/u/page_$pagenumber?".http_build_query(array('url'=>$pdfurl)); 
?>
  <h2>Page <span id="pagenumber"><?php echo $pagenumber; ?></span> of 
    <a id="pdfurl" href="<?php echo $pdfurl; ?>"><?php echo $pdfurl; ?></a> 
  </h2>
  <p>
    <?php if ($pagenumber > 1) { ?>
      <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber-1)); ?>">prev page</a> 
    <?php } ?>
    <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber+1)); ?>">next page</a> 
    <a href="http://scraperwikiviews.com/run/pdf-annotator-database/">Main index</a>
    </p>
</div> 

<div id="annotate">
  Location rectangle <b id="consolidatelink">...</b>
  <textarea id="annottext" title="Put your annotation here"></textarea>
  Username: <input type="text" id="username"/>
  <input type="button" id="commitbutton" value="commit"/>
  <ul id="goingnotes"></ul>
</div>

<div class="pdfpagediv">
  <div class="dpdfpagediv">
    <img id="pdfpageid" src="<?php echo $imgsrc ?>">
  </div>
</div>


</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>PDF Cropper</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery.autoheight.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com//js/jquery.Jcrop.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <style type="text/css">
        .dpdfpagediv { border: thick red solid; width:800px }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #annottext { clear:both; width: 100%; height: 100px; overflow: auto}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var cropperapi; 
function setCrop(c)
{
    var dlk = c.x + " " + c.y + " " + c.x2 + " " + c.y2; 
    $('#consolidatelink').text(dlk); 
};


function appendannotation(lid, rectstring, txt)
{
    $('ul#goingnotes').append($('<li id="'+lid+'"><b>'+rectstring+'</b> <span>'+txt+'</span></li>')); 
    $('#annottext').val(""); 
    // apply the click link to it
    $('#'+lid + " b").click(function() 
    {
        var txt = $(this).next('span').text(); 
        $('#annottext').val(txt); 
        var rect = $(this).text().split(" "); 
        if (cropperapi)
            cropperapi.animateTo([parseInt(rect[0]), parseInt(rect[1]), parseInt(rect[2]), parseInt(rect[3])]);
    }); 
}

var trowid = 10; 
var pagebasereq = ""; 
function commit()
{
    // add the new text into our list
    var txt = $('#annottext').val(); 
    if (txt == "")
        return; 

    var username = $.trim($('#username').val()); 
    if (username == "")
        { alert("Please enter a username"); return }

    var lid = 'g'+trowid; 
    trowid++; 
    appendannotation(lid, $('#consolidatelink').text(), txt); 

    // send the value up to the server
    var values = [ ]; 
    values.push("user="+escape(username)); 
    var rect = $('#consolidatelink').text().split(" "); 
    values.push("x="+rect[0]+"&y="+rect[1]+"&x2="+rect[2]+"&y2="+rect[3]); 
    values.push("imgwidth=800&imgheight=1200"); 
    values.push("content="+escape(txt)); 
    //alert(pagebasereq+"&"+values.join("&")); 

    $.ajax({url:pagebasereq+"&"+values.join("&"), success: function(sdata)
    {
        var data = $.evalJSON(sdata);
        if (data["status"] != "Okay")
            alert(sdata); // would be better with rowid
    }}); 
}

$(document).ready(function() 
{ 
    pagebasereq = "http://scraperwikiviews.com/run/pdf-annotator-database/?pdfurl="+escape($("#pdfurl").attr("href"))+
                  "&pagenumber="+escape($("#pagenumber").text()); 

    $('#pdfpageid').load(function() 
    { 
        // consider boxWidth:800 of setting the real width so it handles its own scaling
        cropperapi = $.Jcrop('#pdfpageid', { onSelect: setCrop, onChange: setCrop, keySupport: false } ); 

        $.ajax({url:pagebasereq, success: function(sdata)
        {
            var data = $.evalJSON(sdata);
            for (var i=0; i < data.length; i++)
                appendannotation("u"+data[i].rowid, data[i].x+" "+data[i].y+" "+data[i].x2+" "+data[i].y2, data[i].content); 
        }}); 
        $("#commitbutton").click(commit); 
    }); 
});

    </script>
</head>
<body class="fullscreen">

<div>
<?php 
  parse_str(getenv("URLQUERY"), $output); 
  $pagenumber = intval(array_key_exists("pagenumber", $output) ? $output["pagenumber"] : "1"); 
  $pdfurl = (array_key_exists("pdfurl", $output) ? $output["pdfurl"] : "http://www.kytreasury.com/NR/rdonlyres/F5AF58E8-7F9E-4067-B31C-AE68EC9F1AE0/0/CaseyCounty.pdf"); 
  $imgsrc = "http://scraperwiki.com/cropper/png/u/page_$pagenumber?".http_build_query(array('url'=>$pdfurl)); 
?>
  <h2>Page <span id="pagenumber"><?php echo $pagenumber; ?></span> of 
    <a id="pdfurl" href="<?php echo $pdfurl; ?>"><?php echo $pdfurl; ?></a> 
  </h2>
  <p>
    <?php if ($pagenumber > 1) { ?>
      <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber-1)); ?>">prev page</a> 
    <?php } ?>
    <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber+1)); ?>">next page</a> 
    <a href="http://scraperwikiviews.com/run/pdf-annotator-database/">Main index</a>
    </p>
</div> 

<div id="annotate">
  Location rectangle <b id="consolidatelink">...</b>
  <textarea id="annottext" title="Put your annotation here"></textarea>
  Username: <input type="text" id="username"/>
  <input type="button" id="commitbutton" value="commit"/>
  <ul id="goingnotes"></ul>
</div>

<div class="pdfpagediv">
  <div class="dpdfpagediv">
    <img id="pdfpageid" src="<?php echo $imgsrc ?>">
  </div>
</div>


</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>PDF Cropper</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery.autoheight.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com//js/jquery.Jcrop.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <style type="text/css">
        .dpdfpagediv { border: thick red solid; width:800px }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #annottext { clear:both; width: 100%; height: 100px; overflow: auto}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var cropperapi; 
function setCrop(c)
{
    var dlk = c.x + " " + c.y + " " + c.x2 + " " + c.y2; 
    $('#consolidatelink').text(dlk); 
};


function appendannotation(lid, rectstring, txt)
{
    $('ul#goingnotes').append($('<li id="'+lid+'"><b>'+rectstring+'</b> <span>'+txt+'</span></li>')); 
    $('#annottext').val(""); 
    // apply the click link to it
    $('#'+lid + " b").click(function() 
    {
        var txt = $(this).next('span').text(); 
        $('#annottext').val(txt); 
        var rect = $(this).text().split(" "); 
        if (cropperapi)
            cropperapi.animateTo([parseInt(rect[0]), parseInt(rect[1]), parseInt(rect[2]), parseInt(rect[3])]);
    }); 
}

var trowid = 10; 
var pagebasereq = ""; 
function commit()
{
    // add the new text into our list
    var txt = $('#annottext').val(); 
    if (txt == "")
        return; 

    var username = $.trim($('#username').val()); 
    if (username == "")
        { alert("Please enter a username"); return }

    var lid = 'g'+trowid; 
    trowid++; 
    appendannotation(lid, $('#consolidatelink').text(), txt); 

    // send the value up to the server
    var values = [ ]; 
    values.push("user="+escape(username)); 
    var rect = $('#consolidatelink').text().split(" "); 
    values.push("x="+rect[0]+"&y="+rect[1]+"&x2="+rect[2]+"&y2="+rect[3]); 
    values.push("imgwidth=800&imgheight=1200"); 
    values.push("content="+escape(txt)); 
    //alert(pagebasereq+"&"+values.join("&")); 

    $.ajax({url:pagebasereq+"&"+values.join("&"), success: function(sdata)
    {
        var data = $.evalJSON(sdata);
        if (data["status"] != "Okay")
            alert(sdata); // would be better with rowid
    }}); 
}

$(document).ready(function() 
{ 
    pagebasereq = "http://scraperwikiviews.com/run/pdf-annotator-database/?pdfurl="+escape($("#pdfurl").attr("href"))+
                  "&pagenumber="+escape($("#pagenumber").text()); 

    $('#pdfpageid').load(function() 
    { 
        // consider boxWidth:800 of setting the real width so it handles its own scaling
        cropperapi = $.Jcrop('#pdfpageid', { onSelect: setCrop, onChange: setCrop, keySupport: false } ); 

        $.ajax({url:pagebasereq, success: function(sdata)
        {
            var data = $.evalJSON(sdata);
            for (var i=0; i < data.length; i++)
                appendannotation("u"+data[i].rowid, data[i].x+" "+data[i].y+" "+data[i].x2+" "+data[i].y2, data[i].content); 
        }}); 
        $("#commitbutton").click(commit); 
    }); 
});

    </script>
</head>
<body class="fullscreen">

<div>
<?php 
  parse_str(getenv("URLQUERY"), $output); 
  $pagenumber = intval(array_key_exists("pagenumber", $output) ? $output["pagenumber"] : "1"); 
  $pdfurl = (array_key_exists("pdfurl", $output) ? $output["pdfurl"] : "http://www.kytreasury.com/NR/rdonlyres/F5AF58E8-7F9E-4067-B31C-AE68EC9F1AE0/0/CaseyCounty.pdf"); 
  $imgsrc = "http://scraperwiki.com/cropper/png/u/page_$pagenumber?".http_build_query(array('url'=>$pdfurl)); 
?>
  <h2>Page <span id="pagenumber"><?php echo $pagenumber; ?></span> of 
    <a id="pdfurl" href="<?php echo $pdfurl; ?>"><?php echo $pdfurl; ?></a> 
  </h2>
  <p>
    <?php if ($pagenumber > 1) { ?>
      <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber-1)); ?>">prev page</a> 
    <?php } ?>
    <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber+1)); ?>">next page</a> 
    <a href="http://scraperwikiviews.com/run/pdf-annotator-database/">Main index</a>
    </p>
</div> 

<div id="annotate">
  Location rectangle <b id="consolidatelink">...</b>
  <textarea id="annottext" title="Put your annotation here"></textarea>
  Username: <input type="text" id="username"/>
  <input type="button" id="commitbutton" value="commit"/>
  <ul id="goingnotes"></ul>
</div>

<div class="pdfpagediv">
  <div class="dpdfpagediv">
    <img id="pdfpageid" src="<?php echo $imgsrc ?>">
  </div>
</div>


</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>PDF Cropper</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery.autoheight.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com//js/jquery.Jcrop.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <style type="text/css">
        .dpdfpagediv { border: thick red solid; width:800px }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #annottext { clear:both; width: 100%; height: 100px; overflow: auto}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var cropperapi; 
function setCrop(c)
{
    var dlk = c.x + " " + c.y + " " + c.x2 + " " + c.y2; 
    $('#consolidatelink').text(dlk); 
};


function appendannotation(lid, rectstring, txt)
{
    $('ul#goingnotes').append($('<li id="'+lid+'"><b>'+rectstring+'</b> <span>'+txt+'</span></li>')); 
    $('#annottext').val(""); 
    // apply the click link to it
    $('#'+lid + " b").click(function() 
    {
        var txt = $(this).next('span').text(); 
        $('#annottext').val(txt); 
        var rect = $(this).text().split(" "); 
        if (cropperapi)
            cropperapi.animateTo([parseInt(rect[0]), parseInt(rect[1]), parseInt(rect[2]), parseInt(rect[3])]);
    }); 
}

var trowid = 10; 
var pagebasereq = ""; 
function commit()
{
    // add the new text into our list
    var txt = $('#annottext').val(); 
    if (txt == "")
        return; 

    var username = $.trim($('#username').val()); 
    if (username == "")
        { alert("Please enter a username"); return }

    var lid = 'g'+trowid; 
    trowid++; 
    appendannotation(lid, $('#consolidatelink').text(), txt); 

    // send the value up to the server
    var values = [ ]; 
    values.push("user="+escape(username)); 
    var rect = $('#consolidatelink').text().split(" "); 
    values.push("x="+rect[0]+"&y="+rect[1]+"&x2="+rect[2]+"&y2="+rect[3]); 
    values.push("imgwidth=800&imgheight=1200"); 
    values.push("content="+escape(txt)); 
    //alert(pagebasereq+"&"+values.join("&")); 

    $.ajax({url:pagebasereq+"&"+values.join("&"), success: function(sdata)
    {
        var data = $.evalJSON(sdata);
        if (data["status"] != "Okay")
            alert(sdata); // would be better with rowid
    }}); 
}

$(document).ready(function() 
{ 
    pagebasereq = "http://scraperwikiviews.com/run/pdf-annotator-database/?pdfurl="+escape($("#pdfurl").attr("href"))+
                  "&pagenumber="+escape($("#pagenumber").text()); 

    $('#pdfpageid').load(function() 
    { 
        // consider boxWidth:800 of setting the real width so it handles its own scaling
        cropperapi = $.Jcrop('#pdfpageid', { onSelect: setCrop, onChange: setCrop, keySupport: false } ); 

        $.ajax({url:pagebasereq, success: function(sdata)
        {
            var data = $.evalJSON(sdata);
            for (var i=0; i < data.length; i++)
                appendannotation("u"+data[i].rowid, data[i].x+" "+data[i].y+" "+data[i].x2+" "+data[i].y2, data[i].content); 
        }}); 
        $("#commitbutton").click(commit); 
    }); 
});

    </script>
</head>
<body class="fullscreen">

<div>
<?php 
  parse_str(getenv("URLQUERY"), $output); 
  $pagenumber = intval(array_key_exists("pagenumber", $output) ? $output["pagenumber"] : "1"); 
  $pdfurl = (array_key_exists("pdfurl", $output) ? $output["pdfurl"] : "http://www.kytreasury.com/NR/rdonlyres/F5AF58E8-7F9E-4067-B31C-AE68EC9F1AE0/0/CaseyCounty.pdf"); 
  $imgsrc = "http://scraperwiki.com/cropper/png/u/page_$pagenumber?".http_build_query(array('url'=>$pdfurl)); 
?>
  <h2>Page <span id="pagenumber"><?php echo $pagenumber; ?></span> of 
    <a id="pdfurl" href="<?php echo $pdfurl; ?>"><?php echo $pdfurl; ?></a> 
  </h2>
  <p>
    <?php if ($pagenumber > 1) { ?>
      <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber-1)); ?>">prev page</a> 
    <?php } ?>
    <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber+1)); ?>">next page</a> 
    <a href="http://scraperwikiviews.com/run/pdf-annotator-database/">Main index</a>
    </p>
</div> 

<div id="annotate">
  Location rectangle <b id="consolidatelink">...</b>
  <textarea id="annottext" title="Put your annotation here"></textarea>
  Username: <input type="text" id="username"/>
  <input type="button" id="commitbutton" value="commit"/>
  <ul id="goingnotes"></ul>
</div>

<div class="pdfpagediv">
  <div class="dpdfpagediv">
    <img id="pdfpageid" src="<?php echo $imgsrc ?>">
  </div>
</div>


</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>PDF Cropper</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery.autoheight.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com//js/jquery.Jcrop.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <style type="text/css">
        .dpdfpagediv { border: thick red solid; width:800px }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #annottext { clear:both; width: 100%; height: 100px; overflow: auto}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var cropperapi; 
function setCrop(c)
{
    var dlk = c.x + " " + c.y + " " + c.x2 + " " + c.y2; 
    $('#consolidatelink').text(dlk); 
};


function appendannotation(lid, rectstring, txt)
{
    $('ul#goingnotes').append($('<li id="'+lid+'"><b>'+rectstring+'</b> <span>'+txt+'</span></li>')); 
    $('#annottext').val(""); 
    // apply the click link to it
    $('#'+lid + " b").click(function() 
    {
        var txt = $(this).next('span').text(); 
        $('#annottext').val(txt); 
        var rect = $(this).text().split(" "); 
        if (cropperapi)
            cropperapi.animateTo([parseInt(rect[0]), parseInt(rect[1]), parseInt(rect[2]), parseInt(rect[3])]);
    }); 
}

var trowid = 10; 
var pagebasereq = ""; 
function commit()
{
    // add the new text into our list
    var txt = $('#annottext').val(); 
    if (txt == "")
        return; 

    var username = $.trim($('#username').val()); 
    if (username == "")
        { alert("Please enter a username"); return }

    var lid = 'g'+trowid; 
    trowid++; 
    appendannotation(lid, $('#consolidatelink').text(), txt); 

    // send the value up to the server
    var values = [ ]; 
    values.push("user="+escape(username)); 
    var rect = $('#consolidatelink').text().split(" "); 
    values.push("x="+rect[0]+"&y="+rect[1]+"&x2="+rect[2]+"&y2="+rect[3]); 
    values.push("imgwidth=800&imgheight=1200"); 
    values.push("content="+escape(txt)); 
    //alert(pagebasereq+"&"+values.join("&")); 

    $.ajax({url:pagebasereq+"&"+values.join("&"), success: function(sdata)
    {
        var data = $.evalJSON(sdata);
        if (data["status"] != "Okay")
            alert(sdata); // would be better with rowid
    }}); 
}

$(document).ready(function() 
{ 
    pagebasereq = "http://scraperwikiviews.com/run/pdf-annotator-database/?pdfurl="+escape($("#pdfurl").attr("href"))+
                  "&pagenumber="+escape($("#pagenumber").text()); 

    $('#pdfpageid').load(function() 
    { 
        // consider boxWidth:800 of setting the real width so it handles its own scaling
        cropperapi = $.Jcrop('#pdfpageid', { onSelect: setCrop, onChange: setCrop, keySupport: false } ); 

        $.ajax({url:pagebasereq, success: function(sdata)
        {
            var data = $.evalJSON(sdata);
            for (var i=0; i < data.length; i++)
                appendannotation("u"+data[i].rowid, data[i].x+" "+data[i].y+" "+data[i].x2+" "+data[i].y2, data[i].content); 
        }}); 
        $("#commitbutton").click(commit); 
    }); 
});

    </script>
</head>
<body class="fullscreen">

<div>
<?php 
  parse_str(getenv("URLQUERY"), $output); 
  $pagenumber = intval(array_key_exists("pagenumber", $output) ? $output["pagenumber"] : "1"); 
  $pdfurl = (array_key_exists("pdfurl", $output) ? $output["pdfurl"] : "http://www.kytreasury.com/NR/rdonlyres/F5AF58E8-7F9E-4067-B31C-AE68EC9F1AE0/0/CaseyCounty.pdf"); 
  $imgsrc = "http://scraperwiki.com/cropper/png/u/page_$pagenumber?".http_build_query(array('url'=>$pdfurl)); 
?>
  <h2>Page <span id="pagenumber"><?php echo $pagenumber; ?></span> of 
    <a id="pdfurl" href="<?php echo $pdfurl; ?>"><?php echo $pdfurl; ?></a> 
  </h2>
  <p>
    <?php if ($pagenumber > 1) { ?>
      <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber-1)); ?>">prev page</a> 
    <?php } ?>
    <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber+1)); ?>">next page</a> 
    <a href="http://scraperwikiviews.com/run/pdf-annotator-database/">Main index</a>
    </p>
</div> 

<div id="annotate">
  Location rectangle <b id="consolidatelink">...</b>
  <textarea id="annottext" title="Put your annotation here"></textarea>
  Username: <input type="text" id="username"/>
  <input type="button" id="commitbutton" value="commit"/>
  <ul id="goingnotes"></ul>
</div>

<div class="pdfpagediv">
  <div class="dpdfpagediv">
    <img id="pdfpageid" src="<?php echo $imgsrc ?>">
  </div>
</div>


</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>PDF Cropper</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery.autoheight.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com//js/jquery.Jcrop.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <style type="text/css">
        .dpdfpagediv { border: thick red solid; width:800px }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #annottext { clear:both; width: 100%; height: 100px; overflow: auto}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var cropperapi; 
function setCrop(c)
{
    var dlk = c.x + " " + c.y + " " + c.x2 + " " + c.y2; 
    $('#consolidatelink').text(dlk); 
};


function appendannotation(lid, rectstring, txt)
{
    $('ul#goingnotes').append($('<li id="'+lid+'"><b>'+rectstring+'</b> <span>'+txt+'</span></li>')); 
    $('#annottext').val(""); 
    // apply the click link to it
    $('#'+lid + " b").click(function() 
    {
        var txt = $(this).next('span').text(); 
        $('#annottext').val(txt); 
        var rect = $(this).text().split(" "); 
        if (cropperapi)
            cropperapi.animateTo([parseInt(rect[0]), parseInt(rect[1]), parseInt(rect[2]), parseInt(rect[3])]);
    }); 
}

var trowid = 10; 
var pagebasereq = ""; 
function commit()
{
    // add the new text into our list
    var txt = $('#annottext').val(); 
    if (txt == "")
        return; 

    var username = $.trim($('#username').val()); 
    if (username == "")
        { alert("Please enter a username"); return }

    var lid = 'g'+trowid; 
    trowid++; 
    appendannotation(lid, $('#consolidatelink').text(), txt); 

    // send the value up to the server
    var values = [ ]; 
    values.push("user="+escape(username)); 
    var rect = $('#consolidatelink').text().split(" "); 
    values.push("x="+rect[0]+"&y="+rect[1]+"&x2="+rect[2]+"&y2="+rect[3]); 
    values.push("imgwidth=800&imgheight=1200"); 
    values.push("content="+escape(txt)); 
    //alert(pagebasereq+"&"+values.join("&")); 

    $.ajax({url:pagebasereq+"&"+values.join("&"), success: function(sdata)
    {
        var data = $.evalJSON(sdata);
        if (data["status"] != "Okay")
            alert(sdata); // would be better with rowid
    }}); 
}

$(document).ready(function() 
{ 
    pagebasereq = "http://scraperwikiviews.com/run/pdf-annotator-database/?pdfurl="+escape($("#pdfurl").attr("href"))+
                  "&pagenumber="+escape($("#pagenumber").text()); 

    $('#pdfpageid').load(function() 
    { 
        // consider boxWidth:800 of setting the real width so it handles its own scaling
        cropperapi = $.Jcrop('#pdfpageid', { onSelect: setCrop, onChange: setCrop, keySupport: false } ); 

        $.ajax({url:pagebasereq, success: function(sdata)
        {
            var data = $.evalJSON(sdata);
            for (var i=0; i < data.length; i++)
                appendannotation("u"+data[i].rowid, data[i].x+" "+data[i].y+" "+data[i].x2+" "+data[i].y2, data[i].content); 
        }}); 
        $("#commitbutton").click(commit); 
    }); 
});

    </script>
</head>
<body class="fullscreen">

<div>
<?php 
  parse_str(getenv("URLQUERY"), $output); 
  $pagenumber = intval(array_key_exists("pagenumber", $output) ? $output["pagenumber"] : "1"); 
  $pdfurl = (array_key_exists("pdfurl", $output) ? $output["pdfurl"] : "http://www.kytreasury.com/NR/rdonlyres/F5AF58E8-7F9E-4067-B31C-AE68EC9F1AE0/0/CaseyCounty.pdf"); 
  $imgsrc = "http://scraperwiki.com/cropper/png/u/page_$pagenumber?".http_build_query(array('url'=>$pdfurl)); 
?>
  <h2>Page <span id="pagenumber"><?php echo $pagenumber; ?></span> of 
    <a id="pdfurl" href="<?php echo $pdfurl; ?>"><?php echo $pdfurl; ?></a> 
  </h2>
  <p>
    <?php if ($pagenumber > 1) { ?>
      <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber-1)); ?>">prev page</a> 
    <?php } ?>
    <a href="?<?php echo http_build_query(array('pdfurl'=>$pdfurl, 'pagenumber'=>$pagenumber+1)); ?>">next page</a> 
    <a href="http://scraperwikiviews.com/run/pdf-annotator-database/">Main index</a>
    </p>
</div> 

<div id="annotate">
  Location rectangle <b id="consolidatelink">...</b>
  <textarea id="annottext" title="Put your annotation here"></textarea>
  Username: <input type="text" id="username"/>
  <input type="button" id="commitbutton" value="commit"/>
  <ul id="goingnotes"></ul>
</div>

<div class="pdfpagediv">
  <div class="dpdfpagediv">
    <img id="pdfpageid" src="<?php echo $imgsrc ?>">
  </div>
</div>


</body>
</html>
