<?php

error_reporting(E_ALL ^ E_NOTICE);

require 'scraperwiki/simple_html_dom.php'; // Hi Scraperwiki!

// We need to start from TODAY!
$today = time();

// Loop through the next 7 days of events
for ($c=0; $c<=6; $c++){
    
    // Get the day to check
    $day = $today+($c*(24 * 60 * 60));
    $d = date('d', $day);
    $m = date('m', $day);
    $y = date('Y', $day);
    
    // Set the source and grab it
    $html_content = scraperwiki::scrape("http://apps.cheshirewestandchester.gov.uk/WhatsOn/events.aspx?f=1&t=d&s=$d%2f$m%2f$y&c=&x=0#results");
    $html = str_get_html($html_content);
    
    $ce = array(); // current event placeholder
    
    foreach ($html->find("#eventList tbody tr") as $tr){
        
        // The title
        if ($tr->find("h2 a", 0))
            $ce['title'] = utf8_encode($tr->find("h2 a", 0)->innertext);
        
        // The URL (for unique ID)
        if ($tr->find("h2 a", 0))
            $ce['url'] = utf8_encode($tr->find("h2 a", 0)->href);
        
        // The date
        if (trim($tr->find("td.label", 0)->innertext) == "When")
            $ce['when'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

        // The location
        if (trim($tr->find("td.label", 0)->innertext) == "Location")
            $ce['location'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

        // The postcode
        if (trim($tr->find("td.label", 0)->innertext) == "Postcode")
            $ce['postcode'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));
    
        // Description
        if (trim($tr->find("td.label", 0)->innertext) == "Description")
            $ce['description'] = utf8_encode(strip_tags(trim($tr->find("td", 1)->innertext)));

        // Contact name
        if (trim($tr->find("td.label", 0)->innertext) == "Contact")
            $ce['contact'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

        // Telephone
        if (trim($tr->find("td.label", 0)->innertext) == "Telephone")
            $ce['phone'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

        // Timings
        if (trim($tr->find("td.label", 0)->innertext) == "Timings")
            $ce['timings'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));
           
        // Age range
        if (trim($tr->find("td.label", 0)->innertext) == "Age range")
            $ce['age'] = utf8_encode(trim(str_replace('-Please Select-', '', strip_tags($tr->find("td", 1)->innertext))));

        // Cost
        if (trim($tr->find("td.label", 0)->innertext) == "Cost"){ // last item
            $ce['cost'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

            // add a unique identifier
            $ce['id'] = md5($ce['title']." ".$ce['when']);
            
            // last item so save the data and clear the array for the next event
            scraperwiki::save(array('title','url','when','location','postcode','description','contact','phone','timings','age','cost', 'id'), $ce);
            $ce = array(); //reset
        }
        
    }
    
}

?>
<?php

error_reporting(E_ALL ^ E_NOTICE);

require 'scraperwiki/simple_html_dom.php'; // Hi Scraperwiki!

// We need to start from TODAY!
$today = time();

// Loop through the next 7 days of events
for ($c=0; $c<=6; $c++){
    
    // Get the day to check
    $day = $today+($c*(24 * 60 * 60));
    $d = date('d', $day);
    $m = date('m', $day);
    $y = date('Y', $day);
    
    // Set the source and grab it
    $html_content = scraperwiki::scrape("http://apps.cheshirewestandchester.gov.uk/WhatsOn/events.aspx?f=1&t=d&s=$d%2f$m%2f$y&c=&x=0#results");
    $html = str_get_html($html_content);
    
    $ce = array(); // current event placeholder
    
    foreach ($html->find("#eventList tbody tr") as $tr){
        
        // The title
        if ($tr->find("h2 a", 0))
            $ce['title'] = utf8_encode($tr->find("h2 a", 0)->innertext);
        
        // The URL (for unique ID)
        if ($tr->find("h2 a", 0))
            $ce['url'] = utf8_encode($tr->find("h2 a", 0)->href);
        
        // The date
        if (trim($tr->find("td.label", 0)->innertext) == "When")
            $ce['when'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

        // The location
        if (trim($tr->find("td.label", 0)->innertext) == "Location")
            $ce['location'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

        // The postcode
        if (trim($tr->find("td.label", 0)->innertext) == "Postcode")
            $ce['postcode'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));
    
        // Description
        if (trim($tr->find("td.label", 0)->innertext) == "Description")
            $ce['description'] = utf8_encode(strip_tags(trim($tr->find("td", 1)->innertext)));

        // Contact name
        if (trim($tr->find("td.label", 0)->innertext) == "Contact")
            $ce['contact'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

        // Telephone
        if (trim($tr->find("td.label", 0)->innertext) == "Telephone")
            $ce['phone'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

        // Timings
        if (trim($tr->find("td.label", 0)->innertext) == "Timings")
            $ce['timings'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));
           
        // Age range
        if (trim($tr->find("td.label", 0)->innertext) == "Age range")
            $ce['age'] = utf8_encode(trim(str_replace('-Please Select-', '', strip_tags($tr->find("td", 1)->innertext))));

        // Cost
        if (trim($tr->find("td.label", 0)->innertext) == "Cost"){ // last item
            $ce['cost'] = utf8_encode(trim(str_replace(' &nbsp;', '', $tr->find("td", 1)->innertext)));

            // add a unique identifier
            $ce['id'] = md5($ce['title']." ".$ce['when']);
            
            // last item so save the data and clear the array for the next event
            scraperwiki::save(array('title','url','when','location','postcode','description','contact','phone','timings','age','cost', 'id'), $ce);
            $ce = array(); //reset
        }
        
    }
    
}

?>
