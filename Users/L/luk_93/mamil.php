<?php
require  'scraperwiki/simple_html_dom.php';


//MUSEUM
/*

//museum
for($i=764; $i<=49; $i++){
    print $i."\n";
 $html = scraperwiki::scrape("http://www.mamilade.de/kinder/2006700-4---1317074400-$i-1324941496.html");

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);
*/

//gastro
for($i=1; $i<=765; $i++){
    print $i."\n";
 $html = scraperwiki::scrape("http://www.mamilade.de/gastronomie/2024700-4---1317074400-$i-1324976513.html");

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);



//LINK

foreach($dom->find('a.headline400') as $name){
        # Store data in the datastore
             $name = $name->href;
           //print $name. "\n";
    scraperwiki::save(array('Link'), array('Link' => $name));

      }




}
?>
