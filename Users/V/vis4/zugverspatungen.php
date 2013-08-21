<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

$stations = array(
    "Berlin" => "Berlin%20Hbf%238011160", 
    "Hannover" => "Hannover%20Hbf%238000152",
    "Hamburg-Altona" => "Hamburg-Altona%238002553",
    "Köln" => "K%F6ln%20Hbf",
    "Frankfurt/Main" => "Frankfurt(Main)Hbf%238000105",
    "Dresden" => "Dresden Hbf%238010085",
    "München" => "M%FCnchen%20Hbf%238000261",
    "Mannheim" => "Mannheim Hbf%238000244",
    "Stuttgart" => "Stuttgart Hbf%238000096"
);

$boardTypes = array("arr", "dep");

foreach ($stations as $city => $city_param) {
    foreach ($boardTypes as $boardType) {
        
        $html = scraperwiki::scrape("http://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=9648&rt=1&input=".$city_param."&boardType=".$boardType."&time=actual&productsFilter=11&start=yes");

        # Use the PHP Simple HTML DOM Parser to extract <td> tags
        $dom = new simple_html_dom();
        $dom->load($html);
        
        foreach($dom->find('table.result tr') as $row)
        {
            $time = $row->find('td.time', 0);
            if ($time != null && $time->find('a', 0) == null) {
                
                $time = $time->innertext;
                
                $train = $row->find('td.train', 1);
                if ($train != null) {
                    $train = $train->find('a', 0)->innertext;
                    $ris = $row->find('td.ris', 0);
                    if ($ris != null) {
                        $late = $ris->find('span span', 0);
                        if ($late != null) $late = s($late->innertext); else $late = "";
                        $m = array();
                        if (preg_match('/ca. (\d+) Minuten später/', $late, $m) > 0) {
                            $minutes = $m[1];
                        } else {
                            $minutes = "";
                        }
                        $reason = $ris->find('span.red', 0);
                        if ($reason != null) $reason = s($reason->innertext); else $reason = "";
                    }

                    $canceled = $reason == "Zug fällt aus" ? "canceled" : "";

                    //print $time."\t".$train."\t".$late ."\t--\t".$reason ."\n";
                    scraperwiki::save(array('city','type','time','train'), array('city' => $city, 'type' => $boardType, 'train' => $train, 'time' => $time, 'canceled' => $canceled, 'late' => $late, 'minutes' => $minutes, 'reason' => $reason));
                }
            }
            # Store data in the datastore
           
            //scraperwiki::save(array('data'), array('data' => $data->plaintext));
        }
    }
}

function s($s) {
    return str_replace(array('&nbsp;','&#252;','&#228;','&#246;','&#220;','&#196;'), array(' ','ü','ä','ö','Ü','Ä'), $s);
}


?>