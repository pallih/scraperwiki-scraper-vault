<?php
# Blank PHP
#$sourcescraper = 'u_1';
scraperwiki::attach("u_1");

$data = scraperwiki::select(
    "* from u_1.swdata 
    where initial like '無料%無料'
    and distance like '%－%'
    and (year like '%南' or year like '%南東')
    order by Address desc limit 60"
);

$total = scraperwiki::select(
    "count(*) as count from u_1.swdata 
    where initial like '無料%無料'
    and distance like '%－%'
    and (year like '%南' or year like '%南東')"
);
$count = $total[0]["count"];

print "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'>
<html>
    <head>
    <style TYPE='text/css'>
/* 全体の枠。ヘッダが入る分だけ上部を空けておく */
    .container {
        position: relative;
        padding-top: 68px;
        border: 1px solid white;}
/* .container からヘッダのスペースを除いた部分。ここがスクロール対象 */
    .content {
        overflow: auto;
        overflow-x: hidden;}
    .scrollable {
        border-collapse: collapse;}
/* ヘッダ部分。位置を .container の左上端に移動 */
    .scrollable thead tr {
        position: absolute;
        top: 0;
        left: 0;}
/* このheightと .container の padding-top を合わせる */
    .scrollable thead th {
        height: 65px;
        border-color: blue;
        border-style: solid;
        text-align: center;
        border-width: 1px 1px 1px 1px;}
    .scrollable tbody td {
        height: 65px;
        border-color: black;
        border-style: solid;
        text-align: center;
        border-width: 1px 1px 1px 1px;}
/* ---------- 表ごとに異なる値はclassを分ける ---------- */
    .container1 {
        width: 1000px;}
    .content1 {
        width: 1000px;
        height: 500px;}
/* 各カラムにはwidth を設定する必要がある */
    .table1 th, .table1 td {
        padding: 0 3px 0 3px;
        width: 100px;}
    .table1 th.wide, .table1 td.wide {
        padding: 0 3px 0 3px;
        width: 300px;}
    .table1 th.narrow, .table1 td.narrow {
        padding: 0 3px 0 3px;
        width: 50px;}
    .table1 th.min, .table1 td.min{
        padding: 0 3px 0 3px;
        width: 10px;}
    .table1 th {
        background-color: #ccc;}
    </style>
    </head>
    <body>";
//<!-- 全体枠 -->
print "<pre>件数: " .$count . "件</pre>";
print "<div class='container container1'>";
//<!-- スクロール領域 -->
print "<div class='content content1'><table class='scrollable table1'>";
print "<thead><tr><th class='wide'>路線/最寄駅<br/>所在地</th><th class='narrow'>徒歩<br/>バス</th><th>間取り<br/>専有面積</th><th>築年数<br/>方位</th><th>種別<br/>所在階<br/>部屋番号</th><th>賃料<br/>管理費等</th><th class='narrow'>敷金<br/>礼金</th><th>物件写真・間取り図</th><th class='min'>c</th></thead><tbody>";
foreach($data as $d){
  print "<tr>";
  print "<td class='wide'>" . $d["link"] . "</td>";
  print "<td class='narrow'>" . preg_replace('/\s/','',preg_replace('/\n/','<br/>',$d["distance"])) . "</td>";
  print "<td>" . preg_replace('/\s/','',preg_replace('/\n/','<br/>',$d["layout"])) . "</td>";
  print "<td>" . preg_replace('/\s/','',preg_replace('/\n/','<br/>',$d["year"])) . "</td>";
  print "<td>" . preg_replace('/\s/','',preg_replace('/\n/','<br/>',$d["room"])) . "</td>";
  print "<td>" . preg_replace('/\s/','',preg_replace('/\n/','<br/>',$d["charge"])) . "</td>";
  print "<td class='narrow'>" . preg_replace('/\s/','',preg_replace('/\n/','<br/>',$d["initial"])) . "</td>";
  print "<td class='zoom'>" . $d["photo"] . "</td>";
  print "<td class='min'></td>";
  print "</tr>";
}
print "</tbody></table></div></div></body></html>";


?>
