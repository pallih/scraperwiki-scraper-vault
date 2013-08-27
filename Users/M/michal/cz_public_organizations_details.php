<?php
//original url: http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/detail.pl?org=2600649
// org= is NOT org_id (IČ) !!
// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php';
//read the data saved from list of org_id
scraperwiki::attach("cz_public_organizations_retrieval", "src");
$data = scraperwiki::select("* from src.swdata");

//sort data
foreach ($data as $key => $row) {
    $x[$key]  = $row['org_id'];
}
array_multisort($x, SORT_ASC, $data);

//last org_id
$last_org_id = scraperwiki::get_var('last_org_id',0);

foreach((array) $data as $data_row) {
  if ($data_row['org_id'] > $last_org_id) {
    //download the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/detail.pl?org=".$data_row['inner_org_id'];
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //clean &nbsp;
    $html = str_replace('&nbsp;',' ',$html);
    //get dom from data
    $dom = new simple_html_dom();
    $dom->load($html);
    //get rows
    $trs = $dom->find("tr");
    //first 2 rows are the header, removing it
    array_shift($trs);
    array_shift($trs);
    //the table is from 2 different parts
    $first_part = true;
    //get the information
    unset($out);
    foreach ((array) $trs as $tr) {
      $tds = $tr->find("td");
      if ($tds[0]->plaintext == "ADRESA ORGANIZACE") {
        $first_part = false;
      } else {
        $out['org_id'] = $data_row['org_id'];
        if ($first_part) {
          $out[trim($tds[0]->plaintext)] = trim($tds[2]->plaintext);
        } else {
          $out[trim($tds[0]->plaintext)] = trim($tds[1]->plaintext);     
        }
      }
    }
    //save it
    scraperwiki::save_sqlite(array('org_id'),$out);
    scraperwiki::save_var('last_org_id',$data_row['org_id']);
  }
}
scraperwiki::save_var('last_org_id',0);

?>
<?php
//original url: http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/detail.pl?org=2600649
// org= is NOT org_id (IČ) !!
// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php';
//read the data saved from list of org_id
scraperwiki::attach("cz_public_organizations_retrieval", "src");
$data = scraperwiki::select("* from src.swdata");

//sort data
foreach ($data as $key => $row) {
    $x[$key]  = $row['org_id'];
}
array_multisort($x, SORT_ASC, $data);

//last org_id
$last_org_id = scraperwiki::get_var('last_org_id',0);

foreach((array) $data as $data_row) {
  if ($data_row['org_id'] > $last_org_id) {
    //download the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/detail.pl?org=".$data_row['inner_org_id'];
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //clean &nbsp;
    $html = str_replace('&nbsp;',' ',$html);
    //get dom from data
    $dom = new simple_html_dom();
    $dom->load($html);
    //get rows
    $trs = $dom->find("tr");
    //first 2 rows are the header, removing it
    array_shift($trs);
    array_shift($trs);
    //the table is from 2 different parts
    $first_part = true;
    //get the information
    unset($out);
    foreach ((array) $trs as $tr) {
      $tds = $tr->find("td");
      if ($tds[0]->plaintext == "ADRESA ORGANIZACE") {
        $first_part = false;
      } else {
        $out['org_id'] = $data_row['org_id'];
        if ($first_part) {
          $out[trim($tds[0]->plaintext)] = trim($tds[2]->plaintext);
        } else {
          $out[trim($tds[0]->plaintext)] = trim($tds[1]->plaintext);     
        }
      }
    }
    //save it
    scraperwiki::save_sqlite(array('org_id'),$out);
    scraperwiki::save_var('last_org_id',$data_row['org_id']);
  }
}
scraperwiki::save_var('last_org_id',0);

?>
<?php
//original url: http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/detail.pl?org=2600649
// org= is NOT org_id (IČ) !!
// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php';
//read the data saved from list of org_id
scraperwiki::attach("cz_public_organizations_retrieval", "src");
$data = scraperwiki::select("* from src.swdata");

//sort data
foreach ($data as $key => $row) {
    $x[$key]  = $row['org_id'];
}
array_multisort($x, SORT_ASC, $data);

//last org_id
$last_org_id = scraperwiki::get_var('last_org_id',0);

foreach((array) $data as $data_row) {
  if ($data_row['org_id'] > $last_org_id) {
    //download the html
    $url = "http://wwwinfo.mfcr.cz/cgi-bin/ufisreg/detail.pl?org=".$data_row['inner_org_id'];
    $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
    //clean &nbsp;
    $html = str_replace('&nbsp;',' ',$html);
    //get dom from data
    $dom = new simple_html_dom();
    $dom->load($html);
    //get rows
    $trs = $dom->find("tr");
    //first 2 rows are the header, removing it
    array_shift($trs);
    array_shift($trs);
    //the table is from 2 different parts
    $first_part = true;
    //get the information
    unset($out);
    foreach ((array) $trs as $tr) {
      $tds = $tr->find("td");
      if ($tds[0]->plaintext == "ADRESA ORGANIZACE") {
        $first_part = false;
      } else {
        $out['org_id'] = $data_row['org_id'];
        if ($first_part) {
          $out[trim($tds[0]->plaintext)] = trim($tds[2]->plaintext);
        } else {
          $out[trim($tds[0]->plaintext)] = trim($tds[1]->plaintext);     
        }
      }
    }
    //save it
    scraperwiki::save_sqlite(array('org_id'),$out);
    scraperwiki::save_var('last_org_id',$data_row['org_id']);
  }
}
scraperwiki::save_var('last_org_id',0);

?>
