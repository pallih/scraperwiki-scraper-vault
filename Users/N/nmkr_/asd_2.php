<?php
require 'scraperwiki/simple_html_dom.php';

    $html_content = scraperWiki::scrape("http://www.gelbeseiten.de/branchenbuch");
    $html = str_get_html($html_content);

    //print_r($html);

    foreach ($html->find("div.float_l ul li a") as $stadt)
    {

        echo $stadt->href . "\n";
        
        $stadt_html_content = scraperWiki::scrape($stadt->href);
        $stadt_html = str_get_html($html_content);

        // Branchen aus der Stadt     


    }


?>