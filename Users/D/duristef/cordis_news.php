<?php
require 'scraperwiki/simple_html_dom.php';

$res = scraperwiki::select("max(fonte_num) from swdata");
// ultimo RCN da cercare
$last_rcn = empty($res)? null : $res[0]['max(fonte_num)']+1;
// minor RCN trovato in home page
$start_rcn = null;
// max numero di RCN da cercare in caso di assenza di dati in swdata
$back = 50;

/* fonte */
$id_fonte = 7;
$db_primarykey = array('fonte_num');
$base_url = "http://cordis.europa.eu/";
$home_url = $base_url."news/home_it.html";
$news_url = $base_url."fetch?CALLER=IT_NEWS&ACTION=D&CAT=NEWS&RCN=%d";
$page_url = $base_url.'fetch?CALLER=IT_NEWS&QP_EN_QVD=EN_QVD+%3E%3D+date+%27sysdate-7D%27%3Buna+settimana&DOC=1&QUERY=01195b67a8af:53e9:25f13118';

/* get news from home page */
$home_file = file_get_html($home_url);
if(!empty($home_file)) {
    $home_dom = str_get_html($home_file);
    if($home_dom) {
        $table_news = $home_dom->find('table.news .subtitle a');
        foreach ($table_news as $a) {
            $num = preg_replace("/^.+RCN\=(\d+)[^\d]*$/", "$1", $a->href);
            $r = get1news($num);
            if(!empty($r)) {
                $start_rcn = ($start_rcn? min($start_rcn, $r['fonte_num']):$r['fonte_num']);
                scraperwiki::save($db_primarykey, $r);
            }
        }
        if(!$start_rcn) exit("Problemi di collegamento - ritentare");

        $start_rcn--;
        if (empty($last_rcn)) $last_rcn = $start_rcn - $back; 
        $last_rcn++;
        for ($i = $start_rcn; $i>=$last_rcn; $i--) {
            $r = get1news($i);
            if(!empty($r)) scraperwiki::save($db_primarykey, $r);
        }
    }
}

function get1news($fonte_num) {
    global $id_fonte, $news_url;
    $r = array();
    $news_href = sprintf($news_url, $fonte_num);
    $news_dom = str_get_html( file_get_html($news_href) );
    if($news_dom) {
        $r['id_fonte'] = $id_fonte;
        $r['fonte_num'] = $fonte_num;
        $r['titolo'] = $news_dom->find('#general h4',0)->plaintext;
        $r['fonte_data'] = preg_replace('/^[^\d]+(\d+)\-(\d+)\-(\d+).*/', '$2-$3-$1',$news_dom->find('#general p.date',0)->plaintext);
        $text = array();
        foreach($news_dom->find('#general p[align=justify]') as $p) {
            $text[] = $p->plaintext;
        }
        $r['testo'] = implode("\n", $text);
        $inner = $news_dom->find('#general',0)->innertext;
        if(preg_match('#<strong>Categoria:</strong> (.+?)<br#',$inner, $matches)) $r['categoria'] = $matches[1];
        if(preg_match('#<strong>Fonte:</strong> (.+?)<br#',$inner, $matches)) $r['fonte'] = $matches[1];
        if(preg_match('#<strong>Documenti di Riferimento:</strong> (.+?)<br#',$inner, $matches)) $r['docrif'] = $matches[1];
        if(preg_match('#<strong>Acronimi dei Programmi:</strong> (.+?)<br#',$inner, $matches)) $r['programmi'] = $matches[1];
        if($r['programmi']) $r['programmi'] = preg_replace('#<[^>]+>#is', " ",$r['programmi']);
        if(preg_match('#<strong>Codici di Classificazione per Materia:</strong> (.+?)(</p>|<br)#',$inner, $matches)) $r['descrittori'] = $matches[1];
        $r['testo'] .= "<br>Fonte: {$r['fonte']}<br>Documenti di Riferimento: {$r['docrif']}<br>Tipo di notizia: {$r['categoria']}";
        foreach($r as $k=>$v) {
            $r[$k] = trim(nl2br($r[$k]));
            $r[$k] = preg_replace('#\s{2,}#s',' ',$r[$k] );
            $r[$k] = preg_replace('#(<br />){2,}#s','<br />',$r[$k] );
            $r[$k] = preg_replace('#(<br />)+$#s','',$r[$k] );
            $r[$k] = preg_replace('#<br />\n#s','<br />',$r[$k] );
            $r[$k] = preg_replace('#<br />(\n|\s)+<br />#s','<br />',$r[$k] );
            $r[$k] = preg_replace('#(<br />)+#s','<br />',$r[$k] );
        }
    }
    return $r;
}
?>
<?php
require 'scraperwiki/simple_html_dom.php';

$res = scraperwiki::select("max(fonte_num) from swdata");
// ultimo RCN da cercare
$last_rcn = empty($res)? null : $res[0]['max(fonte_num)']+1;
// minor RCN trovato in home page
$start_rcn = null;
// max numero di RCN da cercare in caso di assenza di dati in swdata
$back = 50;

/* fonte */
$id_fonte = 7;
$db_primarykey = array('fonte_num');
$base_url = "http://cordis.europa.eu/";
$home_url = $base_url."news/home_it.html";
$news_url = $base_url."fetch?CALLER=IT_NEWS&ACTION=D&CAT=NEWS&RCN=%d";
$page_url = $base_url.'fetch?CALLER=IT_NEWS&QP_EN_QVD=EN_QVD+%3E%3D+date+%27sysdate-7D%27%3Buna+settimana&DOC=1&QUERY=01195b67a8af:53e9:25f13118';

/* get news from home page */
$home_file = file_get_html($home_url);
if(!empty($home_file)) {
    $home_dom = str_get_html($home_file);
    if($home_dom) {
        $table_news = $home_dom->find('table.news .subtitle a');
        foreach ($table_news as $a) {
            $num = preg_replace("/^.+RCN\=(\d+)[^\d]*$/", "$1", $a->href);
            $r = get1news($num);
            if(!empty($r)) {
                $start_rcn = ($start_rcn? min($start_rcn, $r['fonte_num']):$r['fonte_num']);
                scraperwiki::save($db_primarykey, $r);
            }
        }
        if(!$start_rcn) exit("Problemi di collegamento - ritentare");

        $start_rcn--;
        if (empty($last_rcn)) $last_rcn = $start_rcn - $back; 
        $last_rcn++;
        for ($i = $start_rcn; $i>=$last_rcn; $i--) {
            $r = get1news($i);
            if(!empty($r)) scraperwiki::save($db_primarykey, $r);
        }
    }
}

function get1news($fonte_num) {
    global $id_fonte, $news_url;
    $r = array();
    $news_href = sprintf($news_url, $fonte_num);
    $news_dom = str_get_html( file_get_html($news_href) );
    if($news_dom) {
        $r['id_fonte'] = $id_fonte;
        $r['fonte_num'] = $fonte_num;
        $r['titolo'] = $news_dom->find('#general h4',0)->plaintext;
        $r['fonte_data'] = preg_replace('/^[^\d]+(\d+)\-(\d+)\-(\d+).*/', '$2-$3-$1',$news_dom->find('#general p.date',0)->plaintext);
        $text = array();
        foreach($news_dom->find('#general p[align=justify]') as $p) {
            $text[] = $p->plaintext;
        }
        $r['testo'] = implode("\n", $text);
        $inner = $news_dom->find('#general',0)->innertext;
        if(preg_match('#<strong>Categoria:</strong> (.+?)<br#',$inner, $matches)) $r['categoria'] = $matches[1];
        if(preg_match('#<strong>Fonte:</strong> (.+?)<br#',$inner, $matches)) $r['fonte'] = $matches[1];
        if(preg_match('#<strong>Documenti di Riferimento:</strong> (.+?)<br#',$inner, $matches)) $r['docrif'] = $matches[1];
        if(preg_match('#<strong>Acronimi dei Programmi:</strong> (.+?)<br#',$inner, $matches)) $r['programmi'] = $matches[1];
        if($r['programmi']) $r['programmi'] = preg_replace('#<[^>]+>#is', " ",$r['programmi']);
        if(preg_match('#<strong>Codici di Classificazione per Materia:</strong> (.+?)(</p>|<br)#',$inner, $matches)) $r['descrittori'] = $matches[1];
        $r['testo'] .= "<br>Fonte: {$r['fonte']}<br>Documenti di Riferimento: {$r['docrif']}<br>Tipo di notizia: {$r['categoria']}";
        foreach($r as $k=>$v) {
            $r[$k] = trim(nl2br($r[$k]));
            $r[$k] = preg_replace('#\s{2,}#s',' ',$r[$k] );
            $r[$k] = preg_replace('#(<br />){2,}#s','<br />',$r[$k] );
            $r[$k] = preg_replace('#(<br />)+$#s','',$r[$k] );
            $r[$k] = preg_replace('#<br />\n#s','<br />',$r[$k] );
            $r[$k] = preg_replace('#<br />(\n|\s)+<br />#s','<br />',$r[$k] );
            $r[$k] = preg_replace('#(<br />)+#s','<br />',$r[$k] );
        }
    }
    return $r;
}
?>
