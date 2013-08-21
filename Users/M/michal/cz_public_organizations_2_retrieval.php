<?php
require 'scraperwiki/simple_html_dom.php'; 
//read the data saved from downloader
scraperwiki::attach("cz_public_organizations_2_downloader", "src");
$data = scraperwiki::select("* from src.swdata");

//helper
$len = strlen("/cgi-bin/ufisreg/detail.pl?org=");

foreach ((array)$data as $data_row) {
    //get dom from data
    $dom = new simple_html_dom();
    $dom->load($data_row['html']);
    //extract information
    $rows = $dom->find("tr");
    //first row is the header, removing it
    array_shift($rows); 
    //foreach row save info
    foreach ((array) $rows as $row) {
      //inner org_id is in <a href= ... it is used for getting details from the system
      $as = $row->find("a");
      $tmp_text = $as[0]->href;
      $inner_org_id = substr($tmp_text,$len);
      //<td>
      $tds = $row->find("td");
      //save the data
      $out = array(
        'org_id' => trim($tds[0]->plaintext),
        'short_name' => trim($tds[1]->plaintext),
        'inner_org_id' => $inner_org_id,
        'chapter' => $data_row['chapter'],
      );
      scraperwiki::save_sqlite(array('org_id'),$out);
    }
}
?>
