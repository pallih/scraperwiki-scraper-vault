<?php


//since 2012-06-06
//first division: http://www.psp.cz/ff/1d/e9/6a/08.htm

//original url: http:
//need to always find 'next division' (and 'previous division')
// the original is in windows-1250 !!

require 'scraperwiki/simple_html_dom.php'; 

$first_url = '/ff/1d/e9/6a/08.htm';
//44/2 '/ff/8b/64/ec/16.htm';
//44/1 '/ff/89/64/ec/16.htm';
//43/2 '/ff/87/64/ec/16.htm';
//43/1'/ff/85/64/ec/16.htm';
//42/2 '/ff/71/64/ec/16.htm';
//42/1 '/ff/b3/63/ec/16.htm';
//40  '/ff/1d/e9/6a/08.htm';
//41  '/ff/ef/62/ec/16.htm';

//corrections "by hand":
scraperwiki::save_var('last_url',$first_url);
//scraperwiki::save_var('last_i',55939);
//scraperwiki::sqliteexecute("delete from swdata");//55939
//scraperwiki::sqlitecommit();
//print_r($tmp);
//die();

//get last url
$next_url = scraperwiki::get_var('last_url','');
//$last_ok_i = $i;

//set conditions to continue
$continue = true;
//$consecutive_empty = 0;
//date_default_timezone_set('UTC');
//$last_date = new DateTime('1993-01-01');
//$now = new DateTime('now');

while ($continue) {
  $url = 'http://www.psp.cz'.$next_url;
  $url_short = $next_url;
  $html = iconv("cp1250","UTF-8//TRANSLIT",scraperwiki::scrape($url));
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  //is it valid division (or empty)
  $titles = $dom->find("title");

    if (($titles[0]->plaintext == 'Chyba SQW') or ($titles[0]->plaintext == 'Systémová chyba SQW') or (strpos($html,'ErrNo:') > 0) or ($titles[0]->plaintext == 'Error response') or ($html == '') or ($titles[0]->plaintext == '503 Service Temporarily Unavailable') or ($titles[0]->plaintext == 'Hlasování nenalezeno')) {
      //there are problems at the psp.cz (maybe around 3am CET)
      scraperwiki::save_var('last_url',$last_ok_url);
      echo "there are problems at the psp.cz (maybe around 3am CET), stopping";
      die();
    } else {
      //find date
      $h1 = $dom->find('h1',0);
      $h1 = str_replace('&nbsp;','',$h1->innertext);
      preg_match('/([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,4})/' ,$h1,$dates);
      preg_match('/([0-9]{2}:[0-9]{2})/' ,$h1,$times);
      $dates_ar=explode('.',$dates[1]);
      $iso_date = $dates_ar[2].'-'.n2($dates_ar[1]).'-'.n2($dates_ar[0]);

      //find previous and next
      $div = $dom->find('div[class=document-nav-x]',0);
      if (is_object($div)) {
        $prevv = $div->find('a[class=prev]',0);
        $nextt = $div->find('a[class=next]',0);
        $previous = $prevv->href;
        $data = array(
          'html' => $html,
          'url' => $next_url,
          'previous_url' => $previous,
          'date' => $iso_date,
          'time' => $times[1],
        );
        if (is_object($nextt)) {
          $next_url = $nextt->href;
          $data['next_url'] = $next_url;
        }
        else
          $continue = false;

      //save it
      scraperwiki::save_sqlite(array('url'),$data);
      scraperwiki::save_var('last_url',$url_short);
      } else 
          $continue = false;

    }
}

function n2($n){
  if ($n<10) return '0'.$n;
  else return $n;
}
?>
