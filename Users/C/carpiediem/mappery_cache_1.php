<?php
require  'scraperwiki/simple_html_dom.php';
$start = 207;
$limit = 0; //this can enable, disable automatic runs
$count = $start;

for ($i=$start; $i<=$limit; $i+=100) {
  $gURL = scraperwiki::scrape("http://www.google.com/search?q=site%3Amappery.com&num=100&start=".$i);
  $gDOM = new simple_html_dom();
  $gDOM->load($gURL);

  foreach ($gDOM->find('a') as $a) {
    if (substr($a->href,7,8)=="webcache") {
      $rURL = scraperwiki::scrape($a->href);
      $rDOM = new simple_html_dom();
      $rDOM->load($rURL);

      $imgDiv = $rDOM->getElementById('mapPic');
      if (!$imgDiv) continue;
      $imgs = $imgDiv->find('img');
      if (count($imgs)==0) continue;

      $detDiv = $rDOM->getElementById('mapDetailInfo');
      if (!$detDiv) continue;
      $as = $detDiv->find('a');
      if (count($as)==0) continue;
      
      $ps = $rDOM->find('p');
      if (count($ps)==0) continue;

      $latDiv  = $rDOM->getElementById('geoLat');
      $lonDiv  = $rDOM->getElementById('geoLong');
      $zoomDiv = $rDOM->getElementById('zoomLevel');

      scraperwiki::save(array('id','title','imgURL','lat','lon','zoom','source','srcURL','desc'),
                        array('id'     => $count,
                              'title'  => $imgs[1]->title,
                              'imgURL' => $imgs[1]->src,
                              'lat'    => $latDiv->plaintext,
                              'lon'    => $lonDiv->plaintext,
                              'zoom'   => $zoomDiv->plaintext,
                              'source' => $as[0]->plaintext,
                              'srcURL' => $as[0]->href,
                              'desc'   => $ps[0]->plaintext
                             ));
      $count += 1;
    }
  }
}
?><?php
require  'scraperwiki/simple_html_dom.php';
$start = 207;
$limit = 0; //this can enable, disable automatic runs
$count = $start;

for ($i=$start; $i<=$limit; $i+=100) {
  $gURL = scraperwiki::scrape("http://www.google.com/search?q=site%3Amappery.com&num=100&start=".$i);
  $gDOM = new simple_html_dom();
  $gDOM->load($gURL);

  foreach ($gDOM->find('a') as $a) {
    if (substr($a->href,7,8)=="webcache") {
      $rURL = scraperwiki::scrape($a->href);
      $rDOM = new simple_html_dom();
      $rDOM->load($rURL);

      $imgDiv = $rDOM->getElementById('mapPic');
      if (!$imgDiv) continue;
      $imgs = $imgDiv->find('img');
      if (count($imgs)==0) continue;

      $detDiv = $rDOM->getElementById('mapDetailInfo');
      if (!$detDiv) continue;
      $as = $detDiv->find('a');
      if (count($as)==0) continue;
      
      $ps = $rDOM->find('p');
      if (count($ps)==0) continue;

      $latDiv  = $rDOM->getElementById('geoLat');
      $lonDiv  = $rDOM->getElementById('geoLong');
      $zoomDiv = $rDOM->getElementById('zoomLevel');

      scraperwiki::save(array('id','title','imgURL','lat','lon','zoom','source','srcURL','desc'),
                        array('id'     => $count,
                              'title'  => $imgs[1]->title,
                              'imgURL' => $imgs[1]->src,
                              'lat'    => $latDiv->plaintext,
                              'lon'    => $lonDiv->plaintext,
                              'zoom'   => $zoomDiv->plaintext,
                              'source' => $as[0]->plaintext,
                              'srcURL' => $as[0]->href,
                              'desc'   => $ps[0]->plaintext
                             ));
      $count += 1;
    }
  }
}
?>