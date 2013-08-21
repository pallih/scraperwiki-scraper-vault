<?php

require 'scraperwiki/simple_html_dom.php'; 
$dom = new simple_html_dom();
$urls = array();
//$urls[] = array("https://dl.acm.org/citation.cfm?id=2207676&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2012, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=1978942&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2011, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=1753326&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2010, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=1518701&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2009, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=1357054&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2008, 14);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=1240624&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2007, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=1124772&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2006, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=1054972&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2005, 0);
//ScraperWiki::sqliteexecute("delete from swdata where year=2001");
//$urls[] = array("https://dl.acm.org/citation.cfm?id=985692&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2004, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=642611&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2003, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=503376&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2002, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=365024&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 2001, 0);
$urls[] = array("https://dl.acm.org/citation.cfm?id=302979&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 1999, 0);
//$urls[] = array("https://dl.acm.org/citation.cfm?id=302979&CFID=91570192&CFTOKEN=99756614&preflayout=flat", 1998, 0);

foreach ($urls as $url)
{
    $html = scraperWiki::scrape($url[0]);
    $dom->load($html);

    $papertitle = array();
    $paperurl = array();
    $authorlist = array();
    $abstract = array();
    $d = $dom->find("tr td[colspan=1]");
    $d = array_slice($d, $url[2]); 
    foreach($d as $data)
    {
        $papertitle[] = $data->find("span a", 0)->plaintext;
        //print $data->find("span a", 0)->plaintext;
        $paperurl[] = $data->find("span a", 0)->href;
        $first_sib = $data->parent()->next_sibling();
        $authorlist[] = $first_sib->find("td span", 0)->plaintext;
        //print $first_sib->find("td span", 0)->plaintext;
    }

    //foreach($dom->find("div[style=padding-left:20]") as $data) // for 2005-12 and 2002, 2003
    foreach($dom->find("div[style=padding-left:0]") as $data)
    {
        $abstract[] = $data->find("span", 1)->plaintext;
    }

    for($i = 0;$i < count($papertitle);$i++)
    {
        $record = array(
            'paperurl' => $paperurl[$i],
            'papertitle' => $papertitle[$i],
            'authorlist' => $authorlist[$i],
            'num_authors' => count(explode(",", $authorlist[$i])),
            'abstract' => $abstract[$i],
            'year' => $url[1]
        );
        scraperwiki::save_sqlite(array('paperurl'), $record); 
    }
  
    
}
?>
