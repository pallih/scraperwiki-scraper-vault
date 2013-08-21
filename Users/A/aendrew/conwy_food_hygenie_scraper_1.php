<?php
require 'scraperwiki/simple_html_dom.php';  
date_default_timezone_set("Europe/London");
    
    $pageurl = "http://ratings.food.gov.uk/search/en-GB?refla=ZdK3h76%2f0Ns%3d&sm=1&st=1&pi=0&las=333";
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
            echo $cols; exit;
//            $data['id'][] = $cols[0]->find('input', 0)->value;
//            $data['name'][] = $cols[0]->find('.resultName', 0)->plaintext;
            $data['url'][] = $cols->first_child()->find('div.resultName a')->href; print_r($data); exit;
            $data['address'][] = trim($cols[0]->find('.resultAddress', 0)->plaintext);
            $data['postcode'][] = trim($cols[0]->find('.resultPostcode', 0)->plaintext);
//            $stars = sscanf($cols[1]->find('img', 0)->alt, "Food hygiene rating is &#39;%d&#39;");
            //$stars = str_replace("images/scores/", "", $cols[1]->find('img', 0)->src);
  //          $stars = $stars[0];
            print_r($data);
            if (!is_numeric($stars)) {
                $stars = "Exempt";
            }

      /*      $premhtml = scraperWiki::scrape($url);                    
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
        */
        }

?>