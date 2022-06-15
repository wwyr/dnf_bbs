import re
import json
import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from time import sleep


class DNF:
    def __init__(self, bbs_login_url, daily_music_url, pub_url):
        """
        初始化
        """
        self.bbs_login_url = bbs_login_url
        self.daily_music_url = daily_music_url
        self.daily_sign_url = ''
        self.pub_url = pub_url
        self.feel_list = ['悠然自得', '欣喜若狂', '乐不思蜀', '方寸大乱', '心烦意乱', '情不自禁', '心潮澎湃',
                          '垂头丧气', '灰心丧气', '心灰意冷', '万念俱灰', '黯然销魂', '大失所望', '自暴自弃',
                          '欢天喜地', '欢欣鼓舞', '喜从天降', '大喜过望', '兴高采烈', '兴致勃勃', '乐不可支',
                          '心花怒放', '手舞足蹈', '拍手称快', '皆大欢喜', '愁眉不展', '愁眉苦脸', '愁眉紧锁',
                          '忧心忡忡', '怅然若失', '心神不定', '度日如年', '抓耳挠腮', '火急火燎', '心旷神怡']
        self.daily_feel = ''
        self.daily_lyric = ''
        self.daily_name = ''
        self.daily_id = ''
        self.daily_img = ''
        self.today = 1
        self.bbs_cookie = '''[
{
    "domain": ".dnf.gamebbs.qq.com",
    "expirationDate": 1655168327,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ts_last",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "dnf.gamebbs.qq.com/forum.php",
    "id": 1
},
{
    "domain": ".dnf.gamebbs.qq.com",
    "expirationDate": 1718238527,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ts_uid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "2957624892",
    "id": 2
},
{
    "domain": ".qq.com",
    "expirationDate": 1685613086,
    "hostOnly": false,
    "httpOnly": false,
    "name": "eas_sid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "k1Y6F5e4b0t7R7b048E6i8G0u4",
    "id": 3
},
{
    "domain": ".qq.com",
    "expirationDate": 2147385600,
    "hostOnly": false,
    "httpOnly": false,
    "name": "fqm_pvqid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "26597181-c754-4e97-8729-3e240396a1dc",
    "id": 4
},
{
    "domain": ".qq.com",
    "expirationDate": 1970207408.464061,
    "hostOnly": false,
    "httpOnly": false,
    "name": "iip",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "0",
    "id": 5
},
{
    "domain": ".qq.com",
    "expirationDate": 1970207408.464025,
    "hostOnly": false,
    "httpOnly": false,
    "name": "pac_uid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "0_9a05fa35d92b1",
    "id": 6
},
{
    "domain": ".qq.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "pgv_info",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "ssid=s7803175344",
    "id": 7
},
{
    "domain": ".qq.com",
    "expirationDate": 2147385600,
    "hostOnly": false,
    "httpOnly": false,
    "name": "pgv_pvid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "4171289545",
    "id": 8
},
{
    "domain": ".qq.com",
    "expirationDate": 2147483647.051463,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ptcz",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "e7379660bc5961fd004826ba327d71ccc915a9805ca498fd8723e27e3612e4ee",
    "id": 9
},
{
    "domain": ".qq.com",
    "expirationDate": 2147483647.075359,
    "hostOnly": false,
    "httpOnly": false,
    "name": "RK",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "2BVE99GFat",
    "id": 10
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1657331904.783016,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_atarget",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 11
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1656035905.678347,
    "hostOnly": true,
    "httpOnly": true,
    "name": "TQjV_2132_auth",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "81e3SXYSC%2Bb5pmfPdz5bZqysMZcE7FJr%2BrYDYCWlUNp5q%2FUhkJsEJMUyRekUczIKQXX8hR%2BGZzOemLj%2BO6J7seL5DA",
    "id": 12
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1655166556.82137,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_checkpm",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 13
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1655734469.593285,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_forum_lastvisit",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "D_43_1654739904D_42_1655108240D_44_1655129669",
    "id": 14
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1655252926.986793,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_lastact",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1655166526%09home.php%09misc",
    "id": 15
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1656669086.373564,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_lastvisit",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1654073486",
    "id": 16
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1655167127,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_noticeTitle",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 17
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1656669086.373541,
    "hostOnly": true,
    "httpOnly": true,
    "name": "TQjV_2132_saltkey",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "nY8Y5LML",
    "id": 18
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1655166826.986948,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_sendmail",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 19
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1686665674,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_smile",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "4D1",
    "id": 20
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1686702526.434881,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_ulastactivity",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1655166526%7C0",
    "id": 21
},
{
    "domain": "dnf.gamebbs.qq.com",
    "expirationDate": 1657711812.526638,
    "hostOnly": true,
    "httpOnly": false,
    "name": "TQjV_2132_visitedfid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "44D42D43",
    "id": 22
}
]'''
        self.music_cookie = '''[
{
    "domain": ".163.com",
    "expirationDate": 1717666966,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ns",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "NS1.2.724735852.1654594966",
    "id": 1
},
{
    "domain": ".163.com",
    "expirationDate": 4808719769,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ntes_nnid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "4e23f6668a950b2094bb88e5b1bfff5b,1655119769350",
    "id": 2
},
{
    "domain": ".163.com",
    "expirationDate": 4808719769,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_ntes_nuid",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "4e23f6668a950b2094bb88e5b1bfff5b",
    "id": 3
},
{
    "domain": ".163.com",
    "expirationDate": 1686038756,
    "hostOnly": false,
    "httpOnly": false,
    "name": "vinfo_n_f_l_n3",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "88fc74894035e9bb.1.0.1654502723922.0.1654502756554",
    "id": 4
},
{
    "domain": ".music.163.com",
    "expirationDate": 1656415790.833377,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__csrf",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "20675dc4413592b7c5e73d40177c6645",
    "id": 5
},
{
    "domain": ".music.163.com",
    "expirationDate": 1656415780.8327,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__remember_me",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "true",
    "id": 6
},
{
    "domain": ".music.163.com",
    "expirationDate": 1812848410,
    "hostOnly": false,
    "httpOnly": false,
    "name": "_iuqxldmzr_",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "32",
    "id": 7
},
{
    "domain": ".music.163.com",
    "expirationDate": 1812848410,
    "hostOnly": false,
    "httpOnly": false,
    "name": "JSESSIONID-WYYY",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "VgoeTv%5CWr91dUTyZj6QI2ZBadS4%2B2D7ftBBslOy3Zs%5CZ916lk4j6Z14HNKklqSBKhq%5CoYlIWQxPWRe2Ql02F%5CiwP3gYlG4Y1KxwpM%2BwO%5CpKF29%2FmjgaSqbKG4GKjpy3NSfj1rEt9dzm57sbAqkZlgnqZGZ0AM9Xj%2BOscKa%2BVKjGd8vDz%3A1655168410640",
    "id": 8
},
{
    "domain": ".music.163.com",
    "expirationDate": 1656415780.833341,
    "hostOnly": false,
    "httpOnly": true,
    "name": "MUSIC_U",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "a160ce5f08f9085e3c479db1ac6144c546dbfd7622f439bbe6a3cb77714529a51e8907c67206e1edc3b5b2ec6cf95ea02e93f2117182e3475fbf8366fbc97bd61ac3ab5be2c6cef8a0d2166338885bd7",
    "id": 9
},
{
    "domain": ".music.163.com",
    "expirationDate": 1970479769.458364,
    "hostOnly": false,
    "httpOnly": false,
    "name": "NMTID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "00OLx44cUyFLTbwx0eIjZH0pjbaOMgAAAGBXNNvRA",
    "id": 10
},
{
    "domain": ".music.163.com",
    "expirationDate": 2285886610.924578,
    "hostOnly": false,
    "httpOnly": false,
    "name": "ntes_kaola_ad",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 11
},
{
    "domain": ".music.163.com",
    "expirationDate": 1970526610,
    "hostOnly": false,
    "httpOnly": false,
    "name": "WEVNSM",
    "path": "/",
    "sameSite": "strict",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1.0.0",
    "id": 12
},
{
    "domain": ".music.163.com",
    "expirationDate": 1970479769,
    "hostOnly": false,
    "httpOnly": false,
    "name": "WNMCID",
    "path": "/",
    "sameSite": "strict",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "okrkiw.1655119769618.01.0",
    "id": 13
},
{
    "domain": "music.163.com",
    "expirationDate": 2147483647,
    "hostOnly": true,
    "httpOnly": false,
    "name": "WM_NI",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "RLu29TB0hMDz3hdguLgX3qhLBycgdCYjA9atxxo4%2Bt6QYzFMvY9ZP4sePTvIXuame8o3v9Efj2%2Fs%2BihXWBTrPWyKqnadaXz5EBWY61WI69yUEoy6HAmpItNlWs%2BUkSfzQnA%3D",
    "id": 14
},
{
    "domain": "music.163.com",
    "expirationDate": 2147483647,
    "hostOnly": true,
    "httpOnly": false,
    "name": "WM_NIKE",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "9ca17ae2e6ffcda170e2e6eeb7e4349b9ebf9bb43b9aef8ba7c15e939f8a82d45faebfff94eb40b79be195e92af0fea7c3b92a9294bbd3bc6082f0a8aec772f1b8ac88f848a588fd92eb4882a7ad88e7499bb68fdae480bca8a1d5aa80f68f979bc547b687f7bbd340b1bba0b5f5439cabaf8ee834adedbadac86eaaeee194aa63ac8899a3d77a9489b7acf466a3bcafb9f93f879e99bab53b9597fadafc5f87b1b7d7cb4bafb08795cd6895ade5b6ea59a6a69f8fc437e2a3",
    "id": 15
},
{
    "domain": "music.163.com",
    "expirationDate": 2147483647,
    "hostOnly": true,
    "httpOnly": false,
    "name": "WM_TID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "4%2B1H1hmhFvZEVRRABRPUE2al5ko%2BQ6JN",
    "id": 16
}
]'''
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')  # 选择无头模式
        path = r'../测试/chromedriver.exe'  # 驱动文件的相对路径
        self.browser = webdriver.Chrome(options=self.chrome_options, executable_path=path)
        self.browser.set_window_size('1920', '1080')  # 设置页面尺寸
        self.browser.set_page_load_timeout(10)  # 页面加载超时
        self.browser.implicitly_wait(10)  # 执行命令超时

    def update(self):
        """
        运行前检查更新
        :return:
        """
        update_url = 'https://github.com/wyrco/dnf_bbs'
        self.browser.get(update_url)
        sleep(10)
        res = self.browser.page_source
        new_name, new_url = re.findall('<a class=".*?" title=".*?" data-pjax=".*?" href="(.*?)">(.*?)</a>', res)

        '<a class="js-navigation-open Link--primary" title="论坛小工具v1.0.exe" data-pjax="#repo-content-pjax-container" href="/wyrco/dnf_bbs/blob/main/%E8%AE%BA%E5%9D%9B%E5%B0%8F%E5%B7%A5%E5%85%B7v1.0.exe">论坛小工具v1.0.exe</a>'

    def get_msg(self):
        """
        从本地读取基本信息
        :return:
        """

    def daily_share_feel(self):
        """
        获取每日心情
        :return:
        """
        date = datetime.datetime.now().strftime("%Y年%m月%d日")
        self.today = datetime.datetime.today().day
        self.daily_feel = '游戏大区：广东7区\n角色名字：DestinyW\n签到日前{}\n今日心情/祝福：{}'.format(date, self.feel_list[self.today])
        return self.daily_feel

    def get_music(self):
        """
        获取网易云每日推荐音乐
        :return:
        """
        self.browser.get(self.daily_music_url)
        bbs_cookie_list = json.loads(self.music_cookie)
        self.browser.delete_all_cookies()
        for i in bbs_cookie_list:
            if isinstance(i, dict):
                if 'sameSite' in i:
                    i.pop('sameSite')
                    self.browser.add_cookie(i)
        self.browser.get(self.daily_music_url)
        self.browser.switch_to.frame('g_iframe')  # 进入内嵌
        self.browser.find_element_by_xpath("//table/tbody/tr[1]/td[2]/div/div/div/span/a/b").click()
        self.browser.refresh()
        self.browser.switch_to.frame('g_iframe')  # 进入内嵌
        res = self.browser.page_source
        self.daily_img = re.findall(r'img src=".*?" class=".*?" data-src="(.*?)">', res)[0]
        self.daily_id = self.browser.current_url[32:]
        self.daily_name = self.browser.find_element_by_xpath("//*[@class='tit']/em").text
        lyric_list = \
            re.findall(
                r'<div id="lyric-content" class=".*?" data-song-id=".*?" data-third-copy=".*? copy-from=".*?">(.*?)</div>',
                res)[0]
        lyric = lyric_list.split('<br>')
        new_lyric = []
        for i in lyric:
            if ':' in i:
                continue
            if '：' in i:
                continue
            if '【' in i:
                continue
            if '@' in i:
                continue
            if '<div id="flag_more" class="f-hide">' in i:
                i = i[35:]
            if i:
                new_lyric.append(i)
        self.daily_lyric = '\n'.join(new_lyric)
        return self.daily_name, self.daily_id, self.daily_img, self.daily_lyric

    def bbs_login(self):
        """
        dnf论坛登陆并尝试签到
        :return:
        """
        self.browser.get(self.bbs_login_url)
        bbs_cookie_list = json.loads(self.bbs_cookie)
        self.browser.delete_all_cookies()
        for i in bbs_cookie_list:
            if isinstance(i, dict):
                if 'sameSite' in i:
                    i.pop('sameSite')
                    self.browser.add_cookie(i)
        self.browser.get(self.bbs_login_url)
        try:
            self.browser.find_element_by_xpath("//*[@id='JD_sign']").click()  # 点击签到
        except NoSuchElementException:
            pass
        except TimeoutException:
            self.bbs_login()

    def get_sign_url(self):
        """
        获取每月酒馆签到链接。
        :return:
        """
        self.browser.get(self.pub_url)
        res = self.browser.page_source
        url_list = re.findall(r'<a href="(.*?.html)" style=".*?" onclick=".*?" class=".*?">ღ缘来你也在这里.*?签到帖ღ</a>', res)[0]
        self.daily_sign_url = 'https://dnf.gamebbs.qq.com/' + url_list
        return self.daily_sign_url

    def pub_sign(self):
        """
        根据获取到到每日心情进行提交。
        :return:
        """
        self.browser.get(self.daily_sign_url)
        self.browser.find_element_by_xpath("//*[@id='fastpostmessage']").send_keys(self.daily_feel)  # 输入签到内容
        sleep(2)
        self.browser.find_element_by_xpath("//*[@id='fastpostsubmit']").click()  # 点击发送

    def send_music(self):
        """
        根据获取的音乐名字、ID、图片链接、歌词进行提交。
        :return:
        """
        self.browser.get(self.pub_url)
        self.browser.find_element_by_xpath("//*[@id='switchadvance']").click()  # 进入高级模式
        self.browser.find_element_by_xpath("//*[@id='typeid_ctrl']").click()  # 点击主题
        self.browser.find_element_by_xpath("//*[@id='typeid_ctrl_menu']/ul/li[4]").click()  # 选择主题
        self.browser.find_element_by_xpath("//*[@id='subject']").send_keys('【每日音乐推荐】' + self.daily_name)  # 输入标题
        self.browser.find_element_by_xpath("//*[@id='e_simple']").click()  # 点击高级
        self.browser.find_element_by_xpath("//*[@id='e_postbg']").click()  # 点击背景
        self.browser.find_element_by_xpath("//*[@id='e_postbg_menu']/input[2]").click()  # 选择第二个背景
        self.browser.switch_to.frame('e_iframe')  # 进入内嵌
        self.browser.find_element_by_xpath("/html/body").click()  # 点击编辑框
        self.browser.find_element_by_xpath("/html/body").send_keys(f'[img]{self.daily_img}[/img]\n')
        self.browser.find_element_by_xpath("/html/body").send_keys(
            f'[audio5=autoplay]http://music.163.com/song/media//outer/url?id={self.daily_id}.mp3[/audio5]\n')
        self.browser.find_element_by_xpath("/html/body").send_keys(self.daily_lyric)
        self.browser.find_element_by_xpath("/html/body").send_keys(Keys.CONTROL, 'a')
        sleep(1)
        self.browser.switch_to.default_content()  # 跳回最外层页面
        sleep(1)
        self.browser.find_element_by_id('e_justifycenter').click()  # 居中
        sleep(1)
        self.browser.find_element_by_id('postsubmit').click()

    def run(self):
        """
        运行逻辑
        :return:
        """
        self.get_music()
        self.daily_share_feel()
        self.bbs_login()
        self.get_sign_url()
        self.pub_sign()
        sleep(20)
        self.send_music()
        self.browser.quit()
        self.log()

    def log(self):
        """
        记录日志
        :return:
        """
        date = datetime.datetime.now()
        with open('日志.txt', 'at', encoding='utf-8') as f:
            f.write('日期:' + str(date) + '-----' + '歌名:' + self.daily_name + '-----' + '心情:' + self.feel_list[
                self.today] + '\n')

    def __del__(self):
        """
        结束
        :return:
        """
        pass


if __name__ == '__main__':
    URL1 = 'https://dnf.gamebbs.qq.com/plugin.php?id=k_misign:sign'
    URL2 = 'https://music.163.com/#/discover/recommend/taste'
    URL3 = 'https://dnf.gamebbs.qq.com/forum-44-1.html'
    start = DNF(URL1, URL2, URL3)
    start.run()
