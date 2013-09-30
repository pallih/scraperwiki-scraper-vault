<?php

require 'scraperwiki/simple_html_dom.php';     

function obtenerCampoUrl($url,$campo){
    $patron="/$campo=(\d|\w)+/";
    if(preg_match($patron,$url,$coincidencias)!==false){
        $pre="$campo=";
        //$valor=$coincidencias[0];
        $valor=substr($coincidencias[0],strlen($pre));
        return $valor;
    }else{
        return false;
    }
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

function estandarizarOrgano($organo){
    $abrev=array("Parlam.","Seguimto.","Concil.","Corresponsab.");
    $completas=array("Parlamentario","Seguimiento","Conciliación","Corresponsabilidad");
    $correcto= ucfirst(quitarEspaciosSobra(str_replace($abrev,$completas,$organo)));
    return $correcto;
}

function nombreSubcom($organo){
    $subcom=ucfirst(quitarEspaciosSobra(substr($organo,12)));
    if(strpos($subcom,"(") !== false) $subcom=quitarEspaciosSobra(substrHasta($subcom,"("));
    return $subcom;
}

function iniciativaSubcom($organo){
    $inic="";
    if(strpos($organo,"(") !== false) $inic=quitarEspaciosSobra(substrHasta(substrDesde($organo,"("),")"));
    return $inic;
}


    $url="http://www.congreso.es/portal/page/portal/Congreso/Congreso/Organos/Comision";
    $html_content = scraperwiki::scrape($url);
    $comHTML = str_get_html($html_content);

    $atributos=array();
    $atributos[0]["legis"]=1;
    $atributos[0]["perm"]=1;
    $atributos[0]["mixta"]=0;
    $atributos[1]["legis"]=0;
    $atributos[1]["perm"]=1;
    $atributos[1]["mixta"]=0;
    $atributos[2]["legis"]=0;
    $atributos[2]["perm"]=0;
    $atributos[2]["mixta"]=0;
    $atributos[3]["legis"]=0;
    $atributos[3]["perm"]=1;
    $atributos[3]["mixta"]=1;

    for($i=0;$i<4;$i++){
        $lista=$comHTML->find('div[class=listado_1_comisiones]',$i)->find('span');
        if($lista !== null){
            foreach ($lista as $comElem){
                $organo_=quitarEspaciosSobra($comElem->plaintext);
                $organo=estandarizarOrgano($organo_);
                if (strpos($organo, "Subcomisión") !== false){
                    $subcom=array();
                    $urlOrgano=$comElem->find("a",0)->href;

                    $subcom["idOrgano"]=obtenerCampoUrl($urlOrgano,"idOrgano");
                    $subcom["nombre"]=nombreSubcom($organo);
                    $subcom["legislativa"]=$atributos[$i]["legis"];
                    $subcom["permanente"]=$atributos[$i]["perm"];
                    $subcom["mixta"]=$atributos[$i]["mixta"];
                    $subcom["iniciativa"]=iniciativaSubcom($organo);
                    scraperwiki::save_sqlite(array('nombre'),$subcom);
                }
            }
        }
    }

?>
<?php

require 'scraperwiki/simple_html_dom.php';     

function obtenerCampoUrl($url,$campo){
    $patron="/$campo=(\d|\w)+/";
    if(preg_match($patron,$url,$coincidencias)!==false){
        $pre="$campo=";
        //$valor=$coincidencias[0];
        $valor=substr($coincidencias[0],strlen($pre));
        return $valor;
    }else{
        return false;
    }
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

function estandarizarOrgano($organo){
    $abrev=array("Parlam.","Seguimto.","Concil.","Corresponsab.");
    $completas=array("Parlamentario","Seguimiento","Conciliación","Corresponsabilidad");
    $correcto= ucfirst(quitarEspaciosSobra(str_replace($abrev,$completas,$organo)));
    return $correcto;
}

function nombreSubcom($organo){
    $subcom=ucfirst(quitarEspaciosSobra(substr($organo,12)));
    if(strpos($subcom,"(") !== false) $subcom=quitarEspaciosSobra(substrHasta($subcom,"("));
    return $subcom;
}

function iniciativaSubcom($organo){
    $inic="";
    if(strpos($organo,"(") !== false) $inic=quitarEspaciosSobra(substrHasta(substrDesde($organo,"("),")"));
    return $inic;
}


    $url="http://www.congreso.es/portal/page/portal/Congreso/Congreso/Organos/Comision";
    $html_content = scraperwiki::scrape($url);
    $comHTML = str_get_html($html_content);

    $atributos=array();
    $atributos[0]["legis"]=1;
    $atributos[0]["perm"]=1;
    $atributos[0]["mixta"]=0;
    $atributos[1]["legis"]=0;
    $atributos[1]["perm"]=1;
    $atributos[1]["mixta"]=0;
    $atributos[2]["legis"]=0;
    $atributos[2]["perm"]=0;
    $atributos[2]["mixta"]=0;
    $atributos[3]["legis"]=0;
    $atributos[3]["perm"]=1;
    $atributos[3]["mixta"]=1;

    for($i=0;$i<4;$i++){
        $lista=$comHTML->find('div[class=listado_1_comisiones]',$i)->find('span');
        if($lista !== null){
            foreach ($lista as $comElem){
                $organo_=quitarEspaciosSobra($comElem->plaintext);
                $organo=estandarizarOrgano($organo_);
                if (strpos($organo, "Subcomisión") !== false){
                    $subcom=array();
                    $urlOrgano=$comElem->find("a",0)->href;

                    $subcom["idOrgano"]=obtenerCampoUrl($urlOrgano,"idOrgano");
                    $subcom["nombre"]=nombreSubcom($organo);
                    $subcom["legislativa"]=$atributos[$i]["legis"];
                    $subcom["permanente"]=$atributos[$i]["perm"];
                    $subcom["mixta"]=$atributos[$i]["mixta"];
                    $subcom["iniciativa"]=iniciativaSubcom($organo);
                    scraperwiki::save_sqlite(array('nombre'),$subcom);
                }
            }
        }
    }

?>
