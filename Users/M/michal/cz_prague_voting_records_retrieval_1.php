<?php
require 'scraperwiki/simple_html_dom.php';
//read the saved tables
scraperwiki::attach("cz_prague_voting_records_downloader_1", "src");
$rows = scraperwiki::select("* from src.swdata");

foreach($rows as $row) {
  //get dom
  $dom = new simple_html_dom();
  $dom->load("<html><body>".$row['html']."</body></html>");
  //get tbody
  $tables = $dom->find("table");
  //trs, first is header
  $trs = $tables[0]->find("tr");
  array_shift($trs);
  //for each row
  foreach($trs as $tr) {
    $tds = $tr->find("td");
    //extract id
    $as = $tds[4]->find("a");
    preg_match('/votingId=([0-9]{1,})&/' ,$as[0]->href,$matches);
    $id = $matches[1];
    $out = array (
      'id' => $id,
      'decision_number' => $tds[0]->plaintext,
      'date' => $tds[1]->plaintext,
      'document_number' => $tds[2]->plaintext,
      'name' => $tds[3]->plaintext,
      'passed' => $tds[4]->plaintext,
    );
    scraperwiki::save_sqlite(array('id'),$out);
  }
}

?>
