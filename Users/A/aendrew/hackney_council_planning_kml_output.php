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
    from `Planning_Applications`  '.$wardsql.'
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

$writer->startElement('kml'); 
$writer->writeAttribute('xmlns', 'http://www.opengis.net/kml/2.2'); 
$writer->startElement('Document'); 
//---------------------------------------------------- 

foreach ($combined as $item) {
$writer->startElement('Placemark'); 
if (isset($item['Agent name'])) {$type = "Application";} else {$type = "Appeal";}
$writer->writeElement('name', $type.': '.$item['REF']); 
if ($type == "Application") {
        $the_link = 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/PLDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING';
} else { //otherwise, Appeal
        $the_link = 'http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20Appeals%20On-Line&TYPE=PL/APDetailsPK.xml&PARAM0='.$item['PK'].'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/APDetails.xslt&FT=Planning%20Application%20Appeals%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING';
}
$descriptionText = '<br/><b>Address:</b> '.$item['ADDRESS'];
if (isset($item['Wards'])){$descriptionText .='<br><b>Wards:</b> '.$item['Wards'];}
$descriptionText .='<br/><b>Description:</b> '.$item['DESCRIPTION'];
$descriptionText .='<br/><b>Updated:</b> '.DateTime::createFromFormat(DATE_ATOM, $item['DATE'])->format('r'); 
$descriptionText .='<br/><br/><b><a href="'.$the_link.'">More details...</a></b>';
$writer->writeElement('description', $descriptionText);
 
$writer->startElement("Style");
if ($type == "Application") {
$writer->startElement("IconStyle");
    $writer->startElement("Icon");
        $writer->writeElement('href', 'http://maps.google.com/mapfiles/kml/paddle/blu-circle_maps.png');
//        $writer->writeElement('scale', '1.0');
    $writer->endElement(); 
$writer->endElement(); 

} else {
$writer->startElement("IconStyle");
    $writer->startElement("Icon");
        $writer->writeElement('href', 'http://maps.google.com/mapfiles/kml/paddle/pink-circle_maps.png');
//        $writer->writeElement('scale', '1.0');
    $writer->endElement(); 
$writer->endElement(); 
}

$writer->endElement();  //Style

if (isset($item['Latitude']) & isset($item['Longitude'])) {
$writer->startElement('Point');
$writer->writeElement('coordinates', $item['Longitude'] . "," . $item['Latitude']);
$writer->endElement();
}


// End Item 
$writer->endElement(); 
//---------------------------------------------------- 

}
$writer->endDocument();  //end document
$writer->endDocument();  //end kml



$writer->endDocument(); 

$writer->flush(); 
?>