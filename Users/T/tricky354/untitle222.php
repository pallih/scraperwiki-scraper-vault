<?php
    require  'scraperwiki/simple_html_dom.php';
    
    $outerhtml = scraperwiki::scrape("https://www.google.com/fusiontables/DataSource?docid=1Ac2zaREnbywV5q-6AHNQ36Eh1jAzebBid4Zb1U4");
    $outerdom = new simple_html_dom();
    $outerdom->load($outerhtml);

    print($outerdom);

    foreach($outerdom->find('.dtableData') as $outerdata) {

        print("2");

        foreach($outerdata->find('td') as $data) {
                
            
            
        }
    }
    
?>