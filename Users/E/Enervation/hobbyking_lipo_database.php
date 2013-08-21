<?php
# Blank PHP
$sourcescraper = 'hobbyking';
scraperwiki::attach($sourcescraper);
$orderCol = 'Value (Wh/$)';
$data = scraperwiki::select("* from $sourcescraper.swdata where `Config(s)` = 6 order by `$orderCol` desc limit 50" );
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
$link = "http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=11902";

print "<table class='reference' border='1' cellpadding='0' cellspacing='0'>";
print '<tr><th>Cells</th><th>Capacity (mAh)</th><th>Price</th><th>Watt Hours</th><th>Wh / $</th><th>Product ID</th>';

foreach($data as $battery)
{
    $cells = $battery["Config(s)"];
    $capacity = $battery["Capacity(mAh)"];
    $price = $battery["price"]; 
    $energy= sprintf("%.2f", $battery["Energy (Wh)"]); 
    $value = sprintf("%.2f", $battery["Value (Wh/$)"]);
    $id = $battery["id"];
    $link = "http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=$id";

    print "<tr>";
    print "<td>$cells</td>";
    print "<td>$capacity </td>";
    print "<td>$price</td>";
    print "<td>$energy</td>";
    print "<td>$value</td>";
    print "<td><a href='$link'>$id</a></td>";
    print "</tr>";
} 
print "</table>";
?>
<?php
# Blank PHP
$sourcescraper = 'hobbyking';
scraperwiki::attach($sourcescraper);
$orderCol = 'Value (Wh/$)';
$data = scraperwiki::select("* from $sourcescraper.swdata where `Config(s)` = 6 order by `$orderCol` desc limit 50" );
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
$link = "http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=11902";

print "<table class='reference' border='1' cellpadding='0' cellspacing='0'>";
print '<tr><th>Cells</th><th>Capacity (mAh)</th><th>Price</th><th>Watt Hours</th><th>Wh / $</th><th>Product ID</th>';

foreach($data as $battery)
{
    $cells = $battery["Config(s)"];
    $capacity = $battery["Capacity(mAh)"];
    $price = $battery["price"]; 
    $energy= sprintf("%.2f", $battery["Energy (Wh)"]); 
    $value = sprintf("%.2f", $battery["Value (Wh/$)"]);
    $id = $battery["id"];
    $link = "http://www.hobbyking.com/hobbyking/store/uh_viewItem.asp?idProduct=$id";

    print "<tr>";
    print "<td>$cells</td>";
    print "<td>$capacity </td>";
    print "<td>$price</td>";
    print "<td>$energy</td>";
    print "<td>$value</td>";
    print "<td><a href='$link'>$id</a></td>";
    print "</tr>";
} 
print "</table>";
?>
