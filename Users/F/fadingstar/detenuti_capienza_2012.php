<?php
/*

    31 gennaio 2012
 
    Detenuti presenti e capienza regolamentare degli istituti penitenziari per regione di detenzione

    Situazione al 31 gennaio 2012

    Nota su totale_detenuti_semiliberta: i detenuti presenti in semilibertà sono compresi nel totale dei detenuti presenti

    Fonte: Dipartimento dell'amministrazione penitenziaria
           Ufficio per lo sviluppo e la gestione del sistema informativo automatizzato statistica ed automazione di supporto dipartimentale
           Sezione Statistica

*/

// XPATH example

/*
print_r(scraperwiki::show_tables());
scraperwiki::sqliteexecute("drop table if exists detenuti_regioni_italiane");
print_r(scraperwiki::show_tables());
*/

var_dump(libxml_use_internal_errors(true));

$url = scraperWiki::scrape("http://www.giustizia.it/giustizia/it/mg_1_14_1.wp?facetNode_1=1_5_29&previsiousPage=mg_1_14&contentId=SST729064");

$doc = new DOMDocument;
$doc->loadHTML($url);

$xpath = new DOMXpath($doc);

$regione = $xpath->query("/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr");


for ( $i=2; $i <= 21; $i++)
{
    $arr = explode("\n", $regione->item($i)->nodeValue);
    $nome_regione = $arr[0];
    $numero_istituti = $arr[1];
    $capienza_regolamentare = $arr[2];
    $totale_detenuti_presenti = $arr[3];
    $donne_detenuti_presenti = $arr[4];
    $stranieri_detenuti_presenti = $arr[5];
    $totale_detenuti_semiliberta = $arr[6];
    $stranieri_detenuti_semiliberta = $arr[7];
        
    $record = array(        "regione" => trim($nome_regione),
                            "numero_istituti" => trim($numero_istituti),
                            "capienza_regolamentare" => trim($capienza_regolamentare),
                            "totale_detenuti_presenti" => trim($totale_detenuti_presenti),
                            "donne_detenuti_presenti" => trim($donne_detenuti_presenti),
                            "stranieri_detenuti_presenti" => trim($stranieri_detenuti_presenti),
                            "totale_detenuti_semiliberta" => trim($totale_detenuti_semiliberta),
                            "stranieri_detenuti_semiliberta" => trim($stranieri_detenuti_semiliberta));
                
    scraperwiki::save_sqlite(array("regione"), $record, $table_name="detenuti_regioni_italiane");

}


print "\nScraping - 100% complete.\n"

?>
<?php
/*

    31 gennaio 2012
 
    Detenuti presenti e capienza regolamentare degli istituti penitenziari per regione di detenzione

    Situazione al 31 gennaio 2012

    Nota su totale_detenuti_semiliberta: i detenuti presenti in semilibertà sono compresi nel totale dei detenuti presenti

    Fonte: Dipartimento dell'amministrazione penitenziaria
           Ufficio per lo sviluppo e la gestione del sistema informativo automatizzato statistica ed automazione di supporto dipartimentale
           Sezione Statistica

*/

// XPATH example

/*
print_r(scraperwiki::show_tables());
scraperwiki::sqliteexecute("drop table if exists detenuti_regioni_italiane");
print_r(scraperwiki::show_tables());
*/

var_dump(libxml_use_internal_errors(true));

$url = scraperWiki::scrape("http://www.giustizia.it/giustizia/it/mg_1_14_1.wp?facetNode_1=1_5_29&previsiousPage=mg_1_14&contentId=SST729064");

$doc = new DOMDocument;
$doc->loadHTML($url);

$xpath = new DOMXpath($doc);

$regione = $xpath->query("/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr");


for ( $i=2; $i <= 21; $i++)
{
    $arr = explode("\n", $regione->item($i)->nodeValue);
    $nome_regione = $arr[0];
    $numero_istituti = $arr[1];
    $capienza_regolamentare = $arr[2];
    $totale_detenuti_presenti = $arr[3];
    $donne_detenuti_presenti = $arr[4];
    $stranieri_detenuti_presenti = $arr[5];
    $totale_detenuti_semiliberta = $arr[6];
    $stranieri_detenuti_semiliberta = $arr[7];
        
    $record = array(        "regione" => trim($nome_regione),
                            "numero_istituti" => trim($numero_istituti),
                            "capienza_regolamentare" => trim($capienza_regolamentare),
                            "totale_detenuti_presenti" => trim($totale_detenuti_presenti),
                            "donne_detenuti_presenti" => trim($donne_detenuti_presenti),
                            "stranieri_detenuti_presenti" => trim($stranieri_detenuti_presenti),
                            "totale_detenuti_semiliberta" => trim($totale_detenuti_semiliberta),
                            "stranieri_detenuti_semiliberta" => trim($stranieri_detenuti_semiliberta));
                
    scraperwiki::save_sqlite(array("regione"), $record, $table_name="detenuti_regioni_italiane");

}


print "\nScraping - 100% complete.\n"

?>
<?php
/*

    31 gennaio 2012
 
    Detenuti presenti e capienza regolamentare degli istituti penitenziari per regione di detenzione

    Situazione al 31 gennaio 2012

    Nota su totale_detenuti_semiliberta: i detenuti presenti in semilibertà sono compresi nel totale dei detenuti presenti

    Fonte: Dipartimento dell'amministrazione penitenziaria
           Ufficio per lo sviluppo e la gestione del sistema informativo automatizzato statistica ed automazione di supporto dipartimentale
           Sezione Statistica

*/

// XPATH example

/*
print_r(scraperwiki::show_tables());
scraperwiki::sqliteexecute("drop table if exists detenuti_regioni_italiane");
print_r(scraperwiki::show_tables());
*/

var_dump(libxml_use_internal_errors(true));

$url = scraperWiki::scrape("http://www.giustizia.it/giustizia/it/mg_1_14_1.wp?facetNode_1=1_5_29&previsiousPage=mg_1_14&contentId=SST729064");

$doc = new DOMDocument;
$doc->loadHTML($url);

$xpath = new DOMXpath($doc);

$regione = $xpath->query("/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr");


for ( $i=2; $i <= 21; $i++)
{
    $arr = explode("\n", $regione->item($i)->nodeValue);
    $nome_regione = $arr[0];
    $numero_istituti = $arr[1];
    $capienza_regolamentare = $arr[2];
    $totale_detenuti_presenti = $arr[3];
    $donne_detenuti_presenti = $arr[4];
    $stranieri_detenuti_presenti = $arr[5];
    $totale_detenuti_semiliberta = $arr[6];
    $stranieri_detenuti_semiliberta = $arr[7];
        
    $record = array(        "regione" => trim($nome_regione),
                            "numero_istituti" => trim($numero_istituti),
                            "capienza_regolamentare" => trim($capienza_regolamentare),
                            "totale_detenuti_presenti" => trim($totale_detenuti_presenti),
                            "donne_detenuti_presenti" => trim($donne_detenuti_presenti),
                            "stranieri_detenuti_presenti" => trim($stranieri_detenuti_presenti),
                            "totale_detenuti_semiliberta" => trim($totale_detenuti_semiliberta),
                            "stranieri_detenuti_semiliberta" => trim($stranieri_detenuti_semiliberta));
                
    scraperwiki::save_sqlite(array("regione"), $record, $table_name="detenuti_regioni_italiane");

}


print "\nScraping - 100% complete.\n"

?>
<?php
/*

    31 gennaio 2012
 
    Detenuti presenti e capienza regolamentare degli istituti penitenziari per regione di detenzione

    Situazione al 31 gennaio 2012

    Nota su totale_detenuti_semiliberta: i detenuti presenti in semilibertà sono compresi nel totale dei detenuti presenti

    Fonte: Dipartimento dell'amministrazione penitenziaria
           Ufficio per lo sviluppo e la gestione del sistema informativo automatizzato statistica ed automazione di supporto dipartimentale
           Sezione Statistica

*/

// XPATH example

/*
print_r(scraperwiki::show_tables());
scraperwiki::sqliteexecute("drop table if exists detenuti_regioni_italiane");
print_r(scraperwiki::show_tables());
*/

var_dump(libxml_use_internal_errors(true));

$url = scraperWiki::scrape("http://www.giustizia.it/giustizia/it/mg_1_14_1.wp?facetNode_1=1_5_29&previsiousPage=mg_1_14&contentId=SST729064");

$doc = new DOMDocument;
$doc->loadHTML($url);

$xpath = new DOMXpath($doc);

$regione = $xpath->query("/html/body/div[2]/div[2]/div[2]/div/div/div[2]/div/table/tbody/tr");


for ( $i=2; $i <= 21; $i++)
{
    $arr = explode("\n", $regione->item($i)->nodeValue);
    $nome_regione = $arr[0];
    $numero_istituti = $arr[1];
    $capienza_regolamentare = $arr[2];
    $totale_detenuti_presenti = $arr[3];
    $donne_detenuti_presenti = $arr[4];
    $stranieri_detenuti_presenti = $arr[5];
    $totale_detenuti_semiliberta = $arr[6];
    $stranieri_detenuti_semiliberta = $arr[7];
        
    $record = array(        "regione" => trim($nome_regione),
                            "numero_istituti" => trim($numero_istituti),
                            "capienza_regolamentare" => trim($capienza_regolamentare),
                            "totale_detenuti_presenti" => trim($totale_detenuti_presenti),
                            "donne_detenuti_presenti" => trim($donne_detenuti_presenti),
                            "stranieri_detenuti_presenti" => trim($stranieri_detenuti_presenti),
                            "totale_detenuti_semiliberta" => trim($totale_detenuti_semiliberta),
                            "stranieri_detenuti_semiliberta" => trim($stranieri_detenuti_semiliberta));
                
    scraperwiki::save_sqlite(array("regione"), $record, $table_name="detenuti_regioni_italiane");

}


print "\nScraping - 100% complete.\n"

?>
