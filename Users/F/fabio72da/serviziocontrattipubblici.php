<?php

# testcode: estrae campi _EVENTVALIDATION e _VIEWSTATE dalla pagina di ricerca

# $html_content = scraperwiki::scrape("https://www.serviziocontrattipubblici.it/ricerca/dett_ba_lav.aspx?id=75648");
# $html = str_get_html($html_content);

require 'scraperwiki/simple_html_dom.php';

function do_post_request($url, $data, $optional_headers = null)
{
  $params = array('http' => array(
              'method' => 'POST',
              'content' => $data
            ));
  if ($optional_headers !== null) {
    $params['http']['header'] = $optional_headers;
  }
  $ctx = stream_context_create($params);
  $fp = @fopen($url, 'rb', false, $ctx);
  if (!$fp) {
    throw new Exception("Problem with $url, $php_errormsg");
  }
  $response = @stream_get_contents($fp);
  if ($response === false) {
    throw new Exception("Problem reading data from $url, $php_errormsg");
  }
  return $response;
}

//$urlbase="https://www.serviziocontrattipubblici.it/ricerca/";
//$urllist="cerca_appalti.aspx";

$html_content = scraperwiki::scrape("https://www.serviziocontrattipubblici.it/ricerca/cerca_appalti.aspx");

$html = str_get_html($html_content);
$viewstate = $html->find("input[id=__VIEWSTATE]");
$eventval= $html->find("input[id=__EVENTVALIDATION]");

print "viewstate: ".$viewstate[0]->value."\n";
print "eventvalidation: ".$eventval[0]->value."\n";


?>
