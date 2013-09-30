<?php
    # Sett inn ekstern fil med Simple HTML DOM-biblioteket:
    require "scraperwiki/simple_html_dom.php";
    # Hent HTML-koden fra nettstedet og lagre i $h:
    $h = scraperWiki::scrape("http://car.espenandersen.no/?data=1");
    # Konstruere et tomt HTML-tre og lagre objektet i $tree:
    $tree = new simple_html_dom();
    # Last HTML-koden fra nettstedet inn i HTML-treet:
    $tree->load( $h );
    # La $tbody representere <tbody>, bruk stien:    
    $tbody = $tree->find( "html body table tbody", 0 );
    # Dataradene er barn av <tbody>, kall metoden children():
    $rows = $tbody->children();
    # For hver rad blant dataradene...
    foreach( $rows as $row ) {
        # Gjør klar tom array:
        $data = array();
        # Fyll arrayen med skrapede data, feltnavn som nøkler:
        $data["id"]        = $row->find( "td", 0 )->plaintext;
        $data["skolenavn"] = $row->find( "td", 1 )->plaintext;
        $data["kommunenr"] = $row->find( "td", 2 )->plaintext;
        $data["kommune"]   = $row->find( "td", 3 )->plaintext;
        $data["inneklima"] = $row->find( "td", 4 )->plaintext;
        # Lagre dataraden (arrayen) til databasen i ScraperWiki:
        scraperWiki::save( array( "id" ), $data );
        # Fortsett med neste rad...
    }
    # Ferdig når det ikke er flere rader igjen i $rows.
?>
<?php
    # Sett inn ekstern fil med Simple HTML DOM-biblioteket:
    require "scraperwiki/simple_html_dom.php";
    # Hent HTML-koden fra nettstedet og lagre i $h:
    $h = scraperWiki::scrape("http://car.espenandersen.no/?data=1");
    # Konstruere et tomt HTML-tre og lagre objektet i $tree:
    $tree = new simple_html_dom();
    # Last HTML-koden fra nettstedet inn i HTML-treet:
    $tree->load( $h );
    # La $tbody representere <tbody>, bruk stien:    
    $tbody = $tree->find( "html body table tbody", 0 );
    # Dataradene er barn av <tbody>, kall metoden children():
    $rows = $tbody->children();
    # For hver rad blant dataradene...
    foreach( $rows as $row ) {
        # Gjør klar tom array:
        $data = array();
        # Fyll arrayen med skrapede data, feltnavn som nøkler:
        $data["id"]        = $row->find( "td", 0 )->plaintext;
        $data["skolenavn"] = $row->find( "td", 1 )->plaintext;
        $data["kommunenr"] = $row->find( "td", 2 )->plaintext;
        $data["kommune"]   = $row->find( "td", 3 )->plaintext;
        $data["inneklima"] = $row->find( "td", 4 )->plaintext;
        # Lagre dataraden (arrayen) til databasen i ScraperWiki:
        scraperWiki::save( array( "id" ), $data );
        # Fortsett med neste rad...
    }
    # Ferdig når det ikke er flere rader igjen i $rows.
?>
