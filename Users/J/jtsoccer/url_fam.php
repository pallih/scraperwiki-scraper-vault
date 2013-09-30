<?php
require  'scraperwiki/simple_html_dom.php';


for($i = 284; $i<=285; $i++){
print($i."\n");

$x=($i-1)*10;

$html = scraperwiki::scrape('http://www.familion.de/index.php?option=com_sobi2&sobi2Task=search&Itemid=-1&ajax=0&limit=10&limitstart='.$x);

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);


foreach($dom->find('a.details') as $name){
         # Store data in the datastore
         $name=$name->href;
        // print $name."\n";
scraperwiki::save(array('name'), array('name' => $name));
 }



}
?>
<?php
require  'scraperwiki/simple_html_dom.php';


for($i = 284; $i<=285; $i++){
print($i."\n");

$x=($i-1)*10;

$html = scraperwiki::scrape('http://www.familion.de/index.php?option=com_sobi2&sobi2Task=search&Itemid=-1&ajax=0&limit=10&limitstart='.$x);

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);


foreach($dom->find('a.details') as $name){
         # Store data in the datastore
         $name=$name->href;
        // print $name."\n";
scraperwiki::save(array('name'), array('name' => $name));
 }



}
?>
