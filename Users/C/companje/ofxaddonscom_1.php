<?php
//    $sort = $_GET["sort"];
//    $action = $_GET["action"];
//    $link = $_GET["link"];
//    scraperwiki::attach("ofxaddonscom");

?>

<html>
<head> 
    <title>ofxAddons</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1"> 
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.0/jquery.mobile-1.0.min.css" />
    <script type="text/javascript" src="http://code.jquery.com/jquery-1.6.4.min.js"></script>
    <script type="text/javascript" src="http://code.jquery.com/mobile/1.0/jquery.mobile-1.0.min.js"></script>
</head> 
<body onload='document.getElementById("scraperwikipane").style.display="none"'>

<?php
if ($action=="detail") {
       //$data = scraperwiki::select("* from repos order by category,name");
    $data = scraperwiki::select("* from repos where link='$link'");
    $name = $data["name"];
    $author = $data["author"];
    $description = $data["description"];
?>

    <div data-role="page">
        
            <div data-role="header" data-theme="d">
                <h1><?php echo $name; ?></h1>
    
            </div>
    
            <div data-role="content" data-theme="c">
                <h1><?php echo $name; ?></h1>
                <p><?php echo $description; ?></p>
                <!--<a href="?" data-role="button" data-rel="back" data-theme="b">Download</a>       -->
                <a href="?" data-role="button" data-rel="back" data-theme="c">Close</a>    
            </div>
        </div>
    
    
    </body>
    </html>

<?php


}
?>

<div data-role="page">

    <div data-role="header">
        <h1>ofxAddons.com</h1>
        <div data-role="navbar">
            <ul>
                <li><a href="?sort=category">Sort by Category</a></li>
                <li><a href="?sort=alphabet">Sort by Name</a></li>
                <!--<li><a href="?sort=date">Sort by Date</a></li>--> <!--class="ui-btn-active"-->
            </ul>
        </div><!-- /navbar -->
    </div><!-- /header -->

    <div data-role="content">    
  
        <ul data-role="listview" data-inset="true" data-theme="d" data-divider-theme="d" data-filter="true">

            <?php
            
            if ( $sort=="" || $sort=="category") {
                $pCategory = "";
                $data = scraperwiki::select("* from repos order by category,name");
                
                foreach($data as $d){
                    $name = $d["name"];
                    $link = $d["link"];
                    $category = $d["category"];
    
                    if ($category!=$pCategory) {
                        print "<li data-role=\"list-divider\">$category</li>";
                    }
                    $pCategory = $category;
                    print "<li><a href=\"?action=detail&link=$link\" data-rel=\"dialog\">$name</a></li>";
                }
            }

            if ($sort=="alphabet") {
                $data = scraperwiki::select("* from repos order by name");
                foreach($data as $d){
                    $name = $d["name"];
                    $link = $d["link"];
                    print "<li><a href=\"?action=detail&link=$link\" data-rel=\"dialog\">$name</a></li>";
                }
            }
            ?>
        </ul>

    </div><!-- /content -->

    <div data-role="footer">
        <h4>ofxAddons.com</h4>
    </div><!-- /footer -->
</div><!-- /page -->

</body>
</html>