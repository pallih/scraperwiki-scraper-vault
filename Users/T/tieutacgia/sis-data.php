<?php
scraperwiki::attach("s-in-s-noidung-2", "src");
 $count = scraperwiki::select("count(*) as total from src.swdata where type='nguoithe'");
$total= ceil($count[0]['total']/10);
//exit();
$k = 1;
for($i=0;$i< $total;$i++){
    $j = $i *10;
    $src = scraperwiki::select("* from src.swdata where type='nguoithe' limit $j,10");
foreach($src as $val)
{
    scraperwiki::save_sqlite(array('id'),array('id'=> $val['id'], 'title'=> $val['title'],'search' => $val['title'],'url'=> $val['url'],'content'=>$val['content'],'order'=> $val['order'],'num'=>$val['num'],'reply'=>$val['reply'],'cat'=>'nguoithe'));
    $k++;
}
scraperwiki::save_var('last_id',$i);
}
?>

