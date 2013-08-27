<html>
<head>
<script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="http://media.scraperwiki.com/js/json-min.js"></script>
<script>
var paper; 
$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    var st = paper.set();
    var sst = [ ]; 
    var rc = paper.rect(40, 4, 70, 50, 5).attr({"fill": "#049", scale:"0.6 0.6 50 50"});
    rc.drag(
    function(dx, dy)
    {
        this.attr({x: this.ox + dx, y: this.oy + dy});
        this.dx = dx; this.dy = dy; 
    },
    function () 
    {
        this.ox = this.attr("x");
        this.oy = this.attr("y");
        this.dx = 0; this.dy = 0; 
        this.attr({opacity: 0.5});
    },
    function() 
    {
        this.attr({opacity: 1});
        st.translate(this.dx, this.dy); 
        //for (var i = 0; i < sst.length; i++)
        //    sst[i].translate(this.dx*(1+i/5420.0), this.dy); 

    });

    var sss = 0.2; 
    var crc = paper.circle(20, 30, 10).attr("fill", "#094");
    crc.click(function(event) { sss*=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 
    var crc1 = paper.circle(20, 70, 10).attr("fill", "#904");
    crc1.click(function(event) { sss/=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 

    docave(paper, st, sst); 
})

var c1, c; 
function docave(paper, st, sst)
{
$.ajax({url:"http://scraperwikiviews.com/run//cave_svg_server_1/", success: function(sdata)
{
    var data = $.evalJSON(sdata);
    for (var i = 0; i < data["paths"].length; i+=1)
    {
        c1 = paper.path(data["paths"][i]["d"]); 
        st.push(c1); 
        //        var url = "http://knowledgeforge.net/sesame/club/mmmmc/rawscans/"+data[i].url; 
        //alert(url);        var c = paper.image(url, 10 + i*80, 10 + i*80, 500, 500);
        //console.log($.toJSON(data[i]));
        //break; if (i > 0)  break; 
    }

    var sketchframe = data["sketchframes"][2]; 
    var sca = 1.0/sketchframe["scaledown"]; 
    c = paper.image(sketchframe["sfsketch"], 0, 0, sketchframe["imagepixelswidth"], sketchframe["imagepixelsheight"]);
    c.scale(sca, sca, 0, 0); 
    c.rotate(-sketchframe["rotatedeg"], 0, 0); 
    c.translate(sketchframe["rxtrans"], sketchframe["rytrans"]); 
    st.push(c); 
}})
}

</script>
</head>
<body>
<h4>Early cave SVG viewer</h4>
<p>Still needs proper scaling and dragging of view window, within visibility, 
feedback to server of the area so it can partially download  only the polygons in the window, 
styling and colours, a backup bitmap when zoomed out.
<em>Note: Raphael rescales everything by parsing and multiplying it rather than using transforms.  This is no good</em>
    <div id="rstuff" style="width:800px; height:600px;background:#eee;border:thick blue solid; overflow:none"></div>
</body>
</html>


<html>
<head>
<script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="http://media.scraperwiki.com/js/json-min.js"></script>
<script>
var paper; 
$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    var st = paper.set();
    var sst = [ ]; 
    var rc = paper.rect(40, 4, 70, 50, 5).attr({"fill": "#049", scale:"0.6 0.6 50 50"});
    rc.drag(
    function(dx, dy)
    {
        this.attr({x: this.ox + dx, y: this.oy + dy});
        this.dx = dx; this.dy = dy; 
    },
    function () 
    {
        this.ox = this.attr("x");
        this.oy = this.attr("y");
        this.dx = 0; this.dy = 0; 
        this.attr({opacity: 0.5});
    },
    function() 
    {
        this.attr({opacity: 1});
        st.translate(this.dx, this.dy); 
        //for (var i = 0; i < sst.length; i++)
        //    sst[i].translate(this.dx*(1+i/5420.0), this.dy); 

    });

    var sss = 0.2; 
    var crc = paper.circle(20, 30, 10).attr("fill", "#094");
    crc.click(function(event) { sss*=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 
    var crc1 = paper.circle(20, 70, 10).attr("fill", "#904");
    crc1.click(function(event) { sss/=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 

    docave(paper, st, sst); 
})

var c1, c; 
function docave(paper, st, sst)
{
$.ajax({url:"http://scraperwikiviews.com/run//cave_svg_server_1/", success: function(sdata)
{
    var data = $.evalJSON(sdata);
    for (var i = 0; i < data["paths"].length; i+=1)
    {
        c1 = paper.path(data["paths"][i]["d"]); 
        st.push(c1); 
        //        var url = "http://knowledgeforge.net/sesame/club/mmmmc/rawscans/"+data[i].url; 
        //alert(url);        var c = paper.image(url, 10 + i*80, 10 + i*80, 500, 500);
        //console.log($.toJSON(data[i]));
        //break; if (i > 0)  break; 
    }

    var sketchframe = data["sketchframes"][2]; 
    var sca = 1.0/sketchframe["scaledown"]; 
    c = paper.image(sketchframe["sfsketch"], 0, 0, sketchframe["imagepixelswidth"], sketchframe["imagepixelsheight"]);
    c.scale(sca, sca, 0, 0); 
    c.rotate(-sketchframe["rotatedeg"], 0, 0); 
    c.translate(sketchframe["rxtrans"], sketchframe["rytrans"]); 
    st.push(c); 
}})
}

</script>
</head>
<body>
<h4>Early cave SVG viewer</h4>
<p>Still needs proper scaling and dragging of view window, within visibility, 
feedback to server of the area so it can partially download  only the polygons in the window, 
styling and colours, a backup bitmap when zoomed out.
<em>Note: Raphael rescales everything by parsing and multiplying it rather than using transforms.  This is no good</em>
    <div id="rstuff" style="width:800px; height:600px;background:#eee;border:thick blue solid; overflow:none"></div>
</body>
</html>


<html>
<head>
<script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="http://media.scraperwiki.com/js/json-min.js"></script>
<script>
var paper; 
$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    var st = paper.set();
    var sst = [ ]; 
    var rc = paper.rect(40, 4, 70, 50, 5).attr({"fill": "#049", scale:"0.6 0.6 50 50"});
    rc.drag(
    function(dx, dy)
    {
        this.attr({x: this.ox + dx, y: this.oy + dy});
        this.dx = dx; this.dy = dy; 
    },
    function () 
    {
        this.ox = this.attr("x");
        this.oy = this.attr("y");
        this.dx = 0; this.dy = 0; 
        this.attr({opacity: 0.5});
    },
    function() 
    {
        this.attr({opacity: 1});
        st.translate(this.dx, this.dy); 
        //for (var i = 0; i < sst.length; i++)
        //    sst[i].translate(this.dx*(1+i/5420.0), this.dy); 

    });

    var sss = 0.2; 
    var crc = paper.circle(20, 30, 10).attr("fill", "#094");
    crc.click(function(event) { sss*=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 
    var crc1 = paper.circle(20, 70, 10).attr("fill", "#904");
    crc1.click(function(event) { sss/=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 

    docave(paper, st, sst); 
})

var c1, c; 
function docave(paper, st, sst)
{
$.ajax({url:"http://scraperwikiviews.com/run//cave_svg_server_1/", success: function(sdata)
{
    var data = $.evalJSON(sdata);
    for (var i = 0; i < data["paths"].length; i+=1)
    {
        c1 = paper.path(data["paths"][i]["d"]); 
        st.push(c1); 
        //        var url = "http://knowledgeforge.net/sesame/club/mmmmc/rawscans/"+data[i].url; 
        //alert(url);        var c = paper.image(url, 10 + i*80, 10 + i*80, 500, 500);
        //console.log($.toJSON(data[i]));
        //break; if (i > 0)  break; 
    }

    var sketchframe = data["sketchframes"][2]; 
    var sca = 1.0/sketchframe["scaledown"]; 
    c = paper.image(sketchframe["sfsketch"], 0, 0, sketchframe["imagepixelswidth"], sketchframe["imagepixelsheight"]);
    c.scale(sca, sca, 0, 0); 
    c.rotate(-sketchframe["rotatedeg"], 0, 0); 
    c.translate(sketchframe["rxtrans"], sketchframe["rytrans"]); 
    st.push(c); 
}})
}

</script>
</head>
<body>
<h4>Early cave SVG viewer</h4>
<p>Still needs proper scaling and dragging of view window, within visibility, 
feedback to server of the area so it can partially download  only the polygons in the window, 
styling and colours, a backup bitmap when zoomed out.
<em>Note: Raphael rescales everything by parsing and multiplying it rather than using transforms.  This is no good</em>
    <div id="rstuff" style="width:800px; height:600px;background:#eee;border:thick blue solid; overflow:none"></div>
</body>
</html>


<html>
<head>
<script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="http://media.scraperwiki.com/js/json-min.js"></script>
<script>
var paper; 
$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    var st = paper.set();
    var sst = [ ]; 
    var rc = paper.rect(40, 4, 70, 50, 5).attr({"fill": "#049", scale:"0.6 0.6 50 50"});
    rc.drag(
    function(dx, dy)
    {
        this.attr({x: this.ox + dx, y: this.oy + dy});
        this.dx = dx; this.dy = dy; 
    },
    function () 
    {
        this.ox = this.attr("x");
        this.oy = this.attr("y");
        this.dx = 0; this.dy = 0; 
        this.attr({opacity: 0.5});
    },
    function() 
    {
        this.attr({opacity: 1});
        st.translate(this.dx, this.dy); 
        //for (var i = 0; i < sst.length; i++)
        //    sst[i].translate(this.dx*(1+i/5420.0), this.dy); 

    });

    var sss = 0.2; 
    var crc = paper.circle(20, 30, 10).attr("fill", "#094");
    crc.click(function(event) { sss*=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 
    var crc1 = paper.circle(20, 70, 10).attr("fill", "#904");
    crc1.click(function(event) { sss/=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 

    docave(paper, st, sst); 
})

var c1, c; 
function docave(paper, st, sst)
{
$.ajax({url:"http://scraperwikiviews.com/run//cave_svg_server_1/", success: function(sdata)
{
    var data = $.evalJSON(sdata);
    for (var i = 0; i < data["paths"].length; i+=1)
    {
        c1 = paper.path(data["paths"][i]["d"]); 
        st.push(c1); 
        //        var url = "http://knowledgeforge.net/sesame/club/mmmmc/rawscans/"+data[i].url; 
        //alert(url);        var c = paper.image(url, 10 + i*80, 10 + i*80, 500, 500);
        //console.log($.toJSON(data[i]));
        //break; if (i > 0)  break; 
    }

    var sketchframe = data["sketchframes"][2]; 
    var sca = 1.0/sketchframe["scaledown"]; 
    c = paper.image(sketchframe["sfsketch"], 0, 0, sketchframe["imagepixelswidth"], sketchframe["imagepixelsheight"]);
    c.scale(sca, sca, 0, 0); 
    c.rotate(-sketchframe["rotatedeg"], 0, 0); 
    c.translate(sketchframe["rxtrans"], sketchframe["rytrans"]); 
    st.push(c); 
}})
}

</script>
</head>
<body>
<h4>Early cave SVG viewer</h4>
<p>Still needs proper scaling and dragging of view window, within visibility, 
feedback to server of the area so it can partially download  only the polygons in the window, 
styling and colours, a backup bitmap when zoomed out.
<em>Note: Raphael rescales everything by parsing and multiplying it rather than using transforms.  This is no good</em>
    <div id="rstuff" style="width:800px; height:600px;background:#eee;border:thick blue solid; overflow:none"></div>
</body>
</html>


<html>
<head>
<script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="http://media.scraperwiki.com/js/json-min.js"></script>
<script>
var paper; 
$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    var st = paper.set();
    var sst = [ ]; 
    var rc = paper.rect(40, 4, 70, 50, 5).attr({"fill": "#049", scale:"0.6 0.6 50 50"});
    rc.drag(
    function(dx, dy)
    {
        this.attr({x: this.ox + dx, y: this.oy + dy});
        this.dx = dx; this.dy = dy; 
    },
    function () 
    {
        this.ox = this.attr("x");
        this.oy = this.attr("y");
        this.dx = 0; this.dy = 0; 
        this.attr({opacity: 0.5});
    },
    function() 
    {
        this.attr({opacity: 1});
        st.translate(this.dx, this.dy); 
        //for (var i = 0; i < sst.length; i++)
        //    sst[i].translate(this.dx*(1+i/5420.0), this.dy); 

    });

    var sss = 0.2; 
    var crc = paper.circle(20, 30, 10).attr("fill", "#094");
    crc.click(function(event) { sss*=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 
    var crc1 = paper.circle(20, 70, 10).attr("fill", "#904");
    crc1.click(function(event) { sss/=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 

    docave(paper, st, sst); 
})

var c1, c; 
function docave(paper, st, sst)
{
$.ajax({url:"http://scraperwikiviews.com/run//cave_svg_server_1/", success: function(sdata)
{
    var data = $.evalJSON(sdata);
    for (var i = 0; i < data["paths"].length; i+=1)
    {
        c1 = paper.path(data["paths"][i]["d"]); 
        st.push(c1); 
        //        var url = "http://knowledgeforge.net/sesame/club/mmmmc/rawscans/"+data[i].url; 
        //alert(url);        var c = paper.image(url, 10 + i*80, 10 + i*80, 500, 500);
        //console.log($.toJSON(data[i]));
        //break; if (i > 0)  break; 
    }

    var sketchframe = data["sketchframes"][2]; 
    var sca = 1.0/sketchframe["scaledown"]; 
    c = paper.image(sketchframe["sfsketch"], 0, 0, sketchframe["imagepixelswidth"], sketchframe["imagepixelsheight"]);
    c.scale(sca, sca, 0, 0); 
    c.rotate(-sketchframe["rotatedeg"], 0, 0); 
    c.translate(sketchframe["rxtrans"], sketchframe["rytrans"]); 
    st.push(c); 
}})
}

</script>
</head>
<body>
<h4>Early cave SVG viewer</h4>
<p>Still needs proper scaling and dragging of view window, within visibility, 
feedback to server of the area so it can partially download  only the polygons in the window, 
styling and colours, a backup bitmap when zoomed out.
<em>Note: Raphael rescales everything by parsing and multiplying it rather than using transforms.  This is no good</em>
    <div id="rstuff" style="width:800px; height:600px;background:#eee;border:thick blue solid; overflow:none"></div>
</body>
</html>


<html>
<head>
<script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="http://media.scraperwiki.com/js/json-min.js"></script>
<script>
var paper; 
$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    var st = paper.set();
    var sst = [ ]; 
    var rc = paper.rect(40, 4, 70, 50, 5).attr({"fill": "#049", scale:"0.6 0.6 50 50"});
    rc.drag(
    function(dx, dy)
    {
        this.attr({x: this.ox + dx, y: this.oy + dy});
        this.dx = dx; this.dy = dy; 
    },
    function () 
    {
        this.ox = this.attr("x");
        this.oy = this.attr("y");
        this.dx = 0; this.dy = 0; 
        this.attr({opacity: 0.5});
    },
    function() 
    {
        this.attr({opacity: 1});
        st.translate(this.dx, this.dy); 
        //for (var i = 0; i < sst.length; i++)
        //    sst[i].translate(this.dx*(1+i/5420.0), this.dy); 

    });

    var sss = 0.2; 
    var crc = paper.circle(20, 30, 10).attr("fill", "#094");
    crc.click(function(event) { sss*=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 
    var crc1 = paper.circle(20, 70, 10).attr("fill", "#904");
    crc1.click(function(event) { sss/=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 

    docave(paper, st, sst); 
})

var c1, c; 
function docave(paper, st, sst)
{
$.ajax({url:"http://scraperwikiviews.com/run//cave_svg_server_1/", success: function(sdata)
{
    var data = $.evalJSON(sdata);
    for (var i = 0; i < data["paths"].length; i+=1)
    {
        c1 = paper.path(data["paths"][i]["d"]); 
        st.push(c1); 
        //        var url = "http://knowledgeforge.net/sesame/club/mmmmc/rawscans/"+data[i].url; 
        //alert(url);        var c = paper.image(url, 10 + i*80, 10 + i*80, 500, 500);
        //console.log($.toJSON(data[i]));
        //break; if (i > 0)  break; 
    }

    var sketchframe = data["sketchframes"][2]; 
    var sca = 1.0/sketchframe["scaledown"]; 
    c = paper.image(sketchframe["sfsketch"], 0, 0, sketchframe["imagepixelswidth"], sketchframe["imagepixelsheight"]);
    c.scale(sca, sca, 0, 0); 
    c.rotate(-sketchframe["rotatedeg"], 0, 0); 
    c.translate(sketchframe["rxtrans"], sketchframe["rytrans"]); 
    st.push(c); 
}})
}

</script>
</head>
<body>
<h4>Early cave SVG viewer</h4>
<p>Still needs proper scaling and dragging of view window, within visibility, 
feedback to server of the area so it can partially download  only the polygons in the window, 
styling and colours, a backup bitmap when zoomed out.
<em>Note: Raphael rescales everything by parsing and multiplying it rather than using transforms.  This is no good</em>
    <div id="rstuff" style="width:800px; height:600px;background:#eee;border:thick blue solid; overflow:none"></div>
</body>
</html>


<html>
<head>
<script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="http://media.scraperwiki.com/js/json-min.js"></script>
<script>
var paper; 
$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    var st = paper.set();
    var sst = [ ]; 
    var rc = paper.rect(40, 4, 70, 50, 5).attr({"fill": "#049", scale:"0.6 0.6 50 50"});
    rc.drag(
    function(dx, dy)
    {
        this.attr({x: this.ox + dx, y: this.oy + dy});
        this.dx = dx; this.dy = dy; 
    },
    function () 
    {
        this.ox = this.attr("x");
        this.oy = this.attr("y");
        this.dx = 0; this.dy = 0; 
        this.attr({opacity: 0.5});
    },
    function() 
    {
        this.attr({opacity: 1});
        st.translate(this.dx, this.dy); 
        //for (var i = 0; i < sst.length; i++)
        //    sst[i].translate(this.dx*(1+i/5420.0), this.dy); 

    });

    var sss = 0.2; 
    var crc = paper.circle(20, 30, 10).attr("fill", "#094");
    crc.click(function(event) { sss*=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 
    var crc1 = paper.circle(20, 70, 10).attr("fill", "#904");
    crc1.click(function(event) { sss/=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 

    docave(paper, st, sst); 
})

var c1, c; 
function docave(paper, st, sst)
{
$.ajax({url:"http://scraperwikiviews.com/run//cave_svg_server_1/", success: function(sdata)
{
    var data = $.evalJSON(sdata);
    for (var i = 0; i < data["paths"].length; i+=1)
    {
        c1 = paper.path(data["paths"][i]["d"]); 
        st.push(c1); 
        //        var url = "http://knowledgeforge.net/sesame/club/mmmmc/rawscans/"+data[i].url; 
        //alert(url);        var c = paper.image(url, 10 + i*80, 10 + i*80, 500, 500);
        //console.log($.toJSON(data[i]));
        //break; if (i > 0)  break; 
    }

    var sketchframe = data["sketchframes"][2]; 
    var sca = 1.0/sketchframe["scaledown"]; 
    c = paper.image(sketchframe["sfsketch"], 0, 0, sketchframe["imagepixelswidth"], sketchframe["imagepixelsheight"]);
    c.scale(sca, sca, 0, 0); 
    c.rotate(-sketchframe["rotatedeg"], 0, 0); 
    c.translate(sketchframe["rxtrans"], sketchframe["rytrans"]); 
    st.push(c); 
}})
}

</script>
</head>
<body>
<h4>Early cave SVG viewer</h4>
<p>Still needs proper scaling and dragging of view window, within visibility, 
feedback to server of the area so it can partially download  only the polygons in the window, 
styling and colours, a backup bitmap when zoomed out.
<em>Note: Raphael rescales everything by parsing and multiplying it rather than using transforms.  This is no good</em>
    <div id="rstuff" style="width:800px; height:600px;background:#eee;border:thick blue solid; overflow:none"></div>
</body>
</html>


<html>
<head>
<script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
<script src="http://media.scraperwiki.com/js/json-min.js"></script>
<script>
var paper; 
$(document).ready(function()
{
    paper = Raphael(document.getElementById("rstuff"));
    var st = paper.set();
    var sst = [ ]; 
    var rc = paper.rect(40, 4, 70, 50, 5).attr({"fill": "#049", scale:"0.6 0.6 50 50"});
    rc.drag(
    function(dx, dy)
    {
        this.attr({x: this.ox + dx, y: this.oy + dy});
        this.dx = dx; this.dy = dy; 
    },
    function () 
    {
        this.ox = this.attr("x");
        this.oy = this.attr("y");
        this.dx = 0; this.dy = 0; 
        this.attr({opacity: 0.5});
    },
    function() 
    {
        this.attr({opacity: 1});
        st.translate(this.dx, this.dy); 
        //for (var i = 0; i < sst.length; i++)
        //    sst[i].translate(this.dx*(1+i/5420.0), this.dy); 

    });

    var sss = 0.2; 
    var crc = paper.circle(20, 30, 10).attr("fill", "#094");
    crc.click(function(event) { sss*=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 
    var crc1 = paper.circle(20, 70, 10).attr("fill", "#904");
    crc1.click(function(event) { sss/=0.6; st.scale(sss, sss, rc.attr("x"), rc.attr("y")); }); 

    docave(paper, st, sst); 
})

var c1, c; 
function docave(paper, st, sst)
{
$.ajax({url:"http://scraperwikiviews.com/run//cave_svg_server_1/", success: function(sdata)
{
    var data = $.evalJSON(sdata);
    for (var i = 0; i < data["paths"].length; i+=1)
    {
        c1 = paper.path(data["paths"][i]["d"]); 
        st.push(c1); 
        //        var url = "http://knowledgeforge.net/sesame/club/mmmmc/rawscans/"+data[i].url; 
        //alert(url);        var c = paper.image(url, 10 + i*80, 10 + i*80, 500, 500);
        //console.log($.toJSON(data[i]));
        //break; if (i > 0)  break; 
    }

    var sketchframe = data["sketchframes"][2]; 
    var sca = 1.0/sketchframe["scaledown"]; 
    c = paper.image(sketchframe["sfsketch"], 0, 0, sketchframe["imagepixelswidth"], sketchframe["imagepixelsheight"]);
    c.scale(sca, sca, 0, 0); 
    c.rotate(-sketchframe["rotatedeg"], 0, 0); 
    c.translate(sketchframe["rxtrans"], sketchframe["rytrans"]); 
    st.push(c); 
}})
}

</script>
</head>
<body>
<h4>Early cave SVG viewer</h4>
<p>Still needs proper scaling and dragging of view window, within visibility, 
feedback to server of the area so it can partially download  only the polygons in the window, 
styling and colours, a backup bitmap when zoomed out.
<em>Note: Raphael rescales everything by parsing and multiplying it rather than using transforms.  This is no good</em>
    <div id="rstuff" style="width:800px; height:600px;background:#eee;border:thick blue solid; overflow:none"></div>
</body>
</html>


