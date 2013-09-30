<?php
require 'scraperwiki/simple_html_dom.php';  
    
    $pageurl = "http://ratings.food.gov.uk/advanced-search/en-US?st=1&pi=0&las=336";
    $html = scraperWiki::scrape($pageurl);                    
    $dom = new simple_html_dom();
    $dom->load($html);

    # Get number of pages
    
    $searchSummary = $dom->find('#searchSummary');
    
    $nums = explode("returned", $searchSummary[0]->plaintext);
    $num = trim(str_replace(" items.", "", $nums[1]));
    $pages = $num / 10;
    $pages = round($pages);

    # Get first page of results
    
    $rows = $dom->find('.uxMainResults tr');
    
    $numrows=count($rows);
    $numrow = $numrows;
    while ($numrow > $numrows/2-1){
            unset($rows[$numrow]);
            $numrow--;
            }

    unset($rows[0]);


        foreach ($rows as $row) {
            $cols = $row->find('td'); 
            $id = $cols[0]->find('input', 0)->value;
            $name = trim($cols[0]->find('.resultName', 0)->plaintext);
            $url = $cols[0]->find('.resultName', 0)->find('a', 0)->href;
            $address = trim($cols[0]->find('.resultAddress', 0)->plaintext);
            $postcode = trim($cols[0]->find('.resultPostcode', 0)->plaintext);
            $stars = sscanf($cols[1]->find('img', 0)->src, "../App_Themes/default/images/scores/small/sfhrsweb%d.jpg");

            
           
            $prem = array (
                'id' => $id,
                'name' => $name,
                'address' => $address,
                'postcode' => $postcode,
                'url' => $url,
                'rating' => $stars[0]
                );

            
             scraperwiki::save_sqlite(array('id'), $prem);
            

        
        }

    # Check if there's more than one page
    
    if ($pages > 1) {

        $page = 1;

        # Get the viewstate and event validation hidden form elements
        # (For some mad reason, pagination is done via a POST form)

        $viewstate = $dom->find('#__VIEWSTATE', 0)->value;
        $eventvalidation = $dom->find('#__EVENTVALIDATION', 0)->value;
        
        while ($page <= $pages) {

        # Load the next page via cURL

        $ch = curl_init($pageurl);

        $postdata = "__VIEWSTATE=". urlencode($viewstate) ."&__EVENTVALIDATION=". urlencode($eventvalidation) ."&ctl00%24ContentPlaceHolder1%24uxResults%24lnkNext=Next+%3E&ctl00%24ContentPlaceHolder1%24uxResults%24txtPagerGotoPage=1&ctl00%24ContentPlaceHolder1%24hiddenDialogClose=Close";

        curl_setopt($ch, CURLOPT_HEADER, 0); 
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $postdata);

        $html = curl_exec($ch);

        
        curl_close($ch); 
                
        $dom = new simple_html_dom();
        $dom->load($html);

        # Get the next lot of results

        $rows = $dom->find('.uxMainResults tr');
    
        $numrows=count($rows);
        $numrow = $numrows;
        while ($numrow > $numrows/2-1){
            unset($rows[$numrow]);
            $numrow--;
            }
        
        unset($rows[0]);
    
        foreach ($rows as $row) {
            $cols = $row->find('td');
            $id = $cols[0]->find('input', 0)->value;
            $name = trim($cols[0]->find('.resultName', 0)->plaintext);
            $url = $cols[0]->find('.resultName', 0)->find('a', 0)->href;
            $address = trim($cols[0]->find('.resultAddress', 0)->plaintext);
            $postcode = trim($cols[0]->find('.resultPostcode', 0)->plaintext);
            $stars = sscanf($cols[1]->find('img', 0)->src, "../App_Themes/default/images/scores/small/sfhrsweb%d.jpg");
            
           
            $prem = array (
                'id' => $id,
                'name' => $name,
                'address' => $address,
                'postcode' => $postcode,
                'url' => $url,
                'rating' => $stars[0]
               
            );
            
            scraperwiki::save(array('id'), $prem);
        
        }

        # Those pesky form elements again!

        $viewstate = $dom->find('#__VIEWSTATE', 0)->value;
        $eventvalidation = $dom->find('#__EVENTVALIDATION', 0)->value;

        $page++;
        }
    
    }
?>
<?php
require 'scraperwiki/simple_html_dom.php';  
    
    $pageurl = "http://ratings.food.gov.uk/advanced-search/en-US?st=1&pi=0&las=336";
    $html = scraperWiki::scrape($pageurl);                    
    $dom = new simple_html_dom();
    $dom->load($html);

    # Get number of pages
    
    $searchSummary = $dom->find('#searchSummary');
    
    $nums = explode("returned", $searchSummary[0]->plaintext);
    $num = trim(str_replace(" items.", "", $nums[1]));
    $pages = $num / 10;
    $pages = round($pages);

    # Get first page of results
    
    $rows = $dom->find('.uxMainResults tr');
    
    $numrows=count($rows);
    $numrow = $numrows;
    while ($numrow > $numrows/2-1){
            unset($rows[$numrow]);
            $numrow--;
            }

    unset($rows[0]);


        foreach ($rows as $row) {
            $cols = $row->find('td'); 
            $id = $cols[0]->find('input', 0)->value;
            $name = trim($cols[0]->find('.resultName', 0)->plaintext);
            $url = $cols[0]->find('.resultName', 0)->find('a', 0)->href;
            $address = trim($cols[0]->find('.resultAddress', 0)->plaintext);
            $postcode = trim($cols[0]->find('.resultPostcode', 0)->plaintext);
            $stars = sscanf($cols[1]->find('img', 0)->src, "../App_Themes/default/images/scores/small/sfhrsweb%d.jpg");

            
           
            $prem = array (
                'id' => $id,
                'name' => $name,
                'address' => $address,
                'postcode' => $postcode,
                'url' => $url,
                'rating' => $stars[0]
                );

            
             scraperwiki::save_sqlite(array('id'), $prem);
            

        
        }

    # Check if there's more than one page
    
    if ($pages > 1) {

        $page = 1;

        # Get the viewstate and event validation hidden form elements
        # (For some mad reason, pagination is done via a POST form)

        $viewstate = $dom->find('#__VIEWSTATE', 0)->value;
        $eventvalidation = $dom->find('#__EVENTVALIDATION', 0)->value;
        
        while ($page <= $pages) {

        # Load the next page via cURL

        $ch = curl_init($pageurl);

        $postdata = "__VIEWSTATE=". urlencode($viewstate) ."&__EVENTVALIDATION=". urlencode($eventvalidation) ."&ctl00%24ContentPlaceHolder1%24uxResults%24lnkNext=Next+%3E&ctl00%24ContentPlaceHolder1%24uxResults%24txtPagerGotoPage=1&ctl00%24ContentPlaceHolder1%24hiddenDialogClose=Close";

        curl_setopt($ch, CURLOPT_HEADER, 0); 
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $postdata);

        $html = curl_exec($ch);

        
        curl_close($ch); 
                
        $dom = new simple_html_dom();
        $dom->load($html);

        # Get the next lot of results

        $rows = $dom->find('.uxMainResults tr');
    
        $numrows=count($rows);
        $numrow = $numrows;
        while ($numrow > $numrows/2-1){
            unset($rows[$numrow]);
            $numrow--;
            }
        
        unset($rows[0]);
    
        foreach ($rows as $row) {
            $cols = $row->find('td');
            $id = $cols[0]->find('input', 0)->value;
            $name = trim($cols[0]->find('.resultName', 0)->plaintext);
            $url = $cols[0]->find('.resultName', 0)->find('a', 0)->href;
            $address = trim($cols[0]->find('.resultAddress', 0)->plaintext);
            $postcode = trim($cols[0]->find('.resultPostcode', 0)->plaintext);
            $stars = sscanf($cols[1]->find('img', 0)->src, "../App_Themes/default/images/scores/small/sfhrsweb%d.jpg");
            
           
            $prem = array (
                'id' => $id,
                'name' => $name,
                'address' => $address,
                'postcode' => $postcode,
                'url' => $url,
                'rating' => $stars[0]
               
            );
            
            scraperwiki::save(array('id'), $prem);
        
        }

        # Those pesky form elements again!

        $viewstate = $dom->find('#__VIEWSTATE', 0)->value;
        $eventvalidation = $dom->find('#__EVENTVALIDATION', 0)->value;

        $page++;
        }
    
    }
?>
