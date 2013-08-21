<?php

require 'scraperwiki/simple_html_dom.php';

$html_content = scraperwiki::scrape('http://www.heise.de/download/top-downloads-50000505000/');
$html = str_get_html($html_content);

#$ret = $html->find('div[class=programmteaser]');



foreach ($html->find("div.programmteaser h3") as $el) {           
    print $el . "\n";
}





?>
