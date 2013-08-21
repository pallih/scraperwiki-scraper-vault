<?php
scraperwiki::attach("script_extractor");
$data = scraperwiki::select("* from script_extractor.swdata order by url desc limit 10");
print '
<style type="text/css">
table{
    border-width: 1px;
    border-spacing: 2px;
    border-style: dashed;
    border-color: gray;
    border-collapse: separate;
}
table th {
    border-width: 1px;
    padding: 1px;
    border-style: dashed;
    border-color: gray;
    background-color: white;
    -moz-border-radius: ;
}
table td {
    border-width: 1px;
    padding: 1px;
    border-style: dashed;
    border-color: gray;
    background-color: #ddd;
    -moz-border-radius: ;
}
</style>
<h1>Script Extractor</h1>
<table>
<tr><th>URL</th><th>Script Source</th>';
foreach($data as $d){
  print "<tr>";
  print "<td>" . $d["url"] . "</td>";
  print "<td>" . $d["src"] . "</td>";
  print "</tr>";
}
print "</table>";
?>
