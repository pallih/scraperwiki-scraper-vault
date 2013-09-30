<?php

$url = 'http://www.localsportsclubs.co.uk/Viewaddress.asp?adrsid=';
$idMin = 9550;
$idMax = 15500;

    //$idMin = 9687;
    //$idMax = 9687;

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

for ($i = $idMin; $i <= $idMax; $i++)
{
    $html = scraperwiki::scrape($url . $i);
    $dom->load($html);

    //$ret = $dom->find("input.textfield_readonly");
    $nodes = $dom->find("#frmMain table tr.smallblue");
    if (!empty($nodes))
    {
        //print count($ret);
        //print_r($nodes);
        //print_r($nodes[2]->nodes[1]->nodes[0]->attr['value']);
        //print_r($nodes[14]->nodes[3]->nodes[0]->plaintext);
        //exit;
    
        $values = array(
            'id' => $i,
            'AddressType' => clean($nodes[2]->nodes[3]->nodes[0]->attr['value']),
            'Name' => clean($nodes[3]->nodes[3]->nodes[0]->attr['value']),
            'ContactName' => clean($nodes[4]->nodes[3]->nodes[0]->attr['value']), 
            'Details' => clean($nodes[5]->nodes[3]->nodes[0]->plaintext),
            'Tel' => clean($nodes[6]->nodes[3]->nodes[0]->attr['value']),
            'Address1' => clean($nodes[7]->nodes[3]->nodes[0]->attr['value']),
            'Address2' => clean($nodes[8]->nodes[3]->nodes[0]->attr['value']),
            'Address3' => clean($nodes[9]->nodes[3]->nodes[0]->attr['value']),
            'County' => clean($nodes[10]->nodes[3]->nodes[0]->attr['value']),
            'Town' => clean($nodes[11]->nodes[3]->nodes[0]->attr['value']),
            'PostCode' => clean($nodes[12]->nodes[3]->nodes[0]->attr['value'] . ' ' . $nodes[12]->nodes[3]->nodes[1]->attr['value']),
            //'Email' => clean($nodes[13]->attr['value'])
        );
    
        if (isset($nodes[13]->nodes[3]->nodes[0]->attr['href']))
            $values['Website'] = clean($nodes[13]->nodes[3]->nodes[0]->attr['href']);
        if (isset($nodes[14]->nodes[3]->nodes[0]->plaintext))
            $values['Sports'] = clean($nodes[14]->nodes[3]->nodes[0]->plaintext);
    
        //print_r($values);
        scraperwiki::save(array('id'), $values, time());    
    }
}


function clean($val)
{
    $val = str_replace('&nbsp;','',$val);
    $val = str_replace('&amp;','&',$val);
    $val = strip_tags($val);
    $val = trim($val);
    $val = utf8_decode($val);
    return($val);
}

?>
<?php

$url = 'http://www.localsportsclubs.co.uk/Viewaddress.asp?adrsid=';
$idMin = 9550;
$idMax = 15500;

    //$idMin = 9687;
    //$idMax = 9687;

require 'scraperwiki/simple_html_dom.php';
$dom = new simple_html_dom();

for ($i = $idMin; $i <= $idMax; $i++)
{
    $html = scraperwiki::scrape($url . $i);
    $dom->load($html);

    //$ret = $dom->find("input.textfield_readonly");
    $nodes = $dom->find("#frmMain table tr.smallblue");
    if (!empty($nodes))
    {
        //print count($ret);
        //print_r($nodes);
        //print_r($nodes[2]->nodes[1]->nodes[0]->attr['value']);
        //print_r($nodes[14]->nodes[3]->nodes[0]->plaintext);
        //exit;
    
        $values = array(
            'id' => $i,
            'AddressType' => clean($nodes[2]->nodes[3]->nodes[0]->attr['value']),
            'Name' => clean($nodes[3]->nodes[3]->nodes[0]->attr['value']),
            'ContactName' => clean($nodes[4]->nodes[3]->nodes[0]->attr['value']), 
            'Details' => clean($nodes[5]->nodes[3]->nodes[0]->plaintext),
            'Tel' => clean($nodes[6]->nodes[3]->nodes[0]->attr['value']),
            'Address1' => clean($nodes[7]->nodes[3]->nodes[0]->attr['value']),
            'Address2' => clean($nodes[8]->nodes[3]->nodes[0]->attr['value']),
            'Address3' => clean($nodes[9]->nodes[3]->nodes[0]->attr['value']),
            'County' => clean($nodes[10]->nodes[3]->nodes[0]->attr['value']),
            'Town' => clean($nodes[11]->nodes[3]->nodes[0]->attr['value']),
            'PostCode' => clean($nodes[12]->nodes[3]->nodes[0]->attr['value'] . ' ' . $nodes[12]->nodes[3]->nodes[1]->attr['value']),
            //'Email' => clean($nodes[13]->attr['value'])
        );
    
        if (isset($nodes[13]->nodes[3]->nodes[0]->attr['href']))
            $values['Website'] = clean($nodes[13]->nodes[3]->nodes[0]->attr['href']);
        if (isset($nodes[14]->nodes[3]->nodes[0]->plaintext))
            $values['Sports'] = clean($nodes[14]->nodes[3]->nodes[0]->plaintext);
    
        //print_r($values);
        scraperwiki::save(array('id'), $values, time());    
    }
}


function clean($val)
{
    $val = str_replace('&nbsp;','',$val);
    $val = str_replace('&amp;','&',$val);
    $val = strip_tags($val);
    $val = trim($val);
    $val = utf8_decode($val);
    return($val);
}

?>
