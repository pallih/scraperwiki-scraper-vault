<?php
require 'scraperwiki/simple_html_dom.php';
    #
    # this is a 'loose' JSON decoder. the built-in PHP JSON decoder
    # is very strict, and will not accept things which are fairly
    # common in the wild:
    #
    #  * unquoted keys, e.g. {foo: 1}
    #  * single-quoted strings, e.g. {"foo": 'bar'}
    #  * escaped single quoted, e.g. {"foo": "b\'ar"}
    #  * empty array elements, e.g. [1,,2]
    #

    $GLOBALS['json_strings'] = array();

    # these are used as placeholders. they must:
    # 1) only contain alpha, numerics, underscore and dash
    # 2) not exist in the actual json
    $GLOBALS['json_str_prefix'] = 'JSON-STRING-XYZ';
    $GLOBALS['json_slash_temp'] = 'JSON-SLASH-PAIR-XYZ';


scrapePP();#scrape Perro Perdido

//scrapeHF();#scrape Hocicos Felices

//scrapeRM();#scrape Red  Mascotera
//scrapeDH();#scrape Dejando Huellas

    function json_decode_loose($json){

        $GLOBALS['json_strings'] = array();


        #
        # first find obvious strings
        #
#echo "PRE-FIND: $json\n";
        $json = preg_replace_callback('!"((?:[^\\\\"]|\\\\\\\\|\\\\")*)"!', 'json_dqs', $json);
        $json = preg_replace_callback("!'((?:[^\\\\']|\\\\\\\\|\\\\')*)'!", 'json_sqs', $json);
#echo "POST-FIND: $json\n";
#print_r($GLOBALS['json_strings']);

        $json = preg_replace('!\s+!', '', $json);


        #
        # missing elements
        #

        $json = str_replace('[,', '[null,', $json);
        $json = str_replace('{,', '{', $json);

        $json = str_replace(',]', ']', $json);
        $json = str_replace(',}', '}', $json);

        $json = preg_replace('!\[([^[{]+),(\s*),!', '[$1,null,', $json);
        $json = preg_replace('!\{([^[{]+),(\s*),!', '{$1,', $json);


        #
        # quote unquoted key names
        #

        $json = preg_replace_callback('!([a-zA-Z0-9-_]+):!', 'json_key', $json);


        #
        # turn remaning barewords into nulls.
        # loosely based on the ECMA spec, but avoiding requiring unicode PCRE.
        # http://www.ecma-international.org/publications/files/ECMA-ST/Ecma-262.pdf
        # (section 7.6)
        #

        $start = "[A-Za-z\$_]|(\\\\u[0-9A-Fa-f]{4})";
        $continue = $start.'|[0-9-.]';

        $json = preg_replace_callback("!(($start)($continue)*)!", 'json_bareword', $json);


        #
        # strip functions
        #

        $l = strlen($json);
        while (1){
            $json = preg_replace("!null\(([^()]*)\)!", 'null', $json);
            $l2 = strlen($json);
            if ($l == $l2) break;
            $l = $l2;
        }


        #
        # replace the strings
        #

#echo "PRE-CONV: $json\n";

        $pre = preg_quote($GLOBALS['json_str_prefix'], '!');
        $json = preg_replace_callback('!'.$pre.'(\d+)!', 'json_strs', $json);

#echo "POST-CONV: $json\n";

        $ret = JSON_decode($json, true);

        if ($ret === null){
            die("Failed to parse JSON:\n$json\n");
        }

        return $ret;
    }


    function json_dqs($m){

        $idx = count($GLOBALS['json_strings']);
        $GLOBALS['json_strings'][$idx] = $m[1];

        return $GLOBALS['json_str_prefix'].$idx;
    }

    function json_sqs($m){

        $text = str_replace("\\\\", $GLOBALS['json_slash_temp'], $m[1]);
        $text = str_replace("\\'", "'", $text);
        $text = str_replace('"', "\\\"", $text);
        $text = str_replace($GLOBALS['json_slash_temp'], "\\\\", $text);

        $idx = count($GLOBALS['json_strings']);
        $GLOBALS['json_strings'][$idx] = $text;

        return $GLOBALS['json_str_prefix'].$idx;
    }

    function json_strs($m){

        return '"'.$GLOBALS['json_strings'][$m[1]].'"';
    }

    function json_key($m){

        if (strpos($m[1], $GLOBALS['json_str_prefix']) === 0) return $m[0];

        $idx = count($GLOBALS['json_strings']);
        $GLOBALS['json_strings'][$idx] = $m[1];

        return $GLOBALS['json_str_prefix'].$idx.':';
    }

    function json_bareword($m){

        # just a string token
        if (strpos($m[1], $GLOBALS['json_str_prefix']) === 0) return $m[0];

        # reserved words we allow
        $low = StrToLower($m[1]);
        if ($low == 'null') return 'null';
        if ($low == 'true') return 'true';
        if ($low == 'false') return 'false';

        # otherwise it's likely a variable reference, so remove it
        return 'null';
    }
    function scrapePP() {
        $url="http://www.perroperdido.com.ar/mapa-perros.php?foto=b&a=u";
        $html_content = scraperWiki::scrape($url);
        //print $html_content;
        $script_htmls = returnSubstrings($html_content,'var Puntos = {"puntos": [','</script>');
        $pet_htmls = returnSubstrings($script_htmls[0],'{','}');
        
        if (count($pet_htmls) > 0) {
          //array_shift($pet_htmls);
              //print $pet_htmls[0];  
              foreach ($pet_htmls as $pet_html_raw) {
                    //print "pet found: ".$pet_html_raw;
                    $pet_html_raw="{".$pet_html_raw."}";
                    $parsed=json_decode_loose($pet_html_raw);
                     echo $parsed["id"]; 
            }
        }
        /*
        $html = str_get_html($html_content);
        $div =$html->find('div[id=contenido]',0);
        foreach($div->find('ul') as $ul) {
               foreach($ul->find('li') as $li) {
                 $src="";
                $pet_images = array();
                $text = $li->plaintext;
                $address = $li->find('b',0)->plaintext;
                $contact = $li->find('b',1)->plaintext;
                $text = str_replace($contact,'',$text);
                $pieces = explode($address, $text);
                if (count($pieces) > 0) {
                    $date = trim($pieces[1]);
                    $more_info = trim($pieces[0]);
                }
                else {
                    $date = date("Y-m-d H:i:s", time());
                    $more_info = $text;
                }
                //print $more_info." - ".$date." - ".$address." - ".$contact." - ".$src."\n";



                foreach ($li->find("a") as $a) {
                    $img = $a->find('input',0);
                    $pet_images[]=$url.$img->src;
                    //Scrapear el Mapa para saber Lat y Lon originales
                    $pet_detailurl = str_replace("foto.php","mapa.php",$a->href);

                }
                $pet_data["Images"]=$pet_images;
                $pet_data["Titulo"]=$date;

                $pet_data["Mas_info"]=trim($more_info)." ".$address." ".$contact;
                $pet_data["Direccion"]=$address;
                $pet_data["Ingresada"]= date("Y-m-d H:i:s", time());

                    print $more_info." - ".$date." - ".$address." - ".$contact." - ".$pet_detailurl."\n";
               }
        }
    */
    }




    function scrapeHF() {
        $url="http://www.hocicosfelices.com.ar/buscados";
        $html_content = scraperWiki::scrape($url);
        $html = str_get_html($html_content);
        $html_div=$html->find("div.entry-content",0);

        $pet_htmls = returnSubstrings($html_div,'<h3','<h3');
        
        if (count($pet_htmls) > 0) {
          array_shift($pet_htmls);
              foreach ($pet_htmls as $pet_html_raw) {
                    //print "pet found: ".$pet_html."\n";
                    $pet_html_raw="<h3".$pet_html_raw;
                    $pet_html = str_get_html($pet_html_raw);


                    $title = $pet_html->find("h3",0)->plaintext;
                    $more_info = $pet_html->find("p",0)->plaintext;
                    $img_html = $pet_html->find("img",0)->outertext;


                $pet_data = array();
                $pet_data["Codigo"]=utf8_encode(trim($title));
                $pet_data["Titulo"]=(trim($title));
                $pet_data["Mas_info"]=(trim($more_info))."<br>".$img_html;
                $address="";
                if (array_key_exists('Calle', $pet_data)) {
                    $address =$pet_data["Calle"].", ";
                }
                if (array_key_exists('Barrio', $pet_data)) {
                    $address.=$pet_data["Barrio"].", ";
                }            
                $address.="San Carlos de Bariloche, Río Negro, Argentina";
                $pet_data["Direccion"]=$address;
    
                $geo_data=geoCode($address);
                //$geo_data=geoCode($more_info);
                
                //$pet_data["Cat"]=$cat_ext;
                if (array_key_exists('lat', $geo_data)) {
                    $pet_data["Lat"]=$geo_data["lat"];
                    $pet_data["Lng"]=$geo_data["lng"];
                    $pet_data["Direccion_geo"]=$geo_data["formatted_address"];
    
                    createReport($pet_data);
                    //scraperwiki::save(array('Codigo'), $pet_data);
    
                }
    
              
                }
        }
        

    }


    function createReport($petdata)
    {
        /*
        $lat = $petdata["Lat"];
        $lon = $petdata["Lng"];
        $latlon = $lat.','.$lon;

        // Create Location
        $location = new Location_Model();
        $location->location_name = $petdata["Direccion"];
        $location->latitude = $lat;
        $location->longitude = $lon;
        $location->location_date = $petdata["Ingresada"];
        $location->save();                

        // Create Report
        $incident = new Incident_Model();
        $incident->location_id = $location->id;
        $incident->form_id = 1;
        $incident->user_id = $_SESSION['auth_user']->id;
        $incident->incident_title = $petdata["Titulo"];
        $incident->incident_description = $petdata["Mas_info"];
        $incident->incident_date = $petdata["Ingresada"];
        $incident->incident_dateadd = date("Y-m-d H:i:s", time());
        $incident->incident_active = 1;
        $incident->incident_verified = 0;
        //Save
        $incident->save();
        // Set Category (only setting one category per report)
        $incident_category = new Incident_Category_Model();
        $incident_category->incident_id = $incident->id;
        $incident_category->category_id = $petdata["Cat"];
        $incident_category->save();

        */
                $name = $petdata["Titulo"];
        $lname = $petdata["Direccion"];
        $latitude = $petdata["Lat"];
        $longitude = $petdata["Lng"];
        $description = $petdata["Mas_info"];
        $incidentdate = $petdata["Ingresada"];
        $incidenthour = 0;
        $incidentmin = 0;
        $incidentam = date("a");
        $category = $petdata["Cat"];

        $posturl = "http://www.buscadormascotas.com.ar/bm/"; //YOUR USHAHIDI URL HERE
        $Curl_Session = curl_init($posturl);
        curl_setopt ($Curl_Session, CURLOPT_POST, 1);
        
        $post_data="task=report&incident_title=$name&incident_description=$description&incident_date=$incidentdate&incident_hour=$incidenthour";
        $post_data.="&incident_minute=$incidentmin&incident_ampm=$incidentam&incident_category=$category&latitude=$latitude&longitude=$longitude&location_name=$lname";

        curl_setopt ($Curl_Session, CURLOPT_POSTFIELDS,$post_data );
        //You may need to edit this line with the correct variable names

        curl_setopt ($Curl_Session, CURLOPT_FOLLOWLOCATION, 1);
        curl_exec ($Curl_Session);
        curl_close ($Curl_Session);


    }

/**
* finds substrings between opening and closing markers
* @return result array of the substrings
*/
function returnSubstrings($text, $openingMarker, $closingMarker) {
    $openingMarkerLength = strlen($openingMarker);
    $closingMarkerLength = strlen($closingMarker);
    
    $result = array();
    $position = 0;
    while (($position = strpos($text, $openingMarker, $position)) !== false) {
    $position += $openingMarkerLength;
    if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {
    $result[] = substr($text, $position, $closingMarkerPosition - $position);
    $position = $closingMarkerPosition + $closingMarkerLength;
    }
    }
    return $result;
}

function scrapeDH(){
    $max=0;
    for ($index=0; $index<=$max; $index+=20) {
        $url="http://www.derechoanimal.com.ar/dejandohuellas/Result-Cla.asp?letra=1&pag=".$index;
        $html_content = scraperWiki::scrape($url);
        $html = str_get_html($html_content);
        $pets_data = array();
        foreach ($html->find("td.interior") as $html_el) {
            $pet_data = array();
            $tags = explode("&nbsp;",$html_el->plaintext);
            if (sizeof($tags)>1) {
                $code = "DH-PER".utf8_encode(trim($tags[0]));
                $code = str_replace('(','',$code);
                $code = str_replace(')','',$code);
                $pet_data["Codigo"]=utf8_encode(trim($code));
                $pet_data["Provincia"]="Rio Negro";
                $pet_data["Localidad"]="San Carlos De Bariloche";
                $pet_data["Direccion"]=$geo_data["formatted_address"];
                $pet_data["Ingresada"]=date_create_from_format('d/m/Y H:i:s', trim($tags[1]));  
                $pet_data["Mas_info"]=utf8_encode(trim($tags[2]));
                $pet_data["URL"]=utf8_encode($url);
                $geo_data=geoCode($pet_data["Localidad"].", ".$pet_data["Provincia"]);
                $pet_data["Lat"]=$geo_data["lat"];
                $pet_data["Lng"]=$geo_data["lng"];
                scraperwiki::save(array('Codigo'), $pet_data);
            }
         }
    }
}

function scrapeRM(){
    $max=90;
    for ($index=0; $index<$max; $index+=30) {
        $url="http://www.redmascotera.com/see_pet.php?ini=".$index."&bu_pais=1";
        $html_content = scraperWiki::scrape($url);
        $html = str_get_html($html_content);
        $pets_data = array();
        foreach ($html->find("div.cont_m") as $html_el) {
            $pet_data = array();
            $code = $html_el->find("h3 strong",0)->plaintext;
            $title = $html_el->find("h3",0)->plaintext;
            $title = str_replace($code,'',$title);
            $pet_data["Codigo"]=utf8_encode(trim($code));
            $pet_data["Titulo"]=utf8_encode(trim($title));
            $link = $html_el->find("a",0)->href;
            $detail_url="http://www.redmascotera.com/" . $link;
            $detail_content = scraperWiki::scrape($detail_url);
            $detail = str_get_html($detail_content);
            $pet_info = $detail->find("div.bkg_presentacion",0);
            foreach ($pet_info->find("h5") as $pet_el) {
                $tags = explode(":",$pet_el->plaintext);
                $key = utf8_encode(trim($tags[0]));
                $value = utf8_encode(trim($tags[1]));
                if($key=="Ingresada") $value = date_create_from_format('d/m/Y', $value);
                if($key=="Provincia" && $value=="Capital y GBA") $value="Buenos Aires";
                $pet_data[$key]=$value;
            }
            foreach ($pet_info->find("p") as $contact_el) {
                $tags = explode(":",$contact_el->plaintext);
                $key = utf8_encode(trim($tags[0]));
                $value = utf8_encode(trim($tags[1]));
                $pet_data[$key]=$value;
            }    
            $pet_extra = $detail->find("div.bkg_presentacion",1);
            $more_info = $pet_extra->find("p",0)->plaintext;
            $pet_data["Mas_info"]=utf8_encode(trim($more_info));
            $pet_data["URL"]=utf8_encode($detail_url);
            $geo_data=geoCode($pet_data["Calle"].", ".$pet_data["Barrio"].", ".$pet_data["Localidad"].", ".$pet_data["Provincia"].", Argentina");
            $pet_data["Lat"]=$geo_data["lat"];
            $pet_data["Lng"]=$geo_data["lng"];
            $pet_data["Direccion"]=$geo_data["formatted_address"];
    
            scraperwiki::save(array('Codigo'), $pet_data);
            $pets_data[] = $pet_data;
            $img = $html_el->find("img",0)->src;
            $p = $html_el->find("p",0);
            #print $title . " - " .$code . " - " .$link . " - " .$img. " - " .$p."\n";
        }
    }
}

function geoCode($address) {
return geoCodeYp($address);
}

function geoCodeGM($address) {
    $region = 'ar';
    $language = 'es';
    $out = array();
    $url = "http://maps.googleapis.com/maps/api/geocode/json?region={$region}&language={$language}&sensor=false&address=" . urlencode($address);
    $geocoded = json_decode(scraperwiki::scrape($url));
    print_r($geocoded);
    if ($geocoded->status == 'OK') {
        foreach ($geocoded->results[0]->address_components as $component) {
            $out[$component->types[0] . '-long_name'] = $component->long_name;
            $out[$component->types[0] . '-short_name'] = $component->short_name;
        }
        $out['lat'] = $geocoded->results[0]->geometry->location->lat;
        $out['lng'] = $geocoded->results[0]->geometry->location->lng;
        $out['formatted_address'] = $geocoded->results[0]->formatted_address;
    }
    return $out;
}

// Json encode the data
 
function json_code ($json)
{
$json = substr($json, strpos($json,'{')+1, strlen($json));
$json = substr($json, 0, strrpos($json,'}'));
$json=preg_replace('/(^|,)([\\s\\t]*)([^:]*) (([\\s\\t]*)):(([\\s\\t]*))/s','$1"$3"$4:',trim($json));
return json_decode('{'.$json.'}', true);
}
  
// function to get the geocode of the address
 
function geoCodeYp($point)
{
// Replace your Yahoo AppID here
$yahoo_appid = '_18CdmHV34HjeW_rXezIti6jhypsfSqMmAlFFGIOPWC1DW3p0CXYU9eaoL.COp0-';           
 
//URLEncode for eg convert space to %20 .
$pointenc = urlencode($point);
 
// URL Formation that will fetch you the results on query
$url="http://where.yahooapis.com/geocode?location=".$pointenc."&gflags=R&appid=".$yahoo_appid."&flags=J";
 
// get the contents of the URL formed
$jsondata = file_get_contents($url);
 
$json_data= '{
  a: 1,
  b: 245,
  c with whitespaces: "test me",
  d: "function () { echo \"test\" }",
  e: 5.66
  }';
  
 
 $coord=explode(" ",$point);
  
        // this will json encode the data .
  $convertedtoarray=json_code($jsondata);
   
  // line1 of addrress comprising of house,street no etc
        // line 2 of address comprising of city state country
  $line1 =$convertedtoarray['ResultSet']['Results']['0']['line1'] ;
        $line2 =$convertedtoarray['ResultSet']['Results']['0']['line1'] ;
  
        $county =$convertedtoarray['ResultSet']['Results']['0']['county'] ;
        $street =$convertedtoarray['ResultSet']['Results']['0']['street'] ;
   
   
if(($line1=="")||($line2=="")||($county=="")||($street==""))
{
   $yahooresults['status']="noresult";
}
 
else
{
      $countrycode=$convertedtoarray['ResultSet']['Results']['0']['countrycode'] ;
      $statecode=$convertedtoarray['ResultSet']['Results']['0']['statecode']   ;
      $city=$convertedtoarray['ResultSet']['Results']['0']['city'] ;
      $house=$convertedtoarray['ResultSet']['Results']['0']['house'] ;
      $latitude=$convertedtoarray['ResultSet']['Results']['0']['latitude'] ;
      $longitude=$convertedtoarray['ResultSet']['Results']['0']['longitude'] ;    
  
$yahooresults = array('countrycode'=>$countrycode,'statecode'=>$statecode,'county'=>$county,'city'=>$city,'street'=>$street,'house'=>$house,'lat'=>$latitude,'lng'=>$longitude, 'formatted_address'=>$line1.' '.$line2);   
}
   
 return $yahooresults ;
}
 
?><?php
require 'scraperwiki/simple_html_dom.php';
    #
    # this is a 'loose' JSON decoder. the built-in PHP JSON decoder
    # is very strict, and will not accept things which are fairly
    # common in the wild:
    #
    #  * unquoted keys, e.g. {foo: 1}
    #  * single-quoted strings, e.g. {"foo": 'bar'}
    #  * escaped single quoted, e.g. {"foo": "b\'ar"}
    #  * empty array elements, e.g. [1,,2]
    #

    $GLOBALS['json_strings'] = array();

    # these are used as placeholders. they must:
    # 1) only contain alpha, numerics, underscore and dash
    # 2) not exist in the actual json
    $GLOBALS['json_str_prefix'] = 'JSON-STRING-XYZ';
    $GLOBALS['json_slash_temp'] = 'JSON-SLASH-PAIR-XYZ';


scrapePP();#scrape Perro Perdido

//scrapeHF();#scrape Hocicos Felices

//scrapeRM();#scrape Red  Mascotera
//scrapeDH();#scrape Dejando Huellas

    function json_decode_loose($json){

        $GLOBALS['json_strings'] = array();


        #
        # first find obvious strings
        #
#echo "PRE-FIND: $json\n";
        $json = preg_replace_callback('!"((?:[^\\\\"]|\\\\\\\\|\\\\")*)"!', 'json_dqs', $json);
        $json = preg_replace_callback("!'((?:[^\\\\']|\\\\\\\\|\\\\')*)'!", 'json_sqs', $json);
#echo "POST-FIND: $json\n";
#print_r($GLOBALS['json_strings']);

        $json = preg_replace('!\s+!', '', $json);


        #
        # missing elements
        #

        $json = str_replace('[,', '[null,', $json);
        $json = str_replace('{,', '{', $json);

        $json = str_replace(',]', ']', $json);
        $json = str_replace(',}', '}', $json);

        $json = preg_replace('!\[([^[{]+),(\s*),!', '[$1,null,', $json);
        $json = preg_replace('!\{([^[{]+),(\s*),!', '{$1,', $json);


        #
        # quote unquoted key names
        #

        $json = preg_replace_callback('!([a-zA-Z0-9-_]+):!', 'json_key', $json);


        #
        # turn remaning barewords into nulls.
        # loosely based on the ECMA spec, but avoiding requiring unicode PCRE.
        # http://www.ecma-international.org/publications/files/ECMA-ST/Ecma-262.pdf
        # (section 7.6)
        #

        $start = "[A-Za-z\$_]|(\\\\u[0-9A-Fa-f]{4})";
        $continue = $start.'|[0-9-.]';

        $json = preg_replace_callback("!(($start)($continue)*)!", 'json_bareword', $json);


        #
        # strip functions
        #

        $l = strlen($json);
        while (1){
            $json = preg_replace("!null\(([^()]*)\)!", 'null', $json);
            $l2 = strlen($json);
            if ($l == $l2) break;
            $l = $l2;
        }


        #
        # replace the strings
        #

#echo "PRE-CONV: $json\n";

        $pre = preg_quote($GLOBALS['json_str_prefix'], '!');
        $json = preg_replace_callback('!'.$pre.'(\d+)!', 'json_strs', $json);

#echo "POST-CONV: $json\n";

        $ret = JSON_decode($json, true);

        if ($ret === null){
            die("Failed to parse JSON:\n$json\n");
        }

        return $ret;
    }


    function json_dqs($m){

        $idx = count($GLOBALS['json_strings']);
        $GLOBALS['json_strings'][$idx] = $m[1];

        return $GLOBALS['json_str_prefix'].$idx;
    }

    function json_sqs($m){

        $text = str_replace("\\\\", $GLOBALS['json_slash_temp'], $m[1]);
        $text = str_replace("\\'", "'", $text);
        $text = str_replace('"', "\\\"", $text);
        $text = str_replace($GLOBALS['json_slash_temp'], "\\\\", $text);

        $idx = count($GLOBALS['json_strings']);
        $GLOBALS['json_strings'][$idx] = $text;

        return $GLOBALS['json_str_prefix'].$idx;
    }

    function json_strs($m){

        return '"'.$GLOBALS['json_strings'][$m[1]].'"';
    }

    function json_key($m){

        if (strpos($m[1], $GLOBALS['json_str_prefix']) === 0) return $m[0];

        $idx = count($GLOBALS['json_strings']);
        $GLOBALS['json_strings'][$idx] = $m[1];

        return $GLOBALS['json_str_prefix'].$idx.':';
    }

    function json_bareword($m){

        # just a string token
        if (strpos($m[1], $GLOBALS['json_str_prefix']) === 0) return $m[0];

        # reserved words we allow
        $low = StrToLower($m[1]);
        if ($low == 'null') return 'null';
        if ($low == 'true') return 'true';
        if ($low == 'false') return 'false';

        # otherwise it's likely a variable reference, so remove it
        return 'null';
    }
    function scrapePP() {
        $url="http://www.perroperdido.com.ar/mapa-perros.php?foto=b&a=u";
        $html_content = scraperWiki::scrape($url);
        //print $html_content;
        $script_htmls = returnSubstrings($html_content,'var Puntos = {"puntos": [','</script>');
        $pet_htmls = returnSubstrings($script_htmls[0],'{','}');
        
        if (count($pet_htmls) > 0) {
          //array_shift($pet_htmls);
              //print $pet_htmls[0];  
              foreach ($pet_htmls as $pet_html_raw) {
                    //print "pet found: ".$pet_html_raw;
                    $pet_html_raw="{".$pet_html_raw."}";
                    $parsed=json_decode_loose($pet_html_raw);
                     echo $parsed["id"]; 
            }
        }
        /*
        $html = str_get_html($html_content);
        $div =$html->find('div[id=contenido]',0);
        foreach($div->find('ul') as $ul) {
               foreach($ul->find('li') as $li) {
                 $src="";
                $pet_images = array();
                $text = $li->plaintext;
                $address = $li->find('b',0)->plaintext;
                $contact = $li->find('b',1)->plaintext;
                $text = str_replace($contact,'',$text);
                $pieces = explode($address, $text);
                if (count($pieces) > 0) {
                    $date = trim($pieces[1]);
                    $more_info = trim($pieces[0]);
                }
                else {
                    $date = date("Y-m-d H:i:s", time());
                    $more_info = $text;
                }
                //print $more_info." - ".$date." - ".$address." - ".$contact." - ".$src."\n";



                foreach ($li->find("a") as $a) {
                    $img = $a->find('input',0);
                    $pet_images[]=$url.$img->src;
                    //Scrapear el Mapa para saber Lat y Lon originales
                    $pet_detailurl = str_replace("foto.php","mapa.php",$a->href);

                }
                $pet_data["Images"]=$pet_images;
                $pet_data["Titulo"]=$date;

                $pet_data["Mas_info"]=trim($more_info)." ".$address." ".$contact;
                $pet_data["Direccion"]=$address;
                $pet_data["Ingresada"]= date("Y-m-d H:i:s", time());

                    print $more_info." - ".$date." - ".$address." - ".$contact." - ".$pet_detailurl."\n";
               }
        }
    */
    }




    function scrapeHF() {
        $url="http://www.hocicosfelices.com.ar/buscados";
        $html_content = scraperWiki::scrape($url);
        $html = str_get_html($html_content);
        $html_div=$html->find("div.entry-content",0);

        $pet_htmls = returnSubstrings($html_div,'<h3','<h3');
        
        if (count($pet_htmls) > 0) {
          array_shift($pet_htmls);
              foreach ($pet_htmls as $pet_html_raw) {
                    //print "pet found: ".$pet_html."\n";
                    $pet_html_raw="<h3".$pet_html_raw;
                    $pet_html = str_get_html($pet_html_raw);


                    $title = $pet_html->find("h3",0)->plaintext;
                    $more_info = $pet_html->find("p",0)->plaintext;
                    $img_html = $pet_html->find("img",0)->outertext;


                $pet_data = array();
                $pet_data["Codigo"]=utf8_encode(trim($title));
                $pet_data["Titulo"]=(trim($title));
                $pet_data["Mas_info"]=(trim($more_info))."<br>".$img_html;
                $address="";
                if (array_key_exists('Calle', $pet_data)) {
                    $address =$pet_data["Calle"].", ";
                }
                if (array_key_exists('Barrio', $pet_data)) {
                    $address.=$pet_data["Barrio"].", ";
                }            
                $address.="San Carlos de Bariloche, Río Negro, Argentina";
                $pet_data["Direccion"]=$address;
    
                $geo_data=geoCode($address);
                //$geo_data=geoCode($more_info);
                
                //$pet_data["Cat"]=$cat_ext;
                if (array_key_exists('lat', $geo_data)) {
                    $pet_data["Lat"]=$geo_data["lat"];
                    $pet_data["Lng"]=$geo_data["lng"];
                    $pet_data["Direccion_geo"]=$geo_data["formatted_address"];
    
                    createReport($pet_data);
                    //scraperwiki::save(array('Codigo'), $pet_data);
    
                }
    
              
                }
        }
        

    }


    function createReport($petdata)
    {
        /*
        $lat = $petdata["Lat"];
        $lon = $petdata["Lng"];
        $latlon = $lat.','.$lon;

        // Create Location
        $location = new Location_Model();
        $location->location_name = $petdata["Direccion"];
        $location->latitude = $lat;
        $location->longitude = $lon;
        $location->location_date = $petdata["Ingresada"];
        $location->save();                

        // Create Report
        $incident = new Incident_Model();
        $incident->location_id = $location->id;
        $incident->form_id = 1;
        $incident->user_id = $_SESSION['auth_user']->id;
        $incident->incident_title = $petdata["Titulo"];
        $incident->incident_description = $petdata["Mas_info"];
        $incident->incident_date = $petdata["Ingresada"];
        $incident->incident_dateadd = date("Y-m-d H:i:s", time());
        $incident->incident_active = 1;
        $incident->incident_verified = 0;
        //Save
        $incident->save();
        // Set Category (only setting one category per report)
        $incident_category = new Incident_Category_Model();
        $incident_category->incident_id = $incident->id;
        $incident_category->category_id = $petdata["Cat"];
        $incident_category->save();

        */
                $name = $petdata["Titulo"];
        $lname = $petdata["Direccion"];
        $latitude = $petdata["Lat"];
        $longitude = $petdata["Lng"];
        $description = $petdata["Mas_info"];
        $incidentdate = $petdata["Ingresada"];
        $incidenthour = 0;
        $incidentmin = 0;
        $incidentam = date("a");
        $category = $petdata["Cat"];

        $posturl = "http://www.buscadormascotas.com.ar/bm/"; //YOUR USHAHIDI URL HERE
        $Curl_Session = curl_init($posturl);
        curl_setopt ($Curl_Session, CURLOPT_POST, 1);
        
        $post_data="task=report&incident_title=$name&incident_description=$description&incident_date=$incidentdate&incident_hour=$incidenthour";
        $post_data.="&incident_minute=$incidentmin&incident_ampm=$incidentam&incident_category=$category&latitude=$latitude&longitude=$longitude&location_name=$lname";

        curl_setopt ($Curl_Session, CURLOPT_POSTFIELDS,$post_data );
        //You may need to edit this line with the correct variable names

        curl_setopt ($Curl_Session, CURLOPT_FOLLOWLOCATION, 1);
        curl_exec ($Curl_Session);
        curl_close ($Curl_Session);


    }

/**
* finds substrings between opening and closing markers
* @return result array of the substrings
*/
function returnSubstrings($text, $openingMarker, $closingMarker) {
    $openingMarkerLength = strlen($openingMarker);
    $closingMarkerLength = strlen($closingMarker);
    
    $result = array();
    $position = 0;
    while (($position = strpos($text, $openingMarker, $position)) !== false) {
    $position += $openingMarkerLength;
    if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {
    $result[] = substr($text, $position, $closingMarkerPosition - $position);
    $position = $closingMarkerPosition + $closingMarkerLength;
    }
    }
    return $result;
}

function scrapeDH(){
    $max=0;
    for ($index=0; $index<=$max; $index+=20) {
        $url="http://www.derechoanimal.com.ar/dejandohuellas/Result-Cla.asp?letra=1&pag=".$index;
        $html_content = scraperWiki::scrape($url);
        $html = str_get_html($html_content);
        $pets_data = array();
        foreach ($html->find("td.interior") as $html_el) {
            $pet_data = array();
            $tags = explode("&nbsp;",$html_el->plaintext);
            if (sizeof($tags)>1) {
                $code = "DH-PER".utf8_encode(trim($tags[0]));
                $code = str_replace('(','',$code);
                $code = str_replace(')','',$code);
                $pet_data["Codigo"]=utf8_encode(trim($code));
                $pet_data["Provincia"]="Rio Negro";
                $pet_data["Localidad"]="San Carlos De Bariloche";
                $pet_data["Direccion"]=$geo_data["formatted_address"];
                $pet_data["Ingresada"]=date_create_from_format('d/m/Y H:i:s', trim($tags[1]));  
                $pet_data["Mas_info"]=utf8_encode(trim($tags[2]));
                $pet_data["URL"]=utf8_encode($url);
                $geo_data=geoCode($pet_data["Localidad"].", ".$pet_data["Provincia"]);
                $pet_data["Lat"]=$geo_data["lat"];
                $pet_data["Lng"]=$geo_data["lng"];
                scraperwiki::save(array('Codigo'), $pet_data);
            }
         }
    }
}

function scrapeRM(){
    $max=90;
    for ($index=0; $index<$max; $index+=30) {
        $url="http://www.redmascotera.com/see_pet.php?ini=".$index."&bu_pais=1";
        $html_content = scraperWiki::scrape($url);
        $html = str_get_html($html_content);
        $pets_data = array();
        foreach ($html->find("div.cont_m") as $html_el) {
            $pet_data = array();
            $code = $html_el->find("h3 strong",0)->plaintext;
            $title = $html_el->find("h3",0)->plaintext;
            $title = str_replace($code,'',$title);
            $pet_data["Codigo"]=utf8_encode(trim($code));
            $pet_data["Titulo"]=utf8_encode(trim($title));
            $link = $html_el->find("a",0)->href;
            $detail_url="http://www.redmascotera.com/" . $link;
            $detail_content = scraperWiki::scrape($detail_url);
            $detail = str_get_html($detail_content);
            $pet_info = $detail->find("div.bkg_presentacion",0);
            foreach ($pet_info->find("h5") as $pet_el) {
                $tags = explode(":",$pet_el->plaintext);
                $key = utf8_encode(trim($tags[0]));
                $value = utf8_encode(trim($tags[1]));
                if($key=="Ingresada") $value = date_create_from_format('d/m/Y', $value);
                if($key=="Provincia" && $value=="Capital y GBA") $value="Buenos Aires";
                $pet_data[$key]=$value;
            }
            foreach ($pet_info->find("p") as $contact_el) {
                $tags = explode(":",$contact_el->plaintext);
                $key = utf8_encode(trim($tags[0]));
                $value = utf8_encode(trim($tags[1]));
                $pet_data[$key]=$value;
            }    
            $pet_extra = $detail->find("div.bkg_presentacion",1);
            $more_info = $pet_extra->find("p",0)->plaintext;
            $pet_data["Mas_info"]=utf8_encode(trim($more_info));
            $pet_data["URL"]=utf8_encode($detail_url);
            $geo_data=geoCode($pet_data["Calle"].", ".$pet_data["Barrio"].", ".$pet_data["Localidad"].", ".$pet_data["Provincia"].", Argentina");
            $pet_data["Lat"]=$geo_data["lat"];
            $pet_data["Lng"]=$geo_data["lng"];
            $pet_data["Direccion"]=$geo_data["formatted_address"];
    
            scraperwiki::save(array('Codigo'), $pet_data);
            $pets_data[] = $pet_data;
            $img = $html_el->find("img",0)->src;
            $p = $html_el->find("p",0);
            #print $title . " - " .$code . " - " .$link . " - " .$img. " - " .$p."\n";
        }
    }
}

function geoCode($address) {
return geoCodeYp($address);
}

function geoCodeGM($address) {
    $region = 'ar';
    $language = 'es';
    $out = array();
    $url = "http://maps.googleapis.com/maps/api/geocode/json?region={$region}&language={$language}&sensor=false&address=" . urlencode($address);
    $geocoded = json_decode(scraperwiki::scrape($url));
    print_r($geocoded);
    if ($geocoded->status == 'OK') {
        foreach ($geocoded->results[0]->address_components as $component) {
            $out[$component->types[0] . '-long_name'] = $component->long_name;
            $out[$component->types[0] . '-short_name'] = $component->short_name;
        }
        $out['lat'] = $geocoded->results[0]->geometry->location->lat;
        $out['lng'] = $geocoded->results[0]->geometry->location->lng;
        $out['formatted_address'] = $geocoded->results[0]->formatted_address;
    }
    return $out;
}

// Json encode the data
 
function json_code ($json)
{
$json = substr($json, strpos($json,'{')+1, strlen($json));
$json = substr($json, 0, strrpos($json,'}'));
$json=preg_replace('/(^|,)([\\s\\t]*)([^:]*) (([\\s\\t]*)):(([\\s\\t]*))/s','$1"$3"$4:',trim($json));
return json_decode('{'.$json.'}', true);
}
  
// function to get the geocode of the address
 
function geoCodeYp($point)
{
// Replace your Yahoo AppID here
$yahoo_appid = '_18CdmHV34HjeW_rXezIti6jhypsfSqMmAlFFGIOPWC1DW3p0CXYU9eaoL.COp0-';           
 
//URLEncode for eg convert space to %20 .
$pointenc = urlencode($point);
 
// URL Formation that will fetch you the results on query
$url="http://where.yahooapis.com/geocode?location=".$pointenc."&gflags=R&appid=".$yahoo_appid."&flags=J";
 
// get the contents of the URL formed
$jsondata = file_get_contents($url);
 
$json_data= '{
  a: 1,
  b: 245,
  c with whitespaces: "test me",
  d: "function () { echo \"test\" }",
  e: 5.66
  }';
  
 
 $coord=explode(" ",$point);
  
        // this will json encode the data .
  $convertedtoarray=json_code($jsondata);
   
  // line1 of addrress comprising of house,street no etc
        // line 2 of address comprising of city state country
  $line1 =$convertedtoarray['ResultSet']['Results']['0']['line1'] ;
        $line2 =$convertedtoarray['ResultSet']['Results']['0']['line1'] ;
  
        $county =$convertedtoarray['ResultSet']['Results']['0']['county'] ;
        $street =$convertedtoarray['ResultSet']['Results']['0']['street'] ;
   
   
if(($line1=="")||($line2=="")||($county=="")||($street==""))
{
   $yahooresults['status']="noresult";
}
 
else
{
      $countrycode=$convertedtoarray['ResultSet']['Results']['0']['countrycode'] ;
      $statecode=$convertedtoarray['ResultSet']['Results']['0']['statecode']   ;
      $city=$convertedtoarray['ResultSet']['Results']['0']['city'] ;
      $house=$convertedtoarray['ResultSet']['Results']['0']['house'] ;
      $latitude=$convertedtoarray['ResultSet']['Results']['0']['latitude'] ;
      $longitude=$convertedtoarray['ResultSet']['Results']['0']['longitude'] ;    
  
$yahooresults = array('countrycode'=>$countrycode,'statecode'=>$statecode,'county'=>$county,'city'=>$city,'street'=>$street,'house'=>$house,'lat'=>$latitude,'lng'=>$longitude, 'formatted_address'=>$line1.' '.$line2);   
}
   
 return $yahooresults ;
}
 
?>