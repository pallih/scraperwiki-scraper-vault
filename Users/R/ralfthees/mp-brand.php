<?php

$html = scraperWiki::scrape("www.mainpost.de/archiv/?gs[parameter][searchfield]=brand&gs[autostart]=true&gs[parameter][date][fromday]=3&gs[parameter][date][frommonth]=4&gs[parameter][date][fromyear]=2011&gs[parameter][date][today]=3&gs[parameter][date][tomonth]=4&gs[parameter][date][toyear]=2011&gs[parameter][pluginselect][lucenediaserienarchiv]=0&gs[parameter][pluginselect][lucenestreamsetarchiv]=0&gs[parameter][pluginselect][luceneepaperarchiv]=0");


require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();
$dom->load($html);
$datum=$dom->find('.content-body',0);
print_r($datum);

?>