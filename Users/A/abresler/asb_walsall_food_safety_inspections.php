<?php
require 'scraperwiki/simple_html_dom.php';  
date_default_timezone_set("Europe/London");
    
    $pageurl = "http://ratings.food.gov.uk/advanced-search/en-US?st=1&pi=0&las=379";
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
    
    $table = $dom->find('.uxMainResults', 0);
    $rows = $table->find('tr');
    
    unset($rows[0]);

        foreach ($rows as $row) {
            $cols = $row->find('td');
        
            $id = trim($cols[0]->find('input', 0)->value);
            $name = trim($cols[0]->find('.resultName', 0)->plaintext);
            $url = html_entity_decode($cols[0]->find('.resultName', 0)->find('a', 0)->href);
            $address = trim($cols[0]->find('.resultAddress', 0)->plaintext);
            $postcode = trim($cols[0]->find('.resultPostcode', 0)->plaintext);
            $stars = sscanf($cols[1]->find('img', 0)->alt, "Food hygiene rating is &#39;%d&#39;");
            //$stars = str_replace("images/scores/", "", $cols[1]->find('img', 0)->src);
            $stars = $stars[0];

            if (!is_numeric($stars)) {
                $stars = "Exempt";
            }

            $premhtml = scraperWiki::scrape($url);                    
            $premdom = new simple_html_dom();
            $premdom->load($premhtml);

            $businesstype = $premdom->find('h1', 0)->plaintext;
            $date = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessLastInspection', 0)->plaintext;      
            $address1 = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessAddress1', 0)->plaintext;
            $address2 = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessAddress2', 0)->plaintext;
            $address3 = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessAddress3', 0)->plaintext;   
            $address4 = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessAddress4', 0)->plaintext; 

            $latlng = scraperWiki::gb_postcode_to_latlng($postcode);
            
            $prem = array (
                'id' => $id,
                'name' => html_entity_decode($name),
                'address1' => html_entity_decode($address1),
                'address2' => html_entity_decode($address2),
                'address3' => html_entity_decode($address3),
                'address4' => html_entity_decode($address4),
                'postcode' => $postcode,
                'businesstype' => $businesstype,
                'rating' => $stars,
                'url' => html_entity_decode($url),
                'rssdate' => date("r", strtotime($date))
            );

            $date = date("c", strtotime($date)); 
            
            scraperwiki::save(array('id'), $prem, $date, $latlng);  
        
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

        $postdata = "__VIEWSTATE=". urlencode($viewstate) ."&__EVENTVALIDATION=". urlencode($eventvalidation) ."&ctl00%24ContentPlaceHolder1%24uxResults%24uxNext=Next+%3E&ctl00%24ContentPlaceHolder1%24hiddenDialogClose=Close";

        curl_setopt($ch, CURLOPT_HEADER, 0); 
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $postdata);

        $html = curl_exec($ch);

        curl_close($ch); 
                
        $dom = new simple_html_dom();
        $dom->load($html);

        # Get the next lot of results

        $table = $dom->find('.uxMainResults', 0);
        $rows = $table->find('tr');   
 
        unset($rows[0]);
    
        foreach ($rows as $row) {

            $cols = $row->find('td');
        
            $id = trim($cols[0]->find('input', 0)->value);
            $name = trim($cols[0]->find('.resultName', 0)->plaintext);
            $url = html_entity_decode($cols[0]->find('.resultName', 0)->find('a', 0)->href);
            $address = trim($cols[0]->find('.resultAddress', 0)->plaintext);
            $postcode = trim($cols[0]->find('.resultPostcode', 0)->plaintext);
            $stars = sscanf($cols[1]->find('img', 0)->alt, "Food hygiene rating is &#39;%d&#39;");
            //$stars = str_replace("images/scores/", "", $cols[1]->find('img', 0)->src);
            $stars = $stars[0];

            if (!is_numeric($stars)) {
                $stars = "Exempt";
            }

            $premhtml = scraperWiki::scrape($url);                    
            $premdom = new simple_html_dom();
            $premdom->load($premhtml);

            $businesstype = $premdom->find('h1', 0)->plaintext;
            $date = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessLastInspection', 0)->plaintext;      
            $address1 = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessAddress1', 0)->plaintext;
            $address2 = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessAddress2', 0)->plaintext;
            $address3 = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessAddress3', 0)->plaintext;   
            $address4 = $premdom->find('#ctl00_ContentPlaceHolder1_uxBusinessAddress4', 0)->plaintext; 

            $latlng = scraperWiki::gb_postcode_to_latlng($postcode);
            
            $prem = array (
                'id' => $id,
                'name' => html_entity_decode($name),
                'address1' => html_entity_decode($address1),
                'address2' => html_entity_decode($address2),
                'address3' => html_entity_decode($address3),
                'address4' => html_entity_decode($address4),
                'postcode' => $postcode,
                'businesstype' => $businesstype,
                'rating' => $stars,
                'url' => html_entity_decode($url),
                'rssdate' => date("r", strtotime($date))
            );

            $date = date("c", strtotime($date)); 
            
            scraperwiki::save(array('id'), $prem, $date, $latlng);    
        
        }

        # Those pesky form elements again!

        $viewstate = $dom->find('#__VIEWSTATE', 0)->value;
        $eventvalidation = $dom->find('#__EVENTVALIDATION', 0)->value;

        $page++;
        }
    
    }
?>
