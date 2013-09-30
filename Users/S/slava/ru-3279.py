import scraperwiki
import lxml.html
import httplib
import cookielib
import urllib2
import urllib
import re
# Blank Python

urls="""http://www.trust.ru/contact/index.php?regions=3739
http://www.trust.ru/contact/index.php?regions=3858
http://www.trust.ru/contact/index.php?regions=3742
http://www.trust.ru/contact/index.php?regions=42678
http://www.trust.ru/contact/index.php?regions=3743
http://www.trust.ru/contact/index.php?regions=3744
http://www.trust.ru/contact/index.php?regions=4614454
http://www.trust.ru/contact/index.php?regions=3745
http://www.trust.ru/contact/index.php?regions=3746
http://www.trust.ru/contact/index.php?regions=3747
http://www.trust.ru/contact/index.php?regions=3748
http://www.trust.ru/contact/index.php?regions=3749
http://www.trust.ru/contact/index.php?regions=3750
http://www.trust.ru/contact/index.php?regions=3751
http://www.trust.ru/contact/index.php?regions=3752
http://www.trust.ru/contact/index.php?regions=3753
http://www.trust.ru/contact/index.php?regions=3754
http://www.trust.ru/contact/index.php?regions=3755
http://www.trust.ru/contact/index.php?regions=3756
http://www.trust.ru/contact/index.php?regions=3757
http://www.trust.ru/contact/index.php?regions=21118
http://www.trust.ru/contact/index.php?regions=3759
http://www.trust.ru/contact/index.php?regions=53881
http://www.trust.ru/contact/index.php?regions=berdsk
http://www.trust.ru/contact/index.php?regions=3761
http://www.trust.ru/contact/index.php?regions=3762
http://www.trust.ru/contact/index.php?regions=14670
http://www.trust.ru/contact/index.php?regions=bogoroditsk
http://www.trust.ru/contact/index.php?regions=13517
http://www.trust.ru/contact/index.php?regions=26178
http://www.trust.ru/contact/index.php?regions=bronnitsy
http://www.trust.ru/contact/index.php?regions=3763
http://www.trust.ru/contact/index.php?regions=buzuluk
http://www.trust.ru/contact/index.php?regions=13631
http://www.trust.ru/contact/index.php?regions=pyshma
http://www.trust.ru/contact/index.php?regions=55302
http://www.trust.ru/contact/index.php?regions=5667
http://www.trust.ru/contact/index.php?regions=3741
http://www.trust.ru/contact/index.php?regions=3764
http://www.trust.ru/contact/index.php?regions=3765
http://www.trust.ru/contact/index.php?regions=3766
http://www.trust.ru/contact/index.php?regions=volgorechensk
http://www.trust.ru/contact/index.php?regions=3767
http://www.trust.ru/contact/index.php?regions=3768
http://www.trust.ru/contact/index.php?regions=54557
http://www.trust.ru/contact/index.php?regions=52593
http://www.trust.ru/contact/index.php?regions=3740
http://www.trust.ru/contact/index.php?regions=3769
http://www.trust.ru/contact/index.php?regions=49245
http://www.trust.ru/contact/index.php?regions=3770
http://www.trust.ru/contact/index.php?regions=52505
http://www.trust.ru/contact/index.php?regions=gay
http://www.trust.ru/contact/index.php?regions=21458
http://www.trust.ru/contact/index.php?regions=36150
http://www.trust.ru/contact/index.php?regions=3771
http://www.trust.ru/contact/index.php?regions=3772
http://www.trust.ru/contact/index.php?regions=12619
http://www.trust.ru/contact/index.php?regions=49358
http://www.trust.ru/contact/index.php?regions=3774
http://www.trust.ru/contact/index.php?regions=dzerzhinskiy
http://www.trust.ru/contact/index.php?regions=3775
http://www.trust.ru/contact/index.php?regions=3776
http://www.trust.ru/contact/index.php?regions=dubovoe
http://www.trust.ru/contact/index.php?regions=3777
http://www.trust.ru/contact/index.php?regions=3778
http://www.trust.ru/contact/index.php?regions=3779
http://www.trust.ru/contact/index.php?regions=3780
http://www.trust.ru/contact/index.php?regions=3806
http://www.trust.ru/contact/index.php?regions=25662
http://www.trust.ru/contact/index.php?regions=zhigulevsk
http://www.trust.ru/contact/index.php?regions=3781
http://www.trust.ru/contact/index.php?regions=49321
http://www.trust.ru/contact/index.php?regions=3782
http://www.trust.ru/contact/index.php?regions=5173
http://www.trust.ru/contact/index.php?regions=3783
http://www.trust.ru/contact/index.php?regions=3784
http://www.trust.ru/contact/index.php?regions=57427
http://www.trust.ru/contact/index.php?regions=inza
http://www.trust.ru/contact/index.php?regions=3786
http://www.trust.ru/contact/index.php?regions=3787
http://www.trust.ru/contact/index.php?regions=3785
http://www.trust.ru/contact/index.php?regions=3788
http://www.trust.ru/contact/index.php?regions=3789
http://www.trust.ru/contact/index.php?regions=3790
http://www.trust.ru/contact/index.php?regions=71031
http://www.trust.ru/contact/index.php?regions=kamenolomni
http://www.trust.ru/contact/index.php?regions=3791
http://www.trust.ru/contact/index.php?regions=3792
http://www.trust.ru/contact/index.php?regions=karachev
http://www.trust.ru/contact/index.php?regions=14684
http://www.trust.ru/contact/index.php?regions=14685
http://www.trust.ru/contact/index.php?regions=kineshma
http://www.trust.ru/contact/index.php?regions=3794
http://www.trust.ru/contact/index.php?regions=kiselevsk
http://www.trust.ru/contact/index.php?regions=3795
http://www.trust.ru/contact/index.php?regions=54574
http://www.trust.ru/contact/index.php?regions=3796
http://www.trust.ru/contact/index.php?regions=3911
http://www.trust.ru/contact/index.php?regions=3797
http://www.trust.ru/contact/index.php?regions=kolpino
http://www.trust.ru/contact/index.php?regions=52514
http://www.trust.ru/contact/index.php?regions=3798
http://www.trust.ru/contact/index.php?regions=3799
http://www.trust.ru/contact/index.php?regions=3800
http://www.trust.ru/contact/index.php?regions=233646
http://www.trust.ru/contact/index.php?regions=3801
http://www.trust.ru/contact/index.php?regions=37566
http://www.trust.ru/contact/index.php?regions=54548
http://www.trust.ru/contact/index.php?regions=3802
http://www.trust.ru/contact/index.php?regions=14692
http://www.trust.ru/contact/index.php?regions=kronshtadt
http://www.trust.ru/contact/index.php?regions=14693
http://www.trust.ru/contact/index.php?regions=3803
http://www.trust.ru/contact/index.php?regions=3804
http://www.trust.ru/contact/index.php?regions=49371
http://www.trust.ru/contact/index.php?regions=3805
http://www.trust.ru/contact/index.php?regions=kurchatov
http://www.trust.ru/contact/index.php?regions=labinsk
http://www.trust.ru/contact/index.php?regions=3807
http://www.trust.ru/contact/index.php?regions=52464
http://www.trust.ru/contact/index.php?regions=3808
http://www.trust.ru/contact/index.php?regions=3809
http://www.trust.ru/contact/index.php?regions=19876
http://www.trust.ru/contact/index.php?regions=lobnya
http://www.trust.ru/contact/index.php?regions=3811
http://www.trust.ru/contact/index.php?regions=3812
http://www.trust.ru/contact/index.php?regions=3813
http://www.trust.ru/contact/index.php?regions=21809
http://www.trust.ru/contact/index.php?regions=3814
http://www.trust.ru/contact/index.php?regions=3815
http://www.trust.ru/contact/index.php?regions=32881
http://www.trust.ru/contact/index.php?regions=21506
http://www.trust.ru/contact/index.php?regions=mednogorsk
http://www.trust.ru/contact/index.php?regions=3816
http://www.trust.ru/contact/index.php?regions=3818
http://www.trust.ru/contact/index.php?regions=13529
http://www.trust.ru/contact/index.php?regions=3465
http://www.trust.ru/contact/index.php?regions=3819
http://www.trust.ru/contact/index.php?regions=3820
http://www.trust.ru/contact/index.php?regions=54551
http://www.trust.ru/contact/index.php?regions=3821
http://www.trust.ru/contact/index.php?regions=32883
http://www.trust.ru/contact/index.php?regions=3822
http://www.trust.ru/contact/index.php?regions=mtsensk
http://www.trust.ru/contact/index.php?regions=3823
http://www.trust.ru/contact/index.php?regions=3824
http://www.trust.ru/contact/index.php?regions=3825
http://www.trust.ru/contact/index.php?regions=3826
http://www.trust.ru/contact/index.php?regions=3827
http://www.trust.ru/contact/index.php?regions=14704
http://www.trust.ru/contact/index.php?regions=3828
http://www.trust.ru/contact/index.php?regions=14706
http://www.trust.ru/contact/index.php?regions=3829
http://www.trust.ru/contact/index.php?regions=3830
http://www.trust.ru/contact/index.php?regions=3831
http://www.trust.ru/contact/index.php?regions=426728
http://www.trust.ru/contact/index.php?regions=49382
http://www.trust.ru/contact/index.php?regions=novokubansk
http://www.trust.ru/contact/index.php?regions=3832
http://www.trust.ru/contact/index.php?regions=novopavlovsk
http://www.trust.ru/contact/index.php?regions=3834
http://www.trust.ru/contact/index.php?regions=3835
http://www.trust.ru/contact/index.php?regions=32884
http://www.trust.ru/contact/index.php?regions=3837
http://www.trust.ru/contact/index.php?regions=49408
http://www.trust.ru/contact/index.php?regions=23556
http://www.trust.ru/contact/index.php?regions=14714
http://www.trust.ru/contact/index.php?regions=3838
http://www.trust.ru/contact/index.php?regions=3839
http://www.trust.ru/contact/index.php?regions=3840
http://www.trust.ru/contact/index.php?regions=3841
http://www.trust.ru/contact/index.php?regions=osinovaya_gora
http://www.trust.ru/contact/index.php?regions=14716
http://www.trust.ru/contact/index.php?regions=3842
http://www.trust.ru/contact/index.php?regions=3843
http://www.trust.ru/contact/index.php?regions=3844
http://www.trust.ru/contact/index.php?regions=32887
http://www.trust.ru/contact/index.php?regions=3845
http://www.trust.ru/contact/index.php?regions=251789
http://www.trust.ru/contact/index.php?regions=3846
http://www.trust.ru/contact/index.php?regions=3847
http://www.trust.ru/contact/index.php?regions=poykovskiy
http://www.trust.ru/contact/index.php?regions=49362
http://www.trust.ru/contact/index.php?regions=21813
http://www.trust.ru/contact/index.php?regions=14719
http://www.trust.ru/contact/index.php?regions=13582
http://www.trust.ru/contact/index.php?regions=54591
http://www.trust.ru/contact/index.php?regions=3848
http://www.trust.ru/contact/index.php?regions=3849
http://www.trust.ru/contact/index.php?regions=13670
http://www.trust.ru/contact/index.php?regions=3851
http://www.trust.ru/contact/index.php?regions=3852
http://www.trust.ru/contact/index.php?regions=3853
http://www.trust.ru/contact/index.php?regions=3854
http://www.trust.ru/contact/index.php?regions=3855
http://www.trust.ru/contact/index.php?regions=13700
http://www.trust.ru/contact/index.php?regions=3856
http://www.trust.ru/contact/index.php?regions=3857
http://www.trust.ru/contact/index.php?regions=126772
http://www.trust.ru/contact/index.php?regions=saransk
http://www.trust.ru/contact/index.php?regions=3859
http://www.trust.ru/contact/index.php?regions=svetlograd
http://www.trust.ru/contact/index.php?regions=3860
http://www.trust.ru/contact/index.php?regions=13566
http://www.trust.ru/contact/index.php?regions=3862
http://www.trust.ru/contact/index.php?regions=14728
http://www.trust.ru/contact/index.php?regions=slavyansk_na_kubani
http://www.trust.ru/contact/index.php?regions=3863
http://www.trust.ru/contact/index.php?regions=1213097
http://www.trust.ru/contact/index.php?regions=3865
http://www.trust.ru/contact/index.php?regions=3866
http://www.trust.ru/contact/index.php?regions=3867
http://www.trust.ru/contact/index.php?regions=32888
http://www.trust.ru/contact/index.php?regions=3868
http://www.trust.ru/contact/index.php?regions=14731
http://www.trust.ru/contact/index.php?regions=14732
http://www.trust.ru/contact/index.php?regions=3869
http://www.trust.ru/contact/index.php?regions=3870
http://www.trust.ru/contact/index.php?regions=3871
http://www.trust.ru/contact/index.php?regions=3872
http://www.trust.ru/contact/index.php?regions=3873
http://www.trust.ru/contact/index.php?regions=teykovo
http://www.trust.ru/contact/index.php?regions=temryuk
http://www.trust.ru/contact/index.php?regions=32890
http://www.trust.ru/contact/index.php?regions=3874
http://www.trust.ru/contact/index.php?regions=3875
http://www.trust.ru/contact/index.php?regions=3876
http://www.trust.ru/contact/index.php?regions=3877
http://www.trust.ru/contact/index.php?regions=54554
http://www.trust.ru/contact/index.php?regions=3878
http://www.trust.ru/contact/index.php?regions=3879
http://www.trust.ru/contact/index.php?regions=3880
http://www.trust.ru/contact/index.php?regions=3881
http://www.trust.ru/contact/index.php?regions=3882
http://www.trust.ru/contact/index.php?regions=21790
http://www.trust.ru/contact/index.php?regions=14742
http://www.trust.ru/contact/index.php?regions=3883
http://www.trust.ru/contact/index.php?regions=3884
http://www.trust.ru/contact/index.php?regions=3885
http://www.trust.ru/contact/index.php?regions=3886
http://www.trust.ru/contact/index.php?regions=3887
http://www.trust.ru/contact/index.php?regions=33297
http://www.trust.ru/contact/index.php?regions=14748
http://www.trust.ru/contact/index.php?regions=chaplygin
http://www.trust.ru/contact/index.php?regions=3888
http://www.trust.ru/contact/index.php?regions=3889
http://www.trust.ru/contact/index.php?regions=3890
http://www.trust.ru/contact/index.php?regions=234612
http://www.trust.ru/contact/index.php?regions=55297
http://www.trust.ru/contact/index.php?regions=3891
http://www.trust.ru/contact/index.php?regions=137863
http://www.trust.ru/contact/index.php?regions=sheksna
http://www.trust.ru/contact/index.php?regions=34627
http://www.trust.ru/contact/index.php?regions=14750
http://www.trust.ru/contact/index.php?regions=3892
http://www.trust.ru/contact/index.php?regions=23527
http://www.trust.ru/contact/index.php?regions=38893
http://www.trust.ru/contact/index.php?regions=3893
http://www.trust.ru/contact/index.php?regions=32892
http://www.trust.ru/contact/index.php?regions=3894
http://www.trust.ru/contact/index.php?regions=3895
http://www.trust.ru/contact/index.php?regions=3896
http://www.trust.ru/contact/index.php?regions=yartsevo"""



class Search:

    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    def patch_http_response_read(func):
        def inner(*args):
            try:
                return func(*args)
            except httplib.IncompleteRead, e:
                return e.partial
    
        return inner
    httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

    def query(self, address):
        url = address
        headers=[
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')]
        
       
        self.opener.addheaders = headers
        r = self.opener.open(url)
        content = r.read()

        r = self.opener.open("http://www.trust.ru/address/")
        content = r.read()
        #match = re.findall(r'<span.*?"searchPageLatLongContent".*?>(.+?)</span', content, re.U|re.I)

        return content

s=Search()
for u in urls.split("\n"):
    u=u.strip()
    print u
    html=s.query(u)
    print html
    #exit()
    #root=lxml.html.document_fromstring(html)
    #for
    
    
    
import scraperwiki
import lxml.html
import httplib
import cookielib
import urllib2
import urllib
import re
# Blank Python

urls="""http://www.trust.ru/contact/index.php?regions=3739
http://www.trust.ru/contact/index.php?regions=3858
http://www.trust.ru/contact/index.php?regions=3742
http://www.trust.ru/contact/index.php?regions=42678
http://www.trust.ru/contact/index.php?regions=3743
http://www.trust.ru/contact/index.php?regions=3744
http://www.trust.ru/contact/index.php?regions=4614454
http://www.trust.ru/contact/index.php?regions=3745
http://www.trust.ru/contact/index.php?regions=3746
http://www.trust.ru/contact/index.php?regions=3747
http://www.trust.ru/contact/index.php?regions=3748
http://www.trust.ru/contact/index.php?regions=3749
http://www.trust.ru/contact/index.php?regions=3750
http://www.trust.ru/contact/index.php?regions=3751
http://www.trust.ru/contact/index.php?regions=3752
http://www.trust.ru/contact/index.php?regions=3753
http://www.trust.ru/contact/index.php?regions=3754
http://www.trust.ru/contact/index.php?regions=3755
http://www.trust.ru/contact/index.php?regions=3756
http://www.trust.ru/contact/index.php?regions=3757
http://www.trust.ru/contact/index.php?regions=21118
http://www.trust.ru/contact/index.php?regions=3759
http://www.trust.ru/contact/index.php?regions=53881
http://www.trust.ru/contact/index.php?regions=berdsk
http://www.trust.ru/contact/index.php?regions=3761
http://www.trust.ru/contact/index.php?regions=3762
http://www.trust.ru/contact/index.php?regions=14670
http://www.trust.ru/contact/index.php?regions=bogoroditsk
http://www.trust.ru/contact/index.php?regions=13517
http://www.trust.ru/contact/index.php?regions=26178
http://www.trust.ru/contact/index.php?regions=bronnitsy
http://www.trust.ru/contact/index.php?regions=3763
http://www.trust.ru/contact/index.php?regions=buzuluk
http://www.trust.ru/contact/index.php?regions=13631
http://www.trust.ru/contact/index.php?regions=pyshma
http://www.trust.ru/contact/index.php?regions=55302
http://www.trust.ru/contact/index.php?regions=5667
http://www.trust.ru/contact/index.php?regions=3741
http://www.trust.ru/contact/index.php?regions=3764
http://www.trust.ru/contact/index.php?regions=3765
http://www.trust.ru/contact/index.php?regions=3766
http://www.trust.ru/contact/index.php?regions=volgorechensk
http://www.trust.ru/contact/index.php?regions=3767
http://www.trust.ru/contact/index.php?regions=3768
http://www.trust.ru/contact/index.php?regions=54557
http://www.trust.ru/contact/index.php?regions=52593
http://www.trust.ru/contact/index.php?regions=3740
http://www.trust.ru/contact/index.php?regions=3769
http://www.trust.ru/contact/index.php?regions=49245
http://www.trust.ru/contact/index.php?regions=3770
http://www.trust.ru/contact/index.php?regions=52505
http://www.trust.ru/contact/index.php?regions=gay
http://www.trust.ru/contact/index.php?regions=21458
http://www.trust.ru/contact/index.php?regions=36150
http://www.trust.ru/contact/index.php?regions=3771
http://www.trust.ru/contact/index.php?regions=3772
http://www.trust.ru/contact/index.php?regions=12619
http://www.trust.ru/contact/index.php?regions=49358
http://www.trust.ru/contact/index.php?regions=3774
http://www.trust.ru/contact/index.php?regions=dzerzhinskiy
http://www.trust.ru/contact/index.php?regions=3775
http://www.trust.ru/contact/index.php?regions=3776
http://www.trust.ru/contact/index.php?regions=dubovoe
http://www.trust.ru/contact/index.php?regions=3777
http://www.trust.ru/contact/index.php?regions=3778
http://www.trust.ru/contact/index.php?regions=3779
http://www.trust.ru/contact/index.php?regions=3780
http://www.trust.ru/contact/index.php?regions=3806
http://www.trust.ru/contact/index.php?regions=25662
http://www.trust.ru/contact/index.php?regions=zhigulevsk
http://www.trust.ru/contact/index.php?regions=3781
http://www.trust.ru/contact/index.php?regions=49321
http://www.trust.ru/contact/index.php?regions=3782
http://www.trust.ru/contact/index.php?regions=5173
http://www.trust.ru/contact/index.php?regions=3783
http://www.trust.ru/contact/index.php?regions=3784
http://www.trust.ru/contact/index.php?regions=57427
http://www.trust.ru/contact/index.php?regions=inza
http://www.trust.ru/contact/index.php?regions=3786
http://www.trust.ru/contact/index.php?regions=3787
http://www.trust.ru/contact/index.php?regions=3785
http://www.trust.ru/contact/index.php?regions=3788
http://www.trust.ru/contact/index.php?regions=3789
http://www.trust.ru/contact/index.php?regions=3790
http://www.trust.ru/contact/index.php?regions=71031
http://www.trust.ru/contact/index.php?regions=kamenolomni
http://www.trust.ru/contact/index.php?regions=3791
http://www.trust.ru/contact/index.php?regions=3792
http://www.trust.ru/contact/index.php?regions=karachev
http://www.trust.ru/contact/index.php?regions=14684
http://www.trust.ru/contact/index.php?regions=14685
http://www.trust.ru/contact/index.php?regions=kineshma
http://www.trust.ru/contact/index.php?regions=3794
http://www.trust.ru/contact/index.php?regions=kiselevsk
http://www.trust.ru/contact/index.php?regions=3795
http://www.trust.ru/contact/index.php?regions=54574
http://www.trust.ru/contact/index.php?regions=3796
http://www.trust.ru/contact/index.php?regions=3911
http://www.trust.ru/contact/index.php?regions=3797
http://www.trust.ru/contact/index.php?regions=kolpino
http://www.trust.ru/contact/index.php?regions=52514
http://www.trust.ru/contact/index.php?regions=3798
http://www.trust.ru/contact/index.php?regions=3799
http://www.trust.ru/contact/index.php?regions=3800
http://www.trust.ru/contact/index.php?regions=233646
http://www.trust.ru/contact/index.php?regions=3801
http://www.trust.ru/contact/index.php?regions=37566
http://www.trust.ru/contact/index.php?regions=54548
http://www.trust.ru/contact/index.php?regions=3802
http://www.trust.ru/contact/index.php?regions=14692
http://www.trust.ru/contact/index.php?regions=kronshtadt
http://www.trust.ru/contact/index.php?regions=14693
http://www.trust.ru/contact/index.php?regions=3803
http://www.trust.ru/contact/index.php?regions=3804
http://www.trust.ru/contact/index.php?regions=49371
http://www.trust.ru/contact/index.php?regions=3805
http://www.trust.ru/contact/index.php?regions=kurchatov
http://www.trust.ru/contact/index.php?regions=labinsk
http://www.trust.ru/contact/index.php?regions=3807
http://www.trust.ru/contact/index.php?regions=52464
http://www.trust.ru/contact/index.php?regions=3808
http://www.trust.ru/contact/index.php?regions=3809
http://www.trust.ru/contact/index.php?regions=19876
http://www.trust.ru/contact/index.php?regions=lobnya
http://www.trust.ru/contact/index.php?regions=3811
http://www.trust.ru/contact/index.php?regions=3812
http://www.trust.ru/contact/index.php?regions=3813
http://www.trust.ru/contact/index.php?regions=21809
http://www.trust.ru/contact/index.php?regions=3814
http://www.trust.ru/contact/index.php?regions=3815
http://www.trust.ru/contact/index.php?regions=32881
http://www.trust.ru/contact/index.php?regions=21506
http://www.trust.ru/contact/index.php?regions=mednogorsk
http://www.trust.ru/contact/index.php?regions=3816
http://www.trust.ru/contact/index.php?regions=3818
http://www.trust.ru/contact/index.php?regions=13529
http://www.trust.ru/contact/index.php?regions=3465
http://www.trust.ru/contact/index.php?regions=3819
http://www.trust.ru/contact/index.php?regions=3820
http://www.trust.ru/contact/index.php?regions=54551
http://www.trust.ru/contact/index.php?regions=3821
http://www.trust.ru/contact/index.php?regions=32883
http://www.trust.ru/contact/index.php?regions=3822
http://www.trust.ru/contact/index.php?regions=mtsensk
http://www.trust.ru/contact/index.php?regions=3823
http://www.trust.ru/contact/index.php?regions=3824
http://www.trust.ru/contact/index.php?regions=3825
http://www.trust.ru/contact/index.php?regions=3826
http://www.trust.ru/contact/index.php?regions=3827
http://www.trust.ru/contact/index.php?regions=14704
http://www.trust.ru/contact/index.php?regions=3828
http://www.trust.ru/contact/index.php?regions=14706
http://www.trust.ru/contact/index.php?regions=3829
http://www.trust.ru/contact/index.php?regions=3830
http://www.trust.ru/contact/index.php?regions=3831
http://www.trust.ru/contact/index.php?regions=426728
http://www.trust.ru/contact/index.php?regions=49382
http://www.trust.ru/contact/index.php?regions=novokubansk
http://www.trust.ru/contact/index.php?regions=3832
http://www.trust.ru/contact/index.php?regions=novopavlovsk
http://www.trust.ru/contact/index.php?regions=3834
http://www.trust.ru/contact/index.php?regions=3835
http://www.trust.ru/contact/index.php?regions=32884
http://www.trust.ru/contact/index.php?regions=3837
http://www.trust.ru/contact/index.php?regions=49408
http://www.trust.ru/contact/index.php?regions=23556
http://www.trust.ru/contact/index.php?regions=14714
http://www.trust.ru/contact/index.php?regions=3838
http://www.trust.ru/contact/index.php?regions=3839
http://www.trust.ru/contact/index.php?regions=3840
http://www.trust.ru/contact/index.php?regions=3841
http://www.trust.ru/contact/index.php?regions=osinovaya_gora
http://www.trust.ru/contact/index.php?regions=14716
http://www.trust.ru/contact/index.php?regions=3842
http://www.trust.ru/contact/index.php?regions=3843
http://www.trust.ru/contact/index.php?regions=3844
http://www.trust.ru/contact/index.php?regions=32887
http://www.trust.ru/contact/index.php?regions=3845
http://www.trust.ru/contact/index.php?regions=251789
http://www.trust.ru/contact/index.php?regions=3846
http://www.trust.ru/contact/index.php?regions=3847
http://www.trust.ru/contact/index.php?regions=poykovskiy
http://www.trust.ru/contact/index.php?regions=49362
http://www.trust.ru/contact/index.php?regions=21813
http://www.trust.ru/contact/index.php?regions=14719
http://www.trust.ru/contact/index.php?regions=13582
http://www.trust.ru/contact/index.php?regions=54591
http://www.trust.ru/contact/index.php?regions=3848
http://www.trust.ru/contact/index.php?regions=3849
http://www.trust.ru/contact/index.php?regions=13670
http://www.trust.ru/contact/index.php?regions=3851
http://www.trust.ru/contact/index.php?regions=3852
http://www.trust.ru/contact/index.php?regions=3853
http://www.trust.ru/contact/index.php?regions=3854
http://www.trust.ru/contact/index.php?regions=3855
http://www.trust.ru/contact/index.php?regions=13700
http://www.trust.ru/contact/index.php?regions=3856
http://www.trust.ru/contact/index.php?regions=3857
http://www.trust.ru/contact/index.php?regions=126772
http://www.trust.ru/contact/index.php?regions=saransk
http://www.trust.ru/contact/index.php?regions=3859
http://www.trust.ru/contact/index.php?regions=svetlograd
http://www.trust.ru/contact/index.php?regions=3860
http://www.trust.ru/contact/index.php?regions=13566
http://www.trust.ru/contact/index.php?regions=3862
http://www.trust.ru/contact/index.php?regions=14728
http://www.trust.ru/contact/index.php?regions=slavyansk_na_kubani
http://www.trust.ru/contact/index.php?regions=3863
http://www.trust.ru/contact/index.php?regions=1213097
http://www.trust.ru/contact/index.php?regions=3865
http://www.trust.ru/contact/index.php?regions=3866
http://www.trust.ru/contact/index.php?regions=3867
http://www.trust.ru/contact/index.php?regions=32888
http://www.trust.ru/contact/index.php?regions=3868
http://www.trust.ru/contact/index.php?regions=14731
http://www.trust.ru/contact/index.php?regions=14732
http://www.trust.ru/contact/index.php?regions=3869
http://www.trust.ru/contact/index.php?regions=3870
http://www.trust.ru/contact/index.php?regions=3871
http://www.trust.ru/contact/index.php?regions=3872
http://www.trust.ru/contact/index.php?regions=3873
http://www.trust.ru/contact/index.php?regions=teykovo
http://www.trust.ru/contact/index.php?regions=temryuk
http://www.trust.ru/contact/index.php?regions=32890
http://www.trust.ru/contact/index.php?regions=3874
http://www.trust.ru/contact/index.php?regions=3875
http://www.trust.ru/contact/index.php?regions=3876
http://www.trust.ru/contact/index.php?regions=3877
http://www.trust.ru/contact/index.php?regions=54554
http://www.trust.ru/contact/index.php?regions=3878
http://www.trust.ru/contact/index.php?regions=3879
http://www.trust.ru/contact/index.php?regions=3880
http://www.trust.ru/contact/index.php?regions=3881
http://www.trust.ru/contact/index.php?regions=3882
http://www.trust.ru/contact/index.php?regions=21790
http://www.trust.ru/contact/index.php?regions=14742
http://www.trust.ru/contact/index.php?regions=3883
http://www.trust.ru/contact/index.php?regions=3884
http://www.trust.ru/contact/index.php?regions=3885
http://www.trust.ru/contact/index.php?regions=3886
http://www.trust.ru/contact/index.php?regions=3887
http://www.trust.ru/contact/index.php?regions=33297
http://www.trust.ru/contact/index.php?regions=14748
http://www.trust.ru/contact/index.php?regions=chaplygin
http://www.trust.ru/contact/index.php?regions=3888
http://www.trust.ru/contact/index.php?regions=3889
http://www.trust.ru/contact/index.php?regions=3890
http://www.trust.ru/contact/index.php?regions=234612
http://www.trust.ru/contact/index.php?regions=55297
http://www.trust.ru/contact/index.php?regions=3891
http://www.trust.ru/contact/index.php?regions=137863
http://www.trust.ru/contact/index.php?regions=sheksna
http://www.trust.ru/contact/index.php?regions=34627
http://www.trust.ru/contact/index.php?regions=14750
http://www.trust.ru/contact/index.php?regions=3892
http://www.trust.ru/contact/index.php?regions=23527
http://www.trust.ru/contact/index.php?regions=38893
http://www.trust.ru/contact/index.php?regions=3893
http://www.trust.ru/contact/index.php?regions=32892
http://www.trust.ru/contact/index.php?regions=3894
http://www.trust.ru/contact/index.php?regions=3895
http://www.trust.ru/contact/index.php?regions=3896
http://www.trust.ru/contact/index.php?regions=yartsevo"""



class Search:

    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    def patch_http_response_read(func):
        def inner(*args):
            try:
                return func(*args)
            except httplib.IncompleteRead, e:
                return e.partial
    
        return inner
    httplib.HTTPResponse.read = patch_http_response_read(httplib.HTTPResponse.read)

    def query(self, address):
        url = address
        headers=[
            ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11')]
        
       
        self.opener.addheaders = headers
        r = self.opener.open(url)
        content = r.read()

        r = self.opener.open("http://www.trust.ru/address/")
        content = r.read()
        #match = re.findall(r'<span.*?"searchPageLatLongContent".*?>(.+?)</span', content, re.U|re.I)

        return content

s=Search()
for u in urls.split("\n"):
    u=u.strip()
    print u
    html=s.query(u)
    print html
    #exit()
    #root=lxml.html.document_fromstring(html)
    #for
    
    
    
