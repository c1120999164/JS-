import requests
import re
import os
import execjs


class Tax():
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\""
        }
        self.__path__ = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(self.__path__, "fangtianxia_login.js"), "r", encoding="utf-8") as js_file:
            self.js_code = execjs.compile(js_file.read())

    # 获取RSA公钥
    def get_rsa_key(self):
        url = "https://passport.fang.com/"
        params = {
            "backurl": "https://nt.fang.com/"
        }
        response = requests.get(url, headers=self.headers, params=params)
        key_list = re.findall(r'new RSAKeyPair\((.*?)\);',
                              response.text)[0].split(', ')
        return key_list

    def login(self):
        url = "https://passport.fang.com/loginwithpwdStrong.api"
        data = {
            "uid": "wbming_chen",
            "pwd": "15bb415899a292d8b97047cdd65cfff2bf293fe05eba516fd75eff922b46c2a7c31d5e2ba42efde404d010cea2bd471dddc2ec779f420cf5bf792d3814342aedce28730bef2c59dbce083f9090b18ca109f6a8fb60f9e92363ab401e8790e2ea8318ff8d76700ca65aad181a2b1a67f812661f793f6c07aac5778c95d7567c40",
            "Service": "soufun-passport-web",
            "AutoLogin": "1",
            "Operatetype": "0",
            "Gt": "35c3d8dffffd310ca05d87cea3b52786",
            "Challenge": "b247884c498e13aab8f1aec5af5df4ae",
            "Validate": "2e2f29064e19bb0720563c1ead303c2b"
        }
        cookies = {
            "global_cookie": "5o6virc4anet1swuc5rznqonj12m244n00s",
            "g_sourcepage": "txz_dl%5Egg_pc",
            "__utma": "147393320.1605635404.1728614835.1728614835.1728614835.1",
            "__utmc": "147393320",
            "__utmz": "147393320.1728614835.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
            "token": "0ceb4133ee0947bd85ef644083aef654",
            "unique_cookie": "U_5o6virc4anet1swuc5rznqonj12m244n00s*6"
        }
        response = requests.post(url, headers=self.headers, data=data,cookies=cookies)

        print(response.text)


if __name__ == "__main__":
    tax = Tax()
    tax.login()
    # 只能解析出来这个,其他的参数是从验证码中获取的，暂时解析不出来
