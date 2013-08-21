<?php
require 'scraperwiki/simple_html_dom.php';
    
$dom = new simple_html_dom();

for ($i = 1; $i<40; $i++) {
    $uri = "http://www.publidata.es/productoras/" . $i;
    $html = scraperwiki::scrape($uri);
    $uribase = "http://www.publidata.es/";
    

    $dom->load($html);
    
    $rows=$dom->find("span[class=tituloEmp]");
    
    foreach($rows as $row) {
        $urlnode = $row->find("a",0);
        $urinode = "http://www.publidata.es" . $urlnode->href;
        #print $urinode . "\n";
        $htmlnode = scraperwiki::scrape($urinode);
    
        $dom2 = new simple_html_dom();
        $dom2->load($htmlnode);
    
        $nombre = strip_tags($dom2->find("div[class=moduleContent3]",0)->find("h1",0));

    
        $rows2=$dom2->find("dl[class=datosGenerales]");
    
        foreach($rows2 as $row2) {
            $direccion = explode("<br />", $row2->find("dd[class=direccionDef]",0));
            $dir1 = strip_tags($direccion[0]);
            $dir2 = strip_tags($direccion[1]);
            $dir3 = strip_tags($direccion[2]);
            $tel = $row2->find("dt[class=telefono]",0);
            $telefono = "";
            if ($tel)
                $telefono = strip_tags($row2->find("dt[class=telefono]",0)->next_sibling ());
            $email = strip_tags($row2->find("dd[class=email]",0));
            $website = strip_tags($row2->find("dd[class=web]",0));

        }
    
        $record = array(
            'nom' => $nombre,
            'web' => $website,
            'e-mail' => $email,
            'telf' => $telefono,
            'dir1' => $dir1,
            'dir2' => $dir2,
            'dir3' => $dir3,
            'source' => $urinode
        );
        scraperwiki::save(array('nom'), $record);       
    }
}
?>

