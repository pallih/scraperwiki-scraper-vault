<?php
function scrape($viewstate, $event_validation) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.bmfbovespa.com.br/corretoras/BolsaDeValores.aspx?idioma=en-us',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__EVENTTARGET'  => 'ctl00:contentPlaceHolderConteudo:tabStripPesquisa',
            '__EVENTARGUMENT' => 'ctl00$contentPlaceHolderConteudo$tabStripPesquisa$tabTodos',
            '__VIEWSTATE' => $viewstate,
            'ctl00$ucTopo$btnBusca' => 'Search',
            'ctl00$menuBOVESPASecundario' => '',
            'ctl00_contentPlaceHolderConteudo_AjaxPanel3PostDataValue' => 'ctl00_contentPlaceHolderConteudo_AjaxPanel3,ActiveElement,ctl00_bovespa;',
            'ctl00$contentPlaceHolderConteudo$tabStripPesquisa' => '{"State":{"SelectedIndex":2},"TabState":{"ctl00_contentPlaceHolderConteudo_tabStripPesquisa_tabNome":{"Selected":false},"ctl00_contentPlaceHolderConteudo_tabStripPesquisa_tabTodos":{"Selected":true}}}',
            'ctl00_contentPlaceHolderConteudo_ajxPnlBuscaNomePostDataValue' => '',
            'ctl00$contentPlaceHolderConteudo$txtNomeEmpresa$txtNomeEmpresa' => '',
            'ctl00_contentPlaceHolderConteudo_ajxPnlLocalFormPostDataValue' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_Input' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_value' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_text' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_clientWidth' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_clientHeight' => '',
            'ctl00_contentPlaceHolderConteudo_AjaxPanel2PostDataValue' => '',
            'ctl00$contentPlaceHolderConteudo$mpgBusca_Selected' => '2',
            '__EVENTVALIDATION' => $event_validation,
            'RadAJAXControlID' => 'ctl00_contentPlaceHolderConteudo_AjaxPanel3',
            'httprequest' => 'true'
        )),
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $rows = $xpath->query('//div[@class="formulario"]/div');
    $n = $rows->length;
    $xpath = null;
    unset($xpath);
    $results = array();
    for ($i = 3; $i < $n; $i++) {
        $row = $rows->item($i);
        if ($a = @$row->getElementsByTagName('a')->item(0)) {
            $url = @$a->getAttribute('href');
            $broker = @$a->nodeValue;
        } else {
            $url = null;
            $broker = null;
        }
        $category = preg_replace('/Category:\s+/i', '', $row->getElementsByTagName('p')->item(0)->childNodes->item(3)->nodeValue);
        $row = $rows->item($i)->getElementsByTagName('span');
        array_push($results, array(
            'broker' => trim(@$broker),
            'href' => @$url,
            'category' => trim($category),
            'address' => trim(@$row->item(1)->nodeValue) .' '. trim(@$row->item(2)->nodeValue) .' '. trim(@$row->item(3)->nodeValue) .' '. trim(@$row->item(4)->nodeValue) .' '. trim(@$row->item(5)->nodeValue) .' '. trim(@$row->item(6)->nodeValue),
            'contact_1' => trim(@$row->item(7)->nodeValue),
            'contact_2' => trim(@$row->item(8)->nodeValue),
            'contact_3' => trim(@$row->item(9)->nodeValue),
            'contact_4' => trim(@$row->item(10)->nodeValue),
        ));
    }
    scraperwiki::save_sqlite(array('broker'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
}

$dom = new DOMDocument();
@$dom->loadHTML(scraperwiki::scrape('http://www.bmfbovespa.com.br/corretoras/BolsaDeValores.aspx?idioma=en-us'));
$xpath = new DOMXPath($dom);
$viewstate = trim($xpath->query('//input[@name="__VIEWSTATE"]')->item(0)->getAttribute('value'));
$event_validation = trim($xpath->query('//input[@name="__EVENTVALIDATION"]')->item(0)->getAttribute('value'));
scrape($viewstate, $event_validation);
?><?php
function scrape($viewstate, $event_validation) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.bmfbovespa.com.br/corretoras/BolsaDeValores.aspx?idioma=en-us',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__EVENTTARGET'  => 'ctl00:contentPlaceHolderConteudo:tabStripPesquisa',
            '__EVENTARGUMENT' => 'ctl00$contentPlaceHolderConteudo$tabStripPesquisa$tabTodos',
            '__VIEWSTATE' => $viewstate,
            'ctl00$ucTopo$btnBusca' => 'Search',
            'ctl00$menuBOVESPASecundario' => '',
            'ctl00_contentPlaceHolderConteudo_AjaxPanel3PostDataValue' => 'ctl00_contentPlaceHolderConteudo_AjaxPanel3,ActiveElement,ctl00_bovespa;',
            'ctl00$contentPlaceHolderConteudo$tabStripPesquisa' => '{"State":{"SelectedIndex":2},"TabState":{"ctl00_contentPlaceHolderConteudo_tabStripPesquisa_tabNome":{"Selected":false},"ctl00_contentPlaceHolderConteudo_tabStripPesquisa_tabTodos":{"Selected":true}}}',
            'ctl00_contentPlaceHolderConteudo_ajxPnlBuscaNomePostDataValue' => '',
            'ctl00$contentPlaceHolderConteudo$txtNomeEmpresa$txtNomeEmpresa' => '',
            'ctl00_contentPlaceHolderConteudo_ajxPnlLocalFormPostDataValue' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_Input' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_value' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_text' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_clientWidth' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_clientHeight' => '',
            'ctl00_contentPlaceHolderConteudo_AjaxPanel2PostDataValue' => '',
            'ctl00$contentPlaceHolderConteudo$mpgBusca_Selected' => '2',
            '__EVENTVALIDATION' => $event_validation,
            'RadAJAXControlID' => 'ctl00_contentPlaceHolderConteudo_AjaxPanel3',
            'httprequest' => 'true'
        )),
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $rows = $xpath->query('//div[@class="formulario"]/div');
    $n = $rows->length;
    $xpath = null;
    unset($xpath);
    $results = array();
    for ($i = 3; $i < $n; $i++) {
        $row = $rows->item($i);
        if ($a = @$row->getElementsByTagName('a')->item(0)) {
            $url = @$a->getAttribute('href');
            $broker = @$a->nodeValue;
        } else {
            $url = null;
            $broker = null;
        }
        $category = preg_replace('/Category:\s+/i', '', $row->getElementsByTagName('p')->item(0)->childNodes->item(3)->nodeValue);
        $row = $rows->item($i)->getElementsByTagName('span');
        array_push($results, array(
            'broker' => trim(@$broker),
            'href' => @$url,
            'category' => trim($category),
            'address' => trim(@$row->item(1)->nodeValue) .' '. trim(@$row->item(2)->nodeValue) .' '. trim(@$row->item(3)->nodeValue) .' '. trim(@$row->item(4)->nodeValue) .' '. trim(@$row->item(5)->nodeValue) .' '. trim(@$row->item(6)->nodeValue),
            'contact_1' => trim(@$row->item(7)->nodeValue),
            'contact_2' => trim(@$row->item(8)->nodeValue),
            'contact_3' => trim(@$row->item(9)->nodeValue),
            'contact_4' => trim(@$row->item(10)->nodeValue),
        ));
    }
    scraperwiki::save_sqlite(array('broker'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
}

$dom = new DOMDocument();
@$dom->loadHTML(scraperwiki::scrape('http://www.bmfbovespa.com.br/corretoras/BolsaDeValores.aspx?idioma=en-us'));
$xpath = new DOMXPath($dom);
$viewstate = trim($xpath->query('//input[@name="__VIEWSTATE"]')->item(0)->getAttribute('value'));
$event_validation = trim($xpath->query('//input[@name="__EVENTVALIDATION"]')->item(0)->getAttribute('value'));
scrape($viewstate, $event_validation);
?><?php
function scrape($viewstate, $event_validation) {
    $ch = curl_init();
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.bmfbovespa.com.br/corretoras/BolsaDeValores.aspx?idioma=en-us',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => http_build_query(array(
            '__EVENTTARGET'  => 'ctl00:contentPlaceHolderConteudo:tabStripPesquisa',
            '__EVENTARGUMENT' => 'ctl00$contentPlaceHolderConteudo$tabStripPesquisa$tabTodos',
            '__VIEWSTATE' => $viewstate,
            'ctl00$ucTopo$btnBusca' => 'Search',
            'ctl00$menuBOVESPASecundario' => '',
            'ctl00_contentPlaceHolderConteudo_AjaxPanel3PostDataValue' => 'ctl00_contentPlaceHolderConteudo_AjaxPanel3,ActiveElement,ctl00_bovespa;',
            'ctl00$contentPlaceHolderConteudo$tabStripPesquisa' => '{"State":{"SelectedIndex":2},"TabState":{"ctl00_contentPlaceHolderConteudo_tabStripPesquisa_tabNome":{"Selected":false},"ctl00_contentPlaceHolderConteudo_tabStripPesquisa_tabTodos":{"Selected":true}}}',
            'ctl00_contentPlaceHolderConteudo_ajxPnlBuscaNomePostDataValue' => '',
            'ctl00$contentPlaceHolderConteudo$txtNomeEmpresa$txtNomeEmpresa' => '',
            'ctl00_contentPlaceHolderConteudo_ajxPnlLocalFormPostDataValue' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_Input' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_value' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_text' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_clientWidth' => '',
            'ctl00$contentPlaceHolderConteudo$ddlEstados$ddlEstados_clientHeight' => '',
            'ctl00_contentPlaceHolderConteudo_AjaxPanel2PostDataValue' => '',
            'ctl00$contentPlaceHolderConteudo$mpgBusca_Selected' => '2',
            '__EVENTVALIDATION' => $event_validation,
            'RadAJAXControlID' => 'ctl00_contentPlaceHolderConteudo_AjaxPanel3',
            'httprequest' => 'true'
        )),
        CURLOPT_CONNECTTIMEOUT => 0,
        CURLOPT_TIMEOUT => 1000,
    ));

    echo "Loading data ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $rows = $xpath->query('//div[@class="formulario"]/div');
    $n = $rows->length;
    $xpath = null;
    unset($xpath);
    $results = array();
    for ($i = 3; $i < $n; $i++) {
        $row = $rows->item($i);
        if ($a = @$row->getElementsByTagName('a')->item(0)) {
            $url = @$a->getAttribute('href');
            $broker = @$a->nodeValue;
        } else {
            $url = null;
            $broker = null;
        }
        $category = preg_replace('/Category:\s+/i', '', $row->getElementsByTagName('p')->item(0)->childNodes->item(3)->nodeValue);
        $row = $rows->item($i)->getElementsByTagName('span');
        array_push($results, array(
            'broker' => trim(@$broker),
            'href' => @$url,
            'category' => trim($category),
            'address' => trim(@$row->item(1)->nodeValue) .' '. trim(@$row->item(2)->nodeValue) .' '. trim(@$row->item(3)->nodeValue) .' '. trim(@$row->item(4)->nodeValue) .' '. trim(@$row->item(5)->nodeValue) .' '. trim(@$row->item(6)->nodeValue),
            'contact_1' => trim(@$row->item(7)->nodeValue),
            'contact_2' => trim(@$row->item(8)->nodeValue),
            'contact_3' => trim(@$row->item(9)->nodeValue),
            'contact_4' => trim(@$row->item(10)->nodeValue),
        ));
    }
    scraperwiki::save_sqlite(array('broker'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
}

$dom = new DOMDocument();
@$dom->loadHTML(scraperwiki::scrape('http://www.bmfbovespa.com.br/corretoras/BolsaDeValores.aspx?idioma=en-us'));
$xpath = new DOMXPath($dom);
$viewstate = trim($xpath->query('//input[@name="__VIEWSTATE"]')->item(0)->getAttribute('value'));
$event_validation = trim($xpath->query('//input[@name="__EVENTVALIDATION"]')->item(0)->getAttribute('value'));
scrape($viewstate, $event_validation);
?>