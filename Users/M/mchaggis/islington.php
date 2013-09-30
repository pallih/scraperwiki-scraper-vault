<?php
require  'scraperwiki/simple_html_dom.php';
$day  = 86400;
$week = 604800;
$verbose = false;
$quiet = false;
$NoOfVenues = $NoOfActivities = $NoOfNewActivities = 0;

$startDate = date('d/m/Y');
$endDate = date('d/m/Y', (mktime()+($week*12)));


$postcodeMap = array(
    'EC1 3PU' => 'EC1V 3PU'
,    'EC1V 8JA' => 'EC1V 9JA'
);

$site = 'http://events.islington.gov.uk';
$listpage = "{$site}/Booking/Programme/Session/Search.aspx?BookingFacilityUid=&BookingProgrammeUid=&TaxonomyUid=13e001b8-23a6-41eb-8900-55efb08de8ba&Date=dateRange&Start={$startDate}&End={$endDate}&Redirect=Yes&page_num=";
$ActivityLinks = array();
$pages = 1;
$venues = array();

$startTime = array_sum(explode(' ',microtime()));


/**
 * First we need to loop through and get all the links to the activities
 */
for($x=1; $x <= $pages; $x++) {
    
    $html = explode("\n", scraperwiki::scrape("{$listpage}{$x}"));

    while( ($line = array_shift($html)) ) {
        $line = str_replace(array("\r","\n"),"",$line);
        if (preg_match('!([0-9]+) Items found matching your search criteria.</td><td class="Center">(Page [0-9]+ of ([0-9]+))?!i', $line, $registers)) {
            $total_items_found = $registers[1];
            if ($registers[2] > 1 && $x==1) {
                $pages = $registers[2];
                
            }
        } elseif (preg_match('!<span class="result"><img!i', $line, $registers)) {
            while (!preg_match('!</span></span><br /><br />!i', $line)) {
                $line .= str_replace(array("\r","\n"),"",array_shift($html));
            }
            if (preg_match('!<span class="result"><img [^>]+>(.*)</span></span><br /><br />!i', $line, $registers)) {
                $elements = explode('<span class="resultPercent">',$registers[1]);
            
                /**
                 * 0 - Activitiy link and description
                 * 1 - Venue title and link
                 * 2 - Date
                 * 3 - Time
                 */
        
                if ( preg_match('!^.*a href="(.+BookingSessionUid=([^"]+))".*$!i', $elements[0], $registers) ) {
                    $ActivityLinks[$registers[2]] = $registers[1];
                }
            }
        }
    }
    
    
}
$endTime = array_sum(explode(' ',microtime()));
$duration = number_format(($endTime - $startTime),4);

    print "\rStage 1 Completed: ".date('Y-m-d H:i:s',$endTime)."                                                   
    Duration: {$duration}
    No. of Pages: {$pages}
    No. of Activities Found: ".sizeof($ActivityLinks)."
";
$fieldlist = array();
foreach($ActivityLinks as $ActivityID=>$ActivityLink) {
    if ( !($fp = fopen("{$site}{$ActivityLink}", 'r')) ) {
        if (!$quiet) {
            print "Failed: {$ActivityID} = {$ActivityLink}\n";
        }
        continue;
    } else {
        if ($verbose) {
            print "Processing: {$ActivityID} = {$ActivityLink}\n";
        } elseif (!$quiet) {
            print '.';
        }
    }
    flush();
    
    $thisActivity = array(
        'ActivitySourceID' => $ActivityID
    ,    'ProgrammeID' => ereg_replace('^.*BookingProgrammeUid=([a-z0-9-]+)[^a-z0-9-].*$','\\1',$ActivityLink)
    );
    $line = fgets($fp, 2048);
    while( !feof($fp) ) {
        $line = str_replace(array("\r","\n"),"",$line);
        $line = ereg_replace("^[\t ]+",'',$line);
        
        if (ereg('<label for="ctl00_MainContent_.*Booking([^"]+)[^>]+>(.+)</label>',$line, $registers)) {
            // Read til <br />
            $field = $registers[1];
            if (!array_key_exists($field, $fieldlist)) {
                $fieldlist[$field] = 0;
            } 
            $fieldlist[$field]++;
            
            $line = fgets($fp, 2048);
            $line = ereg_replace("^[\t ]+",'',$line);
            $line = str_replace(array("\r","\n"),"",$line);
            while( (substr($line,0,6) != '<label' && $line != '<br />') ) {
                if (!array_key_exists($field, $thisActivity)) {
                    $thisActivity[$field] = '';
                }
                $thisActivity[$field] .= "{$line}";
                $line = fgets($fp, 2048);
                $line = ereg_replace("^[\t ]+",'',$line);
                $line = str_replace(array("\r","\n"),"",$line);
            }
            if ($field=='FacilityTitle') {
                $thisActivity['FacilityLink'] = $site.preg_replace('!^.* href="([^"]+)".*$!i','\\1',$thisActivity[$field]);
                $thisActivity['ProviderVenueID'] = preg_replace('!^.*=([^=]+)$!','\\1',$thisActivity['FacilityLink']);
            }
            $thisActivity[$field] = strip_tags(str_replace('<br />',"\n",$thisActivity[$field]));
            
        } else {
            $line = fgets($fp, 2048);

        }
    }
    fclose($fp);
    
    list ($f,$t) = explode(' - ', $thisActivity['SessionTime']);
    $thisActivity['SessionStarts'] = date('Y-m-d\TH:i:s',strtotime("{$thisActivity['SessionDate']} {$f}"));
    $thisActivity['SessionEnds'] = date('Y-m-d\TH:i:s',strtotime("{$thisActivity['SessionDate']} {$t}"));
    
    if (strtolower($thisActivity['SessionCost']) != 'free' && $thisActivity['SessionCost'] != 0) {
        $thisActivity['SessionDescription'].= "\n{$thisActivity['SessionCost']}";
    }
    
    $thisActivity['FacilityAddress'] = explode("[,\n]", $thisActivity['FacilityAddress']);
    
    if (array_key_exists($thisActivity['FacilityPostcode'], $postcodeMap)) {
        $thisActivity['FacilityPostcode'] = $postcodeMap[$thisActivity['FacilityPostcode']];
    }

    if (array_key_exists('Cost', $thisActivity)) {
        $thisActivity['Cost'] = 'Unknown';
    }
    /**
     * Next sort out the venue
     */
    $thisActivity['FacilityAddress'] = join("\n", $thisActivity['FacilityAddress']);
    if (!array_key_exists('FacilityNotes', $thisActivity)) { $thisActivity['FacilityNotes']=''; }
    if (!array_key_exists('FacilityAccessInformation', $thisActivity)) { $thisActivity['FacilityAccessInformation']=''; }
    

scraperwiki::save(array_keys($thisActivity), $thisActivity);

    //print_r($thisActivity);
    //    print_r($activity);
    //print_r($thisVenue);
}

?><?php
require  'scraperwiki/simple_html_dom.php';
$day  = 86400;
$week = 604800;
$verbose = false;
$quiet = false;
$NoOfVenues = $NoOfActivities = $NoOfNewActivities = 0;

$startDate = date('d/m/Y');
$endDate = date('d/m/Y', (mktime()+($week*12)));


$postcodeMap = array(
    'EC1 3PU' => 'EC1V 3PU'
,    'EC1V 8JA' => 'EC1V 9JA'
);

$site = 'http://events.islington.gov.uk';
$listpage = "{$site}/Booking/Programme/Session/Search.aspx?BookingFacilityUid=&BookingProgrammeUid=&TaxonomyUid=13e001b8-23a6-41eb-8900-55efb08de8ba&Date=dateRange&Start={$startDate}&End={$endDate}&Redirect=Yes&page_num=";
$ActivityLinks = array();
$pages = 1;
$venues = array();

$startTime = array_sum(explode(' ',microtime()));


/**
 * First we need to loop through and get all the links to the activities
 */
for($x=1; $x <= $pages; $x++) {
    
    $html = explode("\n", scraperwiki::scrape("{$listpage}{$x}"));

    while( ($line = array_shift($html)) ) {
        $line = str_replace(array("\r","\n"),"",$line);
        if (preg_match('!([0-9]+) Items found matching your search criteria.</td><td class="Center">(Page [0-9]+ of ([0-9]+))?!i', $line, $registers)) {
            $total_items_found = $registers[1];
            if ($registers[2] > 1 && $x==1) {
                $pages = $registers[2];
                
            }
        } elseif (preg_match('!<span class="result"><img!i', $line, $registers)) {
            while (!preg_match('!</span></span><br /><br />!i', $line)) {
                $line .= str_replace(array("\r","\n"),"",array_shift($html));
            }
            if (preg_match('!<span class="result"><img [^>]+>(.*)</span></span><br /><br />!i', $line, $registers)) {
                $elements = explode('<span class="resultPercent">',$registers[1]);
            
                /**
                 * 0 - Activitiy link and description
                 * 1 - Venue title and link
                 * 2 - Date
                 * 3 - Time
                 */
        
                if ( preg_match('!^.*a href="(.+BookingSessionUid=([^"]+))".*$!i', $elements[0], $registers) ) {
                    $ActivityLinks[$registers[2]] = $registers[1];
                }
            }
        }
    }
    
    
}
$endTime = array_sum(explode(' ',microtime()));
$duration = number_format(($endTime - $startTime),4);

    print "\rStage 1 Completed: ".date('Y-m-d H:i:s',$endTime)."                                                   
    Duration: {$duration}
    No. of Pages: {$pages}
    No. of Activities Found: ".sizeof($ActivityLinks)."
";
$fieldlist = array();
foreach($ActivityLinks as $ActivityID=>$ActivityLink) {
    if ( !($fp = fopen("{$site}{$ActivityLink}", 'r')) ) {
        if (!$quiet) {
            print "Failed: {$ActivityID} = {$ActivityLink}\n";
        }
        continue;
    } else {
        if ($verbose) {
            print "Processing: {$ActivityID} = {$ActivityLink}\n";
        } elseif (!$quiet) {
            print '.';
        }
    }
    flush();
    
    $thisActivity = array(
        'ActivitySourceID' => $ActivityID
    ,    'ProgrammeID' => ereg_replace('^.*BookingProgrammeUid=([a-z0-9-]+)[^a-z0-9-].*$','\\1',$ActivityLink)
    );
    $line = fgets($fp, 2048);
    while( !feof($fp) ) {
        $line = str_replace(array("\r","\n"),"",$line);
        $line = ereg_replace("^[\t ]+",'',$line);
        
        if (ereg('<label for="ctl00_MainContent_.*Booking([^"]+)[^>]+>(.+)</label>',$line, $registers)) {
            // Read til <br />
            $field = $registers[1];
            if (!array_key_exists($field, $fieldlist)) {
                $fieldlist[$field] = 0;
            } 
            $fieldlist[$field]++;
            
            $line = fgets($fp, 2048);
            $line = ereg_replace("^[\t ]+",'',$line);
            $line = str_replace(array("\r","\n"),"",$line);
            while( (substr($line,0,6) != '<label' && $line != '<br />') ) {
                if (!array_key_exists($field, $thisActivity)) {
                    $thisActivity[$field] = '';
                }
                $thisActivity[$field] .= "{$line}";
                $line = fgets($fp, 2048);
                $line = ereg_replace("^[\t ]+",'',$line);
                $line = str_replace(array("\r","\n"),"",$line);
            }
            if ($field=='FacilityTitle') {
                $thisActivity['FacilityLink'] = $site.preg_replace('!^.* href="([^"]+)".*$!i','\\1',$thisActivity[$field]);
                $thisActivity['ProviderVenueID'] = preg_replace('!^.*=([^=]+)$!','\\1',$thisActivity['FacilityLink']);
            }
            $thisActivity[$field] = strip_tags(str_replace('<br />',"\n",$thisActivity[$field]));
            
        } else {
            $line = fgets($fp, 2048);

        }
    }
    fclose($fp);
    
    list ($f,$t) = explode(' - ', $thisActivity['SessionTime']);
    $thisActivity['SessionStarts'] = date('Y-m-d\TH:i:s',strtotime("{$thisActivity['SessionDate']} {$f}"));
    $thisActivity['SessionEnds'] = date('Y-m-d\TH:i:s',strtotime("{$thisActivity['SessionDate']} {$t}"));
    
    if (strtolower($thisActivity['SessionCost']) != 'free' && $thisActivity['SessionCost'] != 0) {
        $thisActivity['SessionDescription'].= "\n{$thisActivity['SessionCost']}";
    }
    
    $thisActivity['FacilityAddress'] = explode("[,\n]", $thisActivity['FacilityAddress']);
    
    if (array_key_exists($thisActivity['FacilityPostcode'], $postcodeMap)) {
        $thisActivity['FacilityPostcode'] = $postcodeMap[$thisActivity['FacilityPostcode']];
    }

    if (array_key_exists('Cost', $thisActivity)) {
        $thisActivity['Cost'] = 'Unknown';
    }
    /**
     * Next sort out the venue
     */
    $thisActivity['FacilityAddress'] = join("\n", $thisActivity['FacilityAddress']);
    if (!array_key_exists('FacilityNotes', $thisActivity)) { $thisActivity['FacilityNotes']=''; }
    if (!array_key_exists('FacilityAccessInformation', $thisActivity)) { $thisActivity['FacilityAccessInformation']=''; }
    

scraperwiki::save(array_keys($thisActivity), $thisActivity);

    //print_r($thisActivity);
    //    print_r($activity);
    //print_r($thisVenue);
}

?>