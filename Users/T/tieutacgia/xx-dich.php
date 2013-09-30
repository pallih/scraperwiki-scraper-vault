<?php
scraperwiki::attach("x-in-x-dich", "src");
$k = 1;
for($i=0;$i< 255;$i++){
    $j = $i *10;
    $src = scraperwiki::select("* from src.swdata limit $j,10");
foreach($src as $val)
{
    @scraperwiki::save_sqlite(array('id'),array('id'=> $k, 'title'=> $val['title'],'search' => base64_decode($val['title']),'url'=> $val['url'],'content'=>$val['content'],'order'=> $val['order'],'num'=>$val['num'],'reply'=>$val['reply'],'cat'=>'nguoithe'));
    $k++;
}
scraperwiki::save_var('last_id',$i);
}
?>

<?php
scraperwiki::attach("x-in-x-dich", "src");
$k = 1;
for($i=0;$i< 255;$i++){
    $j = $i *10;
    $src = scraperwiki::select("* from src.swdata limit $j,10");
foreach($src as $val)
{
    @scraperwiki::save_sqlite(array('id'),array('id'=> $k, 'title'=> $val['title'],'search' => base64_decode($val['title']),'url'=> $val['url'],'content'=>$val['content'],'order'=> $val['order'],'num'=>$val['num'],'reply'=>$val['reply'],'cat'=>'nguoithe'));
    $k++;
}
scraperwiki::save_var('last_id',$i);
}
?>

