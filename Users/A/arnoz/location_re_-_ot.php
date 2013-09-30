<?php



require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.locations-ile-re.com/voir-toutes-les-locations?offset=1&dispo_start=03/08/2013&dispo_end=10/08/2013&nb_pers=4&show=100&nb_pers_sort=desc&mode=oi");
$image = array();
$offre = array();

$dom = new simple_html_dom();
$dom->load($html);


        
        foreach($dom->find('div.ofev') as $annonce) {
            $offre['id' ] =  substr ( $annonce->id , 6 , strlen ($annonce->id) )  ;
            $offre['adresse'] = $annonce->find('div[class=adr-features]', 0)->plaintext;

            if ( strpos ( $offre['adresse'],"COUARDE")!==FALSE) { $offre['ville']="LA COUARDE"; }
            if ( strpos ( $offre['adresse'],"ARS")!==FALSE) { $offre['ville']="ARS EN RE"; }
            if ( strpos ( $offre['adresse'],"LES PORTES")!==FALSE) { $offre['ville']="LES PORTES"; }
            if ( strpos ( $offre['adresse'],"CLEMENT")!==FALSE) { $offre['ville']="ST CLEMENT"; }
            if ( strpos ( $offre['adresse'],"PLAGE")!==FALSE) { $offre['ville']="BOIS PLAGE"; }
            //$offre['url'] = $annonce->find('a', 0);
            //$offre['url'] = $offre['url']->href->plaintext;
            $offre['titre'] = $annonce->find('h2[class=title]', 0);
            $offre['prix_max'] = $annonce->find('div[class=price]', 0);
            $offre['prix_max'] = $offre['prix_max']->find('span[class=max-val]', 0)->plaintext;
            $offre['prix_max'] =rtrim($offre['prix_max'],'€');
            //$image = $image->find('img',0);
            //$offre['image'] = $image->src;
            $offres_en_cours[$offre['id']] = $offre;
                if ($offre['prix_max'] <=1400 && $offre['prix_max'] >0) {
                            print_r($offre);
                            scraperwiki::save(array('id'),$offre);
                }
        }






?>
<?php



require  'scraperwiki/simple_html_dom.php';
$html = scraperwiki::scrape("http://www.locations-ile-re.com/voir-toutes-les-locations?offset=1&dispo_start=03/08/2013&dispo_end=10/08/2013&nb_pers=4&show=100&nb_pers_sort=desc&mode=oi");
$image = array();
$offre = array();

$dom = new simple_html_dom();
$dom->load($html);


        
        foreach($dom->find('div.ofev') as $annonce) {
            $offre['id' ] =  substr ( $annonce->id , 6 , strlen ($annonce->id) )  ;
            $offre['adresse'] = $annonce->find('div[class=adr-features]', 0)->plaintext;

            if ( strpos ( $offre['adresse'],"COUARDE")!==FALSE) { $offre['ville']="LA COUARDE"; }
            if ( strpos ( $offre['adresse'],"ARS")!==FALSE) { $offre['ville']="ARS EN RE"; }
            if ( strpos ( $offre['adresse'],"LES PORTES")!==FALSE) { $offre['ville']="LES PORTES"; }
            if ( strpos ( $offre['adresse'],"CLEMENT")!==FALSE) { $offre['ville']="ST CLEMENT"; }
            if ( strpos ( $offre['adresse'],"PLAGE")!==FALSE) { $offre['ville']="BOIS PLAGE"; }
            //$offre['url'] = $annonce->find('a', 0);
            //$offre['url'] = $offre['url']->href->plaintext;
            $offre['titre'] = $annonce->find('h2[class=title]', 0);
            $offre['prix_max'] = $annonce->find('div[class=price]', 0);
            $offre['prix_max'] = $offre['prix_max']->find('span[class=max-val]', 0)->plaintext;
            $offre['prix_max'] =rtrim($offre['prix_max'],'€');
            //$image = $image->find('img',0);
            //$offre['image'] = $image->src;
            $offres_en_cours[$offre['id']] = $offre;
                if ($offre['prix_max'] <=1400 && $offre['prix_max'] >0) {
                            print_r($offre);
                            scraperwiki::save(array('id'),$offre);
                }
        }






?>
