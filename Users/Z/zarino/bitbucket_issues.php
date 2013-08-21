<?php

$default_username = 'zarino';
$organize_options = array('state','component','milestone','priority');
$sort_options = array('created_on'=>'date created','local_id'=>'ticket id');

$apiurl = 'https://api.bitbucket.org/1.0/repositories/ScraperWiki/scraperwiki/issues/';

if(isset($_GET['username'])){
    $args[] = 'responsible=' . urlencode($_GET['username']);
} else {
    $args[] = 'responsible=' . urlencode($default_username);
}

if(!empty($args)){ $apiurl .= '?' . join('&',$args); }

$issues_data = file_get_contents($apiurl);


?><!doctype html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta http-equiv="content-language" content="en" />
    <title>BitBucket Issues</title>
    <style type="text/css">
        body { padding: 10px; font-family: "Myriad Pro", Helvetica, Arial; }
    </style>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.6/jquery.min.js"></script>
    <script type="text/javascript">
        $(function() {
            $('#sort').change(function(){
                $('#sort_direction').remove();
                if($(this).val() == 'created_on'){
                    var asc = 'old&#8594;new';
                    var desc = 'new&#8594;old';
                } else if($(this).val() == 'local_id'){
                    var asc = '1&#8594;99';
                    var desc = '99&#8594;1';
                } else if($(this).val() == 'title'){
                    var asc = 'A&#8594;Z';
                    var desc = 'Z&#8594;A';
                }
                if(desc !== undefined){
                    $(this).after('<select name="sort_direction" id="sort_direction"><option value="desc">' + desc + '</option><option value="asc">' + asc + '</option></select>');
                }
            });
        });
    </script>
</head>
<body>
    <form action="." method="get">
        <p>
            <label for="username">Username:</label>
            <input type="text" class="text" id="username" name="username" value="<?php if(isset($_GET['username'])){ echo htmlspecialchars($_GET['username']); } else { echo $default_username; } ?>" />
        </p>
        <p>
            <label for="organize">Organize by:</label>
            <select name="organize" id="organize">
                <option<?php if(!isset($_GET['organize'])){ echo ' selected'; } ?>>(nothing)</option>
                <?php
                foreach($organize_options as $o){
                    echo '<option value="' . $o . '"';
                    if(isset($_GET['organize']) && $_GET['organize'] == $o){ echo ' selected'; }
                    echo '>' . $o . '</option>';
                }
                ?>
            </select>
        </p>
        <p>
            <label for="sort">Sort by:</label>
            <select name="sort" id="sort">
                <option<?php if(!isset($_GET['sort'])){ echo ' selected'; } ?>>(surprise me!)</option>
                <?php
                foreach($sort_options as $k => $v){
                    echo '<option value="' . $k . '"';
                    if(isset($_GET['sort']) && $_GET['sort'] == $k){ echo ' selected'; }
                    echo '>' . $v . '</option>';
                }
                ?>
            </select>
            <?php
            if(isset($_GET['sort_direction'])){
                if($_GET['sort'] == 'created_on'){
                    $asc = 'old&#8594;new';
                    $desc = 'new&#8594;old';
                } else if($_GET['sort'] == 'local_id'){
                    $asc = '1&#8594;99';
                    $desc = '99&#8594;1';
                } else if($_GET['sort'] == 'title'){
                    $asc = 'A&#8594;Z';
                    $desc = 'Z&#8594;A';
                }
                echo '<select name="sort_direction" id="sort_direction"><option value="desc">' . $desc . '</option><option value="asc">' . $asc . '</option></select>';
            } 
            ?>
        </p>
        <p><input type="submit" id="submit" /></p>
    </form>
    <div>
        <?php

if(isset($issues_data) && !empty($issues_data)){
    
    $issues_object = json_decode($issues_data,TRUE);
    
    echo '<pre>' . $apiurl . '</pre>';
    
    if(isset($_GET['organize'])){
        $lists_so_far = array();
//        for($i=0;$i<count($issues_object['issues']);$i++){
//            echo $issues_object['issues'][$i][$_GET['organize']];
//        }
    } else {
        //  No organization required. Just output one long list.
        $lists[] = $issues_object['issues'];
    }

    for($l=0;$l<count($lists);$l++){
        for($i=0;$i<count($lists[$l]);$i++){
            echo '<div><h2>' . $lists[$l][$i]['title'] . '</h2></div>'; 
        }
    }

}

        ?>
    </div>
</body>
</html>
