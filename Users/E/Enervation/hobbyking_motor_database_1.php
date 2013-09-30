
<style type="text/css">
table.reference
{
    background-color:#ffffff;
    border:1px solid #c3c3c3;
    border-collapse:collapse;
}

table.reference th
{
    background-color:#e5eecc;
    border:1px solid #c3c3c3;
    padding:3px;
    vertical-align:top;
}

table.reference td
{
    border:1px solid #c3c3c3;
    padding:3px;
    vertical-align:top;
}
</style>

<?php
$sourcescraper = 'hobbyking_motor_database';
scraperwiki::attach($sourcescraper);
$orderCol = 'efficiency';
$data = scraperwiki::select("*, `Power(W)` / `weight (g)` as efficiency from $sourcescraper.swdata order by `$orderCol` desc limit 50" );

print "<table class='reference' border='1' cellpadding='0' cellspacing='0'>";
print '<tr>';
print '<th>Price</th>';
print '<th>Power (W)</th>';
print '<th>Weight</th>';
print '<th>Efficiency (W/g)</th>';
print '<th>Product ID</th>';

foreach($data as $motor)
{
    $weight = $motor["Weight (g)"];
    $power = $motor["Power(W)"];
    $price = $motor["price"];
    $efficiency = $motor["efficiency"];
    $id = $motor["id"];
    $link = "http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=$id";

    print "<tr>";
    print "<td>$price</td>";
    print "<td>$power</td>";
    print "<td>$weight</td>";
    print "<td>$efficiency</td>";
    print "<td><a href='$link'>$id</a></td>";
    print "</tr>";
}
print "</table>";
?>
<style type="text/css">
table.reference
{
    background-color:#ffffff;
    border:1px solid #c3c3c3;
    border-collapse:collapse;
}

table.reference th
{
    background-color:#e5eecc;
    border:1px solid #c3c3c3;
    padding:3px;
    vertical-align:top;
}

table.reference td
{
    border:1px solid #c3c3c3;
    padding:3px;
    vertical-align:top;
}
</style>

<?php
$sourcescraper = 'hobbyking_motor_database';
scraperwiki::attach($sourcescraper);
$orderCol = 'efficiency';
$data = scraperwiki::select("*, `Power(W)` / `weight (g)` as efficiency from $sourcescraper.swdata order by `$orderCol` desc limit 50" );

print "<table class='reference' border='1' cellpadding='0' cellspacing='0'>";
print '<tr>';
print '<th>Price</th>';
print '<th>Power (W)</th>';
print '<th>Weight</th>';
print '<th>Efficiency (W/g)</th>';
print '<th>Product ID</th>';

foreach($data as $motor)
{
    $weight = $motor["Weight (g)"];
    $power = $motor["Power(W)"];
    $price = $motor["price"];
    $efficiency = $motor["efficiency"];
    $id = $motor["id"];
    $link = "http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=$id";

    print "<tr>";
    print "<td>$price</td>";
    print "<td>$power</td>";
    print "<td>$weight</td>";
    print "<td>$efficiency</td>";
    print "<td><a href='$link'>$id</a></td>";
    print "</tr>";
}
print "</table>";
?>