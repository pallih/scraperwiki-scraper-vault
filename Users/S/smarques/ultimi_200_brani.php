<?php
# Blank PHP
$cb = '';
if(isset( $_GET['callback']))
$cb = $_GET['callback'];
if(!$cb)$cb = 'callback';
$sourcescraper = 'battiti';
scraperwiki::attach("battiti");   
$data = scraperwiki::select(           
    "* from battiti.swdata 
    order by date desc limit 200"
);
echo $cb.'('.json_encode($data).')';
?>
<?php
# Blank PHP
$cb = '';
if(isset( $_GET['callback']))
$cb = $_GET['callback'];
if(!$cb)$cb = 'callback';
$sourcescraper = 'battiti';
scraperwiki::attach("battiti");   
$data = scraperwiki::select(           
    "* from battiti.swdata 
    order by date desc limit 200"
);
echo $cb.'('.json_encode($data).')';
?>
