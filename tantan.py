from PIL import ImageGrab
import requests
import time
import hashlib
import base64
from urllib import parse
import mouse

print('请在图像左上角位置点击鼠标')
mouse.wait(button='left', target_types=('down'))
x = mouse.get_position()
print('采集左上角坐标成功，请在图像右下角位置点击鼠标')
mouse.wait(button='left', target_types=('down'))
y = mouse.get_position()
print(x, y)
print('采集图像位置成功，请在喜欢位置点击鼠标')
mouse.wait(button='left', target_types=('down'))
l = mouse.get_position()
print('采集喜欢位置成功，请在不喜欢位置点击鼠标')
mouse.wait(button='left', target_types=('down'))
b = mouse.get_position()
print('采集不喜欢位置成功，采集结束！')

AppID = '2110221337'
AppKey = 'gz2ngtWEEkrJ8DCL'
ApiUrl = 'https://api.ai.qq.com/fcgi-bin/face/face_detectface'


def getReqSign(params):
    url = ''
    for key in sorted(params.keys()):
        url += "%s=%s&" % (key, parse.quote(str(params[key]), safe=''))
    sign_str = url + 'app_key=' + AppKey
    return hashlib.md5(sign_str.encode('utf-8')).hexdigest().upper()


def face_test(img_base64):
    params = {
        'app_id': AppID,
        'mode': 0,
        'time_stamp': int(time.time()),
        'nonce_str': int(time.time()),
        'image': img_base64.decode("utf-8")
    }
    params['sign'] = getReqSign(params)
    res = requests.post(
        ApiUrl,
        data=params
    )
    res_json = res.json()
    if res_json['ret'] == 0:
        return(res_json['data']['face_list'][0]['beauty'])
    else:
        return(400)

while True:
    ImageGrab.grab((x[0], x[1], y[0], y[1])).save(r'C:\facej.png')
    img = open(r'C:\facej.png', 'rb')
    img_data = img.read()
    img_data = base64.b64encode(img_data)
    facevalue = face_test(img_data)
    if facevalue > 200:
        print('程序未检测到人脸，将点击不喜欢')
        mouse.move(b[0], b[1])
        mouse.click()
    else:
        if facevalue > 75:
            print('颜值评分:',facevalue,'程序将点击喜欢')
            mouse.move(l[0], l[1])
            mouse.click()
        else:
            print('颜值评分:',facevalue,'程序将点击不喜欢')
            mouse.move(b[0], b[1])
            mouse.click()
    time.sleep(1)
