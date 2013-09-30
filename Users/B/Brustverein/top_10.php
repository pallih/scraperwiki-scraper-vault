<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>
            MDH Top 10
        </title>
        <meta name="generator" content="TextMate http://macromates.com/">
        <meta name="author" content="Jan Krummrey"><!-- Date: 2011-12-13 -->
    </head>
    <body>
<?php
$sourcescraper = 'mdh-profil-suche-auto';

scraperwiki::attach($sourcescraper); 

$data = scraperwiki::select( "* from swdata order by BHCup desc limit 10" ); 
//print_r($data);


print "<table>"; 
print "<tr><th>Name</th><th>BH-Groesse</th><th>Bild</th>"; 
foreach($data as $d){ 
    print "<tr>"; 
        print "<td>" . $d["Vorname"] . "</td>"; 
        print "<td>" . $d["BHUmfang"].$d["BHCup"]."</td>"; 
        print '<td><img src="' . $d["ProfilBild"] . '"></td>'; 
    print "</tr>"; } print "</table>";
?>
    </body>
</html>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <title>
            MDH Top 10
        </title>
        <meta name="generator" content="TextMate http://macromates.com/">
        <meta name="author" content="Jan Krummrey"><!-- Date: 2011-12-13 -->
    </head>
    <body>
<?php
$sourcescraper = 'mdh-profil-suche-auto';

scraperwiki::attach($sourcescraper); 

$data = scraperwiki::select( "* from swdata order by BHCup desc limit 10" ); 
//print_r($data);


print "<table>"; 
print "<tr><th>Name</th><th>BH-Groesse</th><th>Bild</th>"; 
foreach($data as $d){ 
    print "<tr>"; 
        print "<td>" . $d["Vorname"] . "</td>"; 
        print "<td>" . $d["BHUmfang"].$d["BHCup"]."</td>"; 
        print '<td><img src="' . $d["ProfilBild"] . '"></td>'; 
    print "</tr>"; } print "</table>";
?>
    </body>
</html>

