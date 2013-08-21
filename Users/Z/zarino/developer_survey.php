<?php

//if(!empty($_POST)){ echo '<pre>$_POST: '; print_r($_POST); echo '</pre>'; }

//if(!empty($_GET)){ echo '<pre>$_GET: '; print_r($_GET); echo '</pre>'; }

if(!empty($_GET)){

    echo '<div id="get"><b>$_GET</b>';
    foreach($_GET as $k=>$v){
        echo '<p><b>' . $k . ':</b> ' . $v . '</p>';
    }
    echo '</div>';
}

function asciify($string,$replacement=''){
    $r = strtolower($string);
    $r = preg_replace('/[^a-z0-9]/i',$replacement,$r);
    return $r;
}

if(!empty($_GET)){

    if(!empty($_GET['uuid'])){
        $save['uuid'] = $_GET['uuid'];
    }

    if(!empty($_GET['username'])){
        $save['username'] = $_GET['username'];
    } else {
        $save['username'] = 'anonymous';
    }

    if(!empty($_GET['use'])){
        $save['use'] = $_GET['use'];
    }

    if(!empty($_GET['disappointed'])){
        $save['disappointed'] = $_GET['disappointed'];
        if(!empty($_GET['disappointed_why'])){
            $save['disappointed_why'] = $_GET['disappointed_why'];
        }
    }

    if(!empty($_GET['recommend'])){
        $save['recommend'] = $_GET['recommend'];
        if(!empty($_GET['recommend_why'])){
            $save['recommend_why'] = $_GET['recommend_why'];
        }
    }

    if(!empty($_GET['describe'])){
        $save['describe'] = $_GET['describe'];
        if($_GET['describe'] == 'Other' && !empty($_GET['describe_other_input'])){
            $save['describe_other'] = $_GET['describe_other_input'];
        }
    }

    echo '<div id="debug"><b>$save</b>';
    foreach($save as $k=>$v){
        echo '<p><b>' . $k . ':</b> ' . $v . '</p>';
    }
    echo '</div>';

}


?><!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <title>ScraperWiki Developer Survey</title>
        <style type="text/css">
        /* RESETS */
        html, body, div, span, applet, object, iframe, h1, h2, h3, h4, h5, h6, p, blockquote, pre, a, abbr, acronym, address, big, cite, code, del, dfn, em, img, ins, kbd, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, dl, dt, dd, ol, ul, li, fieldset, form, label, legend, table, caption, tbody, tfoot, thead, tr, th, td, article, aside, canvas, details, embed, figure, figcaption, footer, header, hgroup, menu, nav, output, ruby, section, summary, time, mark, audio, video { margin: 0; padding: 0; border: 0; font-size: 100%; font: inherit; vertical-align: baseline; }
        article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section { display: block; }
        body { font-family: Helvetica, Arial, sans-serif; font-size: 14px; line-height: 18px; }
        ol, ul { list-style: none; }
        blockquote, q { quotes: none; }
        blockquote:before, blockquote:after, q:before, q:after { content: ''; content: none; }
        table { border-collapse: collapse; border-spacing: 0; }
        td { vertical-align: top; }
        label { -webkit-user-select: none; -khtml-user-select: none; -moz-user-select: none; -ms-user-select: none; user-select: none; }

        .extra {
            display: none;
        }

        body {
            width: 400px;
            margin: 0 auto;
        }
        
        h1 {
            text-align: center;
            font-weight: bold;
            font-size: 21px;
            line-height: 21px;
            margin: 20px 0;
        }
        
        fieldset div {
            margin-bottom: 30px;
            border-top: 1px solid #ccc;
        }
        
        fieldset div>label {
            display: block;
            font-weight: bold;
            margin-top: 10px;
            line-height: 20px;
        }
        
        fieldset p {
            padding: 5px 0;
            margin: 5px 0;
            position: relative;
        }
        
        fieldset p:hover {
            background-color: #f6f6f6;
        }
        
        span.extra {
            position: absolute;
            margin-left: 10px;
            padding: 0 5px;
            top: 50%;
            margin-top: -15px;
            line-height: 30px;
        }
        
        p.extra label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        
        p.extra textarea {
            width: 386px;
            height: 50px;
            padding: 5px;
            font-size: 14px;
            line-height: 14px;
        }
        
        p.recommend {
            display: table;
            width: 100%;
            text-align: center;
        }
        
        p.recommend:hover,
        p.extra:hover {
            background: transparent;
        }

        .td {
            display: table-cell;
            padding: 10px;
        }

        .td label {
            display: block;
        }
        
        .td:hover {
            background-color: #eee;
        }
        
        input.radio, input.checkbox {
            margin: 0 5px;
        }

        input.radio {
            vertical-align: 1px;
        }
        
        .td input.radio {
            margin: 0;
            vertical-align: 0;
        }
        
        label b {
            float: right;
            color: #ccc;
            margin: 0 0 5px 10px;
        }

        div.last {
            text-align: center;
        }

        #submit {
            font-size: 20px;
            margin: 20px 0 100px 0;
        }

        #get, #debug {
            width: 380px;
            background: #eee;
            margin: 20px 0;
            padding: 10px;
        }
        
        #get b, #debug b {
            font-weight: bold;
            margin-right: 5px;
        }

        </style>
        <link type="text/css" rel="stylesheet" href="http://example.com"/>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7/jquery.min.js"></script>
        <script type="text/javascript">
        function getip(ip){
            $(function(){ $('<input type="hidden">').attr('id', 'ip').attr('name', 'ip').val(ip.ip).appendTo('#aboutYou'); });
        }
        $(function(){
            $('#scraperwikipane').remove();
            $('<input type="hidden">').attr('id', 'screen_height').attr('name', 'screen_height').val(screen.height).appendTo('#aboutYou');
            $('<input type="hidden">').attr('id', 'screen_width').attr('name', 'screen_width').val(screen.width).appendTo('#aboutYou');
            $('<input type="hidden">').attr('id', 'window_height').attr('name', 'window_height').val($(window).height()).appendTo('#aboutYou');
            $('<input type="hidden">').attr('id', 'window_width').attr('name', 'window_width').val($(window).width()).appendTo('#aboutYou');
            $('<input type="hidden">').attr('id', 'ua').attr('name', 'ua').val(navigator.userAgent).appendTo('#aboutYou');

            $('span.extra').not('.registered span').each(function(){
                var $extra = $(this);
                $extra.prevAll('input').bind('change', function(){
                    $extra.toggle();
                    if($extra.is(':visible')){
                        $('input:text', $extra).focus();
                    }
                });
            });
            $('#registered_yes, #registered_no').bind('change', function(){
                if($('#registered_yes').is(':checked')){
                    $('.registered_yes .extra').show();
                } else {
                    $('.registered_yes .extra').hide();
                }
            });
            $('.recommend input, .disappointed input').bind('change', function(){
                $(this).parents('div').children('.extra').show();
            });

            /*$('textarea, input:text').bind('blur', function(){
                console.log($(this).parents('div'));
            });
            $('input:radio, input:checkbox').bind('change', function(){
                console.log($(this).parents('div'));
            });*/

            $('.td').bind('click', function(e){
                $('input', $(this)).trigger('click');
                e.stopPropagation();
            }).children().bind('click', function(e){
                e.stopPropagation();
            });

            $('p').bind('click', function(e){
                $(this).find('input').eq(0).trigger('click');
            }).children().bind('click', function(e){
                e.stopPropagation();
            });
        });
        </script>
        <script type="text/javascript" src="http://jsonip.com/getip"></script>
    </head>
    <body>
        <form id="form" method="get">
            <fieldset id="aboutScraperwiki">
                <h1>About ScraperWiki</h1>
                
            <?php 
                $n = 1;
                if(isset($_GET['username'])){ 
                    echo '<input type="hidden" id="username" name="username" value="' . $_GET['username'] . '"/>'; 
                } else {
                    echo '<div class="registered">
                    <label for="registered"><b>' . $n . '</b> Do you have a ScraperWiki account?</label>
                    <p class="registered_yes">
                        <input type="radio" class="radio" name="registered" id="registered_yes" value="yes"/> <label for="registered_yes">Yes</label>
                        <span class="extra"><label for="username">&hellip; And my username is</label> <input type="text" name="username" id="username" /></span>
                    </p>
                    <p class="registered_no">
                        <input type="radio" class="radio" name="registered" id="registered_no" value="no"/> <label for="registered_no">No</label>
                    </p>
                </div>';
                    $n++;
                }
            ?>

                <div class="use">
                    <label><b><?php echo $n; $n++; ?></b> Do you mostly use ScraperWiki&nbsp;for&hellip;</label>
                    <?php
                        $options = array('Work', 'Play', 'Learning');
                        // shuffle($options);
                        for($i=0;$i<sizeof($options);$i++){
                            echo '
                    <p class="use_' . asciify($options[$i]) . '">
                        <input type="radio" class="radio" name="use" id="use_' . asciify($options[$i]) . '" value="' . asciify($options[$i]) . '" /> <label for="use_' . asciify($options[$i]) . '">' . $options[$i] . '</label>
                    </p>';
                        }
                    ?>
                </div>

                <div class="disappointed">
                    <label><b><?php echo $n; $n++; ?></b> If ScraperWiki disappeared tomorrow, would&nbsp;you&nbsp;be&hellip;</label>
                    <?php
                        $options = array('verydissappointed'=>'Very disappointed', 'dissappointed'=>'Somewhat disappointed', 'notdissappointed'=>'Not disappointed', 'na'=>'N/A &ndash; I don&rsquo;t use ScraperWiki anymore');
                        foreach($options as $k=>$v){
                            echo '
                    <p class="disappointed_' . $k . '">
                        <input type="radio" class="radio" name="disappointed" id="disappointed_' . $k . '" value="' . $k . '" /> 
                        <label for="disappointed_' . $k . '">' . $v . '</label>
                    </p>';
                        }
                    ?>
                    <p class="disappointed_why extra">
                        <label for="disappointed_why">Why&rsquo;s that?</label>
                        <textarea id="disappointed_why" name="disappointed_why"></textarea>
                    </p>
                </div>

                <div class="recommend">
                    <label><b><?php echo $n; $n++; ?></b> How likely is it that you&rsquo;d recommend ScraperWiki to a&nbsp;friend&nbsp;or&nbsp;colleague?</label>
                    <p class="recommend">
                        <?php
                            for($i=0;$i<11;$i++){
                                echo '
                        <span class="td">
                            <label for="recommend_' . $i . '">' . $i . '</label>
                            <input type="radio" class="radio" name="recommend" id="recommend_' . $i . '" value="' . $i . '" /> 
                        </span>';
                            }
                        ?>
                    </p>
                    <p class="recommend_why extra">
                        <label for="recommend_why">Why&rsquo;s that?</label>
                        <textarea id="recommend_why" name="recommend_why"></textarea>
                    </p>
                </div>
                
            </fieldset>

            <fieldset id="aboutYou">
                <h1>About You</h1>
                
                <div class="describe">
                    <label><b><?php echo $n; $n++; ?></b> How would you describe&nbsp;yourself?</label>
                    <?php
                        $options = array('Data wrangler', 'Programmer', 'Software Engineer', 'Scripter', 'Coder', 'Developer', 'Data scientist', 'Journalist', 'Activist');
                        shuffle($options);
                        for($i=0;$i<sizeof($options);$i++){
                            echo '
                    <p class="describe_' . asciify($options[$i]) . '">
                        <input type="checkbox" class="checkbox" id="describe_' . asciify($options[$i]) . '" name="describe_' . asciify($options[$i]) . '" value="' . $options[$i] . '" />
                        <label for="describe_' . asciify($options[$i]) . '">' . $options[$i] . '</label>
                    </p>';
                        }
                    ?>
                    <p class="describe_other">
                        <input type="checkbox" class="checkbox" id="describe_other" name="describe_other" value="Other" />
                        <label for="describe_other">Other&hellip;</label>
                        <span class="extra"><input type="text" id="describe_other_input" name="describe_other_input" /></span>
                    </p>
                </div>
                
                <div class="languages">
                    <label><b><?php echo $n; $n++; ?></b> Which of these languages have you used in the&nbsp;last&nbsp;6&nbsp;months?</label>
                    <?php
                        $options = array('Erlang', 'Haskell', 'Javascript', 'Perl', 'PHP', 'Python', 'R', 'Ruby', 'Shell scripting');
                        shuffle($options);
                        for($i=0;$i<sizeof($options);$i++){
                            echo '
                    <p class="languages_' . asciify($options[$i]) . '">
                        <input type="checkbox" class="checkbox" id="languages_' . asciify($options[$i]) . '" name="languages_' . asciify($options[$i]) . '" value="' . $options[$i] . '" />
                        <label for="languages_' . asciify($options[$i]) . '">' . $options[$i] . '</label>
                    </p>';
                        }
                    ?>
                </div>
                
                <div class="services">
                    <label><b><?php echo $n; $n++; ?></b> Which of these services do you&nbsp;use?</label>
                    <p class="services_github">
                        <input type="checkbox" class="checkbox" id="services_github" name="services_github" value="Github" />
                        <label for="services_github">Github</label>
                        <span class="extra">&hellip;
                            <input type="checkbox" class="checkbox" id="services_github_paid" name="services_github_paid" value="github_paid" />
                            <label for="services_github_paid">And I pay for private repo&rsquo;s</label> 
                        </span>
                    </p>
                    <p class="services_bitbucket">
                        <input type="checkbox" class="checkbox" id="services_bitbucket" name="services_bitbucket" value="BitBucket" />
                        <label for="services_bitbucket">BitBucket</label>
                        <span class="extra">&hellip;
                            <input type="checkbox" class="checkbox" id="services_bitbucket_paid" name="services_bitbucket_paid" value="bitbucket_paid" />
                            <label for="services_bitbucket_paid">And I pay for it</label> 
                        </span>
                    </p>
                    <p class="services_dropbox">
                        <input type="checkbox" class="checkbox" id="services_dropbox" name="services_dropbox" value="Dropbox" />
                        <label for="services_dropbox">Dropbox</label>
                        <span class="extra">&hellip;
                            <input type="checkbox" class="checkbox" id="services_dropbox_paid" name="services_dropbox_paid" value="dropbox_paid" />
                            <label for="services_dropbox_paid">And I pay for extra space</label> 
                        </span>
                    </p>
                    <?php
                        $options = array('Heroku', 'Amazon S3', 'Amazon EC2', 'Google App Engine', 'Basecamp or Highrise');
                        shuffle($options);
                        for($i=0;$i<sizeof($options);$i++){
                            echo '
                    <p class="services_' . asciify($options[$i]) . '">
                        <input type="checkbox" class="checkbox" id="services_' . asciify($options[$i]) . '" name="services_' . asciify($options[$i]) . '" value="' . $options[$i] . '" />
                        <label for="services_' . asciify($options[$i]) . '">' . $options[$i] . '</label>
                    </p>';
                        }
                    ?>
                </div>
                
                <div class="versioncontrol">
                    <label><b><?php echo $n; $n++; ?></b> Do you use..?</label>
                    <?php
                        $options = array('git'=>'Git', 'hg'=>'Mercurial (Hg)', 'svn'=>'Subversion (SVN)');
                        foreach($options as $k=>$v){
                            echo '
                    <p class="versioncontrol_' . $k . '">
                        <input type="checkbox" class="checkbox" name="versioncontrol_' . $k . '" id="versioncontrol_' . $k . '" value="' . $k . '" /> 
                        <label for="versioncontrol_' . $k . '">' . $v . '</label>
                    </p>';
                        }
                    ?>
                    <p class="versioncontrol_other">
                        <input type="checkbox" class="checkbox" name="versioncontrol_other" id="versioncontrol_other" value="other" /> 
                        <label for="versioncontrol_other">Other VCS&hellip;</label>
                        <span class="extra"><input type="text" id="versioncontrol_other_input" name="versioncontrol_other_input" /></span>
                    </p>
                </div>
                
                <div class="blog">
                    <label><b><?php echo $n; $n++; ?></b> Have you seen the ScraperWiki&nbsp;blog?</label>
                    <p class="blog_yes">
                        <input type="radio" class="radio" name="blog" id="blog_yes" value="yes" />
                        <label for="blog_yes">Yes</label>
                    </p>
                    <p class="blog_no">
                        <input type="radio" class="radio" name="blog" id="blog_no" value="no" />
                        <label for="blog_no">No</label>
                    </p>
                    <p class="blog_dontknow">
                        <input type="radio" class="radio" name="blog" id="blog_dontknow" />
                        <label for="blog_dontknow">Don&rsquo;t know</label>
                    </p>
                </div>
                
                <div class="twitter">
                    <label><b><?php echo $n; $n++; ?></b> Do you follow @scraperwiki on&nbsp;Twitter?</label>
                    <p class="twitter_yes">
                        <input type="radio" class="radio" name="twitter" id="twitter_yes" value="yes" />
                        <label for="twitter_yes">Yes</label>
                    </p>
                    <p class="twitter_no">
                        <input type="radio" class="radio" name="twitter" id="twitter_no" value="no" />
                        <label for="twitter_no">No</label>
                    </p>
                    <p class="twitter_dontknow">
                        <input type="radio" class="radio" name="twitter" id="twitter_dontknow" />
                        <label for="twitter_dontknow">Don&rsquo;t know</label>
                    </p>
                </div>
                
                <input type="hidden" name="uuid" id="uuid" value="<?php echo str_replace('.', '', uniqid('', true)); ?>" />
            </fieldset>
            <fieldset>
                <div class="last">
                    <input type="submit" name="submit" id="submit" value="Save your answers &nbsp;&#10004;" />
                </div>
            </fieldset>
        </form>
    </body>
</html>





