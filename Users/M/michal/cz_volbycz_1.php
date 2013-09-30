<?php

//http://volby.cz/

require 'scraperwiki/simple_html_dom.php';

//get the html->dom
$url = "http://volby.cz/";
$html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
$dom = new simple_html_dom();
$dom->load($html);

//get rows
$table = $dom->find('table[class=border1]',0);
$trs = $table->find('tr');

foreach ($trs as $tr) {
  $tds = $tr->find('td');

  foreach ($tds as $td) {
    //if td has <a>, it is a link, otherwise it is a 'type'
    if (count($td->find('a')) == 0) { //it is a 'type'
      if ($td->innertext != '') {
        $type = $td->plaintext;
      }
    } else { //it is a link
      $link = $td->find('a',0)->href;
      $year = $td->plaintext;
      $data[] = array(
        'type' => $type,
        'link' => $link,
        'year' => $year,
      );
    }
  }
}

scraperwiki::save_sqlite(array('type','year'),$data);


?>
<?php

//http://volby.cz/

require 'scraperwiki/simple_html_dom.php';

//get the html->dom
$url = "http://volby.cz/";
$html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
$dom = new simple_html_dom();
$dom->load($html);

//get rows
$table = $dom->find('table[class=border1]',0);
$trs = $table->find('tr');

foreach ($trs as $tr) {
  $tds = $tr->find('td');

  foreach ($tds as $td) {
    //if td has <a>, it is a link, otherwise it is a 'type'
    if (count($td->find('a')) == 0) { //it is a 'type'
      if ($td->innertext != '') {
        $type = $td->plaintext;
      }
    } else { //it is a link
      $link = $td->find('a',0)->href;
      $year = $td->plaintext;
      $data[] = array(
        'type' => $type,
        'link' => $link,
        'year' => $year,
      );
    }
  }
}

scraperwiki::save_sqlite(array('type','year'),$data);


?>
<?php

//http://volby.cz/

require 'scraperwiki/simple_html_dom.php';

//get the html->dom
$url = "http://volby.cz/";
$html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
$dom = new simple_html_dom();
$dom->load($html);

//get rows
$table = $dom->find('table[class=border1]',0);
$trs = $table->find('tr');

foreach ($trs as $tr) {
  $tds = $tr->find('td');

  foreach ($tds as $td) {
    //if td has <a>, it is a link, otherwise it is a 'type'
    if (count($td->find('a')) == 0) { //it is a 'type'
      if ($td->innertext != '') {
        $type = $td->plaintext;
      }
    } else { //it is a link
      $link = $td->find('a',0)->href;
      $year = $td->plaintext;
      $data[] = array(
        'type' => $type,
        'link' => $link,
        'year' => $year,
      );
    }
  }
}

scraperwiki::save_sqlite(array('type','year'),$data);


?>
<?php

//http://volby.cz/

require 'scraperwiki/simple_html_dom.php';

//get the html->dom
$url = "http://volby.cz/";
$html = str_replace('&nbsp;','',iconv('ISO-8859-2','UTF-8//TRANSLIT',scraperwiki::scrape($url)));
$dom = new simple_html_dom();
$dom->load($html);

//get rows
$table = $dom->find('table[class=border1]',0);
$trs = $table->find('tr');

foreach ($trs as $tr) {
  $tds = $tr->find('td');

  foreach ($tds as $td) {
    //if td has <a>, it is a link, otherwise it is a 'type'
    if (count($td->find('a')) == 0) { //it is a 'type'
      if ($td->innertext != '') {
        $type = $td->plaintext;
      }
    } else { //it is a link
      $link = $td->find('a',0)->href;
      $year = $td->plaintext;
      $data[] = array(
        'type' => $type,
        'link' => $link,
        'year' => $year,
      );
    }
  }
}

scraperwiki::save_sqlite(array('type','year'),$data);


?>
