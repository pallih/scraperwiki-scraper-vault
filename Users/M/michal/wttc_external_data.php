<?php

//delete
/*scraperwiki::sqliteexecute("DELETE FROM swdata WHERE last_name=first_name");
scraperwiki::sqlitecommit(); 
die();*/

//master file contains all the information about the files with external addresses
$master_url = "https://spreadsheets.google.com/a/g.kohovolit.eu/spreadsheet/pub?hl=en_US&hl=en_US&key=0ApmBqWaAzMn_dHJlNjN2WWpaLVVXc005N2E0bTdVeXc&output=csv&dummy=4";
$master_html = grabber($master_url);

//parse master csv
$master = parse_csv($master_html);
//get the last name/town scraped
scraperwiki::save_var('run_first',0); //temp!!
$run_first = scraperwiki::get_var('run_first',0);
//for each parliament/town
foreach ((array) $master as $key => $row) {
  if ($key >= $run_first) {
    $url = $row['link'];
    $html = grabber($url);
    $town = parse_csv($html);
    //add info about parliament, disambiguation
    foreach ((array) $town as $t_key => $t) {
      $town[$t_key]['parliament_code'] = $row['parliament_code'];
      $town[$t_key]['parliament_name'] = $row['parliament_name'];
      $town[$t_key]['term_name'] = $row['term'];
      if (!isset($town[$t_key]['disambiguation'])) $town[$t_key]['disambiguation'] = '';
    }
    $towns[] = $town;
    scraperwiki::save_var('run_first',$key);
  }
}

//save data
foreach ((array) $towns as $town) {
  $i = 1;
  $rows = array();
  foreach((array) $town as $row) {
   $row['source_code'] = str_replace('/','_',$row['parliament_code']) . '_' . str_replace(' ','',$row['term_name']) . '_' . $i;
   //print_r($row);//die();
   $rows[] = $row;
    $i++;
  }
  scraperwiki::save_sqlite(array('parliament_code','last_name','first_name','disambiguation'), $rows);
}
//print_r($towns);


//print('::'.$master_html."::");
scraperwiki::save_var('run_first',0);

/**
* parse csv file
* the first row is considered a header!
* spaces in header's names are replaced by '_'
* http://php.net/manual/en/function.str-getcsv.php (Rob 07-Nov-2008 04:54) + prev. note
* we cannot use str_getscv(), because of a problem with locale settings en_US / utf-8
* @param file csv string
* @param options options
* @return array(row => array(header1 => item1 ... 
*/

function parse_csv($file, $options = null) {
    $delimiter = empty($options['delimiter']) ? "," : $options['delimiter'];
    $to_object = empty($options['to_object']) ? false : true;
    $expr="/$delimiter(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))/"; // added
    $str = $file;
    $lines = explode("\n", $str);
    $field_names = explode($delimiter, array_shift($lines));
    foreach ($lines as $line) {
        // Skip the empty line
        if (empty($line)) continue;
        $fields = preg_split($expr,trim($line)); // added
        $fields = preg_replace("/^\"(.*)\"$/s","$1",$fields); //added
        $fields = preg_replace('/""/','"',$fields); //added ms
        //$fields = explode($delimiter, $line);
        $_res = $to_object ? new stdClass : array();
        foreach ($field_names as $key => $f) {
            $f = trim($f);
            if ($to_object) {
                $_res->{$f} = $fields[$key];
            } else {
                $_res[str_replace(' ','_',$f)] = $fields[$key];
            }
        }
        $res[] = $_res;
    }
    return $res;
} 

/**
* curl downloader, with possible options
* @return html
* example:
* grabber('http://example.com',array(CURLOPT_TIMEOUT,180));
*/
function grabber($url,$options = array())
{
    $ch = curl_init ();
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_URL, $url);
    curl_setopt ($ch, CURLOPT_TIMEOUT, 120);
    if (count($options) > 0) {
      foreach($options as $option) {
        curl_setopt ($ch, $option[0], $option[1]);
      }
    }
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_HEADER, 0); //this option is important here!!
    $out = curl_exec($ch);
    curl_close ($ch);
    return $out;
}
?>
<?php

//delete
/*scraperwiki::sqliteexecute("DELETE FROM swdata WHERE last_name=first_name");
scraperwiki::sqlitecommit(); 
die();*/

//master file contains all the information about the files with external addresses
$master_url = "https://spreadsheets.google.com/a/g.kohovolit.eu/spreadsheet/pub?hl=en_US&hl=en_US&key=0ApmBqWaAzMn_dHJlNjN2WWpaLVVXc005N2E0bTdVeXc&output=csv&dummy=4";
$master_html = grabber($master_url);

//parse master csv
$master = parse_csv($master_html);
//get the last name/town scraped
scraperwiki::save_var('run_first',0); //temp!!
$run_first = scraperwiki::get_var('run_first',0);
//for each parliament/town
foreach ((array) $master as $key => $row) {
  if ($key >= $run_first) {
    $url = $row['link'];
    $html = grabber($url);
    $town = parse_csv($html);
    //add info about parliament, disambiguation
    foreach ((array) $town as $t_key => $t) {
      $town[$t_key]['parliament_code'] = $row['parliament_code'];
      $town[$t_key]['parliament_name'] = $row['parliament_name'];
      $town[$t_key]['term_name'] = $row['term'];
      if (!isset($town[$t_key]['disambiguation'])) $town[$t_key]['disambiguation'] = '';
    }
    $towns[] = $town;
    scraperwiki::save_var('run_first',$key);
  }
}

//save data
foreach ((array) $towns as $town) {
  $i = 1;
  $rows = array();
  foreach((array) $town as $row) {
   $row['source_code'] = str_replace('/','_',$row['parliament_code']) . '_' . str_replace(' ','',$row['term_name']) . '_' . $i;
   //print_r($row);//die();
   $rows[] = $row;
    $i++;
  }
  scraperwiki::save_sqlite(array('parliament_code','last_name','first_name','disambiguation'), $rows);
}
//print_r($towns);


//print('::'.$master_html."::");
scraperwiki::save_var('run_first',0);

/**
* parse csv file
* the first row is considered a header!
* spaces in header's names are replaced by '_'
* http://php.net/manual/en/function.str-getcsv.php (Rob 07-Nov-2008 04:54) + prev. note
* we cannot use str_getscv(), because of a problem with locale settings en_US / utf-8
* @param file csv string
* @param options options
* @return array(row => array(header1 => item1 ... 
*/

function parse_csv($file, $options = null) {
    $delimiter = empty($options['delimiter']) ? "," : $options['delimiter'];
    $to_object = empty($options['to_object']) ? false : true;
    $expr="/$delimiter(?=(?:[^\"]*\"[^\"]*\")*(?![^\"]*\"))/"; // added
    $str = $file;
    $lines = explode("\n", $str);
    $field_names = explode($delimiter, array_shift($lines));
    foreach ($lines as $line) {
        // Skip the empty line
        if (empty($line)) continue;
        $fields = preg_split($expr,trim($line)); // added
        $fields = preg_replace("/^\"(.*)\"$/s","$1",$fields); //added
        $fields = preg_replace('/""/','"',$fields); //added ms
        //$fields = explode($delimiter, $line);
        $_res = $to_object ? new stdClass : array();
        foreach ($field_names as $key => $f) {
            $f = trim($f);
            if ($to_object) {
                $_res->{$f} = $fields[$key];
            } else {
                $_res[str_replace(' ','_',$f)] = $fields[$key];
            }
        }
        $res[] = $_res;
    }
    return $res;
} 

/**
* curl downloader, with possible options
* @return html
* example:
* grabber('http://example.com',array(CURLOPT_TIMEOUT,180));
*/
function grabber($url,$options = array())
{
    $ch = curl_init ();
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_URL, $url);
    curl_setopt ($ch, CURLOPT_TIMEOUT, 120);
    if (count($options) > 0) {
      foreach($options as $option) {
        curl_setopt ($ch, $option[0], $option[1]);
      }
    }
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 1);
    curl_setopt($ch, CURLOPT_HEADER, 0); //this option is important here!!
    $out = curl_exec($ch);
    curl_close ($ch);
    return $out;
}
?>
