<?php
function processPostcode($pcode) {
    if (preg_match("/\A(\w{1,2}\d{1,2}\w?){1}(?<sp>\s{0,3})?(\d\w{2}){1}$/", $pcode, $m)) {
        return $m;
    } else {
        return false;
    }
}


$url = "http://www.youfind.me.uk/directory/Search.aspx?Mode=Detail&ActivityID=";
$pageid = 2551;
require  'scraperwiki/simple_html_dom.php';
$organisationDom = new simple_html_dom();
$activityDom = new simple_html_dom();
for ($j=$pageid; $j<5000; $j++) {
    $activityDom->load(scraperwiki::scrape($url.$j));
    $f = $activityDom->find("h1[@class=headercolor]");
    if ($f[0]->innertext == "Welcome To YouFind") {
        continue;
    }
    $organisation = array();
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblOrganisationName]");
    $organisation['name'] = strip_tags($f[0]->innertext);
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblOrgAccreditations]/a");
    if (!isset($f[0])) {
        $f = $activityDom->find("/span[@id=ActivityDetail1_lblOrganisationName]/a");
    } else {
        $fA = $activityDom->find("/span[@id=ActivityDetail1_lblOrgAccreditations]/a/img");
        $organisation['image'] = "http://www.youfind.me.uk/directory/".$fA[0]->src;
        $f = $activityDom->find("/span[@id=ActivityDetail1_lblOrgAccreditations]/a");
    }
    $organisation['link'] = $f[0]->href;

    
    
        
    $venue = array();
    $f = $activityDom->find("input[@name=ActivityDetail1:hdnEasting]");
    $venue['easting'] = $f[0]->value;
    $f = $activityDom->find("input[@name=ActivityDetail1:hdnNorthing]");
    $venue['northing'] = $f[0]->value;
    $f = $activityDom->find("input[@name=__VIEWSTATE]");
    $state = $f[0]->value;
    $fA = $activityDom->find("input[@name=ActivityDetail1:hdnSessionID]");
    $fB = $activityDom->find("input[@name=ActivityDetail1:hdnActivityID]");
    $fC = $activityDom->find("input[@name=ActivityDetail1:hdnOrgID]");
    $organisation['id'] = $fC[0]->value;
    $fD = $activityDom->find("input[@name=ActivityDetail1:hdnVenueID]");
    $venue['id'] = $fD[0]->value;
    $fE = $activityDom->find("input[@name=ActivityDetail1:hdnActivityLive]");
    $ch = curl_init($url.$j);
    curl_setopt($ch, CURLOPT_POSTFIELDS, array(
         "__VIEWSTATE"=>$state,
         "ActivityDetail1:btnOrgDetail.x"=>5,
         "ActivityDetail1:btnOrgDetail.y"=>5,
         "ActivityDetail1:hdnSessionID"=>$fA[0]->value,
         "ActivityDetail1:hdnActivityID"=>$fB[0]->value,
         "ActivityDetail1:hdnOrgID"=>$fC[0]->value,
         "ActivityDetail1:hdnVenueID"=>$fD[0]->value,
         "ActivityDetail1:hdnActivityLive"=>$fE[0]->value
        ));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $organisationDom->load(curl_exec($ch));
    
    $addr = $organisationDom->find("/span[@id=ActivityDetail1_lblOrgAddress]");
    $addr = $addr[0];
    $addr_array = explode("<br>", $addr->innertext);
    $newAddrArr = array();
    foreach ($addr_array as $a) {
        $newAddrArr = array_merge($newAddrArr, explode(",", $a));
    }
    $addr_array = $newAddrArr;
    $cursor = count($addr_array)-1;
    if (processPostcode(trim($addr_array[$cursor])) !== false) {
        $venue['postcode'] = trim($addr_array[$cursor]);
        $cursor--;
    }
    $venue['county'] = $addr_array[$cursor];
    $cursor--;
    $venue['city'] = $addr_array[$cursor];
    
    for ($i=1; $i<$cursor; $i++) {
        $venue['address_'.$i] = $addr_array[$i];
    }




    $cntct = $organisationDom->find("/span[@id=ActivityDetail1_lblOrgContact]");
    $cntct = explode("&nbsp;", $cntct[0]->innertext);
    $contact = array();
    for ($i=0; $i<count($cntct); $i++) {
        switch (strip_tags($cntct[$i])) {
            case "Contact Name:":
                $contact['name'] = strip_tags($cntct[$i+1]);
                $i++;
                break;
            case "Position:": 
                $contact['position'] = strip_tags($cntct[$i+1]);
                $i++;
                break;
            case "Telephone:":
                $contact['phone'] = strip_tags($cntct[$i+1]);
                $i++;
                break;
            case "Email Address:":
                $contact['email'] = strip_tags($cntct[$i+1]);
                $i++;
                break;
        }
    }
    $contact['venue'] = $venue['id'];

    
    $activity = array();
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblPageHeader]");
    $activity['name'] = $f[0]->innertext;

    $f = $activityDom->find("/span[@id=ActivityDetail1_lblActivityDesc]");
    $fA = $activityDom->find("/span[@id=ActivityDetail1_lblActivityDescPhoto]");
    if (!isset($f[0])) {
        $f = $fA;
    }

    $activity['description'] = $f[0]->innertext;
    
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblTheDates]");

    $start = DateTime::createFromFormat("l d/m/Y (H#i - ?????)", $f[0]->innertext);
    $end = DateTime::createFromFormat("l d/m/Y (????? - H#i)", $f[0]->innertext);

    if ($start === false) {
        $start = DateTime::createFromFormat("l d/m/Y", $f[0]->innertext);
        $end = DateTime::createFromFormat("l d/m/Y", $f[0]->innertext);
    }
    
    if ($start === false) {
        preg_match("/(\w+ \d+\/\d+\/\d+) to (\w+ \d+\/\d+\/\d+) \((\d+:\d+) - (\d+:\d+)\)/", $f[0]->innertext, $m);
        $start = DateTime::createFromFormat("l d/m/Y H#i", $m[1]." ".$m[3]);
        $end = DateTime::createFromFormat("l d/m/Y H#i", $m[2]." ".$m[4]);
    }

    $f = $activityDom->find("/span[@id=ActivityDetail1_lblCategory]");
    $activity['category'] = $f[0]->innertext;
    $f = $activityDom->find("/table[@id=ActivityDetail1_tblCalendar]/tr/td/table/tr/td");
    if (count($f) > 0) {
        $f = $f[0]->innertext;
        preg_match_all("/\d+:\d+/", $f, $time);
        if (strpos($f, "Every Week") !== false) {
            $activity['INTERVAL'] = 1;
        } else if (strpos($f, "Every Fortnight") !== false) {
            $activity['INTERVAL'] = 2;
        } elseif (preg_match("/Every (\d+) Weeks/", $f, $we)) {
            $activity['INTERVAL'] = $we[1][0];
        } else {
            $activity['INTERVAL'] = -1;
        }
    } else {
        $activity['INTERVAL'] = -2;
    }

    if ($activity['INTERVAL'] > -1) {
        $activity['FREQ'] = "WEEKLY";
        $e = explode(" ", utf8_decode(strip_tags(html_entity_decode($f))));
        $ical = array("Monday"=>"MO", "Tuesday"=>"TU", "Wednesday"=>"WE", "Thursday"=>"TH", "Friday"=>"FR", "Saturday"=>"SA", "Sunday"=>"SU");
        $activity['BYDAY'] = $ical[trim($e[0], "?")];
        $activity['COUNT'] = -1;




        $activity['DTSTART'] = $start->getTimestamp();
        $activity['DTEND'] = $end->getTimestamp();
        if (strpos($f, "term time only") !== false) {
            $activity['termtime'] = true;
        } else {
            $activity['termtime'] = false;
        }
    } else {
        $activity['FREQ'] = "DAILY";
        $activity['BYDAY'] = "";
        $ee = $end;
        $activity['DTSTART'] = $start->getTimestamp();
        $start->setTime(0, 0);
        $end->setTime(0,0);
        $activity['COUNT'] = $start->diff($end)->format("%a")+1;
        $ee->setDate($start->format("Y"), $start->format("m"), $start->format("d"));
        $activity['INTERVAL'] = 1;
        $activity['DTEND'] = $ee->getTimestamp();
        $activity['termtime'] = false;
    }
    
    $activity['organisation'] = $organisation['id'];
    $activity['venue'] = $venue['id'];
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblAgeRange]");
    preg_match_all("/\d+/", $f[0]->innertext, $p);
    if (count($p[0]) == 2) {
        $activity['age_start']  =$p[0][0];
        $activity['age_end']  =$p[0][1];
    } else {
        $activity['age_start']  = $activity['age_end']  = -1;
        
    }
    $f = $activityDom->find("/input[@name=ActivityDetail1:hdnActivityID]");
    $activity['id'] = $f[0]->value;
    scraperwiki::save_sqlite(array("id"), $venue, "venue");
    scraperwiki::save_sqlite(array("id"), $organisation, "organisation");
    scraperwiki::save_sqlite(array("email"), $contact, "contact");
    scraperwiki::save_sqlite(array("id"), $activity, "activity");   
}

?>
<?php
function processPostcode($pcode) {
    if (preg_match("/\A(\w{1,2}\d{1,2}\w?){1}(?<sp>\s{0,3})?(\d\w{2}){1}$/", $pcode, $m)) {
        return $m;
    } else {
        return false;
    }
}


$url = "http://www.youfind.me.uk/directory/Search.aspx?Mode=Detail&ActivityID=";
$pageid = 2551;
require  'scraperwiki/simple_html_dom.php';
$organisationDom = new simple_html_dom();
$activityDom = new simple_html_dom();
for ($j=$pageid; $j<5000; $j++) {
    $activityDom->load(scraperwiki::scrape($url.$j));
    $f = $activityDom->find("h1[@class=headercolor]");
    if ($f[0]->innertext == "Welcome To YouFind") {
        continue;
    }
    $organisation = array();
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblOrganisationName]");
    $organisation['name'] = strip_tags($f[0]->innertext);
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblOrgAccreditations]/a");
    if (!isset($f[0])) {
        $f = $activityDom->find("/span[@id=ActivityDetail1_lblOrganisationName]/a");
    } else {
        $fA = $activityDom->find("/span[@id=ActivityDetail1_lblOrgAccreditations]/a/img");
        $organisation['image'] = "http://www.youfind.me.uk/directory/".$fA[0]->src;
        $f = $activityDom->find("/span[@id=ActivityDetail1_lblOrgAccreditations]/a");
    }
    $organisation['link'] = $f[0]->href;

    
    
        
    $venue = array();
    $f = $activityDom->find("input[@name=ActivityDetail1:hdnEasting]");
    $venue['easting'] = $f[0]->value;
    $f = $activityDom->find("input[@name=ActivityDetail1:hdnNorthing]");
    $venue['northing'] = $f[0]->value;
    $f = $activityDom->find("input[@name=__VIEWSTATE]");
    $state = $f[0]->value;
    $fA = $activityDom->find("input[@name=ActivityDetail1:hdnSessionID]");
    $fB = $activityDom->find("input[@name=ActivityDetail1:hdnActivityID]");
    $fC = $activityDom->find("input[@name=ActivityDetail1:hdnOrgID]");
    $organisation['id'] = $fC[0]->value;
    $fD = $activityDom->find("input[@name=ActivityDetail1:hdnVenueID]");
    $venue['id'] = $fD[0]->value;
    $fE = $activityDom->find("input[@name=ActivityDetail1:hdnActivityLive]");
    $ch = curl_init($url.$j);
    curl_setopt($ch, CURLOPT_POSTFIELDS, array(
         "__VIEWSTATE"=>$state,
         "ActivityDetail1:btnOrgDetail.x"=>5,
         "ActivityDetail1:btnOrgDetail.y"=>5,
         "ActivityDetail1:hdnSessionID"=>$fA[0]->value,
         "ActivityDetail1:hdnActivityID"=>$fB[0]->value,
         "ActivityDetail1:hdnOrgID"=>$fC[0]->value,
         "ActivityDetail1:hdnVenueID"=>$fD[0]->value,
         "ActivityDetail1:hdnActivityLive"=>$fE[0]->value
        ));
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $organisationDom->load(curl_exec($ch));
    
    $addr = $organisationDom->find("/span[@id=ActivityDetail1_lblOrgAddress]");
    $addr = $addr[0];
    $addr_array = explode("<br>", $addr->innertext);
    $newAddrArr = array();
    foreach ($addr_array as $a) {
        $newAddrArr = array_merge($newAddrArr, explode(",", $a));
    }
    $addr_array = $newAddrArr;
    $cursor = count($addr_array)-1;
    if (processPostcode(trim($addr_array[$cursor])) !== false) {
        $venue['postcode'] = trim($addr_array[$cursor]);
        $cursor--;
    }
    $venue['county'] = $addr_array[$cursor];
    $cursor--;
    $venue['city'] = $addr_array[$cursor];
    
    for ($i=1; $i<$cursor; $i++) {
        $venue['address_'.$i] = $addr_array[$i];
    }




    $cntct = $organisationDom->find("/span[@id=ActivityDetail1_lblOrgContact]");
    $cntct = explode("&nbsp;", $cntct[0]->innertext);
    $contact = array();
    for ($i=0; $i<count($cntct); $i++) {
        switch (strip_tags($cntct[$i])) {
            case "Contact Name:":
                $contact['name'] = strip_tags($cntct[$i+1]);
                $i++;
                break;
            case "Position:": 
                $contact['position'] = strip_tags($cntct[$i+1]);
                $i++;
                break;
            case "Telephone:":
                $contact['phone'] = strip_tags($cntct[$i+1]);
                $i++;
                break;
            case "Email Address:":
                $contact['email'] = strip_tags($cntct[$i+1]);
                $i++;
                break;
        }
    }
    $contact['venue'] = $venue['id'];

    
    $activity = array();
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblPageHeader]");
    $activity['name'] = $f[0]->innertext;

    $f = $activityDom->find("/span[@id=ActivityDetail1_lblActivityDesc]");
    $fA = $activityDom->find("/span[@id=ActivityDetail1_lblActivityDescPhoto]");
    if (!isset($f[0])) {
        $f = $fA;
    }

    $activity['description'] = $f[0]->innertext;
    
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblTheDates]");

    $start = DateTime::createFromFormat("l d/m/Y (H#i - ?????)", $f[0]->innertext);
    $end = DateTime::createFromFormat("l d/m/Y (????? - H#i)", $f[0]->innertext);

    if ($start === false) {
        $start = DateTime::createFromFormat("l d/m/Y", $f[0]->innertext);
        $end = DateTime::createFromFormat("l d/m/Y", $f[0]->innertext);
    }
    
    if ($start === false) {
        preg_match("/(\w+ \d+\/\d+\/\d+) to (\w+ \d+\/\d+\/\d+) \((\d+:\d+) - (\d+:\d+)\)/", $f[0]->innertext, $m);
        $start = DateTime::createFromFormat("l d/m/Y H#i", $m[1]." ".$m[3]);
        $end = DateTime::createFromFormat("l d/m/Y H#i", $m[2]." ".$m[4]);
    }

    $f = $activityDom->find("/span[@id=ActivityDetail1_lblCategory]");
    $activity['category'] = $f[0]->innertext;
    $f = $activityDom->find("/table[@id=ActivityDetail1_tblCalendar]/tr/td/table/tr/td");
    if (count($f) > 0) {
        $f = $f[0]->innertext;
        preg_match_all("/\d+:\d+/", $f, $time);
        if (strpos($f, "Every Week") !== false) {
            $activity['INTERVAL'] = 1;
        } else if (strpos($f, "Every Fortnight") !== false) {
            $activity['INTERVAL'] = 2;
        } elseif (preg_match("/Every (\d+) Weeks/", $f, $we)) {
            $activity['INTERVAL'] = $we[1][0];
        } else {
            $activity['INTERVAL'] = -1;
        }
    } else {
        $activity['INTERVAL'] = -2;
    }

    if ($activity['INTERVAL'] > -1) {
        $activity['FREQ'] = "WEEKLY";
        $e = explode(" ", utf8_decode(strip_tags(html_entity_decode($f))));
        $ical = array("Monday"=>"MO", "Tuesday"=>"TU", "Wednesday"=>"WE", "Thursday"=>"TH", "Friday"=>"FR", "Saturday"=>"SA", "Sunday"=>"SU");
        $activity['BYDAY'] = $ical[trim($e[0], "?")];
        $activity['COUNT'] = -1;




        $activity['DTSTART'] = $start->getTimestamp();
        $activity['DTEND'] = $end->getTimestamp();
        if (strpos($f, "term time only") !== false) {
            $activity['termtime'] = true;
        } else {
            $activity['termtime'] = false;
        }
    } else {
        $activity['FREQ'] = "DAILY";
        $activity['BYDAY'] = "";
        $ee = $end;
        $activity['DTSTART'] = $start->getTimestamp();
        $start->setTime(0, 0);
        $end->setTime(0,0);
        $activity['COUNT'] = $start->diff($end)->format("%a")+1;
        $ee->setDate($start->format("Y"), $start->format("m"), $start->format("d"));
        $activity['INTERVAL'] = 1;
        $activity['DTEND'] = $ee->getTimestamp();
        $activity['termtime'] = false;
    }
    
    $activity['organisation'] = $organisation['id'];
    $activity['venue'] = $venue['id'];
    $f = $activityDom->find("/span[@id=ActivityDetail1_lblAgeRange]");
    preg_match_all("/\d+/", $f[0]->innertext, $p);
    if (count($p[0]) == 2) {
        $activity['age_start']  =$p[0][0];
        $activity['age_end']  =$p[0][1];
    } else {
        $activity['age_start']  = $activity['age_end']  = -1;
        
    }
    $f = $activityDom->find("/input[@name=ActivityDetail1:hdnActivityID]");
    $activity['id'] = $f[0]->value;
    scraperwiki::save_sqlite(array("id"), $venue, "venue");
    scraperwiki::save_sqlite(array("id"), $organisation, "organisation");
    scraperwiki::save_sqlite(array("email"), $contact, "contact");
    scraperwiki::save_sqlite(array("id"), $activity, "activity");   
}

?>
