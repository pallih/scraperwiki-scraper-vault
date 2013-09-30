<?php

require 'scraperwiki/simple_html_dom.php';           
for( $x = 1; $x <= 1030; $x++ ){
$html_content = scraperwiki::scrape("http://sejmometr.pl/kody_pocztowe?w=&o=&k=&p=${x}");
$html = str_get_html($html_content);

    foreach ($html->find("div.ep_SA_Orzeczenie") as $el) {
          scraperwiki::save_sqlite(array("data"),array("data"=>$el->children(1)->children(0)->innertext . " " . $el->children(2)->children(0)->children(1)->innertext . " " . $el->children(2)->children(1)->children(1)->innertext));

    }
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';           
for( $x = 1; $x <= 1030; $x++ ){
$html_content = scraperwiki::scrape("http://sejmometr.pl/kody_pocztowe?w=&o=&k=&p=${x}");
$html = str_get_html($html_content);

    foreach ($html->find("div.ep_SA_Orzeczenie") as $el) {
          scraperwiki::save_sqlite(array("data"),array("data"=>$el->children(1)->children(0)->innertext . " " . $el->children(2)->children(0)->children(1)->innertext . " " . $el->children(2)->children(1)->children(1)->innertext));

    }
}
?>
