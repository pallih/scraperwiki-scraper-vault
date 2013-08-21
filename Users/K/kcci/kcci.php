<?php

    // Find documentation at http://simplehtmldom.sourceforge.net/manual.htm
    require  'scraperwiki/simple_html_dom.php';

    function kcci($uuid){
        // Create DOM from URL or file
        $html = file_get_html('http://www.kcci.com.pk/UserProfile/tabid/42/userId/'.$uuid.'/Default.aspx');

        // Extract member profile from table
        $table = $html->find('table', 1);
        $profile = array();
        foreach ($table->find('td') as $td){
            array_push($profile, $td->plaintext);
        }
        $record['UUID']  = $uuid;
        for ($i = 0; $i < count($profile); $i += 2) {
            $record[$profile[$i]] = $profile[$i + 1];
        }

        // Save the record
        ksort($record);
        $unique_keys = array('UUID');
        scraperwiki::save_sqlite($unique_keys, $record, $table_name="kcci", $verbose=2);
    
        // Clean up
        unset($record);
        unset($profile);
        $td->clear();
        unset($td);
        $table->clear();
        unset($table);
        $html->clear(); 
        unset($html);
    }

?>