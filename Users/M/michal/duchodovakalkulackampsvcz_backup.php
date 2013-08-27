<?php

//'backup' of http://duchodovakalkulacka.mpsv.cz/www/
//just in case....

require 'scraperwiki/simple_html_dom.php'; 

$birth = array(1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010);
$sex = array(1,2,6);
$lower = array(0,1);
$salary = array(0,10000,15000,20000,25000,30000,40000,60000,90000);
$gain = array(1,4,8);

foreach ($birth as $b) {
  foreach ($sex as $s) {
    foreach ($lower as $l) {
      foreach ($salary as $sa) {
        foreach ($gain as $g) {
          $url = "http://duchodovakalkulacka.mpsv.cz/www/?rok_narozeni={$b}&pokles={$l}&pohlavi={$s}&mzda={$sa}&vynos={$g}&save=Vypo%C4%8D%C3%ADtat&_form_=calc";
          $html = scraperwiki::scrape($url);
          if (!strpos($html,'Důchodový věk byl dosažen před rokem 2013!')) {
            $dom = new simple_html_dom();
            $dom->load($html);
            $div = $dom->find('div[id=vysledek]',0);
            $out = array(
                'birth' => $b,
                'sex' => $s,
                'lower' => $l,
                'salary' => $sa,
                'gain' => $g,
                'html' => $div->outertext,
            );
            scraperwiki::save_sqlite(array('birth','sex','lower','salary','gain','html'),$out);
//die();
          }

          
        }
      }
    }
  }
} 

/* TO HAVE ALL THE COMMON TEXT: 
(http://duchodovakalkulacka.mpsv.cz/www/?rok_narozeni=1974&pokles=-1&pohlavi=6&mzda=0&vynos=8&save=Vypo%C4%8D%C3%ADtat&_form_=calc)

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <meta name="description" content="Důchodová kalkulačka" />

    <title>MPSV.CZ : Důchodová kalkulačka</title>

    <link rel="stylesheet" media="screen,projection,tv" href="/www/css/screen.css" type="text/css" />
    <link rel="stylesheet" media="print" href="/www/css/print.css" type="text/css" />
    <!--[if lt IE 8]>
        <link rel="stylesheet" href="/www/css/ie.css" type="text/css" media="screen, projection" />
    <![endif]-->
    <link rel="stylesheet" media="screen,projection,tv" href="/www/css/duchodovakalkulacka.css?v=1" type="text/css" />
    <link rel="shortcut icon" href="/www/favicon.ico" type="image/x-icon" />

        <script type="text/javascript" src="/www/js/netteForms.js"></script>
    
</head>

<body>

<div id="shadow">
<div id="main">
    <div id="header"><h1><a href="http://www.mpsv.cz" title="Zpět na titulní stránku MPSV"><span>Ministerstvo práce a sociálních věcí</span></a></h1></div>


    <div id="content"><div class="content-border">
<div class="content-in-w"><div class="content-in-w-border">
<h1 class="content-heading">Kalkulačka k důchodové reformě</h1>

<div class="skip"><a href="#vysledek" tabindex="1">Přejít na výsledek výpočtu</a></div>

<p>
Počátek spoření je rok 2013, pro rok narození 1994 a později ve 20 letech.
</p>

<p style="color: red;">
Kalkulačka v základní verzi počítá výši důchodů podle současné situace. Ti, 
kterým je dnes 30 let, ale musí počítat s tím, že jejich důchod od státu 
(z&nbsp;I.&nbsp;pilíře) bude ve srovnání se mzdami výrazně nižší než ten, který 
mají důchodci dnes. Například podle studie 
<a href="http://idea.cerge-ei.cz/documents/kratka_studie_2012_07.pdf">„Jaký důchod nás čeká?“</a> 
mohou být do budoucna státní důchody až o 50 procent nižší. Zkuste také druhou 
novou funkci naší kalkulačky, která vám ukáže předpokládaný budoucí důchod. 
Srovnejte a uvidíte, že je nutné, aby si každý sám spořil na stáří.
</p>

<form action="" method="get" id="frm-calc">
    
    <div class="container">
        <div class="span-4">
        <label class="required" for="frmcalc-rok_narozeni">Rok narození</label>
        </div>
        <div class="span-6">
        <select aria-required="aria-required" name="rok_narozeni" id="frmcalc-rok_narozeni" required="required" data-nette-rules="{op:':filled',msg:&quot;Vyberte, pros\u00edm, rok narozen\u00ed z nab\u00eddky.&quot;}"><option value="1950">1950</option><option value="1951">1951</option><option value="1952">1952</option><option value="1953">1953</option><option value="1954">1954</option><option value="1955">1955</option><option value="1956">1956</option><option value="1957">1957</option><option value="1958">1958</option><option value="1959">1959</option><option value="1960">1960</option><option value="1961">1961</option><option value="1962">1962</option><option value="1963">1963</option><option value="1964">1964</option><option value="1965">1965</option><option value="1966">1966</option><option value="1967">1967</option><option value="1968">1968</option><option value="1969">1969</option><option value="1970">1970</option><option value="1971">1971</option><option value="1972">1972</option><option value="1973">1973</option><option value="1974" selected="selected">1974</option><option value="1975">1975</option><option value="1976">1976</option><option value="1977">1977</option><option value="1978">1978</option><option value="1979">1979</option><option value="1980">1980</option><option value="1981">1981</option><option value="1982">1982</option><option value="1983">1983</option><option value="1984">1984</option><option value="1985">1985</option><option value="1986">1986</option><option value="1987">1987</option><option value="1988">1988</option><option value="1989">1989</option><option value="1990">1990</option><option value="1991">1991</option><option value="1992">1992</option><option value="1993">1993</option><option value="1994">1994</option><option value="1995">1995</option><option value="1996">1996</option><option value="1997">1997</option><option value="1998">1998</option><option value="1999">1999</option><option value="2000">2000</option><option value="2001">2001</option><option value="2002">2002</option><option value="2003">2003</option><option value="2004">2004</option><option value="2005">2005</option><option value="2006">2006</option><option value="2007">2007</option><option value="2008">2008</option><option value="2009">2009</option><option value="2010">2010</option></select>
        </div>
        <div class="span-14 last">
        <label for="frmcalc-pokles">Chcete v kalkulačce zohlednit předpoklad o poklesu státního důchodu?</label>
        <select name="pokles" id="frmcalc-pokles"><option value="0">Ne</option><option value="1">Ano</option></select>
        </div>
    </div>
    <div class="container">
        <div class="span-4">
        <label class="required" for="frmcalc-pohlavi">Pohlaví</label>
        </div>
        <div class="span-6 with-tooltip">
        <select aria-describedby="pohlavi-desc" aria-required="aria-required" name="pohlavi" id="frmcalc-pohlavi" required="required" data-nette-rules="{op:':filled',msg:&quot;Vyberte, pros\u00edm, pohlav\u00ed z nab\u00eddky.&quot;}"><option value="1">Muž</option><option value="2">Žena: 0 dětí</option><option value="3">Žena: 1 dítě</option><option value="4">Žena: 2 děti</option><option value="5">Žena: 3 nebo 4 děti</option><option value="6" selected="selected">Žena: 5 a více dětí</option></select>
        </div>
        <div class="span-14 last">
            <div class="form-info" id="pohlavi-desc">
            <p>U žen celkový počet dětí, tzn. současných i plánovaných</p>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="span-4" id="mzda-label">
        <label class="required" for="frmcalc-mzda">Hrubá mzda</label>
        </div>
        <div class="span-6 with-tooltip">
        <input aria-labelledby="mzda-label frmcalc-mzda mzda-mena" aria-describedby="mzda-desc" type="text" size="6" aria-required="aria-required" class="text" name="mzda" id="frmcalc-mzda" required="required" data-nette-rules="{op:':filled',msg:&quot;Zadejte, pros\u00edm, hrubou mzdu.&quot;},{op:':integer',msg:&quot;Do pole hrub\u00e1 mzda zadejte pouze \u010d\u00edslice - \u010d\u00e1stku v korun\u00e1ch.&quot;},{op:':range',msg:&quot;Zadejte, pros\u00edm, hrubou mzdu jako kladn\u00e9 \u010d\u00edslo.&quot;,arg:[0,1000000000]}" value="0" /><span class="kc" id="mzda-mena">Kč</span>
        </div>
        <div class="span-14 last">
            <div class="form-info" id="mzda-desc">
            <p>Průměrný měsíční hrubý příjem (1/12 ročního)</p>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="span-4">
        <label for="frmcalc-vynos">Výnos</label>
        </div>
        <div class="span-6 with-tooltip">
        <p>
        <select aria-describedby="vynos-desc" aria-required="aria-required" name="vynos" id="frmcalc-vynos" data-nette-rules="{op:':equal',msg:&quot;Pro proveden\u00ed v\u00fdpo\u010dtu mus\u00edte zvolit hodnotu do pole \u201eV\u00fdnos\u201c.&quot;,arg:[1,2,3,4,5,6,7,8]}"><option value="0"></option><option value="1">1,5 %</option><option value="2">2,5 %</option><option value="3">3,5 %</option><option value="4">4,5 %</option><option value="5">5,5 %</option><option value="6">6,5 %</option><option value="7">7,5 %</option><option value="8" selected="selected">8,5 %</option></select>
        </p>
        <p>
        <input type="submit" class="button" name="save" id="frmcalc-save" value="Vypočítat" />
        </p>
        </div>
        <div class="span-14 last">
            <div class="form-info" id="vynos-desc">
            <p>
            Pro jednotlivé způsoby investování očekávané
            (nikoli zaručené) přibližné rozmezí výnosu:
            </p>
            <ul>
            <li>2-3 % Fond Státních dluhopisů</li>
            <li>3-4 % Fond Konzervativní</li>
            <li>4-7 % Fond Vyvážený</li>
            <li>5-7 % Fond Dynamický</li>
            </ul>
            </div>
        </div>
    </div>
<div><input type="hidden" name="_form_" id="frmcalc-_form_" value="calc" /></div>
</form>


<div id="vysledek" class="container">

    

    <div class="span-9">
        <div class="result-frame"><div class="result-frame-border">
        <h2>Důchod při účasti pouze v I. pilíři</h2>
        <table>
            <tbody>
                <tr><th scope="row">Státní důchod (z 28%)</th><td class="currency">2 964 Kč</td></tr>
                <tr><th scope="row">Fondová složka (3%)</th><td class="currency">0 Kč</td></tr>
                <tr><th scope="row">Fondová složka (2%)</th><td class="currency" style="padding-bottom: 2.5em;">0 Kč</td></tr>
                <tr class="result"><th scope="row" class="large">Důchod celkem</th><td class="currency large">2 964 Kč</td></tr>
            </tbody>
        </table>
        </div></div>
    </div>
    <div class="span-9">
        <div class="result-frame"><div class="result-frame-border">    
        <h2>Důchod při účasti i ve II. pilíři</h2>
        <table>
            <tbody>
                <tr><th scope="row">Státní důchod (z 25%)</th><td class="currency">2 964 Kč</td></tr>
                <tr><th scope="row">Fondová složka (3%)</th><td class="currency">0 Kč</td></tr>
                <tr><th scope="row"><b style="margin-left: 1em;">Důchod z veřejného pojištění (25+3%)</b></th><td class="currency"><b>2 964 Kč</b></td></tr>
                <tr><th scope="row">Fondová složka (2%)</th><td class="currency">0 Kč</td></tr>
                <tr class="result"><th scope="row" class="large">Důchod celkem</th><td class="currency large">2 964 Kč</td></tr>
        </tbody></table>
        </div></div>
    </div>
    <div class="span-6 last">
        <div class="result-frame"><div class="result-frame-border">    
        <h2>Důchodový věk</h2>
        <div class="result">
        <p class="result-vek large">
        66 let
        2 měsíce
        </p>
        </div>
        <p style="margin-bottom: .9em;">
        Doba pojištění 46 let<br />
        Doba spoření 28  let
        </p>
        </div></div>
    </div>

    <p style="color: red; clear: left; padding-top: 1.5em">
        <b>Rozhodnutí o vstupu</b> do důchodového spoření <b>není nijak podmíněno předchozím 
        souhlasem zaměstnavatele</b>. Zaměstnanec, který se stane účastníkem, 
        má pouze povinnost zaměstnavateli písemně účast na důchodovém spoření oznámit.
    </p>
    <p style="color: red;">
        Bližší informace o povinnostech zaměstnavatele  vyplývajících zejména 
        přímo ze zákona č.&nbsp;397/2012&nbsp;Sb., o&nbsp;pojistném na důchodové spoření, 
        a zákona č.&nbsp;399/2012&nbsp;Sb. (tj. např. platit pojistné na důchodové spoření) 
        lze nalézt na <a href="http://cds.mfcr.cz/cps/rde/xchg/cds/xsl/duchodove_sporeni.html">http://cds.mfcr.cz/cps/rde/xchg/cds/xsl/duchodove_sporeni.html</a>.
    </p>

</div>

</div></div>

<div class="content-in disclaimer">

<h2>Jaké informace vám důchodová kalkulačka poskytne</h2>
<ul>
<li>Věk odchodu do důchodu</li>
<li>Předpokládaný měsíční důchod. Je přepočtený na „současné ceny“, abyste jej mohli porovnat s Vaší hrubou mzdou</li>
</ul>

<h2>Jaké varianty důchodu vám kalkulačka spočítá</h2>

<dl>
<dt>Varianta 1:</dt>
<dd>
<p>
Varianta 1:  Doživotní důchod od státu pro variantu, že se do reformy nezapojíte
</p>
</dd>

<dt>Varianta 2:</dt>
<dd>
<p>
Celkový doživotní důchod od státu a z II. pilíře pro variantu, že se reformy zúčastníte a vstoupíte do II. pilíře. Důchod bude mít 3 složky:
</p>
<ul>
<li>Důchod od státu snížený podle toho, kolik let skutečně platíte do II. pilíře</li>
<li>Důchod z osobního účtu II. pilíře z 3% pojistného (přesměrované povinné pojistné)</li>
<li>Důchod z osobního účtu II. pilíře z 2% pojistného (Vaše dodatečné vlastní prostředky)</li>
</ul>
</dd>
</dl>

<h2>Podrobnější vysvětlení</h2>
<ul>
<li>Důchodová kalkulačka poskytuje orientační výpočet budoucího důchodu a jejím základním cílem je porovnání výše důchodu pro účastníky, kteří se nezapojí nebo zapojí do II. pilíře. Má tak informovat pro koho a za jakých podmínek je výhodná účast ve II. pilíři.</li>
<li>Kalkulačka pracuje se zjednodušujícími předpoklady, které však umožňují porovnat výsledky dle data narození, pohlaví, počtu dětí a příjmové situace účastníka.</li>
<li>Příjmem se rozumí měsíční mzda v roce 2010. Předpokladem pak je, že současná úroveň výdělku zadavatele výpočtu poroste v budoucnu (až do důchodu) stejně jako průměrná mzda v ekonomice.</li> 
<li>Na základě uvážení uživatele kalkulačky je možné aktuální příjem upravit tak, aby zohledňoval očekávaný budoucí vývoj jeho výdělku.</li>
<li>Výnos penzijního fondu je uvažován v <b>nominálních hodnotách</b>, tedy bez očištění o inflaci. Inflace je uvažována ve výši 2&nbsp;%.</li>
<li>Kalkulačka budoucí důchod přepočítá tak, aby výsledný důchod odpovídal cenám a mzdám roku 2010.</li>
<li>Výnos v jednotlivém fondu, který si uživatel zvolí je výnos <b>čistý</b>, tedy takový, který by byl dosažen po odečtení poplatků za správu aktiv.</li>
<li>Poplatek za převod naspořených prostředků do doživotní anuity (důchodu) <b>je ve výpočtu zohledněn</b>.</li>
<li>Doživotní důchod je vypočten tak, že odpovídá očekávané střední délce dožití v okamžiku přiznání důchodu (tzn. v&nbsp;budoucnu), a to pro každý ročník narození.</li>
<li>Demografické předpoklady jsou převzaty z demografické prognózy Přírodovědecké fakulty Univerzity Karlovy z roku 2010.</li>
</ul>

</div>

    </div></div> <!-- /#content -->
    
    <div id="footer">
        <h4>Ministerstvo práce a sociálních věcí</h4>
        <p>
        Na Poříčním právu 1/376, 128 01 Praha 2<br />
        tel.: +420-221921111, fax: +420-224918391<br />
        e-mail: viz <a href="http://www.mpsv.cz/cs/13" title="Informace jak elektronickou cestou kontaktovat MPSV (odkaz se otevře v novém okně)" target="_blank">elektronická podatelna</a>
        <br />
        kontakt na technického správce: viz <a href="http://www.mpsv.cz/cs/924" title="Kliknutím na tento odkaz zobrazíte Prohlášení o přístupnosti"><span>prohlášení o přístupnosti</span></a></p>
    </div> <!-- /#footer -->
        

</div> <!-- /#main -->
</div> <!-- /#shadow -->

    
</body>
</html>
*/

?>
<?php

//'backup' of http://duchodovakalkulacka.mpsv.cz/www/
//just in case....

require 'scraperwiki/simple_html_dom.php'; 

$birth = array(1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010);
$sex = array(1,2,6);
$lower = array(0,1);
$salary = array(0,10000,15000,20000,25000,30000,40000,60000,90000);
$gain = array(1,4,8);

foreach ($birth as $b) {
  foreach ($sex as $s) {
    foreach ($lower as $l) {
      foreach ($salary as $sa) {
        foreach ($gain as $g) {
          $url = "http://duchodovakalkulacka.mpsv.cz/www/?rok_narozeni={$b}&pokles={$l}&pohlavi={$s}&mzda={$sa}&vynos={$g}&save=Vypo%C4%8D%C3%ADtat&_form_=calc";
          $html = scraperwiki::scrape($url);
          if (!strpos($html,'Důchodový věk byl dosažen před rokem 2013!')) {
            $dom = new simple_html_dom();
            $dom->load($html);
            $div = $dom->find('div[id=vysledek]',0);
            $out = array(
                'birth' => $b,
                'sex' => $s,
                'lower' => $l,
                'salary' => $sa,
                'gain' => $g,
                'html' => $div->outertext,
            );
            scraperwiki::save_sqlite(array('birth','sex','lower','salary','gain','html'),$out);
//die();
          }

          
        }
      }
    }
  }
} 

/* TO HAVE ALL THE COMMON TEXT: 
(http://duchodovakalkulacka.mpsv.cz/www/?rok_narozeni=1974&pokles=-1&pohlavi=6&mzda=0&vynos=8&save=Vypo%C4%8D%C3%ADtat&_form_=calc)

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <meta name="description" content="Důchodová kalkulačka" />

    <title>MPSV.CZ : Důchodová kalkulačka</title>

    <link rel="stylesheet" media="screen,projection,tv" href="/www/css/screen.css" type="text/css" />
    <link rel="stylesheet" media="print" href="/www/css/print.css" type="text/css" />
    <!--[if lt IE 8]>
        <link rel="stylesheet" href="/www/css/ie.css" type="text/css" media="screen, projection" />
    <![endif]-->
    <link rel="stylesheet" media="screen,projection,tv" href="/www/css/duchodovakalkulacka.css?v=1" type="text/css" />
    <link rel="shortcut icon" href="/www/favicon.ico" type="image/x-icon" />

        <script type="text/javascript" src="/www/js/netteForms.js"></script>
    
</head>

<body>

<div id="shadow">
<div id="main">
    <div id="header"><h1><a href="http://www.mpsv.cz" title="Zpět na titulní stránku MPSV"><span>Ministerstvo práce a sociálních věcí</span></a></h1></div>


    <div id="content"><div class="content-border">
<div class="content-in-w"><div class="content-in-w-border">
<h1 class="content-heading">Kalkulačka k důchodové reformě</h1>

<div class="skip"><a href="#vysledek" tabindex="1">Přejít na výsledek výpočtu</a></div>

<p>
Počátek spoření je rok 2013, pro rok narození 1994 a později ve 20 letech.
</p>

<p style="color: red;">
Kalkulačka v základní verzi počítá výši důchodů podle současné situace. Ti, 
kterým je dnes 30 let, ale musí počítat s tím, že jejich důchod od státu 
(z&nbsp;I.&nbsp;pilíře) bude ve srovnání se mzdami výrazně nižší než ten, který 
mají důchodci dnes. Například podle studie 
<a href="http://idea.cerge-ei.cz/documents/kratka_studie_2012_07.pdf">„Jaký důchod nás čeká?“</a> 
mohou být do budoucna státní důchody až o 50 procent nižší. Zkuste také druhou 
novou funkci naší kalkulačky, která vám ukáže předpokládaný budoucí důchod. 
Srovnejte a uvidíte, že je nutné, aby si každý sám spořil na stáří.
</p>

<form action="" method="get" id="frm-calc">
    
    <div class="container">
        <div class="span-4">
        <label class="required" for="frmcalc-rok_narozeni">Rok narození</label>
        </div>
        <div class="span-6">
        <select aria-required="aria-required" name="rok_narozeni" id="frmcalc-rok_narozeni" required="required" data-nette-rules="{op:':filled',msg:&quot;Vyberte, pros\u00edm, rok narozen\u00ed z nab\u00eddky.&quot;}"><option value="1950">1950</option><option value="1951">1951</option><option value="1952">1952</option><option value="1953">1953</option><option value="1954">1954</option><option value="1955">1955</option><option value="1956">1956</option><option value="1957">1957</option><option value="1958">1958</option><option value="1959">1959</option><option value="1960">1960</option><option value="1961">1961</option><option value="1962">1962</option><option value="1963">1963</option><option value="1964">1964</option><option value="1965">1965</option><option value="1966">1966</option><option value="1967">1967</option><option value="1968">1968</option><option value="1969">1969</option><option value="1970">1970</option><option value="1971">1971</option><option value="1972">1972</option><option value="1973">1973</option><option value="1974" selected="selected">1974</option><option value="1975">1975</option><option value="1976">1976</option><option value="1977">1977</option><option value="1978">1978</option><option value="1979">1979</option><option value="1980">1980</option><option value="1981">1981</option><option value="1982">1982</option><option value="1983">1983</option><option value="1984">1984</option><option value="1985">1985</option><option value="1986">1986</option><option value="1987">1987</option><option value="1988">1988</option><option value="1989">1989</option><option value="1990">1990</option><option value="1991">1991</option><option value="1992">1992</option><option value="1993">1993</option><option value="1994">1994</option><option value="1995">1995</option><option value="1996">1996</option><option value="1997">1997</option><option value="1998">1998</option><option value="1999">1999</option><option value="2000">2000</option><option value="2001">2001</option><option value="2002">2002</option><option value="2003">2003</option><option value="2004">2004</option><option value="2005">2005</option><option value="2006">2006</option><option value="2007">2007</option><option value="2008">2008</option><option value="2009">2009</option><option value="2010">2010</option></select>
        </div>
        <div class="span-14 last">
        <label for="frmcalc-pokles">Chcete v kalkulačce zohlednit předpoklad o poklesu státního důchodu?</label>
        <select name="pokles" id="frmcalc-pokles"><option value="0">Ne</option><option value="1">Ano</option></select>
        </div>
    </div>
    <div class="container">
        <div class="span-4">
        <label class="required" for="frmcalc-pohlavi">Pohlaví</label>
        </div>
        <div class="span-6 with-tooltip">
        <select aria-describedby="pohlavi-desc" aria-required="aria-required" name="pohlavi" id="frmcalc-pohlavi" required="required" data-nette-rules="{op:':filled',msg:&quot;Vyberte, pros\u00edm, pohlav\u00ed z nab\u00eddky.&quot;}"><option value="1">Muž</option><option value="2">Žena: 0 dětí</option><option value="3">Žena: 1 dítě</option><option value="4">Žena: 2 děti</option><option value="5">Žena: 3 nebo 4 děti</option><option value="6" selected="selected">Žena: 5 a více dětí</option></select>
        </div>
        <div class="span-14 last">
            <div class="form-info" id="pohlavi-desc">
            <p>U žen celkový počet dětí, tzn. současných i plánovaných</p>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="span-4" id="mzda-label">
        <label class="required" for="frmcalc-mzda">Hrubá mzda</label>
        </div>
        <div class="span-6 with-tooltip">
        <input aria-labelledby="mzda-label frmcalc-mzda mzda-mena" aria-describedby="mzda-desc" type="text" size="6" aria-required="aria-required" class="text" name="mzda" id="frmcalc-mzda" required="required" data-nette-rules="{op:':filled',msg:&quot;Zadejte, pros\u00edm, hrubou mzdu.&quot;},{op:':integer',msg:&quot;Do pole hrub\u00e1 mzda zadejte pouze \u010d\u00edslice - \u010d\u00e1stku v korun\u00e1ch.&quot;},{op:':range',msg:&quot;Zadejte, pros\u00edm, hrubou mzdu jako kladn\u00e9 \u010d\u00edslo.&quot;,arg:[0,1000000000]}" value="0" /><span class="kc" id="mzda-mena">Kč</span>
        </div>
        <div class="span-14 last">
            <div class="form-info" id="mzda-desc">
            <p>Průměrný měsíční hrubý příjem (1/12 ročního)</p>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="span-4">
        <label for="frmcalc-vynos">Výnos</label>
        </div>
        <div class="span-6 with-tooltip">
        <p>
        <select aria-describedby="vynos-desc" aria-required="aria-required" name="vynos" id="frmcalc-vynos" data-nette-rules="{op:':equal',msg:&quot;Pro proveden\u00ed v\u00fdpo\u010dtu mus\u00edte zvolit hodnotu do pole \u201eV\u00fdnos\u201c.&quot;,arg:[1,2,3,4,5,6,7,8]}"><option value="0"></option><option value="1">1,5 %</option><option value="2">2,5 %</option><option value="3">3,5 %</option><option value="4">4,5 %</option><option value="5">5,5 %</option><option value="6">6,5 %</option><option value="7">7,5 %</option><option value="8" selected="selected">8,5 %</option></select>
        </p>
        <p>
        <input type="submit" class="button" name="save" id="frmcalc-save" value="Vypočítat" />
        </p>
        </div>
        <div class="span-14 last">
            <div class="form-info" id="vynos-desc">
            <p>
            Pro jednotlivé způsoby investování očekávané
            (nikoli zaručené) přibližné rozmezí výnosu:
            </p>
            <ul>
            <li>2-3 % Fond Státních dluhopisů</li>
            <li>3-4 % Fond Konzervativní</li>
            <li>4-7 % Fond Vyvážený</li>
            <li>5-7 % Fond Dynamický</li>
            </ul>
            </div>
        </div>
    </div>
<div><input type="hidden" name="_form_" id="frmcalc-_form_" value="calc" /></div>
</form>


<div id="vysledek" class="container">

    

    <div class="span-9">
        <div class="result-frame"><div class="result-frame-border">
        <h2>Důchod při účasti pouze v I. pilíři</h2>
        <table>
            <tbody>
                <tr><th scope="row">Státní důchod (z 28%)</th><td class="currency">2 964 Kč</td></tr>
                <tr><th scope="row">Fondová složka (3%)</th><td class="currency">0 Kč</td></tr>
                <tr><th scope="row">Fondová složka (2%)</th><td class="currency" style="padding-bottom: 2.5em;">0 Kč</td></tr>
                <tr class="result"><th scope="row" class="large">Důchod celkem</th><td class="currency large">2 964 Kč</td></tr>
            </tbody>
        </table>
        </div></div>
    </div>
    <div class="span-9">
        <div class="result-frame"><div class="result-frame-border">    
        <h2>Důchod při účasti i ve II. pilíři</h2>
        <table>
            <tbody>
                <tr><th scope="row">Státní důchod (z 25%)</th><td class="currency">2 964 Kč</td></tr>
                <tr><th scope="row">Fondová složka (3%)</th><td class="currency">0 Kč</td></tr>
                <tr><th scope="row"><b style="margin-left: 1em;">Důchod z veřejného pojištění (25+3%)</b></th><td class="currency"><b>2 964 Kč</b></td></tr>
                <tr><th scope="row">Fondová složka (2%)</th><td class="currency">0 Kč</td></tr>
                <tr class="result"><th scope="row" class="large">Důchod celkem</th><td class="currency large">2 964 Kč</td></tr>
        </tbody></table>
        </div></div>
    </div>
    <div class="span-6 last">
        <div class="result-frame"><div class="result-frame-border">    
        <h2>Důchodový věk</h2>
        <div class="result">
        <p class="result-vek large">
        66 let
        2 měsíce
        </p>
        </div>
        <p style="margin-bottom: .9em;">
        Doba pojištění 46 let<br />
        Doba spoření 28  let
        </p>
        </div></div>
    </div>

    <p style="color: red; clear: left; padding-top: 1.5em">
        <b>Rozhodnutí o vstupu</b> do důchodového spoření <b>není nijak podmíněno předchozím 
        souhlasem zaměstnavatele</b>. Zaměstnanec, který se stane účastníkem, 
        má pouze povinnost zaměstnavateli písemně účast na důchodovém spoření oznámit.
    </p>
    <p style="color: red;">
        Bližší informace o povinnostech zaměstnavatele  vyplývajících zejména 
        přímo ze zákona č.&nbsp;397/2012&nbsp;Sb., o&nbsp;pojistném na důchodové spoření, 
        a zákona č.&nbsp;399/2012&nbsp;Sb. (tj. např. platit pojistné na důchodové spoření) 
        lze nalézt na <a href="http://cds.mfcr.cz/cps/rde/xchg/cds/xsl/duchodove_sporeni.html">http://cds.mfcr.cz/cps/rde/xchg/cds/xsl/duchodove_sporeni.html</a>.
    </p>

</div>

</div></div>

<div class="content-in disclaimer">

<h2>Jaké informace vám důchodová kalkulačka poskytne</h2>
<ul>
<li>Věk odchodu do důchodu</li>
<li>Předpokládaný měsíční důchod. Je přepočtený na „současné ceny“, abyste jej mohli porovnat s Vaší hrubou mzdou</li>
</ul>

<h2>Jaké varianty důchodu vám kalkulačka spočítá</h2>

<dl>
<dt>Varianta 1:</dt>
<dd>
<p>
Varianta 1:  Doživotní důchod od státu pro variantu, že se do reformy nezapojíte
</p>
</dd>

<dt>Varianta 2:</dt>
<dd>
<p>
Celkový doživotní důchod od státu a z II. pilíře pro variantu, že se reformy zúčastníte a vstoupíte do II. pilíře. Důchod bude mít 3 složky:
</p>
<ul>
<li>Důchod od státu snížený podle toho, kolik let skutečně platíte do II. pilíře</li>
<li>Důchod z osobního účtu II. pilíře z 3% pojistného (přesměrované povinné pojistné)</li>
<li>Důchod z osobního účtu II. pilíře z 2% pojistného (Vaše dodatečné vlastní prostředky)</li>
</ul>
</dd>
</dl>

<h2>Podrobnější vysvětlení</h2>
<ul>
<li>Důchodová kalkulačka poskytuje orientační výpočet budoucího důchodu a jejím základním cílem je porovnání výše důchodu pro účastníky, kteří se nezapojí nebo zapojí do II. pilíře. Má tak informovat pro koho a za jakých podmínek je výhodná účast ve II. pilíři.</li>
<li>Kalkulačka pracuje se zjednodušujícími předpoklady, které však umožňují porovnat výsledky dle data narození, pohlaví, počtu dětí a příjmové situace účastníka.</li>
<li>Příjmem se rozumí měsíční mzda v roce 2010. Předpokladem pak je, že současná úroveň výdělku zadavatele výpočtu poroste v budoucnu (až do důchodu) stejně jako průměrná mzda v ekonomice.</li> 
<li>Na základě uvážení uživatele kalkulačky je možné aktuální příjem upravit tak, aby zohledňoval očekávaný budoucí vývoj jeho výdělku.</li>
<li>Výnos penzijního fondu je uvažován v <b>nominálních hodnotách</b>, tedy bez očištění o inflaci. Inflace je uvažována ve výši 2&nbsp;%.</li>
<li>Kalkulačka budoucí důchod přepočítá tak, aby výsledný důchod odpovídal cenám a mzdám roku 2010.</li>
<li>Výnos v jednotlivém fondu, který si uživatel zvolí je výnos <b>čistý</b>, tedy takový, který by byl dosažen po odečtení poplatků za správu aktiv.</li>
<li>Poplatek za převod naspořených prostředků do doživotní anuity (důchodu) <b>je ve výpočtu zohledněn</b>.</li>
<li>Doživotní důchod je vypočten tak, že odpovídá očekávané střední délce dožití v okamžiku přiznání důchodu (tzn. v&nbsp;budoucnu), a to pro každý ročník narození.</li>
<li>Demografické předpoklady jsou převzaty z demografické prognózy Přírodovědecké fakulty Univerzity Karlovy z roku 2010.</li>
</ul>

</div>

    </div></div> <!-- /#content -->
    
    <div id="footer">
        <h4>Ministerstvo práce a sociálních věcí</h4>
        <p>
        Na Poříčním právu 1/376, 128 01 Praha 2<br />
        tel.: +420-221921111, fax: +420-224918391<br />
        e-mail: viz <a href="http://www.mpsv.cz/cs/13" title="Informace jak elektronickou cestou kontaktovat MPSV (odkaz se otevře v novém okně)" target="_blank">elektronická podatelna</a>
        <br />
        kontakt na technického správce: viz <a href="http://www.mpsv.cz/cs/924" title="Kliknutím na tento odkaz zobrazíte Prohlášení o přístupnosti"><span>prohlášení o přístupnosti</span></a></p>
    </div> <!-- /#footer -->
        

</div> <!-- /#main -->
</div> <!-- /#shadow -->

    
</body>
</html>
*/

?>
<?php

//'backup' of http://duchodovakalkulacka.mpsv.cz/www/
//just in case....

require 'scraperwiki/simple_html_dom.php'; 

$birth = array(1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010);
$sex = array(1,2,6);
$lower = array(0,1);
$salary = array(0,10000,15000,20000,25000,30000,40000,60000,90000);
$gain = array(1,4,8);

foreach ($birth as $b) {
  foreach ($sex as $s) {
    foreach ($lower as $l) {
      foreach ($salary as $sa) {
        foreach ($gain as $g) {
          $url = "http://duchodovakalkulacka.mpsv.cz/www/?rok_narozeni={$b}&pokles={$l}&pohlavi={$s}&mzda={$sa}&vynos={$g}&save=Vypo%C4%8D%C3%ADtat&_form_=calc";
          $html = scraperwiki::scrape($url);
          if (!strpos($html,'Důchodový věk byl dosažen před rokem 2013!')) {
            $dom = new simple_html_dom();
            $dom->load($html);
            $div = $dom->find('div[id=vysledek]',0);
            $out = array(
                'birth' => $b,
                'sex' => $s,
                'lower' => $l,
                'salary' => $sa,
                'gain' => $g,
                'html' => $div->outertext,
            );
            scraperwiki::save_sqlite(array('birth','sex','lower','salary','gain','html'),$out);
//die();
          }

          
        }
      }
    }
  }
} 

/* TO HAVE ALL THE COMMON TEXT: 
(http://duchodovakalkulacka.mpsv.cz/www/?rok_narozeni=1974&pokles=-1&pohlavi=6&mzda=0&vynos=8&save=Vypo%C4%8D%C3%ADtat&_form_=calc)

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <meta name="description" content="Důchodová kalkulačka" />

    <title>MPSV.CZ : Důchodová kalkulačka</title>

    <link rel="stylesheet" media="screen,projection,tv" href="/www/css/screen.css" type="text/css" />
    <link rel="stylesheet" media="print" href="/www/css/print.css" type="text/css" />
    <!--[if lt IE 8]>
        <link rel="stylesheet" href="/www/css/ie.css" type="text/css" media="screen, projection" />
    <![endif]-->
    <link rel="stylesheet" media="screen,projection,tv" href="/www/css/duchodovakalkulacka.css?v=1" type="text/css" />
    <link rel="shortcut icon" href="/www/favicon.ico" type="image/x-icon" />

        <script type="text/javascript" src="/www/js/netteForms.js"></script>
    
</head>

<body>

<div id="shadow">
<div id="main">
    <div id="header"><h1><a href="http://www.mpsv.cz" title="Zpět na titulní stránku MPSV"><span>Ministerstvo práce a sociálních věcí</span></a></h1></div>


    <div id="content"><div class="content-border">
<div class="content-in-w"><div class="content-in-w-border">
<h1 class="content-heading">Kalkulačka k důchodové reformě</h1>

<div class="skip"><a href="#vysledek" tabindex="1">Přejít na výsledek výpočtu</a></div>

<p>
Počátek spoření je rok 2013, pro rok narození 1994 a později ve 20 letech.
</p>

<p style="color: red;">
Kalkulačka v základní verzi počítá výši důchodů podle současné situace. Ti, 
kterým je dnes 30 let, ale musí počítat s tím, že jejich důchod od státu 
(z&nbsp;I.&nbsp;pilíře) bude ve srovnání se mzdami výrazně nižší než ten, který 
mají důchodci dnes. Například podle studie 
<a href="http://idea.cerge-ei.cz/documents/kratka_studie_2012_07.pdf">„Jaký důchod nás čeká?“</a> 
mohou být do budoucna státní důchody až o 50 procent nižší. Zkuste také druhou 
novou funkci naší kalkulačky, která vám ukáže předpokládaný budoucí důchod. 
Srovnejte a uvidíte, že je nutné, aby si každý sám spořil na stáří.
</p>

<form action="" method="get" id="frm-calc">
    
    <div class="container">
        <div class="span-4">
        <label class="required" for="frmcalc-rok_narozeni">Rok narození</label>
        </div>
        <div class="span-6">
        <select aria-required="aria-required" name="rok_narozeni" id="frmcalc-rok_narozeni" required="required" data-nette-rules="{op:':filled',msg:&quot;Vyberte, pros\u00edm, rok narozen\u00ed z nab\u00eddky.&quot;}"><option value="1950">1950</option><option value="1951">1951</option><option value="1952">1952</option><option value="1953">1953</option><option value="1954">1954</option><option value="1955">1955</option><option value="1956">1956</option><option value="1957">1957</option><option value="1958">1958</option><option value="1959">1959</option><option value="1960">1960</option><option value="1961">1961</option><option value="1962">1962</option><option value="1963">1963</option><option value="1964">1964</option><option value="1965">1965</option><option value="1966">1966</option><option value="1967">1967</option><option value="1968">1968</option><option value="1969">1969</option><option value="1970">1970</option><option value="1971">1971</option><option value="1972">1972</option><option value="1973">1973</option><option value="1974" selected="selected">1974</option><option value="1975">1975</option><option value="1976">1976</option><option value="1977">1977</option><option value="1978">1978</option><option value="1979">1979</option><option value="1980">1980</option><option value="1981">1981</option><option value="1982">1982</option><option value="1983">1983</option><option value="1984">1984</option><option value="1985">1985</option><option value="1986">1986</option><option value="1987">1987</option><option value="1988">1988</option><option value="1989">1989</option><option value="1990">1990</option><option value="1991">1991</option><option value="1992">1992</option><option value="1993">1993</option><option value="1994">1994</option><option value="1995">1995</option><option value="1996">1996</option><option value="1997">1997</option><option value="1998">1998</option><option value="1999">1999</option><option value="2000">2000</option><option value="2001">2001</option><option value="2002">2002</option><option value="2003">2003</option><option value="2004">2004</option><option value="2005">2005</option><option value="2006">2006</option><option value="2007">2007</option><option value="2008">2008</option><option value="2009">2009</option><option value="2010">2010</option></select>
        </div>
        <div class="span-14 last">
        <label for="frmcalc-pokles">Chcete v kalkulačce zohlednit předpoklad o poklesu státního důchodu?</label>
        <select name="pokles" id="frmcalc-pokles"><option value="0">Ne</option><option value="1">Ano</option></select>
        </div>
    </div>
    <div class="container">
        <div class="span-4">
        <label class="required" for="frmcalc-pohlavi">Pohlaví</label>
        </div>
        <div class="span-6 with-tooltip">
        <select aria-describedby="pohlavi-desc" aria-required="aria-required" name="pohlavi" id="frmcalc-pohlavi" required="required" data-nette-rules="{op:':filled',msg:&quot;Vyberte, pros\u00edm, pohlav\u00ed z nab\u00eddky.&quot;}"><option value="1">Muž</option><option value="2">Žena: 0 dětí</option><option value="3">Žena: 1 dítě</option><option value="4">Žena: 2 děti</option><option value="5">Žena: 3 nebo 4 děti</option><option value="6" selected="selected">Žena: 5 a více dětí</option></select>
        </div>
        <div class="span-14 last">
            <div class="form-info" id="pohlavi-desc">
            <p>U žen celkový počet dětí, tzn. současných i plánovaných</p>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="span-4" id="mzda-label">
        <label class="required" for="frmcalc-mzda">Hrubá mzda</label>
        </div>
        <div class="span-6 with-tooltip">
        <input aria-labelledby="mzda-label frmcalc-mzda mzda-mena" aria-describedby="mzda-desc" type="text" size="6" aria-required="aria-required" class="text" name="mzda" id="frmcalc-mzda" required="required" data-nette-rules="{op:':filled',msg:&quot;Zadejte, pros\u00edm, hrubou mzdu.&quot;},{op:':integer',msg:&quot;Do pole hrub\u00e1 mzda zadejte pouze \u010d\u00edslice - \u010d\u00e1stku v korun\u00e1ch.&quot;},{op:':range',msg:&quot;Zadejte, pros\u00edm, hrubou mzdu jako kladn\u00e9 \u010d\u00edslo.&quot;,arg:[0,1000000000]}" value="0" /><span class="kc" id="mzda-mena">Kč</span>
        </div>
        <div class="span-14 last">
            <div class="form-info" id="mzda-desc">
            <p>Průměrný měsíční hrubý příjem (1/12 ročního)</p>
            </div>
        </div>
    </div>
    <div class="container">
        <div class="span-4">
        <label for="frmcalc-vynos">Výnos</label>
        </div>
        <div class="span-6 with-tooltip">
        <p>
        <select aria-describedby="vynos-desc" aria-required="aria-required" name="vynos" id="frmcalc-vynos" data-nette-rules="{op:':equal',msg:&quot;Pro proveden\u00ed v\u00fdpo\u010dtu mus\u00edte zvolit hodnotu do pole \u201eV\u00fdnos\u201c.&quot;,arg:[1,2,3,4,5,6,7,8]}"><option value="0"></option><option value="1">1,5 %</option><option value="2">2,5 %</option><option value="3">3,5 %</option><option value="4">4,5 %</option><option value="5">5,5 %</option><option value="6">6,5 %</option><option value="7">7,5 %</option><option value="8" selected="selected">8,5 %</option></select>
        </p>
        <p>
        <input type="submit" class="button" name="save" id="frmcalc-save" value="Vypočítat" />
        </p>
        </div>
        <div class="span-14 last">
            <div class="form-info" id="vynos-desc">
            <p>
            Pro jednotlivé způsoby investování očekávané
            (nikoli zaručené) přibližné rozmezí výnosu:
            </p>
            <ul>
            <li>2-3 % Fond Státních dluhopisů</li>
            <li>3-4 % Fond Konzervativní</li>
            <li>4-7 % Fond Vyvážený</li>
            <li>5-7 % Fond Dynamický</li>
            </ul>
            </div>
        </div>
    </div>
<div><input type="hidden" name="_form_" id="frmcalc-_form_" value="calc" /></div>
</form>


<div id="vysledek" class="container">

    

    <div class="span-9">
        <div class="result-frame"><div class="result-frame-border">
        <h2>Důchod při účasti pouze v I. pilíři</h2>
        <table>
            <tbody>
                <tr><th scope="row">Státní důchod (z 28%)</th><td class="currency">2 964 Kč</td></tr>
                <tr><th scope="row">Fondová složka (3%)</th><td class="currency">0 Kč</td></tr>
                <tr><th scope="row">Fondová složka (2%)</th><td class="currency" style="padding-bottom: 2.5em;">0 Kč</td></tr>
                <tr class="result"><th scope="row" class="large">Důchod celkem</th><td class="currency large">2 964 Kč</td></tr>
            </tbody>
        </table>
        </div></div>
    </div>
    <div class="span-9">
        <div class="result-frame"><div class="result-frame-border">    
        <h2>Důchod při účasti i ve II. pilíři</h2>
        <table>
            <tbody>
                <tr><th scope="row">Státní důchod (z 25%)</th><td class="currency">2 964 Kč</td></tr>
                <tr><th scope="row">Fondová složka (3%)</th><td class="currency">0 Kč</td></tr>
                <tr><th scope="row"><b style="margin-left: 1em;">Důchod z veřejného pojištění (25+3%)</b></th><td class="currency"><b>2 964 Kč</b></td></tr>
                <tr><th scope="row">Fondová složka (2%)</th><td class="currency">0 Kč</td></tr>
                <tr class="result"><th scope="row" class="large">Důchod celkem</th><td class="currency large">2 964 Kč</td></tr>
        </tbody></table>
        </div></div>
    </div>
    <div class="span-6 last">
        <div class="result-frame"><div class="result-frame-border">    
        <h2>Důchodový věk</h2>
        <div class="result">
        <p class="result-vek large">
        66 let
        2 měsíce
        </p>
        </div>
        <p style="margin-bottom: .9em;">
        Doba pojištění 46 let<br />
        Doba spoření 28  let
        </p>
        </div></div>
    </div>

    <p style="color: red; clear: left; padding-top: 1.5em">
        <b>Rozhodnutí o vstupu</b> do důchodového spoření <b>není nijak podmíněno předchozím 
        souhlasem zaměstnavatele</b>. Zaměstnanec, který se stane účastníkem, 
        má pouze povinnost zaměstnavateli písemně účast na důchodovém spoření oznámit.
    </p>
    <p style="color: red;">
        Bližší informace o povinnostech zaměstnavatele  vyplývajících zejména 
        přímo ze zákona č.&nbsp;397/2012&nbsp;Sb., o&nbsp;pojistném na důchodové spoření, 
        a zákona č.&nbsp;399/2012&nbsp;Sb. (tj. např. platit pojistné na důchodové spoření) 
        lze nalézt na <a href="http://cds.mfcr.cz/cps/rde/xchg/cds/xsl/duchodove_sporeni.html">http://cds.mfcr.cz/cps/rde/xchg/cds/xsl/duchodove_sporeni.html</a>.
    </p>

</div>

</div></div>

<div class="content-in disclaimer">

<h2>Jaké informace vám důchodová kalkulačka poskytne</h2>
<ul>
<li>Věk odchodu do důchodu</li>
<li>Předpokládaný měsíční důchod. Je přepočtený na „současné ceny“, abyste jej mohli porovnat s Vaší hrubou mzdou</li>
</ul>

<h2>Jaké varianty důchodu vám kalkulačka spočítá</h2>

<dl>
<dt>Varianta 1:</dt>
<dd>
<p>
Varianta 1:  Doživotní důchod od státu pro variantu, že se do reformy nezapojíte
</p>
</dd>

<dt>Varianta 2:</dt>
<dd>
<p>
Celkový doživotní důchod od státu a z II. pilíře pro variantu, že se reformy zúčastníte a vstoupíte do II. pilíře. Důchod bude mít 3 složky:
</p>
<ul>
<li>Důchod od státu snížený podle toho, kolik let skutečně platíte do II. pilíře</li>
<li>Důchod z osobního účtu II. pilíře z 3% pojistného (přesměrované povinné pojistné)</li>
<li>Důchod z osobního účtu II. pilíře z 2% pojistného (Vaše dodatečné vlastní prostředky)</li>
</ul>
</dd>
</dl>

<h2>Podrobnější vysvětlení</h2>
<ul>
<li>Důchodová kalkulačka poskytuje orientační výpočet budoucího důchodu a jejím základním cílem je porovnání výše důchodu pro účastníky, kteří se nezapojí nebo zapojí do II. pilíře. Má tak informovat pro koho a za jakých podmínek je výhodná účast ve II. pilíři.</li>
<li>Kalkulačka pracuje se zjednodušujícími předpoklady, které však umožňují porovnat výsledky dle data narození, pohlaví, počtu dětí a příjmové situace účastníka.</li>
<li>Příjmem se rozumí měsíční mzda v roce 2010. Předpokladem pak je, že současná úroveň výdělku zadavatele výpočtu poroste v budoucnu (až do důchodu) stejně jako průměrná mzda v ekonomice.</li> 
<li>Na základě uvážení uživatele kalkulačky je možné aktuální příjem upravit tak, aby zohledňoval očekávaný budoucí vývoj jeho výdělku.</li>
<li>Výnos penzijního fondu je uvažován v <b>nominálních hodnotách</b>, tedy bez očištění o inflaci. Inflace je uvažována ve výši 2&nbsp;%.</li>
<li>Kalkulačka budoucí důchod přepočítá tak, aby výsledný důchod odpovídal cenám a mzdám roku 2010.</li>
<li>Výnos v jednotlivém fondu, který si uživatel zvolí je výnos <b>čistý</b>, tedy takový, který by byl dosažen po odečtení poplatků za správu aktiv.</li>
<li>Poplatek za převod naspořených prostředků do doživotní anuity (důchodu) <b>je ve výpočtu zohledněn</b>.</li>
<li>Doživotní důchod je vypočten tak, že odpovídá očekávané střední délce dožití v okamžiku přiznání důchodu (tzn. v&nbsp;budoucnu), a to pro každý ročník narození.</li>
<li>Demografické předpoklady jsou převzaty z demografické prognózy Přírodovědecké fakulty Univerzity Karlovy z roku 2010.</li>
</ul>

</div>

    </div></div> <!-- /#content -->
    
    <div id="footer">
        <h4>Ministerstvo práce a sociálních věcí</h4>
        <p>
        Na Poříčním právu 1/376, 128 01 Praha 2<br />
        tel.: +420-221921111, fax: +420-224918391<br />
        e-mail: viz <a href="http://www.mpsv.cz/cs/13" title="Informace jak elektronickou cestou kontaktovat MPSV (odkaz se otevře v novém okně)" target="_blank">elektronická podatelna</a>
        <br />
        kontakt na technického správce: viz <a href="http://www.mpsv.cz/cs/924" title="Kliknutím na tento odkaz zobrazíte Prohlášení o přístupnosti"><span>prohlášení o přístupnosti</span></a></p>
    </div> <!-- /#footer -->
        

</div> <!-- /#main -->
</div> <!-- /#shadow -->

    
</body>
</html>
*/

?>
