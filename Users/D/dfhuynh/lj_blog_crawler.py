import scraperwiki
import lxml.html
import lxml.etree
import re

def parse_url(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html.decode('utf-8'))

def clean_string(s):
    return re.sub(r'^[&\\s]+', '', s.replace('&nbsp;', ' ').strip())

def check_content_element_tag(elmt):
    try:
        tag = elmt.tag.lower()
        return tag == 'div' or tag == 'td' or tag == 'p' or tag == 'font'
    except:
        return False

def crawl_one_post(blogUrl, postUrl, userId, postIndex):
    title = None
    description = None
    
    root = parse_url(postUrl)
    
    meta_title = root.cssselect('meta[name="title"]')
    meta_description = root.cssselect('meta[name="description"]')
    if len(meta_title) > 0 and len(meta_description) > 0:
        title = meta_title[0].attrib["content"].strip()
        abbreviated_description = clean_string(meta_description[0].attrib["content"])
        look_for = abbreviated_description[0:3]

        for text_node in root.xpath("//text()"):
            text = clean_string(text_node)

            index = text.find(look_for)
            if index >= 0:
                def check_parent(parent):
                    tag = parent.tag.lower()
                    if tag == "script":
                        raise 
                    elif check_content_element_tag(parent):
                        parent_text = clean_string(parent.text_content())
                        return parent_text[parent_text.find(look_for):]
                        
                    return None

                try:
                    immediate_parent = text_node.getparent()
                    description = check_parent(immediate_parent)
                    if description is None:
                        for parent in immediate_parent.iterancestors():
                            description = check_parent(parent)
                            if not description is None:
                                break
                except:
                    pass

                if not description is None:
                    break

    if not description is None:
        data = {
            'post': postUrl,
            'index': postIndex,
            'user': userId,
            'title': title,
            'text': description
        }
        scraperwiki.sqlite.save(unique_keys = ['post'], data = data)
        return True
    else:
        return False


def crawl_one_blog(blogUrl, userId):
    posts = []
    
    def populate_post_urls(url):
        try:
            root = parse_url(url)
            entries = root.cssselect("a.subj-link")
            if len(entries) > 0:
                for a in entries:
                    posts.append(a.attrib["href"])
                return True
        except:
            pass

        return False
    
    populate_post_urls(blogUrl)
    skip = 10
    while populate_post_urls('%s?skip=%d' % (blogUrl, skip)):
        skip = skip + 10

    print '%s has %d posts total' % (blogUrl, len(posts))

    index = 0
    for p in posts:
        try:
            if not crawl_one_post(blogUrl, p, userId, index):
                print '*** FAILED to crawl blog %s at post %s' % (blogUrl, p)
        except:
            print '*** FAILED to crawl blog %s at post %s' % (blogUrl, p)
            pass

        index = index + 1

problematic_users = [
    "chenchusi",
    "chengkangwang",
]

users_scraped = [
    "baichangli",
    "baiwanrou",
    "baiyifeng",
    "baozhengde",
    "bijiacaihua",
    "boweiliu",
    "bubangqiang",
    "caijunjing",
    "cantarchen",
    "chen_meili",
    "chenchangyong",
    "chenchengye",
    "chengdawen",
    "chengtian",
    "chengyujohnson",
    "chenjiajun",
    "chenleilei",
    "chenqiming",
    "chenshuhui",
    "chensi",
    "chensile",
    "chenweijia",
    "chenwenze",
    "chenxukun",
    "chenyenfu",
    "chenyingxuan",
    "chenyiya",
    "chenyuping",
    "cheyanrong",
    "chiguilin",
    "chuanqi",
    "chuxinyu",
    "cuiyiting",
    "denganna",
    "dengdongtai",
    "dengyaxian",
    "dinghongyu",
    "dingman89",
    "dingxingzhou",
    "duenbo",
    "duxuejing",
    "erinyu89",
    "fanchiehling",
    "fanjinhong",
    "fengaimei",
    "fengjiechang",
    "fengmeihua",
    "fengnianhua",
    "fubaoqi",
    "gaodeling",
    "gaomengqian",
    "gejixian",
    "guanan",
    "guchen",
    "guhengzhi",
    "guoboting",
    "guojianming",
    "guoyingchen",
    "guoyuxiong",
    "hankelei",
    "hanlinsen",
    "hehuixin",
    "hengzhigu",
    "hexingyue",
    "heyaoqing",
    "heyiru",
    "hohangguo",
    "hongdawei",
    "hongwanpei",
    "hongyukuan",
    "hsutsuhsien",
    "huangdexian",
    "huanghongyu",
    "huangjun",
    "huangxiaochen",
    "huangyanmei",
    "huangyien",
    "huangyoumin",
    "huangzan",
    "huashuoren",
    "huyayun",
    "jiangting",
    "jiangyaqing",
    "jinfenhuang",
    "jingyili",
    "jinminzhi",
    "jujudong",
    "keviiin",
    "kongjunke",
    "kunjin4",
    "kwongjunde",
    "laiqian",
    "leiwanen",
    "lengjie",
    "leunghiuying",
    "liaoxiangke",
    "liaoxuanlun",
    "lichenling",
    "lihuan1",
    "lihuiwen",
    "lijiadong",
    "lijiajing",
    "lijunxian",
    "limingyi",
    "linjiayu",
    "linjierui",
    "linliangyu",
    "linqici",
    "linweiping",
    "linyansen",
    "lishangen",
    "lishaomin",
    "lishaoyu",
    "lisiman",
    "liubojue",
    "liuchengmin",
    "liudewen",
    "liuguoying",

    "liuhuijun",
    "liujiaming",
    "liujingwei",
    "liureihong",
    "liuyangwu",
    "liuyaxuan",
    "liuyichin",
    "liuzhefu",
    "liuzhong",
    "liuziming",
    "liyitat",
    "liyundi",
    "louweidan",
    "lu_meilin",
    "luoguangying",
    "luoshuling",
    "lupeiyun",
    "luxinna",
    "maokeer",
    "maxiaolong",
    "meichengxin",
    "meimeiyun",
    "miaoyicun",
    "mingshuozhang",
    "nancheng",
    "nayuting",
    "ninhcaili",
    "niushilin",
    "peilincui",
    "phil_aying",
    "renfangting",
    "renxiaoxing",
    "ruanfangfeng",
    "runsuzhang",
    "sangjie",
    "shaomengting",
    "shengyunhua",
    "shihaoguan",
    "shihwenchang",
    "shihyuchang",
    "shunjieding",
    "songyuanxiao",
    "su_guo",
    "suboquan",
    "sujiaqi",
    "sunchaojun",
    "sunjiazhen",
    "sunjingwen",
    "szelokc",
    "tanaihua",
    "tangmenghan",
    "tanmeiping",
    "taohe",
    "taolianying",
    "tengzi",
    "wanchenfu",
    "wangchiajen",
    "wangchunxia",
    "wangkeshi",
    "wanglan",
    "wanglidong",
    "wanglingzhu",
    "wangrou",
    "wangsanli",
    "wangshihao",
    "wangweigang",
    "wangyuchen",
    "wangzhijun",
    "wuweiting",
    "wuyouyuan",
    "xialing",
    "xiaoqinle",
    "xiaoxuemei",
    "xiaozhenli",
    "xiaozhenlun",
    "xiesuxian",
    "xieyb",
    "xieyiting",
    "xiezonglin",
    "xinyuyang",
    "xixiaolin",
    "xueweining",
    "xujiawei",
    "xupeixun",
    "xuweijie",
    "xuweining",
    "xuwenjie",
    "yang_da_long",
    "yangbeixin",
    "yangende",
    "yangfangru",
    "yangyuwei",
    "yanlanhuang",
    "yaokailing",
    "yaoxinyu",
    "yaoyongyi",
    "youshibo",
    "youyalun",
    "yuanzhiming",
    "yuxiehua",
    "yuxiuchen",
    "yuzonghan",
    "zhanfuguang",
    "zhang_xinyi",
    "zhangbin",
    "zhangdunqi",
    "zhanghaoxian",
    "zhangjiahao",
    "zhangkuida",
    "zhanglin1123",
    "zhangmeiyi",
    "zhangpeiqi",
    "zhangruizhe",
    "zhangtianhui",
    "zhangtianhui5",
    "zhangwanling",
    "zhangwenting",
    "zhangxinger",
    "zhangxuyifan",
    "zhangyiwen",
    "zhangyourong",
    "zhangyuanjie",
    "zhaojingsheng",
    "zhengliyan",
    "zhengzhiqiang",
    "zhongsichen",
    "zhouliyan",
    "zhouqin",
    "zhouyuanhao",
    "zhuailian",
    "zhurongchang",
    "zhushengtan",
    "zhuyuguang",
    "zisheng_li",
    
    "bbbush",
    "chengluo",
    "chinhsuankuo",
    "gaosiying",
    "guangyuan",
    "guopeiting",
    "guoxinyuan",
    "haishaolan",
    "han_liu",
    "hanlinxi",
    "hanmeng12",
    "hongngawong",
    "huangyizhen",
    "jmko",
    "leilihan",
    "li_congdao",
    "liangjiaxin",
    "lilu1991",
    "linxinqian",
    "linyijing",
    "linyuchong",
    "lipeigeng",
    "lisixian",
    "liwenchu",
    "liyaru27",
    "luhao",
    "meixiaomin",
    "panweiwei",
    "qian_wen_liang",
    "qinjiaqi",
    "qiuyijie",
    "shunwenchen",
    "situmeiqi",
    "suairan",
]
users = [
    "sushangan",
    "tanjiahui1",
    "taolimei",
    "wangchengjie",
    "wangyuanpeng",
    "wangzihua",
    "yanghuiling",
    "yangxilan",
    "yenjulai",
    "yupeici",
    "zhangyiying",
    "zhangyunpei",
    "zhaoqiqi",
    "zhoujiewen",
    "zuojiamin"
]

for user_id in users:
    crawl_one_blog("http://" + user_id + ".livejournal.com/", user_id)

#crawl_one_blog("http://guoyingchen.livejournal.com/", "guoyingchen")import scraperwiki
import lxml.html
import lxml.etree
import re

def parse_url(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html.decode('utf-8'))

def clean_string(s):
    return re.sub(r'^[&\\s]+', '', s.replace('&nbsp;', ' ').strip())

def check_content_element_tag(elmt):
    try:
        tag = elmt.tag.lower()
        return tag == 'div' or tag == 'td' or tag == 'p' or tag == 'font'
    except:
        return False

def crawl_one_post(blogUrl, postUrl, userId, postIndex):
    title = None
    description = None
    
    root = parse_url(postUrl)
    
    meta_title = root.cssselect('meta[name="title"]')
    meta_description = root.cssselect('meta[name="description"]')
    if len(meta_title) > 0 and len(meta_description) > 0:
        title = meta_title[0].attrib["content"].strip()
        abbreviated_description = clean_string(meta_description[0].attrib["content"])
        look_for = abbreviated_description[0:3]

        for text_node in root.xpath("//text()"):
            text = clean_string(text_node)

            index = text.find(look_for)
            if index >= 0:
                def check_parent(parent):
                    tag = parent.tag.lower()
                    if tag == "script":
                        raise 
                    elif check_content_element_tag(parent):
                        parent_text = clean_string(parent.text_content())
                        return parent_text[parent_text.find(look_for):]
                        
                    return None

                try:
                    immediate_parent = text_node.getparent()
                    description = check_parent(immediate_parent)
                    if description is None:
                        for parent in immediate_parent.iterancestors():
                            description = check_parent(parent)
                            if not description is None:
                                break
                except:
                    pass

                if not description is None:
                    break

    if not description is None:
        data = {
            'post': postUrl,
            'index': postIndex,
            'user': userId,
            'title': title,
            'text': description
        }
        scraperwiki.sqlite.save(unique_keys = ['post'], data = data)
        return True
    else:
        return False


def crawl_one_blog(blogUrl, userId):
    posts = []
    
    def populate_post_urls(url):
        try:
            root = parse_url(url)
            entries = root.cssselect("a.subj-link")
            if len(entries) > 0:
                for a in entries:
                    posts.append(a.attrib["href"])
                return True
        except:
            pass

        return False
    
    populate_post_urls(blogUrl)
    skip = 10
    while populate_post_urls('%s?skip=%d' % (blogUrl, skip)):
        skip = skip + 10

    print '%s has %d posts total' % (blogUrl, len(posts))

    index = 0
    for p in posts:
        try:
            if not crawl_one_post(blogUrl, p, userId, index):
                print '*** FAILED to crawl blog %s at post %s' % (blogUrl, p)
        except:
            print '*** FAILED to crawl blog %s at post %s' % (blogUrl, p)
            pass

        index = index + 1

problematic_users = [
    "chenchusi",
    "chengkangwang",
]

users_scraped = [
    "baichangli",
    "baiwanrou",
    "baiyifeng",
    "baozhengde",
    "bijiacaihua",
    "boweiliu",
    "bubangqiang",
    "caijunjing",
    "cantarchen",
    "chen_meili",
    "chenchangyong",
    "chenchengye",
    "chengdawen",
    "chengtian",
    "chengyujohnson",
    "chenjiajun",
    "chenleilei",
    "chenqiming",
    "chenshuhui",
    "chensi",
    "chensile",
    "chenweijia",
    "chenwenze",
    "chenxukun",
    "chenyenfu",
    "chenyingxuan",
    "chenyiya",
    "chenyuping",
    "cheyanrong",
    "chiguilin",
    "chuanqi",
    "chuxinyu",
    "cuiyiting",
    "denganna",
    "dengdongtai",
    "dengyaxian",
    "dinghongyu",
    "dingman89",
    "dingxingzhou",
    "duenbo",
    "duxuejing",
    "erinyu89",
    "fanchiehling",
    "fanjinhong",
    "fengaimei",
    "fengjiechang",
    "fengmeihua",
    "fengnianhua",
    "fubaoqi",
    "gaodeling",
    "gaomengqian",
    "gejixian",
    "guanan",
    "guchen",
    "guhengzhi",
    "guoboting",
    "guojianming",
    "guoyingchen",
    "guoyuxiong",
    "hankelei",
    "hanlinsen",
    "hehuixin",
    "hengzhigu",
    "hexingyue",
    "heyaoqing",
    "heyiru",
    "hohangguo",
    "hongdawei",
    "hongwanpei",
    "hongyukuan",
    "hsutsuhsien",
    "huangdexian",
    "huanghongyu",
    "huangjun",
    "huangxiaochen",
    "huangyanmei",
    "huangyien",
    "huangyoumin",
    "huangzan",
    "huashuoren",
    "huyayun",
    "jiangting",
    "jiangyaqing",
    "jinfenhuang",
    "jingyili",
    "jinminzhi",
    "jujudong",
    "keviiin",
    "kongjunke",
    "kunjin4",
    "kwongjunde",
    "laiqian",
    "leiwanen",
    "lengjie",
    "leunghiuying",
    "liaoxiangke",
    "liaoxuanlun",
    "lichenling",
    "lihuan1",
    "lihuiwen",
    "lijiadong",
    "lijiajing",
    "lijunxian",
    "limingyi",
    "linjiayu",
    "linjierui",
    "linliangyu",
    "linqici",
    "linweiping",
    "linyansen",
    "lishangen",
    "lishaomin",
    "lishaoyu",
    "lisiman",
    "liubojue",
    "liuchengmin",
    "liudewen",
    "liuguoying",

    "liuhuijun",
    "liujiaming",
    "liujingwei",
    "liureihong",
    "liuyangwu",
    "liuyaxuan",
    "liuyichin",
    "liuzhefu",
    "liuzhong",
    "liuziming",
    "liyitat",
    "liyundi",
    "louweidan",
    "lu_meilin",
    "luoguangying",
    "luoshuling",
    "lupeiyun",
    "luxinna",
    "maokeer",
    "maxiaolong",
    "meichengxin",
    "meimeiyun",
    "miaoyicun",
    "mingshuozhang",
    "nancheng",
    "nayuting",
    "ninhcaili",
    "niushilin",
    "peilincui",
    "phil_aying",
    "renfangting",
    "renxiaoxing",
    "ruanfangfeng",
    "runsuzhang",
    "sangjie",
    "shaomengting",
    "shengyunhua",
    "shihaoguan",
    "shihwenchang",
    "shihyuchang",
    "shunjieding",
    "songyuanxiao",
    "su_guo",
    "suboquan",
    "sujiaqi",
    "sunchaojun",
    "sunjiazhen",
    "sunjingwen",
    "szelokc",
    "tanaihua",
    "tangmenghan",
    "tanmeiping",
    "taohe",
    "taolianying",
    "tengzi",
    "wanchenfu",
    "wangchiajen",
    "wangchunxia",
    "wangkeshi",
    "wanglan",
    "wanglidong",
    "wanglingzhu",
    "wangrou",
    "wangsanli",
    "wangshihao",
    "wangweigang",
    "wangyuchen",
    "wangzhijun",
    "wuweiting",
    "wuyouyuan",
    "xialing",
    "xiaoqinle",
    "xiaoxuemei",
    "xiaozhenli",
    "xiaozhenlun",
    "xiesuxian",
    "xieyb",
    "xieyiting",
    "xiezonglin",
    "xinyuyang",
    "xixiaolin",
    "xueweining",
    "xujiawei",
    "xupeixun",
    "xuweijie",
    "xuweining",
    "xuwenjie",
    "yang_da_long",
    "yangbeixin",
    "yangende",
    "yangfangru",
    "yangyuwei",
    "yanlanhuang",
    "yaokailing",
    "yaoxinyu",
    "yaoyongyi",
    "youshibo",
    "youyalun",
    "yuanzhiming",
    "yuxiehua",
    "yuxiuchen",
    "yuzonghan",
    "zhanfuguang",
    "zhang_xinyi",
    "zhangbin",
    "zhangdunqi",
    "zhanghaoxian",
    "zhangjiahao",
    "zhangkuida",
    "zhanglin1123",
    "zhangmeiyi",
    "zhangpeiqi",
    "zhangruizhe",
    "zhangtianhui",
    "zhangtianhui5",
    "zhangwanling",
    "zhangwenting",
    "zhangxinger",
    "zhangxuyifan",
    "zhangyiwen",
    "zhangyourong",
    "zhangyuanjie",
    "zhaojingsheng",
    "zhengliyan",
    "zhengzhiqiang",
    "zhongsichen",
    "zhouliyan",
    "zhouqin",
    "zhouyuanhao",
    "zhuailian",
    "zhurongchang",
    "zhushengtan",
    "zhuyuguang",
    "zisheng_li",
    
    "bbbush",
    "chengluo",
    "chinhsuankuo",
    "gaosiying",
    "guangyuan",
    "guopeiting",
    "guoxinyuan",
    "haishaolan",
    "han_liu",
    "hanlinxi",
    "hanmeng12",
    "hongngawong",
    "huangyizhen",
    "jmko",
    "leilihan",
    "li_congdao",
    "liangjiaxin",
    "lilu1991",
    "linxinqian",
    "linyijing",
    "linyuchong",
    "lipeigeng",
    "lisixian",
    "liwenchu",
    "liyaru27",
    "luhao",
    "meixiaomin",
    "panweiwei",
    "qian_wen_liang",
    "qinjiaqi",
    "qiuyijie",
    "shunwenchen",
    "situmeiqi",
    "suairan",
]
users = [
    "sushangan",
    "tanjiahui1",
    "taolimei",
    "wangchengjie",
    "wangyuanpeng",
    "wangzihua",
    "yanghuiling",
    "yangxilan",
    "yenjulai",
    "yupeici",
    "zhangyiying",
    "zhangyunpei",
    "zhaoqiqi",
    "zhoujiewen",
    "zuojiamin"
]

for user_id in users:
    crawl_one_blog("http://" + user_id + ".livejournal.com/", user_id)

#crawl_one_blog("http://guoyingchen.livejournal.com/", "guoyingchen")