<?php

ini_set('display_errors', 0);

$logo = "http://oi42.tinypic.com/mjbpyw.jpg";
$voters = "biraci.uprava.hr";
$pin = "oib.oib.hr";

$candy = null;
$carry = null;
$persy = null;

if (get_request()) {
    switch ($_GET['page']) {
        case "vote": {
            if (! auth_required()) {
                if (!vote_request()) {
                    vote_form();
                }
            }
            return;
        }
        default: {
            if (! auth_required()) {
                if (vote_form()) {
                    return;
                }
            }
        }
    }
}

input_form();

function auth_required() { try {
    global $voters, $pin;
    if (!isset($_GET['time'])) {
        $uid = hash("sha512",  $_GET['boi'] . $_GET['prezime'] . $_GET['oib'] . $_GET['ime'] . $_GET['mbg']);
    }
    else return false;
    $user = null;
    try {
        $user = scraperwiki::select("* from swdata where BIRAČ='" . $uid . "'");
    }
    catch(Exception $e) {}
    if ($user == null) {
        $person = url_get("http://{$pin}/SaznajOibWeb/fizickaOsoba.html", true, $_GET['cookie2'], array("brOsobIskaznice" => $_GET['boi'], "prezime" => strtolower($_GET['prezime']), "ime" => strtolower($_GET['ime'])));
        $_GET['cookie2'] = $person['cookie'];
        if(! preg_match('/^OIB: (.*?)&/m', $person['content'], $oib)) { $_GET['boi'] = ""; return true; }
        $proxy = url_get("https://{$voters}/EBiraciRH2/___proxy", true, $_SESSION['cookie1'], json_array(true), true);
        $_GET['cookie1'] = $proxy['cookie'];
        if(! preg_match('/^OIB: (.*?),/m', $proxy['content'], $oib)) { $_GET['mbg'] = ""; return true; }
        if (! ($oib === $_GET['oib'])) { $_GET['oib'] = ""; return true; }
        if(! preg_match('/^GROP: (.*?),/m', $proxy['content'], $city)) { $_GET['city'] = ""; return true; }
        $_GET['city'] = $city;
    }
    return false;
}
catch(Exception $e) {
    return true;
}}

function get_request() {
    $ret = true;

    if (!isset($_GET['manjina'])) { $_GET['manjina'] = null; }
    else if (substr($_GET['manjina'], -2) != "ka") {
        $ret = false;
    }

    if (!isset($_GET['oib'])) { $_GET['oib'] = null; $ret = false; }
    if (!isset($_GET['prezime'])) { $_GET['prezime'] = null; $ret = false; }
    if (!isset($_GET['captcha1'])) { $_GET['captcha1'] = null; $ret = false; }
    if (!isset($_GET['mbg'])) { $_GET['mbg'] = null; $ret = false; }
    if (!isset($_GET['boi'])) { $_GET['boi'] = null; $ret = false; }
    if (!isset($_GET['ime'])) { $_GET['ime'] = null; $ret = false; }
    if (!isset($_GET['captcha2'])) { $_GET['captcha2'] = null; $ret = false; }

    if (!isset($_GET['id'])) {
        $_GET['cookie1'] = null;
        $_GET['cookie2'] = null;
        $ret = false;
    }
    else decode_id();


    if (!isset($_GET['page'])) return false;

    if ($ret === true && $_GET['cookie1'] != null && $_GET['cookie2'] != null && $_GET['id'] != "" && $_GET['oib'] != "" &&  $_GET['prezime'] != "" && $_GET['captcha1'] != "" && $_GET['mbg'] != "" && $_GET['boi'] != "" && $_GET['ime'] != "" && $_GET['captcha2'] != "") {
        $_GET['time'] = null;
        unset($_GET['time']);
        return true;
    }

    if ($_GET['captcha1'] != null && $_GET['captcha2'] != null && isset($_GET['time'])) {
        $_GET['county'] = mb_strtoupper($_GET['captcha1']);
        $_GET['city'] = mb_strtoupper($_GET['captcha2']);
        return true;
    }

    return false;
}

function input_form() {
    global $voters, $pin;

/*
    $proxy = url_get("https://{$voters}/EBiraciRH2/___proxy", true, $_SESSION['cookie1'], json_array(false), true);
*/

    $proxy = url_get("https://{$voters}/", true, $_GET['cookie1']);
    $captcha1 = url_get("https://{$voters}/jcaptcha?" . timezone_escape(), true, $proxy['cookie']);
    $_GET['cookie1'] = $captcha1['cookie'];
    
    $person = url_get("http://{$pin}/SaznajOibWeb/fizickaOsoba.html", true, $_GET['cookie2']);
    $captcha2 = url_get("http://{$pin}/SaznajOibWeb/captcha.html", true, $person['cookie']);
    $_GET['cookie2'] = $captcha2['cookie'];

    $image1 = "data:" . $captcha1['content-type'] . ";base64," . base64_encode($captcha1['content']);
    $image2 = "data:" . $captcha2['content-type'] . ";base64," . base64_encode($captcha2['content']);

    print get_auth_doc(encode_id(), $image1, $image2, $_GET['oib'], $_GET['prezime'], $_GET['captcha1'], $_GET['mbg'], $_GET['boi'], $_GET['ime'], $_GET['captcha2'], $_GET['manjina']);
}

function encode_id() {
    $id1 = $_GET['cookie1'];
    $id2 = $_GET['cookie2'];
    $pos = strpos($id1, ';');
    $id1 = substr($id1, strpos($id1, '=')+1, ($pos ? $pos: 255));
    $pos = strpos($id2, ';');
    $id2 = substr($id2, strpos($id2, '=')+1, ($pos ? $pos: 255));
    return $id1 . 'O' . $id2;
}

function decode_id() {
    $id = $_GET['id'];
    $arr = explode('O', $id);
    $_GET['cookie1'] = (count($arr) > 0 ? "JSESSIONID=" . $arr[0] : null);
    $_GET['cookie2'] = (count($arr) > 1 ? "JSESSIONID=" . $arr[1] : null);
}

function timezone_escape() {
    date_default_timezone_set('Europe/Zagreb');
    $timestamp = date("D M d Y H:i:s \G\M\TO (T)");
    return str_replace(array(" ", "CET", "CEST"), array("%20", "Central%20European%20Time", "Central%20European%20Summer%20Time"), $timestamp);
}

function url_get($url, $headers=false, $cookie="", $post=array(), $json=false) {
    $content_type = "";
    $options = array(
        CURLOPT_RETURNTRANSFER => true,     // don't output
        CURLOPT_HEADER         => $headers, // return headers
        CURLOPT_FOLLOWLOCATION => true,     // follow redirects
        CURLOPT_USERAGENT      => "scraperwiki", // who am i
        CURLOPT_COOKIESESSION  => true,
        CURLOPT_AUTOREFERER    => true,     // set referer on redirect
        CURLOPT_SSL_VERIFYPEER => false,    // accept any cert
        CURLOPT_CONNECTTIMEOUT => 10,       // timeout on connect
        CURLOPT_TIMEOUT        => 10,       // timeout on response
        CURLOPT_MAXREDIRS      => 1,        // stop after 1 redirect
    );
    if($cookie != "") $options[CURLOPT_COOKIE] = $cookie;
    if(count($post) > 0) {
        $options[CURLOPT_POST] = count($post);
            $options[CURLOPT_POSTFIELDS] = ( $json ? json_encode($post, JSON_FORCE_OBJECT) : urldecode(http_build_query($post)) );
    }
    $ch = curl_init($url);
    curl_setopt_array($ch, $options);
    $content = curl_exec($ch);
    $code = curl_errno($ch);
    $message = curl_error($ch);
    if($headers === true) {
        if(preg_match('/^Content-Type: (.*?)\n/m', $content, $t)) $content_type = substr($t[1], 0, strlen($t[1])-1);
        if(preg_match('/^Set-Cookie: (.*?);/m', $content, $c)) $cookie = $c[1];
        $content = substr($content, strpos($content, "\r\n\r\n")+4);
    }
    curl_close($ch);
    $result = array();
    $result['code'] = $code;
    $result['message'] = $message;
    $result['cookie'] = $cookie;
    $result['content'] = $content;
    $result['content-type'] = $content_type;
    return $result;
}

function json_array($params) {
return array(
        "uri" => "",
        "queryParameters" => array(),
        "method" => "POST",
        "body" =>  json_encode(array(
            "bindingName" => "servis",
            "method" => ($params ? "dohvatiBrojBiracaZaPopisBiraca" : "getInicijalnoStanje"),
            "params" => ($params ? array($_GET['mbg'], "", $_GET['prezime']) : array()),
            "binding" => array(
                "name" => "servis",
                "type" => "EGLBinding",
                "serviceName" => "hr.apisit.m08pretrazipopisebiraca.services.M08EbiraciService",
                "alias" => "",
                "protocol" => "local"
            ))
        ),
        "headers" => array (
            "EGLDEDICATED" => "TRUE",
            "Content-Type" => "application/json; charset=UTF-8"
        )
    );
}

function get_auth_doc($id, $image1, $image2, $pid, $last, $captcha1, $bcn, $pcn, $first, $captcha2, $minor) {
    global $logo;
    if ($pid == null && $bcn == null && $bcn == null && $pcn == null && ($captcha1 != null || $captcha2 != null)) {
        $captcha1_style = "border: 2px solid #F00000";
        $captcha2_style = "border: 2px solid #F00000";
        $pid_style = "";
        $last_style = "";
        $bcn_style = "";
        $pcn_style = "";
        $first_style = "";
    }
    else {
        $pid_style = ($pid === "" ? "border: 2px solid #F00000" : "");
        $last_style = ($last === "" ? "border: 2px solid #F00000" : "");
        $captcha1_style = ($captcha1 === "" ? "border: 2px solid #F00000" : "");
        $bcn_style = ($bcn === "" ? "border: 2px solid #F00000" : "");
        $pcn_style = ($pcn === "" ? "border: 2px solid #F00000" : "");
        $first_style = ($first === "" ? "border: 2px solid #F00000" : "");
        $captcha2_style = ($captcha2 === "" ? "border: 2px solid #F00000" : "");
    }

    $minor_style = ($minor != null && substr($minor, -2) != "ka" ? "border: 2px solid #F00000" : "");

    $doc = '<meta name="viewport" content="width=device-width"/>
<style type="text/css">
    fieldset {   
    -webkit-border-radius: 5px;
    border-radius: 5px;  
}
#image {
    overflow: hidden;
    height: 40px;
    float: none;
}
#logo {
    border: thin #aaf solid;
    overflow: hidden;
    position:fixed;
    float: none;
    left: 0px;
    top: 0px;
    height: 41px;
}
</style>
<script>
function validateForm()
{
    var form = document.forms["input"];
    if (localStorage != undefined) {
        var time = localStorage.getItem("time");
        if (time == null) {
            time = form["time"].value;
            localStorage.setItem("time", time);
        }
        else
            form["time"].value = time;
    }
    if (form["boi"].value == "" && form["prezime"].value == "" && form["mbg"].value == "" && form["boi"].value == "" && form["ime"].value == ""&& (form["captcha1"].value != "" || form["captcha2"].value != "")) {
        if (form["manjina"].value != "" && form["manjina"].value.slice(-2) != "ka") {
            form["manjina"].style.cssText =  "border: 2px solid #F00000";
            return false;
        }
        return true;
    }
    form["oib"].style.cssText = form["oib"].value === "" ? "border: 2px solid #FF0000" : "";
    form["prezime"].style.cssText = form["prezime"].value === "" ? "border: 2px solid #F00000" : "";
    form["captcha1"].style.cssText = form["captcha1"].value === "" ? "border: 2px solid #F00000" : "";
    form["mbg"].style.cssText = form["mbg"].value === "" ? "border: 2px solid #F00000" : "";
    form["boi"].style.cssText = form["boi"].value === "" ? "border: 2px solid #F00000" : "";
    form["ime"].style.cssText = form["ime"].value === "" ? "border: 2px solid #FF0000" : "";
    form["captcha2"].style.cssText = form["captcha2"].value === "" ? "border: 2px solid #F00000" : "";
    form["manjina"].style.cssText = form["manjina"].value != "" && form["manjina"].value.slice(-2) != "ka" ? "border: 2px solid #F00000" : "";
    return form["boi"].value != "" && form["captcha1"].value != "" && form["mbg"].value != "" && form["boi"].value != "" && form["captcha2"].value != "";
}
</script>
<div id="logo">
  <img src="'.$logo.'"/>
</div>
<br>
<h2><center>Lokalni izbori 2013. (anketa)<center/></h2>
  <br>
  <h4>Anketa završena. Odaziv je bio slabašan. Hvala svima koji su sudjelovali <a href="https://scraperwiki.com/views/izbori_1/"/>(2 biraca)</a></h4><br> 
<form name="input" action="" method="get" onsubmit="return validateForm()">
  <fieldset> <legend>biraci.uprava.hr</legend>
    <br style="margin: 4px; display:block"/>
    <input type="hidden" id="id" name="id" value="'.$id.'" style=""/>
    <input type="hidden" id="time" name="time" value="' . microtime() . '"/>
    <input type="text" id="oib" name="oib" value="'.$pid.'" style="'.$pid_style.'" disabled/><label for="oib"> osobni id broj</label>
    <br>
    <input type="text" id="prezime" name="prezime" value="'.$last.'" style="'.$last_style.'" disabled/><label for="prezime"> prezime</label>
    <br>
    <input type="text" id="captcha1" name="captcha1" value="'.$captcha1.'" style="'.$captcha1_style.'"/ disabled><label for="captcha1"> *prepiši tekst (uputa na vrhu)</label>
    <div>
      <img src="'.$image1.'"/>
    </div>
  </fieldset>
  <br>
  <fieldset> <legend>oib.oib.hr</legend>
    <br style="margin: 4px; display:block"/>
    <input type="text" id="mbg" name="mbg" value="'.$bcn.'" style="'.$bcn_style.'" disabled/><label for="mbg"> matični broj</label>
    <br>
    <input type="text" id="boi" name="boi" value="'.$pcn.'" style="'.$pcn_style.'" disabled/><label for="boi"> broj osobne</label>
    <br>
    <input type="text" id="ime" name="ime" value="'.$first.'" style="'.$first_style.'"/ disabled><label for="ime"> ime</label>
    <br>
    <input type="text" id="captcha2" name="captcha2" value="'.$captcha2.'" style="'.$captcha2_style.'" disabled/><label for="captcha2"> *prepiši tekst (uputa na vrhu)</label>
    <input type="hidden" id="page" name="page" value="auth" style=""/>
    <div id="image">
      <img src="'.$image2.'"/>
    </div>
  </fieldset>
  <br>
  <fieldset> <legend>nacionalne manjine</legend>
    <br style="margin: 4px; display:block"/>
    <input type="text" id="manjina" name="manjina" value="'.$minor.'"/ disabled><label for="manjina"> manjina</label>
    <br><br>
    npr. srpska, bošnjačka, itd.
  </fieldset>
  <br><center><input type="submit"/ disabled></center>
</form>
';
    return $doc;
}

function vote_form() { try {
    global $candy, $carry, $persy;
    global $logo;
    $doc = '<meta name="viewport"/>
<style type="text/css">
    fieldset {   
    -webkit-border-radius: 5px;
    border-radius: 5px;  
}
#logo {
    border: thin #aaf solid;
    overflow: hidden;
    position:fixed;
    float: none;
    left: 0px;
    top: 0px;
    height: 41px;
}
legend {
  padding: 0.3em 0.5em;
  border:1px solid;
  font-size:90%;
}
</style>
<script>
function validateForm()
{
    var form = document.forms["input"];
    if (localStorage != undefined) {
        var time = localStorage.getItem("time");
        if (time == null) {
            time = form["time"].value;
            localStorage.setItem("time", time);
        }
        else
            form["time"].value = time;
    }
    var radios = document.getElementsByTagName("input");
    var i = 0;
    while (radios[i].type === "hidden") { i++; }
    var n = 0;
    while (i < radios.length) {
        var name = "lista" + n;
        var found = false;
        while(i < radios.length && radios[i].type === "radio" && radios[i].name === name) {
            if (radios[i].checked) found = true;
            i++;
        }
        if (!found) {
            if (confirm("Neke su liste ostale neispunjene. Jeste li sigurni u nastavak?")) return true;
            else return false;
        }
        if (radios[i].type === "submit") break;
        n++;
    }
    return true;
}
</script>
<div id="logo">
  <img src="'.$logo.'"/>
</div>
<br>
';
    print '<h2><center>Lokalni izbori 2013. (' . $_GET['city'] . ')</center></h2>';
    $list1 = "LISTA ZA GRADSKO/OPĆINSKO VIJEĆE";
    $list11 = 35;//"LISTA ZA GRADSKO/OPĆINSKO VIJEĆE";
    $list2 = "ŽUPANIJSKA SKUPŠTINA";
    $list3 = "ZAMJENIK ŽUPANA IZ REDA N.M.";
    $list4 = "GRADSKA SKUPŠTINA GRADA ZAGREBA";

    scraperwiki::attach("liste");

    $query = 'zupanija from liste."područja" where grad_opcina="' . $_GET['city'] . '"';
    $county = scraperwiki::select($query);
    if ($county == null || (isset($_GET['county']) && $county[0]['zupanija'] != $_GET['county'])) {
        $_GET['page'] = 'auth';
        return false;
    }
    $_GET['county'] = $county[0]['zupanija'];

    $query = 'lista, izvor, kandidati from liste."' . $_GET['county'] . '" where grad_opcina="' . $_GET['city'] . '" or grad_opcina is null';
    $data = scraperwiki::select($query);

    if (!isset($_GET['time'])) {
        $uid = hash("sha512",  $_GET['boi'] . $_GET['prezime'] . $_GET['oib'] . $_GET['ime'] . $_GET['mbg']);
    }
    else $uid = $_GET['time'];
    $vote = null;
    try {
        $query = '* from swdata where BIRAČ="' . $uid . '" and GRAD="' . $_GET['city'] . '" and ŽUPANIJA="' . $_GET['county'] . '"';
        $vote = scraperwiki::select($query);
    }
    catch(Exception $e) {
        scraperwiki::sqliteexecute('CREATE TABLE `swdata` (`GRAD` text, `LISTA ZA GRADSKO/OPĆINSKO VIJEĆE` text,`LISTA ZA GRADONAČELNIKA/OPĆINSKOG NAČELNIKA` text, `ŽUPANIJA` text, `ŽUPANIJSKA SKUPŠTINA` text, `ŽUPAN` text, `ZAMJENIK ŽUPANA IZ REDA N.M.` text, `LISTA ZA ZAMJENIKA GRADONAČELNIKA/NAČELNIKA IZ REDA N.M. / HRVATSKOG NARODA` text, `GRADSKA SKUPŠTINA GRADA ZAGREBA` text, `GRADONAČELNIK GRADA ZAGREBA` text, `BIRAČ` text)');
    }
    print $doc;
    print '<form name="input" action="" method="get" onsubmit="return validateForm()">
<input type="hidden" id="id" name="id" value="'.$_GET['id'].'"/>
<input type="hidden" id="time" name="time" value="' . microtime() . '"/>
<input type="hidden" id="oib" name="oib" value="'.$_GET['oib'].'"/>
<input type="hidden" id="prezime" name="prezime" value="'.$_GET['prezime'].'"/>
<input type="hidden" id="captcha1" name="captcha1" value="'.$_GET['captcha1'].'"/>
<input type="hidden" id="mbg" name="mbg" value="'.$_GET['mbg'].'"/>
<input type="hidden" id="boi" name="boi" value="'.$_GET['boi'].'"/>
<input type="hidden" id="ime" name="ime" value="'.$_GET['ime'].'"/>
<input type="hidden" id="captcha2" name="captcha2" value="'.$_GET['captcha2'].'"/>
<input type="hidden" id="manjina" name="manjina" value="'.$_GET['manjina'].'"/>
<input type="hidden" id="page" name="page" value="vote"/>';

    for ($i=0; $i<count($data); $i++) {
        print '<fieldset id="set' . ($i+1) . '">';
        $list = "";
        foreach ($data[$i] as $key => $value) {
            if ($key == "lista") {
                print '<legend>' . $value . '</legend>';
                $list = $value;
            }
            else if ($key == "izvor") {
                print '<a href="' . $value . '">' . $value . '</a>';
                print '<br style="margin: 10px; display:block"/>';
            }
            else if ($key == "kandidati") {
                $list = trim($list);
                $len = strlen($list);
                if ($len == strlen($list1) || $len == $list11 || $len == strlen($list2) || $len == strlen($list4)) {
                    $idx = parse_party($value);
                    for ($l=0; $l < $idx; $l++) {
                        $checked1 = -1;
                        $checked2 = -1;
                        if ($vote != null && isset($vote[0][$list])) {
                            $checked =  $vote[0][$list];
                            if (is_numeric($checked)) {
                                $pos = strpos($checked, '.');
                                $checked1 = substr($checked, 0, $pos);
                                $checked2 = substr($checked, $pos+1);
                            }
                            else $checked = -1;
                        }
                        print '<hr style="display:list-item; height:1px; padding:0px">';
                        print '<input type="radio" name="lista' . $i . '" value="kandidat' . $l . '"' . ($l == $checked1 ? " checked" : "") . '>' . $candy[$l] . '</input></hr/></br>' ;
                        print '<ul><select name="lista' . $i . 'kandidat' . $l . '">';
                    
                        $len = count($persy[$l]);
                        for($k=0; $k < $len; $k++) {
                            $pers = $persy[$l][$k];
                            print '<option value="' . $k . '"' . ($k == $checked2 ? " selected" : "") . '>' . substr($pers, strpos($pers, '.')+1) . '</option>';
                        }
                        print '</select></ul>';
                        print '<ul>' . $carry[$l] . '</ul>';
                    }
                }
                else
                {
                    $len = strlen($list);
                    if ($len == strlen($list3)) {
                        if (!isset($_GET['manjina']) || $_GET['manjina'] == "") {
                            print "<ul>Napomena: lista za pripadnike nacionalnih manjina</ul>";
                            continue;
                        }
                        $minor = strtolower($_GET['manjina']);
                        $minor[strlen($minor)-1] = 'e';
                        if (strpos($value, $minor) == -1) {
                            print "<ul>Napomena: lista za pripadnike nacionalnih manjina</ul>";
                            continue;
                        }
                    }
                    $idx = parse_poly($value);
                    for ($l=0; $l < $idx; $l++) {
                        $checked = -1;
                        if ($vote != null) {
                            $checked =  $vote[0][$list];
                            if (!is_numeric($checked))
                                $checked = -1;
                        }
                        print '<hr style="display:list-item; height:1px; padding:0px">';
                        print '<input type="radio" name="lista' . $i . '" value="kandidat' . $l . '"' . ($l == $checked ? " checked" : "") . '>' . $candy[$l] . '</input></hr/></br>' ;
                        print '<ul style="list-style-type:none">';

                        $len = count($persy[$l]);
                        for($k=0; $k < $len; $k++) {
                            print  '<li>Zamjenik: ' . $persy[$l][$k] . '</li>';
                        }
                        print '</ul>';
                        print '<ul>';
                        $len = count($carry[$l])-1;
                        for($k=0; $k < $len; $k++) {
                            print '<li>' . $carry[$l][$k] . '</li>';
                        }
                        print '</ul>';
                    }

                }
            }
        }
        print '</fieldset><br><br>';
    }
    print '<center><input type="submit"/></center></form><br><br>';
    
    return true;
} 
catch(Exception $e) {
    $_GET['page'] = 'auth';
    return false;
}}

function vote_request() { try {
    $list1 = "LISTA ZA GRADSKO/OPĆINSKO VIJEĆE";
    $list11 = 35;//"LISTA ZA GRADSKO/OPĆINSKO VIJEĆE";
    $list2 = "ŽUPANIJSKA SKUPŠTINA";
    $list3 = "ZAMJENIK ŽUPANA IZ REDA N.M.";
    $list4 = "GRADSKA SKUPŠTINA GRADA ZAGREBA";

    scraperwiki::attach("liste");

    $query = 'zupanija from liste."područja" where grad_opcina="' . $_GET['city'] . '"';
    $county = scraperwiki::select($query);
    if ($county == null || $county[0]['zupanija'] != $_GET['county']) {
        $_GET['page'] = 'auth';
        return false;
    }

    $query = 'lista, izvor, kandidati from liste."' . $county[0]['zupanija'] . '" where grad_opcina="' . $_GET['city'] . '" or grad_opcina is null';
    $data = scraperwiki::select($query);
    $votes = array();
    for ($i=0; $i<count($data); $i++) {
        $list = "";
        foreach ($data[$i] as $key => $value) {
            if ($key == "lista") {
                $list = $value;
            }
            else if ($key == "izvor") {
                continue;
            }
            else if ($key == "kandidati") {
                $list = trim($list);
                $len = strlen($list);
                if ($len == strlen($list1) || $len == $list11 || $len == strlen($list2) || $len == strlen($list4)) {
                    if (isset($_GET['lista' . $i])) {
                        $vote = $_GET['lista' . $i];
                        $l = substr($vote, 8);
                        if (isset($_GET['lista' . $i . 'kandidat' . $l])) {
                            $vote = $_GET['lista' . $i . 'kandidat' . $l];
                            if ($vote != "") {
                                $votes[$list] = $l.'.'.$vote;
                            }
                        }
                    }
                }
                else
                {
                    $len = strlen($list);
                    if ($len == strlen($list3)) {
                        if (!isset($_GET['manjina']) || $_GET['manjina'] == "") {
                            continue;
                        }
                        $minor = strtolower($_GET['manjina']);
                        $minor[strlen($minor)-1] = 'e';
                        if (strpos($value, $minor) == -1) {
                            continue;
                        }
                    }
                    if (isset($_GET['lista' . $i])) {
                        $vote = $_GET['lista' . $i];
                        $l = substr($vote, 8);
                        if ($l != "") {
                            $votes[$list] = $l;
                        }
                    }
                }
            }
        }
    }
    if (!isset($_GET['time'])) {   
        $votes['BIRAČ'] = hash("sha512",  $_GET['boi'] . $_GET['prezime'] . $_GET['oib'] . $_GET['ime'] . $_GET['mbg']);
    }
    else 
    $votes['BIRAČ'] = $_GET['time'];
    $votes['GRAD'] = $_GET['city'];
    $votes['ŽUPANIJA'] = $_GET['county'];
    scraperwiki::save_sqlite(array('BIRAČ'), $votes);
    get_results();
    return true;
}
catch(Exception $e) {
    $_GET['page'] = 'auth';
    return false;
}}

function get_results() { try {
    global $candy, $carry, $persy;
    global $logo;
    $list1 = "LISTA ZA GRADSKO/OPĆINSKO VIJEĆE";
    $list11 = 35;//"LISTA ZA GRADSKO/OPĆINSKO VIJEĆE";
    $list2 = "ŽUPANIJSKA SKUPŠTINA";
    $list3 = "ZAMJENIK ŽUPANA IZ REDA N.M.";
    $list4 = "GRADSKA SKUPŠTINA GRADA ZAGREBA";
    $doc = '<meta name="viewport"/>
<style type="text/css">
    fieldset {   
    -webkit-border-radius: 5px;
    border-radius: 5px;  
}
#logo {
    border: thin #aaf solid;
    overflow: hidden;
    position:fixed;
    float: none;
    left: 0px;
    top: 0px;
    height: 41px;
}
legend {
  padding: 0.3em 0.5em;
  border:1px solid;
  font-size:90%;
}
</style>
<script>
function validateForm()
{
    var form = document.forms["input"];
    if (localStorage != undefined) {
        var time = localStorage.getItem("time");
        if (time == null) {
            time = form["time"].value;
            localStorage.setItem("time", time);
        }
        else
            form["time"].value = time;
    }
}
</script>
<div id="logo">
  <img src="'.$logo.'"/>
</div>
<br>
';
    print $doc;
    print '<h2><center>Lokalni izbori 2013. ('. $_GET['city'] . ')</center></h2>';
    print '<form name="input" action="" method="get" onsubmit="return validateForm()">
<input type="hidden" id="id" name="id" value="'.$_GET['id'].'"/>
<input type="hidden" id="time" name="time" value="' . microtime() . '"/>
<input type="hidden" id="oib" name="oib" value="'.$_GET['oib'].'"/>
<input type="hidden" id="prezime" name="prezime" value="'.$_GET['prezime'].'"/>
<input type="hidden" id="captcha1" name="captcha1" value="'.$_GET['captcha1'].'"/>
<input type="hidden" id="mbg" name="mbg" value="'.$_GET['mbg'].'"/>
<input type="hidden" id="boi" name="boi" value="'.$_GET['boi'].'"/>
<input type="hidden" id="ime" name="ime" value="'.$_GET['ime'].'"/>
<input type="hidden" id="captcha2" name="captcha2" value="'.$_GET['captcha2'].'"/>
<input type="hidden" id="manjina" name="manjina" value="'.$_GET['manjina'].'"/>
<input type="hidden" id="page" name="page" value="auth"/>';

    scraperwiki::attach("liste");
    $query = 'zupanija from liste."područja" where grad_opcina="' . $_GET['city'] . '"';
    $county = scraperwiki::select($query);
    if ($county == null || $county[0]['zupanija'] != $_GET['county']) {
        $_GET['page'] = 'auth';
        return false;
    }
    $query = 'lista, izvor, kandidati from liste."' . $county[0]['zupanija'] . '" where grad_opcina="' . $_GET['city'] . '" or grad_opcina is null';
    $data = scraperwiki::select($query);

    for ($i=0; $i<count($data); $i++) {
        print '<fieldset id="set' . ($i+1) . '">';
        $list = "";
        foreach ($data[$i] as $key => $value) {
            if ($key == "lista") {
                print '<legend>' . $value . '</legend>';
                $list = $value;
            }
            else if ($key == "izvor") {
                print '<a href="' . $value . '">' . $value . '</a>';
                print '<br style="margin: 10px; display:block"/>';
            }
            else if ($key == "kandidati") {
                $list = trim($list);
                $len = strlen($list);
                if ($len == strlen($list1) || $len == $list11 || $len == strlen($list2) || $len == strlen($list4)) {
                    parse_party($value);
                    $sql = '(select count(*) from swdata where [' . $list . '] is not null) as ukupno, count(*) as zbirno, cast(['.$list.'] as integer) as lista from swdata where lista is not null and GRAD="' . $_GET['city'] . '" and ŽUPANIJA="' . $_GET['county'] . '" group by lista order by zbirno desc';
                    $votes = scraperwiki::select($sql);
                    $idx = count($votes);
                    for ($l=0; $l < $idx; $l++) {
                        $lista = $votes[$l]['lista'];
                        if (!is_numeric($lista)) continue;
                        $ukupno = $votes[$l]['ukupno'];
                        $zbirno = $votes[$l]['zbirno'];
                        print '<hr style="display:list-item; height:1px; padding:0px">';
                        print '<label name="lista' . $i . '" value="kandidat' . $lista . '">' . ($l+1) . '. ' . $candy[$lista] . '</input></hr/></br>';
                        print '<label style="display:block; float:right"><b>' . round(($zbirno*100)/$ukupno, 2) . '%</b></label>';
                        print '<ul><select name="lista' . $i . 'kandidat' . $lista . '">';
                    
                        $sql = 'count(['.$list.']) as pojedinacno, ['.$list.'] as kandidat from swdata where kandidat is not null and GRAD="' . $_GET['city'] . '" and ŽUPANIJA="' . $_GET['county'] . '" and ['.$list.'] like "'.$lista.'.%" group by kandidat order by pojedinacno desc';
                        $candies = scraperwiki::select($sql);
                        $len = count($candies);
                        for($k=0; $k < $len; $k++) {
                            $kandidat = $candies[$k]['kandidat'];
                            $kandidat = substr($kandidat, strpos($kandidat, '.') + 1);
                            $pers = $persy[$lista][$kandidat];
                            print '<option value="' . $k . '">' . ($k+1) . '.' . substr($pers, strpos($pers, '.')+1) . ' (' . $candies[$k]['pojedinacno'] . ") " . round(($candies[$k]['pojedinacno']*100)/$zbirno, 2) . '%</option>';
                        }
                        print '</select></ul>';
                        print '<label style="display:block; float:right">('. $zbirno . ')</label>'; 
                        print '<ul>' . $carry[$lista] . '</ul>';
                    }
                }
                else
                {
                    parse_poly($value);
                    $sql = '(select count(*) from swdata where ['.$list.'] is not null) as ukupno, count(*) as zbirno, ['.$list.'] as lista, count(distinct ['.$list.']) as pojedinacno, ['.$list.'] as kandidat from swdata where lista is not null and GRAD="' . $_GET['city'] . '" and ŽUPANIJA="' . $_GET['county'] . '" group by lista order by zbirno desc';
                    $votes = scraperwiki::select($sql);
                    $idx = count($votes);
                    for ($l=0; $l < $idx; $l++) {
                        $lista = $votes[$l]['lista'];
                        if (!is_numeric($lista)) continue;
                        $ukupno = $votes[$l]['ukupno'];
                        $zbirno = $votes[$l]['zbirno'];
                        print '<hr style="display:list-item; height:1px; padding:0px">';
                        print '<label name="lista' . $i . '" value="kandidat' . $l . '">' . ($l+1) . '. ' . $candy[$lista] . '</input></hr/></br>' ;
                        print '<label style="display:block; float:right"><b>' . round(($zbirno*100)/$ukupno, 2) . '%</b></label>';
                        print '<ul style="list-style-type:none">';

                        $len = count($persy[$lista]);
                        for($k=0; $k < $len; $k++) {
                            print  '<li>Zamjenik: ' . $persy[$lista][$k] . '</li>';
                        }
                        print '</ul>';
                        print '<label style="display:block; float:right">('. $zbirno . ')</label>';
                        print '<ul>';
                        $len = count($carry[$lista])-1;
                        for($k=0; $k < $len; $k++) {
                            print '<li>' . $carry[$lista][$k] . '</li>';
                        }
                        print '</ul>';
                    }
                }
            }
        }
        print '</fieldset><br><br>';
    }
    print '<center><input type="submit"/></center></form><br><br>';
    
}
catch(Exception $e) {
    $_GET['page'] = 'auth';
    return false;
}}

function parse_party($value) {
    global $candy, $carry, $persy;
    $candy = array();
    $carry = array();
    $persy = array();
    $code = 0;
    $idx = 0;
    $line = strtok($value, "\r\n");
    do {
        while ($line !== false) {
            if (ord($line[0]) <= 57) {
                $candy[$idx] = substr($line, strpos($line, '.') + 1);
                break;
            }
            $line = strtok("\r\n");
        }
        $line = strtok("\r\n");
        while ($line !== false) {
            if (ord($line[0]) == 78 && ord($line[1]) == 111) {
                $carry[$idx++] = $line;
                break;
            }
            $candy[$idx] .= ', ' . $line;
            $line = strtok("\r\n");
        }
        $line = strtok("\r\n");
        $code = ord($line[0]);
    }
    while($code >= 48 && $code <= 57 || ($code == 12 && ord($line[1]) >= 48 && ord($line[1]) <= 57));

    for ($j=0; $j < $idx; $j++) {
        $pdx = 0;
        $persy[$j] = array();
        while ($line != false) {
            $code = ord($line[0]);
            if ($code >= 48 && $code <= 57) {
                break;
            }
            $line = strtok("\r\n");
        }
        $hist = 0;
        while ($line !== false) {
            $code = ord($line[strlen($line)-1]);
            if ($code == 77 || $code == 189 || $code == 32) {
                if ($hist == 32) {
                    $persy[$j][$pdx-1] .= $line;
                } else {
                    $persy[$j][$pdx++] = $line;
                }
            }
            else {
                $line = strtok("\r\n");
                break;
            }
            $hist = $code;
            $line = strtok("\r\n");
        }
    }
    return $idx;
}

function parse_poly($value) {
    global $candy, $carry, $persy;
    $candy = array();
    $persy = array();
    $carry = array();
    $ord = -1;
    $code = 0;
    $idx = -1;
    $idx1 = -1;
    $idx2 = -1;
    $line = strtok($value, "\r\n");
    $hist = 0;
    while ($line !== false) {
        if ($ord == 2) {
            if ($hist == 32) {
                $idx2 == 0 ? $carry[$idx][$idx2] .= $line : $carry[$idx][$idx2-1] .= $line;
            } else {
                $carry[$idx][$idx2++] = $line;
            }
        }
        $len = strlen($line);
        $code = ord($line[$len-1]);
        if ($code == 77 || $code == 189 || $code == 32) {
            switch($ord) {
                case (0): {
                    if ($hist == 32) {
                        $idx == 0 ? $candy[$idx] .= $line : $candy[$idx-1] .= $line;
                    } else {
                        $candy[++$idx] = $line;
                        $carry[$idx] = array();
                        $persy[$idx] = array();
                        $idx1 = 0;
                        $idx2 = 0;
                    }
                    break;
                }
                case (1): {
                    if ($hist == 32) {
                        $idx1 == 0 ? $persy[$idx][$idx1] .= $line : $persy[$idx][$idx1-1] .= $line;
                    } else {
                        $persy[$idx][$idx1++] = $line;
                    }
                    break;
                }
            }
        }
        else if ($len > 2) {
            if (ord($line[1]) == 75 && ord($line[2]) == 97) {
                    $ord = 0;     
            }
            else if (ord($line[0]) == 90 && ord($line[1]) == 97) {
                if ($ord != -1)
                    $ord = 1;
            }
            else if (ord($line[0]) == 80 && ord($line[1]) == 114) {
                if ($ord != -1)
                    $ord = 2;
            }
        }
        $hist = $code;
        $line = strtok("\r\n");
    }
    return $idx+1;
}
?>

