<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Regmem editor</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/CodeMirror-0.92/js/codemirror.js"></script> 
    <style type="text/css">
        .Dfullscreen { text-align: center }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #ulch { float:right; height:500px; width:230px; overflow: auto}
        #cmdiv { width: 544px; border: thin black solid; }
        #tavalue { }
        li { list-style-type:none; }
        li.err { color:red; }
        p.err { color:red; } 
        .CodeMirror-line-numbers {width: 25px;color: #888;background:#fafafa;text-align: right;
            padding: 0.4em 0px 0 0px;margin: 0;font-family: monaco, monospace;font-size: 10pt;line-height: 1.1em;
            border-right:solid 1px #9f9f9f;position:relative;}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var data; 
var cmeditor; 

function gotsec(sdata)
{
    data = $.evalJSON(sdata); 
    $("#mpname").text(data["mpname"]);
    cmeditor.setCode(data["contents"].join("\n")); 
    if (data["err"] != undefined)
    {
        var lnhandle = cmeditor.nthLine(data["lineno"]+1); 
        cmeditor.selectLines(lnhandle, 0, cmeditor.nextLine(lnhandle ), 0)
        $("p.err").text(data["err"] + data["trace"]);
    }
}


$(document).ready(function() 
{ 
    var baseq = "http://scraperwikiviews.com/run/serve-edit-register-of-members-interests/"; 
    cmeditor = CodeMirror.fromTextArea("cmeditor", 
    {
        parserfile: ["parsedummy.js"],
        stylesheet: ["http://media.scraperwiki.com/css/codemirrorcolours.css",
                     "http://media.scraperwiki.com/CodeMirror-0.92/css/jscolors.css"], 
        lineNumbers: true,
        width:"510px", 
        textWrapping: false, 
        path: "http://media.scraperwiki.com/CodeMirror-0.92/js/"
    });

    $("#bdiff").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&diff=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#taback").val(ldata["back"].join("\n")); 
        }})
    });

    $("#bparse").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&save=1"; 
        $.ajax({url:url, success: gotsec});
    });

    $("#btodo").click(function()
    {
        var url = baseq+"?list=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#ulch").text("")
            for (var i=0; i < ldata.length; i++)
            {
                var el = [ "<li" ];
                if (ldata[i][1]["err"] != undefined)
                    el.push(' class="err" ln="'+ldata[i][1]["lineno"]+'"'); 
                el.push(">"); 
                el.push(ldata[i][0]); 
                el.push("</li>"); 
                $("#ulch").append(el.join(""));
            }
            $("#ulch li").click(function()
            {
                var url = baseq+"?mpname="+escape($(this).text()); 
                $.ajax({url:url, contentType: "application/json; charset=utf-8", success: gotsec }); 
            })
        }})
    }); 
})
</script>

</head>
<body class="fullscreen">
<div>
    <ul id="ulch"></ul>
    <h3><span id="mpname"></span> -- <span id="claimcat"></span></h3>
    <p class="err"></p>
    <p>
        <input type="button" id="bdiff" value="bdiff"/>
        <input type="button" id="bparse" value="bparse"/>
        <input type="button" id="btodo" value="btodo"/>
    </p>
    <div style="border: thin black solid" id="cmdiv">
        <textarea id="cmeditor">GGGGGG</textarea>
    </div>
</div>

</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Regmem editor</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/CodeMirror-0.92/js/codemirror.js"></script> 
    <style type="text/css">
        .Dfullscreen { text-align: center }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #ulch { float:right; height:500px; width:230px; overflow: auto}
        #cmdiv { width: 544px; border: thin black solid; }
        #tavalue { }
        li { list-style-type:none; }
        li.err { color:red; }
        p.err { color:red; } 
        .CodeMirror-line-numbers {width: 25px;color: #888;background:#fafafa;text-align: right;
            padding: 0.4em 0px 0 0px;margin: 0;font-family: monaco, monospace;font-size: 10pt;line-height: 1.1em;
            border-right:solid 1px #9f9f9f;position:relative;}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var data; 
var cmeditor; 

function gotsec(sdata)
{
    data = $.evalJSON(sdata); 
    $("#mpname").text(data["mpname"]);
    cmeditor.setCode(data["contents"].join("\n")); 
    if (data["err"] != undefined)
    {
        var lnhandle = cmeditor.nthLine(data["lineno"]+1); 
        cmeditor.selectLines(lnhandle, 0, cmeditor.nextLine(lnhandle ), 0)
        $("p.err").text(data["err"] + data["trace"]);
    }
}


$(document).ready(function() 
{ 
    var baseq = "http://scraperwikiviews.com/run/serve-edit-register-of-members-interests/"; 
    cmeditor = CodeMirror.fromTextArea("cmeditor", 
    {
        parserfile: ["parsedummy.js"],
        stylesheet: ["http://media.scraperwiki.com/css/codemirrorcolours.css",
                     "http://media.scraperwiki.com/CodeMirror-0.92/css/jscolors.css"], 
        lineNumbers: true,
        width:"510px", 
        textWrapping: false, 
        path: "http://media.scraperwiki.com/CodeMirror-0.92/js/"
    });

    $("#bdiff").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&diff=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#taback").val(ldata["back"].join("\n")); 
        }})
    });

    $("#bparse").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&save=1"; 
        $.ajax({url:url, success: gotsec});
    });

    $("#btodo").click(function()
    {
        var url = baseq+"?list=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#ulch").text("")
            for (var i=0; i < ldata.length; i++)
            {
                var el = [ "<li" ];
                if (ldata[i][1]["err"] != undefined)
                    el.push(' class="err" ln="'+ldata[i][1]["lineno"]+'"'); 
                el.push(">"); 
                el.push(ldata[i][0]); 
                el.push("</li>"); 
                $("#ulch").append(el.join(""));
            }
            $("#ulch li").click(function()
            {
                var url = baseq+"?mpname="+escape($(this).text()); 
                $.ajax({url:url, contentType: "application/json; charset=utf-8", success: gotsec }); 
            })
        }})
    }); 
})
</script>

</head>
<body class="fullscreen">
<div>
    <ul id="ulch"></ul>
    <h3><span id="mpname"></span> -- <span id="claimcat"></span></h3>
    <p class="err"></p>
    <p>
        <input type="button" id="bdiff" value="bdiff"/>
        <input type="button" id="bparse" value="bparse"/>
        <input type="button" id="btodo" value="btodo"/>
    </p>
    <div style="border: thin black solid" id="cmdiv">
        <textarea id="cmeditor">GGGGGG</textarea>
    </div>
</div>

</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Regmem editor</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/CodeMirror-0.92/js/codemirror.js"></script> 
    <style type="text/css">
        .Dfullscreen { text-align: center }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #ulch { float:right; height:500px; width:230px; overflow: auto}
        #cmdiv { width: 544px; border: thin black solid; }
        #tavalue { }
        li { list-style-type:none; }
        li.err { color:red; }
        p.err { color:red; } 
        .CodeMirror-line-numbers {width: 25px;color: #888;background:#fafafa;text-align: right;
            padding: 0.4em 0px 0 0px;margin: 0;font-family: monaco, monospace;font-size: 10pt;line-height: 1.1em;
            border-right:solid 1px #9f9f9f;position:relative;}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var data; 
var cmeditor; 

function gotsec(sdata)
{
    data = $.evalJSON(sdata); 
    $("#mpname").text(data["mpname"]);
    cmeditor.setCode(data["contents"].join("\n")); 
    if (data["err"] != undefined)
    {
        var lnhandle = cmeditor.nthLine(data["lineno"]+1); 
        cmeditor.selectLines(lnhandle, 0, cmeditor.nextLine(lnhandle ), 0)
        $("p.err").text(data["err"] + data["trace"]);
    }
}


$(document).ready(function() 
{ 
    var baseq = "http://scraperwikiviews.com/run/serve-edit-register-of-members-interests/"; 
    cmeditor = CodeMirror.fromTextArea("cmeditor", 
    {
        parserfile: ["parsedummy.js"],
        stylesheet: ["http://media.scraperwiki.com/css/codemirrorcolours.css",
                     "http://media.scraperwiki.com/CodeMirror-0.92/css/jscolors.css"], 
        lineNumbers: true,
        width:"510px", 
        textWrapping: false, 
        path: "http://media.scraperwiki.com/CodeMirror-0.92/js/"
    });

    $("#bdiff").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&diff=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#taback").val(ldata["back"].join("\n")); 
        }})
    });

    $("#bparse").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&save=1"; 
        $.ajax({url:url, success: gotsec});
    });

    $("#btodo").click(function()
    {
        var url = baseq+"?list=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#ulch").text("")
            for (var i=0; i < ldata.length; i++)
            {
                var el = [ "<li" ];
                if (ldata[i][1]["err"] != undefined)
                    el.push(' class="err" ln="'+ldata[i][1]["lineno"]+'"'); 
                el.push(">"); 
                el.push(ldata[i][0]); 
                el.push("</li>"); 
                $("#ulch").append(el.join(""));
            }
            $("#ulch li").click(function()
            {
                var url = baseq+"?mpname="+escape($(this).text()); 
                $.ajax({url:url, contentType: "application/json; charset=utf-8", success: gotsec }); 
            })
        }})
    }); 
})
</script>

</head>
<body class="fullscreen">
<div>
    <ul id="ulch"></ul>
    <h3><span id="mpname"></span> -- <span id="claimcat"></span></h3>
    <p class="err"></p>
    <p>
        <input type="button" id="bdiff" value="bdiff"/>
        <input type="button" id="bparse" value="bparse"/>
        <input type="button" id="btodo" value="btodo"/>
    </p>
    <div style="border: thin black solid" id="cmdiv">
        <textarea id="cmeditor">GGGGGG</textarea>
    </div>
</div>

</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Regmem editor</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/CodeMirror-0.92/js/codemirror.js"></script> 
    <style type="text/css">
        .Dfullscreen { text-align: center }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #ulch { float:right; height:500px; width:230px; overflow: auto}
        #cmdiv { width: 544px; border: thin black solid; }
        #tavalue { }
        li { list-style-type:none; }
        li.err { color:red; }
        p.err { color:red; } 
        .CodeMirror-line-numbers {width: 25px;color: #888;background:#fafafa;text-align: right;
            padding: 0.4em 0px 0 0px;margin: 0;font-family: monaco, monospace;font-size: 10pt;line-height: 1.1em;
            border-right:solid 1px #9f9f9f;position:relative;}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var data; 
var cmeditor; 

function gotsec(sdata)
{
    data = $.evalJSON(sdata); 
    $("#mpname").text(data["mpname"]);
    cmeditor.setCode(data["contents"].join("\n")); 
    if (data["err"] != undefined)
    {
        var lnhandle = cmeditor.nthLine(data["lineno"]+1); 
        cmeditor.selectLines(lnhandle, 0, cmeditor.nextLine(lnhandle ), 0)
        $("p.err").text(data["err"] + data["trace"]);
    }
}


$(document).ready(function() 
{ 
    var baseq = "http://scraperwikiviews.com/run/serve-edit-register-of-members-interests/"; 
    cmeditor = CodeMirror.fromTextArea("cmeditor", 
    {
        parserfile: ["parsedummy.js"],
        stylesheet: ["http://media.scraperwiki.com/css/codemirrorcolours.css",
                     "http://media.scraperwiki.com/CodeMirror-0.92/css/jscolors.css"], 
        lineNumbers: true,
        width:"510px", 
        textWrapping: false, 
        path: "http://media.scraperwiki.com/CodeMirror-0.92/js/"
    });

    $("#bdiff").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&diff=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#taback").val(ldata["back"].join("\n")); 
        }})
    });

    $("#bparse").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&save=1"; 
        $.ajax({url:url, success: gotsec});
    });

    $("#btodo").click(function()
    {
        var url = baseq+"?list=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#ulch").text("")
            for (var i=0; i < ldata.length; i++)
            {
                var el = [ "<li" ];
                if (ldata[i][1]["err"] != undefined)
                    el.push(' class="err" ln="'+ldata[i][1]["lineno"]+'"'); 
                el.push(">"); 
                el.push(ldata[i][0]); 
                el.push("</li>"); 
                $("#ulch").append(el.join(""));
            }
            $("#ulch li").click(function()
            {
                var url = baseq+"?mpname="+escape($(this).text()); 
                $.ajax({url:url, contentType: "application/json; charset=utf-8", success: gotsec }); 
            })
        }})
    }); 
})
</script>

</head>
<body class="fullscreen">
<div>
    <ul id="ulch"></ul>
    <h3><span id="mpname"></span> -- <span id="claimcat"></span></h3>
    <p class="err"></p>
    <p>
        <input type="button" id="bdiff" value="bdiff"/>
        <input type="button" id="bparse" value="bparse"/>
        <input type="button" id="btodo" value="btodo"/>
    </p>
    <div style="border: thin black solid" id="cmdiv">
        <textarea id="cmeditor">GGGGGG</textarea>
    </div>
</div>

</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Regmem editor</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/CodeMirror-0.92/js/codemirror.js"></script> 
    <style type="text/css">
        .Dfullscreen { text-align: center }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #ulch { float:right; height:500px; width:230px; overflow: auto}
        #cmdiv { width: 544px; border: thin black solid; }
        #tavalue { }
        li { list-style-type:none; }
        li.err { color:red; }
        p.err { color:red; } 
        .CodeMirror-line-numbers {width: 25px;color: #888;background:#fafafa;text-align: right;
            padding: 0.4em 0px 0 0px;margin: 0;font-family: monaco, monospace;font-size: 10pt;line-height: 1.1em;
            border-right:solid 1px #9f9f9f;position:relative;}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var data; 
var cmeditor; 

function gotsec(sdata)
{
    data = $.evalJSON(sdata); 
    $("#mpname").text(data["mpname"]);
    cmeditor.setCode(data["contents"].join("\n")); 
    if (data["err"] != undefined)
    {
        var lnhandle = cmeditor.nthLine(data["lineno"]+1); 
        cmeditor.selectLines(lnhandle, 0, cmeditor.nextLine(lnhandle ), 0)
        $("p.err").text(data["err"] + data["trace"]);
    }
}


$(document).ready(function() 
{ 
    var baseq = "http://scraperwikiviews.com/run/serve-edit-register-of-members-interests/"; 
    cmeditor = CodeMirror.fromTextArea("cmeditor", 
    {
        parserfile: ["parsedummy.js"],
        stylesheet: ["http://media.scraperwiki.com/css/codemirrorcolours.css",
                     "http://media.scraperwiki.com/CodeMirror-0.92/css/jscolors.css"], 
        lineNumbers: true,
        width:"510px", 
        textWrapping: false, 
        path: "http://media.scraperwiki.com/CodeMirror-0.92/js/"
    });

    $("#bdiff").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&diff=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#taback").val(ldata["back"].join("\n")); 
        }})
    });

    $("#bparse").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&save=1"; 
        $.ajax({url:url, success: gotsec});
    });

    $("#btodo").click(function()
    {
        var url = baseq+"?list=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#ulch").text("")
            for (var i=0; i < ldata.length; i++)
            {
                var el = [ "<li" ];
                if (ldata[i][1]["err"] != undefined)
                    el.push(' class="err" ln="'+ldata[i][1]["lineno"]+'"'); 
                el.push(">"); 
                el.push(ldata[i][0]); 
                el.push("</li>"); 
                $("#ulch").append(el.join(""));
            }
            $("#ulch li").click(function()
            {
                var url = baseq+"?mpname="+escape($(this).text()); 
                $.ajax({url:url, contentType: "application/json; charset=utf-8", success: gotsec }); 
            })
        }})
    }); 
})
</script>

</head>
<body class="fullscreen">
<div>
    <ul id="ulch"></ul>
    <h3><span id="mpname"></span> -- <span id="claimcat"></span></h3>
    <p class="err"></p>
    <p>
        <input type="button" id="bdiff" value="bdiff"/>
        <input type="button" id="bparse" value="bparse"/>
        <input type="button" id="btodo" value="btodo"/>
    </p>
    <div style="border: thin black solid" id="cmdiv">
        <textarea id="cmeditor">GGGGGG</textarea>
    </div>
</div>

</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Regmem editor</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/CodeMirror-0.92/js/codemirror.js"></script> 
    <style type="text/css">
        .Dfullscreen { text-align: center }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #ulch { float:right; height:500px; width:230px; overflow: auto}
        #cmdiv { width: 544px; border: thin black solid; }
        #tavalue { }
        li { list-style-type:none; }
        li.err { color:red; }
        p.err { color:red; } 
        .CodeMirror-line-numbers {width: 25px;color: #888;background:#fafafa;text-align: right;
            padding: 0.4em 0px 0 0px;margin: 0;font-family: monaco, monospace;font-size: 10pt;line-height: 1.1em;
            border-right:solid 1px #9f9f9f;position:relative;}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var data; 
var cmeditor; 

function gotsec(sdata)
{
    data = $.evalJSON(sdata); 
    $("#mpname").text(data["mpname"]);
    cmeditor.setCode(data["contents"].join("\n")); 
    if (data["err"] != undefined)
    {
        var lnhandle = cmeditor.nthLine(data["lineno"]+1); 
        cmeditor.selectLines(lnhandle, 0, cmeditor.nextLine(lnhandle ), 0)
        $("p.err").text(data["err"] + data["trace"]);
    }
}


$(document).ready(function() 
{ 
    var baseq = "http://scraperwikiviews.com/run/serve-edit-register-of-members-interests/"; 
    cmeditor = CodeMirror.fromTextArea("cmeditor", 
    {
        parserfile: ["parsedummy.js"],
        stylesheet: ["http://media.scraperwiki.com/css/codemirrorcolours.css",
                     "http://media.scraperwiki.com/CodeMirror-0.92/css/jscolors.css"], 
        lineNumbers: true,
        width:"510px", 
        textWrapping: false, 
        path: "http://media.scraperwiki.com/CodeMirror-0.92/js/"
    });

    $("#bdiff").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&diff=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#taback").val(ldata["back"].join("\n")); 
        }})
    });

    $("#bparse").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&save=1"; 
        $.ajax({url:url, success: gotsec});
    });

    $("#btodo").click(function()
    {
        var url = baseq+"?list=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#ulch").text("")
            for (var i=0; i < ldata.length; i++)
            {
                var el = [ "<li" ];
                if (ldata[i][1]["err"] != undefined)
                    el.push(' class="err" ln="'+ldata[i][1]["lineno"]+'"'); 
                el.push(">"); 
                el.push(ldata[i][0]); 
                el.push("</li>"); 
                $("#ulch").append(el.join(""));
            }
            $("#ulch li").click(function()
            {
                var url = baseq+"?mpname="+escape($(this).text()); 
                $.ajax({url:url, contentType: "application/json; charset=utf-8", success: gotsec }); 
            })
        }})
    }); 
})
</script>

</head>
<body class="fullscreen">
<div>
    <ul id="ulch"></ul>
    <h3><span id="mpname"></span> -- <span id="claimcat"></span></h3>
    <p class="err"></p>
    <p>
        <input type="button" id="bdiff" value="bdiff"/>
        <input type="button" id="bparse" value="bparse"/>
        <input type="button" id="btodo" value="btodo"/>
    </p>
    <div style="border: thin black solid" id="cmdiv">
        <textarea id="cmeditor">GGGGGG</textarea>
    </div>
</div>

</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Regmem editor</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/CodeMirror-0.92/js/codemirror.js"></script> 
    <style type="text/css">
        .Dfullscreen { text-align: center }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #ulch { float:right; height:500px; width:230px; overflow: auto}
        #cmdiv { width: 544px; border: thin black solid; }
        #tavalue { }
        li { list-style-type:none; }
        li.err { color:red; }
        p.err { color:red; } 
        .CodeMirror-line-numbers {width: 25px;color: #888;background:#fafafa;text-align: right;
            padding: 0.4em 0px 0 0px;margin: 0;font-family: monaco, monospace;font-size: 10pt;line-height: 1.1em;
            border-right:solid 1px #9f9f9f;position:relative;}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var data; 
var cmeditor; 

function gotsec(sdata)
{
    data = $.evalJSON(sdata); 
    $("#mpname").text(data["mpname"]);
    cmeditor.setCode(data["contents"].join("\n")); 
    if (data["err"] != undefined)
    {
        var lnhandle = cmeditor.nthLine(data["lineno"]+1); 
        cmeditor.selectLines(lnhandle, 0, cmeditor.nextLine(lnhandle ), 0)
        $("p.err").text(data["err"] + data["trace"]);
    }
}


$(document).ready(function() 
{ 
    var baseq = "http://scraperwikiviews.com/run/serve-edit-register-of-members-interests/"; 
    cmeditor = CodeMirror.fromTextArea("cmeditor", 
    {
        parserfile: ["parsedummy.js"],
        stylesheet: ["http://media.scraperwiki.com/css/codemirrorcolours.css",
                     "http://media.scraperwiki.com/CodeMirror-0.92/css/jscolors.css"], 
        lineNumbers: true,
        width:"510px", 
        textWrapping: false, 
        path: "http://media.scraperwiki.com/CodeMirror-0.92/js/"
    });

    $("#bdiff").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&diff=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#taback").val(ldata["back"].join("\n")); 
        }})
    });

    $("#bparse").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&save=1"; 
        $.ajax({url:url, success: gotsec});
    });

    $("#btodo").click(function()
    {
        var url = baseq+"?list=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#ulch").text("")
            for (var i=0; i < ldata.length; i++)
            {
                var el = [ "<li" ];
                if (ldata[i][1]["err"] != undefined)
                    el.push(' class="err" ln="'+ldata[i][1]["lineno"]+'"'); 
                el.push(">"); 
                el.push(ldata[i][0]); 
                el.push("</li>"); 
                $("#ulch").append(el.join(""));
            }
            $("#ulch li").click(function()
            {
                var url = baseq+"?mpname="+escape($(this).text()); 
                $.ajax({url:url, contentType: "application/json; charset=utf-8", success: gotsec }); 
            })
        }})
    }); 
})
</script>

</head>
<body class="fullscreen">
<div>
    <ul id="ulch"></ul>
    <h3><span id="mpname"></span> -- <span id="claimcat"></span></h3>
    <p class="err"></p>
    <p>
        <input type="button" id="bdiff" value="bdiff"/>
        <input type="button" id="bparse" value="bparse"/>
        <input type="button" id="btodo" value="btodo"/>
    </p>
    <div style="border: thin black solid" id="cmdiv">
        <textarea id="cmeditor">GGGGGG</textarea>
    </div>
</div>

</body>
</html>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">

<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <title>Regmem editor</title>
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-1.3.2.js"></script> 
    <script type="text/javascript" src="http://media.scraperwiki.com/js/jquery-ui-1.7.2.custom.min.js"></script>    
    <script type="text/javascript" src="http://media.scraperwiki.com/js/json-min.js"></script>
    <script type="text/javascript" src="http://media.scraperwiki.com/CodeMirror-0.92/js/codemirror.js"></script> 
    <style type="text/css">
        .Dfullscreen { text-align: center }
        #pdfpageid { float: left }
        #annotate { position: fixed; left: 820px; top: 100px; background: #aaaaff }
        #ulch { float:right; height:500px; width:230px; overflow: auto}
        #cmdiv { width: 544px; border: thin black solid; }
        #tavalue { }
        li { list-style-type:none; }
        li.err { color:red; }
        p.err { color:red; } 
        .CodeMirror-line-numbers {width: 25px;color: #888;background:#fafafa;text-align: right;
            padding: 0.4em 0px 0 0px;margin: 0;font-family: monaco, monospace;font-size: 10pt;line-height: 1.1em;
            border-right:solid 1px #9f9f9f;position:relative;}
    </style>
    <link rel="stylesheet" type="text/css" href="http://media.scraperwiki.com/css/jquery.Jcrop.css" />    
    <script type="text/javascript">

var data; 
var cmeditor; 

function gotsec(sdata)
{
    data = $.evalJSON(sdata); 
    $("#mpname").text(data["mpname"]);
    cmeditor.setCode(data["contents"].join("\n")); 
    if (data["err"] != undefined)
    {
        var lnhandle = cmeditor.nthLine(data["lineno"]+1); 
        cmeditor.selectLines(lnhandle, 0, cmeditor.nextLine(lnhandle ), 0)
        $("p.err").text(data["err"] + data["trace"]);
    }
}


$(document).ready(function() 
{ 
    var baseq = "http://scraperwikiviews.com/run/serve-edit-register-of-members-interests/"; 
    cmeditor = CodeMirror.fromTextArea("cmeditor", 
    {
        parserfile: ["parsedummy.js"],
        stylesheet: ["http://media.scraperwiki.com/css/codemirrorcolours.css",
                     "http://media.scraperwiki.com/CodeMirror-0.92/css/jscolors.css"], 
        lineNumbers: true,
        width:"510px", 
        textWrapping: false, 
        path: "http://media.scraperwiki.com/CodeMirror-0.92/js/"
    });

    $("#bdiff").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&diff=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#taback").val(ldata["back"].join("\n")); 
        }})
    });

    $("#bparse").click(function()
    {
        var url = baseq+"?mpname="+escape(data["mpname"])+"&contents="+escape(cmeditor.getCode())+"&save=1"; 
        $.ajax({url:url, success: gotsec});
    });

    $("#btodo").click(function()
    {
        var url = baseq+"?list=1"; 
        $.ajax({url:url, success: function(sdata)
        {
            var ldata = $.evalJSON(sdata); 
            $("#ulch").text("")
            for (var i=0; i < ldata.length; i++)
            {
                var el = [ "<li" ];
                if (ldata[i][1]["err"] != undefined)
                    el.push(' class="err" ln="'+ldata[i][1]["lineno"]+'"'); 
                el.push(">"); 
                el.push(ldata[i][0]); 
                el.push("</li>"); 
                $("#ulch").append(el.join(""));
            }
            $("#ulch li").click(function()
            {
                var url = baseq+"?mpname="+escape($(this).text()); 
                $.ajax({url:url, contentType: "application/json; charset=utf-8", success: gotsec }); 
            })
        }})
    }); 
})
</script>

</head>
<body class="fullscreen">
<div>
    <ul id="ulch"></ul>
    <h3><span id="mpname"></span> -- <span id="claimcat"></span></h3>
    <p class="err"></p>
    <p>
        <input type="button" id="bdiff" value="bdiff"/>
        <input type="button" id="bparse" value="bparse"/>
        <input type="button" id="btodo" value="btodo"/>
    </p>
    <div style="border: thin black solid" id="cmdiv">
        <textarea id="cmeditor">GGGGGG</textarea>
    </div>
</div>

</body>
</html>
