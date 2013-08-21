<?php

require 'scraperwiki/simple_html_dom.php';
mb_internal_encoding('UTF-8');

function sinTNS($cad){
    return sinSS(preg_replace("/(\r|\t)/","",$cad));
}

function sinSS($cad){
    return trim(preg_replace("/\s{2,}/"," ",$cad));
}

function sinPSS($cad){
    return trim(sinSS(preg_replace("/^\./","",$cad)));
}

function toRegExp($cad){
    $esp=array("/",".","-");
    $conv=array("\/","\.","\-");
    return str_replace($esp,$conv,$cad);
}

function traducirHTML($cad){
    $cad=htmlspecialchars_decode($cad);
    $esp=array("&nbsp;","&aacute;","&eacute;","&iacute;","&oacute;","&uacute;","&ntilde;","&Aacute;","&Eacute;","&Iacute;","&Oacute;","&Uacute;","&Ntilde;");
    $sust=array(" ","á","é","í","ó","ú","ñ","Á","É","Í","Ó","Ú","Ñ");
    return str_replace($esp,$sust,$cad);
}

function fechaNumerica($fecha){
    if(preg_match_all("/\d+/",$fecha,$coinc)==2){
        $mes=substrEntre($fecha," ",3);
        $mesNum=mesNumerico(sinSS($mes));

        if(strlen($coinc[0][0])==1) $coinc[0][0]="0".$coinc[0][0];
        if(strlen($coinc[0][1])==1) $coinc[0][1]="0".$coinc[0][1];
        return $coinc[0][0]."/".$mesNum."/".$coinc[0][1];
    }else{
        return $fecha;
    }
}

function mesNumerico($mes){
    switch(mb_strtolower($mes,'UTF-8')){
        case "enero":
            $mesNum="01";
            break;
        case "febrero":
            $mesNum="02";
            break;
        case "marzo":
            $mesNum="03";
            break;
        case "abril":
            $mesNum="04";
            break;
        case "mayo":
            $mesNum="05";
            break;
        case "junio":
            $mesNum="06";
            break;
        case "julio":
            $mesNum="07";
            break;
        case "agosto":
            $mesNum="08";
            break;
        case "septiembre":
            $mesNum="09";
            break;
        case "octubre":
            $mesNum="10";
            break;
        case "noviembre":
            $mesNum="11";
            break;
        case "diciembre":
            $mesNum="12";
            break;
        default:
            $mesNum=$mes;
            break;
    }
    return $mesNum;
}

function substrHasta($cad,$subcad){
    $indice = strpos($cad,$subcad);
    if ($indice!== false){
        return substr($cad,0,$indice);
    }else{
        return "";
    }
}

function substrDesde($cad,$subcad){
    $indice = strrpos($cad,$subcad);
    if ($indice!== false){
        return substr($cad,$indice+1,strlen($cad));
    }else{
        return "";
    }
}  

function substrEntre($cad,$subcad,$pos){
    $sub="";
    if ($pos==0){
        return substrHasta($cad,$subcad);
    }else{
        $indice=0;
        for ($i=0;$i<$pos;$i++){
            $indice = strpos($cad,$subcad,$indice) +1;
            if ($indice=== false){
                    break;
            }
        }
        $sig = strpos($cad,$subcad,$indice);
        $sub=substr($cad,$indice,($sig-$indice));
        return $sub;
    }
}

function quitarHora2($cad){
    if(preg_match("/^\s*o fin (\s|\w)+\./",$cad,$coinc)){
        print_r("Coincidencia:".$coinc[0]);
        return sinTNS(str_replace($coinc[0],"",$cad));
    }else if(preg_match("/^\s*y (\s|\w)+\./",$cad,$coinc)){
        return sinTNS(str_replace($coinc[0],"",$cad));
    }else{
        return $cad;
    }
}

function getHora($e){
    $hora=$e->find('span[class=hora_prog]',0)->plaintext;
    if($e->find('span[class=txt_prog]',0)->find('strong',0) != null){
        if($e->find('span[class=txt_prog]',0)->find('strong',0)->find('font',0) != null){
            $hora2=sinTNS($e->find('span[class=txt_prog]',0)->find('strong',0)->find('font',0)->plaintext);
            $hora=sinTNS($hora." ".$hora2);
        }
    }
    $hora=sinTNS(str_replace("h.","",$hora));
    return $hora;
}

function getURL($e){
    if($e->find('span[class=txt_prog]',0)->find('a',0) != null){
            return $e->find('span[class=txt_prog]',0)->find('a',0)->href;
    }else{
        return "";
    }
}

function getLugar($e){
    $bs=$e->find('span[class=txt_prog]',0)->find('b');
    if(count($bs)>0) return sinTNS($e->find('b',count($bs)-1)->plaintext);
    
    $strongs=$e->find('span[class=txt_prog]',0)->find('strong');
    if(count($strongs)>0) return sinTNS($e->find('strong',count($strongs)-1)->plaintext);
    
    return "";
    
}

function getEvento($e,$lugar){
    $elem=$e->find('span[class=txt_prog]',0);
    $todo=sinTNS("".$elem->plaintext);
    $todo=quitarHora2($todo);
    if ($elem->find('a',0)!==null){
        $atext=toRegExp(sinTNS($elem->find('a',0)->plaintext));
        //$atext=sinTNS($elem->find('a',0)->plaintext);
        if (preg_match("/^.*$atext/",$todo,$coinc)) return sinPSS($coinc[0]);
        return sinPSS($atext);
    }else{
        if($lugar!==""){
            return sinPSS(str_replace($lugar," ",$todo));
        }else{
            return $todo;
        }
    }
}

function getInfo($e,$evento,$lugar){
    $elem=$e->find('span[class=txt_prog]',0);
    $todo=sinTNS($elem->plaintext);

    $todo=quitarHora2($todo);
    $info=sinTNS(str_replace($evento,"",$todo));
    if($lugar!=="") $info=sinTNS(str_replace($lugar,"",$info));
   
    return sinPSS($info);
}

function scrapSemana($sem,$year){
    $url="http://www.congreso.es/portal/page/portal/Congreso/GenericPopUp?_piref73_2138150_73_2138147_2138147.next_page=/wc/agendaCompleta&semana=".$sem."-".$year;
    $html_content = scraperwiki::scrape($url);
    $html_content = traducirHTML($html_content);
    $agendaHTML = str_get_html($html_content);
    global $numEvent;
    for($i=1;$i<8;$i++){
        $dia=array();
        $agendaDia=$agendaHTML->find('div[id=agenda'.$i.']',0);
        $fechadia=sinTNS($agendaDia->find('div[class=prog_dia]',0)->plaintext);
        $dia["fecha"]=fechaNumerica($fechadia);
        $dia["nombre"]=substrHasta($fechadia," ");
        
        foreach($agendaDia->find('div[class=parrilla]') as $element){
            $evento=array();
            $evento["dia"]=$dia["nombre"];
            $evento["fecha"]=$dia["fecha"];
            $evento["id"]=$numEvent;
            $evento["hora"]=getHora($element);
            $evento["url"]=getURL($element);
            $evento["lugar"]=getLugar($element);
            $evento["event"]=getEvento($element,$evento["lugar"]);
            $evento["info"]=getInfo($element,$evento["event"],$evento["lugar"]);

            //print_r(". scrapeado evento ".$evento["id"]);
            //print_r(". evento: ".$evento["event"]);
            scraperwiki::save_sqlite(array("id"),array(
                "id"=>$evento["id"],
                "dia"=>$evento["dia"],
                "fecha"=>$evento["fecha"],
                "hora"=>$evento["hora"],
                "url"=>$evento["url"],
                "lugar"=>$evento["lugar"],
                "info"=>$evento["info"],
                "event"=>$evento["event"]));
            $numEvent++;
        }
    }
}

function scrapXLeg(){
    $sem_actual=date("W");
    for($sem=50;$sem<53;$sem++){
        scrapSemana($sem,2011);
    }
    for($sem=1;$sem<$sem_actual+1;$sem++){
        scrapSemana($sem,2012);
    }
}

function scrapSemanaAct(){
    $sem_actual=date("W");
    scrapSemana($sem_actual,2012);
}

scraperwiki::sqliteexecute("drop table if exists swdata");
$numEvent=1;
scrapXLeg();

?>
