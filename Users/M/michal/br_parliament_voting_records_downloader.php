<?php

//source: http://www.camara.gov.br/internet/deputado/RelVotacoes.asp?nuLegislatura=51&nuMatricula=333&dtInicio=01/01/1900&dtFim=26/10/2011
//problems: nuLegislatura: 51, 52, 53, 54 ok; 49, 50 without names; must be set 'useragent'

//note: there was a strange error if saving only part of the html (using $dom) - it worked ok for leg=49, but it downloaded only 1 page for leg=50 and then stopped

$last_leg = scraperwiki::get_var('last_leg',0); //last legislature already in db
$last_id = scraperwiki::get_var('last_id',0); //last id already in db
//$last_leg = 50; //temp
$curl_options = array(
  array(CURLOPT_USERAGENT,'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'),
);

require 'scraperwiki/simple_html_dom.php'; 

$current_legislatura = ceil((date('Y') - 1798)/4);

for ($leg = 49; $leg <= $current_legislatura; $leg++) {
  if ($leg < $last_leg) continue;

  scraperwiki::save_var('last_leg',$leg);

  for ($id = 1; $id <= 1000; $id++) {
//echo '**'.$id.'**';
    if (($leg == $last_leg) and ($id <= $last_id)) continue;

    $url = "http://www.camara.gov.br/internet/deputado/RelVotacoes.asp?nuLegislatura={$leg}&nuMatricula={$id}&dtInicio=01/01/1900&dtFim=01/01/2100";
    $html = grabber($url,$curl_options);

    //valid html?
    if (strpos($html, 'Nenhuma informação encontrada.') > 0) continue;

    //correct utf-8
    $w = "([\s\S]){1,3}"; //ungreedy wildcard
    preg_match("/C{$w}digo/",$html,$matches);
    $html = str_replace($matches[1],'ó',$html);
//print_r($matches);die();
//echo '##'.$id.'##';

    //get dom
    //$dom = null;
    //$dom = new simple_html_dom();
    //$dom->load($html);
    //save html
    //$div = $dom->find('div[id=portal-column-content]',0);
//echo $div->outertext;die();
    $data['term'] = $leg;
    $data['mp_id'] = $id;
//echo '--'.$id.'--'; 
    $data['html'] = $html;//$div->outertext;
//echo '++'.$id.'++'; 
    /*$data = array(
      'term' => $leg,
      'mp_id' => $id,
      'html' => $div->outertext,
    );*/
//print_r($data);
    scraperwiki::save_sqlite(array('term', 'mp_id'),$data);

    scraperwiki::save_var('last_id',$id);
  //echo $last_leg.$last_id.$leg.$id;
  }
  scraperwiki::save_var('last_id',0);
}
scraperwiki::save_var('last_id',0);
scraperwiki::save_var('last_leg',0);

/**
* curl downloader, with possible options
* @return html
* example:
* grabber('http://example.com',array(CURLOPT_TIMEOUT,180));
*/
function grabber($url,$options = array())
{
    $ch = curl_init ();
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_URL, $url);
    curl_setopt ($ch, CURLOPT_TIMEOUT, 120);
    if (count($options) > 0) {
        foreach($options as $option) {
            curl_setopt ($ch, $option[0], $option[1]);
        }
    }
    return curl_exec($ch);
    //curl_close ($ch);
}

?>
<?php

//source: http://www.camara.gov.br/internet/deputado/RelVotacoes.asp?nuLegislatura=51&nuMatricula=333&dtInicio=01/01/1900&dtFim=26/10/2011
//problems: nuLegislatura: 51, 52, 53, 54 ok; 49, 50 without names; must be set 'useragent'

//note: there was a strange error if saving only part of the html (using $dom) - it worked ok for leg=49, but it downloaded only 1 page for leg=50 and then stopped

$last_leg = scraperwiki::get_var('last_leg',0); //last legislature already in db
$last_id = scraperwiki::get_var('last_id',0); //last id already in db
//$last_leg = 50; //temp
$curl_options = array(
  array(CURLOPT_USERAGENT,'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'),
);

require 'scraperwiki/simple_html_dom.php'; 

$current_legislatura = ceil((date('Y') - 1798)/4);

for ($leg = 49; $leg <= $current_legislatura; $leg++) {
  if ($leg < $last_leg) continue;

  scraperwiki::save_var('last_leg',$leg);

  for ($id = 1; $id <= 1000; $id++) {
//echo '**'.$id.'**';
    if (($leg == $last_leg) and ($id <= $last_id)) continue;

    $url = "http://www.camara.gov.br/internet/deputado/RelVotacoes.asp?nuLegislatura={$leg}&nuMatricula={$id}&dtInicio=01/01/1900&dtFim=01/01/2100";
    $html = grabber($url,$curl_options);

    //valid html?
    if (strpos($html, 'Nenhuma informação encontrada.') > 0) continue;

    //correct utf-8
    $w = "([\s\S]){1,3}"; //ungreedy wildcard
    preg_match("/C{$w}digo/",$html,$matches);
    $html = str_replace($matches[1],'ó',$html);
//print_r($matches);die();
//echo '##'.$id.'##';

    //get dom
    //$dom = null;
    //$dom = new simple_html_dom();
    //$dom->load($html);
    //save html
    //$div = $dom->find('div[id=portal-column-content]',0);
//echo $div->outertext;die();
    $data['term'] = $leg;
    $data['mp_id'] = $id;
//echo '--'.$id.'--'; 
    $data['html'] = $html;//$div->outertext;
//echo '++'.$id.'++'; 
    /*$data = array(
      'term' => $leg,
      'mp_id' => $id,
      'html' => $div->outertext,
    );*/
//print_r($data);
    scraperwiki::save_sqlite(array('term', 'mp_id'),$data);

    scraperwiki::save_var('last_id',$id);
  //echo $last_leg.$last_id.$leg.$id;
  }
  scraperwiki::save_var('last_id',0);
}
scraperwiki::save_var('last_id',0);
scraperwiki::save_var('last_leg',0);

/**
* curl downloader, with possible options
* @return html
* example:
* grabber('http://example.com',array(CURLOPT_TIMEOUT,180));
*/
function grabber($url,$options = array())
{
    $ch = curl_init ();
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_URL, $url);
    curl_setopt ($ch, CURLOPT_TIMEOUT, 120);
    if (count($options) > 0) {
        foreach($options as $option) {
            curl_setopt ($ch, $option[0], $option[1]);
        }
    }
    return curl_exec($ch);
    //curl_close ($ch);
}

?>
<?php

//source: http://www.camara.gov.br/internet/deputado/RelVotacoes.asp?nuLegislatura=51&nuMatricula=333&dtInicio=01/01/1900&dtFim=26/10/2011
//problems: nuLegislatura: 51, 52, 53, 54 ok; 49, 50 without names; must be set 'useragent'

//note: there was a strange error if saving only part of the html (using $dom) - it worked ok for leg=49, but it downloaded only 1 page for leg=50 and then stopped

$last_leg = scraperwiki::get_var('last_leg',0); //last legislature already in db
$last_id = scraperwiki::get_var('last_id',0); //last id already in db
//$last_leg = 50; //temp
$curl_options = array(
  array(CURLOPT_USERAGENT,'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'),
);

require 'scraperwiki/simple_html_dom.php'; 

$current_legislatura = ceil((date('Y') - 1798)/4);

for ($leg = 49; $leg <= $current_legislatura; $leg++) {
  if ($leg < $last_leg) continue;

  scraperwiki::save_var('last_leg',$leg);

  for ($id = 1; $id <= 1000; $id++) {
//echo '**'.$id.'**';
    if (($leg == $last_leg) and ($id <= $last_id)) continue;

    $url = "http://www.camara.gov.br/internet/deputado/RelVotacoes.asp?nuLegislatura={$leg}&nuMatricula={$id}&dtInicio=01/01/1900&dtFim=01/01/2100";
    $html = grabber($url,$curl_options);

    //valid html?
    if (strpos($html, 'Nenhuma informação encontrada.') > 0) continue;

    //correct utf-8
    $w = "([\s\S]){1,3}"; //ungreedy wildcard
    preg_match("/C{$w}digo/",$html,$matches);
    $html = str_replace($matches[1],'ó',$html);
//print_r($matches);die();
//echo '##'.$id.'##';

    //get dom
    //$dom = null;
    //$dom = new simple_html_dom();
    //$dom->load($html);
    //save html
    //$div = $dom->find('div[id=portal-column-content]',0);
//echo $div->outertext;die();
    $data['term'] = $leg;
    $data['mp_id'] = $id;
//echo '--'.$id.'--'; 
    $data['html'] = $html;//$div->outertext;
//echo '++'.$id.'++'; 
    /*$data = array(
      'term' => $leg,
      'mp_id' => $id,
      'html' => $div->outertext,
    );*/
//print_r($data);
    scraperwiki::save_sqlite(array('term', 'mp_id'),$data);

    scraperwiki::save_var('last_id',$id);
  //echo $last_leg.$last_id.$leg.$id;
  }
  scraperwiki::save_var('last_id',0);
}
scraperwiki::save_var('last_id',0);
scraperwiki::save_var('last_leg',0);

/**
* curl downloader, with possible options
* @return html
* example:
* grabber('http://example.com',array(CURLOPT_TIMEOUT,180));
*/
function grabber($url,$options = array())
{
    $ch = curl_init ();
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_URL, $url);
    curl_setopt ($ch, CURLOPT_TIMEOUT, 120);
    if (count($options) > 0) {
        foreach($options as $option) {
            curl_setopt ($ch, $option[0], $option[1]);
        }
    }
    return curl_exec($ch);
    //curl_close ($ch);
}

?>
<?php

//source: http://www.camara.gov.br/internet/deputado/RelVotacoes.asp?nuLegislatura=51&nuMatricula=333&dtInicio=01/01/1900&dtFim=26/10/2011
//problems: nuLegislatura: 51, 52, 53, 54 ok; 49, 50 without names; must be set 'useragent'

//note: there was a strange error if saving only part of the html (using $dom) - it worked ok for leg=49, but it downloaded only 1 page for leg=50 and then stopped

$last_leg = scraperwiki::get_var('last_leg',0); //last legislature already in db
$last_id = scraperwiki::get_var('last_id',0); //last id already in db
//$last_leg = 50; //temp
$curl_options = array(
  array(CURLOPT_USERAGENT,'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'),
);

require 'scraperwiki/simple_html_dom.php'; 

$current_legislatura = ceil((date('Y') - 1798)/4);

for ($leg = 49; $leg <= $current_legislatura; $leg++) {
  if ($leg < $last_leg) continue;

  scraperwiki::save_var('last_leg',$leg);

  for ($id = 1; $id <= 1000; $id++) {
//echo '**'.$id.'**';
    if (($leg == $last_leg) and ($id <= $last_id)) continue;

    $url = "http://www.camara.gov.br/internet/deputado/RelVotacoes.asp?nuLegislatura={$leg}&nuMatricula={$id}&dtInicio=01/01/1900&dtFim=01/01/2100";
    $html = grabber($url,$curl_options);

    //valid html?
    if (strpos($html, 'Nenhuma informação encontrada.') > 0) continue;

    //correct utf-8
    $w = "([\s\S]){1,3}"; //ungreedy wildcard
    preg_match("/C{$w}digo/",$html,$matches);
    $html = str_replace($matches[1],'ó',$html);
//print_r($matches);die();
//echo '##'.$id.'##';

    //get dom
    //$dom = null;
    //$dom = new simple_html_dom();
    //$dom->load($html);
    //save html
    //$div = $dom->find('div[id=portal-column-content]',0);
//echo $div->outertext;die();
    $data['term'] = $leg;
    $data['mp_id'] = $id;
//echo '--'.$id.'--'; 
    $data['html'] = $html;//$div->outertext;
//echo '++'.$id.'++'; 
    /*$data = array(
      'term' => $leg,
      'mp_id' => $id,
      'html' => $div->outertext,
    );*/
//print_r($data);
    scraperwiki::save_sqlite(array('term', 'mp_id'),$data);

    scraperwiki::save_var('last_id',$id);
  //echo $last_leg.$last_id.$leg.$id;
  }
  scraperwiki::save_var('last_id',0);
}
scraperwiki::save_var('last_id',0);
scraperwiki::save_var('last_leg',0);

/**
* curl downloader, with possible options
* @return html
* example:
* grabber('http://example.com',array(CURLOPT_TIMEOUT,180));
*/
function grabber($url,$options = array())
{
    $ch = curl_init ();
    curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt ($ch, CURLOPT_URL, $url);
    curl_setopt ($ch, CURLOPT_TIMEOUT, 120);
    if (count($options) > 0) {
        foreach($options as $option) {
            curl_setopt ($ch, $option[0], $option[1]);
        }
    }
    return curl_exec($ch);
    //curl_close ($ch);
}

?>
