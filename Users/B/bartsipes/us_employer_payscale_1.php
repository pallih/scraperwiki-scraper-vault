    <?php
    require 'scraperwiki/simple_html_dom.php';

    scraperwiki::attach("us_employer_payscale");
                        
    $data = scraperwiki::select("* from us_employer_payscale.swdata");
    #print_r($data);


    foreach($data as $d){
        print_r(str_replace(" ", "+", $d['employer_name']));
        $sectorHtml = scraperWiki::scrape("http://www.google.com/finance?q=" . str_replace(" ", "+", $d['employer_name']));
        $sectorDom = new simple_html_dom();
        $sectorDom->load($sectorHtml);

        $sa = $sectorDom->find("a[id='sector']");
        $record = $d;
        if (sizeof($sa) >= 1) {
            $record['sector'] = $sa[0]->plaintext;
        }

        #print_r($record);
        scraperwiki::save( array( 'employer_name' ), $record );
    }
?>    <?php
    require 'scraperwiki/simple_html_dom.php';

    scraperwiki::attach("us_employer_payscale");
                        
    $data = scraperwiki::select("* from us_employer_payscale.swdata");
    #print_r($data);


    foreach($data as $d){
        print_r(str_replace(" ", "+", $d['employer_name']));
        $sectorHtml = scraperWiki::scrape("http://www.google.com/finance?q=" . str_replace(" ", "+", $d['employer_name']));
        $sectorDom = new simple_html_dom();
        $sectorDom->load($sectorHtml);

        $sa = $sectorDom->find("a[id='sector']");
        $record = $d;
        if (sizeof($sa) >= 1) {
            $record['sector'] = $sa[0]->plaintext;
        }

        #print_r($record);
        scraperwiki::save( array( 'employer_name' ), $record );
    }
?>