<?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape('http://www.weihnachtsmaerkte-in-deutschland.de/thueringen.html');

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);


foreach($dom->find('div#centerblock li a') as $name){
         # Store data in the datastore
         $name=$name->href;
         print $name."\n";

scraperwiki::save(array('name'), array('name' => $name));

}



?>
<?php
require  'scraperwiki/simple_html_dom.php';

$html = scraperwiki::scrape('http://www.weihnachtsmaerkte-in-deutschland.de/thueringen.html');

    # Use the PHP Simple HTML DOM Parser to extract <td> tags
    $dom = new simple_html_dom();
    $dom->load($html);


foreach($dom->find('div#centerblock li a') as $name){
         # Store data in the datastore
         $name=$name->href;
         print $name."\n";

scraperwiki::save(array('name'), array('name' => $name));

}



?>
