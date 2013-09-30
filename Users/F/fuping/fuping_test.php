<?php

require 'scraperwiki/simple_html_dom.php';
createTable();   
$html = scraperWiki::scrape("http://civiccommons.org/apps");
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='block-inner clearfix']") as $data){
    $titles=$data->find("h2");
    if(count($titles)==1){
        $title=$titles[0]->plaintext;
        if(strcasecmp($title,"Browse by Software Type")==0||strcasecmp($title,"BROWSE APPS BY FUNCTION")==0||strcasecmp($title,"BROWSE BY SOFTWARE LICENSE")==0){
            foreach($data->find("span[@class='field-content'] a") as $apps){
                $name=$apps->plaintext;
                $names=explode(' ',$name);
                $realname="";
                for($i=0;$i<count($names);$i++){
                    if(strlen($realname)>0){
                            $realname=$realname." ";
                    }
                    if(strcasecmp($names[$i],"&amp;")!=0){
                        $realname=$realname.$names[$i];
                    }else{
                        $realname=$realname."&";
                    }
                }
                print $realname.": \n";
                $url="http://civiccommons.org".$apps->href;
                getApps($title,$realname,$url);
            }
        }
    }
   
}
print "done";
/*$result=scraperwiki::select('* from tagtable limit 1');
print_r ($result);*/


function getApps($title,$tag,$url){
   $html = scraperWiki::scrape($url);
   $dom = new simple_html_dom();
   $dom->load($html); 
   foreach($dom->find("span[@class='field-content'] a") as $data){
   
    $name=$data->plaintext;
    $names=explode(' ',$name);
    $realname="";
    for($i=0;$i<count($names);$i++){
        if(strlen($realname)>0){
            $realname=$realname." ";
        }
        if(strcasecmp($names[$i],"&amp;")!=0){
            $realname=$realname.$names[$i];
        }else{
            $realname=$realname."&";
        }
    }    
    $url="http://civiccommons.org".$data->href;
    $exist=inserttag($title,$tag,$realname,$url);
    if($exist==0){
        storecontent($realname,$url);
    }
    //print "--------".$realname.": ".$url."\n";
  }
}

function inserttag($title,$tag,$appname,$url){
    $sql='* from tagtable where appname=\''.$appname.'\'';
    $data=scraperwiki::select($sql);
    if(count($data)>0){
        if(strcasecmp($title,"Browse by Software Type")==0){
            $typestring=$data[0]['type'];
            if($typestring==null||strlen($typestring)==0){
                $typestring=$tag;
            }else{
                $typestring=$typestring."|".$tag;
            }
            $sql="update tagtable set type='$typestring'where appname='$appname'";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }else if(strcasecmp($title,"BROWSE APPS BY FUNCTION")==0){
            $functionstring=$data[0]['function'];
            if($functionstring==null||strlen($functionstring)==0){
                $functionstring=$tag;
            }else{
                $functionstring=$functionstring."|".$tag;
            }
            $sql="update tagtable set function='$functionstring'where appname='$appname'";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }else if(strcasecmp($title,"BROWSE BY SOFTWARE LICENSE")==0){
            $licensestring=$data[0]['license'];
            if($licensestring==null||strlen($licensestring)==0){
                $licensestring=$tag;
            }else{
                $licensestring=$licensestring."|".$tag;
            }
            $sql="update tagtable set license='$licensestring'where appname='$appname'";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }
        return 1;
    }else{
         if(strcasecmp($title,"Browse by Software Type")==0){
            $sql="insert into tagtable values('$appname','$url','$tag','','')";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }else if(strcasecmp($title,"BROWSE APPS BY FUNCTION")==0){
            $sql="insert into tagtable values('$appname','$url','','$tag','')";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }else if(strcasecmp($title,"BROWSE BY SOFTWARE LICENSE")==0){
            $sql="insert into tagtable values('$appname','$url','','','$tag')";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }
        return 0;
    }
}

function storeContent($appname,$url){
    $html = scraperWiki::scrape($url);
    $array=array(
        "appname"=>$appname,
        "html"=>$html
    );
    scraperwiki::save_sqlite(array("appname"), $array, $table_name="htmltable", $verbose=2);
}

function createTable(){
    scraperwiki::sqliteexecute('create table tagtable(appname text primary key,url text, type text, function type, license type)');
    scraperwiki::sqliteexecute('create table htmltable(appname text primary key,html text)');
    scraperwiki::sqlitecommit();
}
?>
<?php

require 'scraperwiki/simple_html_dom.php';
createTable();   
$html = scraperWiki::scrape("http://civiccommons.org/apps");
$dom = new simple_html_dom();
$dom->load($html);
foreach($dom->find("div[@class='block-inner clearfix']") as $data){
    $titles=$data->find("h2");
    if(count($titles)==1){
        $title=$titles[0]->plaintext;
        if(strcasecmp($title,"Browse by Software Type")==0||strcasecmp($title,"BROWSE APPS BY FUNCTION")==0||strcasecmp($title,"BROWSE BY SOFTWARE LICENSE")==0){
            foreach($data->find("span[@class='field-content'] a") as $apps){
                $name=$apps->plaintext;
                $names=explode(' ',$name);
                $realname="";
                for($i=0;$i<count($names);$i++){
                    if(strlen($realname)>0){
                            $realname=$realname." ";
                    }
                    if(strcasecmp($names[$i],"&amp;")!=0){
                        $realname=$realname.$names[$i];
                    }else{
                        $realname=$realname."&";
                    }
                }
                print $realname.": \n";
                $url="http://civiccommons.org".$apps->href;
                getApps($title,$realname,$url);
            }
        }
    }
   
}
print "done";
/*$result=scraperwiki::select('* from tagtable limit 1');
print_r ($result);*/


function getApps($title,$tag,$url){
   $html = scraperWiki::scrape($url);
   $dom = new simple_html_dom();
   $dom->load($html); 
   foreach($dom->find("span[@class='field-content'] a") as $data){
   
    $name=$data->plaintext;
    $names=explode(' ',$name);
    $realname="";
    for($i=0;$i<count($names);$i++){
        if(strlen($realname)>0){
            $realname=$realname." ";
        }
        if(strcasecmp($names[$i],"&amp;")!=0){
            $realname=$realname.$names[$i];
        }else{
            $realname=$realname."&";
        }
    }    
    $url="http://civiccommons.org".$data->href;
    $exist=inserttag($title,$tag,$realname,$url);
    if($exist==0){
        storecontent($realname,$url);
    }
    //print "--------".$realname.": ".$url."\n";
  }
}

function inserttag($title,$tag,$appname,$url){
    $sql='* from tagtable where appname=\''.$appname.'\'';
    $data=scraperwiki::select($sql);
    if(count($data)>0){
        if(strcasecmp($title,"Browse by Software Type")==0){
            $typestring=$data[0]['type'];
            if($typestring==null||strlen($typestring)==0){
                $typestring=$tag;
            }else{
                $typestring=$typestring."|".$tag;
            }
            $sql="update tagtable set type='$typestring'where appname='$appname'";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }else if(strcasecmp($title,"BROWSE APPS BY FUNCTION")==0){
            $functionstring=$data[0]['function'];
            if($functionstring==null||strlen($functionstring)==0){
                $functionstring=$tag;
            }else{
                $functionstring=$functionstring."|".$tag;
            }
            $sql="update tagtable set function='$functionstring'where appname='$appname'";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }else if(strcasecmp($title,"BROWSE BY SOFTWARE LICENSE")==0){
            $licensestring=$data[0]['license'];
            if($licensestring==null||strlen($licensestring)==0){
                $licensestring=$tag;
            }else{
                $licensestring=$licensestring."|".$tag;
            }
            $sql="update tagtable set license='$licensestring'where appname='$appname'";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }
        return 1;
    }else{
         if(strcasecmp($title,"Browse by Software Type")==0){
            $sql="insert into tagtable values('$appname','$url','$tag','','')";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }else if(strcasecmp($title,"BROWSE APPS BY FUNCTION")==0){
            $sql="insert into tagtable values('$appname','$url','','$tag','')";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }else if(strcasecmp($title,"BROWSE BY SOFTWARE LICENSE")==0){
            $sql="insert into tagtable values('$appname','$url','','','$tag')";
            scraperwiki::sqliteexecute($sql);
            scraperwiki::sqlitecommit();
        }
        return 0;
    }
}

function storeContent($appname,$url){
    $html = scraperWiki::scrape($url);
    $array=array(
        "appname"=>$appname,
        "html"=>$html
    );
    scraperwiki::save_sqlite(array("appname"), $array, $table_name="htmltable", $verbose=2);
}

function createTable(){
    scraperwiki::sqliteexecute('create table tagtable(appname text primary key,url text, type text, function type, license type)');
    scraperwiki::sqliteexecute('create table htmltable(appname text primary key,html text)');
    scraperwiki::sqlitecommit();
}
?>
