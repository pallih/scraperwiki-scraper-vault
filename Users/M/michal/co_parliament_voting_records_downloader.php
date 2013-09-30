<?php

//NOTE TO MY DEAREST SCRAPERWIKI AUTHORS: I have solved the problem with saving raw file (.xls) into database myself (I have asked at the Google group about)
//    using http://groups.google.com/group/scraperwiki/browse_thread/thread/16f313bd5f12e782
//    and https://scraperwiki.com/scrapers/frac_focus_wells/
//    THANK YOU !

//NOTE 2: I have to wait for rar support, put $start at 40 to test it

//http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start=35
//notes: parameter limit does not work;
//    some files are really bad pdfs with no voting records in them
//    the others (possibly with voting records) are either .rar or .zip with good excel, text=.000 (voting records) or bad pdfs(no voting records) files in them

require 'scraperwiki/simple_html_dom.php';

//get number of pages
//$last_start=45;  //temporarily skip the first download
$url = 'http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start=0';
$html = scraperwiki::scrape($url);
$dom = new simple_html_dom();
$dom->load($html);
$as = $dom->find('div[id=dm_nav]',0)->find('a');
$a = end($as)->href;
preg_match('/start=([0-9]{1,})/',$a,$matches);
$last_start = $matches[1];

//create a new table (just once)
/*scraperwiki::sqliteexecute("create table file (`type` text, `name` text, `file_blob` blob)");
scraperwiki::sqlitecommit();*/

for ($start = 0; $start <= $last_start; $start = $start + 5) { //start from 0 !!
  //page
  $url = 'http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start='.$start;
  $html = scraperwiki::scrape($url);
  $dom = new simple_html_dom();
  $dom->load($html);
  
  //zip, rar and other files
  $divs = $dom->find('div[class=dm_row]');
  if (count($divs) > 0) {
    foreach ($divs as $div) {
      //file info
      preg_match('/32x32\/([a-zA-Z]{1,})./',$div->find('img',0)->src,$matches);
      $type = $matches[1];
      $link = 'http://www.camara.gov.co'.$div->find('a',0)->href;
      $title = $div->find('a',0)->title;

      //date
      preg_match('/([0-9]{2}) ([0-9]{1,2}) de ([0-9]{4})/',mes2number($title),$matches);
      $date = $matches[3].'-'.$matches[1]. '-' . ((strlen($matches[2]) == 1) ? '0'.$matches[2] : $matches[2]) ;

      //general info
      $ar = explode('/',$div->find('td',1)->plaintext);
      $date_added = $ar[2].'-'.$ar[0].'-'.$ar[1];
      $ar = explode('/',$div->find('td',3)->plaintext);
      $date_modified = $ar[2].'-'.$ar[0].'-'.$ar[1];
      $filesize = $div->find('td',5)->plaintext;
      $hits = $div->find('td',7)->plaintext;
      
      $data_source = array(
        'name' => $title,
        'link' => $link,
        'type' => $type,
        'date' => $date,       
      );
      scraperwiki::save_sqlite(array('name'),$data_source,'source');
      
      //extract files from zip and save them
      $bin_file = scraperwiki::scrape($link);
      switch ($type) {
        case 'zip':
          $handle = fopen('/tmp/co_parl.zip',"w");
          fwrite($handle,$bin_file);
          $zip = zip_open('/tmp/co_parl.zip');
          while ($zip_entry = zip_read($zip)) {
            $buf = zip_entry_read($zip_entry, zip_entry_filesize($zip_entry));
            $zip_entry_name = zip_entry_name($zip_entry);
            $zen_ar = explode('.',$zip_entry_name);
            $zip_entry_type = end($zen_ar);
            $data = array(
              'date' => $date,
              'type' => $zip_entry_type,
              'name' => $zip_entry_name,
              'file_encode' => base64_encode($buf),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          }
          break;
        case 'rar':
          $handle = fopen('/tmp/co_parl.rar',"w");
          fwrite($handle,$bin_file);
          $rar = RarArchive::open ('/tmp/co_parl.rar');
          $rar_list = $rar->getEntries();
          foreach($rar_list as $rar_file) {
            $ren_ar = explode('.',$rar_file->getName());
            $rar_entry_type = end($ren_ar);

            $entry = rar_entry_get($rar,$rar_file->getName());
            $entry->extract('/tmp/'.$rar_file->getName());
            $buf = file_get_contents('/tmp/'.$rar_file->getName());

            $data = array(
              'date' => $date,
              'type' => $rar_entry_type,
              'name' => $rar_file->getName(),
              'file_encode' => base64_encode($buf),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          }
          break;
        default:
          $data = array(
              'date' => $date,
              'type' => $type,
              'name' => $title.'.'.$type,
              'file_encode' => base64_encode($bin_file),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          break;
      }
      fclose($handle);
    }
  }

//$file = scraperwiki::scrape($url);


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

//NOTE TO MY DEAREST SCRAPERWIKI AUTHORS: I have solved the problem with saving raw file (.xls) into database myself (I have asked at the Google group about)
//    using http://groups.google.com/group/scraperwiki/browse_thread/thread/16f313bd5f12e782
//    and https://scraperwiki.com/scrapers/frac_focus_wells/
//    THANK YOU !

//NOTE 2: I have to wait for rar support, put $start at 40 to test it

//http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start=35
//notes: parameter limit does not work;
//    some files are really bad pdfs with no voting records in them
//    the others (possibly with voting records) are either .rar or .zip with good excel, text=.000 (voting records) or bad pdfs(no voting records) files in them

require 'scraperwiki/simple_html_dom.php';

//get number of pages
//$last_start=45;  //temporarily skip the first download
$url = 'http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start=0';
$html = scraperwiki::scrape($url);
$dom = new simple_html_dom();
$dom->load($html);
$as = $dom->find('div[id=dm_nav]',0)->find('a');
$a = end($as)->href;
preg_match('/start=([0-9]{1,})/',$a,$matches);
$last_start = $matches[1];

//create a new table (just once)
/*scraperwiki::sqliteexecute("create table file (`type` text, `name` text, `file_blob` blob)");
scraperwiki::sqlitecommit();*/

for ($start = 0; $start <= $last_start; $start = $start + 5) { //start from 0 !!
  //page
  $url = 'http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start='.$start;
  $html = scraperwiki::scrape($url);
  $dom = new simple_html_dom();
  $dom->load($html);
  
  //zip, rar and other files
  $divs = $dom->find('div[class=dm_row]');
  if (count($divs) > 0) {
    foreach ($divs as $div) {
      //file info
      preg_match('/32x32\/([a-zA-Z]{1,})./',$div->find('img',0)->src,$matches);
      $type = $matches[1];
      $link = 'http://www.camara.gov.co'.$div->find('a',0)->href;
      $title = $div->find('a',0)->title;

      //date
      preg_match('/([0-9]{2}) ([0-9]{1,2}) de ([0-9]{4})/',mes2number($title),$matches);
      $date = $matches[3].'-'.$matches[1]. '-' . ((strlen($matches[2]) == 1) ? '0'.$matches[2] : $matches[2]) ;

      //general info
      $ar = explode('/',$div->find('td',1)->plaintext);
      $date_added = $ar[2].'-'.$ar[0].'-'.$ar[1];
      $ar = explode('/',$div->find('td',3)->plaintext);
      $date_modified = $ar[2].'-'.$ar[0].'-'.$ar[1];
      $filesize = $div->find('td',5)->plaintext;
      $hits = $div->find('td',7)->plaintext;
      
      $data_source = array(
        'name' => $title,
        'link' => $link,
        'type' => $type,
        'date' => $date,       
      );
      scraperwiki::save_sqlite(array('name'),$data_source,'source');
      
      //extract files from zip and save them
      $bin_file = scraperwiki::scrape($link);
      switch ($type) {
        case 'zip':
          $handle = fopen('/tmp/co_parl.zip',"w");
          fwrite($handle,$bin_file);
          $zip = zip_open('/tmp/co_parl.zip');
          while ($zip_entry = zip_read($zip)) {
            $buf = zip_entry_read($zip_entry, zip_entry_filesize($zip_entry));
            $zip_entry_name = zip_entry_name($zip_entry);
            $zen_ar = explode('.',$zip_entry_name);
            $zip_entry_type = end($zen_ar);
            $data = array(
              'date' => $date,
              'type' => $zip_entry_type,
              'name' => $zip_entry_name,
              'file_encode' => base64_encode($buf),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          }
          break;
        case 'rar':
          $handle = fopen('/tmp/co_parl.rar',"w");
          fwrite($handle,$bin_file);
          $rar = RarArchive::open ('/tmp/co_parl.rar');
          $rar_list = $rar->getEntries();
          foreach($rar_list as $rar_file) {
            $ren_ar = explode('.',$rar_file->getName());
            $rar_entry_type = end($ren_ar);

            $entry = rar_entry_get($rar,$rar_file->getName());
            $entry->extract('/tmp/'.$rar_file->getName());
            $buf = file_get_contents('/tmp/'.$rar_file->getName());

            $data = array(
              'date' => $date,
              'type' => $rar_entry_type,
              'name' => $rar_file->getName(),
              'file_encode' => base64_encode($buf),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          }
          break;
        default:
          $data = array(
              'date' => $date,
              'type' => $type,
              'name' => $title.'.'.$type,
              'file_encode' => base64_encode($bin_file),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          break;
      }
      fclose($handle);
    }
  }

//$file = scraperwiki::scrape($url);


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

//NOTE TO MY DEAREST SCRAPERWIKI AUTHORS: I have solved the problem with saving raw file (.xls) into database myself (I have asked at the Google group about)
//    using http://groups.google.com/group/scraperwiki/browse_thread/thread/16f313bd5f12e782
//    and https://scraperwiki.com/scrapers/frac_focus_wells/
//    THANK YOU !

//NOTE 2: I have to wait for rar support, put $start at 40 to test it

//http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start=35
//notes: parameter limit does not work;
//    some files are really bad pdfs with no voting records in them
//    the others (possibly with voting records) are either .rar or .zip with good excel, text=.000 (voting records) or bad pdfs(no voting records) files in them

require 'scraperwiki/simple_html_dom.php';

//get number of pages
//$last_start=45;  //temporarily skip the first download
$url = 'http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start=0';
$html = scraperwiki::scrape($url);
$dom = new simple_html_dom();
$dom->load($html);
$as = $dom->find('div[id=dm_nav]',0)->find('a');
$a = end($as)->href;
preg_match('/start=([0-9]{1,})/',$a,$matches);
$last_start = $matches[1];

//create a new table (just once)
/*scraperwiki::sqliteexecute("create table file (`type` text, `name` text, `file_blob` blob)");
scraperwiki::sqlitecommit();*/

for ($start = 0; $start <= $last_start; $start = $start + 5) { //start from 0 !!
  //page
  $url = 'http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start='.$start;
  $html = scraperwiki::scrape($url);
  $dom = new simple_html_dom();
  $dom->load($html);
  
  //zip, rar and other files
  $divs = $dom->find('div[class=dm_row]');
  if (count($divs) > 0) {
    foreach ($divs as $div) {
      //file info
      preg_match('/32x32\/([a-zA-Z]{1,})./',$div->find('img',0)->src,$matches);
      $type = $matches[1];
      $link = 'http://www.camara.gov.co'.$div->find('a',0)->href;
      $title = $div->find('a',0)->title;

      //date
      preg_match('/([0-9]{2}) ([0-9]{1,2}) de ([0-9]{4})/',mes2number($title),$matches);
      $date = $matches[3].'-'.$matches[1]. '-' . ((strlen($matches[2]) == 1) ? '0'.$matches[2] : $matches[2]) ;

      //general info
      $ar = explode('/',$div->find('td',1)->plaintext);
      $date_added = $ar[2].'-'.$ar[0].'-'.$ar[1];
      $ar = explode('/',$div->find('td',3)->plaintext);
      $date_modified = $ar[2].'-'.$ar[0].'-'.$ar[1];
      $filesize = $div->find('td',5)->plaintext;
      $hits = $div->find('td',7)->plaintext;
      
      $data_source = array(
        'name' => $title,
        'link' => $link,
        'type' => $type,
        'date' => $date,       
      );
      scraperwiki::save_sqlite(array('name'),$data_source,'source');
      
      //extract files from zip and save them
      $bin_file = scraperwiki::scrape($link);
      switch ($type) {
        case 'zip':
          $handle = fopen('/tmp/co_parl.zip',"w");
          fwrite($handle,$bin_file);
          $zip = zip_open('/tmp/co_parl.zip');
          while ($zip_entry = zip_read($zip)) {
            $buf = zip_entry_read($zip_entry, zip_entry_filesize($zip_entry));
            $zip_entry_name = zip_entry_name($zip_entry);
            $zen_ar = explode('.',$zip_entry_name);
            $zip_entry_type = end($zen_ar);
            $data = array(
              'date' => $date,
              'type' => $zip_entry_type,
              'name' => $zip_entry_name,
              'file_encode' => base64_encode($buf),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          }
          break;
        case 'rar':
          $handle = fopen('/tmp/co_parl.rar',"w");
          fwrite($handle,$bin_file);
          $rar = RarArchive::open ('/tmp/co_parl.rar');
          $rar_list = $rar->getEntries();
          foreach($rar_list as $rar_file) {
            $ren_ar = explode('.',$rar_file->getName());
            $rar_entry_type = end($ren_ar);

            $entry = rar_entry_get($rar,$rar_file->getName());
            $entry->extract('/tmp/'.$rar_file->getName());
            $buf = file_get_contents('/tmp/'.$rar_file->getName());

            $data = array(
              'date' => $date,
              'type' => $rar_entry_type,
              'name' => $rar_file->getName(),
              'file_encode' => base64_encode($buf),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          }
          break;
        default:
          $data = array(
              'date' => $date,
              'type' => $type,
              'name' => $title.'.'.$type,
              'file_encode' => base64_encode($bin_file),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          break;
      }
      fclose($handle);
    }
  }

//$file = scraperwiki::scrape($url);


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

//NOTE TO MY DEAREST SCRAPERWIKI AUTHORS: I have solved the problem with saving raw file (.xls) into database myself (I have asked at the Google group about)
//    using http://groups.google.com/group/scraperwiki/browse_thread/thread/16f313bd5f12e782
//    and https://scraperwiki.com/scrapers/frac_focus_wells/
//    THANK YOU !

//NOTE 2: I have to wait for rar support, put $start at 40 to test it

//http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start=35
//notes: parameter limit does not work;
//    some files are really bad pdfs with no voting records in them
//    the others (possibly with voting records) are either .rar or .zip with good excel, text=.000 (voting records) or bad pdfs(no voting records) files in them

require 'scraperwiki/simple_html_dom.php';

//get number of pages
//$last_start=45;  //temporarily skip the first download
$url = 'http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start=0';
$html = scraperwiki::scrape($url);
$dom = new simple_html_dom();
$dom->load($html);
$as = $dom->find('div[id=dm_nav]',0)->find('a');
$a = end($as)->href;
preg_match('/start=([0-9]{1,})/',$a,$matches);
$last_start = $matches[1];

//create a new table (just once)
/*scraperwiki::sqliteexecute("create table file (`type` text, `name` text, `file_blob` blob)");
scraperwiki::sqlitecommit();*/

for ($start = 0; $start <= $last_start; $start = $start + 5) { //start from 0 !!
  //page
  $url = 'http://www.camara.gov.co/portal2011/gestor-documental/cat_view/98-documentos-votaciones?limit=5&order=date&dir=ASC&change_font=small&start='.$start;
  $html = scraperwiki::scrape($url);
  $dom = new simple_html_dom();
  $dom->load($html);
  
  //zip, rar and other files
  $divs = $dom->find('div[class=dm_row]');
  if (count($divs) > 0) {
    foreach ($divs as $div) {
      //file info
      preg_match('/32x32\/([a-zA-Z]{1,})./',$div->find('img',0)->src,$matches);
      $type = $matches[1];
      $link = 'http://www.camara.gov.co'.$div->find('a',0)->href;
      $title = $div->find('a',0)->title;

      //date
      preg_match('/([0-9]{2}) ([0-9]{1,2}) de ([0-9]{4})/',mes2number($title),$matches);
      $date = $matches[3].'-'.$matches[1]. '-' . ((strlen($matches[2]) == 1) ? '0'.$matches[2] : $matches[2]) ;

      //general info
      $ar = explode('/',$div->find('td',1)->plaintext);
      $date_added = $ar[2].'-'.$ar[0].'-'.$ar[1];
      $ar = explode('/',$div->find('td',3)->plaintext);
      $date_modified = $ar[2].'-'.$ar[0].'-'.$ar[1];
      $filesize = $div->find('td',5)->plaintext;
      $hits = $div->find('td',7)->plaintext;
      
      $data_source = array(
        'name' => $title,
        'link' => $link,
        'type' => $type,
        'date' => $date,       
      );
      scraperwiki::save_sqlite(array('name'),$data_source,'source');
      
      //extract files from zip and save them
      $bin_file = scraperwiki::scrape($link);
      switch ($type) {
        case 'zip':
          $handle = fopen('/tmp/co_parl.zip',"w");
          fwrite($handle,$bin_file);
          $zip = zip_open('/tmp/co_parl.zip');
          while ($zip_entry = zip_read($zip)) {
            $buf = zip_entry_read($zip_entry, zip_entry_filesize($zip_entry));
            $zip_entry_name = zip_entry_name($zip_entry);
            $zen_ar = explode('.',$zip_entry_name);
            $zip_entry_type = end($zen_ar);
            $data = array(
              'date' => $date,
              'type' => $zip_entry_type,
              'name' => $zip_entry_name,
              'file_encode' => base64_encode($buf),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          }
          break;
        case 'rar':
          $handle = fopen('/tmp/co_parl.rar',"w");
          fwrite($handle,$bin_file);
          $rar = RarArchive::open ('/tmp/co_parl.rar');
          $rar_list = $rar->getEntries();
          foreach($rar_list as $rar_file) {
            $ren_ar = explode('.',$rar_file->getName());
            $rar_entry_type = end($ren_ar);

            $entry = rar_entry_get($rar,$rar_file->getName());
            $entry->extract('/tmp/'.$rar_file->getName());
            $buf = file_get_contents('/tmp/'.$rar_file->getName());

            $data = array(
              'date' => $date,
              'type' => $rar_entry_type,
              'name' => $rar_file->getName(),
              'file_encode' => base64_encode($buf),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          }
          break;
        default:
          $data = array(
              'date' => $date,
              'type' => $type,
              'name' => $title.'.'.$type,
              'file_encode' => base64_encode($bin_file),
            );
            scraperwiki::save_sqlite(array('date','name'),$data,'file');
          break;
      }
      fclose($handle);
    }
  }

//$file = scraperwiki::scrape($url);


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
