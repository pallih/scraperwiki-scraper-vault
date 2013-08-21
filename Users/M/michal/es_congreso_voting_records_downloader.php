<?php

# Download XMls - voting records from Spain's Congreso

require 'scraperwiki/simple_html_dom.php';

//temp
//first voting records are from 2012
//scraperwiki::save_var('last_date','2012-01-01');
//scraperwiki::save_var('last_date','2012-05-23');


$date = new DateTime(scraperwiki::get_var('last_date'));
$today = new DateTime();

while ($date < $today) {

    //echo $date->format('U = Y-m-d H:i:s') . "\n";

    $url = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Actualidad/Votaciones?fechaSeleccionada=" . $date->format('Y/m/d');
    $html = scraperwiki::scrape($url);
    $dom = new simple_html_dom();
    $dom->load($html);

    $right_date = compare_dates($dom,$date);
    //if current date <= last date of votes, do; otherwise do nothing, no new votes
    if ($right_date) {
        $url = "http://www.congreso.es/portal/page/portal/Congreso/Congreso/Actualidad/Votaciones?fechaSeleccionada=" . $right_date->format('Y/m/d');
     
        $html0 = scraperwiki::scrape($url);
        $dom = new simple_html_dom();
echo strlen($html0);  
        //problem with scraperwiki with long page:
        if (strlen($html0) > 200000) {
            $strip = get_first_string($html0,'<DIV class="votacionesEncabezado">','mostrarCapa( "capaLegislaturas", "true" );');
            $htmls = returnSubstrings($strip,'<TABLE>','</TABLE>');
            foreach ($htmls as $key=>$html) {
                $htmls[$key] = '<html><body><div class="votacionesResultado"><table>' . $htmls[$key] . '</table></div></body></html>';
            }
        } else {
            $htmls = array($html);
        }
       foreach ($htmls as $key => $html) {
        $dom->load($html);

        $divs = $dom->find('div[class=votacionesResultado]');    
        foreach ($divs as $div) {
            $as = $div->find('a');
            if (count($as) > 1) {
                $link =  $div->find('a',1)->href;
                $td_ar = explode("<br>",$div->find('td',0));
                $si_ar = explode(':',$td_ar[0]);
                $si = trim($si_ar[1]);
                $no_ar = explode(':',$td_ar[1]);
                $no = trim($no_ar[1]);
                $abst_ar = explode(':',$td_ar[2]);
                $abst = trim($abst_ar[1]);
                $number = get_first_string($div->innertext,'votacion=','&');
                $url = "http://www.congreso.es" . $link;
                $xml = str_replace("ISO-8859-1","UTF-8",iconv("ISO-8859-1","UTF-8",scraperwiki::scrape($url)));
                $data = array(
                    'date' => $right_date->format('Y-m-d'),
                    'number' => $number,
                    'yes' => $si,
                    'no' => $no,
                    'abstain' => $abst,
                    'link' => $link,
                    'xml' => $xml
                );   
                scraperwiki::save_sqlite(array('date','number'),$data,'division');
            }    
        }
       }  // /foreach $htmls
    } 
    $date = $right_date->modify('+1 day') ;
    scraperwiki::save_var('last_date',$date->format('Y-m-d'));
}

/*print_r($data);

if (isset($data)) {
    foreach ($data as $row) {
echo '**';
        $url = "http://www.congreso.es" . $row['link'];
        $row['xml'] = scraperwiki::scrape($url);
        scraperwiki::save_sqlite(array('date','number'),$row,'division');
    }
}*/



function compare_dates($dom,$date_address) {
    if ((strpos($dom->plaintext,'No hay votaciones') > 0) or  (strpos($dom->plaintext,'El listener ha devuelto el siguiente mensaje:') > 0)) {
        return false;
    } else {
      $td_ar = explode(':',$dom->find("div[class=tituloVot]",0)->find('td',1)->plaintext);
      $date_website = new DateTime(convert_date(trim($td_ar[1]),"to iso"));
    
      if ($date_website == $date_address)
        return $date_address;
      else
        return $date_website;
    }
}

/**

* converts dates formats between Spanish and ISO (ISO 8601)

* @return converted date

* examples:

* convert_date('2010-02-15','to Spain')

*    returns '15/2/2010;

* convert_date('15/2/2010')

*    returns '2010-02-15'

*/

function convert_date($in,$way = 'to iso') {
    $in = str_replace('&nbsp;','',$in);
    if ($way == 'to iso') {
    $ar = explode('/',$in);
    $out = date('Y-m-d',mktime(0,0,0,$ar[1],$ar[0],$ar[2]));
    } else {
    $ar = explode('-',$in);
    $out = date('j/n/Y',mktime(0,0,0,$ar[1],$ar[2],$ar[0]));
    }
    return $out;
}

/**

* finds substrings between opening and closing markers

* @return result array of the substrings

*/

function returnSubstrings($text, $openingMarker, $closingMarker) {

$openingMarkerLength = strlen($openingMarker);

$closingMarkerLength = strlen($closingMarker);

$result = array();

$position = 0;

while (($position = strpos($text, $openingMarker, $position)) !== false) {

$position += $openingMarkerLength;

if (($closingMarkerPosition = strpos($text, $closingMarker, $position)) !== false) {

$result[] = substr($text, $position, $closingMarkerPosition - $position);

$position = $closingMarkerPosition + $closingMarkerLength;

}

}

return $result;

}


/**

* finds 1st substring between opening and closing markers

* @return result 1st substring

*/

function get_first_string ($text,$openingMarker, $closingMarker) {

$out_ar = returnSubstrings($text, $openingMarker, $closingMarker);

$out = $out_ar[0];

return($out);

}


?>
