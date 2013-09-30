<?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


//print $html;
$base_url = "http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?";


$pages_to_scrape = array(

    
   "sarrera=didaktika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=didaktiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=didaskalia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=didimo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diedro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diego&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dielektriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dieresi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dierri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diese&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diese+bikoitz&sarrera=diese&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diesel&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diesel+motor&sarrera=motor++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dieta++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dieta++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dietario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dietetika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dietetiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difamatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difamatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difamazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferente&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferentzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diferentzia+egin&sarrera=diferentzia&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferentziagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferentzial&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferentziatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difraktatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difraktometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difrakzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difteria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difteriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difusio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difusometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digeritu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digestio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=digestioaparatu&sarrera=digestio&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digestiobide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=digestiohodi&sarrera=digestio&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digestore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digital&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitalina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitalizatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitalizatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitigrado&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitopuntura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diglosia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diglosiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dignatario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dignitate&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digrama&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digresio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diharu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diharudun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diharudundu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dike&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dike+lehor&sarrera=dike&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dikotiledoneo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dikotomia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dikotomiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktadore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktadura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diktadura+militar+militarren+diktadura&sarrera=diktadura&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktafono&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktaketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktamen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktatorial&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktioptero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilatatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilatazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilatometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilema&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diligentzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dilindalan&sarrera=dilin&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilinda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilindaka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dilindalan&sarrera=dilin&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilindan&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilindari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilindatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diluitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diluitzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diluzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dima&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsioanitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsioaniztun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsiobakar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsionatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diminuendo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimisio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimititu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimorfiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimorfismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dina++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dina++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dinako&sarrera=dina++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamita&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamitari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamitatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamizatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamizatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamizazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamo++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dinariar+alpeak&sarrera=alpeak&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinastia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinastiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinbidanba&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinbilidanbala&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindan&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindanboleran&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindil&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindirri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dingilizka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dingo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinosauro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diodo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diokleziano&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dionisia++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dionisia++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dionisiako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dionisio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioniso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioptria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioptrika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diorama&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diorita&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diosal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diosala+egin&sarrera=diosal&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diosaldu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioxido&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diozesi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diozesiar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diploblastiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplodoko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diploide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplokoko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diploma&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomadun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatu++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatu++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomazia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomazialari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplopia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipneo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipolar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipolo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diprotodoi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipsomania&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipsomaniako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptongatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptongazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptongo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diputatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diputatu+nagusi&sarrera=diputatu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diputatugai&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diputatutza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diputazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=foru+diputazio+diputazio+foral&sarrera=diputazio&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diputazio+probintzial&sarrera=diputazio&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdai&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdaitsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdaitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdir&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirdir+egin&sarrera=dirdir&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdira&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirdira+egin&sarrera=dirdira&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdiran&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdiratsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdiratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdirka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdizka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=direktorio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=direktorioa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=direkzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=direlako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=direnak+eta+ez+direnak+zirenak+eta+ez+zirenak&sarrera=izan++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirham&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirigismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diru&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+beltz&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+bereiziak&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+faltsu&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+handi&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+idor&sarrera=idor&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+xehe&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirua+xahutu%2Fbota&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirua+egin&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirua+xahutu%2Fbota&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruak+balio&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirualde&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirualdi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruateratze&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirubide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirubilketa&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirudienez&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirudun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruetxe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirugose&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruitzultze&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirukoi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirulaguntza&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirulari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirumin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirupaper&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirupatroi&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirusari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirusarrera&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirusartze&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirutan&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirutegi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirutsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirutu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirutza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruz&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzain&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzaintza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzale&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzalekeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzaletasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzaletu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzantza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruzorro&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruzuriketa&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disartria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=discjockey&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diseinatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diseinu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diseinugile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disekatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disekzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disekzionatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disenteria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disenteriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disfasia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disfonia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disfuntzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgenesia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgrafia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgregatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgregazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgustu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disidente&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disidentzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disidu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimetria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimetriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimilatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimilazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimulatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimulazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimulu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disimuluan&sarrera=disimulu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disjuntibo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disjuntore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disjuntu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disjuntzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diska&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskalkulia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskete&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disketeunitate&sarrera=diskete&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disko++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+digital+balioaniztun&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+finko%2Fgogor&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+finko%2Fgogor&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+konpaktu%2Ftrinko&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+malgu&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+optiko&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+konpaktu%2Ftrinko&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diskobalazta&sarrera=balazta&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskobolo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diskodenda&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskoetxe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskografia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskografiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diskojaurtiketa&sarrera=jaurtiketa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diskojogailu&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskordantzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskordia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskoteka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskretu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskrezio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskriminatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskriminatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskriminazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskromatopsia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskromia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskurtso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislalia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislexia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislexiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislokatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislokazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dismutazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disnea&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbaezin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbaezintasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbagaitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbagarritasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disoluzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disoluzio+indargetzaile&sarrera=indargetzaile&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disonante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disonantzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disoziatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disoziazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disparate&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispentsa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispentsatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispepsia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispeptiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=displasia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disposatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispositibo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disposizio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disprosio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disputa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disputan&sarrera=disputa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disputatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disruptibo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distantzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distantzia+fokal&sarrera=fokal&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distantzia+fokal+fokudistantzia&sarrera=distantzia&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distantziakide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distantziakidetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distentsio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distilatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distira&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distira+egin&sarrera=distira&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiradura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distiraemaile&sarrera=distira&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiragailu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiragarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distirant&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distirarazteko+makina&sarrera=distiratu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiratsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiratzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distortsio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distortsionatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distraitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distrazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distributibo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distribuzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distrofia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disuasio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disziplina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditare&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diteismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diteista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diti&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditiranbo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditisko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxadun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxagabe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxo++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxo++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=ditxoan+egon&sarrera=ditxo++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=ditxoankila&sarrera=ditxo++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxoka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxolari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxoso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxosozko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diuresi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diuresikontrako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diuretiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=divertimento&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=divo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dixidari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dixidatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dixidu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dixieland&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizdiz++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizdiz++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dizdiz+egin&sarrera=dizdiz++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizdizari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizdizka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizigotiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diziplina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diziplina+jarri%2Fezarri&sarrera=diziplina&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diziplina+jarri%2Fezarri&sarrera=diziplina&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diziplinatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diziplinazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizipulu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=djibuti&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=djibutiar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dna&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=do&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doakotasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doan&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doarik&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doarikako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobatxakur&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobela&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobera&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doberman&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobla&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doblatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doble&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobloi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekaedriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekaedro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekafonia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekafoniko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekafonismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekafonista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekagono&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekasilabiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dofin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dofinerria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogma&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatikoki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatizatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohain&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaindu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaingaitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaingile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohainik&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohainikako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaintasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaintza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabeki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabetu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakaitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsuera&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsuki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsutasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsutu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doi+bat&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doi+izan&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doidoia&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doidoia&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doidoian&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doietsi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doiki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doikuntza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doikuntzak+egite&sarrera=doikuntza&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilor&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilorkeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilorki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilorkume&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilortasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilortu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doinu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doinupean&sarrera=doinu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doipuru&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doiritzi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doitasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doitasunezko+zorrozketa&sarrera=zorrozketa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doitzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokedokeka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktoratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktoregai&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktorego&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktoretza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktrina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktrinamendu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktrinario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktrinatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumental&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumentalista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumentatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumentazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumentu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolamen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolare&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doldabelar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolikozefalia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolikozefalo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolmen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolomia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolomita&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolomitak&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolomitiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doloratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doloretsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolorezki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doloros&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doloroski&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dolu+egin&sarrera=dolu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dolu+izan&sarrera=dolu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dolua+ekarri&sarrera=dolu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolugarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolukor&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolumen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolumin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolutu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dom&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domaia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domeinu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domeka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dome%F1u&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domi+santore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominene&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domingotar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominikar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominikar+errepublika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doministiku&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doministiku+egin&sarrera=doministiku&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domino&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domiziano&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domu+santuru&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domu+santuru&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=domuru+santu+egun&sarrera=santu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dona&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donabera&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donado&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donadotasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donamaria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donausle&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donauste&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donautsi++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donautsi++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=done&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=done+jakueren+bidea&sarrera=jakue&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=done+jakueren+bidea&sarrera=jakue&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donejakue+compostelako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donejakue+compostelako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donemiliaga&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donetsi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donetu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donetzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doneztebe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doneztebeiguzkitza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dongaro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donge&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dongekeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dongetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dongetu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donibane&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donibane+lohizune&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donibanegarazi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donibanezuhaitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donkitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donoki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donostia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donostiar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dontsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dontsutasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dontzeila&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dontzeilatasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dopaketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dopamina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dopatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dopin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorada&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dordoina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doriar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doriar+ordena&sarrera=ordena&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornadura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornagailu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornailu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornaku&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorotea&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doroteo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpeki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpetu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpezia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorrao&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorre&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dorreak+egin&sarrera=dorre&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorreelortzibar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dorrehortz&sarrera=dorre&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorretxe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorretxo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dorretxori&sarrera=dorre&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dortoka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dortsal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosier&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosifikagailu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosifikatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosifikatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosifikazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosimetria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dostatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosteta&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dote&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotezale&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotoregarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotoreria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotoretasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotoretu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotorezia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotrina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=douglas+izei&sarrera=izei&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dozena&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dozenaerdi&sarrera=dozena&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dozenaka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dozenan+hamahiru&sarrera=dozena&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dra&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=draga&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dragatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dragatze&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drago&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dragoi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dragoimutur&sarrera=dragoi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dragoitxo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=draia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=draiada&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drain&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drainatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drainatze&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drakma&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drakoniar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drama&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramagile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramagintza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramatiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramatizatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramatizazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramaturgia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramaturgo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drastiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drenaje&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drenatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dretxo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drezatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=driblatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dribling&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drill&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drindots&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dringilidrangala&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drive&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=driza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=droga&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=droga+atera&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=droga+egin&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=drogamendekotasun&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=drogatrafikatzaile&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=drogatrafiko&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogazale&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogazaletasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogoso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drolekeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dromedario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drop&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drosera&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=droserazeo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drosofila&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drugstore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=druida&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=druidismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drungundrungun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drupa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drusa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=druso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dual&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dualismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dualista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dubaler&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dubel&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dublin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=duda+egin&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudarik+gabe&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudagabe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudagabeko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudaldi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudamuda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudamudazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudamudatan&sarrera=dudamuda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudamudatan&sarrera=dudamuda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudamudazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudatan&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudaperpaus&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudarik+gabe&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudatan&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudatsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duelu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dueluan+ari+izan%2Fhartu&sarrera=duelu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dueluan+ari+izan%2Fhartu&sarrera=duelu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dugong&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duhulate&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duindu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=duineko&sarrera=duin&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duinez&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duineztasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duintasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dukat&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duke&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dukerri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dukesa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duketza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dulabre&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dulantzi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dulcinea&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dultzaina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dultzainero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duma&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dumdum&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dumping&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duna&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunba&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunbada&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunbal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dunbaljotzaile&sarrera=dunbal&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunbots&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dundu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dungulu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duntu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duodenal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duodeno&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duopolio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dupa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dupel&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duple&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duplex&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duralex&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duraluminio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duramater&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durango&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durbante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durditu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdoi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=durdoi+ahotxiki&sarrera=durdoi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=durdoi+handi&sarrera=durdoi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=durdoi+txilibitu&sarrera=durdoi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdula&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdurika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdurikatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdurio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durduza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durduzadura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durduzatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durer&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durruma+donemiliaga&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durruma+kanpezu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durunda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durundatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durundi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durunditsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=d%FCsseldorf&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dutxa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dutxaitxitura&sarrera=dutxa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dutxatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dutxulu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dutzulokeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dux&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dvandva&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dvd&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" 
);


foreach($pages_to_scrape as $page){

    $html = scraperwiki::scrape($base_url.$page);
    $sections_dom = new simple_html_dom();
    $sections_dom->load($html);
    $datah2X='';
     foreach($sections_dom->find('h2 span.azpisarrera') as $datah2)
    {       
        $datah2X=utf8_encode($datah2->plaintext);
        print "h2: ".$datah2X. "\n";

    } 
    if (!isset($datah2X) || $datah2X==''){
     foreach($sections_dom->find('h1 span') as $datah2)
        {   
            $datah2X=utf8_encode($datah2->plaintext);
            print "h1: ".$datah2X. "\n";

        } 
    } 
    
    $alldata='';
    $i=0;
    $arraydom = $sections_dom->find('dt.ordaina strong');

    foreach($arraydom  as $data){
        $sep="|";
        if($i == count($arraydom )-1){
            $sep="";
        }
        
        $alldata .= utf8_encode($data->plaintext). $sep;
        $i++;
    }
    print "data: ".$alldata. "\n----------------\n";

           $entry['Term'] = $datah2X;
           $entry['Definition'] = $alldata;
           scraperwiki::save(array('Definition'), $entry);
            
}

?><?php
######################################
# Basic PHP scraper
######################################

require  'scraperwiki/simple_html_dom.php';


//print $html;
$base_url = "http://www.euskara.euskadi.net/r59-15172x/eu/hizt_el/emaitza.asp?";


$pages_to_scrape = array(

    
   "sarrera=didaktika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=didaktiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=didaskalia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=didimo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diedro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diego&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dielektriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dieresi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dierri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diese&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diese+bikoitz&sarrera=diese&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diesel&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diesel+motor&sarrera=motor++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dieta++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dieta++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dietario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dietetika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dietetiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difamatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difamatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difamazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferente&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferentzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diferentzia+egin&sarrera=diferentzia&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferentziagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferentzial&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diferentziatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difraktatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difraktometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difrakzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difteria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difteriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difusio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=difusometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digeritu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digestio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=digestioaparatu&sarrera=digestio&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digestiobide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=digestiohodi&sarrera=digestio&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digestore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digital&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitalina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitalizatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitalizatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitigrado&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitopuntura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diglosia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diglosiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dignatario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dignitate&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digrama&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=digresio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diharu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diharudun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diharudundu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dike&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dike+lehor&sarrera=dike&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dikotiledoneo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dikotomia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dikotomiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktadore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktadura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diktadura+militar+militarren+diktadura&sarrera=diktadura&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktafono&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktaketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktamen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktatorial&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diktioptero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilatatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilatazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilatometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilema&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diligentzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dilindalan&sarrera=dilin&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilinda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilindaka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dilindalan&sarrera=dilin&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilindan&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilindari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilindatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dilista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diluitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diluitzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diluzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dima&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsioanitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsioaniztun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsiobakar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimentsionatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diminuendo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimisio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimititu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimorfiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimorfismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dimu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dina++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dina++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dinako&sarrera=dina++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamita&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamitari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamitatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamizatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamizatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamizazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamo++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinamometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dinariar+alpeak&sarrera=alpeak&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinastia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinastiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinbidanba&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinbilidanbala&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindan&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindanboleran&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindil&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dindirri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dingilizka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dingo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dinosauro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diodo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diokleziano&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dionisia++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dionisia++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dionisiako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dionisio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioniso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioptria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioptrika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diorama&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diorita&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diosal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diosala+egin&sarrera=diosal&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diosaldu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dioxido&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diozesi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diozesiar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diploblastiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplodoko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diploide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplokoko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diploma&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomadun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatu++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatu++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomatura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomazia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplomazialari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diplopia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipneo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipolar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipolo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diprotodoi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipsomania&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dipsomaniako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptongatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptongazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diptongo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diputatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diputatu+nagusi&sarrera=diputatu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diputatugai&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diputatutza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diputazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=foru+diputazio+diputazio+foral&sarrera=diputazio&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diputazio+probintzial&sarrera=diputazio&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdai&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdaitsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdaitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdir&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirdir+egin&sarrera=dirdir&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdira&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirdira+egin&sarrera=dirdira&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdiran&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdiratsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdiratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdirka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirdizka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=direktorio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=direktorioa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=direkzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=direlako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=direnak+eta+ez+direnak+zirenak+eta+ez+zirenak&sarrera=izan++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirham&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirigismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diru&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+beltz&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+bereiziak&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+faltsu&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+handi&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+idor&sarrera=idor&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diru+xehe&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirua+xahutu%2Fbota&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirua+egin&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirua+xahutu%2Fbota&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruak+balio&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirualde&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirualdi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruateratze&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirubide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirubilketa&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirudienez&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirudun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruetxe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirugose&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruitzultze&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirukoi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirulaguntza&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirulari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirumin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirupaper&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirupatroi&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirusari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirusarrera&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirusartze&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dirutan&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirutegi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirutsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirutu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dirutza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruz&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzain&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzaintza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzale&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzalekeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzaletasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzaletu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diruzantza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruzorro&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diruzuriketa&sarrera=diru&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disartria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=discjockey&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diseinatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diseinu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diseinugile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disekatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disekzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disekzionatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disenteria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disenteriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disfasia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disfonia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disfuntzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgenesia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgrafia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgregatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgregazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disgustu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disidente&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disidentzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disidu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimetria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimetriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimilatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimilazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimulatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimulazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disimulu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disimuluan&sarrera=disimulu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disjuntibo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disjuntore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disjuntu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disjuntzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diska&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskalkulia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskete&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disketeunitate&sarrera=diskete&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disko++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+digital+balioaniztun&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+finko%2Fgogor&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+finko%2Fgogor&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+konpaktu%2Ftrinko&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+malgu&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+optiko&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disko+konpaktu%2Ftrinko&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diskobalazta&sarrera=balazta&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskobolo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diskodenda&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskoetxe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskografia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskografiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diskojaurtiketa&sarrera=jaurtiketa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diskojogailu&sarrera=disko++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskordantzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskordia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskoteka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskretu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskrezio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskriminatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskriminatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskriminazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskromatopsia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskromia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diskurtso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislalia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislexia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislexiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislokatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dislokazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dismutazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disnea&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbaezin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbaezintasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbagaitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbagarritasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disolbatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disoluzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disoluzio+indargetzaile&sarrera=indargetzaile&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disonante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disonantzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disoziatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disoziazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disparate&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispentsa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispentsatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispepsia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispeptiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=displasia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disposatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dispositibo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disposizio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disprosio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disputa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=disputan&sarrera=disputa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disputatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disruptibo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distantzia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distantzia+fokal&sarrera=fokal&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distantzia+fokal+fokudistantzia&sarrera=distantzia&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distantziakide&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distantziakidetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distentsio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distilatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distira&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distira+egin&sarrera=distira&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiradura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distiraemaile&sarrera=distira&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiragailu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiragarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distirant&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=distirarazteko+makina&sarrera=distiratu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiratsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distiratzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distortsio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distortsionatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distraitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distrazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distributibo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distribuzio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=distrofia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disuasio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=disziplina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditare&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diteismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diteista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diti&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditiranbo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditisko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxadun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxagabe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxo++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxo++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=ditxoan+egon&sarrera=ditxo++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=ditxoankila&sarrera=ditxo++2&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxoka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxolari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxoso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=ditxosozko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diuresi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diuresikontrako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diuretiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=divertimento&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=divo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dixidari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dixidatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dixidu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dixieland&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizdiz++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizdiz++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dizdiz+egin&sarrera=dizdiz++1&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizdizari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizdizka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizigotiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diziplina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diziplina+jarri%2Fezarri&sarrera=diziplina&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=diziplina+jarri%2Fezarri&sarrera=diziplina&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diziplinatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=diziplinazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dizipulu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=djibuti&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=djibutiar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dna&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=do&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doakotasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doan&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doarik&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doarikako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobatxakur&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobela&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobera&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doberman&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobla&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doblatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doble&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dobloi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekaedriko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekaedro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekafonia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekafoniko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekafonismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekafonista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekagono&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodekasilabiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dodo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dofin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dofinerria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogma&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatikoki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dogmatizatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohain&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaindu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaingaitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaingile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohainik&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohainikako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaintasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohaintza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabeki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakabetu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohakaitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsuera&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsuki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsutasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatsutu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dohatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doi+bat&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doi+izan&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doidoia&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doidoia&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doidoian&sarrera=doi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doietsi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doiki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doikuntza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doikuntzak+egite&sarrera=doikuntza&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilor&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilorkeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilorki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilorkume&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilortasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doilortu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doinu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doinupean&sarrera=doinu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doipuru&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doiritzi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doitasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doitasunezko+zorrozketa&sarrera=zorrozketa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doitzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokedokeka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktoratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktoregai&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktorego&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktoretza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktrina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktrinamendu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktrinario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doktrinatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumental&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumentalista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumentatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumentazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dokumentu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolamen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolare&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doldabelar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolikozefalia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolikozefalo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolmen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolomia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolomita&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolomitak&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolomitiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doloratu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doloretsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolorezki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doloros&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doloroski&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dolu+egin&sarrera=dolu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dolu+izan&sarrera=dolu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dolua+ekarri&sarrera=dolu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolugarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolukor&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolumen&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolumin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dolutu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dom&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domaia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domeinu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domeka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dome%F1u&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domi+santore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominene&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domingotar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominikar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dominikar+errepublika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doministiku&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doministiku+egin&sarrera=doministiku&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domino&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domiziano&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domu+santuru&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=domu+santuru&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=domuru+santu+egun&sarrera=santu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dona&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donabera&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donado&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donadotasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donamaria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donari&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donausle&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donauste&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donautsi++1&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donautsi++2&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=done&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=done+jakueren+bidea&sarrera=jakue&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=done+jakueren+bidea&sarrera=jakue&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donejakue+compostelako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donejakue+compostelako&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donemiliaga&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donetsi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donetu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donetzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doneztebe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doneztebeiguzkitza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dongaro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donge&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dongekeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dongetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dongetu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donibane&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donibane+lohizune&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donibanegarazi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donibanezuhaitz&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donkitu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donoki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donostia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donostiar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dontsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dontsutasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dontzeila&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dontzeilatasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=donu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dopaketa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dopamina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dopatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dopin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorada&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dordoina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doriar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=doriar+ordena&sarrera=ordena&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornadura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornagailu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornailu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornaku&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dornatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorotea&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=doroteo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpeki&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpetasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpetu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorpezia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorrao&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorre&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dorreak+egin&sarrera=dorre&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorreelortzibar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dorrehortz&sarrera=dorre&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorretxe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dorretxo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dorretxori&sarrera=dorre&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dortoka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dortsal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosier&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosifikagailu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosifikatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosifikatzaile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosifikazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosimetria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dostatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dosteta&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dote&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotezale&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotoregarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotoreria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotoretasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotoretu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotorezia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dotrina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=douglas+izei&sarrera=izei&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dozena&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dozenaerdi&sarrera=dozena&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dozenaka&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dozenan+hamahiru&sarrera=dozena&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dra&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=draga&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dragatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dragatze&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drago&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dragoi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dragoimutur&sarrera=dragoi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dragoitxo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=draia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=draiada&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drain&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drainatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drainatze&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drakma&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drakoniar&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drama&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramagile&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramagintza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramatiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramatizatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramatizazio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramaturgia&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dramaturgo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drastiko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drenaje&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drenatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dretxo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drezatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=driblatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dribling&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drill&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drindots&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dringilidrangala&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drive&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=driza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=droga&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=droga+atera&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=droga+egin&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=drogamendekotasun&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=drogatrafikatzaile&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=drogatrafiko&sarrera=droga&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogazale&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogazaletasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drogoso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drolekeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dromedario&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drop&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drosera&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=droserazeo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drosofila&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drugstore&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=druida&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=druidismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drungundrungun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drupa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=drusa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=druso&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dual&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dualismo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dualista&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dubaler&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dubel&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dublin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=duda+egin&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudarik+gabe&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudagabe&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudagabeko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudagarri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudaldi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudamuda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudamudazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudamudatan&sarrera=dudamuda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudamudatan&sarrera=dudamuda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudamudazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudatan&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudaperpaus&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudarik+gabe&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dudatan&sarrera=duda&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudatsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dudazko&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duelu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dueluan+ari+izan%2Fhartu&sarrera=duelu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dueluan+ari+izan%2Fhartu&sarrera=duelu&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dugong&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duhulate&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duin&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duindu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=duineko&sarrera=duin&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duinez&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duineztasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duintasun&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dukat&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duke&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dukerri&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dukesa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duketza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dulabre&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dulantzi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dulcinea&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dultzaina&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dultzainero&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duma&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dumdum&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dumping&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duna&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunba&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunbada&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunbal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dunbaljotzaile&sarrera=dunbal&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunbots&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dunda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dundu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dungulu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duntu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duo&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duodenal&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duodeno&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duopolio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dupa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dupel&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duple&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duplex&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duralex&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duraluminio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duramater&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durango&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durbante&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durditu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdoi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=durdoi+ahotxiki&sarrera=durdoi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=durdoi+handi&sarrera=durdoi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=durdoi+txilibitu&sarrera=durdoi&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdula&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdurika&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdurikatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durdurio&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durduza&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durduzadura&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durduzatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durer&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=duro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durometro&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durruma+donemiliaga&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durruma+kanpezu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durunda&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durundatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durundi&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=durunditsu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=d%FCsseldorf&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dutxa&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "azpisar=dutxaitxitura&sarrera=dutxa&mota=azpisarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dutxatu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dutxulu&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dutzulokeria&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dux&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dvandva&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" , 
    
    "sarrera=dvd&mota=sarrera&term_hizkuntza=E&aplik_hizkuntza=" 
);


foreach($pages_to_scrape as $page){

    $html = scraperwiki::scrape($base_url.$page);
    $sections_dom = new simple_html_dom();
    $sections_dom->load($html);
    $datah2X='';
     foreach($sections_dom->find('h2 span.azpisarrera') as $datah2)
    {       
        $datah2X=utf8_encode($datah2->plaintext);
        print "h2: ".$datah2X. "\n";

    } 
    if (!isset($datah2X) || $datah2X==''){
     foreach($sections_dom->find('h1 span') as $datah2)
        {   
            $datah2X=utf8_encode($datah2->plaintext);
            print "h1: ".$datah2X. "\n";

        } 
    } 
    
    $alldata='';
    $i=0;
    $arraydom = $sections_dom->find('dt.ordaina strong');

    foreach($arraydom  as $data){
        $sep="|";
        if($i == count($arraydom )-1){
            $sep="";
        }
        
        $alldata .= utf8_encode($data->plaintext). $sep;
        $i++;
    }
    print "data: ".$alldata. "\n----------------\n";

           $entry['Term'] = $datah2X;
           $entry['Definition'] = $alldata;
           scraperwiki::save(array('Definition'), $entry);
            
}

?>