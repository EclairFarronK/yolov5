# -*- coding: utf-8 -*-
import base64
import json
import time
from decimal import Decimal
from urllib.parse import urlencode
import random
import requests
import pyDes
import cv2
import numpy


class Douyin(object):

    def __init__(self):
        self.key_dict = {
            # '爱神菲黄金胶原蛋白弹润眼膜':0.7,
            # '雅诗兰黛夜间密集修护肌活套装':0.55,
            '肌肤之钥净采洁颜油 200ml 1件': 0.8,

        }

        # self.c_phone = '19810718203'  ###登录账号 --需要手动改
        # self.c_password = 'AA797299'  ###登录密码 --需要手动改
        self.c_token = 'c:app:D7CBC9DAC2C3470CA4AC20948DBEBEC5'

        # 收货地址信息v
        self.c_prov = '广东省'
        self.c_city = '东莞市'
        self.c_area = '东莞市'
        self.c_receiveAddress = '塘厦镇振兴围东兴路175号胡小姐收'
        self.c_receiveName = '胡小姐'
        self.c_receivePhone = '19810718203'
        ##使用积分--自己改
        self.c_point = 0

        self.c_couponId = ''
        self.getip = ''
        self.uuid = ''
        self.weigth = 0
        self.h2 = 0
        self.w2 = 0
        self.heightRatio = 0

    def get_detail_url(self):
        self.getip = self.get_ip()
        print('搜索商品getip---' + self.getip)
        for key, value in self.key_dict.items():
            headers = {
                'host': 'gzolmnp.cdfg.com.cn',
                'referrer': 'https://gzolmnp.cdfg.com.cn',
                'content-type': 'application/x-www-form-urlencoded',
                'Accept-Encoding': 'gzip,compress,br,deflate',
                'Referer': 'https://servicewechat.com/wxa01382f985324e00/48/page-frame.html',
                'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f28) NetType/WIFI Language/zh_CN',
            }
            # params = {
            #     'encryJsonData':'acfZd4KzJllfJW8MsLqo//fwUDhzGyaqb0K5ioonxsJ+6fdSakiKAv8p/0yExmhptrAc3QkSrKi+ZW3u6IyNef+tVyZls27o6HOM+DyJuK1LmfZS75UKmaIfZRMUvMTFEL+9D1TuHUJB8hGd5gx7leXlOW8Vq7LYxOKdUER21x01M33rBpjkIhKayAklUqPtaJGSHJXB67uSrfqsx9hJtd0HAL3heLFboaZfXzAFOrGnqJmYTwcF6SIEAQA/9+rgqF6HwSG5I/hhzn8mkNQ5RBGoZwGqd9hHz5w5+ESTGVgAjxdg8p5JZ1oXJqq8hTUYV76MWQUTfcIfk7eQ6VQdqA=='
            # }
            params = {
                "page": 1, "rows": 20, "deliverType": "2", "categoryId": "", "cateLevel": "",
                "proName": "肌肤之钥净采洁颜油 200ml 1件", "activityId": "", "clsType": 1, "maxPrice": "", "minPrice": "",
                "brandIds": [], "featureIds": [], "couTypeCode": "", "proSkuHasStock": 1, "area": {}
            }
            proxies = {
                "http": 'http://' + self.getip.replace('\r\n', ''),
                "https": 'http://' + self.getip.replace('\r\n', ''),
            }
            try:
                url = 'https://gzolmnp.cdfg.com.cn/app/json/product/getAppProSearchList'
                # print(url)
                params = self.get_encrypt(str(params).encode('utf8'))
                # print(params)
                params2 = {
                    'encryJsonData': params
                }
                res = requests.post(url, headers=headers, data=params2, proxies=proxies, timeout=5)
                print(res.json())
                my_list = res.json()['data']
                # print(my_list)
                my_list = self.get_decrypt(my_list)
                my_list = json.loads(my_list)['list']
                # print(my_list)
                for list in my_list:
                    title = list.get('skuName')
                    stock = list.get('stockNum')
                    barcode = list.get('skuCode')
                    c_salesPrice = list.get('activityPrice')
                    c_estimatePrice = list.get('salePrice')
                    # if c_estimatePrice == 0:
                    #     c_estimatePrice = c_salesPrice
                    # c_discount = round(c_estimatePrice / c_salesPrice, 2)
                    print(key + '--商品名称:' + title + '--库存:' + str(stock) + '--商品编码:' + barcode + '--原价:' + str(
                        c_salesPrice) + '--折扣价:' + str(c_estimatePrice) + '--折扣:')
                    if stock >= 0:
                        print(
                            '-----------------------------------------库存超过1个-----------------------------------------有货')
                        # with ProcessPoolExecutor(4) as pool:
                        #     for i in range(3):
                        #         pool.submit(self.buy_gds(barcode, title, self.c_count))
                        #     pool.submit(self.buy_gds(barcode, title, 8))
                        self.buy_gds(barcode, self.c_count)
                        # requests.get('http://wx.xtuis.cn/8nOTAQrC7dzppZdiuQLGOKjM8.send?text=抢货成功通知！'
                        #               '&desp=已抢到货（'+str(self.c_count)+'个），商品名称：'+title+'--原价：'+str(c_salesPrice)+ '--折扣价：' + str(c_estimatePrice)+'请及时付款！')
                        # self.buy_gds(barcode, self.c_count)
                        # requests.get('http://wx.xtuis.cn/8nOTAQrC7dzppZdiuQLGOKjM8.send?text=抢货成功通知！'
                        #              '&desp=已抢到货（'+str(self.c_count)+'个），商品名称：'+title+'--原价：'+str(c_salesPrice)+ '--折扣价：' + str(c_estimatePrice)+'请及时付款！')
                        res.close()
                        # time.sleep(random.randint(1, 1))
                    else:
                        print('--无货或者折扣大于' + str(value) + '折')
                        res.close()
                        # time.sleep(random.randint(1, 1))
            except Exception as err:
                print('error_get_detail_url---' + str(err))
                time.sleep(random.randint(0, 1))
                self.getip = self.get_ip()
                print('重新获取getip---' + self.getip)
            else:
                print('')

    # 加密
    def get_encrypt(self, c_msg):
        keys2 = b'CRMaq7VphmDFchdj9l0Qe7cc'
        k2 = pyDes.triple_des(keys2, pyDes.ECB, "", pad=None, padmode=pyDes.PAD_PKCS5)
        d2 = k2.encrypt(c_msg)
        # d2 = k2.encrypt('{"page":1,"rows":20,"deliverType":"2","categoryId":"","cateLevel":"","proName":"肌肤之钥净采洁颜油 200ml 1件","activityId":"","clsType":1,"maxPrice":"","minPrice":"","brandIds":[],"featureIds":[],"couTypeCode":"","proSkuHasStock":1,"area":{}}'.encode('utf8'))
        c_resutl = base64.b64encode(d2)
        # print(c_resutl.decode('utf8'))
        return c_resutl.decode('utf8')

    # 解密
    def get_decrypt(self, c_msg):
        keys2 = b'CRMaq7VphmDFchdj9l0Qe7cc'
        k2 = pyDes.triple_des(keys2, pyDes.ECB, "", pad=None, padmode=pyDes.PAD_PKCS5)
        # print('k2----------'+str(k2))
        # d2 = k2.encrypt("137613")
        # print(base64.b64encode(d2))
        # c_test='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'
        c_resutl = base64.decodebytes(c_msg.encode('utf8'))
        e2 = k2.decrypt(c_resutl)
        # print(e2.decode('utf8'))
        return e2.decode('utf8')

    def template_matching(self, img_path, tm_path):
        # 导入图片，灰度化
        img_rgb = cv2.imread(img_path)
        template_rgb = cv2.imread(tm_path)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        tm_gray = cv2.cvtColor(template_rgb, cv2.COLOR_BGR2GRAY)
        # 缺口图去除背景
        h, w = tm_gray.shape
        self.h2, self.w2 = img_gray.shape
        # print('h:' + str(h) + '--w:' + str(w))
        # print('h2:' + str(self.h2) + '--w2:' + str(self.w2))
        # 自适应阈值话
        img_thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 0)
        tm_thresh = cv2.adaptiveThreshold(tm_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 0)
        # 边缘检测
        img_canny = cv2.Canny(img_thresh, 0, 500)
        tm_canny = cv2.Canny(tm_thresh, 0, 500)
        # 模板匹配
        res = cv2.matchTemplate(img_canny, tm_canny, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # print(
        #     'min_val:' + str(min_val) + '--max_val:' + str(max_val) + '--min_loc:' + str(min_loc) + '--max_loc:' + str(
        #         max_loc))
        right_bottom = (max_loc[0] + w, max_loc[1] + h)  # 右下角
        # print('max_loc:' + str(max_loc) + '--right_bottom:' + str(right_bottom))
        self.weigth = max_loc[0]
        # 圈出矩形坐标 max_loc 为左上角的坐标  right_bottom为右下角坐标
        cv2.rectangle(img_rgb, max_loc, right_bottom, (0, 0, 255), 1)
        # 保存处理后的图片
        cv2.imwrite('44.png', img_rgb)

    def get_image(self, image_data, file_path):
        # print(image_data)
        binary_image_data = base64.b64decode(image_data, '-_')
        file_like = numpy.fromstring(binary_image_data, numpy.uint8)
        image = cv2.imdecode(file_like, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(file_path, image)
        print('获取图片成功！')

    def get_ip(self):
        # url = 'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=246522&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
        # url = 'http://http.tiqu.letecs.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&pack=259046&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
        url = 'http://13712302301.user.xiecaiyun.com/api/proxies?action=getText&key=NPA30176D6&count=1&word=&rand=false&norepeat=false&detail=false&ltime=0'
        res = requests.get(url)
        # print('get_ip:'+res.text)
        return res.text

    def getVerifyData(self):
        self.getip = self.get_ip()
        print('验证码getip---' + self.getip)
        headers = {
            'host': 'gzolmnp.cdfg.com.cn',
            'referrer': 'https://gzolmnp.cdfg.com.cn',
            'content-type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'Referer': 'https://servicewechat.com/wxa01382f985324e00/48/page-frame.html',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f28) NetType/WIFI Language/zh_CN',
        }
        params = {"phone": "9a84491d-a3be-4efe-9950-31b5ebf86b6b", "token": self.c_token,
                  "interfaceType": "bindUserWeChatMnpByPhone"}

        proxies = {
            "http": 'http://' + self.getip.replace('\r\n', ''),
            "https": 'http://' + self.getip.replace('\r\n', ''),
        }
        try:
            url = 'https://gzolmnp.cdfg.com.cn/app/json/login/getVerifyData'
            # print(url)
            params = self.get_encrypt(str(params).encode('utf8'))
            # print(params)
            params2 = {
                'encryJsonData': params
            }
            res = requests.post(url, headers=headers, proxies=proxies, data=params2, timeout=5)
            print(res.json())
            my_list = res.json()['data']
            # print(my_list)
            my_list = self.get_decrypt(my_list)
            self.uuid = json.loads(my_list)['uuid']
            backgroundImage = json.loads(my_list)['verifyData'].get('backgroundImage')
            frontImage = json.loads(my_list)['verifyData'].get('frontImage')
            self.heightRatio = json.loads(my_list)['verifyData'].get('heightRatio')
            self.get_image(str(backgroundImage).replace('data:image/png;base64,', ''), '11.png')
            self.get_image(str(frontImage).replace('data:image/png;base64,', ''), '22.png')
            self.template_matching('11.png', '22.png')
            print('uuid:' + str(self.uuid) + '--weigth:' + str(self.weigth) + '--heightRatio：' + str(self.heightRatio))
            err_code = res.json()['status']
            if err_code != 0:
                err_msg = res.json()['info']
                # raise Exception(err_msg)
                # print(err_msg)
                res.close()
            else:
                print('获取验证码成功！')
                res.close()
        except Exception as err:
            print('error_buy_gds---' + str(err))
        else:
            print('')

    def buy_gds(self, barcode, barname, count):
        self.getVerifyData()
        # 生成验证码
        c_pathList = []
        i = 0.00
        while i <= round(self.weigth / self.w2, 2):
            c_xd = {"xd":str(Decimal(i).quantize(Decimal("0.00"))),"yd":float(Decimal(self.heightRatio).quantize(Decimal("0.00"))),"time":time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))}
            # print(c_xd)
            c_pathList.append(c_xd)
            i = round(i + 0.01, 2)

        self.getip = self.get_ip()
        print('下单getip---' + self.getip)

        headers = {
            'host': 'gzolmnp.cdfg.com.cn',
            # 'Connection': 'keep-alive',
            # 'Content-Length': '8094',
            'referrer': 'https://gzolmnp.cdfg.com.cn',
            'content-type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip,compress,br,deflate',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.31(0x18001f28) NetType/WIFI Language/zh_CN',
            # 'Referer': 'https://servicewechat.com/wxa01382f985324e00/48/page-frame.html'
        }
        params = {"orderScene": 4, "carts": [
            {"id": "", "proSkuDistributionId": "", "isGift": 0, "spCode": "", "skuId": "23856",
             "storeOuCode": "1001433001001001001", "number": 1, "selfActivityId": "5433", "checked": "1"}],
                  "userAddress": {"id": 1111202, "objectId": "", "listIndex": 0, "inAppId": "", "limitStart": "",
                                  "userId": 1726482, "userCode": "", "userName": "", "provinceId": "19",
                                  "provinceName": "广东", "cityId": "1655", "cityName": "东莞市", "countryId": "5457",
                                  "countryName": "塘厦镇", "townId": "0", "townName": "", "areaCode": "19_1655_5457_0",
                                  "address": "振兴围", "isDefault": 1, "receiverName": "欧", "mobile": "13238398074",
                                  "zipCode": "", "createTime": "", "addressType": "", "tag": "",
                                  "addressFull": "广东东莞市塘厦镇振兴围", "posx": "", "posy": "", "area": "", "storeOuCode": "",
                                  "isWithinDelivery": "", "houseNumber": "", "addresType": "", "screenAddress": "",
                                  "idLong": 1111202}, "userAddressId": 1111202, "deliveryStatusType": 1,
                  "payDigital": [{"acctType": "Points", "userBalanceDigital": 0, "payDigital": 0}],
                  "platformChannel": "", "channel": "", "payThirdDigital": {"acctType": "cdfPoints", "payDigital": 0},
                  "rfrCode": "FX000228", "pickupId": "", "orderCategory": "", "vipUnitUserCode": "", "rfrCodeType": 1,
                  "extendData": {}, "deliveryType": "2", "couNo": [],
                  "remark": [{"storeOuCode": "1001433001001001001", "remark": ""}],
                  "imgVerifyCode": "{\"pathList\":" + str(json.dumps(c_pathList, ensure_ascii=False)).replace(' ','') + "}"
            , "uuid": self.uuid, "token": self.c_token}

        proxies = {
            "http": 'http://' + self.getip.replace('\r\n', ''),
            "https": 'http://' + self.getip.replace('\r\n', ''),
        }
        try:
            url = 'https://gzolmnp.cdfg.com.cn/app/json/app_shopping_order/submit'
            # print(url)
            print('params--' + str(json.dumps(params, ensure_ascii=False)))
            params = self.get_encrypt(str(json.dumps(params, ensure_ascii=False)).encode('utf8'))
            print(params)
            params2 = {
                'encryJsonData': params
                # 'encryJsonData': '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'
            }
            res = requests.post(url, headers=headers, proxies=proxies, data=params2, timeout=5)
            print(res.json())
            err_code = res.json()['code']
            if err_code != 0:
                err_msg = res.json()['addition']['message']
                # raise Exception(err_msg)
                # print(err_msg)
                res.close()
            else:
                print('---------------------------------------------下单成功！！！！')
                requests.get('http://wx.xtuis.cn/8nOTAQrC7dzppZdiuQLGOKjM8.send?text=脚本1--抢货成功通知！'
                             '&desp=已抢到货（' + str(count) + '个），商品名称：' + barname + '请及时付款！')
                # sendEmail('脚本1--' + barname, count)
                res.close()
        except Exception as err:
            print('error_buy_gds---' + str(err))
        else:
            print('')

    def get_max(self, dicts):
        return (sorted(dict(dicts).items(), key=lambda d: d[1], reverse=True)[0])


if __name__ == '__main__':
    douyin = Douyin()
    try:
        while 1 == 1:
            # douyin.get_detail_url()
            # douyin.getip = douyin.get_ip()
            douyin.buy_gds('01C023338', '', '1')
            # douyin.get_order('01C023338','2')
            # douyin.getVerifyData()
            # time.sleep(random.randint(1, 1))
            # douyin.get_decrypt()
            # douyin.get_encrypt('')
            # yanzheng.yanzheng.get_image(yanzheng,
            #     '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','22.png')
    except Exception as err:
        print('error222' + str(err))
    else:
        print('')
