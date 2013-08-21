<?php
function scrape($category, $viewstate) {
    $ch = curl_init();
    $post = array(
        '__EVENTTARGET' => 'ctl00$contentPlaceHolderConteudo$tabAgentes',
        '__EVENTARGUMENT' => '',
        '__VIEWSTATE' => $viewstate,
        'ctl00$ucTopo$btnBusca' => 'Search',
        'ctl00$menuBOVESPASecundario' => '',
        'ctl00$contentPlaceHolderConteudo$tabAgentes' => '',
        'ctl00$contentPlaceHolderConteudo$mpgAgentes_Selected' => ''
    );
    if ($category == 'Self-Clearing Houses') {
        $post['__EVENTARGUMENT'] = 'ctl00$contentPlaceHolderConteudo$tabAgentes$tabAgentesComp$tabAgentesCompProprios';
        $post['ctl00$contentPlaceHolderConteudo$tabAgentes'] = '{"State":{},"TabState":{"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesComp":{"Selected":true},"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesComp_tabAgentesCompPlenos":{"Selected":false},"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesComp_tabAgentesCompProprios":{"Selected":true}}}';
        $post['ctl00$contentPlaceHolderConteudo$mpgAgentes_Selected'] = '0';
    } elseif ($category == 'Full-Clearing Agents') {
        $post['__EVENTARGUMENT'] = 'ctl00$contentPlaceHolderConteudo$tabAgentes$tabAgentesComp$tabAgentesCompPlenos';
        $post['ctl00$contentPlaceHolderConteudo$tabAgentes'] = '{"State":{},"TabState":{"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesComp":{"Selected":true},"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesComp_tabAgentesCompProprios":{"Selected":false},"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesComp_tabAgentesCompPlenos":{"Selected":true}}}';
        $post['ctl00$contentPlaceHolderConteudo$mpgAgentes_Selected'] = '1';
    } elseif ($category == 'Custodians') {
        $post['__EVENTARGUMENT'] = 'ctl00$contentPlaceHolderConteudo$tabAgentes$tabAgentesCustodia';
        $post['ctl00$contentPlaceHolderConteudo$tabAgentes'] = '{"State":{"SelectedIndex":1},"TabState":{"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesComp":{"SelectedIndex":1,"Selected":false},"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesComp_tabAgentesCompPlenos":{"Selected":true},"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesCustodia":{"Selected":true}}}';
        $post['ctl00$contentPlaceHolderConteudo$mpgAgentes_Selected'] = '2';
    } elseif ($category == 'Gross Settlement Agents') {
        $post['__EVENTARGUMENT'] = 'ctl00$contentPlaceHolderConteudo$tabAgentes$tabAgentesLiqBruta';
        $post['ctl00$contentPlaceHolderConteudo$tabAgentes'] = '{"State":{"SelectedIndex":2},"TabState":{"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesComp_tabAgentesCompPlenos":{"Selected":true},"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesCustodia":{"Selected":false},"ctl00_contentPlaceHolderConteudo_tabAgentes_tabAgentesLiqBruta":{"Selected":true}}}';
        $post['ctl00$contentPlaceHolderConteudo$mpgAgentes_Selected'] = '3';
    }
    curl_setopt_array($ch, array(
        CURLOPT_URL => 'http://www.bmfbovespa.com.br/Agentes/agentes.aspx?idioma=en-us',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POSTFIELDS => http_build_query($post)
    ));

    echo "Loading data ($category) ...\n";
    $dom = new DOMDocument();
    @$dom->loadHTML(curl_exec($ch));
    $xpath = new DOMXPath($dom);
    $dom = null;
    unset($dom);
    $rows = $xpath->query('//div[@id="listaAlternada"]')->item(0)->getElementsByTagName('li');
    $n = $rows->length;
    $xpath = null;
    unset($xpath);
    $results = array();
    for ($i = 0; $i < $n; $i++) {
        $row = $rows->item($i);
        if ($a = @$row->getElementsByTagName('a')->item(0)) {
            $name = @$a->nodeValue;
        } else {
            $name = null;
        }
        if ($p = @$row->getElementsByTagName('p')->item(0)) {
            $address = @$p->nodeValue;
        } else {
            $address = null;
        }
        array_push($results, array(
            'unique_id' => preg_replace('/\s+/', '', $category .'-'. @$name),
            'name' => trim(@$name),
            'address' => trim(@$address),
            'category' => trim($category)
        ));
    }

    scraperwiki::save_sqlite(array('unique_id'), $results);
    echo "Peak memory usage: ". memory_get_peak_usage() . "\n";
    $query = null;
    $results = null;
    unset($query);
    unset($results);
}

$sections = array('Self-Clearing Houses', 'Full-Clearing Agents', 'Custodians', 'Gross Settlement Agents');
$dom = new DOMDocument();
@$dom->loadHTML(scraperwiki::scrape('http://www.bmfbovespa.com.br/Agentes/agentes.aspx?idioma=en-us'));
$xpath = new DOMXPath($dom);
$viewstate = trim($xpath->query('//input[@name="__VIEWSTATE"]')->item(0)->getAttribute('value'));

foreach ($sections as $section) {
    scrape($section, $viewstate);
};
?>