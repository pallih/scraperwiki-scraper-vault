<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';

/* strpos that takes an array of values to match against a string 
 * note the stupid argument order (to match strpos) 
 */ 
function strpos_arr($trainNumbers, $train) { 
    if(!is_array($train)) $train = array($train); 
    foreach($train as $what) { 
        if(($pos = strpos($trainNumbers, $what))!==false) return $pos; 
    } 
    return false; 
}

$stations = array(
    "Bruxelles-Midi" => "Bruxelles-Midi%238800004",
    "Liège-Guillemins" => "Li%E8ge-Guillemins%238800012",
    "Aachen Hbf" => "Aachen%20Hbf%238000001",
    "Köln Hbf" => "K%F6ln%20Hbf%238000207"
);

$boardTypes = array("arr", "dep");

$trainNumbers = array("THA 9401", "THA 9412", "THA 9413", "THA 9424", "THA 9437", "THA 9448", "THA 9461", "THA 9472", "THA 9473", "THA 9484", "ICE   10", "ICE   11", "ICE   14", "ICE   15", "ICE   16", "ICE   17", "ICE   18", "ICE   19");

foreach ($stations as $city => $city_param) {
    foreach ($boardTypes as $boardType) {
        
        $html = scraperwiki::scrape("http://reiseauskunft.bahn.de/bin/bhftafel.exe/dn?ld=9648&rt=1&input=".$city_param."&boardType=".$boardType."&time=actual&productsFilter=1&start=yes");

        # Use the PHP Simple HTML DOM Parser to extract <td> tags
        $dom = new simple_html_dom();
        $dom->load($html);
        
        foreach($dom->find('table.result tr') as $row)
        {
            $time = $row->find('td.time', 0);
            if ($time != null && $time->find('a', 0) == null) {
                
                $time = $time->innertext;
                
                $train = $row->find('td.train', 1);
                if (strpos_arr($train, $trainNumbers)) {
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
                    scraperwiki::save(array('city','type','time','train'), array('city' => $city, 'type' => $boardType, 'train' => $train, 'time' => $time, 'canceled' => $canceled, 'reason' => $reason, 'late' => $late, 'minutes' => $minutes, 'date' => (Date("Ymd"))));
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