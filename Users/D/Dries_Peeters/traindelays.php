<?php
    print "Create tables if not exists\n";
    scraperwiki::sqliteexecute("create table if not exists DelaysOnTrains (DATE string, TRAINNUMBER string, BEGIN_STATION string, END_STATION string, DEPARTURE_TIME string, TRAJECT int)");
    scraperwiki::sqliteexecute("create table if not exists Trajects (ID unsigned integer, STATION string, NORMAL_DEPARTURE_TIME string, DELAY string)");
    scraperwiki::sqlitecommit(); 

    // neem datum van gisteren
    $yesterday = date("d/m/Y", time() - (60*60*24) );
    $generalInfoCollected = false;
    $trainInfoCollected = false;
    
        
    //print_r(scraperwiki::sqliteexecute(" select max(ID) from Trajects"));
    $response = scraperwiki::sqliteexecute("select max(ID) from Trajects");
    $maxid = $response->data[0][0];
    if($maxid == "")
    {
         $maxid = 0;
    }
    $id = $maxid + 1;
    print "start ID: " . $id . "\n";

    // Voor elk treinnummer (1 tot 19999)
    for ($number = 1; $number < 20000; ++$number)
    {
        $url = trim(sprintf("http://www.railtime.be/mobile/HTML/TrainDetail.aspx?tid=%d&da=D&dt=%s&l=NL", $number, $yesterday));
        print "Checking URL: " . $url . "\n";
        $html = scraperwiki::scrape($url);
                  
        $from = "";
        $to = "";
        $date = $yesterday;
        $depTime = "";



        if(strpos($html, "errorMessage") === false)
        {
            print "Trainnumber: " . $number . "\n";
            preg_match_all('/<div class="logo">.*?<\/div>.*?<h1>(.*?)-&gt;(.*?) \[.*?<\/h1>/s',
                $html,
                $infolines, // will contain the blog posts
                PREG_SET_ORDER // formats data into an array of posts
                );
            
            foreach ($infolines as $info) {
                $generalInfoCollected = true;
                $from = trim($info[1]);
                $to = trim($info[2]);
                              
                print $from . " -> " . $to . " #" . $number . " " . $date . "\n";
            }

            preg_match_all('/<tr class=\' trainLeft rowHeightTraject.*?\'>.*?<td class="TrainColumnLocation .*?">.*?<\/td>.*?<td>.*?(<label|<a) class="Graylabel".*?>(.*?)(<\/label>|<\/a>).*?<\/td>.*?<td align="center">.*?<label>(.*?)<\/label>.*?<\/td>.*?<td align="left">.*?<label class="orange">(.*?)<\/label>.*?<\/td>.*?<\/tr>/s',
                    $html,
                    $stops,
                    PREG_SET_ORDER
                    );
            
            $stopcounter = 0;
            foreach ($stops as $stop) {
                $trainInfoCollected = true;
                $station = trim($stop[2]);
                $normalDepTime = trim($stop[4]);
                $delay = trim($stop[5]);                       
                
                if($stopcounter == 0)
                    $depTime = $normalDepTime;

                if (strlen($delay) == 0) {
                    $delay = "0";
                } else if ($delay[0] == "+") {
                    $delay = substr($delay, 1, -1);
                }
                
                print "INSERT IN TRAJECTS: " . $id . " | " . $station . " | " . $normalDepTime . " | " . $delay . "\n";
                scraperwiki::sqliteexecute("insert into Trajects values (?,?,?,?)", array($id, $station, $normalDepTime, $delay));
                scraperwiki::sqlitecommit();                
                $stopcounter++;
            }

            if($generalInfoCollected && $trainInfoCollected) {
                print "INSERT IN DELAYS_ON_TRAINS: " . $date . " | " . $number . " | " . $from . " | " . $to . " | " . $depTime . " | " . $id . "\n"; 
                scraperwiki::sqliteexecute("insert into DelaysOnTrains values (?,?,?,?,?,?)", array($date, $number, $from, $to, $depTime, $id));
                scraperwiki::sqlitecommit();                
                ++$id;
            }
            
            $generalInfoCollected = false;
            $trainInfoCollected = false;            
        }
   }
?>
<?php
    print "Create tables if not exists\n";
    scraperwiki::sqliteexecute("create table if not exists DelaysOnTrains (DATE string, TRAINNUMBER string, BEGIN_STATION string, END_STATION string, DEPARTURE_TIME string, TRAJECT int)");
    scraperwiki::sqliteexecute("create table if not exists Trajects (ID unsigned integer, STATION string, NORMAL_DEPARTURE_TIME string, DELAY string)");
    scraperwiki::sqlitecommit(); 

    // neem datum van gisteren
    $yesterday = date("d/m/Y", time() - (60*60*24) );
    $generalInfoCollected = false;
    $trainInfoCollected = false;
    
        
    //print_r(scraperwiki::sqliteexecute(" select max(ID) from Trajects"));
    $response = scraperwiki::sqliteexecute("select max(ID) from Trajects");
    $maxid = $response->data[0][0];
    if($maxid == "")
    {
         $maxid = 0;
    }
    $id = $maxid + 1;
    print "start ID: " . $id . "\n";

    // Voor elk treinnummer (1 tot 19999)
    for ($number = 1; $number < 20000; ++$number)
    {
        $url = trim(sprintf("http://www.railtime.be/mobile/HTML/TrainDetail.aspx?tid=%d&da=D&dt=%s&l=NL", $number, $yesterday));
        print "Checking URL: " . $url . "\n";
        $html = scraperwiki::scrape($url);
                  
        $from = "";
        $to = "";
        $date = $yesterday;
        $depTime = "";



        if(strpos($html, "errorMessage") === false)
        {
            print "Trainnumber: " . $number . "\n";
            preg_match_all('/<div class="logo">.*?<\/div>.*?<h1>(.*?)-&gt;(.*?) \[.*?<\/h1>/s',
                $html,
                $infolines, // will contain the blog posts
                PREG_SET_ORDER // formats data into an array of posts
                );
            
            foreach ($infolines as $info) {
                $generalInfoCollected = true;
                $from = trim($info[1]);
                $to = trim($info[2]);
                              
                print $from . " -> " . $to . " #" . $number . " " . $date . "\n";
            }

            preg_match_all('/<tr class=\' trainLeft rowHeightTraject.*?\'>.*?<td class="TrainColumnLocation .*?">.*?<\/td>.*?<td>.*?(<label|<a) class="Graylabel".*?>(.*?)(<\/label>|<\/a>).*?<\/td>.*?<td align="center">.*?<label>(.*?)<\/label>.*?<\/td>.*?<td align="left">.*?<label class="orange">(.*?)<\/label>.*?<\/td>.*?<\/tr>/s',
                    $html,
                    $stops,
                    PREG_SET_ORDER
                    );
            
            $stopcounter = 0;
            foreach ($stops as $stop) {
                $trainInfoCollected = true;
                $station = trim($stop[2]);
                $normalDepTime = trim($stop[4]);
                $delay = trim($stop[5]);                       
                
                if($stopcounter == 0)
                    $depTime = $normalDepTime;

                if (strlen($delay) == 0) {
                    $delay = "0";
                } else if ($delay[0] == "+") {
                    $delay = substr($delay, 1, -1);
                }
                
                print "INSERT IN TRAJECTS: " . $id . " | " . $station . " | " . $normalDepTime . " | " . $delay . "\n";
                scraperwiki::sqliteexecute("insert into Trajects values (?,?,?,?)", array($id, $station, $normalDepTime, $delay));
                scraperwiki::sqlitecommit();                
                $stopcounter++;
            }

            if($generalInfoCollected && $trainInfoCollected) {
                print "INSERT IN DELAYS_ON_TRAINS: " . $date . " | " . $number . " | " . $from . " | " . $to . " | " . $depTime . " | " . $id . "\n"; 
                scraperwiki::sqliteexecute("insert into DelaysOnTrains values (?,?,?,?,?,?)", array($date, $number, $from, $to, $depTime, $id));
                scraperwiki::sqlitecommit();                
                ++$id;
            }
            
            $generalInfoCollected = false;
            $trainInfoCollected = false;            
        }
   }
?>
