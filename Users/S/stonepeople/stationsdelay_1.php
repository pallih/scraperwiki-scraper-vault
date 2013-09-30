<?php

    scraperwiki::sqliteexecute("create table if not exists DelaysInStations (STATION string, DATE string, DESTINATION string, NORMAL_DEPARTURE_TIME string, DELAY string)");
    scraperwiki::sqlitecommit(); 


    // neem datum van gisteren
    $yesterday = date("d/m/Y", time() - (60*60*24) );

    // elk station afgaan (inlezen uit bestand)        
    $stations = array(  "Hasselt",
                        "Antwerpen-Centraal",
                        "Antwerpen-Berchem",
                        "Gent-Sint-Pieters",
                        "Brussel-Zuid",
                        "Brussel-Centraal",
                        "Mechelen", // sid = 810
                        "Brugge", // zelfde als voor lier. sid = 210
                        "Charleroi-Zuid",
                        "Gent-Dampoort",
                        "Kortrijk",
                        "Leuven",
                        "Lier", // voor lier extra sid (station id meegeven, aangezien hij niet weet wat er bedoelt wordt: lier, lierse, ...) sid = 732
                        "Luik-Guillemins",
                        "Luik-Paleis",
                        "Namen",
                        "Bergen", //  zelfde als bij lier. sid = 
                        "Sint-Truiden",
                        "Oostende",
                        "Blankenberge");
    
    foreach($stations as $station) {
        // elk uur afgaan: van 0:00 tot 23:00
        for ($i = 0; $i < 24; ++$i) {
            $hour = "" + $i;
            if (strlen ( $hour ) == 1)
                $hour = "0" . $hour;
            
            if($station == "Lier")
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&sid=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, "732", $yesterday, $hour));
            else if($station == "Bergen")
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&sid=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, "848", $yesterday, $hour));
            else if($station == "Brugge")
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&sid=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, "210", $yesterday, $hour));
            else if($station == "Mechelen")
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&sid=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, "810", $yesterday, $hour));
            else
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, $yesterday, $hour));
            print $url . "\n";
            $html = scraperwiki::scrape($url);
            
            if(strpos($html, "errorMessage") === false){
                preg_match_all(
                    '/<tr>.*?<td>.*?<label>(.*?)<\/label>.*?<label class="orange">(.*?)<\/label>.*?<\/td>.*?<td>.*?<label>(.*?)<\/label>.*?<label class="TrainType">.*?<\/label>.*?<div class="info">.*?<label class="orange">.*?<\/label>.*?<\/div>.*?<\/td>.*?<td style="text-align:center" rowspan=\'1\'>.*?<label>.*?<\/label>.*?<\/td>.*?<td rowspan="1">.*?<a class="button cmd blue" href=".*?">&gt;<\/a>.*?<\/td>.*?<\/tr>/s',
                    $html,
                    $trains, // will contain the blog posts
                    PREG_SET_ORDER // formats data into an array of posts
                );

                foreach ($trains as $train) {
                    $normalDepTime = trim($train[1]);
                    $delay = trim($train[2]);
                    $destination = trim($train[3]);

                    if (strlen($delay) == 0) {
                        $delay = "0";
                    } else if ($delay[0] == "+") {
                        $delay = substr($delay, 1, -1);
                    }

                    scraperwiki::sqliteexecute("insert into DelaysInStations  values (?,?,?,?,?)", array($station, $yesterday, $destination, $normalDepTime, $delay));
                    scraperwiki::sqlitecommit();
                    // do something with data
                    print $normalDepTime . " " . $delay . " " . $destination . "\n";
                        
                }
            }
        }
    }

    
?>
<?php

    scraperwiki::sqliteexecute("create table if not exists DelaysInStations (STATION string, DATE string, DESTINATION string, NORMAL_DEPARTURE_TIME string, DELAY string)");
    scraperwiki::sqlitecommit(); 


    // neem datum van gisteren
    $yesterday = date("d/m/Y", time() - (60*60*24) );

    // elk station afgaan (inlezen uit bestand)        
    $stations = array(  "Hasselt",
                        "Antwerpen-Centraal",
                        "Antwerpen-Berchem",
                        "Gent-Sint-Pieters",
                        "Brussel-Zuid",
                        "Brussel-Centraal",
                        "Mechelen", // sid = 810
                        "Brugge", // zelfde als voor lier. sid = 210
                        "Charleroi-Zuid",
                        "Gent-Dampoort",
                        "Kortrijk",
                        "Leuven",
                        "Lier", // voor lier extra sid (station id meegeven, aangezien hij niet weet wat er bedoelt wordt: lier, lierse, ...) sid = 732
                        "Luik-Guillemins",
                        "Luik-Paleis",
                        "Namen",
                        "Bergen", //  zelfde als bij lier. sid = 
                        "Sint-Truiden",
                        "Oostende",
                        "Blankenberge");
    
    foreach($stations as $station) {
        // elk uur afgaan: van 0:00 tot 23:00
        for ($i = 0; $i < 24; ++$i) {
            $hour = "" + $i;
            if (strlen ( $hour ) == 1)
                $hour = "0" . $hour;
            
            if($station == "Lier")
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&sid=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, "732", $yesterday, $hour));
            else if($station == "Bergen")
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&sid=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, "848", $yesterday, $hour));
            else if($station == "Brugge")
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&sid=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, "210", $yesterday, $hour));
            else if($station == "Mechelen")
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&sid=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, "810", $yesterday, $hour));
            else
                $url = trim(sprintf("http://www.railtime.be/mobile/HTML/StationDetail.aspx?sn=%s&dt=%s&ti=%s:00&da=D&l=NL", $station, $yesterday, $hour));
            print $url . "\n";
            $html = scraperwiki::scrape($url);
            
            if(strpos($html, "errorMessage") === false){
                preg_match_all(
                    '/<tr>.*?<td>.*?<label>(.*?)<\/label>.*?<label class="orange">(.*?)<\/label>.*?<\/td>.*?<td>.*?<label>(.*?)<\/label>.*?<label class="TrainType">.*?<\/label>.*?<div class="info">.*?<label class="orange">.*?<\/label>.*?<\/div>.*?<\/td>.*?<td style="text-align:center" rowspan=\'1\'>.*?<label>.*?<\/label>.*?<\/td>.*?<td rowspan="1">.*?<a class="button cmd blue" href=".*?">&gt;<\/a>.*?<\/td>.*?<\/tr>/s',
                    $html,
                    $trains, // will contain the blog posts
                    PREG_SET_ORDER // formats data into an array of posts
                );

                foreach ($trains as $train) {
                    $normalDepTime = trim($train[1]);
                    $delay = trim($train[2]);
                    $destination = trim($train[3]);

                    if (strlen($delay) == 0) {
                        $delay = "0";
                    } else if ($delay[0] == "+") {
                        $delay = substr($delay, 1, -1);
                    }

                    scraperwiki::sqliteexecute("insert into DelaysInStations  values (?,?,?,?,?)", array($station, $yesterday, $destination, $normalDepTime, $delay));
                    scraperwiki::sqlitecommit();
                    // do something with data
                    print $normalDepTime . " " . $delay . " " . $destination . "\n";
                        
                }
            }
        }
    }

    
?>
