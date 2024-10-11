import requests
import re,os,execjs

class Tax():
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Referer": "https://iam.pt.ouchn.cn/am/UI/Login",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\""
        }
        self.__path__ = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(self.__path__, "kaifang_login.js"), "r", encoding="utf-8") as js_file:
            self.js_code = execjs.compile(js_file.read())
    
    # 获取DES密钥
    def get_des_key(self):
        url = "https://iam.pt.ouchn.cn/am/UI/Login"
        response = requests.get(url, headers=self.headers)
        # 用正则取出其中的value值,就一个值懒的xpath了
        key = re.findall(r'name="random" value="(.+?)"', response.text)
        return key[0]
    
    # 获取登录的加密参数
    def get_login_params(self, username, password, des_key):
        IDToken1  = self.js_code.call("strEnc", username,des_key, "", "")
        IDToken2  = self.js_code.call("strEnc", password,des_key, "", "")
        return IDToken1, IDToken2
    
if __name__ == "__main__":
    tax = Tax()
    des_key = tax.get_des_key()
    name,pwd = tax.get_login_params("admin", "admin", des_key)
    print(name, pwd)
    # 只能解析出来这个,其他的参数是从验证码中获取的，暂时解析不出来
