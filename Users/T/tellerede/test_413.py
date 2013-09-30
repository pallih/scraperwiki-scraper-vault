# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# -*- coding: utf-8 -*-

# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree, lxml.html, re, scraperwiki
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup

#print help(lxml.html.parse)


# create an example case
samplehtml = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml"  dir="ltr" lang="hun" id="vbulletin_html"> <head>  <script type="text/javascript" src="https://www.kenderforum.org/mobiquo/tapatalkdetect.js"></script>  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> <meta id="e_vb_meta_bburl" name="vb_meta_bburl" content="https://www.kenderforum.org" /> <meta name="generator" content="vBulletin 4.1.12" /> <link rel="Shortcut Icon" href="favicon.ico" type="image/x-icon" /> <meta name="keywords" content="" /> <meta name="description" content="" /> <script type="text/javascript"> <!--
    if (typeof YAHOO === 'undefined') // Load ALL YUI Local
    {
        document.write('<script type="text/javascript" src="clientscript/yui/yuiloader-dom-event/yuiloader-dom-event.js?v=4112"><\/script>');
        document.write('<script type="text/javascript" src="clientscript/yui/connection/connection-min.js?v=4112"><\/script>');
        var yuipath = 'clientscript/yui';
        var yuicombopath = '';
        var remoteyui = false;
    }
    else    // Load Rest of YUI remotely (where possible)
    {
        var yuipath = 'clientscript/yui';
        var yuicombopath = '';
        var remoteyui = true;
        if (!yuicombopath)
        {
            document.write('<script type="text/javascript" src="clientscript/yui/connection/connection-min.js"><\/script>');
        }
    }
    var SESSIONURL = "";
    var SECURITYTOKEN = "1370472078-81f10ad2088edd0fb3d800b27eefe81d962b42cc";
    var IMGDIR_MISC = "images/misc";
    var IMGDIR_BUTTON = "images/buttons";
    var vb_disable_ajax = parseInt("0", 10);
    var SIMPLEVERSION = "4112";
    var BBURL = "https://www.kenderforum.org";
    var LOGGEDIN = 5893 > 0 ? true : false;
    var THIS_SCRIPT = "mgc_cb_evo";
    var RELPATH = "mgc_cb_evo.php?do=view_archives&amp;page=1";
    var PATHS = {
        forum : "",
        cms   : "",
        blog  : ""
    };
    var AJAXBASEURL = "https://www.kenderforum.org/";
// --> </script> <script type="text/javascript" src="https://www.kenderforum.org/clientscript/vbulletin-core.js?v=4112"></script> <link rel="alternate" type="application/rss+xml" title="Kender Fórum RSS Feed" href="https://www.kenderforum.org/external.php?type=RSS2" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/main-rollup.css?d=1360781686" /> <!--[if lt IE 8]> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/popupmenu-ie.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/vbulletin-ie.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/vbulletin-chrome-ie.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/vbulletin-formcontrols-ie.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/editor-ie.css?d=1360781686" /> <![endif]--
> <script src="https://kenderforum.org/clientscript/jquery/jquery-1.6.4.min.js"></script> <script src="https://kenderforum.org/clientscript/sticky_panel.js"></script>  <script type="text/javascript">
        $().ready(function () {
            var stickyPanelOptions = {
                topPadding: 10,
                afterDetachCSSClass: "off_stick1",
                savePanelSpace: true
            };
            $("#column_left_ad1").stickyPanel(stickyPanelOptions);
            $("#column_right_ad2").stickyPanel(stickyPanelOptions);


        });
    </script>  <link rel="stylesheet" href="mgc_cb_evo/clientscript/dojo/dijit/themes/claro/claro.css" type="text/css"><link rel="stylesheet" href="css.php?styleid=6&amp;langid=2&amp;d=1360781686&amp;sheet=mgc_cb_evo.css" type="text/css"> <title>Kender Forum Chat : Archives</title> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/additional.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="css.php?styleid=6&amp;langid=2&amp;d=1360781686&amp;sheet=ss_twincolumns_css.css" /> </head> <body> <div class="above_body">  <div id="header" class="floatcontainer doc_header"> <div><a name="top" href="https://www.kenderforum.org/" class="logo-image"><img src="images/misc/vbulletin4_logo.png" alt="Kender Fórum - Powered by vBulletin" /></a></div> <div style="float: left; padding-left: 15%;"> <a class="navtab" href="private.php"><img  style="vertical-align: middle;" src="kendimg/pm.png" alt="Új privát üzeneted érkezett" />&nbsp; &nbsp; <font size="2" style="text-alig:right;
" >ÚJ ÜZENET</font></a> </div> <div id="toplinks" class="toplinks"> <ul class="isuser"> <li><a rel="nofollow" href="login.php?do=logout&amp;logouthash=1370472078-81f10ad2088edd0fb3d800b27eefe81d962b42cc" onclick="return log_out('Biztos hogy ki akarsz lépni?')">Kilép</a></li> <li><a href="usercp.php">Kezelőpult</a></li> <li><a href="tagok/5893/ppp">Profil</a></li> <li class="popupmenu notifications" id="notifications"> <a class="popupctrl" href="usercp.php">Értesítők: <span class="notifications-number"><strong>10</strong></span></a> <ul class="popupbody popuphover"> <li><a href="private.php"><span>10</span> Olvasatlan privát üzenetek</a></li> </ul> </li> <li class="welcomelink">Üdvözlünk, <a href="tagok/5893/ppp">ppp</a>.</li> </ul> </div> <div class="ad_global_header"> </div> <hr /> </div> <div id="navbar" class="navbar"> <ul id="navtabs" class="navtabs floatcontainer notify"> <li class="selected"><a class="navtab" href="https://www.kenderforum.org/">Fórum</a> <ul class="floatcontainer"> <li><a href="https://
www.kenderforum.org/">Fórum</a></li> <li><a rel="nofollow" href="search.php?do=getnew&amp;contenttype=vBForum_Post">Új hozzászólások</a></li> <li><a href="private.php" rel="nofollow">Privát üzenetek</a></li> <li><a rel="help" href="faq.php" accesskey="5">Súgó</a></li> <li><a href="calendar.php">Naptár</a></li> <li class="popupmenu"> <a href="javascript://" class="popupctrl" accesskey="6">Közösség</a> <ul class="popupbody popuphover"> <li><a href="csoportok/csoport.html">Közösségi csoportok</a></li> <li><a href="https://www.kenderforum.org/tagok/albumok/">Képek &amp; Albumok </a></li> <li><a rel="nofollow" href="profile.php?do=buddylist">Kapcsolatok &amp; Barátok</a></li> <li><a href="tagok/lista/">Taglista</a></li> <li><a rel="nofollow" href="thanks.php?do=hottest">Hottest Threads / Posts</a></li> <li><a rel="nofollow" href="thanks.php?do=statistics">Thanks / Like Statistics</a></li> </ul> </li> <li class="popupmenu"> <a href="javascript://" class="popupctrl">Fórum eszközök</a> <ul class="popupbody 
popuphover"> <li> <a rel="nofollow" href="forumdisplay.php?do=markread&amp;markreadhash=1370472078-81f10ad2088edd0fb3d800b27eefe81d962b42cc">Fórumokat olvasottnak jelöli</a> </li> <li> <a rel="nofollow" href="profile.php?do=editoptions">Beállítások módosítása</a> </li> <li> <a rel="nofollow" href="profile.php?do=editprofile">Profil módosítása</a> </li> </ul> </li> <li class="popupmenu"> <a href="javascript://" class="popupctrl" accesskey="3">Expressz</a> <ul class="popupbody popuphover"> <li><a href="search.php?do=getdaily&amp;contenttype=vBForum_Post">Mai hozzászólások</a></li> <li><a href="subscription.php" rel="nofollow">Követett témák</a></li> <li><a href="javascript://" onclick="window.open(getBaseUrl() + 'misc.php?do=buddylist&amp;focus=1','buddylist','statusbar=no,menubar=no,toolbar=no,scrollbars=yes,resizable=yes,width=250,height=300'); return false;">Kapcsolat popup megnyitása</a></li> <li><a href="showgroups.php" rel="nofollow">
                                
                                    Fórum vezetők listázása
                                
                            </a></li> <li><a href="online.php">Jelenlévő aktív tagok</a></li> <li><a rel="nofollow" href="misc.php?do=donlist">View Donations</a></li> </ul> </li> <li><a rel="nofollow" href="misc.php?do=donate"><span style="color:[b][color=#008000]Donate[/color][/b];">Donate<span></a></li> </ul> </li> <li ><a class='navtab' href='https://www.kenderforum.org/5/szabalyzat-1954.html#post49757' target='_blank'> Szabályzat</a></li><li ><a class='navtab' href='https://www.kenderforum.org/5/biztonsag-1983.html' target='_blank'> Biztonság</a></li><li class="popupmenu"><a href="javascript://" class="popupctrl navtab" style="background:transparent url(images/misc/arrow.png) no-repeat right center; padding-right: 15px">Eszköztár</a><ul class="popupbody popuphover"><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/5/kw-ar-szamolo-77.html" target="_blank">KW / ÁR számoló</a></li><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/5/grow-szamolo-
30.html" target="_blank">GROW Számoló</a></li><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/uploded/doc/" target="_blank">Könyvek</a></li><li style="text-indent: 0px;"><a rel="nofollow" style="color:" href="https://twitter.com/#!/kenderforum" target="_blank">Twitter</a></li></ul></li><li class="popupmenu"><a href="javascript://" class="popupctrl navtab" style="background:transparent url(images/misc/arrow.png) no-repeat right center; padding-right: 15px">Magrendelés</a><ul class="popupbody popuphover"><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/57/pick-n-mix-2647.html" target="_blank">Pick and Mix</a></li><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/57/nirvana-seed-2112.html" target="_blank">Nirvana Seed</a></li><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/57/sensi-seeds-2655.html" target="_blank">Sensi Seeds</a></li></ul></li> </ul> <div id="globalsearch" class="
globalsearch"> <form action="search.php?do=process" method="post" id="navbar_search" class="navbar_search"> <input type="hidden" name="securitytoken" value="1370472078-81f10ad2088edd0fb3d800b27eefe81d962b42cc" /> <input type="hidden" name="do" value="process" /> <span class="textboxcontainer"><span><input type="text" value="" name="query" class="textbox" tabindex="99"/></span></span> <span class="buttoncontainer"><span><input type="image" class="searchbutton" src="images/buttons/search.png" name="submit" onclick="document.getElementById('navbar_search').submit;" tabindex="100"/></span></span> </form> <ul class="navbar_advanced_search"> <li><a href="search.php" accesskey="4">Részletes keresés</a></li> </ul> </div> </div> </div> <div class="body_wrapper">   <div id="breadcrumb" class="breadcrumb"> <ul class="floatcontainer"> <li class="navbithome"><a href="https://www.kenderforum.org/" accesskey="1"><img src="images/misc/navbit-home.png" alt="Főoldal" /></a></li> <div itemscope="itemscope" itemtype="http://
data-vocabulary.org/Breadcrumb"> <li class="navbit lastnavbit"><span><span itemprop="title">Kender Forum Chat : Archives</span></span></li> </div> </ul> <hr /> </div> <div id="ad_global_below_navbar"><center> <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"
WIDTH="800"
wmode="transparent" 
HEIGHT="100"
CODEBASE="https://active.macromedia.com/flash5/cabs/swflash.cab#version=5,0,0,0"> <PARAM NAME="MOVIE" VALUE="https://www.kenderforum.org/images/banners/AHOH.swf"> <PARAM NAME="PLAY" VALUE="true"> <param name="wmode" value="transparent"> <PARAM NAME="LOOP" VALUE="true"> <PARAM NAME="QUALITY" VALUE="high"> <PARAM NAME="SCALE" value="noborder"> <EMBED SRC="https://www.kenderforum.org/images/banners/AHOH.swf"
WIDTH="800"
HEIGHT="100"
PLAY="true" 
LOOP="true"
QUALITY="high" 
scale="noborder"
PLUGINSPAGE="https://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash"> </EMBED> </OBJECT> </center> </div> <script type="text/javascript">
var chatids_array = [209013,209012,209011,209010,209009,209008,209007,209006,209005,209004,209003,209002,209001,209000,208999];var MGCCbEvoNS = {};
var phrase_error_chat_in_process = "Error : A chat is already being processed, please wait.";
var phrase_enter_url = "Enter the URL";
var phrase_enter_email = "Enter the email address";
var phrase_enter_imgurl = "Enter the image URL";
var phrase_already_editing = "Error : A chat is already being edited";
var phrase_edit_forbidden = "Error : You are not allowed to edit this chat";
var phrase_inactive = "<strong>The chatbox is in inactive mode.<br />To leave this mode, click on the refresh button if visible, otherwise press the F5 key to reload you browser's page.</strong>";
var phrase_enter_urltext = "Link text (optional)";
var phrase_enter_name = "Please enter a username for your chats";
var phrase_error_name = "Error: the entered username is incorrect";
var phrase_ok = "OK";
var phrase_yes = "Igen";
var phrase_no = "Nem";
var phrase_save = "Mentés";
var phrase_cancel = "Mégse";
var phrase_enter_report_reason = "Enter your report's reason:";
var phrase_pm_maxtabs_reached = "Error : You have reached the maximum number of private discussions tabs authorized (5)";
var phrase_mgc_cb_evo_cmd_syntax = "Syntax:";
MGCCbEvoNS.height = "0";
MGCCbEvoNS.refresh_delay = 30000;
MGCCbEvoNS.pm_refresh_delay = 3000;
MGCCbEvoNS.auto_refresh = 1;
MGCCbEvoNS.chats_when_collapsed = 5;
MGCCbEvoNS.chats_order = 0;
MGCCbEvoNS.inactive_mode_on = 0;
MGCCbEvoNS.inactive_mode_delay = 600000;
MGCCbEvoNS.bburl = "https://www.kenderforum.org";
MGCCbEvoNS.avatar_on = 0;
MGCCbEvoNS.align_chats = 1;
MGCCbEvoNS.alt_chat_colors = 0;
MGCCbEvoNS.warn_delay = 300000;
MGCCbEvoNS.warn_active = 0;
MGCCbEvoNS.chat_valign = "middle";
MGCCbEvoNS.hide_refreshimg = 0;
MGCCbEvoNS.left = "left";
MGCCbEvoNS.right = "right";
MGCCbEvoNS.imgdir_misc = "images/misc";
MGCCbEvoNS.br_after_username = 0;
MGCCbEvoNS.wysiwyg = 1;
MGCCbEvoNS.showtime = 1;
MGCCbEvoNS.time_24hours = 1;
MGCCbEvoNS.colspan = 2;
MGCCbEvoNS.pm_maxtab = 5;
MGCCbEvoNS.filename = "mgc_cb_evo.php";
MGCCbEvoNS.activate_atusername_icon = 0;
MGCCbEvoNS.char_limit = 0;
MGCCbEvoNS.dojo_theme = 0;
MGCCbEvoNS.small_version = 0;
MGCCbEvoNS.notifs_display = 0;
MGCCbEvoNS.this_script = "mgc_cb_evo";
MGCCbEvoNS.ubbcode_b = 0;
MGCCbEvoNS.ubbcode_u = 0;
MGCCbEvoNS.ubbcode_i = 0;
MGCCbEvoNS.ubbcode_color     = "#";
MGCCbEvoNS.ubbcode_font     = "";
MGCCbEvoNS.ubbcode_size        = "";
MGCCbEvoNS.ugpbbcode_color    = "#000000";
MGCCbEvoNS.sound = 0;
MGCCbEvoNS.channel_sound = 0;
MGCCbEvoNS.ask_anonymous_name = 0;
MGCCbEvoNS.editor_onside = 0;
MGCCbEvoNS.chatbox_inactive = 0;
MGCCbEvoNS.inactive_timeout = null;
MGCCbEvoNS.iscollapsed = 0;
MGCCbEvoNS.initstate = 1;
MGCCbEvoNS.isvb4 = 1;
MGCCbEvoNS.isoldvb3 = 0;
MGCCbEvoNS.autorefresh_on = 0;
MGCCbEvoNS.jsloc = "";
MGCCbEvoNS.input_prompt_msg = 0;
MGCCbEvoNS.autocomplete_on = 0;
MGCCbEvoNS.disable_refresh_upon_postlimit = 0;

</script> <script type="text/javascript" src="mgc_cb_evo/clientscript/dojo/dojo/dojo.js"  data-dojo-config="parseOnLoad: true"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_common.js"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_menu.js"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_dialog.js"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_chat.js"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_archives.js"></script> <table cellpadding="0" cellspacing="0" border="0" width="100%" align="center"> <tr valign="top">  <td>  <table class="block mgc_cb_evo_block_chatbit" cellpadding="5" cellspacing="5" border="0"> <thead> <tr> <td class="blockheader" colspan="2" width="100%" nowrap="nowrap">10 best chatters</td> </tr> </thead> <tbody class="blockbody"> <tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  
href="tagok/6107/szotyiba">szotyibá</a></td><td class="alt1" align="center">143</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/6539/ooosuli">óÓóSULI</a></td><td class="alt1" align="center">80</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/5104/szajmoka">szajmoka</a></td><td class="alt1" align="center">79</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/4938/bullterrier07">Bullterrier07</a></td><td class="alt1" align="center">75</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/6486/jeffry">Jeffry</a></td><td class="alt1" align="center">66</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/928/coldfusion">Coldfusion</a></td><td class="alt1" align="center">52</td></
tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/6614/vacak">vacak</a></td><td class="alt1" align="center">49</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/7022/d%40nte">d@nte</a></td><td class="alt1" align="center">46</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/6669/hydromester">hydromester</a></td><td class="alt1" align="center">46</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/7424/tiktiktik">Tiktiktik</a></td><td class="alt1" align="center">40</td></tr> </tbody> <thead> <tr> <td class="blockheader" colspan="2" width="100%" nowrap="nowrap">Other stats</td> </tr> </thead> <tbody class="blockbody"> <tr class="blockrow"> <td class="alt2" width="100%" align="left" nowrap="nowrap">Chats</td> <td class="alt1" align="center" nowrap="
nowrap">1033</td> </tr> <tr class="blockrow"> <td class="alt2" width="100%" align="left" nowrap="nowrap">Last 24h chats</td> <td class="alt1" align="center" nowrap="nowrap">1033</td> </tr> <tr class="blockrow"> <td class="alt2" width="100%" align="left" nowrap="nowrap">Your chats</td> <td class="alt1" align="center" nowrap="nowrap">0</td> </tr> </tbody> </table>  <br />  <table class="block mgc_cb_evo_block_chatbit" cellpadding="5" cellspacing="5" border="0" width="100%"> <thead> <tr> <td class="blockheader" width="100%" nowrap="nowrap">Navigation</td> </tr> </thead> <tbody class="blockbody"> <tr> <td class="alt2 smallfont" width="100%"> <strong>Since:</strong><br /> <select name="channel_dlimit" id="channel_dlimit" onchange="return MGCCbEvoNS.change_archives_page();"> <option value="1" selected="selected">Yesterday</option> <option value="2" >2 days</option> <option value="7" >1 week</option> <option value="14" >2 weeks</option> <option value="30" >30 days</option> <option value="60" >60 days</option> 
<option value="90" >90 days</option> <option value="120" >120 days</option> <option value="-1" >The beginning</option> </select> <input type="button" name="dochangeview" value="Mehet" onclick="return MGCCbEvoNS.change_archives_page();" /> </td> </tr> </tbody> </table>  <br />   </td>  <td>&nbsp;&nbsp;</td>  <td width="100%">  <table class="block mgc_cb_evo_block_chatbit" cellpadding="5" cellspacing="5" border="0" width="100%" align="center"> <thead> <tr> <td class="blockheader" width="0" align="center" valign="middle">&nbsp;</td> <td class="blockheader" width="0" nowrap="nowrap"="nowrap="nowrap"" align="center" valign="middle">Dátum</td> <td class="blockheader" width="0" nowrap="nowrap"="nowrap="nowrap"" align="$stylevar[left]" valign="middle">Becenév</td> <td class="blockheader" valign="middle" width="100%" nowrap="nowrap"="nowrap="nowrap"" align="left">Chat</td> </tr> </thead> <tbody class="blockbody"><tr> <td class="alt2" width="0" id="chat_209013" align="center" valign="middle"> <div class="popupmenu" 
id="chat_209013_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209013_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/7458/bogota-rich" rel="nofollow">
                    View BOGOTA RICH's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209013" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            06/06/2013 00:39
        </span> </td> <td valign="middle" class="alt2" id="uname_209013" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/7458/bogota-rich">&lt;BOGOTA RICH&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209013" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209013" >
            kemény ez a citromos gösser
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209012" align="center" valign="middle"> <div class="popupmenu" id="chat_209012_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209012_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/7458/bogota-rich" rel="nofollow">
                    View BOGOTA RICH's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209012" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            06/06/2013 00:39
        </span> </td> <td valign="middle" class="alt2" id="uname_209012" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/7458/bogota-rich">&lt;BOGOTA RICH&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209012" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209012" >
            grrrrrrrrr besörözteeeeeeeeeeem
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209011" align="center" valign="middle"> <div class="popupmenu" id="chat_209011_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209011_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/5104/szajmoka" rel="nofollow">
                    View szajmoka's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209011" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            06/06/2013 00:15
        </span> </td> <td valign="middle" class="alt2" id="uname_209011" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/5104/szajmoka">&lt;szajmoka&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209011" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209011" > <font face="Arial Black"><a rel="nofollow" href="http://m.youtube.com/index?&amp;desktop_uri=%2F" target="_blank">http://m.youtube.com/index?&amp;desktop_uri=%2F</a></font> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209010" align="center" valign="middle"> <div class="popupmenu" id="chat_209010_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209010_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/2569/smoke2joints" rel="nofollow">
                    View smoke2joints's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209010" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 23:35
        </span> </td> <td valign="middle" class="alt2" id="uname_209010" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/2569/smoke2joints">&lt;smoke2joints&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209010" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209010" >
            miert ne tudnal?
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209009" align="center" valign="middle"> <div class="popupmenu" id="chat_209009_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209009_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6013/bigbuds" rel="nofollow">
                    View bigbuds's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209009" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 23:01
        </span> </td> <td valign="middle" class="alt2" id="uname_209009" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6013/bigbuds">&lt;bigbuds&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209009" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209009" >
            szerintetek repülön tudok kivinni vapourizert mongyuk a mobilt lotli csak gàztarjtàlyos és nem vàgom..
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209008" align="center" valign="middle"> <div class="popupmenu" id="chat_209008_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209008_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6013/bigbuds" rel="nofollow">
                    View bigbuds's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209008" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:54
        </span> </td> <td valign="middle" class="alt2" id="uname_209008" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6013/bigbuds">&lt;bigbuds&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209008" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209008" > <img src="images/smilies/116.gif" border="0" alt="" title="" class="inlineimg" /><img src="images/smilies/4204.gif" border="0" alt="" title="" class="inlineimg" /><img src="images/smilies/party.gif" border="0" alt="" title="(party)" class="inlineimg" /> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209007" align="center" valign="middle"> <div class="popupmenu" id="chat_209007_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209007_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6013/bigbuds" rel="
nofollow">
                    View bigbuds's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209007" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:54
        </span> </td> <td valign="middle" class="alt2" id="uname_209007" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6013/bigbuds">&lt;bigbuds&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209007" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209007" >
            megyek pàr hét mulva angliaba ott hajora szàlok és irany hollandia... jack herer
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209006" align="center" valign="middle"> <div class="popupmenu" id="chat_209006_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209006_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209006" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:51
        </span> </td> <td valign="middle" class="alt2" id="uname_209006" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209006" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209006" >
            de hát jó pap holtig tanul <img src="images/smilies/21.gif" border="0" alt="" title="" class="inlineimg" /> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209005" align="center" valign="middle"> <div class="popupmenu" id="chat_209005_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209005_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209005" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:51
        </span> </td> <td valign="middle" class="alt2" id="uname_209005" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209005" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209005" >
            sok a kérdés mi
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209004" align="center" valign="middle"> <div class="popupmenu" id="chat_209004_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209004_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209004" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:50
        </span> </td> <td valign="middle" class="alt2" id="uname_209004" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209004" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209004" > <img src="images/smilies/4.gif" border="0" alt="" title="" class="inlineimg" /> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209003" align="center" valign="middle"> <div class="popupmenu" id="chat_209003_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209003_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209003" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:50
        </span> </td> <td valign="middle" class="alt2" id="uname_209003" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209003" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209003" >
            :jó éjt
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209002" align="center" valign="middle"> <div class="popupmenu" id="chat_209002_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209002_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6107/szotyiba" rel="nofollow">
                    View szotyibá's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209002" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:50
        </span> </td> <td valign="middle" class="alt2" id="uname_209002" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6107/szotyiba">&lt;szotyibá&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209002" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209002" > <font face="Comic Sans MS"><font color="#483D8B"><font size="2"><b>jóéjt <img src="images/smilies/103.gif" border="0" alt="" title="" class="inlineimg" /></b></font></font></font> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209001" align="center" valign="middle"> <div class="popupmenu" id="chat_209001_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209001_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6107/szotyiba" rel="nofollow">
                    View szotyibá's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209001" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:50
        </span> </td> <td valign="middle" class="alt2" id="uname_209001" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6107/szotyiba">&lt;szotyibá&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209001" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209001" > <font face="Comic Sans MS"><font color="#483D8B"><font size="2"><b>de kb jó 5db-al.</b></font></font></font> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209000" align="center" valign="middle"> <div class="popupmenu" id="chat_209000_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209000_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6107/szotyiba" rel="nofollow">
                    View szotyibá's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209000" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:49
        </span> </td> <td valign="middle" class="alt2" id="uname_209000" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6107/szotyiba">&lt;szotyibá&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209000" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209000" > <font face="Comic Sans MS"><font color="#483D8B"><font size="2"><b>ehhez már késő van <img src="images/smilies/4.gif" border="0" alt="" title="" class="inlineimg" /></b></font></font></font> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_208999" align="center" valign="middle"> <div class="popupmenu" id="chat_208999_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_208999_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_208999" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:47
        </span> </td> <td valign="middle" class="alt2" id="uname_208999" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_208999" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_208999" >
            na, tehát 400w 3hét 80x80?
        </span> </td> </tr></tbody> </table>  <br /> <div style="float : left"> <div class="pagination"> <form action="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1" method="get" class="pagination popupmenu nohovermenu"> <input type="hidden" name="do" value="view_archives" /><input type="hidden" name="r" value="channel_id" /><input type="hidden" name="dlimit" value="1" /> <span><a href="javascript://" class="popupctrl">Oldal: 1 / 69</a></span> <span class="selected"><a href="javascript://" title="Eredmény: 1 - 15  (1.033) összesen">1</a></span><span><a rel="nofollow" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=2" title="Eredmények megjelenítése: 16 - 30 (1.033) összesen">2</a></span><span><a rel="nofollow" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=3" title="Eredmények megjelenítése: 31 - 45 (1.033) összesen">3</a></span><span><a rel="nofollow" 
href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=11" title="Eredmények megjelenítése: 151 - 165 (1.033) összesen">11</a></span><span><a rel="nofollow" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=51" title="Eredmények megjelenítése: 751 - 765 (1.033) összesen">51</a></span> <span class="separator">...</span> <span class="prev_next"><a rel="next" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=2" title="Következő oldal - Eredmények: 16 - 30, (1.033) összesen"><img src="images/pagination/next-right.png" alt="Következő" /></a></span> <span class="first_last"><a rel="nofollow" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=69" title="Utolsó oldal - Eredmények: 1.021 - 1.033, (1.033) összesen">Utolsó<img src="images/pagination/last-right.png" alt="Utolsó" /></a></span> <ul class="
popupbody popuphover"> <li class="formsubmit jumptopage"><label>Jump to page: <input type="text" name="page" size="4" /></label> <input type="submit" class="button" value="Mehet" /></li> </ul> </form> </div> </div> <div style="clear: both;">   <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:"Information request"' id="mgc_cb_evo_promptdialog"> <div id="mgc_cb_evo_promptdialog_content"></div> <input type="text" size="35" id="mgc_cb_evo_promptdialog_input" /> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:MGCCbEvoNS.show_promptdialog_submit">Mentés</button> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:MGCCbEvoNS.hide_promptdialog">Mégse</button> </div> </div>  <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:""' id="mgc_cb_evo_dialog"> <div id="mgc_cb_evo_dialog_content"></div> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:MGCCbEvoNS.
hide_dialog">OK</button> </div> </div>  <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:""' id="mgc_cb_evo_yesnodialog"> <div id="mgc_cb_evo_yesnodialog_content"></div> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:dojo.hitch(MGCCbEvoNS,'hide_yesnodialog_yes')">Igen</button> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:MGCCbEvoNS.hide_yesnodialog_no">Nem</button> </div> </div>  <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:"Chatbox rules"' id="mgc_cb_evo_rules"> </div> </div>  <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:"MGC Chatbox Evo Help"' id="mgc_cb_evo_help"> </div> </div>  </div> </td>  </tr> </table><div align="center"><b><a rel="nofollow" href="http://www.mgcproducts.com/" title="MGC Products / Support Site">MGC Chatbox Evo</a></b> v3.2.3 by MGC &copy; 2008-2012</div>   <div style="
clear: left"> </div> <div id="footer" class="floatcontainer footer"> <form action="https://www.kenderforum.org/" method="get" id="footer_select" class="footer_select"> </form> <ul id="footer_links" class="footer_links"> <li><a href="sendmessage.php" rel="nofollow" accesskey="9">Írjál nekünk!</a></li> <li><a href="https://www.kenderforum.org">Kender Fórum</a></li> <li><a href="sitemap/">Archívum</a></li> <li><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#top" onclick="document.location.hash='top'; return false;">Ugrás a tetejére</a></li> </ul> <script type="text/javascript"> <!--
        // Main vBulletin Javascript Initialization
        vBulletin_init();
    //--> </script> </div> </div>  <div class="below_body"> <div id="footer_time" class="shade footer_time">A pontos idő <span class="time">00:41</span> , a GMT +2 időzóna szerint.</div> <div id="footer_copyright" class="shade footer_copyright"> 
    Powered by vBulletin&reg;  Version 4.1.12 - Copyright &copy; 2000 - 2013, vBulletin Solutions, Inc. 

    
<br />Content Relevant URLs by <a rel="nofollow" href="http://www.vbseo.com/2352/">vBSEO</a> 3.6.0 </div> <div id="footer_morecopyright" class="shade footer_morecopyright">   </div> <script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-21499087-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script> <script type="text/javascript" src="https://www.duppy.org/clickheat/js/clickheat.js"></script><noscript><p><a rel="nofollow" href="http://www.dugwood.com/index.html">Open Source Sofware</a></p></noscript><script type="text/javascript"><!--
clickHeatSite = '';clickHeatGroup = encodeURIComponent(window.location.pathname+window.location.search);clickHeatServer = 'https://www.duppy.org/clickheat/click.php';initClickHeat(); //--> </script> </div> </body> </html>"""

soup = BeautifulSoup(samplehtml)

szoveg = soup.findAll(id=re.compile('text.'))
nev = soup.findAll(id=re.compile('uname.'))
datum = soup.findAll(id=re.compile('date.'))

for incu in range(1,10):
    #nev = unicode(nev[incu].text)
    #nev = nev[4:len(nev)-4] #konvertalni kell strbe de ugy a charset nem stimmel
    sor = datum[incu].text + ('\t') + nev[incu].text + ('\t') + szoveg[incu].text + ('\n')
    #scraperwiki.sqlite.save(data={"Datum": datum[incu].text, "Nev": nev[incu].text, "Text": szoveg[incu].text})
    scraperwiki.sqlite.save(unique_keys=["Datum"], data={"Datum":datum[incu].text, "Nev":nev[incu].text, "Text": szoveg[incu].text})# lxml is a complete library for parsing xml and html files.  http://codespeak.net/lxml/
# -*- coding: utf-8 -*-

# The interface is not totally intuitive, but it is very effective to use, 
# especially with cssselect.

import lxml.etree, lxml.html, re, scraperwiki
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup

#print help(lxml.html.parse)


# create an example case
samplehtml = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"> <html xmlns="http://www.w3.org/1999/xhtml"  dir="ltr" lang="hun" id="vbulletin_html"> <head>  <script type="text/javascript" src="https://www.kenderforum.org/mobiquo/tapatalkdetect.js"></script>  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> <meta id="e_vb_meta_bburl" name="vb_meta_bburl" content="https://www.kenderforum.org" /> <meta name="generator" content="vBulletin 4.1.12" /> <link rel="Shortcut Icon" href="favicon.ico" type="image/x-icon" /> <meta name="keywords" content="" /> <meta name="description" content="" /> <script type="text/javascript"> <!--
    if (typeof YAHOO === 'undefined') // Load ALL YUI Local
    {
        document.write('<script type="text/javascript" src="clientscript/yui/yuiloader-dom-event/yuiloader-dom-event.js?v=4112"><\/script>');
        document.write('<script type="text/javascript" src="clientscript/yui/connection/connection-min.js?v=4112"><\/script>');
        var yuipath = 'clientscript/yui';
        var yuicombopath = '';
        var remoteyui = false;
    }
    else    // Load Rest of YUI remotely (where possible)
    {
        var yuipath = 'clientscript/yui';
        var yuicombopath = '';
        var remoteyui = true;
        if (!yuicombopath)
        {
            document.write('<script type="text/javascript" src="clientscript/yui/connection/connection-min.js"><\/script>');
        }
    }
    var SESSIONURL = "";
    var SECURITYTOKEN = "1370472078-81f10ad2088edd0fb3d800b27eefe81d962b42cc";
    var IMGDIR_MISC = "images/misc";
    var IMGDIR_BUTTON = "images/buttons";
    var vb_disable_ajax = parseInt("0", 10);
    var SIMPLEVERSION = "4112";
    var BBURL = "https://www.kenderforum.org";
    var LOGGEDIN = 5893 > 0 ? true : false;
    var THIS_SCRIPT = "mgc_cb_evo";
    var RELPATH = "mgc_cb_evo.php?do=view_archives&amp;page=1";
    var PATHS = {
        forum : "",
        cms   : "",
        blog  : ""
    };
    var AJAXBASEURL = "https://www.kenderforum.org/";
// --> </script> <script type="text/javascript" src="https://www.kenderforum.org/clientscript/vbulletin-core.js?v=4112"></script> <link rel="alternate" type="application/rss+xml" title="Kender Fórum RSS Feed" href="https://www.kenderforum.org/external.php?type=RSS2" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/main-rollup.css?d=1360781686" /> <!--[if lt IE 8]> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/popupmenu-ie.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/vbulletin-ie.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/vbulletin-chrome-ie.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/vbulletin-formcontrols-ie.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/editor-ie.css?d=1360781686" /> <![endif]--
> <script src="https://kenderforum.org/clientscript/jquery/jquery-1.6.4.min.js"></script> <script src="https://kenderforum.org/clientscript/sticky_panel.js"></script>  <script type="text/javascript">
        $().ready(function () {
            var stickyPanelOptions = {
                topPadding: 10,
                afterDetachCSSClass: "off_stick1",
                savePanelSpace: true
            };
            $("#column_left_ad1").stickyPanel(stickyPanelOptions);
            $("#column_right_ad2").stickyPanel(stickyPanelOptions);


        });
    </script>  <link rel="stylesheet" href="mgc_cb_evo/clientscript/dojo/dijit/themes/claro/claro.css" type="text/css"><link rel="stylesheet" href="css.php?styleid=6&amp;langid=2&amp;d=1360781686&amp;sheet=mgc_cb_evo.css" type="text/css"> <title>Kender Forum Chat : Archives</title> <link rel="stylesheet" type="text/css" href="clientscript/vbulletin_css/style00006l/additional.css?d=1360781686" /> <link rel="stylesheet" type="text/css" href="css.php?styleid=6&amp;langid=2&amp;d=1360781686&amp;sheet=ss_twincolumns_css.css" /> </head> <body> <div class="above_body">  <div id="header" class="floatcontainer doc_header"> <div><a name="top" href="https://www.kenderforum.org/" class="logo-image"><img src="images/misc/vbulletin4_logo.png" alt="Kender Fórum - Powered by vBulletin" /></a></div> <div style="float: left; padding-left: 15%;"> <a class="navtab" href="private.php"><img  style="vertical-align: middle;" src="kendimg/pm.png" alt="Új privát üzeneted érkezett" />&nbsp; &nbsp; <font size="2" style="text-alig:right;
" >ÚJ ÜZENET</font></a> </div> <div id="toplinks" class="toplinks"> <ul class="isuser"> <li><a rel="nofollow" href="login.php?do=logout&amp;logouthash=1370472078-81f10ad2088edd0fb3d800b27eefe81d962b42cc" onclick="return log_out('Biztos hogy ki akarsz lépni?')">Kilép</a></li> <li><a href="usercp.php">Kezelőpult</a></li> <li><a href="tagok/5893/ppp">Profil</a></li> <li class="popupmenu notifications" id="notifications"> <a class="popupctrl" href="usercp.php">Értesítők: <span class="notifications-number"><strong>10</strong></span></a> <ul class="popupbody popuphover"> <li><a href="private.php"><span>10</span> Olvasatlan privát üzenetek</a></li> </ul> </li> <li class="welcomelink">Üdvözlünk, <a href="tagok/5893/ppp">ppp</a>.</li> </ul> </div> <div class="ad_global_header"> </div> <hr /> </div> <div id="navbar" class="navbar"> <ul id="navtabs" class="navtabs floatcontainer notify"> <li class="selected"><a class="navtab" href="https://www.kenderforum.org/">Fórum</a> <ul class="floatcontainer"> <li><a href="https://
www.kenderforum.org/">Fórum</a></li> <li><a rel="nofollow" href="search.php?do=getnew&amp;contenttype=vBForum_Post">Új hozzászólások</a></li> <li><a href="private.php" rel="nofollow">Privát üzenetek</a></li> <li><a rel="help" href="faq.php" accesskey="5">Súgó</a></li> <li><a href="calendar.php">Naptár</a></li> <li class="popupmenu"> <a href="javascript://" class="popupctrl" accesskey="6">Közösség</a> <ul class="popupbody popuphover"> <li><a href="csoportok/csoport.html">Közösségi csoportok</a></li> <li><a href="https://www.kenderforum.org/tagok/albumok/">Képek &amp; Albumok </a></li> <li><a rel="nofollow" href="profile.php?do=buddylist">Kapcsolatok &amp; Barátok</a></li> <li><a href="tagok/lista/">Taglista</a></li> <li><a rel="nofollow" href="thanks.php?do=hottest">Hottest Threads / Posts</a></li> <li><a rel="nofollow" href="thanks.php?do=statistics">Thanks / Like Statistics</a></li> </ul> </li> <li class="popupmenu"> <a href="javascript://" class="popupctrl">Fórum eszközök</a> <ul class="popupbody 
popuphover"> <li> <a rel="nofollow" href="forumdisplay.php?do=markread&amp;markreadhash=1370472078-81f10ad2088edd0fb3d800b27eefe81d962b42cc">Fórumokat olvasottnak jelöli</a> </li> <li> <a rel="nofollow" href="profile.php?do=editoptions">Beállítások módosítása</a> </li> <li> <a rel="nofollow" href="profile.php?do=editprofile">Profil módosítása</a> </li> </ul> </li> <li class="popupmenu"> <a href="javascript://" class="popupctrl" accesskey="3">Expressz</a> <ul class="popupbody popuphover"> <li><a href="search.php?do=getdaily&amp;contenttype=vBForum_Post">Mai hozzászólások</a></li> <li><a href="subscription.php" rel="nofollow">Követett témák</a></li> <li><a href="javascript://" onclick="window.open(getBaseUrl() + 'misc.php?do=buddylist&amp;focus=1','buddylist','statusbar=no,menubar=no,toolbar=no,scrollbars=yes,resizable=yes,width=250,height=300'); return false;">Kapcsolat popup megnyitása</a></li> <li><a href="showgroups.php" rel="nofollow">
                                
                                    Fórum vezetők listázása
                                
                            </a></li> <li><a href="online.php">Jelenlévő aktív tagok</a></li> <li><a rel="nofollow" href="misc.php?do=donlist">View Donations</a></li> </ul> </li> <li><a rel="nofollow" href="misc.php?do=donate"><span style="color:[b][color=#008000]Donate[/color][/b];">Donate<span></a></li> </ul> </li> <li ><a class='navtab' href='https://www.kenderforum.org/5/szabalyzat-1954.html#post49757' target='_blank'> Szabályzat</a></li><li ><a class='navtab' href='https://www.kenderforum.org/5/biztonsag-1983.html' target='_blank'> Biztonság</a></li><li class="popupmenu"><a href="javascript://" class="popupctrl navtab" style="background:transparent url(images/misc/arrow.png) no-repeat right center; padding-right: 15px">Eszköztár</a><ul class="popupbody popuphover"><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/5/kw-ar-szamolo-77.html" target="_blank">KW / ÁR számoló</a></li><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/5/grow-szamolo-
30.html" target="_blank">GROW Számoló</a></li><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/uploded/doc/" target="_blank">Könyvek</a></li><li style="text-indent: 0px;"><a rel="nofollow" style="color:" href="https://twitter.com/#!/kenderforum" target="_blank">Twitter</a></li></ul></li><li class="popupmenu"><a href="javascript://" class="popupctrl navtab" style="background:transparent url(images/misc/arrow.png) no-repeat right center; padding-right: 15px">Magrendelés</a><ul class="popupbody popuphover"><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/57/pick-n-mix-2647.html" target="_blank">Pick and Mix</a></li><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/57/nirvana-seed-2112.html" target="_blank">Nirvana Seed</a></li><li style="text-indent: 0px;"><a style="color:" href="https://www.kenderforum.org/57/sensi-seeds-2655.html" target="_blank">Sensi Seeds</a></li></ul></li> </ul> <div id="globalsearch" class="
globalsearch"> <form action="search.php?do=process" method="post" id="navbar_search" class="navbar_search"> <input type="hidden" name="securitytoken" value="1370472078-81f10ad2088edd0fb3d800b27eefe81d962b42cc" /> <input type="hidden" name="do" value="process" /> <span class="textboxcontainer"><span><input type="text" value="" name="query" class="textbox" tabindex="99"/></span></span> <span class="buttoncontainer"><span><input type="image" class="searchbutton" src="images/buttons/search.png" name="submit" onclick="document.getElementById('navbar_search').submit;" tabindex="100"/></span></span> </form> <ul class="navbar_advanced_search"> <li><a href="search.php" accesskey="4">Részletes keresés</a></li> </ul> </div> </div> </div> <div class="body_wrapper">   <div id="breadcrumb" class="breadcrumb"> <ul class="floatcontainer"> <li class="navbithome"><a href="https://www.kenderforum.org/" accesskey="1"><img src="images/misc/navbit-home.png" alt="Főoldal" /></a></li> <div itemscope="itemscope" itemtype="http://
data-vocabulary.org/Breadcrumb"> <li class="navbit lastnavbit"><span><span itemprop="title">Kender Forum Chat : Archives</span></span></li> </div> </ul> <hr /> </div> <div id="ad_global_below_navbar"><center> <OBJECT CLASSID="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"
WIDTH="800"
wmode="transparent" 
HEIGHT="100"
CODEBASE="https://active.macromedia.com/flash5/cabs/swflash.cab#version=5,0,0,0"> <PARAM NAME="MOVIE" VALUE="https://www.kenderforum.org/images/banners/AHOH.swf"> <PARAM NAME="PLAY" VALUE="true"> <param name="wmode" value="transparent"> <PARAM NAME="LOOP" VALUE="true"> <PARAM NAME="QUALITY" VALUE="high"> <PARAM NAME="SCALE" value="noborder"> <EMBED SRC="https://www.kenderforum.org/images/banners/AHOH.swf"
WIDTH="800"
HEIGHT="100"
PLAY="true" 
LOOP="true"
QUALITY="high" 
scale="noborder"
PLUGINSPAGE="https://www.macromedia.com/shockwave/download/index.cgi?P1_Prod_Version=ShockwaveFlash"> </EMBED> </OBJECT> </center> </div> <script type="text/javascript">
var chatids_array = [209013,209012,209011,209010,209009,209008,209007,209006,209005,209004,209003,209002,209001,209000,208999];var MGCCbEvoNS = {};
var phrase_error_chat_in_process = "Error : A chat is already being processed, please wait.";
var phrase_enter_url = "Enter the URL";
var phrase_enter_email = "Enter the email address";
var phrase_enter_imgurl = "Enter the image URL";
var phrase_already_editing = "Error : A chat is already being edited";
var phrase_edit_forbidden = "Error : You are not allowed to edit this chat";
var phrase_inactive = "<strong>The chatbox is in inactive mode.<br />To leave this mode, click on the refresh button if visible, otherwise press the F5 key to reload you browser's page.</strong>";
var phrase_enter_urltext = "Link text (optional)";
var phrase_enter_name = "Please enter a username for your chats";
var phrase_error_name = "Error: the entered username is incorrect";
var phrase_ok = "OK";
var phrase_yes = "Igen";
var phrase_no = "Nem";
var phrase_save = "Mentés";
var phrase_cancel = "Mégse";
var phrase_enter_report_reason = "Enter your report's reason:";
var phrase_pm_maxtabs_reached = "Error : You have reached the maximum number of private discussions tabs authorized (5)";
var phrase_mgc_cb_evo_cmd_syntax = "Syntax:";
MGCCbEvoNS.height = "0";
MGCCbEvoNS.refresh_delay = 30000;
MGCCbEvoNS.pm_refresh_delay = 3000;
MGCCbEvoNS.auto_refresh = 1;
MGCCbEvoNS.chats_when_collapsed = 5;
MGCCbEvoNS.chats_order = 0;
MGCCbEvoNS.inactive_mode_on = 0;
MGCCbEvoNS.inactive_mode_delay = 600000;
MGCCbEvoNS.bburl = "https://www.kenderforum.org";
MGCCbEvoNS.avatar_on = 0;
MGCCbEvoNS.align_chats = 1;
MGCCbEvoNS.alt_chat_colors = 0;
MGCCbEvoNS.warn_delay = 300000;
MGCCbEvoNS.warn_active = 0;
MGCCbEvoNS.chat_valign = "middle";
MGCCbEvoNS.hide_refreshimg = 0;
MGCCbEvoNS.left = "left";
MGCCbEvoNS.right = "right";
MGCCbEvoNS.imgdir_misc = "images/misc";
MGCCbEvoNS.br_after_username = 0;
MGCCbEvoNS.wysiwyg = 1;
MGCCbEvoNS.showtime = 1;
MGCCbEvoNS.time_24hours = 1;
MGCCbEvoNS.colspan = 2;
MGCCbEvoNS.pm_maxtab = 5;
MGCCbEvoNS.filename = "mgc_cb_evo.php";
MGCCbEvoNS.activate_atusername_icon = 0;
MGCCbEvoNS.char_limit = 0;
MGCCbEvoNS.dojo_theme = 0;
MGCCbEvoNS.small_version = 0;
MGCCbEvoNS.notifs_display = 0;
MGCCbEvoNS.this_script = "mgc_cb_evo";
MGCCbEvoNS.ubbcode_b = 0;
MGCCbEvoNS.ubbcode_u = 0;
MGCCbEvoNS.ubbcode_i = 0;
MGCCbEvoNS.ubbcode_color     = "#";
MGCCbEvoNS.ubbcode_font     = "";
MGCCbEvoNS.ubbcode_size        = "";
MGCCbEvoNS.ugpbbcode_color    = "#000000";
MGCCbEvoNS.sound = 0;
MGCCbEvoNS.channel_sound = 0;
MGCCbEvoNS.ask_anonymous_name = 0;
MGCCbEvoNS.editor_onside = 0;
MGCCbEvoNS.chatbox_inactive = 0;
MGCCbEvoNS.inactive_timeout = null;
MGCCbEvoNS.iscollapsed = 0;
MGCCbEvoNS.initstate = 1;
MGCCbEvoNS.isvb4 = 1;
MGCCbEvoNS.isoldvb3 = 0;
MGCCbEvoNS.autorefresh_on = 0;
MGCCbEvoNS.jsloc = "";
MGCCbEvoNS.input_prompt_msg = 0;
MGCCbEvoNS.autocomplete_on = 0;
MGCCbEvoNS.disable_refresh_upon_postlimit = 0;

</script> <script type="text/javascript" src="mgc_cb_evo/clientscript/dojo/dojo/dojo.js"  data-dojo-config="parseOnLoad: true"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_common.js"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_menu.js"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_dialog.js"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_chat.js"></script><script type="text/javascript" src="mgc_cb_evo/clientscript/mgc_cb_evo_archives.js"></script> <table cellpadding="0" cellspacing="0" border="0" width="100%" align="center"> <tr valign="top">  <td>  <table class="block mgc_cb_evo_block_chatbit" cellpadding="5" cellspacing="5" border="0"> <thead> <tr> <td class="blockheader" colspan="2" width="100%" nowrap="nowrap">10 best chatters</td> </tr> </thead> <tbody class="blockbody"> <tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  
href="tagok/6107/szotyiba">szotyibá</a></td><td class="alt1" align="center">143</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/6539/ooosuli">óÓóSULI</a></td><td class="alt1" align="center">80</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/5104/szajmoka">szajmoka</a></td><td class="alt1" align="center">79</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/4938/bullterrier07">Bullterrier07</a></td><td class="alt1" align="center">75</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/6486/jeffry">Jeffry</a></td><td class="alt1" align="center">66</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/928/coldfusion">Coldfusion</a></td><td class="alt1" align="center">52</td></
tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/6614/vacak">vacak</a></td><td class="alt1" align="center">49</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/7022/d%40nte">d@nte</a></td><td class="alt1" align="center">46</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/6669/hydromester">hydromester</a></td><td class="alt1" align="center">46</td></tr><tr class="blockrow"><td class="alt2" width="100%" align="left"><a style="text-decoration: none"  href="tagok/7424/tiktiktik">Tiktiktik</a></td><td class="alt1" align="center">40</td></tr> </tbody> <thead> <tr> <td class="blockheader" colspan="2" width="100%" nowrap="nowrap">Other stats</td> </tr> </thead> <tbody class="blockbody"> <tr class="blockrow"> <td class="alt2" width="100%" align="left" nowrap="nowrap">Chats</td> <td class="alt1" align="center" nowrap="
nowrap">1033</td> </tr> <tr class="blockrow"> <td class="alt2" width="100%" align="left" nowrap="nowrap">Last 24h chats</td> <td class="alt1" align="center" nowrap="nowrap">1033</td> </tr> <tr class="blockrow"> <td class="alt2" width="100%" align="left" nowrap="nowrap">Your chats</td> <td class="alt1" align="center" nowrap="nowrap">0</td> </tr> </tbody> </table>  <br />  <table class="block mgc_cb_evo_block_chatbit" cellpadding="5" cellspacing="5" border="0" width="100%"> <thead> <tr> <td class="blockheader" width="100%" nowrap="nowrap">Navigation</td> </tr> </thead> <tbody class="blockbody"> <tr> <td class="alt2 smallfont" width="100%"> <strong>Since:</strong><br /> <select name="channel_dlimit" id="channel_dlimit" onchange="return MGCCbEvoNS.change_archives_page();"> <option value="1" selected="selected">Yesterday</option> <option value="2" >2 days</option> <option value="7" >1 week</option> <option value="14" >2 weeks</option> <option value="30" >30 days</option> <option value="60" >60 days</option> 
<option value="90" >90 days</option> <option value="120" >120 days</option> <option value="-1" >The beginning</option> </select> <input type="button" name="dochangeview" value="Mehet" onclick="return MGCCbEvoNS.change_archives_page();" /> </td> </tr> </tbody> </table>  <br />   </td>  <td>&nbsp;&nbsp;</td>  <td width="100%">  <table class="block mgc_cb_evo_block_chatbit" cellpadding="5" cellspacing="5" border="0" width="100%" align="center"> <thead> <tr> <td class="blockheader" width="0" align="center" valign="middle">&nbsp;</td> <td class="blockheader" width="0" nowrap="nowrap"="nowrap="nowrap"" align="center" valign="middle">Dátum</td> <td class="blockheader" width="0" nowrap="nowrap"="nowrap="nowrap"" align="$stylevar[left]" valign="middle">Becenév</td> <td class="blockheader" valign="middle" width="100%" nowrap="nowrap"="nowrap="nowrap"" align="left">Chat</td> </tr> </thead> <tbody class="blockbody"><tr> <td class="alt2" width="0" id="chat_209013" align="center" valign="middle"> <div class="popupmenu" 
id="chat_209013_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209013_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/7458/bogota-rich" rel="nofollow">
                    View BOGOTA RICH's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209013" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            06/06/2013 00:39
        </span> </td> <td valign="middle" class="alt2" id="uname_209013" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/7458/bogota-rich">&lt;BOGOTA RICH&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209013" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209013" >
            kemény ez a citromos gösser
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209012" align="center" valign="middle"> <div class="popupmenu" id="chat_209012_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209012_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/7458/bogota-rich" rel="nofollow">
                    View BOGOTA RICH's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209012" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            06/06/2013 00:39
        </span> </td> <td valign="middle" class="alt2" id="uname_209012" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/7458/bogota-rich">&lt;BOGOTA RICH&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209012" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209012" >
            grrrrrrrrr besörözteeeeeeeeeeem
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209011" align="center" valign="middle"> <div class="popupmenu" id="chat_209011_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209011_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/5104/szajmoka" rel="nofollow">
                    View szajmoka's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209011" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            06/06/2013 00:15
        </span> </td> <td valign="middle" class="alt2" id="uname_209011" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/5104/szajmoka">&lt;szajmoka&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209011" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209011" > <font face="Arial Black"><a rel="nofollow" href="http://m.youtube.com/index?&amp;desktop_uri=%2F" target="_blank">http://m.youtube.com/index?&amp;desktop_uri=%2F</a></font> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209010" align="center" valign="middle"> <div class="popupmenu" id="chat_209010_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209010_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/2569/smoke2joints" rel="nofollow">
                    View smoke2joints's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209010" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 23:35
        </span> </td> <td valign="middle" class="alt2" id="uname_209010" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/2569/smoke2joints">&lt;smoke2joints&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209010" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209010" >
            miert ne tudnal?
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209009" align="center" valign="middle"> <div class="popupmenu" id="chat_209009_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209009_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6013/bigbuds" rel="nofollow">
                    View bigbuds's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209009" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 23:01
        </span> </td> <td valign="middle" class="alt2" id="uname_209009" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6013/bigbuds">&lt;bigbuds&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209009" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209009" >
            szerintetek repülön tudok kivinni vapourizert mongyuk a mobilt lotli csak gàztarjtàlyos és nem vàgom..
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209008" align="center" valign="middle"> <div class="popupmenu" id="chat_209008_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209008_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6013/bigbuds" rel="nofollow">
                    View bigbuds's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209008" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:54
        </span> </td> <td valign="middle" class="alt2" id="uname_209008" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6013/bigbuds">&lt;bigbuds&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209008" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209008" > <img src="images/smilies/116.gif" border="0" alt="" title="" class="inlineimg" /><img src="images/smilies/4204.gif" border="0" alt="" title="" class="inlineimg" /><img src="images/smilies/party.gif" border="0" alt="" title="(party)" class="inlineimg" /> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209007" align="center" valign="middle"> <div class="popupmenu" id="chat_209007_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209007_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6013/bigbuds" rel="
nofollow">
                    View bigbuds's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209007" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:54
        </span> </td> <td valign="middle" class="alt2" id="uname_209007" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6013/bigbuds">&lt;bigbuds&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209007" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209007" >
            megyek pàr hét mulva angliaba ott hajora szàlok és irany hollandia... jack herer
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209006" align="center" valign="middle"> <div class="popupmenu" id="chat_209006_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209006_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209006" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:51
        </span> </td> <td valign="middle" class="alt2" id="uname_209006" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209006" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209006" >
            de hát jó pap holtig tanul <img src="images/smilies/21.gif" border="0" alt="" title="" class="inlineimg" /> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209005" align="center" valign="middle"> <div class="popupmenu" id="chat_209005_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209005_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209005" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:51
        </span> </td> <td valign="middle" class="alt2" id="uname_209005" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209005" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209005" >
            sok a kérdés mi
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209004" align="center" valign="middle"> <div class="popupmenu" id="chat_209004_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209004_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209004" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:50
        </span> </td> <td valign="middle" class="alt2" id="uname_209004" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209004" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209004" > <img src="images/smilies/4.gif" border="0" alt="" title="" class="inlineimg" /> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209003" align="center" valign="middle"> <div class="popupmenu" id="chat_209003_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209003_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209003" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:50
        </span> </td> <td valign="middle" class="alt2" id="uname_209003" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209003" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209003" >
            :jó éjt
        </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209002" align="center" valign="middle"> <div class="popupmenu" id="chat_209002_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209002_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6107/szotyiba" rel="nofollow">
                    View szotyibá's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209002" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:50
        </span> </td> <td valign="middle" class="alt2" id="uname_209002" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6107/szotyiba">&lt;szotyibá&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209002" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209002" > <font face="Comic Sans MS"><font color="#483D8B"><font size="2"><b>jóéjt <img src="images/smilies/103.gif" border="0" alt="" title="" class="inlineimg" /></b></font></font></font> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209001" align="center" valign="middle"> <div class="popupmenu" id="chat_209001_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209001_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6107/szotyiba" rel="nofollow">
                    View szotyibá's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209001" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:50
        </span> </td> <td valign="middle" class="alt2" id="uname_209001" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6107/szotyiba">&lt;szotyibá&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209001" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209001" > <font face="Comic Sans MS"><font color="#483D8B"><font size="2"><b>de kb jó 5db-al.</b></font></font></font> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_209000" align="center" valign="middle"> <div class="popupmenu" id="chat_209000_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_209000_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/6107/szotyiba" rel="nofollow">
                    View szotyibá's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_209000" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:49
        </span> </td> <td valign="middle" class="alt2" id="uname_209000" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/6107/szotyiba">&lt;szotyibá&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_209000" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_209000" > <font face="Comic Sans MS"><font color="#483D8B"><font size="2"><b>ehhez már késő van <img src="images/smilies/4.gif" border="0" alt="" title="" class="inlineimg" /></b></font></font></font> </span> </td> </tr><tr> <td class="alt2" width="0" id="chat_208999" align="center" valign="middle"> <div class="popupmenu" id="chat_208999_menu"> <h6><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#chat_208999_menu" class="popupctrl">Actions</a></h6> <ul class="popupbody popuphover"> <li> <a href="tagok/928/coldfusion" rel="nofollow">
                    View Coldfusion's profile
                </a> </li> </ul> </div> </td> <td valign="middle" class="alt1" id="date_208999" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont">
            05/06/2013 22:47
        </span> </td> <td valign="middle" class="alt2" id="uname_208999" align="center" style="width: auto; white-space:nowrap;"> <span class="smallfont" align="left"> <a style="text-decoration: none" href="https://www.kenderforum.org/tagok/928/coldfusion">&lt;Coldfusion&gt;</a> </span> </td> <td class="alt1" valign="middle" id="text_208999" width="100%" align="left"> <span class="smallfont"  align="left" id="cspan_208999" >
            na, tehát 400w 3hét 80x80?
        </span> </td> </tr></tbody> </table>  <br /> <div style="float : left"> <div class="pagination"> <form action="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1" method="get" class="pagination popupmenu nohovermenu"> <input type="hidden" name="do" value="view_archives" /><input type="hidden" name="r" value="channel_id" /><input type="hidden" name="dlimit" value="1" /> <span><a href="javascript://" class="popupctrl">Oldal: 1 / 69</a></span> <span class="selected"><a href="javascript://" title="Eredmény: 1 - 15  (1.033) összesen">1</a></span><span><a rel="nofollow" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=2" title="Eredmények megjelenítése: 16 - 30 (1.033) összesen">2</a></span><span><a rel="nofollow" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=3" title="Eredmények megjelenítése: 31 - 45 (1.033) összesen">3</a></span><span><a rel="nofollow" 
href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=11" title="Eredmények megjelenítése: 151 - 165 (1.033) összesen">11</a></span><span><a rel="nofollow" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=51" title="Eredmények megjelenítése: 751 - 765 (1.033) összesen">51</a></span> <span class="separator">...</span> <span class="prev_next"><a rel="next" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=2" title="Következő oldal - Eredmények: 16 - 30, (1.033) összesen"><img src="images/pagination/next-right.png" alt="Következő" /></a></span> <span class="first_last"><a rel="nofollow" href="https://www.kenderforum.org/mgc_cb_evo.php?do=view_archives&amp;channel_id=0&amp;dlimit=1&amp;page=69" title="Utolsó oldal - Eredmények: 1.021 - 1.033, (1.033) összesen">Utolsó<img src="images/pagination/last-right.png" alt="Utolsó" /></a></span> <ul class="
popupbody popuphover"> <li class="formsubmit jumptopage"><label>Jump to page: <input type="text" name="page" size="4" /></label> <input type="submit" class="button" value="Mehet" /></li> </ul> </form> </div> </div> <div style="clear: both;">   <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:"Information request"' id="mgc_cb_evo_promptdialog"> <div id="mgc_cb_evo_promptdialog_content"></div> <input type="text" size="35" id="mgc_cb_evo_promptdialog_input" /> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:MGCCbEvoNS.show_promptdialog_submit">Mentés</button> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:MGCCbEvoNS.hide_promptdialog">Mégse</button> </div> </div>  <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:""' id="mgc_cb_evo_dialog"> <div id="mgc_cb_evo_dialog_content"></div> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:MGCCbEvoNS.
hide_dialog">OK</button> </div> </div>  <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:""' id="mgc_cb_evo_yesnodialog"> <div id="mgc_cb_evo_yesnodialog_content"></div> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:dojo.hitch(MGCCbEvoNS,'hide_yesnodialog_yes')">Igen</button> <button data-dojo-type="dijit.form.Button" data-dojo-props="onClick:MGCCbEvoNS.hide_yesnodialog_no">Nem</button> </div> </div>  <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:"Chatbox rules"' id="mgc_cb_evo_rules"> </div> </div>  <div class="dijitHidden"> <div data-dojo-type="dijit.Dialog" style="width:600px;" data-dojo-props='title:"MGC Chatbox Evo Help"' id="mgc_cb_evo_help"> </div> </div>  </div> </td>  </tr> </table><div align="center"><b><a rel="nofollow" href="http://www.mgcproducts.com/" title="MGC Products / Support Site">MGC Chatbox Evo</a></b> v3.2.3 by MGC &copy; 2008-2012</div>   <div style="
clear: left"> </div> <div id="footer" class="floatcontainer footer"> <form action="https://www.kenderforum.org/" method="get" id="footer_select" class="footer_select"> </form> <ul id="footer_links" class="footer_links"> <li><a href="sendmessage.php" rel="nofollow" accesskey="9">Írjál nekünk!</a></li> <li><a href="https://www.kenderforum.org">Kender Fórum</a></li> <li><a href="sitemap/">Archívum</a></li> <li><a rel="nofollow" href="mgc_cb_evo.php?do=view_archives&amp;page=1#top" onclick="document.location.hash='top'; return false;">Ugrás a tetejére</a></li> </ul> <script type="text/javascript"> <!--
        // Main vBulletin Javascript Initialization
        vBulletin_init();
    //--> </script> </div> </div>  <div class="below_body"> <div id="footer_time" class="shade footer_time">A pontos idő <span class="time">00:41</span> , a GMT +2 időzóna szerint.</div> <div id="footer_copyright" class="shade footer_copyright"> 
    Powered by vBulletin&reg;  Version 4.1.12 - Copyright &copy; 2000 - 2013, vBulletin Solutions, Inc. 

    
<br />Content Relevant URLs by <a rel="nofollow" href="http://www.vbseo.com/2352/">vBSEO</a> 3.6.0 </div> <div id="footer_morecopyright" class="shade footer_morecopyright">   </div> <script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-21499087-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script> <script type="text/javascript" src="https://www.duppy.org/clickheat/js/clickheat.js"></script><noscript><p><a rel="nofollow" href="http://www.dugwood.com/index.html">Open Source Sofware</a></p></noscript><script type="text/javascript"><!--
clickHeatSite = '';clickHeatGroup = encodeURIComponent(window.location.pathname+window.location.search);clickHeatServer = 'https://www.duppy.org/clickheat/click.php';initClickHeat(); //--> </script> </div> </body> </html>"""

soup = BeautifulSoup(samplehtml)

szoveg = soup.findAll(id=re.compile('text.'))
nev = soup.findAll(id=re.compile('uname.'))
datum = soup.findAll(id=re.compile('date.'))

for incu in range(1,10):
    #nev = unicode(nev[incu].text)
    #nev = nev[4:len(nev)-4] #konvertalni kell strbe de ugy a charset nem stimmel
    sor = datum[incu].text + ('\t') + nev[incu].text + ('\t') + szoveg[incu].text + ('\n')
    #scraperwiki.sqlite.save(data={"Datum": datum[incu].text, "Nev": nev[incu].text, "Text": szoveg[incu].text})
    scraperwiki.sqlite.save(unique_keys=["Datum"], data={"Datum":datum[incu].text, "Nev":nev[incu].text, "Text": szoveg[incu].text})