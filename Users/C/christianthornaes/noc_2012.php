<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.olympic.org/brazil");
$html = str_get_html($html_content); 

$ret = $html->find('mailto:');
echo $ret;






?>
<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.olympic.org/brazil");
$html = str_get_html($html_content); 

$ret = $html->find('mailto:');
echo $ret;






?>
