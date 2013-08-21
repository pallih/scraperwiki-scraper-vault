<?php
require 'scraperwiki/simple_html_dom.php';
date_default_timezone_set('Europe/Dublin');

// Get the most recently scraped date from the DB
$maxlong = scraperwiki::select('date FROM swdata ORDER by date DESC LIMIT 1');
// If none start in 1997
//print_r($max);
//$max = strtotime('2011-10-01');

//$maxlong = $max['date'];
//$year = date('Y',$maxlong);
if(!$maxlong) $maxlong = strtotime('2011-10-01');
else {
    $maxlong = strtotime($maxlong[0]['date']);
    $year = date('Y',$maxlong);
    if($year < date('Y')) $year++;
    $maxlong = strtotime($year.'-01-01');
}

print "maxlong" . $maxlong;
print_r($year);
//$maxlong = strtotime('2011-10-01');
echo 'Scraping engagements from '.date('Y',$maxlong)."\n";

// Scrape the page with the list of weeks for that year
$html = scraperwiki::scrape('http://president.ie/index.php?section=6&lang=eng&year='.date('Y',$maxlong));

//Fetch all the week IDs
preg_match_all('/engagement=([0-9]{5,7})/',$html,$dates);

// Fetch all the week start dates
preg_match_all('|Week beginning ([a-z0-9 ]{10,30})</a>|i',$html,$first);

// Work from the start of the year forwards to today
krsort($dates[1]);
print_r($dates);
// Loop through the weeks and scrape pages
foreach($dates[1] as $key => $week) {

    // Make week beginning date into unix time
    $f = strtotime($first[1][$key]);
    // Deduce if this is new information
    if($maxlong < $f) {
        // Scrape the engagements from the given week
        $html = scraperwiki::scrape('http://president.ie/index.php?section=6&engagement='.$week.'&lang=eng');
print "week" . $week;
        // Remove annoying tabs, newlines etc
        $html = preg_replace('/\s+/',' ',$html);
        // Tidy up the HTML to make it consistent
      $html = str_replace('<span class="bodytextBold" style="font-weight: bold;">','<p>',$html);
   //     $html = str_replace('<span style="font-weight: bold;">','<p>',$html);
        $html = str_replace('<b class="bodytextBold">','<p>',$html);
$html = str_replace('<br><br>','</p>',$html); #</span>
        $html = str_replace('<p class="bodytextBold">','<p>',$html);
        $html = str_replace('<p class="bodytext">','<p>',$html);
        $html = str_replace('<b class="bodytextBold">','<p>',$html);
        $html = str_replace('<p class="bodytextBold">','<p>',$html);
        $html = str_replace('<p class="bodytextBold" style="TEXT-ALIGN: left">','<p>',$html);
        $html = str_replace('<div align="left"> <p class="bodytextBold" style="TEXT-ALIGN: left" align="left">','<p>',$html);
        $html = str_replace('<br /><p>','<br />',$html);
        $html = str_replace('&amp;','&',$html);
        $html = str_replace('<BR><BR>','<br />',$html);
        $html = str_replace('<p><br />','<br />',$html);
        $html = str_replace('<b>','<p>',$html);
        $html = str_replace('&nbsp;',' ',$html);
     //   $html = str_replace('<span style="font-weight: bold;" class="bodytextBold">','<p>',$html); #span
$html = str_replace('<P></P>','',$html);
$html = str_replace('<p></p>','',$html);
//$html = str_replace('<P></P> <P></P> ','',$html);
$html = str_replace('</P> <P>','',$html);
$html = str_replace('<p> </p>','',$html);
//$html = str_replace('</span>','<br />',$html);
$html = str_replace('<p style="font-weight: bold;">','<p>',$html);
//$html = str_replace('</span><p>','<br /><p>',$html);
$html = str_replace('<p style="font-weight: bold;">','<p>',$html);
$html = str_replace('<P><STRONG>','<STRONG>',$html);

        $parser = new simple_html_dom();
        $parser->load($html);
        // Loop through the days
        foreach($parser->find('dl') as $day) {

            //Grab the date
            $date = $day->find('dt');
            $date = $date[0]->plaintext;
            echo $date."\n";
            //Grab the list of events for that day
            list($junk,$events) = explode('<dd>',$day);

print "$junk";
print_r($junk);
print "events";
print_r($events);
            // Depends on formatting of data which loop to run
            if(strpos($events,'<strong>') === 0) {
                $es = explode('<strong>',$events);
print "strongevents" . $events;
                unset($es[0]);
                // Loop through the days events
                foreach($es as $event) {

                    $info = explode('</strong>',$event);
print "sinfo";
print_r($info);
                    $data = date_time_place($date,$info[0]);
                    $data['info'] = trim(utf8_encode(strip_tags($info[1])));
$urlweek = $week; # - 1;
$url = "http://president.ie/index.php?section=6&engagement=".$urlweek."&lang=eng";
$data['url'] = $url;
$data['type'] = "engt";
$data['startdate'] = $data['date']."T".$data['time'].":00Z";
$data['latlng'] = "53.36018,-6.3175";
                    save_data($data);
                }
            } elseif(strpos($events,'<p>') === 0) {
print "eventspb" . $events;
                $es = explode('<p>',$events);
print "espb";
print_r($es);
unset($es[0]);

                foreach($es as $event) {
                   
$info = explode('<br />',$event);
print "infopb";
print_r($info);     $data = date_time_place($date,$info[0]);
                    $data['info'] = utf8_encode(strip_tags($info[1]));
$urlweek = $week; # - 1;
$url = "http://president.ie/index.php?section=6&engagement=".$urlweek."&lang=eng";
$data['url'] = $url;
$data['type'] = "engt";
$data['startdate'] = $data['date']."T".$data['time'].":00Z";
$data['latlng'] = "53.36018,-6.3175";
                    save_data($data);
                }
}  elseif(strpos($events,'<span') === 0) {
                $es = explode('<span',$events);
print "PeventsP" . $events;
                foreach($es as $event) {
print "infop";                    $info = explode('</span>',$event);
print_r($info);                    $data = date_time_place($date,$info[0]);
                    $data['info'] = trim(utf8_encode(strip_tags($info[1])));
$urlweek = $week; # - 1;
$url = "http://president.ie/index.php?section=6&engagement=".$urlweek."&lang=eng";
$data['url'] = $url;
$data['type'] = "engt";
$data['startdate'] = $data['date']."T".$data['time'].":00Z";
$data['latlng'] = "53.36018,-6.3175";
                    save_data($data);
                }
            }   elseif(strpos($events,'<p') === 0) {
                $es = explode('<p',$events);
print "PeventsP" . $events;
                foreach($es as $event) {
print "infop";                    $info = explode('</p>',$event);
print_r($info);                    $data = date_time_place($date,$info[0]);
                    $data['info'] = trim(utf8_encode(strip_tags($info[1])));
$urlweek = $week; # - 1;
$url = "http://president.ie/index.php?section=6&engagement=".$urlweek."&lang=eng";
$data['url'] = $url;
$data['type'] = "engt";
$data['startdate'] = $data['date']."T".$data['time'].":00Z";
$data['latlng'] = "53.36018,-6.3175";
                    save_data($data);
                }
            }   
else echo 'No parser for: '.$events."\n";
        }
    }

}

function date_time_place($date,$str) {
    // Grab out the time in hh:mm & the am/pm
    preg_match('|([0-9]{1,2}[:.]{1}[0-9]{1,2}) ?([apm.]{2,4})|i',$str,$timeplace);
print "timeplace";
print_r($timeplace);

    $hours = $timeplace[1];
    $apm = $timeplace[2];
    // Reformat the time along with the date and
    // get a UNIX compatable timestamp
    $timestring = $date.' '.$hours.$apm;
    $unix_date = strtotime($timestring);
    // If the date didn't work abort
    if($unix_date > 0) {
        // Account for events with no time (start at midnight)
        // If there is an am/pm use that to work out the place details
        if(empty($apm)) {
            $unix_date = strtotime($date);
            $data['label'] = utf8_encode(strip_tags($str));
        } else {
            $label = explode($apm,$str);
            $data['label'] = utf8_encode(strip_tags(trim($label[1])));
            if($data['label'][0] == ':') $data['label'] = substr($data['label'],1);
        }

        $data['date'] = date('Y-m-d',$unix_date);
        $data['time'] = date('H:i',$unix_date);

        $data['label'] = trim($data['label']);
        return $data;
    } else return false;
}

function save_data($data) {
    if(isset($data['date'])) {
        if($data['label'] != '' OR $data['info'] != '') {
            scraperwiki::save_sqlite(array('date','time'),$data);
            echo "\t".$data['startdate'].': '.$data['label'].' / '.$data['label'].$data['url']."\n";
            return true;
        } else return false;
    } else return false;
}
?>
<?php
require 'scraperwiki/simple_html_dom.php';
date_default_timezone_set('Europe/Dublin');

// Get the most recently scraped date from the DB
$maxlong = scraperwiki::select('date FROM swdata ORDER by date DESC LIMIT 1');
// If none start in 1997
//print_r($max);
//$max = strtotime('2011-10-01');

//$maxlong = $max['date'];
//$year = date('Y',$maxlong);
if(!$maxlong) $maxlong = strtotime('2011-10-01');
else {
    $maxlong = strtotime($maxlong[0]['date']);
    $year = date('Y',$maxlong);
    if($year < date('Y')) $year++;
    $maxlong = strtotime($year.'-01-01');
}

print "maxlong" . $maxlong;
print_r($year);
//$maxlong = strtotime('2011-10-01');
echo 'Scraping engagements from '.date('Y',$maxlong)."\n";

// Scrape the page with the list of weeks for that year
$html = scraperwiki::scrape('http://president.ie/index.php?section=6&lang=eng&year='.date('Y',$maxlong));

//Fetch all the week IDs
preg_match_all('/engagement=([0-9]{5,7})/',$html,$dates);

// Fetch all the week start dates
preg_match_all('|Week beginning ([a-z0-9 ]{10,30})</a>|i',$html,$first);

// Work from the start of the year forwards to today
krsort($dates[1]);
print_r($dates);
// Loop through the weeks and scrape pages
foreach($dates[1] as $key => $week) {

    // Make week beginning date into unix time
    $f = strtotime($first[1][$key]);
    // Deduce if this is new information
    if($maxlong < $f) {
        // Scrape the engagements from the given week
        $html = scraperwiki::scrape('http://president.ie/index.php?section=6&engagement='.$week.'&lang=eng');
print "week" . $week;
        // Remove annoying tabs, newlines etc
        $html = preg_replace('/\s+/',' ',$html);
        // Tidy up the HTML to make it consistent
      $html = str_replace('<span class="bodytextBold" style="font-weight: bold;">','<p>',$html);
   //     $html = str_replace('<span style="font-weight: bold;">','<p>',$html);
        $html = str_replace('<b class="bodytextBold">','<p>',$html);
$html = str_replace('<br><br>','</p>',$html); #</span>
        $html = str_replace('<p class="bodytextBold">','<p>',$html);
        $html = str_replace('<p class="bodytext">','<p>',$html);
        $html = str_replace('<b class="bodytextBold">','<p>',$html);
        $html = str_replace('<p class="bodytextBold">','<p>',$html);
        $html = str_replace('<p class="bodytextBold" style="TEXT-ALIGN: left">','<p>',$html);
        $html = str_replace('<div align="left"> <p class="bodytextBold" style="TEXT-ALIGN: left" align="left">','<p>',$html);
        $html = str_replace('<br /><p>','<br />',$html);
        $html = str_replace('&amp;','&',$html);
        $html = str_replace('<BR><BR>','<br />',$html);
        $html = str_replace('<p><br />','<br />',$html);
        $html = str_replace('<b>','<p>',$html);
        $html = str_replace('&nbsp;',' ',$html);
     //   $html = str_replace('<span style="font-weight: bold;" class="bodytextBold">','<p>',$html); #span
$html = str_replace('<P></P>','',$html);
$html = str_replace('<p></p>','',$html);
//$html = str_replace('<P></P> <P></P> ','',$html);
$html = str_replace('</P> <P>','',$html);
$html = str_replace('<p> </p>','',$html);
//$html = str_replace('</span>','<br />',$html);
$html = str_replace('<p style="font-weight: bold;">','<p>',$html);
//$html = str_replace('</span><p>','<br /><p>',$html);
$html = str_replace('<p style="font-weight: bold;">','<p>',$html);
$html = str_replace('<P><STRONG>','<STRONG>',$html);

        $parser = new simple_html_dom();
        $parser->load($html);
        // Loop through the days
        foreach($parser->find('dl') as $day) {

            //Grab the date
            $date = $day->find('dt');
            $date = $date[0]->plaintext;
            echo $date."\n";
            //Grab the list of events for that day
            list($junk,$events) = explode('<dd>',$day);

print "$junk";
print_r($junk);
print "events";
print_r($events);
            // Depends on formatting of data which loop to run
            if(strpos($events,'<strong>') === 0) {
                $es = explode('<strong>',$events);
print "strongevents" . $events;
                unset($es[0]);
                // Loop through the days events
                foreach($es as $event) {

                    $info = explode('</strong>',$event);
print "sinfo";
print_r($info);
                    $data = date_time_place($date,$info[0]);
                    $data['info'] = trim(utf8_encode(strip_tags($info[1])));
$urlweek = $week; # - 1;
$url = "http://president.ie/index.php?section=6&engagement=".$urlweek."&lang=eng";
$data['url'] = $url;
$data['type'] = "engt";
$data['startdate'] = $data['date']."T".$data['time'].":00Z";
$data['latlng'] = "53.36018,-6.3175";
                    save_data($data);
                }
            } elseif(strpos($events,'<p>') === 0) {
print "eventspb" . $events;
                $es = explode('<p>',$events);
print "espb";
print_r($es);
unset($es[0]);

                foreach($es as $event) {
                   
$info = explode('<br />',$event);
print "infopb";
print_r($info);     $data = date_time_place($date,$info[0]);
                    $data['info'] = utf8_encode(strip_tags($info[1]));
$urlweek = $week; # - 1;
$url = "http://president.ie/index.php?section=6&engagement=".$urlweek."&lang=eng";
$data['url'] = $url;
$data['type'] = "engt";
$data['startdate'] = $data['date']."T".$data['time'].":00Z";
$data['latlng'] = "53.36018,-6.3175";
                    save_data($data);
                }
}  elseif(strpos($events,'<span') === 0) {
                $es = explode('<span',$events);
print "PeventsP" . $events;
                foreach($es as $event) {
print "infop";                    $info = explode('</span>',$event);
print_r($info);                    $data = date_time_place($date,$info[0]);
                    $data['info'] = trim(utf8_encode(strip_tags($info[1])));
$urlweek = $week; # - 1;
$url = "http://president.ie/index.php?section=6&engagement=".$urlweek."&lang=eng";
$data['url'] = $url;
$data['type'] = "engt";
$data['startdate'] = $data['date']."T".$data['time'].":00Z";
$data['latlng'] = "53.36018,-6.3175";
                    save_data($data);
                }
            }   elseif(strpos($events,'<p') === 0) {
                $es = explode('<p',$events);
print "PeventsP" . $events;
                foreach($es as $event) {
print "infop";                    $info = explode('</p>',$event);
print_r($info);                    $data = date_time_place($date,$info[0]);
                    $data['info'] = trim(utf8_encode(strip_tags($info[1])));
$urlweek = $week; # - 1;
$url = "http://president.ie/index.php?section=6&engagement=".$urlweek."&lang=eng";
$data['url'] = $url;
$data['type'] = "engt";
$data['startdate'] = $data['date']."T".$data['time'].":00Z";
$data['latlng'] = "53.36018,-6.3175";
                    save_data($data);
                }
            }   
else echo 'No parser for: '.$events."\n";
        }
    }

}

function date_time_place($date,$str) {
    // Grab out the time in hh:mm & the am/pm
    preg_match('|([0-9]{1,2}[:.]{1}[0-9]{1,2}) ?([apm.]{2,4})|i',$str,$timeplace);
print "timeplace";
print_r($timeplace);

    $hours = $timeplace[1];
    $apm = $timeplace[2];
    // Reformat the time along with the date and
    // get a UNIX compatable timestamp
    $timestring = $date.' '.$hours.$apm;
    $unix_date = strtotime($timestring);
    // If the date didn't work abort
    if($unix_date > 0) {
        // Account for events with no time (start at midnight)
        // If there is an am/pm use that to work out the place details
        if(empty($apm)) {
            $unix_date = strtotime($date);
            $data['label'] = utf8_encode(strip_tags($str));
        } else {
            $label = explode($apm,$str);
            $data['label'] = utf8_encode(strip_tags(trim($label[1])));
            if($data['label'][0] == ':') $data['label'] = substr($data['label'],1);
        }

        $data['date'] = date('Y-m-d',$unix_date);
        $data['time'] = date('H:i',$unix_date);

        $data['label'] = trim($data['label']);
        return $data;
    } else return false;
}

function save_data($data) {
    if(isset($data['date'])) {
        if($data['label'] != '' OR $data['info'] != '') {
            scraperwiki::save_sqlite(array('date','time'),$data);
            echo "\t".$data['startdate'].': '.$data['label'].' / '.$data['label'].$data['url']."\n";
            return true;
        } else return false;
    } else return false;
}
?>
