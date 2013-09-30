<?php

require 'scraperwiki/simple_html_dom.php';

$html = file_get_html('http://www.crackle.com/shows/shows.aspx?cl=o%3D2%26fa%3D82%26fs%3D%26fab%3D%26fg%3D%26fry%3D&st=a&fb=f&p=0');

foreach($html->find('div.thumbnail a') as $element) {
    $movieTitle = $element->title;
    $movieUrl = 'http://www.crackle.com' . $element->href;
    echo $movieTitle . ' ' . $movieUrl . '<br>';
    }

?>
<?php

require 'scraperwiki/simple_html_dom.php';

$html = file_get_html('http://www.crackle.com/shows/shows.aspx?cl=o%3D2%26fa%3D82%26fs%3D%26fab%3D%26fg%3D%26fry%3D&st=a&fb=f&p=0');

foreach($html->find('div.thumbnail a') as $element) {
    $movieTitle = $element->title;
    $movieUrl = 'http://www.crackle.com' . $element->href;
    echo $movieTitle . ' ' . $movieUrl . '<br>';
    }

?>
