<?php
//there are voting records for 2010 and 3/4 of 2011 at old website

require 'scraperwiki/simple_html_dom.php';

$url = 'http://201.245.176.228/camara/site/artic/20090826/pags/20090826160757.html';
$html = iconv("ISO-8859-1", "UTF-8//TRANSLIT",scraperwiki::scrape($url));

$dom = new simple_html_dom();
$dom->load($html);

$tds = $dom->find('table[class=conBorde]',0)->find('td');
foreach ($tds as $td) {
  if (str_replace('&nbsp;','',$td->plaintext) != '') {
    $link = 'http://201.245.176.228'.$td->find('a',0)->href;
    $bin_file = scraperwiki::scrape($link);

    $title = str_replace('&nbsp;', ' ',trim($td->plaintext));
    $title = trim(str_replace('  ', ' ',$title));
    if ($title == '') continue;

    //date
    preg_match('/([0-9]{1,2}) de ([0-9]{2}) de ([0-9]{4})/',mes2number($title),$matches);
    $date = $matches[3].'-'.$matches[2]. '-' . ((strlen($matches[1]) == 1) ? '0'.$matches[1] : $matches[1]) ;

    //type
    $tmp = explode(' ',$title);
    $type = mb_strtolower(end($tmp), 'UTF-8');

    //format
    $tmp = explode('.',$link);
    $format = end($tmp);
    
    $data = array(
      'date' => $date,
      'file' => base64_encode($bin_file),
      'type' => $type,
      'name' => $title,
      'link' => $link,
      'format' => $format,
    );
    scraperwiki::save_sqlite(array('date','name'),$data,'file');
  }
}


function mes2number ($title) {
  $title = mb_strtolower($title, 'UTF-8');
  $title = str_replace('enero', '01', $title);
  $title = str_replace('febrero', '02', $title);
  $title = str_replace('marzo', '03', $title);
  $title = str_replace('abril', '04', $title);
  $title = str_replace('mayo', '05', $title);
  $title = str_replace('junio', '06', $title);
  $title = str_replace('julio', '07', $title);
  $title = str_replace('agosto', '08', $title);
  $title = str_replace('septiembre', '09', $title);
  $title = str_replace('setiembre', '09', $title);
  $title = str_replace('octubre', '10', $title);
  $title = str_replace('noviembre', '11', $title);
  $title = str_replace('diciembre', '12', $title);
  return $title;
}
?>
<?php
//there are voting records for 2010 and 3/4 of 2011 at old website

require 'scraperwiki/simple_html_dom.php';

$url = 'http://201.245.176.228/camara/site/artic/20090826/pags/20090826160757.html';
$html = iconv("ISO-8859-1", "UTF-8//TRANSLIT",scraperwiki::scrape($url));

$dom = new simple_html_dom();
$dom->load($html);

$tds = $dom->find('table[class=conBorde]',0)->find('td');
foreach ($tds as $td) {
  if (str_replace('&nbsp;','',$td->plaintext) != '') {
    $link = 'http://201.245.176.228'.$td->find('a',0)->href;
    $bin_file = scraperwiki::scrape($link);

    $title = str_replace('&nbsp;', ' ',trim($td->plaintext));
    $title = trim(str_replace('  ', ' ',$title));
    if ($title == '') continue;

    //date
    preg_match('/([0-9]{1,2}) de ([0-9]{2}) de ([0-9]{4})/',mes2number($title),$matches);
    $date = $matches[3].'-'.$matches[2]. '-' . ((strlen($matches[1]) == 1) ? '0'.$matches[1] : $matches[1]) ;

    //type
    $tmp = explode(' ',$title);
    $type = mb_strtolower(end($tmp), 'UTF-8');

    //format
    $tmp = explode('.',$link);
    $format = end($tmp);
    
    $data = array(
      'date' => $date,
      'file' => base64_encode($bin_file),
      'type' => $type,
      'name' => $title,
      'link' => $link,
      'format' => $format,
    );
    scraperwiki::save_sqlite(array('date','name'),$data,'file');
  }
}


function mes2number ($title) {
  $title = mb_strtolower($title, 'UTF-8');
  $title = str_replace('enero', '01', $title);
  $title = str_replace('febrero', '02', $title);
  $title = str_replace('marzo', '03', $title);
  $title = str_replace('abril', '04', $title);
  $title = str_replace('mayo', '05', $title);
  $title = str_replace('junio', '06', $title);
  $title = str_replace('julio', '07', $title);
  $title = str_replace('agosto', '08', $title);
  $title = str_replace('septiembre', '09', $title);
  $title = str_replace('setiembre', '09', $title);
  $title = str_replace('octubre', '10', $title);
  $title = str_replace('noviembre', '11', $title);
  $title = str_replace('diciembre', '12', $title);
  return $title;
}
?>
<?php
//there are voting records for 2010 and 3/4 of 2011 at old website

require 'scraperwiki/simple_html_dom.php';

$url = 'http://201.245.176.228/camara/site/artic/20090826/pags/20090826160757.html';
$html = iconv("ISO-8859-1", "UTF-8//TRANSLIT",scraperwiki::scrape($url));

$dom = new simple_html_dom();
$dom->load($html);

$tds = $dom->find('table[class=conBorde]',0)->find('td');
foreach ($tds as $td) {
  if (str_replace('&nbsp;','',$td->plaintext) != '') {
    $link = 'http://201.245.176.228'.$td->find('a',0)->href;
    $bin_file = scraperwiki::scrape($link);

    $title = str_replace('&nbsp;', ' ',trim($td->plaintext));
    $title = trim(str_replace('  ', ' ',$title));
    if ($title == '') continue;

    //date
    preg_match('/([0-9]{1,2}) de ([0-9]{2}) de ([0-9]{4})/',mes2number($title),$matches);
    $date = $matches[3].'-'.$matches[2]. '-' . ((strlen($matches[1]) == 1) ? '0'.$matches[1] : $matches[1]) ;

    //type
    $tmp = explode(' ',$title);
    $type = mb_strtolower(end($tmp), 'UTF-8');

    //format
    $tmp = explode('.',$link);
    $format = end($tmp);
    
    $data = array(
      'date' => $date,
      'file' => base64_encode($bin_file),
      'type' => $type,
      'name' => $title,
      'link' => $link,
      'format' => $format,
    );
    scraperwiki::save_sqlite(array('date','name'),$data,'file');
  }
}


function mes2number ($title) {
  $title = mb_strtolower($title, 'UTF-8');
  $title = str_replace('enero', '01', $title);
  $title = str_replace('febrero', '02', $title);
  $title = str_replace('marzo', '03', $title);
  $title = str_replace('abril', '04', $title);
  $title = str_replace('mayo', '05', $title);
  $title = str_replace('junio', '06', $title);
  $title = str_replace('julio', '07', $title);
  $title = str_replace('agosto', '08', $title);
  $title = str_replace('septiembre', '09', $title);
  $title = str_replace('setiembre', '09', $title);
  $title = str_replace('octubre', '10', $title);
  $title = str_replace('noviembre', '11', $title);
  $title = str_replace('diciembre', '12', $title);
  return $title;
}
?>
