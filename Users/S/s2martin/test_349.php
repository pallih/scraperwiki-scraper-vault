<?php

# WARNING - there is some dirty old code here, please wash your eyes after viewing! (or help me improve it!) 

require 'scraperwiki/simple_html_dom.php'; 

# get all pages
for($i=1;$i<=30;$i++) {

    $html_content = scraperwiki::scrape("http://www.greendealorb.co.uk/installers/installer-search?page=".$i."");
    $html = str_get_html($html_content);
    
    foreach ($html->find("table.mcsResultsTable tr") as $data) {
            
        # get general installer details from summary table   
        $name = $data->find("td", 0)->plaintext;
        $installer_href = $data->find("td a",0);
        $installer_href = $installer_href->href;
        $installer_id = array();
        preg_match("/installer_id=([0-9]+)/", $installer_href, $installer_id);
        $telephone = $data->find("td",3)->plaintext;

        # only run if installer ID is not empty
        if (!empty($installer_id)) {

            # get detailed installer details
            $html_content = scraperwiki::scrape("http://www.greendealorb.co.uk/index.php?option=com_content&amp;view=article&amp;id=131&amp;".$installer_id[0]);
            $html = str_get_html($html_content);

            foreach ($html->find("div.mcsColumnsTwoOne") as $data) {

                $address = $data->find("p", 2)->plaintext;
                $url = $data->find("p", 4)->plaintext;
                $url_full = array();
                preg_match("/Website:\s*(.*)/", $url, $url_match);
                # check URL array is not empty
                if (!empty($url_match) ? $url = $url_match[1] : $url="NULL");
                # check if website is listed
                if (empty($url_match) ? $email = $data->find("p", 4)->plaintext : $email = $data->find("p", 5)->plaintext); 
                $email_full = array();
                preg_match("/Email:\s*(.*)/", $email, $email_full);
                # check email array is not empty
                if (!empty($email_full) ? $email = $email_full[1] : $email="NULL");
                if (empty($url_match) ? $contact = $data->find("p", 5)->plaintext : $contact = $data->find("p", 6)->plaintext);
                $contact_full = array();
                preg_match("/Contact:\s*(.*)/", $contact, $contact_full);
                if (!empty($contact_full) ? $contact = $contact_full[1] : $contact="NULL");

            }
                
            $record = array (
                'installer_id' => $installer_id[1],
                'name' => utf8_encode($name),
                'telephone' => utf8_encode($telephone),
                'address' => utf8_encode($address),
                'email' => utf8_encode($email),
                'url' => utf8_encode($url),
                'contact' => utf8_encode($contact) 
            );

            #print json_encode($record) . "\n";
            scraperwiki::save(array('installer_id'), $record);

        }            
        
    }
               
}
                
?>
