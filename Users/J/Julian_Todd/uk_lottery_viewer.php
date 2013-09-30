<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

<html>
    <head>
        <script src="http://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
        <script src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script>
        <script src="http://media.scraperwiki.com/js/json-min.js"></script>
    </head>

<body>
    <h4>View of lottery data</h4>
    <p>Click on a green bar to show the grants for that Local Authority</p>
    <p>The code can be edited here <a href="http://scraperwiki.com/views/uk_lottery_viewer/edit/">here</a> and the corresponding server script is <a href="http://scraperwiki.com/views/uk_lottery_jsonserver/edit/">here</a>.</p>

<div id="rspecial" style="float:right; width:500px; height:500px;background:#eee;border:thin red solid; overflow:auto"></div>
<div id="rstuff" style="width:400px; height:3000px;background:#eee;border:thin red solid; overflow:none"></div>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var font = '100 10px "Helvetica Neue", Helvetica, "Arial Unicode MS", Arial, sans-serif'; 
    var data; 
    var rects; 
    var prevrects = [ ]; 
    $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/", success: function(sdata)
    {
        data = $.evalJSON(sdata);
        rects = [ ]; 
        for (var i = 0; i < data.length; i++) 
        { (function(i) {

            var w = data[i]["money"]/80000; 
            var c = paper.circle(300, i*10+20, Math.sqrt(w)).attr({fill:"green"});
            rects.push(c); 
            var txt = paper.text(610, i*10+21, data[i]["localauthority"]).attr({"font":font, "text-anchor":"start"});
            c.node.onclick = function() 
            { 
                $("#rspecial").html("<h1>Loading...</h1>"); 
                while (prevrects.length != 0)
                    prevrects.pop().animate({"stroke-width":1, fill:"#999", stroke:"black"}, 100);  
                rects[i].animate({"stroke-width":5, fill:"red", stroke:"red"}, 100); 
                prevrects.push(rects[i]); 
                $.ajax({url:"http://scraperwikiviews.com/run/UK_lottery_jsonserver/?"+escape(data[i]["localauthority"]), success:function(lsdata)
                {
                    ldata = $.evalJSON(lsdata);
                    var rows = [ "<h3>Grants in "+data[i]["localauthority"]+"</h3>", '<table style="font-size:50%;">']
                    for (var j = 0; j < ldata.length; j++)
                    {
                        var d = ldata[j]; 
                        rows.push('<tr><td>'+d["date"].substring(0, 10)+'</td><td>');
                        rows.push('£'+d["amount"]+"</td><td>"+d["distributor"]+"</td><td>"); 
                        rows.push('<a href="'+d["url"]+'">'+d["recipient"]+"</td></tr>"); 
                    }
                    rows.push("</table>");
                    $("#rspecial").html(rows.join("")); 
                } 
            })}; 
        })(i) }
    }})
})

</script>

</body>
</html>

