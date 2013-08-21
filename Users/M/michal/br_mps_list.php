<?php

//http://www.camara.gov.br/internet/deputado/DepNovos_Lista.asp?Legislatura=41&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=QQ&forma=lista&nome=&ordem=nome&origem=

$curl_options = array(
  array(CURLOPT_USERAGENT,'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'),
);

require 'scraperwiki/simple_html_dom.php';

for ($term = 41; $term <= 54; $term++) {
  $url = "http://www.camara.gov.br/internet/deputado/DepNovos_Lista.asp?Legislatura={$term}&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=QQ&forma=lista&nome=&ordem=nome&origem=";
  $html = grabber($url,$curl_options);

  $dom = new simple_html_dom();
  $dom->load($html);
  $lis = $dom->find('div[id=content]',0)->find('li');
  foreach ($lis as $li) {
    $plain = trim($li->plaintext);
    $pa = explode('-',$plain);
    $na = explode('/',end($pa));
    preg_match('/pk=([0-9]{1,})/',$li->find('a',0)->href,$matches);
    $data[] = array(
        'name' => trim($pa[0]),
        'party' => trim($na[0]),
        'state' => trim($na[1]),
        'mp_pk_id' => $matches[1],
        'term' => $term,
    );
  }
}
scraperwiki::save_sqlite(array('term','mp_pk_id'),$data);

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

//http://www.camara.gov.br/internet/deputado/DepNovos_Lista.asp?Legislatura=41&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=QQ&forma=lista&nome=&ordem=nome&origem=

$curl_options = array(
  array(CURLOPT_USERAGENT,'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'),
);

require 'scraperwiki/simple_html_dom.php';

for ($term = 41; $term <= 54; $term++) {
  $url = "http://www.camara.gov.br/internet/deputado/DepNovos_Lista.asp?Legislatura={$term}&Partido=QQ&SX=QQ&Todos=None&UF=QQ&condic=QQ&forma=lista&nome=&ordem=nome&origem=";
  $html = grabber($url,$curl_options);

  $dom = new simple_html_dom();
  $dom->load($html);
  $lis = $dom->find('div[id=content]',0)->find('li');
  foreach ($lis as $li) {
    $plain = trim($li->plaintext);
    $pa = explode('-',$plain);
    $na = explode('/',end($pa));
    preg_match('/pk=([0-9]{1,})/',$li->find('a',0)->href,$matches);
    $data[] = array(
        'name' => trim($pa[0]),
        'party' => trim($na[0]),
        'state' => trim($na[1]),
        'mp_pk_id' => $matches[1],
        'term' => $term,
    );
  }
}
scraperwiki::save_sqlite(array('term','mp_pk_id'),$data);

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
