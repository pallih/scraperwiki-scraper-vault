<?php
require 'scraperwiki/simple_html_dom.php';
mb_internal_encoding("UTF-8");

// FUNCIONES

function fechaNumerica($fecha){
    if(preg_match_all("/\d+/",$fecha,$coinc)==2){
        $mes=mb_substrEntre($fecha," ",2);
        $mesNum=mesNumerico($mes);

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

function quitarEspaciosSobra($cad){
    $cadena=trim($cad);
    $retorno="";
    if (strlen($cadena) > 0){
        $retorno=$cadena[0];
        for($i=1;$i<strlen($cadena);$i++){
            if( ($cadena[$i] != ' ') || ($cadena[$i] == ' ' && $cadena[$i-1] != ' ')){
                $retorno=$retorno . $cadena[$i];
            }
        }
    }
    return $retorno;
}

function mb_substrHasta($cad,$subcad){
    //$c = quitarEspaciosSobra($cad);
    $indice = strpos($cad,$subcad);
    if ($indice!== false){
        return mb_substr($cad,0,$indice);
    }else{
        return "";
    }
}

function mb_substrDesde($cad,$subcad){
    //$c = quitarEspaciosSobra($cad);
    $indice = strrpos($cad,$subcad);
    if ($indice!== false){
        return mb_substr($cad,$indice+1,strlen($cad));
    }else{
        return "";
    }
}

function mb_substrEntre($cad,$subcad,$pos){
    $sub="";
    if ($pos==0){
        return mb_substrHasta($cad,$subcad);
    }else{
        $indice=0;
        for ($i=0;$i<$pos;$i++){
            $indice = strpos($cad,$subcad,$indice) +1;
            if ($indice=== false){
                    break;
            }
        }
        $sig = strpos($cad,$subcad,$indice);
        $sub=mb_substr($cad,$indice,($sig-$indice));
        return $sub;
    }
}

function estandarizarOrgano($organo){
    $abrev=array("Parlam.","Seguimto.","Concil.","Corresponsab.");
    $completas=array("Parlamentario","Seguimiento","Conciliación","Corresponsabilidad");
    $correcto= ucfirst(quitarEspaciosSobra(str_replace($abrev,$completas,$organo)));
    return $correcto;
}

function nombreCom($organo){
    if (strpos($organo, "Comisión del") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,14));
    }else if (strpos($organo, "Comisión sobre") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,15));
    }else if (strpos($organo, "Comisión de") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,12));
    }else if (strpos($organo, "Comisión para el") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,17));
    }else if (strpos($organo, "Comisión para las") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,18));
    }else if (strpos($organo, "Comisión Mixta para las") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,24));
    }else if (strpos($organo, "Comisión Mixta para la") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,23));
    }else if (strpos($organo, "Comisión Mixta de") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,18));
    }else if (strpos($organo, "Comisión Mixta para el") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,23));
    }else if (strpos($organo, "Comisión Mixta") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,15));
    }else{
        $com=quitarEspaciosSobra(mb_substr($organo,9));
    }
    return $com;
}

function nombreSubcom($organo){
    $subcom=ucfirst(quitarEspaciosSobra(mb_substr($organo,12)));
    if(strpos($subcom,"(") !== false) $subcom=quitarEspaciosSobra(mb_substrHasta($subcom,"("));
    return $subcom;
}

function estandarizarLegislaturas($cad){
    $patron="/[E-Z]+/";
    $legis="";
    preg_match_all($patron,$cad,$matches);
    for($i=0;$i<count($matches[0]);$i++){
        $legis=$legis.$matches[0][$i]." ";
    }
    return $legis;
}

function estandarizarGP($cad){
    return quitarEspaciosSobra(mb_substr(mb_substrHasta($cad,"("),5));
}

// Función para obtener los emails del diputado
function obtenerEmails($html){
    $correos="";
    $lista=$html->find('div[class=webperso_dip_parte]');
    foreach($lista as $div){
        $correoTag=$div->find('a',0);
        if($correoTag!==null){
            $correo=quitarEspaciosSobra($correoTag->plaintext);
            if(strpos($correo,'@')!==false){
                $correos=$correos." $correo";
            }
        }
    }
    return quitarEspaciosSobra($correos);
}

function obtenerWebs($html){
    $webs="";
    $lista=$html->find('div[class=webperso_dip_parte]');
    foreach($lista as $div){
        $webTag=$div->find('a',0);
        if($webTag!==null){
            $web=quitarEspaciosSobra($webTag->plaintext);
            if(strpos($web,'http://')!==false){
                $webs=$webs." $web";
            }
        }
    }
    return quitarEspaciosSobra($webs);
}

function obtenerPosHemiciclo($html){
    $img=$html->find('p[class=pos_hemiciclo]',0)->find('img',0)->src;
    $pos_hemiciclo=mb_substr(mb_substrHasta(mb_substrDesde($img,"hemi_100_"),".gif"),8);
    return $pos_hemiciclo;
}

// Función para separar comisiones, subcomisiones y otros órganos, así como sus cargos
function obtenerCargosCongreso($html){
    $lista=$html->find('div[class=listado_1]',0)->find('li');
    if ($lista != null){
        $cargosCongreso = array();
        $comisiones="";
        $subcomisiones="";
        $organosCongreso="";
        foreach($lista as $elem){
            $organoTag=$elem->find('a',0);
            if ( $organoTag!= null){
                $organo_ = quitarEspaciosSobra($organoTag->innertext);
                $organo=estandarizarOrgano($organo_);
                $cargo = quitarEspaciosSobra(mb_substrHasta($elem->plaintext,"de la"));
                if (strpos($organo, "Comisión") !== false){
                    $organo=nombreCom($organo);
                    $comisiones = $comisiones.$organo." (".$cargo."). ";
                }else if (strpos($organo, "Subcomisión") !== false){
                    $organo=nombreSubcom($organo);
                    $subcomisiones=$subcomisiones.$organo." (".$cargo."). ";
                }else if ( (strpos($organo, "Delegación") === false) && (strpos($organo, "Ponencia") === false) ){
                    if(strpos($organo,"(") !== false)    $organo=quitarEspaciosSobra(mb_substrHasta($organo,"("));
                    $organosCongreso=$organosCongreso.$organo." (".$cargo."). ";
                }
            }
        }
        
        $cargosCongreso["comisiones"]=quitarEspaciosSobra($comisiones);
        $cargosCongreso["subcomisiones"]=quitarEspaciosSobra($subcomisiones);
        $cargosCongreso["organosCongreso"]=quitarEspaciosSobra($organosCongreso);
        
        return $cargosCongreso;
    }else{
        return false;
    }
    
}

scraperwiki::sqliteexecute("drop table if exists datosDipus");
scraperwiki::sqliteexecute("create table if not exists datosDipus(id integer)");
// Obtenemos la info ya scrapeada por pablog
scraperwiki::attach('congreso_datos_diputado','pablog');
//$campos="id,nombre,apellidos,circunscripcion,nacimiento,partido,grupo_parlamentario,cargos_anteriores,estado_civil,curriculum,pos_fila,pos_butaca,pos_sector,twitter,facebook_url,web,linkedin_url,flickr_url";
$datos=scraperwiki::select("id,nombre,apellidos,circunscripcion,partido,grupo_parlamentario,cargos_anteriores,estado_civil,twitter,facebook_url,linkedin_url,flickr_url,nacimiento from pablog.swdata");

//Scrapeamos diputado a diputado sus correos y la info de los órganos a los que pertenece
// y lo insertamos en la tabla junto a la info ya existente (pablog)
foreach($datos as $fila){
    unset($diputado);
    $diputado=array();
    
    $diputado["id"]=$fila["id"];
    $diputado["nombre"]=$fila["nombre"];
    $diputado["apellidos"]=$fila["apellidos"];
    $diputado["circunscripcion"]=$fila["circunscripcion"];
    $diputado["partido"]=$fila["partido"];
    $diputado["grupo_parlamentario"]=estandarizarGP($fila["grupo_parlamentario"]);
    $diputado["ecivil_estudios_cv"]=$fila["estado_civil"]; print_r("ECECV: ".$diputado["ecivil_estudios_cv"]);
    $diputado["fecha_nac"]=fechaNumerica($fila["nacimiento"]);
    $diputado["otras_legis"]=estandarizarLegislaturas($fila["cargos_anteriores"]);
    $diputado["twitter"]=$fila["twitter"];
    $diputado["fb"]=$fila["facebook_url"];
    $diputado["linkedin_url"]=$fila["linkedin_url"];
    $diputado["flickr_url"]=$fila["flickr_url"];
    

    
    $url="http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=".$diputado["id"]."&idLegislatura=10";
    $html_content = scraperwiki::scrape($url);
    $html_content = html_entity_decode(htmlspecialchars_decode($html_content),ENT_COMPAT,"UTF-8");
    $html = str_get_html($html_content);
    $diputado["email"]=obtenerEmails($html);
    $diputado["web"]=obtenerWebs($html);
    $diputado["pos_hemiciclo"]=obtenerPosHemiciclo($html);

    $cargos=obtenerCargosCongreso($html);
    if($cargos !== false){
        $diputado["comisiones"]=$cargos["comisiones"];
        $diputado["subcomisiones"]=$cargos["subcomisiones"];
        $diputado["organos_congreso"]=$cargos["organosCongreso"];
    }
    scraperwiki::save_sqlite(array('id'), $diputado,'datosDipus');
}

?>
<?php
require 'scraperwiki/simple_html_dom.php';
mb_internal_encoding("UTF-8");

// FUNCIONES

function fechaNumerica($fecha){
    if(preg_match_all("/\d+/",$fecha,$coinc)==2){
        $mes=mb_substrEntre($fecha," ",2);
        $mesNum=mesNumerico($mes);

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

function quitarEspaciosSobra($cad){
    $cadena=trim($cad);
    $retorno="";
    if (strlen($cadena) > 0){
        $retorno=$cadena[0];
        for($i=1;$i<strlen($cadena);$i++){
            if( ($cadena[$i] != ' ') || ($cadena[$i] == ' ' && $cadena[$i-1] != ' ')){
                $retorno=$retorno . $cadena[$i];
            }
        }
    }
    return $retorno;
}

function mb_substrHasta($cad,$subcad){
    //$c = quitarEspaciosSobra($cad);
    $indice = strpos($cad,$subcad);
    if ($indice!== false){
        return mb_substr($cad,0,$indice);
    }else{
        return "";
    }
}

function mb_substrDesde($cad,$subcad){
    //$c = quitarEspaciosSobra($cad);
    $indice = strrpos($cad,$subcad);
    if ($indice!== false){
        return mb_substr($cad,$indice+1,strlen($cad));
    }else{
        return "";
    }
}

function mb_substrEntre($cad,$subcad,$pos){
    $sub="";
    if ($pos==0){
        return mb_substrHasta($cad,$subcad);
    }else{
        $indice=0;
        for ($i=0;$i<$pos;$i++){
            $indice = strpos($cad,$subcad,$indice) +1;
            if ($indice=== false){
                    break;
            }
        }
        $sig = strpos($cad,$subcad,$indice);
        $sub=mb_substr($cad,$indice,($sig-$indice));
        return $sub;
    }
}

function estandarizarOrgano($organo){
    $abrev=array("Parlam.","Seguimto.","Concil.","Corresponsab.");
    $completas=array("Parlamentario","Seguimiento","Conciliación","Corresponsabilidad");
    $correcto= ucfirst(quitarEspaciosSobra(str_replace($abrev,$completas,$organo)));
    return $correcto;
}

function nombreCom($organo){
    if (strpos($organo, "Comisión del") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,14));
    }else if (strpos($organo, "Comisión sobre") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,15));
    }else if (strpos($organo, "Comisión de") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,12));
    }else if (strpos($organo, "Comisión para el") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,17));
    }else if (strpos($organo, "Comisión para las") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,18));
    }else if (strpos($organo, "Comisión Mixta para las") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,24));
    }else if (strpos($organo, "Comisión Mixta para la") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,23));
    }else if (strpos($organo, "Comisión Mixta de") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,18));
    }else if (strpos($organo, "Comisión Mixta para el") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,23));
    }else if (strpos($organo, "Comisión Mixta") !== false){
        $com=quitarEspaciosSobra(mb_substr($organo,15));
    }else{
        $com=quitarEspaciosSobra(mb_substr($organo,9));
    }
    return $com;
}

function nombreSubcom($organo){
    $subcom=ucfirst(quitarEspaciosSobra(mb_substr($organo,12)));
    if(strpos($subcom,"(") !== false) $subcom=quitarEspaciosSobra(mb_substrHasta($subcom,"("));
    return $subcom;
}

function estandarizarLegislaturas($cad){
    $patron="/[E-Z]+/";
    $legis="";
    preg_match_all($patron,$cad,$matches);
    for($i=0;$i<count($matches[0]);$i++){
        $legis=$legis.$matches[0][$i]." ";
    }
    return $legis;
}

function estandarizarGP($cad){
    return quitarEspaciosSobra(mb_substr(mb_substrHasta($cad,"("),5));
}

// Función para obtener los emails del diputado
function obtenerEmails($html){
    $correos="";
    $lista=$html->find('div[class=webperso_dip_parte]');
    foreach($lista as $div){
        $correoTag=$div->find('a',0);
        if($correoTag!==null){
            $correo=quitarEspaciosSobra($correoTag->plaintext);
            if(strpos($correo,'@')!==false){
                $correos=$correos." $correo";
            }
        }
    }
    return quitarEspaciosSobra($correos);
}

function obtenerWebs($html){
    $webs="";
    $lista=$html->find('div[class=webperso_dip_parte]');
    foreach($lista as $div){
        $webTag=$div->find('a',0);
        if($webTag!==null){
            $web=quitarEspaciosSobra($webTag->plaintext);
            if(strpos($web,'http://')!==false){
                $webs=$webs." $web";
            }
        }
    }
    return quitarEspaciosSobra($webs);
}

function obtenerPosHemiciclo($html){
    $img=$html->find('p[class=pos_hemiciclo]',0)->find('img',0)->src;
    $pos_hemiciclo=mb_substr(mb_substrHasta(mb_substrDesde($img,"hemi_100_"),".gif"),8);
    return $pos_hemiciclo;
}

// Función para separar comisiones, subcomisiones y otros órganos, así como sus cargos
function obtenerCargosCongreso($html){
    $lista=$html->find('div[class=listado_1]',0)->find('li');
    if ($lista != null){
        $cargosCongreso = array();
        $comisiones="";
        $subcomisiones="";
        $organosCongreso="";
        foreach($lista as $elem){
            $organoTag=$elem->find('a',0);
            if ( $organoTag!= null){
                $organo_ = quitarEspaciosSobra($organoTag->innertext);
                $organo=estandarizarOrgano($organo_);
                $cargo = quitarEspaciosSobra(mb_substrHasta($elem->plaintext,"de la"));
                if (strpos($organo, "Comisión") !== false){
                    $organo=nombreCom($organo);
                    $comisiones = $comisiones.$organo." (".$cargo."). ";
                }else if (strpos($organo, "Subcomisión") !== false){
                    $organo=nombreSubcom($organo);
                    $subcomisiones=$subcomisiones.$organo." (".$cargo."). ";
                }else if ( (strpos($organo, "Delegación") === false) && (strpos($organo, "Ponencia") === false) ){
                    if(strpos($organo,"(") !== false)    $organo=quitarEspaciosSobra(mb_substrHasta($organo,"("));
                    $organosCongreso=$organosCongreso.$organo." (".$cargo."). ";
                }
            }
        }
        
        $cargosCongreso["comisiones"]=quitarEspaciosSobra($comisiones);
        $cargosCongreso["subcomisiones"]=quitarEspaciosSobra($subcomisiones);
        $cargosCongreso["organosCongreso"]=quitarEspaciosSobra($organosCongreso);
        
        return $cargosCongreso;
    }else{
        return false;
    }
    
}

scraperwiki::sqliteexecute("drop table if exists datosDipus");
scraperwiki::sqliteexecute("create table if not exists datosDipus(id integer)");
// Obtenemos la info ya scrapeada por pablog
scraperwiki::attach('congreso_datos_diputado','pablog');
//$campos="id,nombre,apellidos,circunscripcion,nacimiento,partido,grupo_parlamentario,cargos_anteriores,estado_civil,curriculum,pos_fila,pos_butaca,pos_sector,twitter,facebook_url,web,linkedin_url,flickr_url";
$datos=scraperwiki::select("id,nombre,apellidos,circunscripcion,partido,grupo_parlamentario,cargos_anteriores,estado_civil,twitter,facebook_url,linkedin_url,flickr_url,nacimiento from pablog.swdata");

//Scrapeamos diputado a diputado sus correos y la info de los órganos a los que pertenece
// y lo insertamos en la tabla junto a la info ya existente (pablog)
foreach($datos as $fila){
    unset($diputado);
    $diputado=array();
    
    $diputado["id"]=$fila["id"];
    $diputado["nombre"]=$fila["nombre"];
    $diputado["apellidos"]=$fila["apellidos"];
    $diputado["circunscripcion"]=$fila["circunscripcion"];
    $diputado["partido"]=$fila["partido"];
    $diputado["grupo_parlamentario"]=estandarizarGP($fila["grupo_parlamentario"]);
    $diputado["ecivil_estudios_cv"]=$fila["estado_civil"]; print_r("ECECV: ".$diputado["ecivil_estudios_cv"]);
    $diputado["fecha_nac"]=fechaNumerica($fila["nacimiento"]);
    $diputado["otras_legis"]=estandarizarLegislaturas($fila["cargos_anteriores"]);
    $diputado["twitter"]=$fila["twitter"];
    $diputado["fb"]=$fila["facebook_url"];
    $diputado["linkedin_url"]=$fila["linkedin_url"];
    $diputado["flickr_url"]=$fila["flickr_url"];
    

    
    $url="http://www.congreso.es/portal/page/portal/Congreso/Congreso/Diputados/BusqForm?_piref73_1333155_73_1333154_1333154.next_page=/wc/fichaDiputado?idDiputado=".$diputado["id"]."&idLegislatura=10";
    $html_content = scraperwiki::scrape($url);
    $html_content = html_entity_decode(htmlspecialchars_decode($html_content),ENT_COMPAT,"UTF-8");
    $html = str_get_html($html_content);
    $diputado["email"]=obtenerEmails($html);
    $diputado["web"]=obtenerWebs($html);
    $diputado["pos_hemiciclo"]=obtenerPosHemiciclo($html);

    $cargos=obtenerCargosCongreso($html);
    if($cargos !== false){
        $diputado["comisiones"]=$cargos["comisiones"];
        $diputado["subcomisiones"]=$cargos["subcomisiones"];
        $diputado["organos_congreso"]=$cargos["organosCongreso"];
    }
    scraperwiki::save_sqlite(array('id'), $diputado,'datosDipus');
}

?>
