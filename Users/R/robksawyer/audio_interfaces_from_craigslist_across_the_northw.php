<?php
    $limit = 100; // No of records to be shown per page.
    
    function myTruncate($string, $limit, $break=".", $pad="..."){
      // return with no change if string is shorter than $limit
      if(strlen($string) <= $limit) return $string;
    
      // is $break present between $limit and the end of the string?
      if(false !== ($breakpoint = strpos($string, $break, $limit))) {
        if($breakpoint < strlen($string) - 1) {
          $string = substr($string, 0, $breakpoint) . $pad;
        }
      }
        
      return $string;
    }

?>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js" type="text/javascript"></script>
<script src="http://robksawyer.com/js/jquery.masonry.min.js" type="text/javascript"></script>
<script src="http://robksawyer.com/js/modernizr-transitions.js" type="text/javascript"></script>
<script src="http://robksawyer.com/js/synthfilter.utils.js" type="text/javascript"></script>
<link href='http://fonts.googleapis.com/css?family=Contrail+One|Fjord+One' rel='stylesheet' type='text/css'>
<style type="text/css">
    body{
        font-family: sans-serif;
        color: #666666;
    }
    h1,h2,h3,h4,th {
        font-family: 'Fjord One', serif;
        color: #000000;
    }
    a{ color: #000000; }
    #content{
        position: relative;
        margin:0 auto;
        padding: 0;
        width: 100%;
    }
    div.synth-container{
        margin: 0 auto;
        text-align:left;
    }
    div.synth-container div.item{
        display: block;
        position: relative;
        float: left;
        clear: none;
    }
    div.synth-container div.item img{
        height: 150px; 
        width: auto;
        max-width: 200px;
    }
    div.pager{
        position: relative;
        clear: both;
        margin: 100px 0 0 0;
        font-size: 20px;
        text-align: center;
    }
    div.pager a:first-child{ margin-right: 75px; }
    a.disabled{ color: #e7e7e7; }
    .tip {
        color: #fff;
        background:#1d1d1d;
        display:none; /*--Hides by default--*/
        padding:10px;
        position:absolute;
        z-index:1000;
        -webkit-border-radius: 15px;
        -moz-border-radius: 15px;
        border-radius: 15px;
        max-width: 400px;
    }
    .tip ul { margin: 0; padding: 0; text-align:center; }
    .tip ul li{ list-style-type: none; padding: 0; margin: 0; }
    .tip ul li.synth_name { font-size: 20px; }
    .tip ul li.price { font-size: 16px; padding: 5px; color: green; }
    .tip ul li.date { font-size: 14px; color: #e7e7e7; text-align: right; }
    .tip ul li.description { font-size: 14px; color: #e7e7e7; text-align: left; padding-bottom: 15px; }
</style>
<div id="content">
    <h1 align='center'>Audio Interfaces - Northwest Craigslist</h1>
    <div class='synth-container'>
    <?php
    //scraperwiki::attach('synthfilter_utils');
    //$manufacturers = scraperwiki::get_var('manufacturers');
    //$manufacturers = explode(',',$manufacturers); //Convert to array
    
    if(!empty($_GET['start'])) $start = $_GET['start']; // To take care global variable if OFF
    if(empty($start)){
        $start = 0;
    }
    if(strlen($start) > 0 and !is_numeric($start)){
        //echo "Data Error";
        //exit;
        $start = 0;
    }
    
    $sourcescraper = 'nw_audio_interface_scraper';
    scraperwiki::attach($sourcescraper);
    $recordCount = scraperwiki::sqliteexecute("SELECT count(*) FROM $sourcescraper.swdata");
    $recordCount = $recordCount->data[0][0];
    //echo "Total Records: ".$recordCount."\n";
    
    $totalPages = ceil($recordCount/$limit);
    
    //Make sure that the user doesn't pass go.
    if($start > $recordCount){
        if($recordCount > $limit) $start = $recordCount-$limit;
        else $start = $limit-$recordCount;
    }
    
    $eu = ($start - 0);
    $current = $eu;
    $back = $current - $limit;
    if($back < 0) $back = 0;
    $next = $eu + $limit;
    if($next > $recordCount){
        $next = 0;
    }
    
    try {
        //https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=oregon_craigslist_synth_collector&query=select%20*%20from%20%60swdata%60%20limit%2010%2C10
        $data = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=$sourcescraper&query=select%20*%20from%20%60swdata%60%20limit%20$start%2C$limit");
        if(!empty($data)){
            $dataDecoded = json_decode($data);
            //print_r($dataDecoded);
            if(!empty($dataDecoded)){
                if(!isset($dataDecoded->error)){
                    buildTable($dataDecoded);
                }else{
                    //echo $dataDecoded->error;
                }
            }
        }
    }catch(Exception $e){
        //echo "There is no data for this manufacturer.<br/>";
    }
    
    function buildTable($data){
        //print "<tr><th></th><th>Post</th><th>Synth</th><th>Item price</th><th>Item date</th>";
        $counter = 0;
        foreach($data as $d){
            $imageSources = $d->post_item_images;
            print "<div class='item'>";
            if(!empty($imageSources)){
                $imageSources = explode(',',$imageSources);
                foreach($imageSources as $imgSrc){
                    //$size = getimagesize($imgSrc);
                    print "<a href='".$d->link."' target='_blank' class='tip_trigger' id='tooltip_".$counter."'>";
                    print "<img src='".$imgSrc."'/>";
                    print "<span id='data_tooltip_".$counter."' class='tip'>";
                    print "<ul>";
                    print "<li class='synth_name'>".$d->post_item_name."</li>";
                    print "<li class='synth_searched'>Item query: ".$d->name."</li>";
                    print "<li class='manufacturer'>Manufacturer query: ".$d->manufacturer."</li>";
                    print "<li class='location'>".$d->post_item_link."</li>";
                    print "<li class='price'>".$d->post_item_price."</li>";
                    print "<li class='description'>".myTruncate(strval($d->post_item_description),300)."</li>";
                    print "<li class='click'>Click the image to read more.</li>";
                    print "<li class='date'>".$d->post_item_date."</li>";
                    print "</ul>";
                    print "</span>";
                    print "</a>";
                    $counter++;
                }
            }
            print "</div>";
        }
    }
    ?>
    </div>
    <div class="pager">
        <?php
            if($back >= 0 && $current >= $limit){
                echo "<a href='https://views.scraperwiki.com/run/audio_interfaces_from_craigslist_across_the_northw/?start=".$back."'><< Back</a>";
            }else{
                echo "<a href='#' class='disabled'><< Back</a>";
            }
            if($next > 0){
                echo "<a href='https://views.scraperwiki.com/run/audio_interfaces_from_craigslist_across_the_northw/?start=".$next."'>Next >></a>";
            }else{
                echo "<a href='#' class='disabled'>Next >></a>";
            }
        ?>
    </div>
</div><?php
    $limit = 100; // No of records to be shown per page.
    
    function myTruncate($string, $limit, $break=".", $pad="..."){
      // return with no change if string is shorter than $limit
      if(strlen($string) <= $limit) return $string;
    
      // is $break present between $limit and the end of the string?
      if(false !== ($breakpoint = strpos($string, $break, $limit))) {
        if($breakpoint < strlen($string) - 1) {
          $string = substr($string, 0, $breakpoint) . $pad;
        }
      }
        
      return $string;
    }

?>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.0/jquery.min.js" type="text/javascript"></script>
<script src="http://robksawyer.com/js/jquery.masonry.min.js" type="text/javascript"></script>
<script src="http://robksawyer.com/js/modernizr-transitions.js" type="text/javascript"></script>
<script src="http://robksawyer.com/js/synthfilter.utils.js" type="text/javascript"></script>
<link href='http://fonts.googleapis.com/css?family=Contrail+One|Fjord+One' rel='stylesheet' type='text/css'>
<style type="text/css">
    body{
        font-family: sans-serif;
        color: #666666;
    }
    h1,h2,h3,h4,th {
        font-family: 'Fjord One', serif;
        color: #000000;
    }
    a{ color: #000000; }
    #content{
        position: relative;
        margin:0 auto;
        padding: 0;
        width: 100%;
    }
    div.synth-container{
        margin: 0 auto;
        text-align:left;
    }
    div.synth-container div.item{
        display: block;
        position: relative;
        float: left;
        clear: none;
    }
    div.synth-container div.item img{
        height: 150px; 
        width: auto;
        max-width: 200px;
    }
    div.pager{
        position: relative;
        clear: both;
        margin: 100px 0 0 0;
        font-size: 20px;
        text-align: center;
    }
    div.pager a:first-child{ margin-right: 75px; }
    a.disabled{ color: #e7e7e7; }
    .tip {
        color: #fff;
        background:#1d1d1d;
        display:none; /*--Hides by default--*/
        padding:10px;
        position:absolute;
        z-index:1000;
        -webkit-border-radius: 15px;
        -moz-border-radius: 15px;
        border-radius: 15px;
        max-width: 400px;
    }
    .tip ul { margin: 0; padding: 0; text-align:center; }
    .tip ul li{ list-style-type: none; padding: 0; margin: 0; }
    .tip ul li.synth_name { font-size: 20px; }
    .tip ul li.price { font-size: 16px; padding: 5px; color: green; }
    .tip ul li.date { font-size: 14px; color: #e7e7e7; text-align: right; }
    .tip ul li.description { font-size: 14px; color: #e7e7e7; text-align: left; padding-bottom: 15px; }
</style>
<div id="content">
    <h1 align='center'>Audio Interfaces - Northwest Craigslist</h1>
    <div class='synth-container'>
    <?php
    //scraperwiki::attach('synthfilter_utils');
    //$manufacturers = scraperwiki::get_var('manufacturers');
    //$manufacturers = explode(',',$manufacturers); //Convert to array
    
    if(!empty($_GET['start'])) $start = $_GET['start']; // To take care global variable if OFF
    if(empty($start)){
        $start = 0;
    }
    if(strlen($start) > 0 and !is_numeric($start)){
        //echo "Data Error";
        //exit;
        $start = 0;
    }
    
    $sourcescraper = 'nw_audio_interface_scraper';
    scraperwiki::attach($sourcescraper);
    $recordCount = scraperwiki::sqliteexecute("SELECT count(*) FROM $sourcescraper.swdata");
    $recordCount = $recordCount->data[0][0];
    //echo "Total Records: ".$recordCount."\n";
    
    $totalPages = ceil($recordCount/$limit);
    
    //Make sure that the user doesn't pass go.
    if($start > $recordCount){
        if($recordCount > $limit) $start = $recordCount-$limit;
        else $start = $limit-$recordCount;
    }
    
    $eu = ($start - 0);
    $current = $eu;
    $back = $current - $limit;
    if($back < 0) $back = 0;
    $next = $eu + $limit;
    if($next > $recordCount){
        $next = 0;
    }
    
    try {
        //https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=oregon_craigslist_synth_collector&query=select%20*%20from%20%60swdata%60%20limit%2010%2C10
        $data = file_get_contents("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=$sourcescraper&query=select%20*%20from%20%60swdata%60%20limit%20$start%2C$limit");
        if(!empty($data)){
            $dataDecoded = json_decode($data);
            //print_r($dataDecoded);
            if(!empty($dataDecoded)){
                if(!isset($dataDecoded->error)){
                    buildTable($dataDecoded);
                }else{
                    //echo $dataDecoded->error;
                }
            }
        }
    }catch(Exception $e){
        //echo "There is no data for this manufacturer.<br/>";
    }
    
    function buildTable($data){
        //print "<tr><th></th><th>Post</th><th>Synth</th><th>Item price</th><th>Item date</th>";
        $counter = 0;
        foreach($data as $d){
            $imageSources = $d->post_item_images;
            print "<div class='item'>";
            if(!empty($imageSources)){
                $imageSources = explode(',',$imageSources);
                foreach($imageSources as $imgSrc){
                    //$size = getimagesize($imgSrc);
                    print "<a href='".$d->link."' target='_blank' class='tip_trigger' id='tooltip_".$counter."'>";
                    print "<img src='".$imgSrc."'/>";
                    print "<span id='data_tooltip_".$counter."' class='tip'>";
                    print "<ul>";
                    print "<li class='synth_name'>".$d->post_item_name."</li>";
                    print "<li class='synth_searched'>Item query: ".$d->name."</li>";
                    print "<li class='manufacturer'>Manufacturer query: ".$d->manufacturer."</li>";
                    print "<li class='location'>".$d->post_item_link."</li>";
                    print "<li class='price'>".$d->post_item_price."</li>";
                    print "<li class='description'>".myTruncate(strval($d->post_item_description),300)."</li>";
                    print "<li class='click'>Click the image to read more.</li>";
                    print "<li class='date'>".$d->post_item_date."</li>";
                    print "</ul>";
                    print "</span>";
                    print "</a>";
                    $counter++;
                }
            }
            print "</div>";
        }
    }
    ?>
    </div>
    <div class="pager">
        <?php
            if($back >= 0 && $current >= $limit){
                echo "<a href='https://views.scraperwiki.com/run/audio_interfaces_from_craigslist_across_the_northw/?start=".$back."'><< Back</a>";
            }else{
                echo "<a href='#' class='disabled'><< Back</a>";
            }
            if($next > 0){
                echo "<a href='https://views.scraperwiki.com/run/audio_interfaces_from_craigslist_across_the_northw/?start=".$next."'>Next >></a>";
            }else{
                echo "<a href='#' class='disabled'>Next >></a>";
            }
        ?>
    </div>
</div>