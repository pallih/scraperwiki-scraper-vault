<?php

//extract answers from Wahl-O-Mats
//need to be downloaded in advance (the completed tests)

//domain with downloaded files
$domain = "http://dev.kohovolit.eu/tmp/germany/";

$files = array(
array('land'=>'sl','file'=>'sl_1.html','year'=>'2012'),
array('land'=>'sl','file'=>'sl_2.html','year'=>'2012'),

array('land'=>'sh','file'=>'sh_1.html','year'=>'2012'),
array('land'=>'sh','file'=>'sh_2.html','year'=>'2012'),

array('land'=>'nw','file'=>'nw_1.html','year'=>'2012'),
array('land'=>'nw','file'=>'nw_2.html','year'=>'2012'),
array('land'=>'nw','file'=>'nw_3.html','year'=>'2012'),

array('land'=>'hh','file'=>'hh_1.html','year'=>'2011'),
array('land'=>'hh','file'=>'hh_2.html','year'=>'2011'),

array('land'=>'rp','file'=>'rp_1.html','year'=>'2011'),
array('land'=>'rp','file'=>'rp_2.html','year'=>'2011'),

array('land'=>'bw','file'=>'bw_1.html','year'=>'2011'),
array('land'=>'bw','file'=>'bw_2.html','year'=>'2011'),
array('land'=>'bw','file'=>'bw_3.html','year'=>'2011'),

array('land'=>'hb','file'=>'hb_1.html','year'=>'2011'),
array('land'=>'hb','file'=>'hb_2.html','year'=>'2011'),

array('land'=>'be','file'=>'be_1.html','year'=>'2011'),
array('land'=>'be','file'=>'be_2.html','year'=>'2011'),
array('land'=>'be','file'=>'be_3.html','year'=>'2011'),
);


require 'scraperwiki/simple_html_dom.php';

foreach ($files as $row) {
  $url = $domain . $row['file'];
  $html = html_entity_decode(iconv("ISO-8859-1","UTF-8//TRANSLIT",scraperwiki::scrape($url)),ENT_COMPAT,'UTF-8');
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  $diff_rows = array(1,2);
  $answers = array(
    'y' => 'stimmt zu',
    'n' => 'stimmt nicht zu',
    'a' => 'steht neutral dazu',
  );
  $j = 0;
  foreach ($diff_rows as $zebra) {
    $i = 0;
    $divs=$dom->find("div[class=tablebg{$zebra}]");
    foreach ($divs as $div) {
      $k = 2*$i+$j+1;
      $q_ar = explode("<span",trim($div->find("a",0)->innertext));
      $question_name = trim($q_ar[0]);
      $question_full = trim($div->find("span",0)->plaintext);
      $question = array(
         'name' => $question_name,
         'description' => $question_full,
         'land' => $row['land'],
         'year' => $row['year'],
         'number' => $k,
      );
      scraperwiki::save_sqlite(array('land','year','number'),$question,'question');
      $as = $div->find("a");
      array_shift($as);
      foreach ($as as $a) {
        foreach ($answers as $akey => $answer) {
          $text = $a->plaintext;
          if (strpos($text,$answer)) {
            $party = str_replace(' ' . $answer,'',$text);
            $vote = $akey;
          }
//echo $question_name . $question_full . $party . $vote; die();
        }
      $one_answer[] = array(
         'land' => $row['land'],
         'year' => $row['year'],
         'number' => $k,
         'party' => $party,
         'vote' => $vote,
      );  
      }
    $i++;
    }
  $j++;
  }

}
scraperwiki::save_sqlite(array('land','year','number','party'),$one_answer,'answer');

?>
<?php

//extract answers from Wahl-O-Mats
//need to be downloaded in advance (the completed tests)

//domain with downloaded files
$domain = "http://dev.kohovolit.eu/tmp/germany/";

$files = array(
array('land'=>'sl','file'=>'sl_1.html','year'=>'2012'),
array('land'=>'sl','file'=>'sl_2.html','year'=>'2012'),

array('land'=>'sh','file'=>'sh_1.html','year'=>'2012'),
array('land'=>'sh','file'=>'sh_2.html','year'=>'2012'),

array('land'=>'nw','file'=>'nw_1.html','year'=>'2012'),
array('land'=>'nw','file'=>'nw_2.html','year'=>'2012'),
array('land'=>'nw','file'=>'nw_3.html','year'=>'2012'),

array('land'=>'hh','file'=>'hh_1.html','year'=>'2011'),
array('land'=>'hh','file'=>'hh_2.html','year'=>'2011'),

array('land'=>'rp','file'=>'rp_1.html','year'=>'2011'),
array('land'=>'rp','file'=>'rp_2.html','year'=>'2011'),

array('land'=>'bw','file'=>'bw_1.html','year'=>'2011'),
array('land'=>'bw','file'=>'bw_2.html','year'=>'2011'),
array('land'=>'bw','file'=>'bw_3.html','year'=>'2011'),

array('land'=>'hb','file'=>'hb_1.html','year'=>'2011'),
array('land'=>'hb','file'=>'hb_2.html','year'=>'2011'),

array('land'=>'be','file'=>'be_1.html','year'=>'2011'),
array('land'=>'be','file'=>'be_2.html','year'=>'2011'),
array('land'=>'be','file'=>'be_3.html','year'=>'2011'),
);


require 'scraperwiki/simple_html_dom.php';

foreach ($files as $row) {
  $url = $domain . $row['file'];
  $html = html_entity_decode(iconv("ISO-8859-1","UTF-8//TRANSLIT",scraperwiki::scrape($url)),ENT_COMPAT,'UTF-8');
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  $diff_rows = array(1,2);
  $answers = array(
    'y' => 'stimmt zu',
    'n' => 'stimmt nicht zu',
    'a' => 'steht neutral dazu',
  );
  $j = 0;
  foreach ($diff_rows as $zebra) {
    $i = 0;
    $divs=$dom->find("div[class=tablebg{$zebra}]");
    foreach ($divs as $div) {
      $k = 2*$i+$j+1;
      $q_ar = explode("<span",trim($div->find("a",0)->innertext));
      $question_name = trim($q_ar[0]);
      $question_full = trim($div->find("span",0)->plaintext);
      $question = array(
         'name' => $question_name,
         'description' => $question_full,
         'land' => $row['land'],
         'year' => $row['year'],
         'number' => $k,
      );
      scraperwiki::save_sqlite(array('land','year','number'),$question,'question');
      $as = $div->find("a");
      array_shift($as);
      foreach ($as as $a) {
        foreach ($answers as $akey => $answer) {
          $text = $a->plaintext;
          if (strpos($text,$answer)) {
            $party = str_replace(' ' . $answer,'',$text);
            $vote = $akey;
          }
//echo $question_name . $question_full . $party . $vote; die();
        }
      $one_answer[] = array(
         'land' => $row['land'],
         'year' => $row['year'],
         'number' => $k,
         'party' => $party,
         'vote' => $vote,
      );  
      }
    $i++;
    }
  $j++;
  }

}
scraperwiki::save_sqlite(array('land','year','number','party'),$one_answer,'answer');

?>
<?php

//extract answers from Wahl-O-Mats
//need to be downloaded in advance (the completed tests)

//domain with downloaded files
$domain = "http://dev.kohovolit.eu/tmp/germany/";

$files = array(
array('land'=>'sl','file'=>'sl_1.html','year'=>'2012'),
array('land'=>'sl','file'=>'sl_2.html','year'=>'2012'),

array('land'=>'sh','file'=>'sh_1.html','year'=>'2012'),
array('land'=>'sh','file'=>'sh_2.html','year'=>'2012'),

array('land'=>'nw','file'=>'nw_1.html','year'=>'2012'),
array('land'=>'nw','file'=>'nw_2.html','year'=>'2012'),
array('land'=>'nw','file'=>'nw_3.html','year'=>'2012'),

array('land'=>'hh','file'=>'hh_1.html','year'=>'2011'),
array('land'=>'hh','file'=>'hh_2.html','year'=>'2011'),

array('land'=>'rp','file'=>'rp_1.html','year'=>'2011'),
array('land'=>'rp','file'=>'rp_2.html','year'=>'2011'),

array('land'=>'bw','file'=>'bw_1.html','year'=>'2011'),
array('land'=>'bw','file'=>'bw_2.html','year'=>'2011'),
array('land'=>'bw','file'=>'bw_3.html','year'=>'2011'),

array('land'=>'hb','file'=>'hb_1.html','year'=>'2011'),
array('land'=>'hb','file'=>'hb_2.html','year'=>'2011'),

array('land'=>'be','file'=>'be_1.html','year'=>'2011'),
array('land'=>'be','file'=>'be_2.html','year'=>'2011'),
array('land'=>'be','file'=>'be_3.html','year'=>'2011'),
);


require 'scraperwiki/simple_html_dom.php';

foreach ($files as $row) {
  $url = $domain . $row['file'];
  $html = html_entity_decode(iconv("ISO-8859-1","UTF-8//TRANSLIT",scraperwiki::scrape($url)),ENT_COMPAT,'UTF-8');
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  $diff_rows = array(1,2);
  $answers = array(
    'y' => 'stimmt zu',
    'n' => 'stimmt nicht zu',
    'a' => 'steht neutral dazu',
  );
  $j = 0;
  foreach ($diff_rows as $zebra) {
    $i = 0;
    $divs=$dom->find("div[class=tablebg{$zebra}]");
    foreach ($divs as $div) {
      $k = 2*$i+$j+1;
      $q_ar = explode("<span",trim($div->find("a",0)->innertext));
      $question_name = trim($q_ar[0]);
      $question_full = trim($div->find("span",0)->plaintext);
      $question = array(
         'name' => $question_name,
         'description' => $question_full,
         'land' => $row['land'],
         'year' => $row['year'],
         'number' => $k,
      );
      scraperwiki::save_sqlite(array('land','year','number'),$question,'question');
      $as = $div->find("a");
      array_shift($as);
      foreach ($as as $a) {
        foreach ($answers as $akey => $answer) {
          $text = $a->plaintext;
          if (strpos($text,$answer)) {
            $party = str_replace(' ' . $answer,'',$text);
            $vote = $akey;
          }
//echo $question_name . $question_full . $party . $vote; die();
        }
      $one_answer[] = array(
         'land' => $row['land'],
         'year' => $row['year'],
         'number' => $k,
         'party' => $party,
         'vote' => $vote,
      );  
      }
    $i++;
    }
  $j++;
  }

}
scraperwiki::save_sqlite(array('land','year','number','party'),$one_answer,'answer');

?>
<?php

//extract answers from Wahl-O-Mats
//need to be downloaded in advance (the completed tests)

//domain with downloaded files
$domain = "http://dev.kohovolit.eu/tmp/germany/";

$files = array(
array('land'=>'sl','file'=>'sl_1.html','year'=>'2012'),
array('land'=>'sl','file'=>'sl_2.html','year'=>'2012'),

array('land'=>'sh','file'=>'sh_1.html','year'=>'2012'),
array('land'=>'sh','file'=>'sh_2.html','year'=>'2012'),

array('land'=>'nw','file'=>'nw_1.html','year'=>'2012'),
array('land'=>'nw','file'=>'nw_2.html','year'=>'2012'),
array('land'=>'nw','file'=>'nw_3.html','year'=>'2012'),

array('land'=>'hh','file'=>'hh_1.html','year'=>'2011'),
array('land'=>'hh','file'=>'hh_2.html','year'=>'2011'),

array('land'=>'rp','file'=>'rp_1.html','year'=>'2011'),
array('land'=>'rp','file'=>'rp_2.html','year'=>'2011'),

array('land'=>'bw','file'=>'bw_1.html','year'=>'2011'),
array('land'=>'bw','file'=>'bw_2.html','year'=>'2011'),
array('land'=>'bw','file'=>'bw_3.html','year'=>'2011'),

array('land'=>'hb','file'=>'hb_1.html','year'=>'2011'),
array('land'=>'hb','file'=>'hb_2.html','year'=>'2011'),

array('land'=>'be','file'=>'be_1.html','year'=>'2011'),
array('land'=>'be','file'=>'be_2.html','year'=>'2011'),
array('land'=>'be','file'=>'be_3.html','year'=>'2011'),
);


require 'scraperwiki/simple_html_dom.php';

foreach ($files as $row) {
  $url = $domain . $row['file'];
  $html = html_entity_decode(iconv("ISO-8859-1","UTF-8//TRANSLIT",scraperwiki::scrape($url)),ENT_COMPAT,'UTF-8');
  //get dom
  $dom = new simple_html_dom();
  $dom->load($html);
  $diff_rows = array(1,2);
  $answers = array(
    'y' => 'stimmt zu',
    'n' => 'stimmt nicht zu',
    'a' => 'steht neutral dazu',
  );
  $j = 0;
  foreach ($diff_rows as $zebra) {
    $i = 0;
    $divs=$dom->find("div[class=tablebg{$zebra}]");
    foreach ($divs as $div) {
      $k = 2*$i+$j+1;
      $q_ar = explode("<span",trim($div->find("a",0)->innertext));
      $question_name = trim($q_ar[0]);
      $question_full = trim($div->find("span",0)->plaintext);
      $question = array(
         'name' => $question_name,
         'description' => $question_full,
         'land' => $row['land'],
         'year' => $row['year'],
         'number' => $k,
      );
      scraperwiki::save_sqlite(array('land','year','number'),$question,'question');
      $as = $div->find("a");
      array_shift($as);
      foreach ($as as $a) {
        foreach ($answers as $akey => $answer) {
          $text = $a->plaintext;
          if (strpos($text,$answer)) {
            $party = str_replace(' ' . $answer,'',$text);
            $vote = $akey;
          }
//echo $question_name . $question_full . $party . $vote; die();
        }
      $one_answer[] = array(
         'land' => $row['land'],
         'year' => $row['year'],
         'number' => $k,
         'party' => $party,
         'vote' => $vote,
      );  
      }
    $i++;
    }
  $j++;
  }

}
scraperwiki::save_sqlite(array('land','year','number','party'),$one_answer,'answer');

?>
