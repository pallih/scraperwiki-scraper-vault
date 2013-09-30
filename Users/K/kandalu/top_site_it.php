

<?php
require 'scraperwiki/simple_html_dom.php';

function topSites(){
    $page = 0;
    $country = 'IT';
    $limit = 20;
    $count = 0;

    while($limit > $page){
        $html = scraperWiki::scrape("http://www.alexa.com/topsites/countries;" . $page . "/" . $country);
        $dom = new simple_html_dom();
        $dom->load($html);
        foreach($dom->find("span[class=topsites-label]") as $data){
            $record = array( 
                'site' => $data->plaintext
            );
            scraperwiki::save(array('site'), $record);
            $count++;
        }
        ++$page;
    }
    print $count;
}

topSites();

?>




<?php
require 'scraperwiki/simple_html_dom.php';

function topSites(){
    $page = 0;
    $country = 'IT';
    $limit = 20;
    $count = 0;

    while($limit > $page){
        $html = scraperWiki::scrape("http://www.alexa.com/topsites/countries;" . $page . "/" . $country);
        $dom = new simple_html_dom();
        $dom->load($html);
        foreach($dom->find("span[class=topsites-label]") as $data){
            $record = array( 
                'site' => $data->plaintext
            );
            scraperwiki::save(array('site'), $record);
            $count++;
        }
        ++$page;
    }
    print $count;
}

topSites();

?>


