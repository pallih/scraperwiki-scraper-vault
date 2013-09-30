<?php
require_once 'scraperwiki/simple_html_dom.php';
date_default_timezone_set("Europe/Brussels");
$sources=Array();

$sources[]=Array(
    "name" => "PDA",
    "url" => "https://europe.pda.org/index.php?n1=665&n2=689",
    "region" => "EUROPE",
    "list_patt" => '<table width="100%" id="sortTable" class="dashedLine" border="0">(.*)<!-- column left end -->',
    "item_patt" => '<tr class="\w*">(.*)onclick="',
    "name_patt" => '<a href="[^"]*">([^<]*)</a>',
    "city_patt" => "<td>([^(<]* \([\s\w]*\))</td>",
    "date_patt" => '<td>([\d\.]*20\d\d)</td><td style="margin:0;">',
    "link_patt" => '<a href="([^"]*)">[^<]*</a>',
    );
/*
<tr class="even"><td>15.03.2011</td><td style="margin:0;">-</td><td>16.03.2011</td><td><strong><a href="/index.php?n1=665&n2=689&id=484&content=Overview">Pharmaceutical Microbiology/ Mycoplasma</a></strong><br />Open</td><td>Berlin (Germany)</td><td><a class="register-btn fee-button" href="registration/registration_form.php?id=484" onclick="return hs.htmlExpand(this, {wrapperClassName: 'draggable-header', dimmingOpacity: 0.75, align: 'center', objectType: 'iframe',width: 800} )"><span>Register</span></a><div class="tooltipEvents"><div class="border"><table border="0" class="registrationFee even">    <tr>
*/
$sources[]=Array(
    "name" => "GMP",
    "url" => "http://www.gmp-compliance.org/eca_seminare.html",
    "region" => "EUROPE",
    "list_patt" => "<table width=590 cellspacing=0 cellpadding=0 border=1>(.*)</table>",
    "item_patt" => "<tr(.*)</tr>",
    "name_patt" => "<a href=[^>]*.html>([^<]*)</a>",
    "city_patt" => "<td>([^,<]*, [\w\s]*)</td>",
    "date_patt" => "<td>([^>]* 20\d\d)</td>",
    "link_patt" => "<a href=([^>]*.html)>[^<]*</a>",
    );

$events=Array();
foreach($sources as $source){
    $html = scraperwiki::scrape($source["url"]);
    $list=Regexp($html,$source["list_patt"]);
    $items=RegexpMulti($list,$source["item_patt"]);
    $urlpart=parse_url($source["url"]);
    $pre_dom=$urlpart["scheme"] . "://" . $urlpart["host"];
    $pre_path=dirname($source["url"])."/";
    foreach($items as $item){
        $name=Regexp($item,$source["name_patt"]);
        $city=Regexp($item,$source["city_patt"]);
        $date=Regexp($item,$source["date_patt"]);
        if($date){
            $day=$date;
            $day=str_replace('- ','-',$day);
            $day=preg_replace("#(\-\d*)#","",$day);
            $time=strtotime($day);
        } else {
            $time=false;
        }
        $link=Regexp($item,$source["link_patt"]);
        switch(true){
        case substr($link,0,4) == "http":
            // leave as it is
            break;
        case substr($link,0,1) == "/":
            $link=$pre_dom.$link;
            break;
        default:
            $link=$pre_path.$link;
        }
        $region=$source["region"];
        $page=$source["name"];
        $event=Array(
            "source" => $page,
            "region" => $region,
            "name" => $name,
            "date" => $date,
            "start" => date("Y-m-d",$time),
            "city" => $city,
            "link" => $link,
            );
        if($name)
            scraperwiki::save(Array("link"),$event,$time);
    }
}

function Regexp($text,$patt){
    $matches=Array();
    $before=strlen($text);
    $text=str_replace(Array("\n","\r")," ",$text);
    preg_match("#$patt#miU",$text,$matches);
    if($matches){
        //trace("looking for [$patt] in $before chars");
        return $matches[1];
    } else {
        //trace("could not find [$patt] in $before chars");
        return false;
    }
}

function RegexpMulti($text,$patt){
    $before=strlen($text);
    $text=str_replace(Array("\n","\r")," ",$text);
    preg_match_all("#$patt#miU",$text,$matches);
    if($matches){
        trace("found [$patt] in $before chars: " . count($matches[1]));
        return $matches[1];
    } else {
        return false;
    }
}

function trace($text){
    echo "$text\r\n";
}

?>
<?php
require_once 'scraperwiki/simple_html_dom.php';
date_default_timezone_set("Europe/Brussels");
$sources=Array();

$sources[]=Array(
    "name" => "PDA",
    "url" => "https://europe.pda.org/index.php?n1=665&n2=689",
    "region" => "EUROPE",
    "list_patt" => '<table width="100%" id="sortTable" class="dashedLine" border="0">(.*)<!-- column left end -->',
    "item_patt" => '<tr class="\w*">(.*)onclick="',
    "name_patt" => '<a href="[^"]*">([^<]*)</a>',
    "city_patt" => "<td>([^(<]* \([\s\w]*\))</td>",
    "date_patt" => '<td>([\d\.]*20\d\d)</td><td style="margin:0;">',
    "link_patt" => '<a href="([^"]*)">[^<]*</a>',
    );
/*
<tr class="even"><td>15.03.2011</td><td style="margin:0;">-</td><td>16.03.2011</td><td><strong><a href="/index.php?n1=665&n2=689&id=484&content=Overview">Pharmaceutical Microbiology/ Mycoplasma</a></strong><br />Open</td><td>Berlin (Germany)</td><td><a class="register-btn fee-button" href="registration/registration_form.php?id=484" onclick="return hs.htmlExpand(this, {wrapperClassName: 'draggable-header', dimmingOpacity: 0.75, align: 'center', objectType: 'iframe',width: 800} )"><span>Register</span></a><div class="tooltipEvents"><div class="border"><table border="0" class="registrationFee even">    <tr>
*/
$sources[]=Array(
    "name" => "GMP",
    "url" => "http://www.gmp-compliance.org/eca_seminare.html",
    "region" => "EUROPE",
    "list_patt" => "<table width=590 cellspacing=0 cellpadding=0 border=1>(.*)</table>",
    "item_patt" => "<tr(.*)</tr>",
    "name_patt" => "<a href=[^>]*.html>([^<]*)</a>",
    "city_patt" => "<td>([^,<]*, [\w\s]*)</td>",
    "date_patt" => "<td>([^>]* 20\d\d)</td>",
    "link_patt" => "<a href=([^>]*.html)>[^<]*</a>",
    );

$events=Array();
foreach($sources as $source){
    $html = scraperwiki::scrape($source["url"]);
    $list=Regexp($html,$source["list_patt"]);
    $items=RegexpMulti($list,$source["item_patt"]);
    $urlpart=parse_url($source["url"]);
    $pre_dom=$urlpart["scheme"] . "://" . $urlpart["host"];
    $pre_path=dirname($source["url"])."/";
    foreach($items as $item){
        $name=Regexp($item,$source["name_patt"]);
        $city=Regexp($item,$source["city_patt"]);
        $date=Regexp($item,$source["date_patt"]);
        if($date){
            $day=$date;
            $day=str_replace('- ','-',$day);
            $day=preg_replace("#(\-\d*)#","",$day);
            $time=strtotime($day);
        } else {
            $time=false;
        }
        $link=Regexp($item,$source["link_patt"]);
        switch(true){
        case substr($link,0,4) == "http":
            // leave as it is
            break;
        case substr($link,0,1) == "/":
            $link=$pre_dom.$link;
            break;
        default:
            $link=$pre_path.$link;
        }
        $region=$source["region"];
        $page=$source["name"];
        $event=Array(
            "source" => $page,
            "region" => $region,
            "name" => $name,
            "date" => $date,
            "start" => date("Y-m-d",$time),
            "city" => $city,
            "link" => $link,
            );
        if($name)
            scraperwiki::save(Array("link"),$event,$time);
    }
}

function Regexp($text,$patt){
    $matches=Array();
    $before=strlen($text);
    $text=str_replace(Array("\n","\r")," ",$text);
    preg_match("#$patt#miU",$text,$matches);
    if($matches){
        //trace("looking for [$patt] in $before chars");
        return $matches[1];
    } else {
        //trace("could not find [$patt] in $before chars");
        return false;
    }
}

function RegexpMulti($text,$patt){
    $before=strlen($text);
    $text=str_replace(Array("\n","\r")," ",$text);
    preg_match_all("#$patt#miU",$text,$matches);
    if($matches){
        trace("found [$patt] in $before chars: " . count($matches[1]));
        return $matches[1];
    } else {
        return false;
    }
}

function trace($text){
    echo "$text\r\n";
}

?>
