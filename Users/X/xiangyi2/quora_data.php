<?php

# Blank PHP
    
require 'scraperwiki/simple_html_dom.php';
$i = 1;
$html = scraperWiki::scrape("http://www.quora.com/Placerville-CA/What-is-nightlife-like-in-Placerville-CA");
scraperWiki::save(array('id'=>$i),array('id'=>$i,'html'=>$html ->outertext));

?>
<?php

# Blank PHP
    
require 'scraperwiki/simple_html_dom.php';
$i = 1;
$html = scraperWiki::scrape("http://www.quora.com/Placerville-CA/What-is-nightlife-like-in-Placerville-CA");
scraperWiki::save(array('id'=>$i),array('id'=>$i,'html'=>$html ->outertext));

?>
