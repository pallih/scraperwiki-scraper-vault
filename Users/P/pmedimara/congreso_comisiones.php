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

function estandarizarOrgano($organo){
    $abrev=array("Parlam.","Seguimto.","Concil.","Corresponsab.");
    $completas=array("Parlamentario","Seguimiento","Conciliación","Corresponsabilidad");
    $correcto= ucfirst(quitarEspaciosSobra(str_replace($abrev,$completas,$organo)));
    return $correcto;
}

function nombreCom($organo){
    if (strpos($organo, "Comisión del") !== false){
        $com=quitarEspaciosSobra(substr($organo,14));
    }else if (strpos($organo, "Comisión sobre") !== false){
        $com=quitarEspaciosSobra(substr($organo,15));
    }else if (strpos($organo, "Comisión de") !== false){
        $com=quitarEspaciosSobra(substr($organo,13));
    }else if (strpos($organo, "Comisión para el") !== false){
        $com=quitarEspaciosSobra(substr($organo,17));
    }else if (strpos($organo, "Comisión para las") !== false){
        $com=quitarEspaciosSobra(substr($organo,18));
    }else if (strpos($organo, "Comisión Mixta para las") !== false){
        $com=quitarEspaciosSobra(substr($organo,24));
    }else if (strpos($organo, "Comisión Mixta para la") !== false){
        $com=quitarEspaciosSobra(substr($organo,23));
    }else if (strpos($organo, "Comisión Mixta de") !== false){
        $com=quitarEspaciosSobra(substr($organo,18));
    }else if (strpos($organo, "Comisión Mixta para el") !== false){
        $com=quitarEspaciosSobra(substr($organo,23));
    }else if (strpos($organo, "Comisión Mixta") !== false){
        $com=quitarEspaciosSobra(substr($organo,15));
    }else{
        $com=quitarEspaciosSobra(substr($organo,9));
    }
    return $com;
}

function prefijoComision($organo){
    if (strpos($organo, "Comisión del") !== false){
        $pre="del";
    }else if (strpos($organo, "Comisión sobre") !== false){
        $pre="sobre";
    }else if (strpos($organo, "Comisión de") !== false){
        $pre="de";
    }else if (strpos($organo, "Comisión para el") !== false){
        $pre="para el";
    }else if (strpos($organo, "Comisión para las") !== false){
        $pre="para las";
    }else if (strpos($organo, "Comisión Mixta para las") !== false){
        $pre="para las";
    }else if (strpos($organo, "Comisión Mixta para la") !== false){
        $pre="para la";
    }else if (strpos($organo, "Comisión Mixta de") !== false){
        $pre="de";
    }else if (strpos($organo, "Comisión Mixta para el") !== false){
        $pre="para el";
    }else if (strpos($organo, "Comisión Mixta") !== false){
        $pre="";
    }else{
        $pre="";
    }
    
    return $pre;
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
        $lista=$comHTML->find('div[class=listado_1_comisiones]',$i)->find('li');
        if($lista !== null){
            foreach ($lista as $comElem){
                $organo_=quitarEspaciosSobra($comElem->plaintext);
                $organo=estandarizarOrgano($organo_);
                if (strpos($organo, "Comisión") !== false){
                    $comision=array();
                    $urlOrgano=$comElem->find("a",0)->href;

                    $comision["idOrgano"]=obtenerCampoUrl($urlOrgano,"idOrgano");
                    $comision["nombre"]=nombreCom($organo);
                    $comision["prefijo"]=prefijoComision($organo);
                    $comision["legislativa"]=$atributos[$i]["legis"];
                    $comision["permanente"]=$atributos[$i]["perm"];
                    $comision["mixta"]=$atributos[$i]["mixta"];
                    scraperwiki::save_sqlite(array('idOrgano'), $comision);
                }
            }
        }else{
            echo "Error al obtener la lista de comisiones ($i/4)";
        }
    }

?>
