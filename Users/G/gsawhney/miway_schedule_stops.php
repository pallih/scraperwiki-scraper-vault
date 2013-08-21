<?php
$tablename = "miway20121004";

require 'scraperwiki/simple_html_dom.php';


$html = scraperWiki::scrape("http://m.miway.ca/routes.jsp");           
$dom = new simple_html_dom();
$dom->load($html);

$count = 0;
$toplinks = $dom->find('table tr td a[href^=routeStops.jsp]');
usort($toplinks,"toplinks_sort");

$tables = scraperwiki::show_tables();
if ( (count($tables) > 0) && ($tables[$tablename]) ) { 
    $lastruninfo = scraperwiki::select("* FROM ".$tablename." ORDER BY routeid DESC LIMIT 1");
    $lastrouteid = $lastruninfo[0]["routeid"];
} else {
    //this is a fresh run
    $lastrouteid = -1;
}

foreach($toplinks as $data){
    list($routeid,$nothing,$routename) = explode(" ",$data->innertext,3);

//    if ($routeid >= $lastrouteid) {
    if ($routeid > 91) {
        $cleanlink = preg_replace('/;jsessionid=[A-Z0-9]*/i','',$data->href);  
        print("VISITING http://m.miway.ca/".$cleanlink . "\n");
        $route_html_content = scraperwiki::scrape("http://m.miway.ca/".$cleanlink);
        $route_html = str_get_html($route_html_content);
        foreach ($route_html->find('a[href^=nextPassingTimes]') as $el) {           
            if (preg_match('/sId=([0-9]*)&id=([0-9]*_[A-Za-z]*)/',$el,$stopmatches)) {
                $stopid = $stopmatches[1];
                $routeex = $stopmatches[2];
                list($anothing,$bnothing,$stopname) = explode(" ",$el->innertext,3);

                print("VISITING http://m.miway.ca/fullSchedule.jsp?sId=".$stopid."&id=".$routeex . "\n");

                $stop_html_content = scraperwiki::scrape("http://m.miway.ca/fullSchedule.jsp?sId=".$stopid."&id=".$routeex);
                $stop_html = str_get_html($stop_html_content);

                unset($stoptimes);
                if (!is_object($stop_html)) {
                    break; // this keeps the script going even if we get some bad data
                }
                foreach ($stop_html->find('td[width=50%]') as $box) {
                    $stoptimesarray = explode('<br/>',$box->innertext);
                    foreach ($stoptimesarray as $stoptime) {
                        if (preg_match("/([0-9][0-9]?:[0-9][0-9][AP]M)/",$stoptime,$timematches)) {
                            $goodtime = $timematches[1];
                            $stoptimes[] = date("H:i", strtotime(trim($goodtime)));
                        } else {
                            //possible parse error, but probably data we don't want
                        }
                    }
                }

                //here's where we store what's in stoptimes
                if (is_array($stoptimes)) {
                    foreach ($stoptimes as $thisstop) {
//print("saving record for ".$thisstop." / ".$routeid." / ".$stopid."\n");

                        scraperwiki::save_sqlite(array('departure_time','routeid','stopid'), array("departure_time"=>$thisstop,"routeid"=>$routeid,"stopid"=>$stopid,"stopname"=>$stopname), $table_name=$tablename, $verbose=2);
                    }
                }
            }
        }
    } else {
        print("(skipping route ".$routeid.") \n");
    }
}

function toplinks_sort($aa,$bb) {
    $a = substr($aa->innertext,0, strpos($aa->innertext,' '));
    $b = substr($bb->innertext,0, strpos($bb->innertext,' '));
    if ($a == $b) {
        return 0;
    }
    return ($a < $b) ? -1 : 1;
}
?>
