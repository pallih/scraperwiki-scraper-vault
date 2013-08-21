<?php

require 'scraperwiki/simple_html_dom.php';

$dom = new simple_html_dom();

//page URLs
$url[0] = 'http://www.user-agents.org/index.shtml';
$url[1] = 'http://www.user-agents.org/index.shtml?g_m';
$url[2] = 'http://www.user-agents.org/index.shtml?moz';
$url[3] = 'http://www.user-agents.org/index.shtml?n_s';
$url[4] = 'http://www.user-agents.org/index.shtml?t_z';

//crawl pages
function crawlAgents($pageUrl, $domObj){
    $html = scraperwiki::scrape($pageUrl);
    $domObj->load($html);
    $html = null;
    $table = $domObj->find('/html/body/table[5]');

    foreach($table[0]->find('tr') as $trs){
        if(strpos($trs->firstChild()->plaintext," String ") == false){
            $tds = $trs->find('td');
            $agentstring = str_replace('&nbsp;','',$tds[0]->plaintext);
            $agentdescription = str_replace('&nbsp;','',$tds[1]->plaintext);
            $agenttype = str_replace('&nbsp;','',$tds[2]->plaintext);
            $record = array('agent' => $agentstring , 'description' => $agentdescription, 'agent_type' => $agenttype);
            scraperwiki::save_sqlite(array('agent'), $record, $table_name="UserAgents");
        }
    }
}

foreach($url as $nextUrl){
    crawlAgents($nextUrl, $dom);
}
?>
