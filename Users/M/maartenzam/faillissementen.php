<?php
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.unizo.be/graydon_fal.jsp?pc=&naam=&pagina=0#list");
$html = str_get_html($html_content);

foreach ($html->find("div.oms li") as $el) {
    print $el . "\n";
}


?>
<?php
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.unizo.be/graydon_fal.jsp?pc=&naam=&pagina=0#list");
$html = str_get_html($html_content);

foreach ($html->find("div.oms li") as $el) {
    print $el . "\n";
}


?>
