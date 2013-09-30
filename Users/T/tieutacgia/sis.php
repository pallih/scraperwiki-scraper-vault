<?php $src = isset($_GET['src'])?$_GET['src']:'';?>
<?php  $cat = isset($_GET['cat'])?base64_decode($_GET['cat']):'';?>
<?php $page = (isset($_GET['page']) && $_GET['page']>0)?$_GET['page']:1;?>
 <?php 
    scraperwiki::attach("s-in-s-noidung-2", "src");

        if($src =="" && $cat !=""){ 
         $start = ($page-1)*50;
         $dt = scraperwiki::select("* from src.swdata where `type`='$cat' and `order`='1' order by CAST(`num` as integer) desc limit $start,50");
    } elseif($src !="" && $cat =="") {
     $dt = scraperwiki::select("* from src.swdata where `id`='$src'");
}
    
             ?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <?php if ($src=="" && $cat !="") { ?>
        <title> Sex In Sex Mobile - Trang <?php echo $page ?></title>
        <?php } elseif($cat == "" && $src != "") { ?>
         <title> <?php echo base64_decode($dt[0]['title'])?> Sex In Sex Mobile </title>
        <?php } else {?>
        <title>Sex In Sex Mobile </title>
<?php }?>
        <link rel="stylesheet" href="https://ajax.aspnetcdn.com/ajax/jquery.mobile/1.2.0/jquery.mobile-1.2.0.min.css" />
        
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js">
        </script>
        <script src="https://ajax.aspnetcdn.com/ajax/jquery.mobile/1.2.0/jquery.mobile-1.2.0.min.js">
        </script>
        
    </head>
    <body>
        <!-- Home -->
        <div data-role="page" id="page1">
            <div data-theme="a" data-role="header">
                <h1>
                   Sex In Sex Mobile
                </h1>
            <a href="/?" data-icon="home" data-iconpos="notext" data-direction="reverse">Home</a>
               
            </div>
            <div data-role="content">
           <div class="content-primary">    
           <?php if($cat =="" && $src =="") { ?>
            <ul data-role="listview">
            <li><a href="?cat=<?php echo base64_encode('nguoithe')?>">Người Thê</a></li>
            
            </ul>
            <?php } else {?>
            
               <?php if($src =="") {?>
            <ul data-role="listview">
        <li data-role="list-divider">Danh Sách Truyện</li>
            <?php foreach( $dt as $val ){?>
                <li><a href="?src=<?php echo $val['id'] ?>"><p style="white-space:normal;"><?php echo base64_decode( $val['title'] ) ?></p><span style="display:block;float:right;font-size:small">Xem : <strong><?php echo $val['num']?></strong></span></a></li>
                <?php } ?>
                
            </ul>
            <?php } 
            else {
        
         //  echo $src;
 //var_dump($dt);
echo "<h3>". base64_decode($dt[0]['title'])."</h3>";
foreach( $dt as $val ){
            echo "<p><a href='".urldecode(base64_decode($val['url']))."'> Link Gốc</a></p>";
            echo base64_decode($val['content']);
            }
            }
}
            ?>
            </div><!--/content-primary -->    
    
            </div>
            <?php 
    if($src=="" && $cat !=""){ ?>
           <div data-role="footer" class="ui-bar">
           
    <?php 
    
    if($page >1) { ?>
    <a href="?cat=<?php echo base64_encode($cat) ?>&page=<?php echo ($page - 1 )?>" data-role="button" data-icon="arrow-l" >Prev</a>
    <?php } else {?>
    <a href="?" data-role="button" data-icon="arrow-l" class="ui-disabled">Prev</a>
    <?php } ?>
    <a href="?cat=<?php echo base64_encode($cat) ?>&page=<?php echo ($page + 1)?>" data-role="button" data-icon="arrow-r">Next</a>

</div>
    <?php }?>
        </div>
        <script>
            //App custom javascript
        </script>
    </body>
</html><?php $src = isset($_GET['src'])?$_GET['src']:'';?>
<?php  $cat = isset($_GET['cat'])?base64_decode($_GET['cat']):'';?>
<?php $page = (isset($_GET['page']) && $_GET['page']>0)?$_GET['page']:1;?>
 <?php 
    scraperwiki::attach("s-in-s-noidung-2", "src");

        if($src =="" && $cat !=""){ 
         $start = ($page-1)*50;
         $dt = scraperwiki::select("* from src.swdata where `type`='$cat' and `order`='1' order by CAST(`num` as integer) desc limit $start,50");
    } elseif($src !="" && $cat =="") {
     $dt = scraperwiki::select("* from src.swdata where `id`='$src'");
}
    
             ?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <?php if ($src=="" && $cat !="") { ?>
        <title> Sex In Sex Mobile - Trang <?php echo $page ?></title>
        <?php } elseif($cat == "" && $src != "") { ?>
         <title> <?php echo base64_decode($dt[0]['title'])?> Sex In Sex Mobile </title>
        <?php } else {?>
        <title>Sex In Sex Mobile </title>
<?php }?>
        <link rel="stylesheet" href="https://ajax.aspnetcdn.com/ajax/jquery.mobile/1.2.0/jquery.mobile-1.2.0.min.css" />
        
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.2/jquery.min.js">
        </script>
        <script src="https://ajax.aspnetcdn.com/ajax/jquery.mobile/1.2.0/jquery.mobile-1.2.0.min.js">
        </script>
        
    </head>
    <body>
        <!-- Home -->
        <div data-role="page" id="page1">
            <div data-theme="a" data-role="header">
                <h1>
                   Sex In Sex Mobile
                </h1>
            <a href="/?" data-icon="home" data-iconpos="notext" data-direction="reverse">Home</a>
               
            </div>
            <div data-role="content">
           <div class="content-primary">    
           <?php if($cat =="" && $src =="") { ?>
            <ul data-role="listview">
            <li><a href="?cat=<?php echo base64_encode('nguoithe')?>">Người Thê</a></li>
            
            </ul>
            <?php } else {?>
            
               <?php if($src =="") {?>
            <ul data-role="listview">
        <li data-role="list-divider">Danh Sách Truyện</li>
            <?php foreach( $dt as $val ){?>
                <li><a href="?src=<?php echo $val['id'] ?>"><p style="white-space:normal;"><?php echo base64_decode( $val['title'] ) ?></p><span style="display:block;float:right;font-size:small">Xem : <strong><?php echo $val['num']?></strong></span></a></li>
                <?php } ?>
                
            </ul>
            <?php } 
            else {
        
         //  echo $src;
 //var_dump($dt);
echo "<h3>". base64_decode($dt[0]['title'])."</h3>";
foreach( $dt as $val ){
            echo "<p><a href='".urldecode(base64_decode($val['url']))."'> Link Gốc</a></p>";
            echo base64_decode($val['content']);
            }
            }
}
            ?>
            </div><!--/content-primary -->    
    
            </div>
            <?php 
    if($src=="" && $cat !=""){ ?>
           <div data-role="footer" class="ui-bar">
           
    <?php 
    
    if($page >1) { ?>
    <a href="?cat=<?php echo base64_encode($cat) ?>&page=<?php echo ($page - 1 )?>" data-role="button" data-icon="arrow-l" >Prev</a>
    <?php } else {?>
    <a href="?" data-role="button" data-icon="arrow-l" class="ui-disabled">Prev</a>
    <?php } ?>
    <a href="?cat=<?php echo base64_encode($cat) ?>&page=<?php echo ($page + 1)?>" data-role="button" data-icon="arrow-r">Next</a>

</div>
    <?php }?>
        </div>
        <script>
            //App custom javascript
        </script>
    </body>
</html>