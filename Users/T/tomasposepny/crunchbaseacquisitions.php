<?php

require 'scraperwiki/simple_html_dom.php';   

for ($i=1; $i<=15; $i++) {       
    $html_content = scraperwiki::scrape("http://www.crunchbase.com/acquisitions?page=" . $i);
    $html = str_get_html($html_content);
    
    $posts_array = $html->find("div#col2_internal > table > tbody > tr");
    
    foreach($posts_array as $post) {
        $post_cells = $post->find("td");
        $date = $post_cells[0]->plaintext;
        $target = trim($post_cells[1]->plaintext);
        $target_web = $post_cells[1]->find("a",0)->href;
        $acquirer = trim($post_cells[2]->plaintext);
        $acquirer_web = $post_cells[2]->find("a",0)->href;
        $price = trim($post_cells[3]->plaintext);
    
        $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $target_web);
        $detail_html = str_get_html($html_content);
        $target_twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
        if(isset($target_twitter)) {
            $target_twitter = trim($target_twitter->plaintext);
        }
    
        $target_category = null;
        $target_rows = $detail_html->find("tr > td.td_left");
        foreach($target_rows as $row) {
            if($row->plaintext === "Category") {
                $target_category = trim($row->nextSibling()->plaintext);    
            }
        }
    
        $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $acquirer_web);
        $detail_html = str_get_html($html_content);
        $acquirer_twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
        if(isset($acquirer_twitter)) {
            $acquirer_twitter = trim($acquirer_twitter->plaintext);
        }   
    
        $acquirer_category = null;
        $acquirer_rows = $detail_html->find("tr > td.td_left");
        foreach($acquirer_rows as $row) {
            if($row->plaintext === "Category") {
                $acquirer_category = trim($row->nextSibling()->plaintext);    
            }
        }

        //prepare tweet text
        $tweet_text = null;
        if(!is_null($acquirer_twitter) || !is_null($target_twitter)) {
            $tweet_text = $acquirer 
            . (is_null($acquirer_twitter) ? "" : (" - " . $acquirer_twitter . " -")) 
            . " acquired " . ($target_twitter ?: $target) 
            . " for " . ((is_null($price) || $price === "N/A") ? "an undisclosed price" : $price) 
            . (is_null($target_category) ? "" : (" #".$target_category)) . " #acquisition";  
        }
        
        
        $acquisition = array('date' => $date, 
                             'target' => $target, 
                             'target_twitter' => $target_twitter, 
                             'acquirer' => $acquirer, 
                             'acquirer_twitter' => $acquirer_twitter, 
                             'price' => $price, 
                             'target_category' => $target_category, 
                             'acquirer_category' => $acquirer_category, 
                             'tweet' => $tweet_text);
        
        scraperwiki::save(array("date", "target", "acquirer"), $acquisition);           
    }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';   

for ($i=1; $i<=15; $i++) {       
    $html_content = scraperwiki::scrape("http://www.crunchbase.com/acquisitions?page=" . $i);
    $html = str_get_html($html_content);
    
    $posts_array = $html->find("div#col2_internal > table > tbody > tr");
    
    foreach($posts_array as $post) {
        $post_cells = $post->find("td");
        $date = $post_cells[0]->plaintext;
        $target = trim($post_cells[1]->plaintext);
        $target_web = $post_cells[1]->find("a",0)->href;
        $acquirer = trim($post_cells[2]->plaintext);
        $acquirer_web = $post_cells[2]->find("a",0)->href;
        $price = trim($post_cells[3]->plaintext);
    
        $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $target_web);
        $detail_html = str_get_html($html_content);
        $target_twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
        if(isset($target_twitter)) {
            $target_twitter = trim($target_twitter->plaintext);
        }
    
        $target_category = null;
        $target_rows = $detail_html->find("tr > td.td_left");
        foreach($target_rows as $row) {
            if($row->plaintext === "Category") {
                $target_category = trim($row->nextSibling()->plaintext);    
            }
        }
    
        $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $acquirer_web);
        $detail_html = str_get_html($html_content);
        $acquirer_twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
        if(isset($acquirer_twitter)) {
            $acquirer_twitter = trim($acquirer_twitter->plaintext);
        }   
    
        $acquirer_category = null;
        $acquirer_rows = $detail_html->find("tr > td.td_left");
        foreach($acquirer_rows as $row) {
            if($row->plaintext === "Category") {
                $acquirer_category = trim($row->nextSibling()->plaintext);    
            }
        }

        //prepare tweet text
        $tweet_text = null;
        if(!is_null($acquirer_twitter) || !is_null($target_twitter)) {
            $tweet_text = $acquirer 
            . (is_null($acquirer_twitter) ? "" : (" - " . $acquirer_twitter . " -")) 
            . " acquired " . ($target_twitter ?: $target) 
            . " for " . ((is_null($price) || $price === "N/A") ? "an undisclosed price" : $price) 
            . (is_null($target_category) ? "" : (" #".$target_category)) . " #acquisition";  
        }
        
        
        $acquisition = array('date' => $date, 
                             'target' => $target, 
                             'target_twitter' => $target_twitter, 
                             'acquirer' => $acquirer, 
                             'acquirer_twitter' => $acquirer_twitter, 
                             'price' => $price, 
                             'target_category' => $target_category, 
                             'acquirer_category' => $acquirer_category, 
                             'tweet' => $tweet_text);
        
        scraperwiki::save(array("date", "target", "acquirer"), $acquisition);           
    }
}

?>
