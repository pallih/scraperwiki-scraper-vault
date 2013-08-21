<?php

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

function win2ascii($txt)    {    

return strtr($txt,
 "\xe1\xc1\xe0\xc0\xe2\xc2\xe4\xc4\xe3\xc3\xe5\xc5".
 "\xaa\xe7\xc7\xe9\xc9\xe8\xc8\xea\xca\xeb\xcb\xed".
 "\xcd\xec\xcc\xee\xce\xef\xcf\xf1\xd1\xf3\xd3\xf2".
 "\xd2\xf4\xd4\xf6\xd6\xf5\xd5\x8\xd8\xba\xf0\xfa\xda".
 "\xf9\xd9\xfb\xdb\xfc\xdc\xfd\xdd\xff\xe6\xc6\xdf\xf8",
 "aAaAaAaAaAaAacCeEeEeEeEiIiIiIiInNo".
 "OoOoOoOoOoOoouUuUuUuUyYyaAso");

}

// resetta le vars di status dello scraping
scraperwiki::save_var('current_prov', "");
scraperwiki::save_var('current_type', "");

//legge i valori di __VIEWSTATE e __EVENTVALIDATION per costruire la query
$html_content = scraperwiki::scrape("https://www.serviziocontrattipubblici.it/ricerca/cerca_appalti.aspx");

$html = str_get_html($html_content);
$viewstate = $html->find("input[id=__VIEWSTATE]");
$eventval= $html->find("input[id=__EVENTVALIDATION]");
// in viewstate[0]->value e $eventval[0]->value sono contenute le costanti nascoste per la query

$urlbase="https://www.serviziocontrattipubblici.it/ricerca/";
$urllist="cerca_appalti.aspx";
$regions = array(
'Abruzzo',
'Basilicata',
'Calabria',
'Campania',
'Emilia-Romagna',
'Friuli Venezia Giulia',
'Lazio',
'Liguria',
'Lombardia',
'Marche',
'Molise',
'Piemonte',
'Puglia',
'Sardegna',
'Sicilia',
'Toscana',
'Umbria',
'Veneto',

"Valle d'Aosta",
'Provincia autonoma di Bolzano',
'Provincia autonoma di Trento');


$provinces= array(
'AG',
'AL',
/*'AN',*/
'AO',
'AP',
'AQ',
'AR',
'AT',
'AV',
/*'BA',*/
'BG',
'BI',
'BL',
'BN',
'BO',
'BR',
'BS',
'BT',
'BZ',
/*'CA',*/
'CB',
'CE',
'CH',
'CI',
'CL',
'CN',
'CO',
'CR',
'CS',
'CT',
'CZ',
'EN',
'FC',
'FE',
'FG',
/*'FI',*/
'FM',
'FR',
'GE',
'GO',
'GR',
'IM',
'IS',
'KR',
'LC',
'LE',
'LI',
'LO',
'LT',
'LU',
'MB',
'MC',
'ME',
/*'MI',*/
'MN',
'MO',
'MS',
'MT',
'NA',
'NO',
'NU',
'OG',
'OR',
'OT',
'PA',
'PC',
'PD',
'PE',
'PG',
'PI',
'PN',
'PO',
'PR',
'PT',
'PU',
'PV',
'PZ',
'RA',
'RC',
'RE',
'RG',
'RI',
/*'RM',*/
'RN',
'RO',
'SA',
'SI',
'SO',
'SP',
'SR',
'SS',
'SV',
'TA',
'TE',
'TN',
/*'TO',*/
'TP',
'TR',
'TS',
'TV',
'UD',
'VA',
'VB',
'VC',
'VE',
'VI',
'VR',
'VS',
'VT'
/*'VV'*/
);


$provinces= array(
"AN",
"BA",
"CA",
"FI",
"MI",
"RM",
"TO",
"VV"
);


$tenders= array(/* 'agg' ,*/ 'ba');

#estremi entro i quali screperare
$lowerdate=date('01/07/2012');
$upperdate=date('d/m/Y');
#$upperdate=date('01/05/2012');


// ciclo sulle province
foreach ($provinces as $prov) {

// ciclo tra bandi (ba) ed esiti (agg)
foreach ($tenders as $tender) {

scraperwiki::save_var('current_prov', $prov);
scraperwiki::save_var('current_type', $tender);

//in partenza range da grattare coincide con tutto il dominio
$actualmax=$upperdate;
$actualmin=$lowerdate;

//in partenza range grattato è degenere
$scrapedmax=$lowerdate;
$scrapedmin=$lowerdate;

do {

post_query:

print ">> actualmin: " . $actualmin . " >> actualmax: " . $actualmax . "\n";
print ">> >> gara: " . $tender . " >> >> provincia: " . $prov. "\n";

$data = array ('__VIEWSTATE'=>$viewstate[0]->value,
             '__EVENTVALIDATION'=>$eventval[0]->value,
             'tipoappalto'=>$tender,
             'regioni'=>'- qualsiasi -',
             'province'=>$prov,
             'tipo_ente'=>'- qualsiasi -',
             'tipoapp'=>'1',
             'imp_fino_a'=>'',
             'cat_qual'=>'- qualsiasi -',
             'pubbl_dopo'=>$actualmin,
             'pubbl_prima'=>$actualmax
            );

$data = http_build_query($data);

$response = do_post_request($urlbase.$urllist, $data, $optional_headers = null);
$response =explode('<html',$response);

#$html_content = scraperwiki::scrape("https://www.serviziocontrattipubblici.it/ricerca/dett_ba_lav.aspx?id=75648");
$html = str_get_html('<html'.$response[1]);

//legge paragrafo con i risultati
$nores = $html->find("span#no_res",0);
$numres = $html->find("span#num_res",0);


//quanti risultati ?
if (isset($nores)) {
    print ">> No res >>".$nores->innertext."\n";
    goto next_item;
}
elseif (isset($numres) && stripos($numres->innertext,"ma sono stati visualizzati solo") !== false) {
    # differenza in giorni tra min e max
    $actmin_Ymd=new DateTime(implode(array_reverse(explode('/',$actualmin)),'-'));
    $actmax_Ymd=new DateTime(implode(array_reverse(explode('/',$actualmax)),'-'));
    $d_diff = intval(date_diff($actmin_Ymd,$actmax_Ymd)->format('%a') / 2 );
    $actualmax = date('d/m/Y' , strtotime("+".$d_diff." day", strtotime($actmin_Ymd->format('m/d/Y'))));
    print ">>Too res (d_diff:".$d_diff.")\n";
    goto post_query;
  }

print ">>OK res >>".$numres->innertext."\n";

$anchors = $html->find("a[href*=dett_".$tender."_lav.aspx]");

#ciclo sulle schede bando presenti nella lista
foreach ($anchors as $a) {

$sleeping=rand(3,6);
print ">>".$tender."+".$prov." >> sleep ".$sleeping."s >> a->href:" . $a->href . "\n";
$slept=sleep($sleeping);

$idarray=explode('?id=',$a->href);
#print ">>id[1]:" . $idarray[1]."\n";
#$idnum=intval($id[1]);

$id=$idarray[1];


#$html_content = scraperwiki::scrape("https://www.serviziocontrattipubblici.it/ricerca/dett_ba_lav.aspx?id=75648");
$html_content = scraperwiki::scrape("https://www.serviziocontrattipubblici.it/ricerca/".$a->href);

$html = str_get_html($html_content);


$stazapp = $html->find("span#lbl_denominaz",0);
$stazapp_cfpiva= $html->find("span#lbl_cf_piva",0);
$stazapp_ufficio= $html->find("span#lbl_ufficio",0);
$tipo_settore = $html->find("span#tipo_settore",0);
$infr_strat = $html->find("span#infr_strat",0);
$tipo_bando = $html->find("span#tipo_realizz",0);
$contr_gen = $html->find("span#contr_gen",0);
$oggetto = $html->find("span#oggetto",0);
$lotti = $html->find("span#lotti",0);
$num_lotto = $html->find("span#num_lotto",0);
$cpv1 = $html->find("span#desccpv1",0);
$cpv2 = $html->find("span#desccpv2",0);
$cpv3 = $html->find("span#desccpv3",0);
$tipo_interv = $html->find("span#tipo_interv",0);
$cup = $html->find("span#cup",0);
$luogo = $html->find("span#desc_istat",0);
$imp_base = $html->find("span#imp_base",0);
$sicur= $html->find("span#lbl_sicurez",0);
$imp_sicur = $html->find("span#imp_sicurez",0);
$imp_contr = $html->find("span#imp_contratt",0);
$pct_rib = $html->find("span#perc_rib_asta",0);
$proc_agg = $html->find("span#proc_agg",0);
$data_guce = $html->find("span#data_guce",0);
$data_guri = $html->find("span#data_guri",0);
$data_albo = $html->find("span#data_albo",0);
$prof_comm = $html->find("span#prof_comm",0);
$n_quot_naz = $html->find("span#n_quot_naz",0);
$n_quot_reg = $html->find("span#n_quot_reg",0);
$data_guce_agg = $html->find("span#data_guce_agg",0);
$data_scadenza = $html->find("span#data_scadenza",0);
$imp_corpo = $html->find("span#imp_corpo",0);
$imp_misura = $html->find("span#imp_misura",0);
$imp_corpo_mis = $html->find("span#imp_corpo_mis",0);
$cat_prev = $html->find("span#cat_prev",0);
$imp_cat_prev = $html->find("span#imp_cat_prev",0);
$cat_sc1 = $html->find("span#cat_scorp1",0);
$imp_cat_sc1 = $html->find("span#imp_cat_scorp1",0);
$cat_sc2 = $html->find("span#cat_scorp2",0);
$imp_cat_sc2 = $html->find("span#imp_cat_scorp2",0);
$cat_sc3 = $html->find("span#cat_scorp3",0);
$imp_cat_sc3 = $html->find("span#imp_cat_scorp3",0);
$cat_sc4 = $html->find("span#cat_scorp4",0);
$imp_cat_sc4 = $html->find("span#imp_cat_scorp4",0);
$cat_sc5 = $html->find("span#cat_scorp5",0);
$imp_cat_sc5 = $html->find("span#imp_cat_scorp5",0);
$cat_sc6 = $html->find("span#cat_scorp6",0);
$imp_cat_sc6 = $html->find("span#imp_cat_scorp6",0);
$cat_sc7 = $html->find("span#cat_scorp7",0);
$imp_cat_sc7 = $html->find("span#imp_cat_scorp7",0);
$data_agg = $html->find("span#data_agg",0);
$n_imp_rich = $html->find("span#n_imp_rich",0);
$n_imp_inv = $html->find("span#n_imp_inv",0);
$n_imp_off = $html->find("span#n_imp_off",0);
$n_imp_amm = $html->find("span#n_imp_amm",0);
$lista_agg = $html->find("span#list_az",0);
$tipo_agg = $html->find("span#tipo_agg",0);
$durata = $html->find("span#n_gg_termine",0);
$data_fine_lav = $html->find("span#data_fine_lav",0);
$note = $html->find("span#note",0);
$url_esito = $html->find("span#down_all",0);


/*
$cpv = explode("-",$cpv1->innertext);
$luogo= explode("-",$luogo->innertext);
*/


$gara = array(  "load_date"=>date("Ymd"),
                "load_time"=>date("H:m:s"),
                "id"=>$id,                
                "stazapp"=>isset($stazapp)?utf8_encode(win2ascii($stazapp->innertext)):"",
                "stazapp_cfpiva"=>isset($stazapp_cfpiva)?$stazapp_cfpiva->innertext:"",
                "stazapp_ufficio"=>isset($stazapp_ufficio)?utf8_encode(win2ascii($stazapp_ufficio->innertext)):"",
                "tipo_settore"=>isset($tipo_settore)?$tipo_settore->innertext:"",
                "infr_strat"=>isset($infr_strat)?utf8_encode(win2ascii($infr_strat->innertext)):"",
                "tipo_bando"=>isset($tipo_bando)?$tipo_bando->innertext:"",
                "stato_bando"=>$tender,
                "contr_gen"=>isset($contr_gen)?utf8_encode(win2ascii($contr_gen->innertext)):"",
                "oggetto"=>isset($oggetto)?utf8_encode(win2ascii($oggetto->innertext)):"",
                "lotti"=>isset($lotti)?utf8_encode(win2ascii($lotti->innertext)):"",
                "num_lotti"=>isset($num_lotti)?$num_lotti->innertext:"",
                "cpv1"=>isset($cpv1)?$cpv1->innertext:"",
                "cpv2"=>isset($cpv2)?$cpv2->innertext:"",
                "cpv3"=>isset($cpv3)?$cpv3->innertext:"",
                "tipo_interv"=>isset($tipo_interv)?$tipo_interv->innertext:"",
                "cup"=>isset($cup)?$cup->innertext:"",
                "luogo"=>isset($luogo)?utf8_encode(win2ascii($luogo->innertext)):"",
                "provincia"=>$prov,
                "imp_base"=>isset($imp_base)?$imp_base->innertext:"",
                "sicur"=>isset($sicur)?utf8_encode(win2ascii($sicur->innertext)):"",
                "imp_sicur"=>isset($imp_sicur)?$imp_sicur->innertext:"",
                "imp_contr"=>isset($imp_contr)?$imp_contr->innertext:"",
                "pct_rib"=>isset($pct_rib)?$pct_rib->innertext:"",
                "proc_agg"=>isset($proc_agg)?utf8_encode(win2ascii($proc_agg->innertext)):"",
                "data_guce"=>isset($data_guce)?$data_guce->innertext:"",
                "data_guri"=>isset($data_guri)?$data_guri->innertext:"",
                "data_albo"=>isset($data_albo)?$data_albo->innertext:"",
                "prof_comm"=>isset($prof_comm)?$prof_comm->innertext:"",
                "n_quot_naz"=>isset($n_quot_naz)?$n_quot_naz->innertext:"",
                "n_quot_reg"=>isset($n_quot_reg)?$n_quot_reg->innertext:"",
                "data_guce_agg"=>isset($data_guce_agg)?$data_guce_agg->innertext:"",
                "data_scadenza"=>isset($data_scadenza)?$data_scadenza->innertext:"",
                "imp_corpo"=>isset($imp_corpo)?$imp_corpo->innertext:"",
                "imp_misura"=>isset($imp_misura)?$imp_misura->innertext:"",
                "imp_corpo_mis"=>isset($imp_corpo_mis)?$imp_corpo_mis->innertext:"",
                "cat_prev"=>isset($cat_prev)?$cat_prev->innertext:"",
                "imp_cat_prev"=>isset($imp_cat_prev)?$imp_cat_prev->innertext:"",
                "cat_sc1"=>isset($cat_sc1)?$cat_sc1->innertext:"",
                "imp_cat_sc1"=>isset($imp_cat_sc1)?$imp_cat_sc1->innertext:"",
                "cat_sc2"=>isset($cat_sc2)?$cat_sc2->innertext:"",
                "imp_cat_sc2"=>isset($imp_cat_sc2)?$imp_cat_sc2->innertext:"",
                "cat_sc3"=>isset($cat_sc3)?$cat_sc3->innertext:"",
                "imp_cat_sc3"=>isset($imp_cat_sc3)?$imp_cat_sc3->innertext:"",
                "cat_sc4"=>isset($cat_sc4)?$cat_sc4->innertext:"",
                "imp_cat_sc4"=>isset($imp_cat_sc4)?$imp_cat_sc4->innertext:"",
                "cat_sc5"=>isset($cat_sc5)?$cat_sc5->innertext:"",
                "imp_cat_sc5"=>isset($imp_cat_sc5)?$imp_cat_sc5->innertext:"",
                "cat_sc6"=>isset($cat_sc6)?$cat_sc6->innertext:"",
                "imp_cat_sc6"=>isset($imp_cat_sc6)?$imp_cat_sc6->innertext:"",
                "cat_sc7"=>isset($cat_sc7)?$cat_sc7->innertext:"",
                "imp_cat_sc7"=>isset($imp_cat_sc7)?$imp_cat_sc7->innertext:"",
                "data_agg"=>isset($data_agg)?$data_agg->innertext:"",
                "n_imp_rich"=>isset($n_imp_rich)?$n_imp_rich->innertext:"",
                "n_imp_inv"=>isset($n_imp_inv)?$n_imp_inv->innertext:"",
                "n_imp_off"=>isset($n_imp_off)?$n_imp_off->innertext:"",
                "n_imp_amm"=>isset($n_imp_amm)?$n_imp_amm->innertext:"",
                "lista_agg"=>isset($lista_agg)?utf8_encode(win2ascii($lista_agg->innertext)):"",
                "tipo_agg"=>isset($tipo_agg)?utf8_encode(win2ascii($tipo_agg->innertext)):"",
                "durata"=>isset($durata)?$durata->innertext:"",
                "data_fine_lav"=>isset($data_fine_lav)?$data_fine_lav->innertext:"",
                "note"=>isset($note)?utf8_encode(win2ascii($note->innertext)):"",
                "url_esito"=>isset($url_esito)?$url_esito->innertext:""
            );

print ">>".$tender."+".$prov.">>id:".$gara["id"].">>CUP:".$gara["cup"].">>oggetto:".$gara["oggetto"]."\n";

scraperwiki::save_sqlite(array("id"), $gara);
print ">> scheda archiviata\n";

 }

next_item:

#aggiorna gli estremi del range già scraperato
$scrapedmax = max($scrapedmax,$actualmax);
$scrapedmin = min($scrapedmin,$actualmin);

#imposta i nuovi estremi di ricerca
$actualmin=$actualmax;
$actualmax=$upperdate;

print ">>endloop>>scrapedmin:".$scrapedmin.">>scrapedmax:".$scrapedmax."\n";
print ">>endloop>>actualmin:".$actualmin.">>actualmax:".$actualmax."\n";
print ">>endloop>>lowerdate:".$lowerdate.">>upperdate:".$upperdate."\n";

} while ($scrapedmin != $lowerdate || $scrapedmax != $upperdate); //loop range

} //loop ba-agg
} //loop province

// resetta le vars di status dello scraping
scraperwiki::save_var('current_prov', "");
scraperwiki::save_var('current_type', "");


?>
