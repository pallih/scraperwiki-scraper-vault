<?php
    require  'scraperwiki/simple_html_dom.php';
    
    $outerhtml = scraperwiki::scrape("http://www.caa.co.uk/default.aspx?catid=80&pagetype=88&pageid=3&sglid=3#Data");
    $outerdom = new simple_html_dom();
    $outerdom->load($outerhtml);

    foreach($outerdom->find('.datatable a') as $outerdata) {

        $outerdata->href = str_replace("default.aspx?catid=80&amp;pagetype=88&amp;sglid=3&amp;fld=","",$outerdata->href);

        $html = scraperwiki::scrape("http://www.caa.co.uk/default.aspx?catid=80&pagetype=88&sglid=3&fld=".$outerdata->href);
 
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find('.datatable') as $datapage) {

            foreach($datapage->find('a') as $page) {
                
                if (stripos($page, ".csv") !== false) {
                    //print $page->href;
                    
                    $data = scraperWiki::scrape("http://www.caa.co.uk/".$page->href);
                    $rows = explode("\n", $data);

                    // Extract CSV header
                    $headers = str_getcsv(array_shift($rows));

                    $sql = "create table if not exists swdata ($headers)";
                    print($sql);

                    scraperwiki::sqliteexecute($sql);
                    print_r($headers);
            
                    foreach($rows as $row) {
                        print_r($rows);
                        $row = str_getcsv($row);
                        //print_r(scraperwiki::show_tables());
                        //scraperwiki::save_sqlite(array("header"),array("header"=>1, "data"=>"Hi there")); 
                        //scraperwiki::save(array($headers), $line);
                    }   
                    exit;
                    
                }
            }
        }
    }
    
?><?php
    require  'scraperwiki/simple_html_dom.php';
    
    $outerhtml = scraperwiki::scrape("http://www.caa.co.uk/default.aspx?catid=80&pagetype=88&pageid=3&sglid=3#Data");
    $outerdom = new simple_html_dom();
    $outerdom->load($outerhtml);

    foreach($outerdom->find('.datatable a') as $outerdata) {

        $outerdata->href = str_replace("default.aspx?catid=80&amp;pagetype=88&amp;sglid=3&amp;fld=","",$outerdata->href);

        $html = scraperwiki::scrape("http://www.caa.co.uk/default.aspx?catid=80&pagetype=88&sglid=3&fld=".$outerdata->href);
 
        $dom = new simple_html_dom();
        $dom->load($html);
    
        foreach($dom->find('.datatable') as $datapage) {

            foreach($datapage->find('a') as $page) {
                
                if (stripos($page, ".csv") !== false) {
                    //print $page->href;
                    
                    $data = scraperWiki::scrape("http://www.caa.co.uk/".$page->href);
                    $rows = explode("\n", $data);

                    // Extract CSV header
                    $headers = str_getcsv(array_shift($rows));

                    $sql = "create table if not exists swdata ($headers)";
                    print($sql);

                    scraperwiki::sqliteexecute($sql);
                    print_r($headers);
            
                    foreach($rows as $row) {
                        print_r($rows);
                        $row = str_getcsv($row);
                        //print_r(scraperwiki::show_tables());
                        //scraperwiki::save_sqlite(array("header"),array("header"=>1, "data"=>"Hi there")); 
                        //scraperwiki::save(array($headers), $line);
                    }   
                    exit;
                    
                }
            }
        }
    }
    
?>