<?php
$key= array('year', 'month', 'day', 'hour');

function test($hour,$day,$month,$year,$d,$d2){
    echo "Test: $year,$month,$day,$hour,$d2,$d\n";
}

function save($hour,$day,$month,$year,$d,$d2){
    global $key;
    $data = array('year' => $year,
                  'month' => $month,
                  'day' => $day,
                  'hour' => $hour,
                  'direction' => $d2,
                  'degree' => $d);                
    scraperwiki::save($key, $data);
}

/*
The  direction (true or geographic, not magnetic) from which the  wind  blows. Expressed in ten's of degrees, 9 means 90 degrees true or  an east  wind, and 36 means 360 degrees true or a wind blowing from  the  geographic north pole. A value of zero (0) denotes a calm wind.              
*/
function deg2nesw($v){
    $v=(int)$v;
    $v=$v*10;
    if($v==0){
        return "";
    }else if($v<45 || $v>315){
        return "N";
    }else if($v<135 && $v>45){
        return "E";
    }else if($v<225 && $v>135){
        return "S";
    }else if($v<315 && $v>225){
        return "W";
    }
}

/*
 N=  338 to 22, excluding 0 (which denotes calm)
 NE= 23 to 67
 E= 68 to 112
 SE = 113 to 157
 S = 158 to 202
 SW = 203 to 247
 W = 248 to 292
 NW = 293 to 337
*/
function deg2nesw8($v){
    $v=(int)$v;
    $v=$v*10;
    if($v==0){
        return "";
    }else if($v<=22 || $v>=338){
        return "N";
    }else if($v<=67 && $v>=23){
        return "NE";
    }else if($v<=112 && $v>=68){
        return "E";
    }else if($v<=157 && $v>=113){
        return "SE";
    }else if($v<=202 && $v>=158){
        return "S";
    }else if($v<=247 && $v>=203){
        return "SW";
    }else if($v<=292 && $v>=248){
        return "W";
    }else if($v<=337 && $v>=293){
        return "NW";
    }else{
        echo "unexpected deg $v";
        exit(-1);
    }
}

function scrapeDay($day,$month,$year){
    $html = scraperwiki::scrape('http://www.climate.weatheroffice.gc.ca/climateData/hourlydata_e.html?timeframe=1&Prov=XX&StationID=889&Year='.$year.'&Month='.$month.'&Day='.$day);
    $pattern = '/\s+/i';
    $string = $html;
    $replacement = ' ';
    $string = preg_replace($pattern, $replacement, $string);
    if (strrpos($string,"unable to satisfy your request")){
        echo "No data for: $year/$month/$day\n";
        return;
    } else{        
        //
        //crop to the data table
        $pattern = '/^.+(\<table[^\<\>]+dataTable[^\<\>]+\>.+?\<\/table\>).+/i';
        $replacement = '$1';
        $string = preg_replace($pattern, $replacement, $string);
        //
        //split into lines on table rows
        $pattern = '/(<tr )/i';
        $replacement = "\n$1";
        $string = preg_replace($pattern, $replacement, $string);
        $string=preg_split('/\n/',$string);
        //
        //reduse to the hour and direction
        $pattern = '/.*?(\<td[^\<\>]*\>[^\<\>]*)(\<td[^\<\>]*\>[^\<\>]*\<\/td\>)(\<td[^\<\>]*\>[^\<\>]*\<\/td\>)(\<td[^\<\>]*\>[^\<\>]*\<\/td\>)(\<td[^\<\>]*\>[^\<\>]*\<\/td\>).*/i';
        $replacement = "$1\t$5";
        $string = preg_replace($pattern, $replacement, $string);
        //
        //trim off the tags
        $pattern = '/\<[^\<\>]*\>/i';
        $replacement = "";
        $string = preg_replace($pattern, $replacement, $string);
        //
        //cut off the header
        $pattern = '/\t/i';
        $string = preg_grep($pattern, $string);
        foreach ($string as $value){
            $value=explode("\t", $value);
            $hour=$value[0];
            $d=$value[1];
            $d2=deg2nesw8($d);
             #test($hour,$day,$month,$year,$d,$d2);
             save($hour,$day,$month,$year,$d,$d2);
        }
         echo "Scraped: $year/$month/$day\n";
    }
}

function scrape_the_last_days($n){
    $now=time();
    $sPerDay=24*60*60;
    for ( $i = 0; $i <$n; $i++) {
        $aDay="".date('Y-m-d', ($now-($i*$sPerDay)));
        $aDay=explode("-", $aDay);
        scrapeDay($aDay[2],$aDay[1],$aDay[0]);
    }
}

function scrape_a_test_day(){
    $day=1;
    $month=3;
    $year=2011;
    scrapeDay($day,$month,$year);
}

scrape_the_last_days(12);
#scrape_a_test_day();

?>


<?php
$key= array('year', 'month', 'day', 'hour');

function test($hour,$day,$month,$year,$d,$d2){
    echo "Test: $year,$month,$day,$hour,$d2,$d\n";
}

function save($hour,$day,$month,$year,$d,$d2){
    global $key;
    $data = array('year' => $year,
                  'month' => $month,
                  'day' => $day,
                  'hour' => $hour,
                  'direction' => $d2,
                  'degree' => $d);                
    scraperwiki::save($key, $data);
}

/*
The  direction (true or geographic, not magnetic) from which the  wind  blows. Expressed in ten's of degrees, 9 means 90 degrees true or  an east  wind, and 36 means 360 degrees true or a wind blowing from  the  geographic north pole. A value of zero (0) denotes a calm wind.              
*/
function deg2nesw($v){
    $v=(int)$v;
    $v=$v*10;
    if($v==0){
        return "";
    }else if($v<45 || $v>315){
        return "N";
    }else if($v<135 && $v>45){
        return "E";
    }else if($v<225 && $v>135){
        return "S";
    }else if($v<315 && $v>225){
        return "W";
    }
}

/*
 N=  338 to 22, excluding 0 (which denotes calm)
 NE= 23 to 67
 E= 68 to 112
 SE = 113 to 157
 S = 158 to 202
 SW = 203 to 247
 W = 248 to 292
 NW = 293 to 337
*/
function deg2nesw8($v){
    $v=(int)$v;
    $v=$v*10;
    if($v==0){
        return "";
    }else if($v<=22 || $v>=338){
        return "N";
    }else if($v<=67 && $v>=23){
        return "NE";
    }else if($v<=112 && $v>=68){
        return "E";
    }else if($v<=157 && $v>=113){
        return "SE";
    }else if($v<=202 && $v>=158){
        return "S";
    }else if($v<=247 && $v>=203){
        return "SW";
    }else if($v<=292 && $v>=248){
        return "W";
    }else if($v<=337 && $v>=293){
        return "NW";
    }else{
        echo "unexpected deg $v";
        exit(-1);
    }
}

function scrapeDay($day,$month,$year){
    $html = scraperwiki::scrape('http://www.climate.weatheroffice.gc.ca/climateData/hourlydata_e.html?timeframe=1&Prov=XX&StationID=889&Year='.$year.'&Month='.$month.'&Day='.$day);
    $pattern = '/\s+/i';
    $string = $html;
    $replacement = ' ';
    $string = preg_replace($pattern, $replacement, $string);
    if (strrpos($string,"unable to satisfy your request")){
        echo "No data for: $year/$month/$day\n";
        return;
    } else{        
        //
        //crop to the data table
        $pattern = '/^.+(\<table[^\<\>]+dataTable[^\<\>]+\>.+?\<\/table\>).+/i';
        $replacement = '$1';
        $string = preg_replace($pattern, $replacement, $string);
        //
        //split into lines on table rows
        $pattern = '/(<tr )/i';
        $replacement = "\n$1";
        $string = preg_replace($pattern, $replacement, $string);
        $string=preg_split('/\n/',$string);
        //
        //reduse to the hour and direction
        $pattern = '/.*?(\<td[^\<\>]*\>[^\<\>]*)(\<td[^\<\>]*\>[^\<\>]*\<\/td\>)(\<td[^\<\>]*\>[^\<\>]*\<\/td\>)(\<td[^\<\>]*\>[^\<\>]*\<\/td\>)(\<td[^\<\>]*\>[^\<\>]*\<\/td\>).*/i';
        $replacement = "$1\t$5";
        $string = preg_replace($pattern, $replacement, $string);
        //
        //trim off the tags
        $pattern = '/\<[^\<\>]*\>/i';
        $replacement = "";
        $string = preg_replace($pattern, $replacement, $string);
        //
        //cut off the header
        $pattern = '/\t/i';
        $string = preg_grep($pattern, $string);
        foreach ($string as $value){
            $value=explode("\t", $value);
            $hour=$value[0];
            $d=$value[1];
            $d2=deg2nesw8($d);
             #test($hour,$day,$month,$year,$d,$d2);
             save($hour,$day,$month,$year,$d,$d2);
        }
         echo "Scraped: $year/$month/$day\n";
    }
}

function scrape_the_last_days($n){
    $now=time();
    $sPerDay=24*60*60;
    for ( $i = 0; $i <$n; $i++) {
        $aDay="".date('Y-m-d', ($now-($i*$sPerDay)));
        $aDay=explode("-", $aDay);
        scrapeDay($aDay[2],$aDay[1],$aDay[0]);
    }
}

function scrape_a_test_day(){
    $day=1;
    $month=3;
    $year=2011;
    scrapeDay($day,$month,$year);
}

scrape_the_last_days(12);
#scrape_a_test_day();

?>


