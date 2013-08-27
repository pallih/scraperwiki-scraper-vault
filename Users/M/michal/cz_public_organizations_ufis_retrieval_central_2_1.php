<?php

//read the last retrieved values
//scraperwiki::save_var('last_i',0); die(); //temp
$i = scraperwiki::get_var('last_i',0);
echo $i;
//read the saved tables
scraperwiki::attach("cz_public_organizations_ufis_ids", "src0");
$forms = scraperwiki::select("* from src0.form where period='12/2012' and form=50 and chapter is not null order by dri ASC,form DESC,period DESC,org_id ASC");
//echo count($forms);print_r($forms[0]);die();
scraperwiki::attach("cz_public_organizations_ufis_downloader", "src");
//print_r(count($forms));
foreach($forms as $k => $form) {
  //if ($k < $i) continue; 
  if ($form['form'] != 50) continue;

  $rows = scraperwiki::select("* from src.swdata where dri={$form['dri']} and period='{$form['period']}' and org_id='{$form['org_id']}' and form={$form['form']}");
  $row = $rows[0];

  $xml_str = $row['xml'];
//echo $xml_str;die();
  $report_number = $row['form'];
  $org_id = $row['org_id'];
  $period = $row['period'];
  $tmp = explode('/',$period);
  if ($tmp[0] == '12') $year = $tmp[1];
  else $year = $tmp[1].'-'.$tmp[0].'-30';
 //Creating Instance of the Class
    $xmlObj    = new XmlToArray($xml_str);
    //Creating Array
    $arrayData = $xmlObj->createArray();
    //array
    //print_r($arrayData);die();
    $info = array(
      'org_id' => ltrim($org_id,'0'),
      'report_id' => $report_number,
      'period' => $period,
      'year' => $year,
    );
//print_r($info);die();
    $data = ufis2data($arrayData,$info,$report_number);
    foreach ($data as $data_part) {
        switch ($form['form']) {
          case '50':
          case '40':
//print_r($data_part);die();
            scraperwiki::save_sqlite(array('report_id','org_id','year','paragraph_id','entry_id','column_code'),$data_part);
          break;
            /*foreach ($data_part as $key => $data_row) {
              $d = $data_row;
              $d['org_id'] = ltrim($org_id,'0');
              if ($form['form'] != 50)
                  $d['account_id'] = $key;
              $d['report_id'] = $report_number;
              $d['period'] = $period;
              $d['year'] = $year;
              scraperwiki::save_sqlite(array('report_id','account_id','org_id','year','paragraph_id','entry_id','column_code'),$d);*/
            
          default:
            break;
        }
    }
//die();
  $i++;
  scraperwiki::save_var('last_i',$i);

}
scraperwiki::save_var('last_i',0);


/**
* extract real ufis data from array
*/
function ufis2data ($arrayData, $info, $report_number = 50) {
  $part_form = $arrayData['ufis:Vykaz']['ufis:CastFormulare'];
  $out = array();

  switch ($report_number){
    case 40: // report_number = 40 or 50
    case 50:
      foreach ((array) $part_form as $pf) {
        switch ($pf['ufis:CastFormulareID'][0]['ufis:CastFormulareNazev']) {
          case 'I. Rozpočtové příjmy':
            $out[] = ufis2data_fce($pf,$info,$report_number,'Prijmy');
            break;
          case 'II. Rozpočtové výdaje':
          case 'II. Rozpočtové výdaje a financování':
            $out[] = ufis2data_fce($pf,$info,$report_number,'Vydaje');
            break;
        }
      }
      break;
      //balance, profit and loss
    case 60:
    case 65:
    case 1:
    case 2:
    //case 3:
    //case 4:
    //case 61:
    //case 67:
//print_r(count($part_form));
      foreach ((array) $part_form as $pf) {
        $out_ar[] = ufis2data_fce($pf,$info,$report_number);
      }
      foreach ((array) $out_ar as $oa) {
        foreach ((array)$oa as $key => $row) {
          $out[$key] = $row;
        }
      }
    break;  
  }
  //echo 'xx'; print_r($out_ar);die();
  return $out;
}
/**
* helper for extracting ufis data from array
*/
function ufis2data_fce ($pf,$info,$report_number,$str = '') {
  $data = array();
  $k = 0;
  if (($report_number == 40) or ($report_number == 50)) {
    $ufis_2 = 'ufis:ParagrafRozpoctoveSkladby';
    $ufis_3 = 'ufis:PolozkaRozpoctoveSkladby';
    $ufis_4 = 'ufis:ParagrafRozpoctoveSkladbyKod';
    $ufis_5 = 'ufis:PolozkaRozpoctoveSkladbyKod';
    $column = array(
      1 => 'approved_budget',
      2 => 'adjusted_budget',
      3 => 'final_budget',
      4 => 'result',
    );
    if ($str == 'Prijmy') {
      $ufis_1 = 'ufis:BunkaFormulareIDPrijmyX40';
    }
    if ($str == 'Vydaje') {
      $ufis_1 = 'ufis:BunkaFormulareIDVydajeX40';
    }
  
    foreach ((array) $pf['ufis:BunkaFormulare'] as $pfb) {
      $data[$k]['paragraph_id'] = my_coalesce($pfb['ufis:BunkaFormulareID'][0][$ufis_1][0][$ufis_2][0][$ufis_4]);
        $data[$k]['entry_id'] = my_coalesce($pfb['ufis:BunkaFormulareID'][0][$ufis_1][0][$ufis_3][0][$ufis_5]);

        $data[$k]['column_code'] = $column[$pfb['ufis:BunkaFormulareID'][0][$ufis_1][0]['ufis:SloupecFormulareCislo']];

        $data[$k]['_value'] = my_coalesce($pfb['ufis:HodnotaUkazatele']);
        $data[$k]['report_id'] = $info['report_id'];
        $data[$k]['org_id'] = $info['org_id'];
        $data[$k]['year'] = $info['year'];
        $data[$k]['period'] = $info['period'];
        $k++;
    }
    
  } else { //report number is not 40/50
    //echo 'ff' . count($pf['ufis:BunkaFormulare']) . 'ff';die();
    foreach ((array) $pf['ufis:BunkaFormulare'] as $pfb) {
      $description = str_replace(chr(32),' ',my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:RadekFormulareNazev']));
      $description = preg_replace('!\s+!', ' ', $description);
      /*foreach ((array) str_split($description) as $d) {
        echo "::".$d."::".ord($d)."<br/>";
      }*/
      //echo $description ."<br/>";
      if (is_raw_row($description)) {
        //which value (beggining or end of the year)
        //echo $pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:RadekFormulareNazev'] . "<br/>";
        //echo my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']);
        //balance -2009
        if (($report_number == 60) or ($report_number == 65)) {
            if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'1.') > 0) {
              $col_val = 'value_1_1';
            } else {
              $col_val = '_value';
            }
            $account_id = get_account($description);
        }
        //balance 2010-
        if ($report_number == 1) {
            if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'Brutto') > 0)
              $col_val = 'value_brutto';
            else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'Korekce') > 0)
              $col_val = 'value_correction'; 
            else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'inulé') > 0)
              $col_val = 'previous_value_netto';
            else
              $col_val = 'value_netto';
            $tmp_ar = explode(' ',$description);
            $account_id = end($tmp_ar);
            $tmp_ar2 = explode('.',$tmp_ar[0]);
            $data[$account_id]['entry_number_1'] = $tmp_ar2[0];
            $data[$account_id]['entry_number_2'] = $tmp_ar2[1];
            $data[$account_id]['entry_number_3'] = $tmp_ar2[2];
        }
        //profit and loss
        if (($report_number == 61) or ($report_number == 67)) {
            if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'SPODÁŘSKÁ') > 0) {
              $col_val = 'value_economic';
            } else {
              $col_val = 'value_main';
            }
            $account_id = get_account($description);
        }
        if ($report_number == 2) {
          if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'ěžné období-Hospodářská') > 0)
              $col_val = 'value_economic';
          else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'ěžné období-Hlavní') > 0)
              $col_val = 'value_main';
          else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'inulé období-Hlavní') > 0)
              $col_val = 'previous_value_main';
          else 
              $col_val = 'previous_value_economic';
        }
        
        $data[$account_id][$col_val] = my_coalesce($pfb['ufis:HodnotaUkazatele']);
        $data[$account_id]['description'] = $description;    
        //echo '::'.$account_id . '::' . $col_val . '::<br/>';
      } //else echo "**" . $description . "<br/>";
    }
  }
  return $data;
}

/*
* get account number from description
* example: '1. NEHMOTNÝ INVEST.MAJETEK-JINÝ NEHMOTNÝ INVESTIČNÍ MAJETEK  /018+019/'
*    return: 018
*/
function get_account($str) {
   $tmp = get_first_string($str,'/','/');
   preg_match('/([0-9]{3})/',$tmp,$match);
   return $match[1];
}

/**
* find if is a row with raw data or sum of other rows
*/
function is_raw_row($str) {
  if (strpos($str,'/') > 0)  //includes number in / /, e.g. '.../123/'
    {  
      $tmp = get_first_string($str,'/','/');
      if ((is_numeric(get_account($str))) AND ((strpos($tmp,'Ř.') === false) OR (!(strpos($tmp,'MIMO') === false)))
         )
        return true;
      else
        return false;
    }
  else {
    $tmp_ar = explode(' ',$str);
    $tmp = end($tmp_ar);
    if (is_numeric($tmp))
        return true;
      else
        return false;
  }
}


/**
* XMLToArray Generator Class
* @author  :  MA Razzaque Rupom <rupom_315@yahoo.com>, <rupom.bd@gmail.com>
*             Moderator, phpResource (LINK1http://groups.yahoo.com/group/phpresource/LINK1)
*             URL: LINK2http://www.rupom.infoLINK2
* @version :  1.0
* @date       06/05/2006
* Purpose  : Creating Hierarchical Array from XML Data
* Released : Under GPL
*/

class XmlToArray
{
   
    var $xml='';
   
    /**
    * Default Constructor
    * @param $xml = xml data
    * @return none
    */
   
    function XmlToArray($xml)
    {
       $this->xml = $xml;   
    }
   
    /**
    * _struct_to_array($values, &$i)
    *
    * This is adds the contents of the return xml into the array for easier processing.
    * Recursive, Static
    *
    * @access    private
    * @param    array  $values this is the xml data in an array
    * @param    int    $i  this is the current location in the array
    * @return    Array
    */
   
    function _struct_to_array($values, &$i)
    {
        $child = array();
        if (isset($values[$i]['value'])) array_push($child, $values[$i]['value']);
       
        while ($i++ < count($values)) {
            switch ($values[$i]['type']) {
                case 'cdata':
                array_push($child, $values[$i]['value']);
                break;
               
                case 'complete':
                    $name = $values[$i]['tag'];
                    if(!empty($name)){
                    $child[$name]= (isset($values[$i]['value'])?(($values[$i]['value'])?($values[$i]['value']):''):'');
                    if(isset($values[$i]['attributes'])) {                   
                        $child[$name] = $values[$i]['attributes'];
                    }
                }   
              break;
               
                case 'open':
                    $name = $values[$i]['tag'];
                    $size = isset($child[$name]) ? sizeof($child[$name]) : 0;
                    $child[$name][$size] = $this->_struct_to_array($values, $i);
                break;
               
                case 'close':
                return $child;
                break;
            }
        }
        return $child;
    }//_struct_to_array
   
    /**
    * createArray($data)
    *
    * This is adds the contents of the return xml into the array for easier processing.
    *
    * @access    public
    * @param    string    $data this is the string of the xml data
    * @return    Array
    */
    function createArray()
    {
        $xml    = $this->xml;
        $values = array();
        $index  = array();
        $array  = array();
        $parser = xml_parser_create();
        xml_parser_set_option($parser, XML_OPTION_SKIP_WHITE, 1);
        xml_parser_set_option($parser, XML_OPTION_CASE_FOLDING, 0);
        xml_parse_into_struct($parser, $xml, $values, $index);
        xml_parser_free($parser);
        $i = 0;
        $name = $values[$i]['tag'];
        $array[$name] = isset($values[$i]['attributes']) ? $values[$i]['attributes'] : '';
        $array[$name] = $this->_struct_to_array($values, $i);
        return $array;
    }//createArray
   
   
}//XmlToArray
/**
* Create  connection to the legacy database
* @return connection
*/
function  create_connection() {
    include  'database_credentials.php';//include the database credentials; necessary  to use     'include' and not 'include_once' so that multiple queries  can be made from the same web page.
    
// Connect to  pgsql
  $connection = pg_connect("host={$host}  port={$port} dbname={$dbname} user={$user} password={$password}");
  return  $connection;
} // end modulename_create_connection()

/**
* Perform database queries.
* @return result  Database query result
*/
function  exec_sql($query_string,$params = array(),$schema = 'ufis') {
  // Create  connection
  $connection = create_connection();
  if  (!$connection){
    return false;
  } else {
    // Perform  DB Query
    pg_query_params("SET search_path='{$schema}';",array());
    pg_query_params("SET client_encoding TO 'UTF-8';",array());
    $result = pg_fetch_all(pg_query_params($query_string,$params));   
    //pg_close  ($connection);
    return $result;
  }
} // end  modulename_perform_query()

/**
* "coalesce" - returns another value if input is NULL or ''
*/
function my_coalesce($in, $new = 0) {
  if (($in === NULL) or ($in == '')) {
    $out = $new;
  } else {
    $out = $in;
  }
  return $out;
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


/**
* finds 1st substring between opening and closing markers
* @return result 1st substring
*/
function get_first_string ($text,$openingMarker, $closingMarker) {
$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);
$out = $out_ar[0];
return($out);
}

?><?php

//read the last retrieved values
//scraperwiki::save_var('last_i',0); die(); //temp
$i = scraperwiki::get_var('last_i',0);
echo $i;
//read the saved tables
scraperwiki::attach("cz_public_organizations_ufis_ids", "src0");
$forms = scraperwiki::select("* from src0.form where period='12/2012' and form=50 and chapter is not null order by dri ASC,form DESC,period DESC,org_id ASC");
//echo count($forms);print_r($forms[0]);die();
scraperwiki::attach("cz_public_organizations_ufis_downloader", "src");
//print_r(count($forms));
foreach($forms as $k => $form) {
  //if ($k < $i) continue; 
  if ($form['form'] != 50) continue;

  $rows = scraperwiki::select("* from src.swdata where dri={$form['dri']} and period='{$form['period']}' and org_id='{$form['org_id']}' and form={$form['form']}");
  $row = $rows[0];

  $xml_str = $row['xml'];
//echo $xml_str;die();
  $report_number = $row['form'];
  $org_id = $row['org_id'];
  $period = $row['period'];
  $tmp = explode('/',$period);
  if ($tmp[0] == '12') $year = $tmp[1];
  else $year = $tmp[1].'-'.$tmp[0].'-30';
 //Creating Instance of the Class
    $xmlObj    = new XmlToArray($xml_str);
    //Creating Array
    $arrayData = $xmlObj->createArray();
    //array
    //print_r($arrayData);die();
    $info = array(
      'org_id' => ltrim($org_id,'0'),
      'report_id' => $report_number,
      'period' => $period,
      'year' => $year,
    );
//print_r($info);die();
    $data = ufis2data($arrayData,$info,$report_number);
    foreach ($data as $data_part) {
        switch ($form['form']) {
          case '50':
          case '40':
//print_r($data_part);die();
            scraperwiki::save_sqlite(array('report_id','org_id','year','paragraph_id','entry_id','column_code'),$data_part);
          break;
            /*foreach ($data_part as $key => $data_row) {
              $d = $data_row;
              $d['org_id'] = ltrim($org_id,'0');
              if ($form['form'] != 50)
                  $d['account_id'] = $key;
              $d['report_id'] = $report_number;
              $d['period'] = $period;
              $d['year'] = $year;
              scraperwiki::save_sqlite(array('report_id','account_id','org_id','year','paragraph_id','entry_id','column_code'),$d);*/
            
          default:
            break;
        }
    }
//die();
  $i++;
  scraperwiki::save_var('last_i',$i);

}
scraperwiki::save_var('last_i',0);


/**
* extract real ufis data from array
*/
function ufis2data ($arrayData, $info, $report_number = 50) {
  $part_form = $arrayData['ufis:Vykaz']['ufis:CastFormulare'];
  $out = array();

  switch ($report_number){
    case 40: // report_number = 40 or 50
    case 50:
      foreach ((array) $part_form as $pf) {
        switch ($pf['ufis:CastFormulareID'][0]['ufis:CastFormulareNazev']) {
          case 'I. Rozpočtové příjmy':
            $out[] = ufis2data_fce($pf,$info,$report_number,'Prijmy');
            break;
          case 'II. Rozpočtové výdaje':
          case 'II. Rozpočtové výdaje a financování':
            $out[] = ufis2data_fce($pf,$info,$report_number,'Vydaje');
            break;
        }
      }
      break;
      //balance, profit and loss
    case 60:
    case 65:
    case 1:
    case 2:
    //case 3:
    //case 4:
    //case 61:
    //case 67:
//print_r(count($part_form));
      foreach ((array) $part_form as $pf) {
        $out_ar[] = ufis2data_fce($pf,$info,$report_number);
      }
      foreach ((array) $out_ar as $oa) {
        foreach ((array)$oa as $key => $row) {
          $out[$key] = $row;
        }
      }
    break;  
  }
  //echo 'xx'; print_r($out_ar);die();
  return $out;
}
/**
* helper for extracting ufis data from array
*/
function ufis2data_fce ($pf,$info,$report_number,$str = '') {
  $data = array();
  $k = 0;
  if (($report_number == 40) or ($report_number == 50)) {
    $ufis_2 = 'ufis:ParagrafRozpoctoveSkladby';
    $ufis_3 = 'ufis:PolozkaRozpoctoveSkladby';
    $ufis_4 = 'ufis:ParagrafRozpoctoveSkladbyKod';
    $ufis_5 = 'ufis:PolozkaRozpoctoveSkladbyKod';
    $column = array(
      1 => 'approved_budget',
      2 => 'adjusted_budget',
      3 => 'final_budget',
      4 => 'result',
    );
    if ($str == 'Prijmy') {
      $ufis_1 = 'ufis:BunkaFormulareIDPrijmyX40';
    }
    if ($str == 'Vydaje') {
      $ufis_1 = 'ufis:BunkaFormulareIDVydajeX40';
    }
  
    foreach ((array) $pf['ufis:BunkaFormulare'] as $pfb) {
      $data[$k]['paragraph_id'] = my_coalesce($pfb['ufis:BunkaFormulareID'][0][$ufis_1][0][$ufis_2][0][$ufis_4]);
        $data[$k]['entry_id'] = my_coalesce($pfb['ufis:BunkaFormulareID'][0][$ufis_1][0][$ufis_3][0][$ufis_5]);

        $data[$k]['column_code'] = $column[$pfb['ufis:BunkaFormulareID'][0][$ufis_1][0]['ufis:SloupecFormulareCislo']];

        $data[$k]['_value'] = my_coalesce($pfb['ufis:HodnotaUkazatele']);
        $data[$k]['report_id'] = $info['report_id'];
        $data[$k]['org_id'] = $info['org_id'];
        $data[$k]['year'] = $info['year'];
        $data[$k]['period'] = $info['period'];
        $k++;
    }
    
  } else { //report number is not 40/50
    //echo 'ff' . count($pf['ufis:BunkaFormulare']) . 'ff';die();
    foreach ((array) $pf['ufis:BunkaFormulare'] as $pfb) {
      $description = str_replace(chr(32),' ',my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:RadekFormulareNazev']));
      $description = preg_replace('!\s+!', ' ', $description);
      /*foreach ((array) str_split($description) as $d) {
        echo "::".$d."::".ord($d)."<br/>";
      }*/
      //echo $description ."<br/>";
      if (is_raw_row($description)) {
        //which value (beggining or end of the year)
        //echo $pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:RadekFormulareNazev'] . "<br/>";
        //echo my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']);
        //balance -2009
        if (($report_number == 60) or ($report_number == 65)) {
            if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'1.') > 0) {
              $col_val = 'value_1_1';
            } else {
              $col_val = '_value';
            }
            $account_id = get_account($description);
        }
        //balance 2010-
        if ($report_number == 1) {
            if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'Brutto') > 0)
              $col_val = 'value_brutto';
            else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'Korekce') > 0)
              $col_val = 'value_correction'; 
            else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'inulé') > 0)
              $col_val = 'previous_value_netto';
            else
              $col_val = 'value_netto';
            $tmp_ar = explode(' ',$description);
            $account_id = end($tmp_ar);
            $tmp_ar2 = explode('.',$tmp_ar[0]);
            $data[$account_id]['entry_number_1'] = $tmp_ar2[0];
            $data[$account_id]['entry_number_2'] = $tmp_ar2[1];
            $data[$account_id]['entry_number_3'] = $tmp_ar2[2];
        }
        //profit and loss
        if (($report_number == 61) or ($report_number == 67)) {
            if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'SPODÁŘSKÁ') > 0) {
              $col_val = 'value_economic';
            } else {
              $col_val = 'value_main';
            }
            $account_id = get_account($description);
        }
        if ($report_number == 2) {
          if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'ěžné období-Hospodářská') > 0)
              $col_val = 'value_economic';
          else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'ěžné období-Hlavní') > 0)
              $col_val = 'value_main';
          else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'inulé období-Hlavní') > 0)
              $col_val = 'previous_value_main';
          else 
              $col_val = 'previous_value_economic';
        }
        
        $data[$account_id][$col_val] = my_coalesce($pfb['ufis:HodnotaUkazatele']);
        $data[$account_id]['description'] = $description;    
        //echo '::'.$account_id . '::' . $col_val . '::<br/>';
      } //else echo "**" . $description . "<br/>";
    }
  }
  return $data;
}

/*
* get account number from description
* example: '1. NEHMOTNÝ INVEST.MAJETEK-JINÝ NEHMOTNÝ INVESTIČNÍ MAJETEK  /018+019/'
*    return: 018
*/
function get_account($str) {
   $tmp = get_first_string($str,'/','/');
   preg_match('/([0-9]{3})/',$tmp,$match);
   return $match[1];
}

/**
* find if is a row with raw data or sum of other rows
*/
function is_raw_row($str) {
  if (strpos($str,'/') > 0)  //includes number in / /, e.g. '.../123/'
    {  
      $tmp = get_first_string($str,'/','/');
      if ((is_numeric(get_account($str))) AND ((strpos($tmp,'Ř.') === false) OR (!(strpos($tmp,'MIMO') === false)))
         )
        return true;
      else
        return false;
    }
  else {
    $tmp_ar = explode(' ',$str);
    $tmp = end($tmp_ar);
    if (is_numeric($tmp))
        return true;
      else
        return false;
  }
}


/**
* XMLToArray Generator Class
* @author  :  MA Razzaque Rupom <rupom_315@yahoo.com>, <rupom.bd@gmail.com>
*             Moderator, phpResource (LINK1http://groups.yahoo.com/group/phpresource/LINK1)
*             URL: LINK2http://www.rupom.infoLINK2
* @version :  1.0
* @date       06/05/2006
* Purpose  : Creating Hierarchical Array from XML Data
* Released : Under GPL
*/

class XmlToArray
{
   
    var $xml='';
   
    /**
    * Default Constructor
    * @param $xml = xml data
    * @return none
    */
   
    function XmlToArray($xml)
    {
       $this->xml = $xml;   
    }
   
    /**
    * _struct_to_array($values, &$i)
    *
    * This is adds the contents of the return xml into the array for easier processing.
    * Recursive, Static
    *
    * @access    private
    * @param    array  $values this is the xml data in an array
    * @param    int    $i  this is the current location in the array
    * @return    Array
    */
   
    function _struct_to_array($values, &$i)
    {
        $child = array();
        if (isset($values[$i]['value'])) array_push($child, $values[$i]['value']);
       
        while ($i++ < count($values)) {
            switch ($values[$i]['type']) {
                case 'cdata':
                array_push($child, $values[$i]['value']);
                break;
               
                case 'complete':
                    $name = $values[$i]['tag'];
                    if(!empty($name)){
                    $child[$name]= (isset($values[$i]['value'])?(($values[$i]['value'])?($values[$i]['value']):''):'');
                    if(isset($values[$i]['attributes'])) {                   
                        $child[$name] = $values[$i]['attributes'];
                    }
                }   
              break;
               
                case 'open':
                    $name = $values[$i]['tag'];
                    $size = isset($child[$name]) ? sizeof($child[$name]) : 0;
                    $child[$name][$size] = $this->_struct_to_array($values, $i);
                break;
               
                case 'close':
                return $child;
                break;
            }
        }
        return $child;
    }//_struct_to_array
   
    /**
    * createArray($data)
    *
    * This is adds the contents of the return xml into the array for easier processing.
    *
    * @access    public
    * @param    string    $data this is the string of the xml data
    * @return    Array
    */
    function createArray()
    {
        $xml    = $this->xml;
        $values = array();
        $index  = array();
        $array  = array();
        $parser = xml_parser_create();
        xml_parser_set_option($parser, XML_OPTION_SKIP_WHITE, 1);
        xml_parser_set_option($parser, XML_OPTION_CASE_FOLDING, 0);
        xml_parse_into_struct($parser, $xml, $values, $index);
        xml_parser_free($parser);
        $i = 0;
        $name = $values[$i]['tag'];
        $array[$name] = isset($values[$i]['attributes']) ? $values[$i]['attributes'] : '';
        $array[$name] = $this->_struct_to_array($values, $i);
        return $array;
    }//createArray
   
   
}//XmlToArray
/**
* Create  connection to the legacy database
* @return connection
*/
function  create_connection() {
    include  'database_credentials.php';//include the database credentials; necessary  to use     'include' and not 'include_once' so that multiple queries  can be made from the same web page.
    
// Connect to  pgsql
  $connection = pg_connect("host={$host}  port={$port} dbname={$dbname} user={$user} password={$password}");
  return  $connection;
} // end modulename_create_connection()

/**
* Perform database queries.
* @return result  Database query result
*/
function  exec_sql($query_string,$params = array(),$schema = 'ufis') {
  // Create  connection
  $connection = create_connection();
  if  (!$connection){
    return false;
  } else {
    // Perform  DB Query
    pg_query_params("SET search_path='{$schema}';",array());
    pg_query_params("SET client_encoding TO 'UTF-8';",array());
    $result = pg_fetch_all(pg_query_params($query_string,$params));   
    //pg_close  ($connection);
    return $result;
  }
} // end  modulename_perform_query()

/**
* "coalesce" - returns another value if input is NULL or ''
*/
function my_coalesce($in, $new = 0) {
  if (($in === NULL) or ($in == '')) {
    $out = $new;
  } else {
    $out = $in;
  }
  return $out;
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


/**
* finds 1st substring between opening and closing markers
* @return result 1st substring
*/
function get_first_string ($text,$openingMarker, $closingMarker) {
$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);
$out = $out_ar[0];
return($out);
}

?><?php

//read the last retrieved values
//scraperwiki::save_var('last_i',0); die(); //temp
$i = scraperwiki::get_var('last_i',0);
echo $i;
//read the saved tables
scraperwiki::attach("cz_public_organizations_ufis_ids", "src0");
$forms = scraperwiki::select("* from src0.form where period='12/2012' and form=50 and chapter is not null order by dri ASC,form DESC,period DESC,org_id ASC");
//echo count($forms);print_r($forms[0]);die();
scraperwiki::attach("cz_public_organizations_ufis_downloader", "src");
//print_r(count($forms));
foreach($forms as $k => $form) {
  //if ($k < $i) continue; 
  if ($form['form'] != 50) continue;

  $rows = scraperwiki::select("* from src.swdata where dri={$form['dri']} and period='{$form['period']}' and org_id='{$form['org_id']}' and form={$form['form']}");
  $row = $rows[0];

  $xml_str = $row['xml'];
//echo $xml_str;die();
  $report_number = $row['form'];
  $org_id = $row['org_id'];
  $period = $row['period'];
  $tmp = explode('/',$period);
  if ($tmp[0] == '12') $year = $tmp[1];
  else $year = $tmp[1].'-'.$tmp[0].'-30';
 //Creating Instance of the Class
    $xmlObj    = new XmlToArray($xml_str);
    //Creating Array
    $arrayData = $xmlObj->createArray();
    //array
    //print_r($arrayData);die();
    $info = array(
      'org_id' => ltrim($org_id,'0'),
      'report_id' => $report_number,
      'period' => $period,
      'year' => $year,
    );
//print_r($info);die();
    $data = ufis2data($arrayData,$info,$report_number);
    foreach ($data as $data_part) {
        switch ($form['form']) {
          case '50':
          case '40':
//print_r($data_part);die();
            scraperwiki::save_sqlite(array('report_id','org_id','year','paragraph_id','entry_id','column_code'),$data_part);
          break;
            /*foreach ($data_part as $key => $data_row) {
              $d = $data_row;
              $d['org_id'] = ltrim($org_id,'0');
              if ($form['form'] != 50)
                  $d['account_id'] = $key;
              $d['report_id'] = $report_number;
              $d['period'] = $period;
              $d['year'] = $year;
              scraperwiki::save_sqlite(array('report_id','account_id','org_id','year','paragraph_id','entry_id','column_code'),$d);*/
            
          default:
            break;
        }
    }
//die();
  $i++;
  scraperwiki::save_var('last_i',$i);

}
scraperwiki::save_var('last_i',0);


/**
* extract real ufis data from array
*/
function ufis2data ($arrayData, $info, $report_number = 50) {
  $part_form = $arrayData['ufis:Vykaz']['ufis:CastFormulare'];
  $out = array();

  switch ($report_number){
    case 40: // report_number = 40 or 50
    case 50:
      foreach ((array) $part_form as $pf) {
        switch ($pf['ufis:CastFormulareID'][0]['ufis:CastFormulareNazev']) {
          case 'I. Rozpočtové příjmy':
            $out[] = ufis2data_fce($pf,$info,$report_number,'Prijmy');
            break;
          case 'II. Rozpočtové výdaje':
          case 'II. Rozpočtové výdaje a financování':
            $out[] = ufis2data_fce($pf,$info,$report_number,'Vydaje');
            break;
        }
      }
      break;
      //balance, profit and loss
    case 60:
    case 65:
    case 1:
    case 2:
    //case 3:
    //case 4:
    //case 61:
    //case 67:
//print_r(count($part_form));
      foreach ((array) $part_form as $pf) {
        $out_ar[] = ufis2data_fce($pf,$info,$report_number);
      }
      foreach ((array) $out_ar as $oa) {
        foreach ((array)$oa as $key => $row) {
          $out[$key] = $row;
        }
      }
    break;  
  }
  //echo 'xx'; print_r($out_ar);die();
  return $out;
}
/**
* helper for extracting ufis data from array
*/
function ufis2data_fce ($pf,$info,$report_number,$str = '') {
  $data = array();
  $k = 0;
  if (($report_number == 40) or ($report_number == 50)) {
    $ufis_2 = 'ufis:ParagrafRozpoctoveSkladby';
    $ufis_3 = 'ufis:PolozkaRozpoctoveSkladby';
    $ufis_4 = 'ufis:ParagrafRozpoctoveSkladbyKod';
    $ufis_5 = 'ufis:PolozkaRozpoctoveSkladbyKod';
    $column = array(
      1 => 'approved_budget',
      2 => 'adjusted_budget',
      3 => 'final_budget',
      4 => 'result',
    );
    if ($str == 'Prijmy') {
      $ufis_1 = 'ufis:BunkaFormulareIDPrijmyX40';
    }
    if ($str == 'Vydaje') {
      $ufis_1 = 'ufis:BunkaFormulareIDVydajeX40';
    }
  
    foreach ((array) $pf['ufis:BunkaFormulare'] as $pfb) {
      $data[$k]['paragraph_id'] = my_coalesce($pfb['ufis:BunkaFormulareID'][0][$ufis_1][0][$ufis_2][0][$ufis_4]);
        $data[$k]['entry_id'] = my_coalesce($pfb['ufis:BunkaFormulareID'][0][$ufis_1][0][$ufis_3][0][$ufis_5]);

        $data[$k]['column_code'] = $column[$pfb['ufis:BunkaFormulareID'][0][$ufis_1][0]['ufis:SloupecFormulareCislo']];

        $data[$k]['_value'] = my_coalesce($pfb['ufis:HodnotaUkazatele']);
        $data[$k]['report_id'] = $info['report_id'];
        $data[$k]['org_id'] = $info['org_id'];
        $data[$k]['year'] = $info['year'];
        $data[$k]['period'] = $info['period'];
        $k++;
    }
    
  } else { //report number is not 40/50
    //echo 'ff' . count($pf['ufis:BunkaFormulare']) . 'ff';die();
    foreach ((array) $pf['ufis:BunkaFormulare'] as $pfb) {
      $description = str_replace(chr(32),' ',my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:RadekFormulareNazev']));
      $description = preg_replace('!\s+!', ' ', $description);
      /*foreach ((array) str_split($description) as $d) {
        echo "::".$d."::".ord($d)."<br/>";
      }*/
      //echo $description ."<br/>";
      if (is_raw_row($description)) {
        //which value (beggining or end of the year)
        //echo $pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:RadekFormulareNazev'] . "<br/>";
        //echo my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']);
        //balance -2009
        if (($report_number == 60) or ($report_number == 65)) {
            if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'1.') > 0) {
              $col_val = 'value_1_1';
            } else {
              $col_val = '_value';
            }
            $account_id = get_account($description);
        }
        //balance 2010-
        if ($report_number == 1) {
            if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'Brutto') > 0)
              $col_val = 'value_brutto';
            else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'Korekce') > 0)
              $col_val = 'value_correction'; 
            else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'inulé') > 0)
              $col_val = 'previous_value_netto';
            else
              $col_val = 'value_netto';
            $tmp_ar = explode(' ',$description);
            $account_id = end($tmp_ar);
            $tmp_ar2 = explode('.',$tmp_ar[0]);
            $data[$account_id]['entry_number_1'] = $tmp_ar2[0];
            $data[$account_id]['entry_number_2'] = $tmp_ar2[1];
            $data[$account_id]['entry_number_3'] = $tmp_ar2[2];
        }
        //profit and loss
        if (($report_number == 61) or ($report_number == 67)) {
            if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'SPODÁŘSKÁ') > 0) {
              $col_val = 'value_economic';
            } else {
              $col_val = 'value_main';
            }
            $account_id = get_account($description);
        }
        if ($report_number == 2) {
          if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'ěžné období-Hospodářská') > 0)
              $col_val = 'value_economic';
          else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'ěžné období-Hlavní') > 0)
              $col_val = 'value_main';
          else if (strpos(my_coalesce($pfb['ufis:BunkaFormulareID'][0]['ufis:BunkaFormulareIDPevna'][0]['ufis:SloupecFormulareNazev']),'inulé období-Hlavní') > 0)
              $col_val = 'previous_value_main';
          else 
              $col_val = 'previous_value_economic';
        }
        
        $data[$account_id][$col_val] = my_coalesce($pfb['ufis:HodnotaUkazatele']);
        $data[$account_id]['description'] = $description;    
        //echo '::'.$account_id . '::' . $col_val . '::<br/>';
      } //else echo "**" . $description . "<br/>";
    }
  }
  return $data;
}

/*
* get account number from description
* example: '1. NEHMOTNÝ INVEST.MAJETEK-JINÝ NEHMOTNÝ INVESTIČNÍ MAJETEK  /018+019/'
*    return: 018
*/
function get_account($str) {
   $tmp = get_first_string($str,'/','/');
   preg_match('/([0-9]{3})/',$tmp,$match);
   return $match[1];
}

/**
* find if is a row with raw data or sum of other rows
*/
function is_raw_row($str) {
  if (strpos($str,'/') > 0)  //includes number in / /, e.g. '.../123/'
    {  
      $tmp = get_first_string($str,'/','/');
      if ((is_numeric(get_account($str))) AND ((strpos($tmp,'Ř.') === false) OR (!(strpos($tmp,'MIMO') === false)))
         )
        return true;
      else
        return false;
    }
  else {
    $tmp_ar = explode(' ',$str);
    $tmp = end($tmp_ar);
    if (is_numeric($tmp))
        return true;
      else
        return false;
  }
}


/**
* XMLToArray Generator Class
* @author  :  MA Razzaque Rupom <rupom_315@yahoo.com>, <rupom.bd@gmail.com>
*             Moderator, phpResource (LINK1http://groups.yahoo.com/group/phpresource/LINK1)
*             URL: LINK2http://www.rupom.infoLINK2
* @version :  1.0
* @date       06/05/2006
* Purpose  : Creating Hierarchical Array from XML Data
* Released : Under GPL
*/

class XmlToArray
{
   
    var $xml='';
   
    /**
    * Default Constructor
    * @param $xml = xml data
    * @return none
    */
   
    function XmlToArray($xml)
    {
       $this->xml = $xml;   
    }
   
    /**
    * _struct_to_array($values, &$i)
    *
    * This is adds the contents of the return xml into the array for easier processing.
    * Recursive, Static
    *
    * @access    private
    * @param    array  $values this is the xml data in an array
    * @param    int    $i  this is the current location in the array
    * @return    Array
    */
   
    function _struct_to_array($values, &$i)
    {
        $child = array();
        if (isset($values[$i]['value'])) array_push($child, $values[$i]['value']);
       
        while ($i++ < count($values)) {
            switch ($values[$i]['type']) {
                case 'cdata':
                array_push($child, $values[$i]['value']);
                break;
               
                case 'complete':
                    $name = $values[$i]['tag'];
                    if(!empty($name)){
                    $child[$name]= (isset($values[$i]['value'])?(($values[$i]['value'])?($values[$i]['value']):''):'');
                    if(isset($values[$i]['attributes'])) {                   
                        $child[$name] = $values[$i]['attributes'];
                    }
                }   
              break;
               
                case 'open':
                    $name = $values[$i]['tag'];
                    $size = isset($child[$name]) ? sizeof($child[$name]) : 0;
                    $child[$name][$size] = $this->_struct_to_array($values, $i);
                break;
               
                case 'close':
                return $child;
                break;
            }
        }
        return $child;
    }//_struct_to_array
   
    /**
    * createArray($data)
    *
    * This is adds the contents of the return xml into the array for easier processing.
    *
    * @access    public
    * @param    string    $data this is the string of the xml data
    * @return    Array
    */
    function createArray()
    {
        $xml    = $this->xml;
        $values = array();
        $index  = array();
        $array  = array();
        $parser = xml_parser_create();
        xml_parser_set_option($parser, XML_OPTION_SKIP_WHITE, 1);
        xml_parser_set_option($parser, XML_OPTION_CASE_FOLDING, 0);
        xml_parse_into_struct($parser, $xml, $values, $index);
        xml_parser_free($parser);
        $i = 0;
        $name = $values[$i]['tag'];
        $array[$name] = isset($values[$i]['attributes']) ? $values[$i]['attributes'] : '';
        $array[$name] = $this->_struct_to_array($values, $i);
        return $array;
    }//createArray
   
   
}//XmlToArray
/**
* Create  connection to the legacy database
* @return connection
*/
function  create_connection() {
    include  'database_credentials.php';//include the database credentials; necessary  to use     'include' and not 'include_once' so that multiple queries  can be made from the same web page.
    
// Connect to  pgsql
  $connection = pg_connect("host={$host}  port={$port} dbname={$dbname} user={$user} password={$password}");
  return  $connection;
} // end modulename_create_connection()

/**
* Perform database queries.
* @return result  Database query result
*/
function  exec_sql($query_string,$params = array(),$schema = 'ufis') {
  // Create  connection
  $connection = create_connection();
  if  (!$connection){
    return false;
  } else {
    // Perform  DB Query
    pg_query_params("SET search_path='{$schema}';",array());
    pg_query_params("SET client_encoding TO 'UTF-8';",array());
    $result = pg_fetch_all(pg_query_params($query_string,$params));   
    //pg_close  ($connection);
    return $result;
  }
} // end  modulename_perform_query()

/**
* "coalesce" - returns another value if input is NULL or ''
*/
function my_coalesce($in, $new = 0) {
  if (($in === NULL) or ($in == '')) {
    $out = $new;
  } else {
    $out = $in;
  }
  return $out;
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


/**
* finds 1st substring between opening and closing markers
* @return result 1st substring
*/
function get_first_string ($text,$openingMarker, $closingMarker) {
$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);
$out = $out_ar[0];
return($out);
}

?>