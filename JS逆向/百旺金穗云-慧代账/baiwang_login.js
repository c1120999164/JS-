const CryptoJS = require('crypto-js')

// var captchaVerification = this.secretKey ? aesEncrypt(this.backToken+'---'+JSON.stringify({x:this.moveLeftDistance,y:5.0}),this.secretKey):this.backToken+'---'+JSON.stringify({x:this.moveLeftDistance,y:5.0})

function aesEncrypt(data, key) {
    var key = CryptoJS.enc.Utf8.parse(key);
    var srcs = CryptoJS.enc.Utf8.parse(data);
    var encrypted = CryptoJS.AES.encrypt(srcs, key, {mode:CryptoJS.mode.ECB,padding: CryptoJS.pad.Pkcs7});
    return encrypted.toString();
}

function get_pointJson(secretKey,moveLeftDistance){
    return secretKey ? aesEncrypt(JSON.stringify({x:moveLeftDistance,y:5.0}),secretKey):JSON.stringify({x:moveLeftDistance,y:5.0})

}

function get_captchaVerification(secretKey,backToken,moveLeftDistance) {
    return secretKey ? aesEncrypt(backToken+'---'+JSON.stringify({x:moveLeftDistance,y:5.0}),secretKey):backToken+'---'+JSON.stringify({x:moveLeftDistance,y:5.0})
}

// a = get_captchaVerification(123,1234,1234)
// console.log(a);
// console.log(123);

