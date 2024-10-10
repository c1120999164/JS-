import json,os
import time
import base64
import execjs
import ddddocr
import requests
from loguru import logger


class Tax():
    def __init__(self):
        self.__path__ = os.path.dirname(os.path.abspath(__file__))
        self.headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://hdz.baiwangjs.com",
            "priority": "u=0, i",
            "referer": "https://hdz.baiwangjs.com/manage/login.html?v=1728524456347",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"macOS\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        with open(os.path.join(self.__path__, "baiwang_login.js"), "r", encoding="utf-8") as js_file:
            self.js_code = execjs.compile(js_file.read())
    
    # 获取图片及其他登录加密参数
    def get_login_params(self):
        url = "https://hdz.baiwangjs.com/captcha/get"
        data = {
            "captchaType": "blockPuzzle",
            "clientUid": "slider-e1cc0bea-449d-4c07-88ed-d91b89f45df4",
            "ts": int(time.time() * 1000)
        }
        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=self.headers, data=data)
        token = response.json()["repData"]["token"]
        secretKey = response.json()["repData"]["secretKey"]
        # 获取图片,上面是大图下面是小图
        originalImageBase64 = response.json()["repData"]["originalImageBase64"]
        jigsawImageBase64 = response.json()["repData"]["jigsawImageBase64"]
        return token, secretKey, originalImageBase64, jigsawImageBase64

    # 获取滑块距离
    def get_moveLeftDistance(self, originalImageBase64, jigsawImageBase64):
        # 将 Base64 编码字符串转换为字节对象
        originalImageBytes = base64.b64decode(originalImageBase64)
        jigsawImageBytes = base64.b64decode(jigsawImageBase64)
        d = ddddocr.DdddOcr(det=False, show_ad=False)
        # 获取滑块距离
        moveLeftDistance = d.slide_match(originalImageBytes, jigsawImageBytes,simple_target = True)["target"][0]
        logger.info(f'识别到的滑块距离为：{moveLeftDistance}')
        return moveLeftDistance
    
    # 验证码检测
    def check_captcha(self,secretKey,token,moveLeftDistance):
        url = "https://hdz.baiwangjs.com/captcha/check"
        pointJson = self.js_code.call("get_pointJson",secretKey,moveLeftDistance)
        data = {
            "captchaType": "blockPuzzle",
            "pointJson": pointJson,
            "token": token,
            "clientUid": "slider-e1cc0bea-449d-4c07-88ed-d91b89f45df4",
            "ts": 1728525395786
        }
        data = json.dumps(data, separators=(',', ':'))
        response = requests.post(url, headers=self.headers,data=data)
        logger.info(response)
        
    # 登录
    def login(self, username, password,moveLeftDistance):
        url = "https://hdz.baiwangjs.com/login"
        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "origin": "https://hdz.baiwangjs.com",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://hdz.baiwangjs.com/manage/login.html?v=1718943162401",
            "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"
        }
        captchaVerification = self.js_code.call("get_captchaVerification", secretKey, token, moveLeftDistance)
        data = {
            "username": username,
            "password": password[::-1],
            "yzm": "",
            "data_type": "0",
            "captchaVerification": captchaVerification
        }
        response = requests.post(url, headers=headers, data=data)
        logger.debug(response.text)
        # print(response)


if __name__ == '__main__':
    tax = Tax()
    token, secretKey, originalImageBase64, jigsawImageBase64 = tax.get_login_params()
    moveLeftDistance = tax.get_moveLeftDistance(originalImageBase64, jigsawImageBase64)
    tax.check_captcha(secretKey, token,moveLeftDistance)
    tax.login('admin', 'admin', moveLeftDistance)
