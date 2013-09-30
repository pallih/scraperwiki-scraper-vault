<?php

function esImporte($texto)
{
    sscanf($texto, "%d.%d,%d", $uMil, $centena, $decimales);
    if (!is_numeric($uMil))
        return false;
    if (!is_numeric($centena))
        return false;
    if (!is_numeric($decimales))
        return false;
    return true;
}

function esFecha($texto)
{
    if (substr($texto, 2, 1) == "/")
        if (substr($texto, 5, 1) == "/")
            return true;
    return false;
}

function convertirImporte($importe)
{
    $importe = str_replace(",","#",$importe);
    $importe = str_replace(".",",",$importe);
    $importe = str_replace("#",".",$importe);
    return $importe;
}

function convertirFecha($fecha)
{
    $arrayFecha = explode("/", $fecha);
    $nuevaFecha = $arrayFecha[1]."/".$arrayFecha[0]."/".$arrayFecha[2];
    return $nuevaFecha;
}

function crearTabla($nombreTabla)
{
    scraperwiki::sqliteexecute("create table ".$nombreTabla." (idContrato int, `fecha` string, `objeto` string, `importe` string, `adjudicatario` string, `NIF` string)");
    scraperwiki::sqlitecommit();
}

function insertar($nombreTabla, $idContrato, $fecha, $objeto, $importe, $adjudicatario, $NIF)
{
    scraperwiki::sqliteexecute("insert into ".$nombreTabla." values (?,?,?,?,?,?)", array($idContrato, $fecha, utf8_decode($objeto), $importe, utf8_decode($adjudicatario), $NIF));
    scraperwiki::sqlitecommit();
}

$nombreTabla = "contratos4T2012";
crearTabla($nombreTabla);

$arrayPDF = array("https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_2_1.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_30_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_31_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_32_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_33_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_34_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_35_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_36_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5000.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5001.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5002.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5003.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5004.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5005.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5006.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5007.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5008.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_51_5101.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_51_15101.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_53_5301.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_61_1.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_61_6101.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_63_6301.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_64_16401.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_65_3.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_65_4.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_65_5.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_67_6701.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_4.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_6.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_8.pdf");

$idContrato = 1;

foreach($arrayPDF as $src_pdf) {

    # Some temporary files
    $pdf_f = tempnam('/tmp', 'inp') . '.pdf';
    $xml_f = tempnam('/tmp', 'out') . '.xml';

    # Download the PDF into a temporary file
    file_put_contents($pdf_f, file_get_contents($src_pdf));

    # Convert the PDF to XML
    $cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "' . $pdf_f . '" "'. $xml_f .'" >/dev/null 2>&1';
    system($cmd);

    # Load the XML and parse it.
    $xml = new SimpleXMLElement( file_get_contents($xml_f) );

    $objeto = "";
    $adjudicatario = "";
    $registro= array();

    foreach( $xml->page as $page) {
        $contadorElementos = 0;
        foreach( $page->text as $txt) {
            if ( strlen( trim($txt) ) > 3 && trim($txt) != "/" )
            {
                if ($contadorElementos == 0 && esImporte($txt))
                    $contadorElementos = 1;
                if ($contadorElementos == 3 && esFecha($txt))
                    $contadorElementos = 4;
                switch ($contadorElementos)
                {
                    case 0:
                        if (trim($txt) != "Hoja")
                            $objeto .= $txt." ";
                        break;
                    case 1:
                        $importe = $txt;
                        $contadorElementos = 2;
                        break;
                    case 2:
                        $NIF = $txt;
                        $contadorElementos = 3;
                        break;
                    case 3:
                        $adjudicatario .= $txt." ";
                        break;
                    case 4:
                        $fecha = convertirFecha($txt);
                        $contadorElementos = 6;
                        break;
                    case 6:
                        // Se inserta en la bd.
                       
                        $fecha = utf8_encode($fecha);
                        $objeto = utf8_encode($objeto);
                        $importe = utf8_encode(convertirImporte($importe));
                        $adjudicatario = utf8_encode($adjudicatario);
                        $NIF = utf8_encode($NIF);
                        insertar($nombreTabla, $idContrato, $fecha, $objeto, $importe, $adjudicatario, $NIF);
                        $idContrato++;
                        
                        if (trim($txt) != "Hoja")
                            $objeto = $txt." ";
                        $adjudicatario = "";
                        $contadorElementos = 0;
                        break;
                    default:
                        print "NO ENTRA NUNCA. Elemento: ".$contadorElementos."\n";
                        break;
                }
            }
        }
    }
}
?><?php

function esImporte($texto)
{
    sscanf($texto, "%d.%d,%d", $uMil, $centena, $decimales);
    if (!is_numeric($uMil))
        return false;
    if (!is_numeric($centena))
        return false;
    if (!is_numeric($decimales))
        return false;
    return true;
}

function esFecha($texto)
{
    if (substr($texto, 2, 1) == "/")
        if (substr($texto, 5, 1) == "/")
            return true;
    return false;
}

function convertirImporte($importe)
{
    $importe = str_replace(",","#",$importe);
    $importe = str_replace(".",",",$importe);
    $importe = str_replace("#",".",$importe);
    return $importe;
}

function convertirFecha($fecha)
{
    $arrayFecha = explode("/", $fecha);
    $nuevaFecha = $arrayFecha[1]."/".$arrayFecha[0]."/".$arrayFecha[2];
    return $nuevaFecha;
}

function crearTabla($nombreTabla)
{
    scraperwiki::sqliteexecute("create table ".$nombreTabla." (idContrato int, `fecha` string, `objeto` string, `importe` string, `adjudicatario` string, `NIF` string)");
    scraperwiki::sqlitecommit();
}

function insertar($nombreTabla, $idContrato, $fecha, $objeto, $importe, $adjudicatario, $NIF)
{
    scraperwiki::sqliteexecute("insert into ".$nombreTabla." values (?,?,?,?,?,?)", array($idContrato, $fecha, utf8_decode($objeto), $importe, utf8_decode($adjudicatario), $NIF));
    scraperwiki::sqlitecommit();
}

$nombreTabla = "contratos4T2012";
crearTabla($nombreTabla);

$arrayPDF = array("https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_2_1.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_30_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_31_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_32_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_33_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_34_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_35_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_36_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5000.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5001.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5002.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5003.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5004.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5005.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5006.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5007.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5008.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_51_5101.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_51_15101.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_53_5301.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_61_1.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_61_6101.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_63_6301.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_64_16401.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_65_3.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_65_4.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_65_5.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_67_6701.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_4.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_6.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_8.pdf");

$idContrato = 1;

foreach($arrayPDF as $src_pdf) {

    # Some temporary files
    $pdf_f = tempnam('/tmp', 'inp') . '.pdf';
    $xml_f = tempnam('/tmp', 'out') . '.xml';

    # Download the PDF into a temporary file
    file_put_contents($pdf_f, file_get_contents($src_pdf));

    # Convert the PDF to XML
    $cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "' . $pdf_f . '" "'. $xml_f .'" >/dev/null 2>&1';
    system($cmd);

    # Load the XML and parse it.
    $xml = new SimpleXMLElement( file_get_contents($xml_f) );

    $objeto = "";
    $adjudicatario = "";
    $registro= array();

    foreach( $xml->page as $page) {
        $contadorElementos = 0;
        foreach( $page->text as $txt) {
            if ( strlen( trim($txt) ) > 3 && trim($txt) != "/" )
            {
                if ($contadorElementos == 0 && esImporte($txt))
                    $contadorElementos = 1;
                if ($contadorElementos == 3 && esFecha($txt))
                    $contadorElementos = 4;
                switch ($contadorElementos)
                {
                    case 0:
                        if (trim($txt) != "Hoja")
                            $objeto .= $txt." ";
                        break;
                    case 1:
                        $importe = $txt;
                        $contadorElementos = 2;
                        break;
                    case 2:
                        $NIF = $txt;
                        $contadorElementos = 3;
                        break;
                    case 3:
                        $adjudicatario .= $txt." ";
                        break;
                    case 4:
                        $fecha = convertirFecha($txt);
                        $contadorElementos = 6;
                        break;
                    case 6:
                        // Se inserta en la bd.
                       
                        $fecha = utf8_encode($fecha);
                        $objeto = utf8_encode($objeto);
                        $importe = utf8_encode(convertirImporte($importe));
                        $adjudicatario = utf8_encode($adjudicatario);
                        $NIF = utf8_encode($NIF);
                        insertar($nombreTabla, $idContrato, $fecha, $objeto, $importe, $adjudicatario, $NIF);
                        $idContrato++;
                        
                        if (trim($txt) != "Hoja")
                            $objeto = $txt." ";
                        $adjudicatario = "";
                        $contadorElementos = 0;
                        break;
                    default:
                        print "NO ENTRA NUNCA. Elemento: ".$contadorElementos."\n";
                        break;
                }
            }
        }
    }
}
?><?php

function esImporte($texto)
{
    sscanf($texto, "%d.%d,%d", $uMil, $centena, $decimales);
    if (!is_numeric($uMil))
        return false;
    if (!is_numeric($centena))
        return false;
    if (!is_numeric($decimales))
        return false;
    return true;
}

function esFecha($texto)
{
    if (substr($texto, 2, 1) == "/")
        if (substr($texto, 5, 1) == "/")
            return true;
    return false;
}

function convertirImporte($importe)
{
    $importe = str_replace(",","#",$importe);
    $importe = str_replace(".",",",$importe);
    $importe = str_replace("#",".",$importe);
    return $importe;
}

function convertirFecha($fecha)
{
    $arrayFecha = explode("/", $fecha);
    $nuevaFecha = $arrayFecha[1]."/".$arrayFecha[0]."/".$arrayFecha[2];
    return $nuevaFecha;
}

function crearTabla($nombreTabla)
{
    scraperwiki::sqliteexecute("create table ".$nombreTabla." (idContrato int, `fecha` string, `objeto` string, `importe` string, `adjudicatario` string, `NIF` string)");
    scraperwiki::sqlitecommit();
}

function insertar($nombreTabla, $idContrato, $fecha, $objeto, $importe, $adjudicatario, $NIF)
{
    scraperwiki::sqliteexecute("insert into ".$nombreTabla." values (?,?,?,?,?,?)", array($idContrato, $fecha, utf8_decode($objeto), $importe, utf8_decode($adjudicatario), $NIF));
    scraperwiki::sqlitecommit();
}

$nombreTabla = "contratos4T2012";
crearTabla($nombreTabla);

$arrayPDF = array("https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_2_1.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_30_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_31_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_32_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_33_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_34_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_35_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_36_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5000.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5001.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5002.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5003.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5004.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5005.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5006.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5007.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_50_5008.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_51_5101.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_51_15101.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_53_5301.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_61_1.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_61_6101.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_63_6301.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_64_16401.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_65_3.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_65_4.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_65_5.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_67_6701.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_2.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_4.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_6.pdf",
"https://dl.dropboxusercontent.com/u/71960705/Contratos%20Menores%20Junta/Q3%202012/2012_3_69_8.pdf");

$idContrato = 1;

foreach($arrayPDF as $src_pdf) {

    # Some temporary files
    $pdf_f = tempnam('/tmp', 'inp') . '.pdf';
    $xml_f = tempnam('/tmp', 'out') . '.xml';

    # Download the PDF into a temporary file
    file_put_contents($pdf_f, file_get_contents($src_pdf));

    # Convert the PDF to XML
    $cmd = '/usr/bin/pdftohtml -xml -nodrm -zoom 1.5 -enc UTF-8 -noframes "' . $pdf_f . '" "'. $xml_f .'" >/dev/null 2>&1';
    system($cmd);

    # Load the XML and parse it.
    $xml = new SimpleXMLElement( file_get_contents($xml_f) );

    $objeto = "";
    $adjudicatario = "";
    $registro= array();

    foreach( $xml->page as $page) {
        $contadorElementos = 0;
        foreach( $page->text as $txt) {
            if ( strlen( trim($txt) ) > 3 && trim($txt) != "/" )
            {
                if ($contadorElementos == 0 && esImporte($txt))
                    $contadorElementos = 1;
                if ($contadorElementos == 3 && esFecha($txt))
                    $contadorElementos = 4;
                switch ($contadorElementos)
                {
                    case 0:
                        if (trim($txt) != "Hoja")
                            $objeto .= $txt." ";
                        break;
                    case 1:
                        $importe = $txt;
                        $contadorElementos = 2;
                        break;
                    case 2:
                        $NIF = $txt;
                        $contadorElementos = 3;
                        break;
                    case 3:
                        $adjudicatario .= $txt." ";
                        break;
                    case 4:
                        $fecha = convertirFecha($txt);
                        $contadorElementos = 6;
                        break;
                    case 6:
                        // Se inserta en la bd.
                       
                        $fecha = utf8_encode($fecha);
                        $objeto = utf8_encode($objeto);
                        $importe = utf8_encode(convertirImporte($importe));
                        $adjudicatario = utf8_encode($adjudicatario);
                        $NIF = utf8_encode($NIF);
                        insertar($nombreTabla, $idContrato, $fecha, $objeto, $importe, $adjudicatario, $NIF);
                        $idContrato++;
                        
                        if (trim($txt) != "Hoja")
                            $objeto = $txt." ";
                        $adjudicatario = "";
                        $contadorElementos = 0;
                        break;
                    default:
                        print "NO ENTRA NUNCA. Elemento: ".$contadorElementos."\n";
                        break;
                }
            }
        }
    }
}
?>