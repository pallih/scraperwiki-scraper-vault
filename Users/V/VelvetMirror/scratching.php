<?php

$html = scraperWiki::scrape("<html><head></head><body>Alimentação</body></html>");           

require 'scraperwiki/simple_html_dom.php';           
$dom = new simple_html_dom();
$dom->load($html);

