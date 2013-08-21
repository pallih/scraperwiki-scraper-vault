<?php
//credit goes to my awesome girlfriend for being awesome.

if (!file_exists('simpletest/browser.php')){ //first need to download SimpleTest
        $data = file_get_contents("http://aendrew.com/sites/all/libraries/simpletest_1.1alpha3.tar.gz"); 
        file_put_contents("simpletest.tar.gz", $data);
        exec('tar -xzvf simpletest.tar.gz');
}
if (!file_exists('phpcoord-2.3.php')){ //next need to download phpCoord
        $data2 = file_get_contents("http://www.jstott.me.uk/phpcoord/phpcoord-2.3.tar.gz"); 
        file_put_contents("phpcoord-2.3.tar.gz", $data2);
        exec('tar -xzvf phpcoord-2.3.tar.gz');
}

    require_once('simpletest/browser.php');
    require_once('phpcoord-2.3.php');  //Here we go now!
    $browser = new SimpleBrowser();
    $browser->useCookies();
    $browser->get('http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/generalsearch.aspx?blah='.rand(1,99)); //the "blah" flag disables caching on SW.
    //$viewstate = $browser->getField('__VIEWSTATE');
    //$eventValidation = $browser->getField('__EVENTVALIDATION');
    //$browser->setField('__VIEWSTATE', $viewstate);
    //$browser->setField('__EVENTVALIDATION', $eventValidation);
    $browser->setField('cboSelectDateValue', 'DATE_RECEIVED');
    $browser->setField('cboMonths', '1');    
    $browser->setField('rbGroup', 'rbMonth');
    $browser->setField('cboDays', '7');
    $browser->clickSubmitByName('csbtnSearch');
    $url = $browser->getUrl();
    $xmlloc = 'http://apps.hackney.gov.uk' . preg_replace('/.*XMLLoc=(.*)$/', '\1', $url);
    $apps = simplexml_load_file($xmlloc);
    foreach ($apps->M3_DC_LIVE_GENERAL_QUERY_LIST as $app){

     /* COMMENTED OUT: old code to geolocate via postcode. Now handled via Eastings/Northings.
       $regex = "/([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)/";
        $address = (string) $app->SITE_ADDRESS;
        preg_match($regex, $address, $matches);
        if(isset($matches[0])){
            $coords = scraperwiki::gb_postcode_to_latlng($matches[0]);
        }*/
        $pk = &$app->PK;
        $appscrape = scraperwiki::scrape('http://apps.hackney.gov.uk/servapps/Northgate/PlanningExplorer/Generic/StdDetails.aspx?PT=Planning%20Applications%20On-Line&TYPE=PL/PlanningPK.xml&PARAM0='.$pk.'&XSLT=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/xslt/PL/PLDetails.xslt&FT=Planning%20Application%20Details&PUBLIC=Y&XMLSIDE=/servapps/Northgate/PlanningExplorer/SiteFiles/Skins/Hackney/Menus/PL.xml&DAURI=PLANNING');

        preg_match('/Easting\S+([0-9]{6,6})\S+Northing\S+([0-9]{6,6})/i', $appscrape, $coordmatches);
        preg_match('/<span>Wards<\/span>(.*)<\/div>/i', $appscrape, $wardmatches);
        if (isset($coordmatches[1]) && isset($coordmatches[2])) {
            $easting = (integer) $coordmatches[1];
            $northing = (integer) $coordmatches[2];
            $os1 = new OSRef($easting, $northing);
            $latlng = $os1->toLatLng();
            $latlng->OSGB36ToWGS84();
            
        }

        $rows[] = array(       
            "PK" => (integer)$pk,
            "Application Number" => (string)$app->APPLICATION_NUMBER,
            "Site address" => (string)$app->SITE_ADDRESS,
            "Applicant name" => (string)$app->APPLICANT_NAME,
            "Agent name" => (string)$app->AGENT_NAME,
            "Proposal" => (string)$app->PROPOSAL,
            "Date registered" => (string)$app->DATE_REGISTERED,
            "Date target" => (string)$app->DATE_TARGET,
            "Date received" => (string)$app->DATE_RECEIVED,
            "Date valid" => (string)$app->DATE_VALID,
            "Status" => (string)$app->STATUS_DESCRIPTION,
            "Application type" => (string)$app->APPLICATION_TYPE_DESCRIPTION,
            "Latitude" => (string) @$latlng->lat,
            "Longitude" => (string) @$latlng->lng,
            "Wards" => @$wardmatches[1]
        );
    }
    $unique_keys = array("PK");
    $table = "Planning_Applications";
    scraperwiki::save_sqlite($unique_keys, $rows, $table);
 // print_r($rows);
?>