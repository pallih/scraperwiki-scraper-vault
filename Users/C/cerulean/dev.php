<?php

 require 'scraperwiki/simple_html_dom.php';

$html = scraperWiki::scrape("http://www.zend.com/en/yellow-pages#list-cid=229certtype=ANYPHP");           
#print $html . "\n";
sleep(5);
$html = scraperWiki::scrape("http://www.zend.com/en/yellow-pages#list-cid=39&firstname=&lastname=&orderby=name&sid=AB&company=&photo_first=&certtype=PHPZF&ClientCandidateID=");   
print $html . "\n";

$dom = new simple_html_dom();
$dom->load($html);

$table = $dom->find("table",0);

$trs = $table->find("tr");
array_shift($trs);
array_shift($trs);

foreach ($trs as $tr) {
  $td = $tr->find("td");
  $data = array(
    'pic' => $td[0]->plaintext,
    'name' => str_replace('&nbsp;',' ',$td[1]->plaintext),
    'date' => $td[2]->plaintext,
    'company' => $td[3]->plaintext,
    'email' => $td[4]->plaintext,

  );
echo  $data;
  scraperwiki::save_sqlite(array('pic','name'),$data);
}


?>
