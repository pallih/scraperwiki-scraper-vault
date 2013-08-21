<?php
require  'scraperwiki/simple_html_dom.php';

// Using my own lazy XML Parser here

function xml2array($contents, $get_attributes=1) {
    if(!$contents) return array();

    if(!function_exists('xml_parser_create')) {
        //print "'xml_parser_create()' function not found!";
        return array();
    }
    //Get the XML parser of PHP - PHP must have this module for the parser to work
    $parser = xml_parser_create();
    xml_parser_set_option( $parser, XML_OPTION_CASE_FOLDING, 0 );
    xml_parser_set_option( $parser, XML_OPTION_SKIP_WHITE, 1 );
    xml_parse_into_struct( $parser, $contents, $xml_values );
    xml_parser_free( $parser );

    if(!$xml_values) return;//Hmm...

    //Initializations
    $xml_array = array();
    $parents = array();
    $opened_tags = array();
    $arr = array();

    $current = &$xml_array;

    //Go through the tags.
    foreach($xml_values as $data) {
        unset($attributes,$value);//Remove existing values, or there will be trouble

        //This command will extract these variables into the foreach scope
        // tag(string), type(string), level(int), attributes(array).
        extract($data);//We could use the array by itself, but this cooler.

        $result = '';
        if($get_attributes) {//The second argument of the function decides this.
            $result = array();
            if(isset($value)) $result['value'] = $value;

            //Set the attributes too.
            if(isset($attributes)) {
                foreach($attributes as $attr => $val) {
                    if($get_attributes == 1) $result['attr'][$attr] = $val; //Set all the attributes in a array called 'attr'
                    /**  :TODO: should we change the key name to '_attr'? Someone may use the tagname 'attr'. Same goes for 'value' too */
                }
            }
        } elseif(isset($value)) {
            $result = $value;
        }

        //See tag status and do the needed.
        if($type == "open") {//The starting of the tag '<tag>'
            $parent[$level-1] = &$current;

            if(!is_array($current) or (!in_array($tag, array_keys($current)))) { //Insert New tag
                $current[$tag] = $result;
                $current = &$current[$tag];

            } else { //There was another element with the same tag name
                if(isset($current[$tag][0])) {
                    array_push($current[$tag], $result);
                } else {
                    $current[$tag] = array($current[$tag],$result);
                }
                $last = count($current[$tag]) - 1;
                $current = &$current[$tag][$last];
            }

        } elseif($type == "complete") { //Tags that ends in 1 line '<tag />'
            //See if the key is already taken.
            if(!isset($current[$tag])) { //New Key
                $current[$tag] = $result;

            } else { //If taken, put all things inside a list(array)
                if((is_array($current[$tag]) and $get_attributes == 0)//If it is already an array...
                        or (isset($current[$tag][0]) and is_array($current[$tag][0]) and $get_attributes == 1)) {
                    array_push($current[$tag],$result); // ...push the new element into that array.
                } else { //If it is not an array...
                    $current[$tag] = array($current[$tag],$result); //...Make it an array using using the existing value and the new value
                }
            }

        } elseif($type == 'close') { //End of tag '</tag>'
            $current = &$parent[$level-1];
        }
    }

    return($xml_array);
} 

function get_xml($url) {
$ch = curl_init($url);

curl_setopt($ch, CURLOPT_HEADER, 0); 
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

$data = curl_exec($ch);

curl_close($ch); 

$news = xml2array($data);
return $news;
}


$html = scraperwiki::scrape("http://www.cicregulator.gov.uk/coSearch/companyList.shtml");

$dom = new simple_html_dom();
$dom->load($html);

$rows = $dom->find('tr');

// Dump the first element of the array as it contains headers
array_shift($rows);

foreach($rows as $row)
{
    $name = $row->children[0]->plaintext;

    $number = $row->children[1]->plaintext;
    $location = $row->children[2]->plaintext;
    $url = "http://opencorporates.com/companies/uk/". $number .".xml";
    $xml = get_xml($url);
    
    ///sometimes the xml source file isn't found or is a 404 page or an error response
    if(empty($xml) 
    || isset($xml['html']) 
    || (isset($xml['head']) 
        && isset($xml['head']['title']) 
        && isset($xml['head']['title']['value']) 
        && $xml['head']['title']['value'] == 'Error response')
    ){
        continue;
    }
    if(!isset($xml['company'])){
        print_r(array('xml'=>$xml, 'url'=>$url, 'isset'=>isset($xml), 'is_array'=>is_array($xml), 'empty'=>empty($xml)));
        die;
    }

    if(isset($xml['company']['incorporation-date']) && isset($xml['company']['incorporation-date']['value'])){
        $incorporationdate = $xml['company']['incorporation-date']['value'];
    }else{
        $incorporationdate = '';
    }

    if(isset($xml['company']['registered-address-in-full']) && isset($xml['company']['registered-address-in-full']['value'])){
        $address = $xml['company']['registered-address-in-full']['value'];
    }else{
        $address = '';
    }
    
    if(isset($xml['company']['opencorporates-url']) && !isset($xml['company']['opencorporates-url']['value'])){
        $opencorporates = $xml['company']['opencorporates-url']['value'];
    }else{
        $opencorporates = '';
    }
    
    if(isset($xml['company']['current-status']) && !isset($xml['company']['current-status']['value'])){
        $status = $xml['company']['current-status']['value'];
    }else{
        $status = '';
    }

    $siccodes = array();
    $i=1;
    foreach ($xml['company']['sic-codes'] as $key=>$sic) {
        ///ignore the non-sic codes
        if($key == 'sic-code'){
            if(is_array($sic) && isset($sic['value'])){
                $siccodes[] = $sic['value'];
            }else if(is_array($sic) && isset($sic['title']['value'])){
                $siccodes[] = $sic['title']['value'];
            }else{
                print_r(array('sic'=>$sic)); die;
            }        
        }    
    }

    $sic = implode(",", $siccodes);

    if ($name != "Back to top") {
    scraperwiki::save(array('Company Number'), array('Company Name' => $name, 'Company Number' => $number, 'Incorpotation Date' => $incorporationdate,'Address' => $address, 'Open Corporates URL' => $opencorporates, 'Sic Codes' => $sic, 'Status' => $status));
    }
}

?>