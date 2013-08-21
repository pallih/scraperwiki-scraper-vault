<?php
    require  'scraperwiki/simple_html_dom.php';
    
    $outerhtml = scraperwiki::scrape("http://www.sabmiller.com/index.asp?pageid=315");
    $outerdom = new simple_html_dom();
    $outerdom->load($outerhtml);

    print($outerdom);

    foreach($outerdom->find('.dtableData') as $outerdata) {

        print("2");

        foreach($outerdata->find('td') as $data) {
                
            
            
        }
    }
    
?>