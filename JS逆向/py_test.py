import requests
import json


headers = {
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
cookies = {
    "SESSION": "b3aea1eb-3ce2-4909-a8ae-a2386ee382dd"
}
url = "https://hdz.baiwangjs.com/captcha/get"
data = {
    "captchaType": "blockPuzzle",
    "clientUid": "slider-e1cc0bea-449d-4c07-88ed-d91b89f45df4",
    "ts": 1728525391029
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, data=data)

# print(response.text)
print(response)