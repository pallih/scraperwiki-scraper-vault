<?php
require  'scraperwiki/simple_html_dom.php';
$months = array("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");
$days = array("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun");
$ical_days = array("Mon"=>"MO", "Tue"=>"TU", "Wed"=>"WE", "Thu"=>"TH", "Fri"=>"FR", "Sat"=>"SA", "Sun"=>"SU");

function decode_entities($string) {
    return html_entity_decode(preg_replace('~&#x([0-9a-f]+);~ei', 'chr(hexdec("\\1"))', preg_replace('~&#([0-9]+);~e', 'chr("\\1")', $string)));
}
$url = "http://whatson.visitbirmingham.com/?&search_type=all&page=";
for ($page=0; $page<20; $page++) {
    $dom = new simple_html_dom();
    $dom->load(scraperwiki::scrape($url.$page));
    echo count($dom->find('//div[@class=whatson-info]'));
    foreach ($dom->find('//div[@class=whatson-info]') as $item) {
        $insert = array();
        $i = $item->find('//div[@class=whatson-image]/img');
        if (count($i) > 0) {
            $i = $i[0];
            $insert['img'] = "http://whatson.visitbirmingham.com".$i->src;
        } else {
            $insert['img'] = "";
        }
        $t = $item->find('//div[@class=whatson-main-info]/h2/a');
        $t = $t[0];
        $insert['link'] = $t->href;
        $insert['title'] = decode_entities($t->innertext);
        if ($insert['title'] == "Marvellous Mothers") {
            var_dump($page);
        }
        $ve = $item->find('//span[@class=venue]');
        $ve = $ve[0];
        $ve = strip_tags($ve->innertext);
        $ve = explode(",", $ve);
        $insert['venue_name'] = decode_entities($ve[0]);
        preg_match("/(\w{1,2}\d{1,2}\w?){1}(?<sp>\s{0,3})?(\d\w{2}){1}/", $ve[1], $m);
        if (isset($m[0])) {
            $insert['venue_postcode'] = $m[0];
            $ll = scraperwiki::gb_postcode_to_latlng($insert['venue_postcode']);
            $insert['lat'] = $ll[0];
            $insert['lng'] = $ll[1];
        } else {
            $insert['venue_postcode'] = $insert['lat'] = $insert['lng'] = "";
        }
        $date = $item->find('//span[@class=datetime]');
        $date = $date[0];
        $date = $date->innertext;
        
        $insert['start_date'] = "";
        $insert['end_date'] = "";

        //21 - 23 Jan 2012
        if (preg_match_all("/((?<start>\d{1,2})( \- (?<end>\d{1,2}))? (?<month>\w{3}) (?<year>\d{4}))/", $date, $m)) {
            for ($i=0; $i<count($m['start']); $i++) {
                //var_dump($m['month'][$i]);
                //var_dump(array_search($m['month'][$i], $months));
                if (array_search($m['month'][$i], $months) === false) {
                    die;
                }
                $strt = new DateTime(null, new DateTimeZone('Europe/London'));
                $strt->setTime(0, 0, 0);
                $strt->setDate($m['year'][$i], array_search($m['month'][$i], $months)+1, $m['start'][$i]);
                //$insert['start_date'] .= $strt.":";
                $nd = new DateTime(null, new DateTimeZone('Europe/London'));
                $nd->setTime(23, 59, 59);
                if ($m['end'][$i]) {
                    $nd->setDate($m['year'][$i], array_search($m['month'][$i], $months)+1, $m['end'][$i]);
                } else {
                     $nd->setDate($m['year'][$i], array_search($m['month'][$i], $months)+1, $m['start'][$i]);
                }
                //$insert['end_date'] .= $nd.":";
                
                $insert_ical = array();
                $insert_ical['link'] = $insert['link'];
                $insert_ical['DTSTART'] = $strt->getTimestamp();
                $insert_ical['DTEND'] = $nd->getTimestamp();
                $insert_ical['FREQ'] = "DAILY";
                $insert_ical['BYDAY'] = "";
                $insert_ical['WKST'] = "MO";
                $insert_ical['COUNT'] = round(($nd->getTimestamp()-$strt->getTimestamp())/86400);
                //var_dump($insert_ical);
                //die();
                scraperwiki::save_sqlite(array('link', 'DTSTART'), $insert_ical, "ical");
            }
        }
        
        //Daily 11:00 AM; 12:00 AM
        if (preg_match_all("/Daily ((?<start_hour>\d{1,2}):(?<start_min>\d{2}) (?<start_m>\w{2})(; )?)+/", $date, $m)) {
            continue;
            //var_dump($m);
            //die();
        }

      //Every Mon 10:00 AM - 10:00 PM
        if (preg_match_all("/Every (?<day>Mon|Tue|Wed|Thu|Fri|Sat|Sun) ((?<start_hour>\d{1,2}):(?<start_min>\d{2}) (?<start_m>\w{2})( - (?<end_hour>\d{1,2}):(?<end_min>\d{2}) (?<end_m>\w{2}))?)?/", $date, $m)) {
            
            for ($i=0; $i<count($m['day']); $i++) {
                $d = new DateTime();
                $day = $d->format("D");
                $day_offset = array_search($day, $days)-array_search($m['day'][$i], $days);
                
                if ($day_offset < 0) {
                    $day_offset += 7;
                }
                $d->modify("+{$day_offset} days");
                //for ($j=0; $j<5; $j++) {
                    $start = new DateTime();
                    if (isset($m['start_hour'][$i]) && $m['start_hour'][$i]) {
                        if ($m['start_hour'][$i] != 12 && $m['start_m'][$i] == "pm") {
                            $m['start_hour'][$i] += 12;
                        } elseif ($m['start_hour'][$i] == 12 && $m['start_m'][$i] == "am") {
                            $m['start_hour'][$i] == "00";
                        }
                        $start->setTime($m['start_hour'][$i], $m['start_min'][$i]);
                        $start->setDate($d->format("Y"), $d->format("m"), $d->format("d"));
                    } else {
                        $start->setDate($d->format("Y"), $d->format("m"), $d->format("d"));
                        $start->setTime(0, 0, 0);
                    }
                    
                    
                    if (isset ($m['end_hour'][$i]) && $m['end_hour'][$i]) {
                        $end = new DateTime();
                        if ($m['end_hour'][$i] != 12 && $m['end_m'][$i] == "pm") {
                            $m['end_hour'][$i] += 12;
                        } elseif ($m['end_hour'][$i] == 12 && $m['end_m'][$i] == "am") {
                            $m['end_hour'][$i] == "00";
                        }
                        $end->setDate($d->format("Y"), $d->format("m"), $d->format("d"));
                        $end->setTime($m['end_hour'][$i], $m['end_min'][$i]);
                    } else {
                        $end = new DateTime("@".$start->getTimestamp());
                        $end->add(new DateInterval("PT1H"));
                    }
                    //$d->modify("+7 days");
                   // $insert['start_date'] = $start->getTimestamp().":";
                    //$insert['end_date'] = $end->getTimestamp().":";
                    //if ($j == 0) {
                        $ical_start = $start->getTimestamp();
                        $ical_end = $end->getTimestamp();
                    //}
                //}
                $interval = $start->diff($end);
                $insert_ical = array();
                $insert_ical['link'] = $insert['link'];
                $insert_ical['DTSTART'] = $ical_start;
                $insert_ical['DTEND'] = $ical_end;

                $insert_ical['COUNT'] = "-1";
                $insert_ical['WKST'] = "MO";
                $insert_ical['BYDAY']= $ical_days[$m['day'][$i]];
                $insert_ical['FREQ'] = "WEEKLY";
                //$insert_ical['DURATION'] = 3599;
                scraperwiki::save_sqlite(array('link', 'DTSTART'), $insert_ical, "ical");
            }
                       
        }
        

        //Mon - Wed, 10:00 AM - 10:00 PM
        if (preg_match_all("/(?<day_start>Mon|Tue|Wed|Thu|Fri|Sat|Sun) - (?<day_end>Mon|Tue|Wed|Thu|Fri|Sat|Sun)(,)? ((?<start_hour>\d{1,2}):(?<start_min>\d{2}) (?<start_m>\w{2})( - (?<end_hour>\d{1,2}):(?<end_min>\d{2}) (?<end_m>\w{2}))?)?/", $date, $m)) {
            for ($i=0; $i<count($m['day_start']); $i++) {
                $d = new DateTime();
                $day = $d->format("D");
                $day_offset = array_search($day, $days)-array_search($m['day_start'][$i], $days);
                if ($day_offset < 0) {
                    $day_offset += 7;
                }
                $d->modify("+{$day_offset} days");
                $days_per_week = array_search($m['day_end'][$i], $days)-array_search($m['day_start'][$i], $days);



                $start = new DateTime();
                if (isset($m['start_hour'][$i]) && $m['start_hour'][$i]) {
                    if ($m['start_hour'][$i] != 12 && $m['start_m'][$i] == "pm") {
                        $m['start_hour'][$i] += 12;
                    } elseif ($m['startmar_hour'][$i] == 12 && $m['start_m'][$i] == "am") {
                        $m['start_hour'][$i] == "00";
                    }
                    $start->setDate($d->format("Y"), $d->format("m"), $d->format("d"));
                    $start->setTime($m['start_hour'][$i], $m['start_min'][$i]);
                } else {
                    $start->setDate($d->format("Y"), $d->format("m"), $d->format("d"));
                    $start->setTime(0, 0, 0);
                }
                    
                $end = new DateTime();
                if (isset ($m['end_hour'][$i]) && $m['end_hour'][$i]) {
                    if ($m['end_hour'][$i] != 12 && $m['end_m'][$i] == "pm") {
                        $m['end_hour'][$i] += 12;
                    } elseif ($m['end_hour'][$i] == 12 && $m['end_m'][$i] == "am") {
                        $m['end_hour'][$i] == "00";
                    }
                    $end->setTime($m['end_hour'][$i], $m['end_min'][$i]);
                    $end->setDate($d->format("Y"), $d->format("m"), $d->format("d"));
                } else {
                    $end->setTime(23, 59, 59);
                    $end->setDate($d->format("Y"), $d->format("m"), $d->format("d"));
                }
                $ical_start = $start->getTimestamp();
                $ical_end = $end->getTimestamp();
                
                
                
                
                $insert_ical = array();
                $insert_ical['link'] = $insert['link'];
                $dtstart = new DateTime();
                $dtstart->setTime($start->format("H"), $start->format("i"));
                $insert_ical['DTSTART'] = $ical_start;
                $insert_ical['DTEND'] = $ical_end;
                $insert_ical['COUNT'] = "-1";
                //$insert_ical['DURATION'] = $interval->s*$interval->i*60*$interval->h*120;
                $start = array_search($m['day_start'][$i], $days);
                $end = array_search($m['day_end'][$i], $days);

                $insert_ical['FREQ'] = $insert_ical['BYDAY'] = "";
                $insert_ical['WKST'] = "MO";
                
                if (array_search($m['day_end'][$i], $days) < array_search($m['day_start'][$i], $days)) {
                    $end = array_search($m['day_end'][$i], $days)+7;
                }
                $insert_ical['FREQ'] = "WEEKLY";
                
                for ($j=array_search($m['day_start'][$i], $days); $j<=$end; $j++) {
                    //var_dump(($j>6? $j-7: $j), $ical_days[$days[($j>6? $j-7: $j)]]);
                    $insert_ical['BYDAY']= $ical_days[$days[($j>6? $j-7: $j)]];
                    //var_dump($insert_ical);
                    //die;
                    scraperwiki::save_sqlite(array('link', 'DTSTART'), $insert_ical, "ical");
                }
                //var_dump($m[0]);
                //die();
    
                
            }

            //Daily 12:00 - 15:00
            if (preg_match_all("/Daily (?<start_hour>\d{1,2}):(?<start_min>\d{2}) (?<start_m>\w{2})( - (?<end_hour>\d{1,2}):(?<end_min>\d{2}) (?<end_m>\w{2}))?/", $date, $m)) {
                


                for ($i=0; $i<count($m['start_hour']); $i++) {
                        $start = new DateTime();
                        if (isset($m['start_hour'][$i]) && $m['start_hour'][$i]) {
                            if ($m['start_hour'][$i] != 12 && $m['start_m'][$i] == "pm") {
                                $m['start_hour'][$i] += 12;
                            } elseif ($m['start_hour'][$i] == 12 && $m['start_m'][$i] == "am") {
                                $m['start_hour'][$i] == "00";
                            }
                            $start->setTime($m['start_hour'][$i], $m['start_min'][$i]);
                        } else {
                            $start->setTime(9, 0, 0);
                        }
                        
                        $end = new DateTime();
                        if (isset ($m['end_hour'][$i]) && $m['end_hour'][$i]) {
                            if ($m['end_hour'][$i] != 12 && $m['end_m'][$i] == "pm") {
                                $m['end_hour'][$i] += 12;
                            } elseif ($m['end_hour'][$i] == 12 && $m['end_m'][$i] == "am") {
                                $m['end_hour'][$i] == "00";
                            }
                            $end->setTime($m['end_hour'][$i], $m['end_min'][$i]);
                        } else {
                            $end->setTime(17, 00, 00);
                        }

                        for ($i=0; $i<7*5; $i++) {
                            $insert['start_date'] = $start->getTimestamp().":";
                            $insert['end_date'] = $end->getTimestamp().":";

                            if ($i == 0) {
                                $ical_start = $start->getTimestamp();
                                $ical_end = $end->getTimestamp();
                            }
                            $start->modify("+1 day");
                            $end->modify("+1 day");
                            $interval = $start->diff($end);
                        }


                        $insert_ical = array();
                        $insert_ical['link'] = $insert['link'];
                        $insert_ical['DTSTART'] = $ical_start->getTimestamp();
                        $insert_ical['DTEND'] = $ical_end->getTimestamp();
                        $insert_ical['COUNT'] = "-1$";
                        $insert_ical['FREQ'] = "DAILY";
                        //$insert_ical['DURATION'] = $interval->s*$interval->i*60*$interval->h*120;

                        $insert_ical['BYDAY'] = $insert_ical['WKST'] = "";
                        scraperwiki::save_sqlite(array('link', 'DTSTART'), $insert_ical, "ical");


                    }
            }

            
        }

        if (strlen($insert['start_date']) > 1) {
            $insert['start_date'] = substr($insert['start_date'], 0, -1);
            $insert['end_date'] = substr($insert['end_date'], 0, -1);
        } else {
           var_dump($date);
        }
        foreach ($insert as $key=>$data) {
            $insert[$key] = utf8_decode($data);
        }

        $dom = new simple_html_dom();
        $dom->load(scraperwiki::scrape($insert['link']));
        $items = $dom->find('//p[@class=category]/strong');
        $categories = array();
        foreach ($items as $item) {
            switch ($item->innertext) {
                case "Classical":
                    $cat = "Music - Classical";
                    break;
                case "Music":
                    $cat = "Music - Other";
                    break;
                default:
                    $cat = $item->innertext;
                    break;
            }
            $categories[] = $item->innertext;
        }
        $insert['categories'] = implode(":", $categories);

        $description = $dom->find('//div[@class=production-content]/p');
        $insert['description'] = strip_tags(decode_entities($description[0]->innertext));
        scraperwiki::save_sqlite(array('link'), $insert, "items");
        
    }
}

?>
