<?php

# Blank PHP
require 'scraperwiki/simple_html_dom.php';  

function campi()
{
    return array("lbOrdinanza","lbPresentata","lbEsito","lbCodice","lbPermesso","lbTipoContributo","lbIntervento","lbFoglio","lbNumero","lbSubalterno","lbInizioLavori","lbFineLavori","lbDefinitivoRitiro","lbContributo");
}


/*
scraperwiki::sqliteexecute("alter table pratica add column 'lbContributo' DECIMAL");
scraperwiki::sqliteexecute("drop table fabbricati_aq");
scraperwiki::sqliteexecute("drop table fabbricati_has_pratiche");
scraperwiki::sqliteexecute("create table fabbricato (id int PRIMARY KEY, 'richiesto' DECIMAL, 'rilasciato' DECIMAL, 'created_at' datetime, 'updated_at' datetime)");
scraperwiki::sqliteexecute("create table fabbricato_has_pratica (id INTEGER PRIMARY KEY AUTOINCREMENT, 'fabbricato_id' int, 'pratica_id' text, 'created_at' datetime, 'updated_at' datetime)");
scraperwiki::sqliteexecute("create table soprintendenza ('aggregato' text PRIMARY KEY, 'denominazione' text, 'foglio' int, 'numero' text, 'importo' DECIMAL, 'created_at' datetime, 'updated_at' datetime)");
scraperwiki::sqliteexecute("ALTER TABLE soprintendenza add column sit_id int");
scraperwiki::sqliteexecute("delete from fabbricato where created_at like '2013-04-17%'");
scraperwiki::sqliteexecute("delete from pratica where created_at like '2013-04-17%'");
scraperwiki::sqliteexecute("delete from fabbricato_has_pratica where fabbricato_id=3923 and pratica_id='AQ-MBAC-21307' ");
scraperwiki::sqlitecommit();
*/



$date=date('Y-m-d H:i:s');


//Controllo e import dei nuovi fabbricati
$max=scraperwiki::select ("id from fabbricato order by id desc limit 1");
$start= ($max[0]['id']) +1;
echo "=====".$start."=======\n";
for ($i=$start; $i<=10000; $i++)
{
    $cn=scraperwiki::select ("count(*) as c from fabbricato where id=".$i);
    if ($cn[0]['c']==0)
    {
        echo $uri="http://laquila.geoportal.it/webgis/tooltip/richiesti.aspx?IdFabb=".$i;
        echo "\n";
        $pratiche=array();
        $euro=array();
        $ch=curl_init($uri);
        curl_setopt($ch,CURLOPT_HEADER,0);
        curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, 
         array(
         'Host: laquila.geoportal.it' ,
         'Connection: keep-alive' ,
         'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' ,
         'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:19.0) Gecko/20100101 Firefox/19.0' ,
         'Accept-Encoding: gzip, deflate' ,
         'Cookie: ASP.NET_SessionId=lpx4ql52v15h4ssr1fqp2q3b; digi_gis=Sessione=599398ae-9a25-11e2-8000-00155d036001_en_MTI3LjAuMC4x0AF20AF10AF0&Utente=laquila&Mappa=Ricostruzione51586d2796293; submenuheader=0c; PHPSESSID=b3d70ed8-996a-11e2-8000-00155d036001-en-MTI3LjAuMC4x0AF20AF10AF0'
        ));
  
        $page=curl_exec($ch);
        if (curl_getinfo($ch, CURLINFO_HTTP_CODE)!=200)
        {
             curl_close($ch);
             break;
        }   
     
        $html=str_get_html($page);
        $tds=$html->find('table[id=gvPra] tr[style=color:#000000;border-color:#B9CAD1;border-width:1px;border-style:Solid;] td[1]');
        foreach ($tds as $td)
        {
            $pratiche[]=$td->plaintext;
        }
        $rich=$html->find('span[id^=lb]');
        foreach ($rich as $ric)
        {
             $euro[]=trim(str_replace('€','',$ric->plaintext));
        }
        if (count($pratiche)>0 && count($euro)>0)
        {
             if (count($euro)==1)
                $euro[1]=0;
             
             scraperwiki::sqliteexecute("insert into fabbricato values (?,?,?,?,?)", array($i,$euro[0],$euro[1],$date,$date)); 
             scraperwiki::sqlitecommit();   
        }
        foreach($pratiche as $p)
        {
            $cn2=scraperwiki::select ("* from fabbricato_has_pratica where fabbricato_id=".$i." and pratica_id='".$p."'");
            if (count($cn2)==0)
            {
             $cn1=scraperwiki::select ("* from pratica where id_pratica='".$p."'");
             if (count($cn1)==0)
                 scraperwiki::sqliteexecute("insert into pratica values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", array($p, $date, $date.NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL));  
  
             scraperwiki::sqliteexecute("insert into fabbricato_has_pratica values (?,?,?,?,?)", array(NULL,$i,$p,$date,$date)); 
             scraperwiki::sqlitecommit();
            }
        }
        curl_close($ch);
    }
    elseif ($cn[0]['c']>1)
    {
        echo "attenzione!!!\n";
    }
}

//FINE Controllo e import dei nuovi fabbricati

//Controllo, update e import delle pratiche
$pratiche=scraperwiki::select ("id_pratica from pratica where updated_at not like '2013-05-06%'");
foreach ($pratiche as $pratica)
{
  $arr_pratica=array();
  $pratica_id=$pratica['id_pratica'];
  $uri="http://laquila.geoportal.it/webgis/visurapratiche.aspx";
  $page=shell_exec("curl -G -d 'protNorm=$pratica_id' -G -d 'Utente=laquila' -H 'Host: laquila.geoportal.it' -H 'Connection: keep-alive' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:19.0) Gecko/20100101 Firefox/19.0' -H 'Accept-Encoding: gzip, deflate' -H 'Cookie: ASP.NET_SessionId=lpx4ql52v15h4ssr1fqp2q3b; digi_gis=Sessione=599398ae-9a25-11e2-8000-00155d036001_en_MTI3LjAuMC4x0AF20AF10AF0&Utente=laquila&Mappa=Ricostruzione51586d2796293; submenuheader=0c; PHPSESSID=b3d70ed8-996a-11e2-8000-00155d036001-en-MTI3LjAuMC4x0AF20AF10AF0' ".$uri);
  $html=str_get_html($page);
  $campi=campi();
  foreach ($campi as $campo)
  {
    $tds=$html->find("'span[id=".$campo."']");
    foreach ($tds as $td)
    {
      //echo $campo."-".trim($td->plaintext);
      $valore=str_replace("€","",($td->plaintext));
      $valore=str_replace("d'","di ",$valore);
      $valore=trim($valore);
      if (substr_count($valore,"/")==2)
      {
        $valore=explode("/",$valore);
        $valore=$valore[2]."-".$valore[1]."-".$valore[0];
      }
      $arr_pratica[$campo]=$valore;
    }
  }
  foreach ($arr_pratica as $k=>$ar)
  {
    scraperwiki::sqliteexecute("update pratica set $k='$ar' where id_pratica='$pratica_id'");
    scraperwiki::sqlitecommit();  
  }  
  scraperwiki::sqliteexecute("update pratica set updated_at='$date' where id_pratica='$pratica_id'");
  scraperwiki::sqlitecommit(); 
}
//FINE Controllo, update e import delle pratiche

// Ctrl SOPRINTENDENZA IN ISTRUTTORIA
$istruttorie=array();
for ($i=1;$i<=300;$i++)
{
  $uri="http://laquila.geoportal.it/webgis/tooltip/istruttoria.aspx?IdFabb=".$i;
  $singola_istr=array();
  $ch=curl_init($uri);
  curl_setopt($ch,CURLOPT_HEADER,0);
  curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
  curl_setopt($ch, CURLOPT_HTTPHEADER, array(
         'Host: laquila.geoportal.it' ,
         'Connection: keep-alive' ,
         'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' ,
         'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:19.0) Gecko/20100101 Firefox/19.0' ,
         'Accept-Encoding: gzip, deflate' ,
         'Cookie: ASP.NET_SessionId=lpx4ql52v15h4ssr1fqp2q3b; digi_gis=Sessione=599398ae-9a25-11e2-8000-00155d036001_en_MTI3LjAuMC4x0AF20AF10AF0&Utente=laquila&Mappa=Ricostruzione51586d2796293; submenuheader=0c; PHPSESSID=b3d70ed8-996a-11e2-8000-00155d036001-en-MTI3LjAuMC4x0AF20AF10AF0'
   ));
  $page=curl_exec($ch);
  $html=str_get_html($page);
  $tds=$html->find('table tr td span[id^=lb]');
  foreach($tds as $k=>$td)
  {
    
    if ($td->id=='lbAggregato' && $td->plaintext=='')
       break;
    $singola_istr[]=$td->plaintext;
    if ($td->id=='lbQuadro')
       $istruttorie[$i]=$singola_istr;
  }
}
foreach($istruttorie as $j=>$istruttoria)
{
  $cn1=scraperwiki::select ("* from soprintendenza where aggregato='".$istruttoria[0]."'");
  if (count($cn1)==0)
  {
    scraperwiki::sqliteexecute("insert into soprintendenza values   (?,?,?,?,?,?,?,?)", array($istruttoria[0],$istruttoria[1],$istruttoria[2],$istruttoria[3],$istruttoria[4],$date,$date,$j));
    scraperwiki::sqlitecommit(); 
  }
}
// FINE SOPRINTENDENZA IN ISTRUTTORIA

?>