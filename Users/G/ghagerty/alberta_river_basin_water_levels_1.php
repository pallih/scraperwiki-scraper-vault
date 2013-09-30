<?php
// Where to find the Alberta Environment text files with river level data
$baseurl = "http://environment.alberta.ca/forecasting/data/hydro/tables/";

// Name of the text file for a particular station
$feeds = array('NSA-RNSASEDM-WL.txt','NSA-RNSAS759-WL.txt','NSA-RNSASRMH-WL.txt','NSA-RNSASWHI-WL.txt');

foreach ($feeds as $stationFile) {
    $sourceurl = $baseurl . $stationFile;
    
    $txt = scraperWiki::scrape($sourceurl);
    
    /**
    * We want to extract the following data points from the text file headers:
    * Last updated date and time, station ID, and station description from the
    * header of the file. The header format is as follows:
    *
    *             Alberta Environment                          Page: 1
    *         REAL TIME HYDROMETRIC REPORT    Last Updated: 2011-06-22
    *                                                 Time:   15:11:52
    * RNSASEDM : North Saskatchewan River at Hwy #759orth Saskatchewan River at Edmonton
    */
     
    $pattern = '/Last Updated:\s*([\d-]*)\s*\n\s*Time:\s*([\d:]*)\s*\n\s*([\S]*)\s*:\s*([^\n]*)\s*\n/i';
    preg_match($pattern, $txt, $matches);
    
    $matches = array_map('trim', $matches);
    $stationID = $matches[3];
    
    // Store all meta data in a database
    $stationMeta = array(
        'stationID' => $matches[3],
        'lastDate' => $matches[1],
        'lastTime' => $matches[2],
        'location' => $matches[4],
        'website' => 'http://environment.alberta.ca/apps/basins/Default.aspx',
        'feed' => $sourceurl);
    
    // Save the metadata using stationID as the primary key
    scraperwiki::save_sqlite(array('stationID'), $stationMeta, $table_name='abwl_meta');
    
    /**
    * The data points in the text file returned from Alberta Environment
    * can then be pulled out using a regular expression.
    * The lines with data look like this:
    * RNSASEDM      2011-06-20 03:15:00          7.830      1871.20
    *
    *
    * So that's what we regex for
    */
    $pattern = "/\s*{$stationID}\s+([\d-]*)\s+([\d:]*)\s+([\S]*)\s+([\S]*)\s*\n/i";

    preg_match_all($pattern, $txt, $matches, PREG_SET_ORDER);
    
    // Specify the name of the data columns in the database
    $abwl_columns = array('Date', 'Time', 'Level', 'Flow');
    
    // Extract the relevant data from our matches
    $abwl_data = array();
    foreach ($matches as $key => $value) {
      $abwl_data[$key] = array_combine($abwl_columns, array_slice($value, 1));
    }

    // Save the data using the timestamp  (Date + Time) as the primary key
    scraperwiki::save_sqlite(array_slice($abwl_columns, 0, 2), $abwl_data, $table_name=$stationID);
}
?>
<?php
// Where to find the Alberta Environment text files with river level data
$baseurl = "http://environment.alberta.ca/forecasting/data/hydro/tables/";

// Name of the text file for a particular station
$feeds = array('NSA-RNSASEDM-WL.txt','NSA-RNSAS759-WL.txt','NSA-RNSASRMH-WL.txt','NSA-RNSASWHI-WL.txt');

foreach ($feeds as $stationFile) {
    $sourceurl = $baseurl . $stationFile;
    
    $txt = scraperWiki::scrape($sourceurl);
    
    /**
    * We want to extract the following data points from the text file headers:
    * Last updated date and time, station ID, and station description from the
    * header of the file. The header format is as follows:
    *
    *             Alberta Environment                          Page: 1
    *         REAL TIME HYDROMETRIC REPORT    Last Updated: 2011-06-22
    *                                                 Time:   15:11:52
    * RNSASEDM : North Saskatchewan River at Hwy #759orth Saskatchewan River at Edmonton
    */
     
    $pattern = '/Last Updated:\s*([\d-]*)\s*\n\s*Time:\s*([\d:]*)\s*\n\s*([\S]*)\s*:\s*([^\n]*)\s*\n/i';
    preg_match($pattern, $txt, $matches);
    
    $matches = array_map('trim', $matches);
    $stationID = $matches[3];
    
    // Store all meta data in a database
    $stationMeta = array(
        'stationID' => $matches[3],
        'lastDate' => $matches[1],
        'lastTime' => $matches[2],
        'location' => $matches[4],
        'website' => 'http://environment.alberta.ca/apps/basins/Default.aspx',
        'feed' => $sourceurl);
    
    // Save the metadata using stationID as the primary key
    scraperwiki::save_sqlite(array('stationID'), $stationMeta, $table_name='abwl_meta');
    
    /**
    * The data points in the text file returned from Alberta Environment
    * can then be pulled out using a regular expression.
    * The lines with data look like this:
    * RNSASEDM      2011-06-20 03:15:00          7.830      1871.20
    *
    *
    * So that's what we regex for
    */
    $pattern = "/\s*{$stationID}\s+([\d-]*)\s+([\d:]*)\s+([\S]*)\s+([\S]*)\s*\n/i";

    preg_match_all($pattern, $txt, $matches, PREG_SET_ORDER);
    
    // Specify the name of the data columns in the database
    $abwl_columns = array('Date', 'Time', 'Level', 'Flow');
    
    // Extract the relevant data from our matches
    $abwl_data = array();
    foreach ($matches as $key => $value) {
      $abwl_data[$key] = array_combine($abwl_columns, array_slice($value, 1));
    }

    // Save the data using the timestamp  (Date + Time) as the primary key
    scraperwiki::save_sqlite(array_slice($abwl_columns, 0, 2), $abwl_data, $table_name=$stationID);
}
?>
