<?php

# Hydropower planning applications

$DEBUG_TABLES=FALSE;
$DEBUG=TRUE;

# Read and filter hydro applications and authorities for a region
function fetchRegionHydroData($dbname, $aliasname) {
    scraperwiki::attach($dbname, $aliasname);
    debug_tables($aliasname);
    updateHydroApplications($aliasname, '');
}


function recreateTables() {
    createHydroAuthorities(TRUE);
    createHydroApplications(TRUE);
}


function createHydroApplications($drop = FALSE) {    
    if ($drop) {
        scraperwiki::sqliteexecute("drop table hydro_applications");
        scraperwiki::sqlitecommit(); 
    }
    scraperwiki::sqliteexecute("create table hydro_applications(authority string, ".
                                                               "reference string, ".
                                                               "scrape_date string, ".
                                                               "received_date string, ".
                                                               "validated_date string, ".
                                                               "address string, ".
                                                               "postcode string, ".
                                                               "lat real, ".
                                                               "lng real, ".
                                                               "description string, ".
                                                               "info_url string ".
                                                               ")");
    scraperwiki::sqlitecommit(); 
}


function createHydroAuthorities($drop = FALSE) {   
    if ($drop) {
        scraperwiki::sqliteexecute("drop table hydro_authorities");
        scraperwiki::sqlitecommit(); 
    }
    scraperwiki::sqliteexecute("CREATE TABLE `hydro_authorities` (`name` text,
                                                                  `long_name` text, 
                                                                  `region` text, 
                                                                  `last_match_count` integer, 
                                                                  `scrape_date_type` text, 
                                                                  `last_msg` text, 
                                                                  `last_count` integer, 
                                                                  `last_date` text, 
                                                                  `last_scrape` text, 
                                                                  `last_status` text, 
                                                                  `start_url` text, 
                                                                  `config` text, 
                                                                  `start_date` text, 
                                                                  `total` integer, 
                                                                  `info` text, 
                                                                  `status` text, 
                                                                  `base_url` text)");
    scraperwiki::sqlitecommit(); 
}


function updateHydroApplications($schema, $authority) {
    $tablename = $schema.".applications";
    $applications = scraperwiki::select( "* FROM ".$tablename
                                        # ." WHERE authority='"+$authority+"'"
                                        ." WHERE (description LIKE '%hydro%' OR description LIKE '%turbine%')"
    );
    print "Searching ".count($applications)." rows in ".$tablename."...";

    # Exclude rows with these words in the description
    $excludes = "(hydrogen)|(hydrotherapy)|(hydrological)|(hydrogeological)|"
               ."(hydrocarbon)|(hydrology)|(hydrolysis)|(biomass)|"
               ."(gas.*turbine)|(mast.*turbine)|(turbine.*mast)|(wind.*turbine)|(turbine.*tower)";

    # Include rows with these words, even if excluded by $excludes
    $includes = "(archimedes)|(francis)|(kaplan)|(hydropower)|(hydroelectric)|(hydro-electric)";

    $authorities = array();
    $matches = array();
    foreach ($applications as $row) {
        if (preg_match("/$excludes/i", $row['description']) == 0 || 
            preg_match("/$includes/i", $row['description']) != 0) {
            #print "Match:".$row['authority']." ".$row['reference']." ".$row['description']."\n";
            array_push($matches, $row);
            #debug_array($row);
            if (!array_key_exists($row['authority'], $authorities)) {
                $authorities[$row['authority']] = NULL;
            }
        }
    }
    print " found ".count($matches)." hydropower matches across ".count($authorities)." authorities in $schema.\n";

    # Update saved authorities 
    updateHydroAuthorities($schema, $authorities);

    # Save applications
    saveHydroApplications($matches);
}


function saveHydroApplications($applications) {
    $n = 0;
    $pk = array( "authority", "reference" );
    $verbose = 2;
    foreach ($applications as $row) {
        $existingApp = findHydroApplication($row);
        if (!$existingApp) {
            print "Saving new/updated hydroApplication: ".$row['authority']." : ".$row['reference']."\n";
            scraperwiki::save_sqlite($pk, $row, "hydro_applications", $verbose);
            scraperwiki::sqlitecommit(); 
            $n++;
        }
    }
    if ($n > 0)
        print "Saved $n new/updated hydro applications.\n";
}


# Read an existing hydro application record, scraped on same or newer date
# (because some authorities eg. Peak District are in more than one region)
function findHydroApplication($appKey) {
    $bind = array( 0 => $appKey['authority'], 1 => $appKey['reference'], 2 => $appKey['scrape_date'] );
    $application = scraperwiki::select("* FROM hydro_applications WHERE authority = ? AND reference = ? AND scrape_date >= ?", $bind);
    return $application;
}


# Fetch missing authorities
function updateHydroAuthorities($schema, $authorities) {
    $n = 0;
    $knownAuthorities = readHydroAuthorities();
    foreach ($authorities as $aid => $row) {
        if ($row == NULL && !array_key_exists($aid, $knownAuthorities)) {
            $row = fetchAuthority($schema, $aid);
            saveHydroAuthority($row);
            $n++;
        }
    }
    if ($n > 0)
        print "Saved $n new hydro authorities.\n";
}


function saveHydroAuthority($authority) {
    # Save applications
    $pk = array( "name" );
    $verbose = 2;
    scraperwiki::save_sqlite($pk, $authority, "hydro_authorities", $verbose);
    scraperwiki::sqlitecommit();
}


# Read known hydro authorities
function readHydroAuthorities() {
    $authorities = array();
    $data = scraperwiki::select("* FROM hydro_authorities ORDER BY name");
    foreach ($data as $row) {
        $authorities[$row['name']] = $row;
    }
    return $authorities;
}
 

function fetchAuthority($schema, $aid) {
    $authority = scraperwiki::select("* FROM $schema.authorities WHERE name='$aid'");
    debug_array($authority[0], "Fetched $schema authority $aid:");
    return $authority[0];
}


# show table types
function debug_tables($schema) {
    global $DEBUG_TABLES;
    if (!$DEBUG_TABLES)
        return;
    $tables = scraperwiki::show_tables($schema);
    print "Schema '".$schema."' contains ".count($tables)." tables\n";
    foreach (array_keys($tables) as $tableName) {
        debug_table($schema, $tableName, TRUE);
    }
}


function debug_table($schema, $tname, $showSchema=FALSE) {
    global $DEBUG_TABLES;
    if (!$DEBUG_TABLES)
        return;
    $tablename = $schema.".".$tname;
    $num = scraperwiki::select("count(*) AS n FROM ".$tablename);
    print "$tablename size: ".$num[0]['n']." rows.\n";

    if ($showSchema) {
        print "$tablename schema: ";
        $info = scraperwiki::table_info($tablename);
        #debug_array($info, "Table_info($tablename)");
        foreach ($info as $column) {
            print $column['name']."(".$column['type']."); ";
        }
        print "\n";
    }
 }


function debug_array($a, $title="Array") {
    global $DEBUG;
    if (!$DEBUG) 
        return;
    print "$title = ";
    print_r($a);
    print "\n";
}


# Uncomment this to drop all data and start again
# recreateTables();

$regions = array(
    "scotpa" => 'scotland_planning_applications',
    "walespa" => 'wales_planning_applications',
    "nepa" => 'north_east_planning_applications',
    "nwpa" => 'north_west_planning_applications',
    "wmidpa" => 'west_midlands_planning_applications',
    "emidpa" => 'east_midlands_planning_applications',
    "eepa" => 'east_england_planning_applications',
    "swpa" => 'south_west_planning_applications',
    "sepa" => 'south_east_planning_applications', 
    "lonpa" => 'london_planning_applications'
);

foreach ($regions as $dbalias => $dbname) {
    fetchRegionHydroData($dbname, $dbalias);
}


?>
<?php

# Hydropower planning applications

$DEBUG_TABLES=FALSE;
$DEBUG=TRUE;

# Read and filter hydro applications and authorities for a region
function fetchRegionHydroData($dbname, $aliasname) {
    scraperwiki::attach($dbname, $aliasname);
    debug_tables($aliasname);
    updateHydroApplications($aliasname, '');
}


function recreateTables() {
    createHydroAuthorities(TRUE);
    createHydroApplications(TRUE);
}


function createHydroApplications($drop = FALSE) {    
    if ($drop) {
        scraperwiki::sqliteexecute("drop table hydro_applications");
        scraperwiki::sqlitecommit(); 
    }
    scraperwiki::sqliteexecute("create table hydro_applications(authority string, ".
                                                               "reference string, ".
                                                               "scrape_date string, ".
                                                               "received_date string, ".
                                                               "validated_date string, ".
                                                               "address string, ".
                                                               "postcode string, ".
                                                               "lat real, ".
                                                               "lng real, ".
                                                               "description string, ".
                                                               "info_url string ".
                                                               ")");
    scraperwiki::sqlitecommit(); 
}


function createHydroAuthorities($drop = FALSE) {   
    if ($drop) {
        scraperwiki::sqliteexecute("drop table hydro_authorities");
        scraperwiki::sqlitecommit(); 
    }
    scraperwiki::sqliteexecute("CREATE TABLE `hydro_authorities` (`name` text,
                                                                  `long_name` text, 
                                                                  `region` text, 
                                                                  `last_match_count` integer, 
                                                                  `scrape_date_type` text, 
                                                                  `last_msg` text, 
                                                                  `last_count` integer, 
                                                                  `last_date` text, 
                                                                  `last_scrape` text, 
                                                                  `last_status` text, 
                                                                  `start_url` text, 
                                                                  `config` text, 
                                                                  `start_date` text, 
                                                                  `total` integer, 
                                                                  `info` text, 
                                                                  `status` text, 
                                                                  `base_url` text)");
    scraperwiki::sqlitecommit(); 
}


function updateHydroApplications($schema, $authority) {
    $tablename = $schema.".applications";
    $applications = scraperwiki::select( "* FROM ".$tablename
                                        # ." WHERE authority='"+$authority+"'"
                                        ." WHERE (description LIKE '%hydro%' OR description LIKE '%turbine%')"
    );
    print "Searching ".count($applications)." rows in ".$tablename."...";

    # Exclude rows with these words in the description
    $excludes = "(hydrogen)|(hydrotherapy)|(hydrological)|(hydrogeological)|"
               ."(hydrocarbon)|(hydrology)|(hydrolysis)|(biomass)|"
               ."(gas.*turbine)|(mast.*turbine)|(turbine.*mast)|(wind.*turbine)|(turbine.*tower)";

    # Include rows with these words, even if excluded by $excludes
    $includes = "(archimedes)|(francis)|(kaplan)|(hydropower)|(hydroelectric)|(hydro-electric)";

    $authorities = array();
    $matches = array();
    foreach ($applications as $row) {
        if (preg_match("/$excludes/i", $row['description']) == 0 || 
            preg_match("/$includes/i", $row['description']) != 0) {
            #print "Match:".$row['authority']." ".$row['reference']." ".$row['description']."\n";
            array_push($matches, $row);
            #debug_array($row);
            if (!array_key_exists($row['authority'], $authorities)) {
                $authorities[$row['authority']] = NULL;
            }
        }
    }
    print " found ".count($matches)." hydropower matches across ".count($authorities)." authorities in $schema.\n";

    # Update saved authorities 
    updateHydroAuthorities($schema, $authorities);

    # Save applications
    saveHydroApplications($matches);
}


function saveHydroApplications($applications) {
    $n = 0;
    $pk = array( "authority", "reference" );
    $verbose = 2;
    foreach ($applications as $row) {
        $existingApp = findHydroApplication($row);
        if (!$existingApp) {
            print "Saving new/updated hydroApplication: ".$row['authority']." : ".$row['reference']."\n";
            scraperwiki::save_sqlite($pk, $row, "hydro_applications", $verbose);
            scraperwiki::sqlitecommit(); 
            $n++;
        }
    }
    if ($n > 0)
        print "Saved $n new/updated hydro applications.\n";
}


# Read an existing hydro application record, scraped on same or newer date
# (because some authorities eg. Peak District are in more than one region)
function findHydroApplication($appKey) {
    $bind = array( 0 => $appKey['authority'], 1 => $appKey['reference'], 2 => $appKey['scrape_date'] );
    $application = scraperwiki::select("* FROM hydro_applications WHERE authority = ? AND reference = ? AND scrape_date >= ?", $bind);
    return $application;
}


# Fetch missing authorities
function updateHydroAuthorities($schema, $authorities) {
    $n = 0;
    $knownAuthorities = readHydroAuthorities();
    foreach ($authorities as $aid => $row) {
        if ($row == NULL && !array_key_exists($aid, $knownAuthorities)) {
            $row = fetchAuthority($schema, $aid);
            saveHydroAuthority($row);
            $n++;
        }
    }
    if ($n > 0)
        print "Saved $n new hydro authorities.\n";
}


function saveHydroAuthority($authority) {
    # Save applications
    $pk = array( "name" );
    $verbose = 2;
    scraperwiki::save_sqlite($pk, $authority, "hydro_authorities", $verbose);
    scraperwiki::sqlitecommit();
}


# Read known hydro authorities
function readHydroAuthorities() {
    $authorities = array();
    $data = scraperwiki::select("* FROM hydro_authorities ORDER BY name");
    foreach ($data as $row) {
        $authorities[$row['name']] = $row;
    }
    return $authorities;
}
 

function fetchAuthority($schema, $aid) {
    $authority = scraperwiki::select("* FROM $schema.authorities WHERE name='$aid'");
    debug_array($authority[0], "Fetched $schema authority $aid:");
    return $authority[0];
}


# show table types
function debug_tables($schema) {
    global $DEBUG_TABLES;
    if (!$DEBUG_TABLES)
        return;
    $tables = scraperwiki::show_tables($schema);
    print "Schema '".$schema."' contains ".count($tables)." tables\n";
    foreach (array_keys($tables) as $tableName) {
        debug_table($schema, $tableName, TRUE);
    }
}


function debug_table($schema, $tname, $showSchema=FALSE) {
    global $DEBUG_TABLES;
    if (!$DEBUG_TABLES)
        return;
    $tablename = $schema.".".$tname;
    $num = scraperwiki::select("count(*) AS n FROM ".$tablename);
    print "$tablename size: ".$num[0]['n']." rows.\n";

    if ($showSchema) {
        print "$tablename schema: ";
        $info = scraperwiki::table_info($tablename);
        #debug_array($info, "Table_info($tablename)");
        foreach ($info as $column) {
            print $column['name']."(".$column['type']."); ";
        }
        print "\n";
    }
 }


function debug_array($a, $title="Array") {
    global $DEBUG;
    if (!$DEBUG) 
        return;
    print "$title = ";
    print_r($a);
    print "\n";
}


# Uncomment this to drop all data and start again
# recreateTables();

$regions = array(
    "scotpa" => 'scotland_planning_applications',
    "walespa" => 'wales_planning_applications',
    "nepa" => 'north_east_planning_applications',
    "nwpa" => 'north_west_planning_applications',
    "wmidpa" => 'west_midlands_planning_applications',
    "emidpa" => 'east_midlands_planning_applications',
    "eepa" => 'east_england_planning_applications',
    "swpa" => 'south_west_planning_applications',
    "sepa" => 'south_east_planning_applications', 
    "lonpa" => 'london_planning_applications'
);

foreach ($regions as $dbalias => $dbname) {
    fetchRegionHydroData($dbname, $dbalias);
}


?>
