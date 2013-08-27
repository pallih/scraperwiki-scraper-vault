<html>
<head>
    <script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
    <script src="https://media.scraperwiki.com/js/jquery-1.5.2.js"></script>
    <script src="https://media.scraperwiki.com/js/json-min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
</head>

<body>
  <!--[if IE]>
    <script type="text/javascript" 
     src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>

    <style>
     .chromeFrameInstallDefaultStyle {
       width: 100%; /* default is 800px */
       border: 5px solid blue;
     }
    </style>

    <div id="prompt">
     <!-- if IE without GCF, prompt goes here -->
    </div>
 
    <script>
     // The conditional ensures that this code will only execute in IE,
     // Therefore we can use the IE-specific attachEvent without worry
/*     window.attachEvent("onload", function() {
       CFInstall.check({
         mode: "overlay", // the default
         node: "prompt"
       });
     }); */
    </script>
  <!--[endif]-->

    <h4>View of launched objects</h4>
    <p>Blobs for numbers of satellites using <a href="http://raphaeljs.com/">Raphaeljs technology</a>.
    Data is <a href="https://scraperwiki.com/scrapers/outer_space_objects_parsecollector/">here</a>.
    <input type="button" id="bgo" value="Go"/>
    With some real elbow grease, may be possible to ape <a href="http://energy.publicdata.eu/ee/">this visualization</a>.
    The clue is in line 1146 of <a href="https://bitbucket.org/okfn/openenergy/src/c586fa14ab48/src/OpenEnergyVis.as">this code</a>
    showing damping and recalculation figures (favouring x motions and giving bigger velocities to large circles)
    </p>

<div id="rstuff" style="width:100%; height:100%;background:#f8f8f8;border:thin red solid; overflow:none"></div>

<script>
var paper; 
var circs = [ ]; 
var papercx = 350; 
var papercy = 200; 
var pixmove = 40; 
var pixpersec = 30; 
var txt; 
var font = '100 30px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 

var count = 0; 
function gofunc()
{
    force(); 
    count++; 
    if (count < 300)
        setTimeout(gofunc, 30); 
}

var start = function () 
{
    this.txt = paper.text(this.attr("cx"), this.attr("cy"), this.country).attr({"font":font, "text-anchor":"middle", "fill":"black"});
    this.ox = this.attr("cx");
    this.oy = this.attr("cy");
    this.attr({opacity: 0.5});
}
var move = function (dx, dy) 
{
    this.attr({cx: this.ox + dx, cy: this.oy + dy});
}
var up = function () 
{
    this.txt.remove(); 
    this.attr({opacity: 1});
}

function circ(i, row)
{
    result = { rad: Math.sqrt(row[1])*3 }
    var c = paper.circle(300-i*20, i*10+20, result["rad"]).attr({fill:"#9f9"}); 
    c.country = row[0]; 
    c.drag(move, start, up);
    result["c"] = c; 
    return result
}

function force()
{
    for (var i = 0; i < circs.length; i++)
    {
        circs[i].sx = 0.0; 
        circs[i].sy = 0.0; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        for (var j = i+1; j < circs.length; j++)
        {
            var dx = cx - circs[j].c.attr("cx"); 
            var dy = cy - circs[j].c.attr("cy"); 
            var dleng = Math.sqrt(dx*dx+dy*dy); 
            var sumrad = circs[j]["rad"] + circs[i]["rad"]+5; 
            if ((dleng != 0.0) && (sumrad - dleng>0))
            {
                var fac = (sumrad - dleng)/dleng; 
                if (fac > 0.0)
                    fac *= 1; //(sumrad - dleng); 
                else
                    fac *= 0; //-(sumrad - dleng) / 8; 
                circs[i].sx += dx*fac; 
                circs[i].sy += dy*fac; 
                circs[j].sx -= dx*fac; 
                circs[j].sy -= dy*fac; 
            }
        } 
        circs[i].sx += (papercx - cx)/4; 
        circs[i].sy += (papercy - cy)/4; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        var fac = 0.1; 
        circs[i]["c"].attr({"cx":cx+circs[i].sx*fac, "cy":cy+circs[i].sy*fac});
    }
}

$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    $.ajax({url:"https://views.scraperwiki.com/run/outer-space-objects-view/?json", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < Math.min(data.length, 40); i++) 
        { 
            circs.push(circ(i, data[i])); 
              
//            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
/*            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
            }; */
        }
    }})

    $("#bgo").click(function() { count=0; gofunc(); }); 
})

</script>

</body>
</html>
<html>
<head>
    <script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
    <script src="https://media.scraperwiki.com/js/jquery-1.5.2.js"></script>
    <script src="https://media.scraperwiki.com/js/json-min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
</head>

<body>
  <!--[if IE]>
    <script type="text/javascript" 
     src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>

    <style>
     .chromeFrameInstallDefaultStyle {
       width: 100%; /* default is 800px */
       border: 5px solid blue;
     }
    </style>

    <div id="prompt">
     <!-- if IE without GCF, prompt goes here -->
    </div>
 
    <script>
     // The conditional ensures that this code will only execute in IE,
     // Therefore we can use the IE-specific attachEvent without worry
/*     window.attachEvent("onload", function() {
       CFInstall.check({
         mode: "overlay", // the default
         node: "prompt"
       });
     }); */
    </script>
  <!--[endif]-->

    <h4>View of launched objects</h4>
    <p>Blobs for numbers of satellites using <a href="http://raphaeljs.com/">Raphaeljs technology</a>.
    Data is <a href="https://scraperwiki.com/scrapers/outer_space_objects_parsecollector/">here</a>.
    <input type="button" id="bgo" value="Go"/>
    With some real elbow grease, may be possible to ape <a href="http://energy.publicdata.eu/ee/">this visualization</a>.
    The clue is in line 1146 of <a href="https://bitbucket.org/okfn/openenergy/src/c586fa14ab48/src/OpenEnergyVis.as">this code</a>
    showing damping and recalculation figures (favouring x motions and giving bigger velocities to large circles)
    </p>

<div id="rstuff" style="width:100%; height:100%;background:#f8f8f8;border:thin red solid; overflow:none"></div>

<script>
var paper; 
var circs = [ ]; 
var papercx = 350; 
var papercy = 200; 
var pixmove = 40; 
var pixpersec = 30; 
var txt; 
var font = '100 30px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 

var count = 0; 
function gofunc()
{
    force(); 
    count++; 
    if (count < 300)
        setTimeout(gofunc, 30); 
}

var start = function () 
{
    this.txt = paper.text(this.attr("cx"), this.attr("cy"), this.country).attr({"font":font, "text-anchor":"middle", "fill":"black"});
    this.ox = this.attr("cx");
    this.oy = this.attr("cy");
    this.attr({opacity: 0.5});
}
var move = function (dx, dy) 
{
    this.attr({cx: this.ox + dx, cy: this.oy + dy});
}
var up = function () 
{
    this.txt.remove(); 
    this.attr({opacity: 1});
}

function circ(i, row)
{
    result = { rad: Math.sqrt(row[1])*3 }
    var c = paper.circle(300-i*20, i*10+20, result["rad"]).attr({fill:"#9f9"}); 
    c.country = row[0]; 
    c.drag(move, start, up);
    result["c"] = c; 
    return result
}

function force()
{
    for (var i = 0; i < circs.length; i++)
    {
        circs[i].sx = 0.0; 
        circs[i].sy = 0.0; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        for (var j = i+1; j < circs.length; j++)
        {
            var dx = cx - circs[j].c.attr("cx"); 
            var dy = cy - circs[j].c.attr("cy"); 
            var dleng = Math.sqrt(dx*dx+dy*dy); 
            var sumrad = circs[j]["rad"] + circs[i]["rad"]+5; 
            if ((dleng != 0.0) && (sumrad - dleng>0))
            {
                var fac = (sumrad - dleng)/dleng; 
                if (fac > 0.0)
                    fac *= 1; //(sumrad - dleng); 
                else
                    fac *= 0; //-(sumrad - dleng) / 8; 
                circs[i].sx += dx*fac; 
                circs[i].sy += dy*fac; 
                circs[j].sx -= dx*fac; 
                circs[j].sy -= dy*fac; 
            }
        } 
        circs[i].sx += (papercx - cx)/4; 
        circs[i].sy += (papercy - cy)/4; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        var fac = 0.1; 
        circs[i]["c"].attr({"cx":cx+circs[i].sx*fac, "cy":cy+circs[i].sy*fac});
    }
}

$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    $.ajax({url:"https://views.scraperwiki.com/run/outer-space-objects-view/?json", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < Math.min(data.length, 40); i++) 
        { 
            circs.push(circ(i, data[i])); 
              
//            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
/*            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
            }; */
        }
    }})

    $("#bgo").click(function() { count=0; gofunc(); }); 
})

</script>

</body>
</html>
<html>
<head>
    <script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
    <script src="https://media.scraperwiki.com/js/jquery-1.5.2.js"></script>
    <script src="https://media.scraperwiki.com/js/json-min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
</head>

<body>
  <!--[if IE]>
    <script type="text/javascript" 
     src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>

    <style>
     .chromeFrameInstallDefaultStyle {
       width: 100%; /* default is 800px */
       border: 5px solid blue;
     }
    </style>

    <div id="prompt">
     <!-- if IE without GCF, prompt goes here -->
    </div>
 
    <script>
     // The conditional ensures that this code will only execute in IE,
     // Therefore we can use the IE-specific attachEvent without worry
/*     window.attachEvent("onload", function() {
       CFInstall.check({
         mode: "overlay", // the default
         node: "prompt"
       });
     }); */
    </script>
  <!--[endif]-->

    <h4>View of launched objects</h4>
    <p>Blobs for numbers of satellites using <a href="http://raphaeljs.com/">Raphaeljs technology</a>.
    Data is <a href="https://scraperwiki.com/scrapers/outer_space_objects_parsecollector/">here</a>.
    <input type="button" id="bgo" value="Go"/>
    With some real elbow grease, may be possible to ape <a href="http://energy.publicdata.eu/ee/">this visualization</a>.
    The clue is in line 1146 of <a href="https://bitbucket.org/okfn/openenergy/src/c586fa14ab48/src/OpenEnergyVis.as">this code</a>
    showing damping and recalculation figures (favouring x motions and giving bigger velocities to large circles)
    </p>

<div id="rstuff" style="width:100%; height:100%;background:#f8f8f8;border:thin red solid; overflow:none"></div>

<script>
var paper; 
var circs = [ ]; 
var papercx = 350; 
var papercy = 200; 
var pixmove = 40; 
var pixpersec = 30; 
var txt; 
var font = '100 30px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 

var count = 0; 
function gofunc()
{
    force(); 
    count++; 
    if (count < 300)
        setTimeout(gofunc, 30); 
}

var start = function () 
{
    this.txt = paper.text(this.attr("cx"), this.attr("cy"), this.country).attr({"font":font, "text-anchor":"middle", "fill":"black"});
    this.ox = this.attr("cx");
    this.oy = this.attr("cy");
    this.attr({opacity: 0.5});
}
var move = function (dx, dy) 
{
    this.attr({cx: this.ox + dx, cy: this.oy + dy});
}
var up = function () 
{
    this.txt.remove(); 
    this.attr({opacity: 1});
}

function circ(i, row)
{
    result = { rad: Math.sqrt(row[1])*3 }
    var c = paper.circle(300-i*20, i*10+20, result["rad"]).attr({fill:"#9f9"}); 
    c.country = row[0]; 
    c.drag(move, start, up);
    result["c"] = c; 
    return result
}

function force()
{
    for (var i = 0; i < circs.length; i++)
    {
        circs[i].sx = 0.0; 
        circs[i].sy = 0.0; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        for (var j = i+1; j < circs.length; j++)
        {
            var dx = cx - circs[j].c.attr("cx"); 
            var dy = cy - circs[j].c.attr("cy"); 
            var dleng = Math.sqrt(dx*dx+dy*dy); 
            var sumrad = circs[j]["rad"] + circs[i]["rad"]+5; 
            if ((dleng != 0.0) && (sumrad - dleng>0))
            {
                var fac = (sumrad - dleng)/dleng; 
                if (fac > 0.0)
                    fac *= 1; //(sumrad - dleng); 
                else
                    fac *= 0; //-(sumrad - dleng) / 8; 
                circs[i].sx += dx*fac; 
                circs[i].sy += dy*fac; 
                circs[j].sx -= dx*fac; 
                circs[j].sy -= dy*fac; 
            }
        } 
        circs[i].sx += (papercx - cx)/4; 
        circs[i].sy += (papercy - cy)/4; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        var fac = 0.1; 
        circs[i]["c"].attr({"cx":cx+circs[i].sx*fac, "cy":cy+circs[i].sy*fac});
    }
}

$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    $.ajax({url:"https://views.scraperwiki.com/run/outer-space-objects-view/?json", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < Math.min(data.length, 40); i++) 
        { 
            circs.push(circ(i, data[i])); 
              
//            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
/*            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
            }; */
        }
    }})

    $("#bgo").click(function() { count=0; gofunc(); }); 
})

</script>

</body>
</html>
<html>
<head>
    <script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
    <script src="https://media.scraperwiki.com/js/jquery-1.5.2.js"></script>
    <script src="https://media.scraperwiki.com/js/json-min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
</head>

<body>
  <!--[if IE]>
    <script type="text/javascript" 
     src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>

    <style>
     .chromeFrameInstallDefaultStyle {
       width: 100%; /* default is 800px */
       border: 5px solid blue;
     }
    </style>

    <div id="prompt">
     <!-- if IE without GCF, prompt goes here -->
    </div>
 
    <script>
     // The conditional ensures that this code will only execute in IE,
     // Therefore we can use the IE-specific attachEvent without worry
/*     window.attachEvent("onload", function() {
       CFInstall.check({
         mode: "overlay", // the default
         node: "prompt"
       });
     }); */
    </script>
  <!--[endif]-->

    <h4>View of launched objects</h4>
    <p>Blobs for numbers of satellites using <a href="http://raphaeljs.com/">Raphaeljs technology</a>.
    Data is <a href="https://scraperwiki.com/scrapers/outer_space_objects_parsecollector/">here</a>.
    <input type="button" id="bgo" value="Go"/>
    With some real elbow grease, may be possible to ape <a href="http://energy.publicdata.eu/ee/">this visualization</a>.
    The clue is in line 1146 of <a href="https://bitbucket.org/okfn/openenergy/src/c586fa14ab48/src/OpenEnergyVis.as">this code</a>
    showing damping and recalculation figures (favouring x motions and giving bigger velocities to large circles)
    </p>

<div id="rstuff" style="width:100%; height:100%;background:#f8f8f8;border:thin red solid; overflow:none"></div>

<script>
var paper; 
var circs = [ ]; 
var papercx = 350; 
var papercy = 200; 
var pixmove = 40; 
var pixpersec = 30; 
var txt; 
var font = '100 30px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 

var count = 0; 
function gofunc()
{
    force(); 
    count++; 
    if (count < 300)
        setTimeout(gofunc, 30); 
}

var start = function () 
{
    this.txt = paper.text(this.attr("cx"), this.attr("cy"), this.country).attr({"font":font, "text-anchor":"middle", "fill":"black"});
    this.ox = this.attr("cx");
    this.oy = this.attr("cy");
    this.attr({opacity: 0.5});
}
var move = function (dx, dy) 
{
    this.attr({cx: this.ox + dx, cy: this.oy + dy});
}
var up = function () 
{
    this.txt.remove(); 
    this.attr({opacity: 1});
}

function circ(i, row)
{
    result = { rad: Math.sqrt(row[1])*3 }
    var c = paper.circle(300-i*20, i*10+20, result["rad"]).attr({fill:"#9f9"}); 
    c.country = row[0]; 
    c.drag(move, start, up);
    result["c"] = c; 
    return result
}

function force()
{
    for (var i = 0; i < circs.length; i++)
    {
        circs[i].sx = 0.0; 
        circs[i].sy = 0.0; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        for (var j = i+1; j < circs.length; j++)
        {
            var dx = cx - circs[j].c.attr("cx"); 
            var dy = cy - circs[j].c.attr("cy"); 
            var dleng = Math.sqrt(dx*dx+dy*dy); 
            var sumrad = circs[j]["rad"] + circs[i]["rad"]+5; 
            if ((dleng != 0.0) && (sumrad - dleng>0))
            {
                var fac = (sumrad - dleng)/dleng; 
                if (fac > 0.0)
                    fac *= 1; //(sumrad - dleng); 
                else
                    fac *= 0; //-(sumrad - dleng) / 8; 
                circs[i].sx += dx*fac; 
                circs[i].sy += dy*fac; 
                circs[j].sx -= dx*fac; 
                circs[j].sy -= dy*fac; 
            }
        } 
        circs[i].sx += (papercx - cx)/4; 
        circs[i].sy += (papercy - cy)/4; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        var fac = 0.1; 
        circs[i]["c"].attr({"cx":cx+circs[i].sx*fac, "cy":cy+circs[i].sy*fac});
    }
}

$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    $.ajax({url:"https://views.scraperwiki.com/run/outer-space-objects-view/?json", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < Math.min(data.length, 40); i++) 
        { 
            circs.push(circ(i, data[i])); 
              
//            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
/*            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
            }; */
        }
    }})

    $("#bgo").click(function() { count=0; gofunc(); }); 
})

</script>

</body>
</html>
<html>
<head>
    <script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
    <script src="https://media.scraperwiki.com/js/jquery-1.5.2.js"></script>
    <script src="https://media.scraperwiki.com/js/json-min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
</head>

<body>
  <!--[if IE]>
    <script type="text/javascript" 
     src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>

    <style>
     .chromeFrameInstallDefaultStyle {
       width: 100%; /* default is 800px */
       border: 5px solid blue;
     }
    </style>

    <div id="prompt">
     <!-- if IE without GCF, prompt goes here -->
    </div>
 
    <script>
     // The conditional ensures that this code will only execute in IE,
     // Therefore we can use the IE-specific attachEvent without worry
/*     window.attachEvent("onload", function() {
       CFInstall.check({
         mode: "overlay", // the default
         node: "prompt"
       });
     }); */
    </script>
  <!--[endif]-->

    <h4>View of launched objects</h4>
    <p>Blobs for numbers of satellites using <a href="http://raphaeljs.com/">Raphaeljs technology</a>.
    Data is <a href="https://scraperwiki.com/scrapers/outer_space_objects_parsecollector/">here</a>.
    <input type="button" id="bgo" value="Go"/>
    With some real elbow grease, may be possible to ape <a href="http://energy.publicdata.eu/ee/">this visualization</a>.
    The clue is in line 1146 of <a href="https://bitbucket.org/okfn/openenergy/src/c586fa14ab48/src/OpenEnergyVis.as">this code</a>
    showing damping and recalculation figures (favouring x motions and giving bigger velocities to large circles)
    </p>

<div id="rstuff" style="width:100%; height:100%;background:#f8f8f8;border:thin red solid; overflow:none"></div>

<script>
var paper; 
var circs = [ ]; 
var papercx = 350; 
var papercy = 200; 
var pixmove = 40; 
var pixpersec = 30; 
var txt; 
var font = '100 30px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 

var count = 0; 
function gofunc()
{
    force(); 
    count++; 
    if (count < 300)
        setTimeout(gofunc, 30); 
}

var start = function () 
{
    this.txt = paper.text(this.attr("cx"), this.attr("cy"), this.country).attr({"font":font, "text-anchor":"middle", "fill":"black"});
    this.ox = this.attr("cx");
    this.oy = this.attr("cy");
    this.attr({opacity: 0.5});
}
var move = function (dx, dy) 
{
    this.attr({cx: this.ox + dx, cy: this.oy + dy});
}
var up = function () 
{
    this.txt.remove(); 
    this.attr({opacity: 1});
}

function circ(i, row)
{
    result = { rad: Math.sqrt(row[1])*3 }
    var c = paper.circle(300-i*20, i*10+20, result["rad"]).attr({fill:"#9f9"}); 
    c.country = row[0]; 
    c.drag(move, start, up);
    result["c"] = c; 
    return result
}

function force()
{
    for (var i = 0; i < circs.length; i++)
    {
        circs[i].sx = 0.0; 
        circs[i].sy = 0.0; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        for (var j = i+1; j < circs.length; j++)
        {
            var dx = cx - circs[j].c.attr("cx"); 
            var dy = cy - circs[j].c.attr("cy"); 
            var dleng = Math.sqrt(dx*dx+dy*dy); 
            var sumrad = circs[j]["rad"] + circs[i]["rad"]+5; 
            if ((dleng != 0.0) && (sumrad - dleng>0))
            {
                var fac = (sumrad - dleng)/dleng; 
                if (fac > 0.0)
                    fac *= 1; //(sumrad - dleng); 
                else
                    fac *= 0; //-(sumrad - dleng) / 8; 
                circs[i].sx += dx*fac; 
                circs[i].sy += dy*fac; 
                circs[j].sx -= dx*fac; 
                circs[j].sy -= dy*fac; 
            }
        } 
        circs[i].sx += (papercx - cx)/4; 
        circs[i].sy += (papercy - cy)/4; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        var fac = 0.1; 
        circs[i]["c"].attr({"cx":cx+circs[i].sx*fac, "cy":cy+circs[i].sy*fac});
    }
}

$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    $.ajax({url:"https://views.scraperwiki.com/run/outer-space-objects-view/?json", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < Math.min(data.length, 40); i++) 
        { 
            circs.push(circ(i, data[i])); 
              
//            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
/*            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
            }; */
        }
    }})

    $("#bgo").click(function() { count=0; gofunc(); }); 
})

</script>

</body>
</html>
<html>
<head>
    <script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
    <script src="https://media.scraperwiki.com/js/jquery-1.5.2.js"></script>
    <script src="https://media.scraperwiki.com/js/json-min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
</head>

<body>
  <!--[if IE]>
    <script type="text/javascript" 
     src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>

    <style>
     .chromeFrameInstallDefaultStyle {
       width: 100%; /* default is 800px */
       border: 5px solid blue;
     }
    </style>

    <div id="prompt">
     <!-- if IE without GCF, prompt goes here -->
    </div>
 
    <script>
     // The conditional ensures that this code will only execute in IE,
     // Therefore we can use the IE-specific attachEvent without worry
/*     window.attachEvent("onload", function() {
       CFInstall.check({
         mode: "overlay", // the default
         node: "prompt"
       });
     }); */
    </script>
  <!--[endif]-->

    <h4>View of launched objects</h4>
    <p>Blobs for numbers of satellites using <a href="http://raphaeljs.com/">Raphaeljs technology</a>.
    Data is <a href="https://scraperwiki.com/scrapers/outer_space_objects_parsecollector/">here</a>.
    <input type="button" id="bgo" value="Go"/>
    With some real elbow grease, may be possible to ape <a href="http://energy.publicdata.eu/ee/">this visualization</a>.
    The clue is in line 1146 of <a href="https://bitbucket.org/okfn/openenergy/src/c586fa14ab48/src/OpenEnergyVis.as">this code</a>
    showing damping and recalculation figures (favouring x motions and giving bigger velocities to large circles)
    </p>

<div id="rstuff" style="width:100%; height:100%;background:#f8f8f8;border:thin red solid; overflow:none"></div>

<script>
var paper; 
var circs = [ ]; 
var papercx = 350; 
var papercy = 200; 
var pixmove = 40; 
var pixpersec = 30; 
var txt; 
var font = '100 30px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 

var count = 0; 
function gofunc()
{
    force(); 
    count++; 
    if (count < 300)
        setTimeout(gofunc, 30); 
}

var start = function () 
{
    this.txt = paper.text(this.attr("cx"), this.attr("cy"), this.country).attr({"font":font, "text-anchor":"middle", "fill":"black"});
    this.ox = this.attr("cx");
    this.oy = this.attr("cy");
    this.attr({opacity: 0.5});
}
var move = function (dx, dy) 
{
    this.attr({cx: this.ox + dx, cy: this.oy + dy});
}
var up = function () 
{
    this.txt.remove(); 
    this.attr({opacity: 1});
}

function circ(i, row)
{
    result = { rad: Math.sqrt(row[1])*3 }
    var c = paper.circle(300-i*20, i*10+20, result["rad"]).attr({fill:"#9f9"}); 
    c.country = row[0]; 
    c.drag(move, start, up);
    result["c"] = c; 
    return result
}

function force()
{
    for (var i = 0; i < circs.length; i++)
    {
        circs[i].sx = 0.0; 
        circs[i].sy = 0.0; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        for (var j = i+1; j < circs.length; j++)
        {
            var dx = cx - circs[j].c.attr("cx"); 
            var dy = cy - circs[j].c.attr("cy"); 
            var dleng = Math.sqrt(dx*dx+dy*dy); 
            var sumrad = circs[j]["rad"] + circs[i]["rad"]+5; 
            if ((dleng != 0.0) && (sumrad - dleng>0))
            {
                var fac = (sumrad - dleng)/dleng; 
                if (fac > 0.0)
                    fac *= 1; //(sumrad - dleng); 
                else
                    fac *= 0; //-(sumrad - dleng) / 8; 
                circs[i].sx += dx*fac; 
                circs[i].sy += dy*fac; 
                circs[j].sx -= dx*fac; 
                circs[j].sy -= dy*fac; 
            }
        } 
        circs[i].sx += (papercx - cx)/4; 
        circs[i].sy += (papercy - cy)/4; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        var fac = 0.1; 
        circs[i]["c"].attr({"cx":cx+circs[i].sx*fac, "cy":cy+circs[i].sy*fac});
    }
}

$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    $.ajax({url:"https://views.scraperwiki.com/run/outer-space-objects-view/?json", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < Math.min(data.length, 40); i++) 
        { 
            circs.push(circ(i, data[i])); 
              
//            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
/*            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
            }; */
        }
    }})

    $("#bgo").click(function() { count=0; gofunc(); }); 
})

</script>

</body>
</html>
<html>
<head>
    <script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
    <script src="https://media.scraperwiki.com/js/jquery-1.5.2.js"></script>
    <script src="https://media.scraperwiki.com/js/json-min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
</head>

<body>
  <!--[if IE]>
    <script type="text/javascript" 
     src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>

    <style>
     .chromeFrameInstallDefaultStyle {
       width: 100%; /* default is 800px */
       border: 5px solid blue;
     }
    </style>

    <div id="prompt">
     <!-- if IE without GCF, prompt goes here -->
    </div>
 
    <script>
     // The conditional ensures that this code will only execute in IE,
     // Therefore we can use the IE-specific attachEvent without worry
/*     window.attachEvent("onload", function() {
       CFInstall.check({
         mode: "overlay", // the default
         node: "prompt"
       });
     }); */
    </script>
  <!--[endif]-->

    <h4>View of launched objects</h4>
    <p>Blobs for numbers of satellites using <a href="http://raphaeljs.com/">Raphaeljs technology</a>.
    Data is <a href="https://scraperwiki.com/scrapers/outer_space_objects_parsecollector/">here</a>.
    <input type="button" id="bgo" value="Go"/>
    With some real elbow grease, may be possible to ape <a href="http://energy.publicdata.eu/ee/">this visualization</a>.
    The clue is in line 1146 of <a href="https://bitbucket.org/okfn/openenergy/src/c586fa14ab48/src/OpenEnergyVis.as">this code</a>
    showing damping and recalculation figures (favouring x motions and giving bigger velocities to large circles)
    </p>

<div id="rstuff" style="width:100%; height:100%;background:#f8f8f8;border:thin red solid; overflow:none"></div>

<script>
var paper; 
var circs = [ ]; 
var papercx = 350; 
var papercy = 200; 
var pixmove = 40; 
var pixpersec = 30; 
var txt; 
var font = '100 30px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 

var count = 0; 
function gofunc()
{
    force(); 
    count++; 
    if (count < 300)
        setTimeout(gofunc, 30); 
}

var start = function () 
{
    this.txt = paper.text(this.attr("cx"), this.attr("cy"), this.country).attr({"font":font, "text-anchor":"middle", "fill":"black"});
    this.ox = this.attr("cx");
    this.oy = this.attr("cy");
    this.attr({opacity: 0.5});
}
var move = function (dx, dy) 
{
    this.attr({cx: this.ox + dx, cy: this.oy + dy});
}
var up = function () 
{
    this.txt.remove(); 
    this.attr({opacity: 1});
}

function circ(i, row)
{
    result = { rad: Math.sqrt(row[1])*3 }
    var c = paper.circle(300-i*20, i*10+20, result["rad"]).attr({fill:"#9f9"}); 
    c.country = row[0]; 
    c.drag(move, start, up);
    result["c"] = c; 
    return result
}

function force()
{
    for (var i = 0; i < circs.length; i++)
    {
        circs[i].sx = 0.0; 
        circs[i].sy = 0.0; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        for (var j = i+1; j < circs.length; j++)
        {
            var dx = cx - circs[j].c.attr("cx"); 
            var dy = cy - circs[j].c.attr("cy"); 
            var dleng = Math.sqrt(dx*dx+dy*dy); 
            var sumrad = circs[j]["rad"] + circs[i]["rad"]+5; 
            if ((dleng != 0.0) && (sumrad - dleng>0))
            {
                var fac = (sumrad - dleng)/dleng; 
                if (fac > 0.0)
                    fac *= 1; //(sumrad - dleng); 
                else
                    fac *= 0; //-(sumrad - dleng) / 8; 
                circs[i].sx += dx*fac; 
                circs[i].sy += dy*fac; 
                circs[j].sx -= dx*fac; 
                circs[j].sy -= dy*fac; 
            }
        } 
        circs[i].sx += (papercx - cx)/4; 
        circs[i].sy += (papercy - cy)/4; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        var fac = 0.1; 
        circs[i]["c"].attr({"cx":cx+circs[i].sx*fac, "cy":cy+circs[i].sy*fac});
    }
}

$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    $.ajax({url:"https://views.scraperwiki.com/run/outer-space-objects-view/?json", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < Math.min(data.length, 40); i++) 
        { 
            circs.push(circ(i, data[i])); 
              
//            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
/*            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
            }; */
        }
    }})

    $("#bgo").click(function() { count=0; gofunc(); }); 
})

</script>

</body>
</html>
<html>
<head>
    <script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
    <script src="https://media.scraperwiki.com/js/jquery-1.5.2.js"></script>
    <script src="https://media.scraperwiki.com/js/json-min.js"></script>
    <meta http-equiv="X-UA-Compatible" content="chrome=1">
</head>

<body>
  <!--[if IE]>
    <script type="text/javascript" 
     src="http://ajax.googleapis.com/ajax/libs/chrome-frame/1/CFInstall.min.js"></script>

    <style>
     .chromeFrameInstallDefaultStyle {
       width: 100%; /* default is 800px */
       border: 5px solid blue;
     }
    </style>

    <div id="prompt">
     <!-- if IE without GCF, prompt goes here -->
    </div>
 
    <script>
     // The conditional ensures that this code will only execute in IE,
     // Therefore we can use the IE-specific attachEvent without worry
/*     window.attachEvent("onload", function() {
       CFInstall.check({
         mode: "overlay", // the default
         node: "prompt"
       });
     }); */
    </script>
  <!--[endif]-->

    <h4>View of launched objects</h4>
    <p>Blobs for numbers of satellites using <a href="http://raphaeljs.com/">Raphaeljs technology</a>.
    Data is <a href="https://scraperwiki.com/scrapers/outer_space_objects_parsecollector/">here</a>.
    <input type="button" id="bgo" value="Go"/>
    With some real elbow grease, may be possible to ape <a href="http://energy.publicdata.eu/ee/">this visualization</a>.
    The clue is in line 1146 of <a href="https://bitbucket.org/okfn/openenergy/src/c586fa14ab48/src/OpenEnergyVis.as">this code</a>
    showing damping and recalculation figures (favouring x motions and giving bigger velocities to large circles)
    </p>

<div id="rstuff" style="width:100%; height:100%;background:#f8f8f8;border:thin red solid; overflow:none"></div>

<script>
var paper; 
var circs = [ ]; 
var papercx = 350; 
var papercy = 200; 
var pixmove = 40; 
var pixpersec = 30; 
var txt; 
var font = '100 30px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 

var count = 0; 
function gofunc()
{
    force(); 
    count++; 
    if (count < 300)
        setTimeout(gofunc, 30); 
}

var start = function () 
{
    this.txt = paper.text(this.attr("cx"), this.attr("cy"), this.country).attr({"font":font, "text-anchor":"middle", "fill":"black"});
    this.ox = this.attr("cx");
    this.oy = this.attr("cy");
    this.attr({opacity: 0.5});
}
var move = function (dx, dy) 
{
    this.attr({cx: this.ox + dx, cy: this.oy + dy});
}
var up = function () 
{
    this.txt.remove(); 
    this.attr({opacity: 1});
}

function circ(i, row)
{
    result = { rad: Math.sqrt(row[1])*3 }
    var c = paper.circle(300-i*20, i*10+20, result["rad"]).attr({fill:"#9f9"}); 
    c.country = row[0]; 
    c.drag(move, start, up);
    result["c"] = c; 
    return result
}

function force()
{
    for (var i = 0; i < circs.length; i++)
    {
        circs[i].sx = 0.0; 
        circs[i].sy = 0.0; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        for (var j = i+1; j < circs.length; j++)
        {
            var dx = cx - circs[j].c.attr("cx"); 
            var dy = cy - circs[j].c.attr("cy"); 
            var dleng = Math.sqrt(dx*dx+dy*dy); 
            var sumrad = circs[j]["rad"] + circs[i]["rad"]+5; 
            if ((dleng != 0.0) && (sumrad - dleng>0))
            {
                var fac = (sumrad - dleng)/dleng; 
                if (fac > 0.0)
                    fac *= 1; //(sumrad - dleng); 
                else
                    fac *= 0; //-(sumrad - dleng) / 8; 
                circs[i].sx += dx*fac; 
                circs[i].sy += dy*fac; 
                circs[j].sx -= dx*fac; 
                circs[j].sy -= dy*fac; 
            }
        } 
        circs[i].sx += (papercx - cx)/4; 
        circs[i].sy += (papercy - cy)/4; 
    }

    for (var i = 0; i < circs.length; i++)
    {
        var cx = circs[i].c.attr("cx"); 
        var cy = circs[i].c.attr("cy"); 
        var fac = 0.1; 
        circs[i]["c"].attr({"cx":cx+circs[i].sx*fac, "cy":cy+circs[i].sy*fac});
    }
}

$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    $.ajax({url:"https://views.scraperwiki.com/run/outer-space-objects-view/?json", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < Math.min(data.length, 40); i++) 
        { 
            circs.push(circ(i, data[i])); 
              
//            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
/*            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
            }; */
        }
    }})

    $("#bgo").click(function() { count=0; gofunc(); }); 
})

</script>

</body>
</html>
