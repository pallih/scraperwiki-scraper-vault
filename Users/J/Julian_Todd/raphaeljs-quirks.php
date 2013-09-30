<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


<html>
<head>
<script src="https://media.scraperwiki.com/js/raphael-1.5.2.min.js"></script>
<script src="https://media.scraperwiki.com/js/jquery-1.3.2.js"></script>

<script>
$(document).ready(function()
{
    var paper = Raphael(document.getElementById("rstuff"));
    var line = paper.path("M150 50L320 90").attr("stroke-width", 30); 
    var c1 = paper.text(30, 50, "scaledown").click(function(event) { line.scale(0.6, 0.6, 0, 0); }); 
    var c2 = paper.text(30, 60, "scaledownA").click(function(event) { line.attr("scale", "0.6 0.6 0 0") }); 
    var c1 = paper.text(30, 80, "translate").click(function(event) { line.translate(100, 0); }); 
    for (var x = 0; x < 600; x += 100)
        paper.path("M"+x+" 0L"+x+" 200"); 
})


</script>
</head>
<body>
<h4>Quirky behaviour on <a href="http://raphaeljs.com/reference.html">RaphaelJS</a> SVG library</h4>
<p>Most of the issues are to do with scaling and translating.</p>
<p>The source for this page is accessible <a href="http://scraperwiki.com/views/raphaeljs-quirks/edit/">here</a>.</p>

<div id="rstuff" style="width:600px; height:200px;background:#eee;border:thick blue solid; overflow:none"></div>

<p><b>Scale:</b> According to <a href="http://raphaeljs.com/reference.html#scale">the documentation</a> 
clicking on <b>scaledown</b> which does <br/><tt>line.scale(0.6, 0.6, 0, 0)</tt><br/> (scale by 0.6 around the point (0, 0) of top left corner) 
should be the same as clicking on <b>scaledownA</b> which does <br/><tt>line.attr("scale", "0.6 0.6 0 0")</tt><br/>  
This is true in Chrome, but not IE, which chooses to scale about the centre of the line object (235, 70).
</p>
  

</body>
</html>


