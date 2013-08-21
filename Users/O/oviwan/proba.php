<?php
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.movildinero.es/buscar-moviles?orderby=price&orderway=desc&search_query=acer");
$html = str_get_html($html_content);
foreach ($html->find("div.center_block,div.right_block p.product_desc,span.price") as $el) {
    print $el->innertext . "\n";

}



?>
