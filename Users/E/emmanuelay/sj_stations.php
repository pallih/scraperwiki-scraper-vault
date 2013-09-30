<?php
######################################
# SJ Stationsscraper
# PHP Scraper av Emmanuel Ay 2011
######################################
# Syftet är att scrape:a upp samtliga 
# stationer med Banverkets unika ID 
# för att kunna bearbeta på fler sätt
######################################

require  'scraperwiki/simple_html_dom.php';

# get startpage
$html = scraperwiki::scrape("http://www4.banverket.se/trafikinformation/WebPage/StartPage.aspx?JF=7");
$dom = new simple_html_dom();
$dom->load($html);

# get redirect URL that contains ASP.NET state string
$newurl = $dom->find("a");
$newhref = get_href($newurl[0]);

# URL found, fetch it
if ($newhref != "") {
    $html = scraperwiki::scrape($newhref);
    $dom->load($html);

    # parse it
    $grid = $dom->find('#TrafficInfoStart_StationList',0); 
    $stations = $grid->find("option");

    # rip it apart
    $rowCount = 0;
    foreach($stations as $station) {
        if ($rowCount > 0) {
            # save it
            $dataset = array( 
                            'Station' => fix_chars($station->plaintext), 
                            'StationID' => fix_chars($station->value)
                        ) ;
            scraperwiki::save( array('Station', 'StationID'), $dataset );
        }
        $rowCount++;
    }
}


# Support functions

function fix_chars( $str ) {
    $str = str_replace("Ã¥", "å", $str);
    $str = str_replace("Ã¤", "ä", $str);
    $str = str_replace("Ã", "Ö", $str);
    $str = str_replace("Ö¶", "ö", $str);
    $str = str_replace("&#246;", "ö", $str);
    $str = str_replace("&#228;", "ä", $str);
    $str = str_replace("&#229;", "å", $str);
    $str = str_replace("&#196;", "Ä", $str);
    $str = str_replace("&#214;", "Ö", $str);
    $str = str_replace("&#197;", "Å", $str);

    return $str;
}

function get_href($inputString) {
    if (preg_match('/href="([^"]*)"/i', $inputString , $regs))
    {
        $result = $regs[1];
    } else {
        $result = "";
    }
    return $result ;
}
?><?php
######################################
# SJ Stationsscraper
# PHP Scraper av Emmanuel Ay 2011
######################################
# Syftet är att scrape:a upp samtliga 
# stationer med Banverkets unika ID 
# för att kunna bearbeta på fler sätt
######################################

require  'scraperwiki/simple_html_dom.php';

# get startpage
$html = scraperwiki::scrape("http://www4.banverket.se/trafikinformation/WebPage/StartPage.aspx?JF=7");
$dom = new simple_html_dom();
$dom->load($html);

# get redirect URL that contains ASP.NET state string
$newurl = $dom->find("a");
$newhref = get_href($newurl[0]);

# URL found, fetch it
if ($newhref != "") {
    $html = scraperwiki::scrape($newhref);
    $dom->load($html);

    # parse it
    $grid = $dom->find('#TrafficInfoStart_StationList',0); 
    $stations = $grid->find("option");

    # rip it apart
    $rowCount = 0;
    foreach($stations as $station) {
        if ($rowCount > 0) {
            # save it
            $dataset = array( 
                            'Station' => fix_chars($station->plaintext), 
                            'StationID' => fix_chars($station->value)
                        ) ;
            scraperwiki::save( array('Station', 'StationID'), $dataset );
        }
        $rowCount++;
    }
}


# Support functions

function fix_chars( $str ) {
    $str = str_replace("Ã¥", "å", $str);
    $str = str_replace("Ã¤", "ä", $str);
    $str = str_replace("Ã", "Ö", $str);
    $str = str_replace("Ö¶", "ö", $str);
    $str = str_replace("&#246;", "ö", $str);
    $str = str_replace("&#228;", "ä", $str);
    $str = str_replace("&#229;", "å", $str);
    $str = str_replace("&#196;", "Ä", $str);
    $str = str_replace("&#214;", "Ö", $str);
    $str = str_replace("&#197;", "Å", $str);

    return $str;
}

function get_href($inputString) {
    if (preg_match('/href="([^"]*)"/i', $inputString , $regs))
    {
        $result = $regs[1];
    } else {
        $result = "";
    }
    return $result ;
}
?>