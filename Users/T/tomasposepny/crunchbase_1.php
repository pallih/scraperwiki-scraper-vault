<?php

require 'scraperwiki/simple_html_dom.php';  
  
for ($i=1; $i<=50; $i++) {    
    
    $html_content = scraperwiki::scrape("http://www.crunchbase.com/funding-rounds?page=" . $i);
    $html = str_get_html($html_content);
    
    $posts_array = $html->find("div#col2_internal > table > tbody > tr");
    
    foreach($posts_array as $post) {
        $post_cells = $post->find("td");
        $date = $post_cells[0]->plaintext;
        $name = $post_cells[1]->plaintext;
        $name_web = $post_cells[1]->find("a", 0)->href;
        $round = trim($post_cells[2]->plaintext);
        $amount = $post_cells[3]->plaintext;
        $investors = $post_cells[4]->find("a");
        $investors_names = array();
        $investors_twitters = array();
        foreach($investors as $investor) {
            array_push($investors_names, $investor->title);
            $investor_web = $investor->href;
            $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $investor_web);
            $html = str_get_html($html_content);
            $investor_twitter = $html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
            if(isset($investor_twitter)) {
                $investor_twitter = $investor_twitter->plaintext;
                array_push($investors_twitters, $investor_twitter);
            }     
        }
    
        $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $name_web);
        $detail_html = str_get_html($html_content);
        $name_twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
        if(isset($name_twitter)) {
            $name_twitter = $name_twitter->plaintext;
        }
    
        $name_category = null;
        $target_rows = $detail_html->find("tr > td.td_left");
        foreach($target_rows as $row) {
            if($row->plaintext === "Category") {
                $name_category = $row->nextSibling()->plaintext;    
            }
        }
    
        //prepare tweet text
        $tweet_text = null;
        if(!empty($investors_names) && (!is_null($name_twitter) || !empty($investors_twitters))) {
            $tweet_text = implode(", ", $investors_names)
            . (empty($investors_twitters) ? "" : (" - " . implode(", ", $investors_twitters) . " -"))
            . " invested " . ((is_null($amount) || $amount === "N/A") ? "an undisclosed price" : $amount)
            . " in " . $round
            . " in " . ($name_twitter ?: $name)
            . (is_null($name_category) ? "" : (" #".$name_category)) . " #funding"; 
        }
        
        $tweet = array('date' => $date, 
                       'name' => $name, 
                       'name_twitter' => $name_twitter,
                       'name_category' => $name_category, 
                       'amount' => trim($amount), 
                       'investors' => implode(";", $investors_names), 
                       'investors_twitters' => implode(";", $investors_twitters), 
                       'tweet' => $tweet_text);

        scraperwiki::save(array("date", "name", "investors"), $tweet);           
    }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';  
  
for ($i=1; $i<=50; $i++) {    
    
    $html_content = scraperwiki::scrape("http://www.crunchbase.com/funding-rounds?page=" . $i);
    $html = str_get_html($html_content);
    
    $posts_array = $html->find("div#col2_internal > table > tbody > tr");
    
    foreach($posts_array as $post) {
        $post_cells = $post->find("td");
        $date = $post_cells[0]->plaintext;
        $name = $post_cells[1]->plaintext;
        $name_web = $post_cells[1]->find("a", 0)->href;
        $round = trim($post_cells[2]->plaintext);
        $amount = $post_cells[3]->plaintext;
        $investors = $post_cells[4]->find("a");
        $investors_names = array();
        $investors_twitters = array();
        foreach($investors as $investor) {
            array_push($investors_names, $investor->title);
            $investor_web = $investor->href;
            $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $investor_web);
            $html = str_get_html($html_content);
            $investor_twitter = $html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
            if(isset($investor_twitter)) {
                $investor_twitter = $investor_twitter->plaintext;
                array_push($investors_twitters, $investor_twitter);
            }     
        }
    
        $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $name_web);
        $detail_html = str_get_html($html_content);
        $name_twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
        if(isset($name_twitter)) {
            $name_twitter = $name_twitter->plaintext;
        }
    
        $name_category = null;
        $target_rows = $detail_html->find("tr > td.td_left");
        foreach($target_rows as $row) {
            if($row->plaintext === "Category") {
                $name_category = $row->nextSibling()->plaintext;    
            }
        }
    
        //prepare tweet text
        $tweet_text = null;
        if(!empty($investors_names) && (!is_null($name_twitter) || !empty($investors_twitters))) {
            $tweet_text = implode(", ", $investors_names)
            . (empty($investors_twitters) ? "" : (" - " . implode(", ", $investors_twitters) . " -"))
            . " invested " . ((is_null($amount) || $amount === "N/A") ? "an undisclosed price" : $amount)
            . " in " . $round
            . " in " . ($name_twitter ?: $name)
            . (is_null($name_category) ? "" : (" #".$name_category)) . " #funding"; 
        }
        
        $tweet = array('date' => $date, 
                       'name' => $name, 
                       'name_twitter' => $name_twitter,
                       'name_category' => $name_category, 
                       'amount' => trim($amount), 
                       'investors' => implode(";", $investors_names), 
                       'investors_twitters' => implode(";", $investors_twitters), 
                       'tweet' => $tweet_text);

        scraperwiki::save(array("date", "name", "investors"), $tweet);           
    }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';  
  
for ($i=1; $i<=50; $i++) {    
    
    $html_content = scraperwiki::scrape("http://www.crunchbase.com/funding-rounds?page=" . $i);
    $html = str_get_html($html_content);
    
    $posts_array = $html->find("div#col2_internal > table > tbody > tr");
    
    foreach($posts_array as $post) {
        $post_cells = $post->find("td");
        $date = $post_cells[0]->plaintext;
        $name = $post_cells[1]->plaintext;
        $name_web = $post_cells[1]->find("a", 0)->href;
        $round = trim($post_cells[2]->plaintext);
        $amount = $post_cells[3]->plaintext;
        $investors = $post_cells[4]->find("a");
        $investors_names = array();
        $investors_twitters = array();
        foreach($investors as $investor) {
            array_push($investors_names, $investor->title);
            $investor_web = $investor->href;
            $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $investor_web);
            $html = str_get_html($html_content);
            $investor_twitter = $html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
            if(isset($investor_twitter)) {
                $investor_twitter = $investor_twitter->plaintext;
                array_push($investors_twitters, $investor_twitter);
            }     
        }
    
        $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $name_web);
        $detail_html = str_get_html($html_content);
        $name_twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
        if(isset($name_twitter)) {
            $name_twitter = $name_twitter->plaintext;
        }
    
        $name_category = null;
        $target_rows = $detail_html->find("tr > td.td_left");
        foreach($target_rows as $row) {
            if($row->plaintext === "Category") {
                $name_category = $row->nextSibling()->plaintext;    
            }
        }
    
        //prepare tweet text
        $tweet_text = null;
        if(!empty($investors_names) && (!is_null($name_twitter) || !empty($investors_twitters))) {
            $tweet_text = implode(", ", $investors_names)
            . (empty($investors_twitters) ? "" : (" - " . implode(", ", $investors_twitters) . " -"))
            . " invested " . ((is_null($amount) || $amount === "N/A") ? "an undisclosed price" : $amount)
            . " in " . $round
            . " in " . ($name_twitter ?: $name)
            . (is_null($name_category) ? "" : (" #".$name_category)) . " #funding"; 
        }
        
        $tweet = array('date' => $date, 
                       'name' => $name, 
                       'name_twitter' => $name_twitter,
                       'name_category' => $name_category, 
                       'amount' => trim($amount), 
                       'investors' => implode(";", $investors_names), 
                       'investors_twitters' => implode(";", $investors_twitters), 
                       'tweet' => $tweet_text);

        scraperwiki::save(array("date", "name", "investors"), $tweet);           
    }
}

?>
<?php

require 'scraperwiki/simple_html_dom.php';  
  
for ($i=1; $i<=50; $i++) {    
    
    $html_content = scraperwiki::scrape("http://www.crunchbase.com/funding-rounds?page=" . $i);
    $html = str_get_html($html_content);
    
    $posts_array = $html->find("div#col2_internal > table > tbody > tr");
    
    foreach($posts_array as $post) {
        $post_cells = $post->find("td");
        $date = $post_cells[0]->plaintext;
        $name = $post_cells[1]->plaintext;
        $name_web = $post_cells[1]->find("a", 0)->href;
        $round = trim($post_cells[2]->plaintext);
        $amount = $post_cells[3]->plaintext;
        $investors = $post_cells[4]->find("a");
        $investors_names = array();
        $investors_twitters = array();
        foreach($investors as $investor) {
            array_push($investors_names, $investor->title);
            $investor_web = $investor->href;
            $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $investor_web);
            $html = str_get_html($html_content);
            $investor_twitter = $html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
            if(isset($investor_twitter)) {
                $investor_twitter = $investor_twitter->plaintext;
                array_push($investors_twitters, $investor_twitter);
            }     
        }
    
        $html_content = scraperwiki::scrape("http://www.crunchbase.com" . $name_web);
        $detail_html = str_get_html($html_content);
        $name_twitter = $detail_html->find("div#col1 td.td_right > a[href*=twitter.com]",0);
        if(isset($name_twitter)) {
            $name_twitter = $name_twitter->plaintext;
        }
    
        $name_category = null;
        $target_rows = $detail_html->find("tr > td.td_left");
        foreach($target_rows as $row) {
            if($row->plaintext === "Category") {
                $name_category = $row->nextSibling()->plaintext;    
            }
        }
    
        //prepare tweet text
        $tweet_text = null;
        if(!empty($investors_names) && (!is_null($name_twitter) || !empty($investors_twitters))) {
            $tweet_text = implode(", ", $investors_names)
            . (empty($investors_twitters) ? "" : (" - " . implode(", ", $investors_twitters) . " -"))
            . " invested " . ((is_null($amount) || $amount === "N/A") ? "an undisclosed price" : $amount)
            . " in " . $round
            . " in " . ($name_twitter ?: $name)
            . (is_null($name_category) ? "" : (" #".$name_category)) . " #funding"; 
        }
        
        $tweet = array('date' => $date, 
                       'name' => $name, 
                       'name_twitter' => $name_twitter,
                       'name_category' => $name_category, 
                       'amount' => trim($amount), 
                       'investors' => implode(";", $investors_names), 
                       'investors_twitters' => implode(";", $investors_twitters), 
                       'tweet' => $tweet_text);

        scraperwiki::save(array("date", "name", "investors"), $tweet);           
    }
}

?>
