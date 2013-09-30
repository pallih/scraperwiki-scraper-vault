<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.quotationspage.com/quotes/Albert_Einstein/");
$html = str_get_html($html_content);

foreach ($html->find("dt.quote a") as $el) {           
    print $el . "\n";
}

?>
<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';
$html_content = scraperwiki::scrape("http://www.quotationspage.com/quotes/Albert_Einstein/");
$html = str_get_html($html_content);

foreach ($html->find("dt.quote a") as $el) {           
    print $el . "\n";
}

?>
