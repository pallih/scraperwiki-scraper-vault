<?php

require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("linkshare.co.uk");
 $es = $html->find('omniture');
?>
