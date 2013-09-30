<?php
# Blank PHP
$sourcescraper = 'tunisia_postal_codes';
scraperwiki::attach($sourcescraper);
$data = scraperwiki::select(           
    "* from data order by id"
);
?>
<!DOCTYPE html>           
<html>
    <head>
        <title>Tunisia Postal codes 2012</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <meta charset="UTF-8">
        <style type="text/css">
            html, body {
                font-family: trebuchet ms;
                font-size: 12px;
            }
            .tbl {
                border-collapse:collapse;
            }

            .tbl td {
                border:solid 1px gray;
                padding: 3px;
            }

            
        </style>
    </head>
<body>
<h1>Tunisia Postal codes</h1>

<table class="tbl">
    <tr>
        <th>id</th>
        <th>Guvernorate</th>
        <th>Delegation</th>
        <th>Locality</th>
        <th>Postal code</th>
    <tr>
<?php foreach($data as $d){ ?>
    <tr><td><?php echo $d['id']; ?></td><td><?php echo $d['guvernorate']; ?></td><td><?php echo $d['delegation']; ?></td><td><?php echo $d['localite']; ?></td><td><?php echo $d['postal_code']; ?></td></tr>
<?php } ?>
</table>
<p>Data colected at 5 december 2012, source: <a href="http://www.poste.tn/codes.php">http://www.poste.tn/codes.php</a> </p>
</body>
</html>
<?php
# Blank PHP
$sourcescraper = 'tunisia_postal_codes';
scraperwiki::attach($sourcescraper);
$data = scraperwiki::select(           
    "* from data order by id"
);
?>
<!DOCTYPE html>           
<html>
    <head>
        <title>Tunisia Postal codes 2012</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
        <meta charset="UTF-8">
        <style type="text/css">
            html, body {
                font-family: trebuchet ms;
                font-size: 12px;
            }
            .tbl {
                border-collapse:collapse;
            }

            .tbl td {
                border:solid 1px gray;
                padding: 3px;
            }

            
        </style>
    </head>
<body>
<h1>Tunisia Postal codes</h1>

<table class="tbl">
    <tr>
        <th>id</th>
        <th>Guvernorate</th>
        <th>Delegation</th>
        <th>Locality</th>
        <th>Postal code</th>
    <tr>
<?php foreach($data as $d){ ?>
    <tr><td><?php echo $d['id']; ?></td><td><?php echo $d['guvernorate']; ?></td><td><?php echo $d['delegation']; ?></td><td><?php echo $d['localite']; ?></td><td><?php echo $d['postal_code']; ?></td></tr>
<?php } ?>
</table>
<p>Data colected at 5 december 2012, source: <a href="http://www.poste.tn/codes.php">http://www.poste.tn/codes.php</a> </p>
</body>
</html>
