<?php
//Outputs Hackney Council planning applications and appeals
scraperwiki::httpresponseheader('Content-Type', 'text/xml; charset=utf-8');

if(isset($_GET)) {
    reset($_GET);
    $i = 0;
    while (list($key, $val) = each ($_GET)) {
        if ($i == 0) {
            $req = '?' . $key . '=' . $val;
        }
        else {
            $req .= '&' . $key . '=' . $val;
        }   
     $i++;    
    }
}
else {
    $req = '';
}

if(isset($_GET['feed'])) {$feed = $_GET['feed'];} else {$feed = "combined";}
if(isset($_GET['strict'])) {$strict = TRUE; } else {$strict = FALSE;}
if(isset($_GET['kml']) && ($_GET['kml'] == TRUE)) {$kml = TRUE;} else {$kml = FALSE;}
if(isset($_GET['wards'])){ //supply wards=ward1,ward2 for specific wards.
    $wards = explode(",", $_GET['wards']); 
    $wardcount = count($wards);
    for ($i = 0; $i < $wardcount; $i++){
        if ($i < 1) {
            $wardsql = 'WHERE (`Wards` LIKE "%'.$wards[$i].'%") ';
        }
        else {
            $wardsql .= 'OR (`Wards` LIKE "%'.$wards[$i].'%") ';
        }
    }         
}
else {
    $wardsql = "";
}
if ($feed == 'applications'){
scraperwiki::attach('hackney_planning_simpletest_browser_attempt_1'); 
$combined = scraperwiki::select('
    `Date received` AS `DATE`, 
    `Date valid`, 
    `Status`, 
    `Site Address` AS `ADDRESS`,
    `Agent name`, 
    `PK`, 
    `Proposal` AS `DESCRIPTION`, 
    `Date registered`, 
    `Date target`, 
    `Applicant name`, 
    `Application type`, 
    `Application Number` AS `REF`,
    `Latitude`, `Longitude`,
    `Wards`
    from `Planning_Applications` '.$wardsql.'
    ORDER BY `Date registered` DESC 
    LIMIT 20');
}
else if ($feed == 'appeals') {
scraperwiki::attach('hackney_planning_appeal_simpletest_browser'); 
$combined = scraperwiki::select('
    `Appeal Received Date` AS `DATE`,
    `Appeal Description` AS `DESCRIPTION`,
    `Site Address` AS `ADDRESS`,
    `Local Authority Reference` AS `REF`,
    `Restricted`,
    `PK`,
    `Latitude`, `Longitude`,
    `Wards`
    from `Planning_Appeals` '.$wardsql.'
    ORDER BY `Appeal Received Date` DESC 
    LIMIT 20');
}
else {

scraperwiki::attach('hackney_planning_simpletest_browser_attempt_1'); 
$apps = scraperwiki::select('
    `Date received` AS `DATE`, 
    `Date valid`, 
    `Status`, 
    `Site Address` AS `ADDRESS`,
    `Agent name`, 
    `PK`, 
    `Proposal` AS `DESCRIPTION`, 
    `Date registered`, 
    `Date target`, 
    `Applicant name`, 
    `Application type`, 
    `Application Number` AS `REF`,
    `Latitude`, `Longitude`,
    `Wards`
    from `Planning_Applications` '.$wardsql.'
    ORDER BY `Date registered` DESC 
    LIMIT 20');


scraperwiki::attach('hackney_planning_appeal_simpletest_browser'); 
$appeals = scraperwiki::select('
    `Appeal Received Date` AS `DATE`,
    `Appeal Description` AS `DESCRIPTION`,
    `Site Address` AS `ADDRESS`,
    `Local Authority Reference` AS `REF`,
    `Restricted`,
    `PK`,
    `Latitude`, `Longitude`,
    `Wards`
    from `Planning_Appeals` '.$wardsql.'
    ORDER BY `Appeal Received Date` DESC 
    LIMIT 20');

$combined = array_merge($apps, $appeals);

}
function date_sort($a, $b) {
return strcmp($a['DATE'], $b['DATE']);
}
usort($combined, "date_sort");

//print_r($combined);


// THIS IS ABSOLUTELY ESSENTIAL - DO NOT FORGET TO SET THIS 
@date_default_timezone_set("GMT"); 

$writer = new XMLWriter(); 
// Output directly to the user 

$writer->openURI('php://output'); 
$writer->startDocument('1.0'); 

$writer->setIndent(4); 

if ($kml == FALSE){ //do RSS
// declare it as an rss document 
$writer->startElement('rss'); 
$writer->writeAttribute('version', '2.0'); 
$writer->writeAttribute('xmlns:atom', 'http://www.w3.org/2005/Atom'); 
$writer->writeAttribute('xmlns:georss', 'http://www.georss.org/georss');

$writer->startElement("channel"); 
//---------------------------------------------------- 
//$writer->writeElement('ttl', '60'); 
$writer->writeElement('title', 'Latest Planning Applications'); 
$writer->writeElement('description', 'These are the latest planning applications and appeals from Hackney Council.'); 
$writer->writeElement('link', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/home.aspx'); 
$writer->writeElement('pubDate', date("D, d M Y H:i:s e")); 

// set self properties for validating RSS -- note, $_SERVER['QUERY_STRING'] seems not to work...
$writer->startElement('atom:link');
$writer->writeAttribute('href', 'https://views.scraperwiki.com/run/hackney_council_planning_and_appeals_rss_output/' . @$req);


//if (isset($_SERVER['QUERY_STRING'])) {$qs = $_SERVER['QUERY_STRING'];} else {$query_string = "";}
//$writer->writeAttribute('href', "https://views.scraperwiki.com/run/hackney_council_planning_and_appeals_rss_output/" . "?" . @$_SERVER['QUERY_STRING']);

$writer->writeAttribute('rel', 'self');
$writer->writeAttribute('type', 'application/rss+xml');
$writer->endElement();

//---------------------------------------------------- 

foreach ($combined as $item) { if (($strict == TRUE & (isset($item['Latitude']) & isset($item['Longitude']))) | $strict == FALSE) {

//---------------------------------------------------- 
$writer->startElement("item"); 
if (isset($item['Agent name'])) {$type = "Application";} else {$type = "Appeal";}
$writer->writeElement('title', $type.': '.$item['REF']); 
if ($type == "Application") {
        $writer->writeElement('link', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/PLDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
} else { //otherwise, Appeal
        $writer->writeElement('link', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20Appeals%20On-Line&TYPE=PL/APDetailsPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/APDetails.xslt&FT=Planning%20Application%20Appeals%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
}
$descriptionText = 'Address: '.$item['ADDRESS'];
if (isset($item['Wards'])){$descriptionText .='<br>Wards: '.$item['Wards'];}
$descriptionText .='<br>Description: '.$item['DESCRIPTION'];
$writer->writeElement('description', $descriptionText);
 
if ($type == "Application") {
        $writer->writeElement('guid', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/PLDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
} else { //otherwise, Appeal
        $writer->writeElement('guid', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20Appeals%20On-Line&TYPE=PL/APDetailsPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/APDetails.xslt&FT=Planning%20Application%20Appeals%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
}

$writer->writeElement('pubDate', DateTime::createFromFormat(DATE_ATOM, $item['DATE'])->format('r')); 

if (isset($item['Latitude']) & isset($item['Longitude'])) {$writer->writeElement('georss:point', $item['Latitude'] . " " . $item['Longitude']);}

$writer->startElement('category'); 
    $writer->writeAttribute('domain', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/home.aspx'); 
    if (isset($item['Agent name'])) $writer->text('Application'); else $writer->text('Appeal');
$writer->endElement(); // Category 

// End Item 
$writer->endElement(); 
//---------------------------------------------------- 
} //end strict checking
}
// End rss 
$writer->endElement(); 

} else if ($kml == TRUE) { //begin KML
$writer->startElement('kml'); 
$writer->writeAttribute('xmlns', 'http://www.opengis.net/kml/2.2'); 
//---------------------------------------------------- 

foreach ($combined as $item) { if (($strict == TRUE & (isset($item['Latitude']) & isset($item['Longitude']))) | $strict == FALSE) {
$writer->startElement('Placemark'); 
if (isset($item['Agent name'])) {$type = "Application";} else {$type = "Appeal";}
$writer->writeElement('name', $type.': '.$item['REF']); 
if ($type == "Application") {
        $the_link = 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/PLDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING';
} else { //otherwise, Appeal
        $the_link = 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20Appeals%20On-Line&TYPE=PL/APDetailsPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/APDetails.xslt&FT=Planning%20Application%20Appeals%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING';
}
$descriptionText = 'Address: '.$item['ADDRESS'];
if (isset($item['Wards'])){$descriptionText .='<br>Wards: '.$item['Wards'];}
$descriptionText .='<br/>Description: '.$item['DESCRIPTION'];
$descriptionText .='<br/><strong><a href="'.$the_link.'">More details...</a>';
$descriptionText .='<br/>Updated: '.DateTime::createFromFormat(DATE_ATOM, $item['DATE'])->format('r'); 
$writer->writeElement('description', $descriptionText);
 
if ($type == "Application") {
$writer->startElement("IconStyle");
    $writer->startElement("Icon");
        $writer->writeElement('href', 'http://maps.google.com/mapfiles/kml/paddle/wht-circle_maps.png');
        $writer->writeElement('scale', '1.0');
    $writer->endElement(); 
$writer->endElement(); 

} else {
$writer->startElement("IconStyle");
    $writer->startElement("Icon");
        $writer->writeElement('href', 'http://maps.google.com/mapfiles/kml/paddle/ylw-circle_maps.png');
        $writer->writeElement('scale', '1.0');
    $writer->endElement(); 
$writer->endElement(); 


}

if (isset($item['Latitude']) & isset($item['Longitude'])) {
$writer->startElement('Point');
$writer->writeElement('coordinates', $item['Longitude'] . "," . $item['Latitude']);
$writer->endElement();
}


// End Item 
$writer->endElement(); 
//---------------------------------------------------- 
} //end strict checking
}

$writer->endDocument();  //end kml

}

$writer->endDocument(); 

$writer->flush(); 
?><?php
//Outputs Hackney Council planning applications and appeals
scraperwiki::httpresponseheader('Content-Type', 'text/xml; charset=utf-8');

if(isset($_GET)) {
    reset($_GET);
    $i = 0;
    while (list($key, $val) = each ($_GET)) {
        if ($i == 0) {
            $req = '?' . $key . '=' . $val;
        }
        else {
            $req .= '&' . $key . '=' . $val;
        }   
     $i++;    
    }
}
else {
    $req = '';
}

if(isset($_GET['feed'])) {$feed = $_GET['feed'];} else {$feed = "combined";}
if(isset($_GET['strict'])) {$strict = TRUE; } else {$strict = FALSE;}
if(isset($_GET['kml']) && ($_GET['kml'] == TRUE)) {$kml = TRUE;} else {$kml = FALSE;}
if(isset($_GET['wards'])){ //supply wards=ward1,ward2 for specific wards.
    $wards = explode(",", $_GET['wards']); 
    $wardcount = count($wards);
    for ($i = 0; $i < $wardcount; $i++){
        if ($i < 1) {
            $wardsql = 'WHERE (`Wards` LIKE "%'.$wards[$i].'%") ';
        }
        else {
            $wardsql .= 'OR (`Wards` LIKE "%'.$wards[$i].'%") ';
        }
    }         
}
else {
    $wardsql = "";
}
if ($feed == 'applications'){
scraperwiki::attach('hackney_planning_simpletest_browser_attempt_1'); 
$combined = scraperwiki::select('
    `Date received` AS `DATE`, 
    `Date valid`, 
    `Status`, 
    `Site Address` AS `ADDRESS`,
    `Agent name`, 
    `PK`, 
    `Proposal` AS `DESCRIPTION`, 
    `Date registered`, 
    `Date target`, 
    `Applicant name`, 
    `Application type`, 
    `Application Number` AS `REF`,
    `Latitude`, `Longitude`,
    `Wards`
    from `Planning_Applications` '.$wardsql.'
    ORDER BY `Date registered` DESC 
    LIMIT 20');
}
else if ($feed == 'appeals') {
scraperwiki::attach('hackney_planning_appeal_simpletest_browser'); 
$combined = scraperwiki::select('
    `Appeal Received Date` AS `DATE`,
    `Appeal Description` AS `DESCRIPTION`,
    `Site Address` AS `ADDRESS`,
    `Local Authority Reference` AS `REF`,
    `Restricted`,
    `PK`,
    `Latitude`, `Longitude`,
    `Wards`
    from `Planning_Appeals` '.$wardsql.'
    ORDER BY `Appeal Received Date` DESC 
    LIMIT 20');
}
else {

scraperwiki::attach('hackney_planning_simpletest_browser_attempt_1'); 
$apps = scraperwiki::select('
    `Date received` AS `DATE`, 
    `Date valid`, 
    `Status`, 
    `Site Address` AS `ADDRESS`,
    `Agent name`, 
    `PK`, 
    `Proposal` AS `DESCRIPTION`, 
    `Date registered`, 
    `Date target`, 
    `Applicant name`, 
    `Application type`, 
    `Application Number` AS `REF`,
    `Latitude`, `Longitude`,
    `Wards`
    from `Planning_Applications` '.$wardsql.'
    ORDER BY `Date registered` DESC 
    LIMIT 20');


scraperwiki::attach('hackney_planning_appeal_simpletest_browser'); 
$appeals = scraperwiki::select('
    `Appeal Received Date` AS `DATE`,
    `Appeal Description` AS `DESCRIPTION`,
    `Site Address` AS `ADDRESS`,
    `Local Authority Reference` AS `REF`,
    `Restricted`,
    `PK`,
    `Latitude`, `Longitude`,
    `Wards`
    from `Planning_Appeals` '.$wardsql.'
    ORDER BY `Appeal Received Date` DESC 
    LIMIT 20');

$combined = array_merge($apps, $appeals);

}
function date_sort($a, $b) {
return strcmp($a['DATE'], $b['DATE']);
}
usort($combined, "date_sort");

//print_r($combined);


// THIS IS ABSOLUTELY ESSENTIAL - DO NOT FORGET TO SET THIS 
@date_default_timezone_set("GMT"); 

$writer = new XMLWriter(); 
// Output directly to the user 

$writer->openURI('php://output'); 
$writer->startDocument('1.0'); 

$writer->setIndent(4); 

if ($kml == FALSE){ //do RSS
// declare it as an rss document 
$writer->startElement('rss'); 
$writer->writeAttribute('version', '2.0'); 
$writer->writeAttribute('xmlns:atom', 'http://www.w3.org/2005/Atom'); 
$writer->writeAttribute('xmlns:georss', 'http://www.georss.org/georss');

$writer->startElement("channel"); 
//---------------------------------------------------- 
//$writer->writeElement('ttl', '60'); 
$writer->writeElement('title', 'Latest Planning Applications'); 
$writer->writeElement('description', 'These are the latest planning applications and appeals from Hackney Council.'); 
$writer->writeElement('link', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/home.aspx'); 
$writer->writeElement('pubDate', date("D, d M Y H:i:s e")); 

// set self properties for validating RSS -- note, $_SERVER['QUERY_STRING'] seems not to work...
$writer->startElement('atom:link');
$writer->writeAttribute('href', 'https://views.scraperwiki.com/run/hackney_council_planning_and_appeals_rss_output/' . @$req);


//if (isset($_SERVER['QUERY_STRING'])) {$qs = $_SERVER['QUERY_STRING'];} else {$query_string = "";}
//$writer->writeAttribute('href', "https://views.scraperwiki.com/run/hackney_council_planning_and_appeals_rss_output/" . "?" . @$_SERVER['QUERY_STRING']);

$writer->writeAttribute('rel', 'self');
$writer->writeAttribute('type', 'application/rss+xml');
$writer->endElement();

//---------------------------------------------------- 

foreach ($combined as $item) { if (($strict == TRUE & (isset($item['Latitude']) & isset($item['Longitude']))) | $strict == FALSE) {

//---------------------------------------------------- 
$writer->startElement("item"); 
if (isset($item['Agent name'])) {$type = "Application";} else {$type = "Appeal";}
$writer->writeElement('title', $type.': '.$item['REF']); 
if ($type == "Application") {
        $writer->writeElement('link', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/PLDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
} else { //otherwise, Appeal
        $writer->writeElement('link', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20Appeals%20On-Line&TYPE=PL/APDetailsPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/APDetails.xslt&FT=Planning%20Application%20Appeals%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
}
$descriptionText = 'Address: '.$item['ADDRESS'];
if (isset($item['Wards'])){$descriptionText .='<br>Wards: '.$item['Wards'];}
$descriptionText .='<br>Description: '.$item['DESCRIPTION'];
$writer->writeElement('description', $descriptionText);
 
if ($type == "Application") {
        $writer->writeElement('guid', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/PLDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
} else { //otherwise, Appeal
        $writer->writeElement('guid', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20Appeals%20On-Line&TYPE=PL/APDetailsPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/APDetails.xslt&FT=Planning%20Application%20Appeals%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');
}

$writer->writeElement('pubDate', DateTime::createFromFormat(DATE_ATOM, $item['DATE'])->format('r')); 

if (isset($item['Latitude']) & isset($item['Longitude'])) {$writer->writeElement('georss:point', $item['Latitude'] . " " . $item['Longitude']);}

$writer->startElement('category'); 
    $writer->writeAttribute('domain', 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/home.aspx'); 
    if (isset($item['Agent name'])) $writer->text('Application'); else $writer->text('Appeal');
$writer->endElement(); // Category 

// End Item 
$writer->endElement(); 
//---------------------------------------------------- 
} //end strict checking
}
// End rss 
$writer->endElement(); 

} else if ($kml == TRUE) { //begin KML
$writer->startElement('kml'); 
$writer->writeAttribute('xmlns', 'http://www.opengis.net/kml/2.2'); 
//---------------------------------------------------- 

foreach ($combined as $item) { if (($strict == TRUE & (isset($item['Latitude']) & isset($item['Longitude']))) | $strict == FALSE) {
$writer->startElement('Placemark'); 
if (isset($item['Agent name'])) {$type = "Application";} else {$type = "Appeal";}
$writer->writeElement('name', $type.': '.$item['REF']); 
if ($type == "Application") {
        $the_link = 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/PLDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING';
} else { //otherwise, Appeal
        $the_link = 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20Appeals%20On-Line&TYPE=PL/APDetailsPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/APDetails.xslt&FT=Planning%20Application%20Appeals%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING';
}
$descriptionText = 'Address: '.$item['ADDRESS'];
if (isset($item['Wards'])){$descriptionText .='<br>Wards: '.$item['Wards'];}
$descriptionText .='<br/>Description: '.$item['DESCRIPTION'];
$descriptionText .='<br/><strong><a href="'.$the_link.'">More details...</a>';
$descriptionText .='<br/>Updated: '.DateTime::createFromFormat(DATE_ATOM, $item['DATE'])->format('r'); 
$writer->writeElement('description', $descriptionText);
 
if ($type == "Application") {
$writer->startElement("IconStyle");
    $writer->startElement("Icon");
        $writer->writeElement('href', 'http://maps.google.com/mapfiles/kml/paddle/wht-circle_maps.png');
        $writer->writeElement('scale', '1.0');
    $writer->endElement(); 
$writer->endElement(); 

} else {
$writer->startElement("IconStyle");
    $writer->startElement("Icon");
        $writer->writeElement('href', 'http://maps.google.com/mapfiles/kml/paddle/ylw-circle_maps.png');
        $writer->writeElement('scale', '1.0');
    $writer->endElement(); 
$writer->endElement(); 


}

if (isset($item['Latitude']) & isset($item['Longitude'])) {
$writer->startElement('Point');
$writer->writeElement('coordinates', $item['Longitude'] . "," . $item['Latitude']);
$writer->endElement();
}


// End Item 
$writer->endElement(); 
//---------------------------------------------------- 
} //end strict checking
}

$writer->endDocument();  //end kml

}

$writer->endDocument(); 

$writer->flush(); 
?>