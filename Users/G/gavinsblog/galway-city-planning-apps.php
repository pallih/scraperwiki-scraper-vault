<?php

/*
 * Planning applications for Galway City Council
 *
 * Based on John Handelaar's scraper for Cork City Council
 *
 * The LGCSB's ePlan app is an aspx nightmare which forcibly paginates results
 * and refuses GETs on its search form.
 * Once we grab all received applications for the last N days, we loop through
 * only those applications in the state of 'New Application' (and ignore 'Incomplete')
 * because the City adds Irish grid references to the 'Site location' detail page.
 *
 * TODO: Add data to datastore after checking we haven't added the same planning ref number
 * previously.
 */

require  'scraperwiki/simple_html_dom.php';

/*
 * Setting any global vars here in order to
 * make reuse easier
 */
$recent_days = 14;
$authority_code = "GC";
$authority_name = "Galway City Council";
$authority_short_name = "Galway City";
$site_url = "http://gis.galwaycity.ie/ePlan/InternetEnquiry/";
$nearby_api_key = "64c962e53d1c01"; # Seriously. Don't use this if you're not me. Sign up at nearby.org.uk


# Initialise POST form data
$postvars = array (
    'txtFileNum' => '',
    'txtSurname' => '',
    'ReportType' => 'RECEIVED',
    'txtLocation' => '',
    'NoDays' => $recent_days,
    'limitResults' => '0',
    'Submit5' => 'Search',
    'btnLookupFileNum' => 'Processing...'
);

$thispage = 1;
echo "Fetching search ​​result page for last $recent_days days\n";
$result = scraperpost($site_url . "frmSelCritSearch.asp", $postvars);
$html = $result['body'];
$cookie = $result['cookie'];

$applications = parse_search_result_page($html);

foreach ($applications as $key => $application) {
    $url = $site_url . "rpt_ViewApplicDetails.asp?validFileNum=1&app_num_file=$application[rawappref]";
    echo "Fetching detail page for application $application[appref]\n";
    $detail_html = scraperwiki::scrape($url);
    $details = parse_detail_page($detail_html);
    echo "Fetching location page for application $application[appref]\n";
    $location_html = scraperwiki::scrape($site_url . "rpt_ViewSiteLocDetails.asp?page_num=0&file_number=$application[rawappref]");
    $location = parse_location_page($location_html);
    $latlong = gridref_to_latlong($location['easting'], $location['northing']);
    $application['lat'] = $latlong[0];
    $application['long'] = $latlong[1];
    $application['details'] = $details;
    $application['url'] = $url;
    scraperwiki::save(array('appref'), $application, $application["date"], array($application['lat'], $application['long']));
}

/*
 * A function to use instead of scraperwiki::scrape since that function only performs simple GETs
 *
 * Arguments:
 * $url - a URL to which we will post form variables
 * $postvars - an array of keys and values containing all the form variables we're POSTing
 * $cookie - a cookie to send along with the request
 *
 * Response array keys:
 * 'headers' - string containing all HTTP response headers
 * 'body' - response body
 * 'cookie' - response cookie if any, or NULL
 */
function scraperpost($url, $postvars=NULL, $cookie=NULL) {
    $curl = curl_init($url);
    $fields_string = "";
    if($postvars) {
        foreach($postvars as $key=>$value) {
            $fields_string .= $key.'='.$value.'&';
        }
    }
    rtrim($fields_string,'&');
    curl_setopt($curl,CURLOPT_POST,true);
    curl_setopt($curl,CURLOPT_RETURNTRANSFER,true);
    curl_setopt($curl,CURLOPT_POSTFIELDS,$fields_string);
    curl_setopt($curl,CURLOPT_COOKIESESSION,true);
    curl_setopt($curl,CURLOPT_HEADER, 1);
    if ($cookie) {
        curl_setopt($curl,CURLOPT_COOKIE, $cookie);
    }
    $res  = curl_exec($curl);
    curl_close($curl);
    if (!preg_match("/^(([^\n\r]+\r?\n)+)\r?\n/", $res, $match)) {
        trigger_error("Invalid HTTP response:\n" . $res, E_USER_ERROR);
    };
    $headers = $match[1];
    $body = substr($res, strlen($headers));
    if (preg_match('/^Set-Cookie: (.*?);/m', $headers, $match)) {
        $cookie = $match[1];
    }
    return array('headers' => $headers, 'body' => $body, 'cookie' => $cookie);
}

function parse_search_result_page($html) {
    $dom = new simple_html_dom();
    $dom->load($html);
    $apps = array();
    global $authority_code;
    global $nearby_api_key;
    foreach($dom->find("table[class='AppDetailsTable'] tr") as $row) {
        #  Man, this is hacky, but I'm not using dom here in case 'td' shows in plaintext of var
        if (!stristr($row,'FINALISED') && !stristr($row,'CONDITIONAL') && !stristr($row,'APPEALED') & !stristr($row,'WITHDRAWN') && !stristr($row,'NEW<') && !stristr($row,'APPROVED') && !stristr($row,'REFUSED')) continue;

        $appref = $authority_code . substr($row->children[0]->plaintext,0,2) . "/" . substr($row->children[0]->plaintext,2);
        $rawappref = trim($row->children[0]->plaintext);
        $rawdate   = substr($row->children[4]->plaintext,0,10);
        $date = substr($rawdate,-4) . "-" . substr($rawdate,3,2) . "-" . substr($rawdate,0,2);
        $applicant = trim($row->children[5]->plaintext);
        $address = str_replace("<br>",",",str_replace("<BR>",",",$row->children[6]->innertext));
        $apps["$appref"] = array(
            'appref'    => $appref,
            'rawappref' => $rawappref,
            'date'      => $date,
            'applicant' => $applicant,
            'address'   => $address,
        );
    }
    return $apps;
}

function parse_detail_page($html) {
    $dom = new simple_html_dom();
    $dom->load($html);
    $details = $dom->find("table[class='AppDetailsTable'] tr",15)->children(1)->plaintext;
    return $details;
}

function parse_location_page($html) {
    if (stristr($html,"No Site Location Details Found")) {
        return false;
    }
    $dom = new simple_html_dom();
    $dom->load($html);
    $northing = round(floatval($dom->find("table[class='AppDetailsTable'] tr",1)->children(1)->plaintext));
    $easting  = round(floatval($dom->find("table[class='AppDetailsTable'] tr",1)->children(4)->plaintext));
    return array('easting' => $easting, 'northing' => $northing);
}

function gridref_to_latlong($easting, $northing) {
    return Grid_Ref_Utils::toolbox()->grid_to_lat_long($easting, $northing, Grid_Ref_Utils::toolbox()->COORDS_OSI);
}





// ===================================================

/*****************************************************
               Grid Reference Utilities
Version 2.1 - Written by Mark Wilton-Jones 1-10/4/2010
Updated 6/5/2010 to allow methods to return text
strings and add support for ITM, UTM and UPS
Updated 9/5/2010 to add dd_format
******************************************************

Please see http://www.howtocreate.co.uk/php/ for details
Please see http://www.howtocreate.co.uk/php/gridref.php for demos and instructions
Please see http://www.howtocreate.co.uk/php/gridrefapi.php for API documentation
Please see http://www.howtocreate.co.uk/jslibs/termsOfUse.html for terms and conditions of use

Provides functions to convert between different NGR formats and latitude/longitude formats.

_______________________________________________________________________________________________*/

//use a class to keep all of the method/property clutter out of the global scope
class Grid_Ref_Utils {

    //class instantiation forcing use as a singleton - state can also be stored if needed (or can use separate instances)
    //could be done as an abstract class with static methods, but would still need instantiation to prepare UK_grid_numbers
    //(as methods/properties do not exist during initial class constructor parsing), and would restrict future flexibility
    private static $only_instance;
    public static function toolbox() {
        if( !isset( self::$only_instance ) ) {
            self::$only_instance = new Grid_Ref_Utils();
        }
        return self::$only_instance;
    }
    private function __construct() {
        $this->UK_grid_numbers = $this->grid_to_hashmap($this->UK_grid_squares);
        $this->TEXT_EUROPEAN = html_entity_decode( '&deg;', ENT_QUOTES, 'ISO-8859-1' );
        $this->TEXT_UNICODE = html_entity_decode( '&deg;', ENT_QUOTES, 'UTF-8' );
        $this->TEXT_ASIAN = html_entity_decode( '&deg;', ENT_QUOTES, 'Shift_JIS' );
    }

    //character grids used by map systems
    private function grid_to_hashmap($grid_2d_array) {
        //make a hashmap of arrays giving the x,y values for grid letters
        $hashmap = Array();
        foreach( $grid_2d_array as $grid_row_index => $grid_row_array ) {
            foreach( $grid_row_array as $grid_col_index => $grid_letter ) {
                $hashmap[$grid_letter] = Array($grid_col_index,$grid_row_index);
            }
        }
        return $hashmap;
    }
    private $UK_grid_squares = Array(
        //the order of grid square letters in the UK NGR system - note that in the array they start from the bottom, like grid references
        //there is no I in team
        Array('V','W','X','Y','Z'),
        Array('Q','R','S','T','U'),
        Array('L','M','N','O','P'),
        Array('F','G','H','J','K'),
        Array('A','B','C','D','E')
    );
    private $UK_grid_numbers; //will be set up when the object is constructed

    //define return types
    public $DATA_ARRAY = false;
    public $HTML = true;
    //will be set up when the object is constructed
    public $TEXT_EUROPEAN;
    public $TEXT_UNICODE;
    public $TEXT_ASIAN;

    //ellipsoid parameters used during grid->lat/long conversions and Helmert transformations
    private $ellipsoid_Airy_1830 = Array(
        //Airy 1830 (OS)
        'a' => 6377563.396,
        'b' => 6356256.910
    );
    private $ellipsoid_Airy_1830_mod = Array(
        //Airy 1830 modified (OSI)
        'a' => 6377340.189,
        'b' => 6356034.447
    );
    private $ellipsoid_WGS84 = Array(
        //WGS84 (GPS)
        'a' => 6378137,
        'b' => 6356752.314140356
    );
    private $datumset_OSGB36 = Array(
        //Airy 1830 (OS)
        'a' => 6377563.396,
        'b' => 6356256.910,
        'F0' => 0.9996012717,
        'E0' => 400000,
        'N0' => -100000,
        'Phi0' => 49,
        'Lambda0' => -2
    );
    private $datumset_Ireland_1965 = Array(
        //Airy 1830 modified (OSI)
        'a' => 6377340.189,
        'b' => 6356034.447,
        'F0' => 1.000035,
        'E0' => 200000,
        'N0' => 250000,
        'Phi0' => 53.5,
        'Lambda0' => -8
    );
    private $datumset_IRENET95 = Array(
        //ITM (uses WGS84) (OSI) taken from http://en.wikipedia.org/wiki/Irish_Transverse_Mercator
        'a' => 6378137,
        'b' => 6356752.314140356,
        'F0' => 0.999820,
        'E0' => 600000,
        'N0' => 750000,
        'Phi0' => 53.5,
        'Lambda0' => -8
    );
    //UPS (uses WGS84), taken from http://www.epsg.org/guides/ number 7 part 2 "Coordinate Conversions and Transformations including Formulas"
    //officially defined in http://earth-info.nga.mil/GandG/publications/tm8358.2/TM8358_2.pdf
    private $datumset_UPS_North = Array(
        'a' => 6378137,
        'b' => 6356752.314140356,
        'F0' => 0.994,
        'E0' => 2000000,
        'N0' => 2000000,
        'Phi0' => 90,
        'Lambda0' => 0
    );
    private $datumset_UPS_South = Array(
        'a' => 6378137,
        'b' => 6356752.314140356,
        'F0' => 0.994,
        'E0' => 2000000,
        'N0' => 2000000,
        'Phi0' => -90,
        'Lambda0' => 0
    );
    public function get_ellipsoid($name) {
        $name = 'ellipsoid_'.$name;
        if( isset( $this->$name ) ) {
            return $this->$name;
        }
        return null;
    }
    public function create_ellipsoid($a,$b) {
        return Array('a'=>$a,'b'=>$b);
    }
    public function get_datum($name) {
        $name = 'datumset_'.$name;
        if( isset( $this->$name ) ) {
            return $this->$name;
        }
        return null;
    }
    public function create_datum($ellip,$F0,$E0,$N0,$Phi0,$Lambda0) {
        if( !isset($ellip['a']) ) {
            return null;
        }
        return Array('a'=>$ellip['a'],'b'=>$ellip['b'],'F0'=>$F0,'E0'=>$E0,'N0'=>$N0,'Phi0'=>$Phi0,'Lambda0'=>$Lambda0);
    }

    //conversions between 12345,67890 grid references and latitude/longitude formats
    public $COORDS_OS_UK = 1;
    public $COORDS_OSI = 2;
    public $COORDS_GPS_UK = 3;
    public $COORDS_GPS_IRISH = 4;
    public $COORDS_GPS_ITM = 5;
    public function grid_to_lat_long($E,$N,$type = false,$return_type = false) {
        //horribly complex conversion according to "A guide to coordinate systems in Great Britain" Annexe C:
        //http://www.ordnancesurvey.co.uk/oswebsite/gps/information/coordinatesystemsinfo/guidecontents/
        //http://www.movable-type.co.uk/scripts/latlong-gridref.html shows an alternative script for JS, which also says what some OS variables represent
        if( is_array( $E ) ) {
            //passed an array, split it into parts
            $return_type = $type;
            $type = $N;
            $N = $E[1];
            $E = $E[0];
        }
        //get appropriate ellipsoid semi-major axis 'a' (metres) and semi-minor axis 'b' (metres),
        //grid scale factor on central meridian, and true origin (grid and lat-long) from Annexe A
        //extracts variables called $a,$b,$F0,$E0,$N0,$Phi0,$Lambda0
        if( is_array($type) ) {
            extract( $type, EXTR_SKIP );
        } elseif( $type == $this->COORDS_OS_UK || $type == $this->COORDS_GPS_UK ) {
            extract( $this->datumset_OSGB36, EXTR_SKIP );
        } elseif( $type == $this->COORDS_GPS_ITM ) {
            extract( $this->datumset_IRENET95, EXTR_SKIP );
        } elseif( $type == $this->COORDS_OSI || $type == $this->COORDS_GPS_IRISH ) {
            extract( $this->datumset_Ireland_1965, EXTR_SKIP );
        }
        if( !isset($F0) ) {
            //invalid type
            return false;
        }
        //PHP will not allow expressions in the arrays as they are defined inline as class properties, so do the conversion to radians here
        $Phi0 *= M_PI / 180;
        //eccentricity-squared from Annexe B B1
        //$e2 = ( ( $a * $a ) - ( $b * $b ) ) / ( $a * $a );
        $e2 = 1 - ( $b * $b ) / ( $a * $a ); //optimised
        //C1
        $n = ( $a - $b ) / ( $a + $b );
        //pre-compute values that will be re-used many times in the C3 formula
        $n2 = $n * $n;
        $n3 = pow( $n, 3 );
        $n_parts1 = ( 1 + $n + 1.25 * $n2 + 1.25 * $n3 );
        $n_parts2 = ( 3 * $n + 3 * $n2 + 2.625 * $n3 );
        $n_parts3 = ( 1.875 * $n2 + 1.875 * $n3 );
        $n_parts4 = ( 35 / 24 ) * $n3;
        //iterate to find latitude (when $N - $N0 - $M < 0.01mm)
        $Phi = $Phi0;
        $M = 0;
        $loopcount = 0;
        do {
            //C6 and C7
            $Phi += ( ( $N - $N0 - $M ) / ( $a * $F0 ) );
            //C3
            $M = $b * $F0 * (
                $n_parts1 * ( $Phi - $Phi0 ) -
                $n_parts2 * sin( $Phi - $Phi0 ) * cos( $Phi + $Phi0 ) +
                $n_parts3 * sin( 2 * ( $Phi - $Phi0 ) ) * cos( 2 * ( $Phi + $Phi0 ) ) -
                $n_parts4 * sin( 3 * ( $Phi - $Phi0 ) ) * cos( 3 * ( $Phi + $Phi0 ) )
            ); //meridonal arc
            //due to number precision, it is possible to get infinite loops here for extreme cases (especially for invalid ellipsoid numbers)
            //in tests, upto 6 loops are needed for grid 25 times Earth circumference - if it reaches 100, assume it must be infinite, and break out
        } while( abs( $N - $N0 - $M ) >= 0.00001 && ++$loopcount < 100 ); //0.00001 == 0.01 mm
        //pre-compute values that will be re-used many times in the C2 and C8 formulae
        $sin_Phi = sin( $Phi );
        $sin2_Phi = $sin_Phi * $sin_Phi;
        $tan_Phi = tan( $Phi );
        $sec_Phi = 1 / cos( $Phi );
        $tan2_Phi = $tan_Phi * $tan_Phi;
        $tan4_Phi = $tan2_Phi * $tan2_Phi;
        //C2
        $Rho = $a * $F0 * ( 1 - $e2 ) * pow( 1 - $e2 * $sin2_Phi, -1.5 ); //meridional radius of curvature
        $Nu = $a * $F0 / sqrt( 1 - $e2 * $sin2_Phi ); //transverse radius of curvature
        $Eta2 = $Nu / $Rho - 1;
        //pre-compute more values that will be re-used many times in the C8 formulae
        $Nu3 = pow( $Nu, 3 );
        $Nu5 = pow( $Nu, 5 );
        //C8 parts
        $VII = $tan_Phi / ( 2 * $Rho * $Nu );
        $VIII = ( $tan_Phi / ( 24 * $Rho * $Nu3 ) ) * ( 5 + 3 * $tan2_Phi + $Eta2 - 9 * $tan2_Phi * $Eta2 );
        $IX = ( $tan_Phi / ( 720 * $Rho * $Nu5 ) ) * ( 61 + 90 * $tan2_Phi + 45 * $tan4_Phi );
        $X = $sec_Phi / $Nu;
        $XI = ( $sec_Phi / ( 6 * $Nu3 ) ) * ( ( $Nu / $Rho ) + 2 * $tan2_Phi );
        $XII = ( $sec_Phi / ( 120 * $Nu5 ) ) * ( 5 + 28 * $tan2_Phi + 24 * $tan4_Phi );
        $XIIA = ( $sec_Phi / ( 5040 * pow( $Nu, 7 ) ) ) * ( 61 + 662 * $tan2_Phi + 1320 * $tan4_Phi + 720 * pow( $tan_Phi, 6 ) );
        //C8, C9
        $Edif = $E - $E0;
        $latitude = ( $Phi - $VII * $Edif * $Edif + $VIII * pow( $Edif, 4 ) - $IX * pow( $Edif, 6 ) ) * ( 180 / M_PI );
        $longitude = $Lambda0 + ( $X * $Edif - $XI * pow( $Edif, 3 ) + $XII * pow( $Edif, 5 ) - $XIIA * pow( $Edif, 7 ) ) * ( 180 / M_PI );
        if( $type == $this->COORDS_GPS_UK ) {
            list( $latitude, $longitude ) = $this->Helmert_transform( $latitude, $longitude, $this->ellipsoid_Airy_1830, $this->Helmert_OSGB36_to_WGS84, $this->ellipsoid_WGS84 );
        } elseif( $type == $this->COORDS_GPS_IRISH ) {
            list( $latitude, $longitude ) = $this->Helmert_transform( $latitude, $longitude, $this->ellipsoid_Airy_1830_mod, $this->Helmert_Ireland65_to_WGS84, $this->ellipsoid_WGS84 );
        }
        //force the longitude between -180 and 180
        if( $longitude > 180 || $longitude < -180 ) {
            $longitude -= floor( ( $longitude + 180 ) / 360 ) * 360;
        }
        if( $return_type ) {
            //sprintf to produce simple numbers instead of scientific notation (also reduces accuracy to 6 decimal places)
            $deg = is_string($return_type) ? $return_type : '&deg;';
            return sprintf( '%F', $latitude ) . $deg . ', ' . sprintf( '%F', $longitude ) . $deg;
        } else {
            //avoid stupid -0 by adding 0
            return Array($latitude+0,$longitude+0);
        }
    }

    //Helmert transform parameters used during Helmert transformations
    //OSGB<->WGS84 parameters taken from "6.6 Approximate WGS84 to OSGB36/ODN transformation"
    //http://www.ordnancesurvey.co.uk/oswebsite/gps/information/coordinatesystemsinfo/guidecontents/guide6.html
    private $Helmert_WGS84_to_OSGB36 = Array(
        'tx' => -446.448,
        'ty' => 125.157,
        'tz' => -542.060,
        's' => 20.4894,
        'rx' => -0.1502,
        'ry' => -0.2470,
        'rz' => -0.8421
    );
    private $Helmert_OSGB36_to_WGS84 = Array(
        'tx' => 446.448,
        'ty' => -125.157,
        'tz' => 542.060,
        's' => -20.4894,
        'rx' => 0.1502,
        'ry' => 0.2470,
        'rz' => 0.8421
    );
    //Ireland65<->WGS84 parameters taken from http://en.wikipedia.org/wiki/Helmert_transformation
    private $Helmert_WGS84_to_Ireland65 = Array(
        'tx' => -482.53,
        'ty' => 130.596,
        'tz' => -564.557,
        's' => -8.15,
        'rx' => 1.042,
        'ry' => 0.214,
        'rz' => 0.631
    );
    private $Helmert_Ireland65_to_WGS84 = Array(
        'tx' => 482.53,
        'ty' => -130.596,
        'tz' => 564.557,
        's' => 8.15,
        'rx' => -1.042,
        'ry' => -0.214,
        'rz' => -0.631
    );
    public function get_transformation($name) {
        $name = 'Helmert_'.$name;
        if( isset( $this->$name ) ) {
            return $this->$name;
        }
        return null;
    }
    public function create_transformation($tx,$ty,$tz,$s,$rx,$ry,$rz) {
        return Array('tx'=>$tx,'ty'=>$ty,'tz'=>$tz,'s'=>$s,'rx'=>$rx,'ry'=>$ry,'rz'=>$rz);
    }
    public function Helmert_transform($N,$E,$H,$from,$via = false,$to = false,$return_type = false) {
        //conversion according to formulae listed on http://www.movable-type.co.uk/scripts/latlong-convert-coords.html
        //parts taken from http://www.ordnancesurvey.co.uk/oswebsite/gps/information/coordinatesystemsinfo/guidecontents/
        $has_height = true;
        if( is_array( $N ) ) {
            //passed an array, split it into parts
            $return_type = $via;
            $to = $from;
            $via = $H;
            $from = $E;
            $E = $N[1];
            $N = $N[0];
            $has_height = isset( $N[2] );
            $H = $has_height ? $N[2] : 0;
        } elseif( is_array( $H ) ) {
            //no height, assume 0
            $has_height = false;
            $return_type = $to;
            $to = $via;
            $via = $from;
            $from = $H;
            $H = 0;
        }
        //work in radians
        $N *= M_PI / 180;
        $E *= M_PI / 180;
        //convert polar coords to cartesian
        //eccentricity-squared of source ellipsoid from Annexe B B1
        $e2 = 1 - ( $from['b'] * $from['b'] ) / ( $from['a'] * $from['a'] );
        $sin_Phi = sin( $N );
        $cos_Phi = cos( $N );
        //transverse radius of curvature
        $Nu = $from['a'] / sqrt( 1 - $e2 * $sin_Phi * $sin_Phi );
        $x = ( $Nu + $H ) * $cos_Phi * cos( $E );
        $y = ( $Nu + $H ) * $cos_Phi * sin( $E );
        $z = ( ( 1 - $e2 ) * $Nu + $H ) * $sin_Phi;
        //extracts variables called $tx,$ty,$tz,$s,$rx,$ry,$rz
        extract( $via, EXTR_SKIP );
        //convert seconds to radians
        $rx *= M_PI / 648000;
        $ry *= M_PI / 648000;
        $rz *= M_PI / 648000;
        //convert ppm to pp_one, and add one to avoid recalculating
        $s = $s / 1000000 + 1;
        //apply Helmert transform (algorithm notes incorrectly show rx instead of rz in $x1 line)
        $x1 = $tx + $s * $x - $rz * $y + $ry * $z;
        $y1 = $ty + $rz * $x + $s * $y - $rx * $z;
        $z1 = $tz - $ry * $x + $rx * $y + $s * $z;
        //convert cartesian coords back to polar
        //eccentricity-squared of destination ellipsoid from Annexe B B1
        $e2 = 1 - ( $to['b'] * $to['b'] ) / ( $to['a'] * $to['a'] );
        $p = sqrt( $x1 * $x1 + $y1 * $y1 );
        $Phi = atan2( $z1, $p * ( 1 - $e2 ) );
        $Phi1 = 2 * M_PI;
        $accuracy = 0.000001 / $to['a']; //0.01 mm accuracy, though the OS transform itself only has 4-5 metres
        $loopcount = 0;
        //due to number precision, it is possible to get infinite loops here for extreme cases (especially for invalid parameters)
        //in tests, upto 4 loops are needed - if it reaches 100, assume it must be infinite, and break out
        while( abs( $Phi - $Phi1 ) > $accuracy && $loopcount++ < 100 ) {
            $sin_Phi = sin( $Phi );
            $Nu = $to['a'] / sqrt( 1 - $e2 * $sin_Phi * $sin_Phi );
            $Phi1 = $Phi;
            $Phi = atan2( $z1 + $e2 * $Nu * $sin_Phi, $p );
        }
        $Lambda = atan2( $y1, $x1 );
        $H = ( $p / cos( $Phi ) ) - $Nu;
        //done converting - return in degrees - avoid stupid -0 by adding 0
        $latitude = ( $Phi * ( 180 / M_PI ) ) + 0;
        $longitude = ( $Lambda * ( 180 / M_PI ) ) + 0;
        if( $return_type ) {
            //sprintf to produce simple numbers instead of scientific notation (also reduces accuracy to 6 decimal places)
            $deg = is_string($return_type) ? $return_type : '&deg;';
            return sprintf( '%F', $latitude ) . $deg . ', ' . sprintf( '%F', $longitude ) . $deg . ( $has_height ? ( ', ' . sprintf( '%F', $H ) ) : '' );
        } else {
            $temparray = Array($latitude,$longitude);
            if( $has_height ) { $temparray[] = $H; }
            return $temparray;
        }
    }
}

?>

