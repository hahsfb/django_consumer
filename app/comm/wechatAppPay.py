import datetime, random, time, json, string
import hashlib
import requests
import xmltodict

from app.cli.comm.request import Request
from app.cli.comm.utils import random_char
from flask import request
from app.cli.setting import DOMAIN_NAME, APP_KEY, SHOPPING_APPID, SHOPPING_SECRET, DOMAIN_NAME_BIZ, WX_MCH_ID, WX_PLAN_ID


# 接口API URL前缀
API_URL_PREFIX = 'https://api.mch.weixin.qq.com'
# 下单地址URL
UNIFIEDORDER_URL = "/pay/unifiedorder"
# 查询订单URL
ORDERQUERY_URL = "/pay/orderquery"
# 关闭订单URL
CLOSEORDER_URL = "/pay/closeorder"
# 代扣申请扣款
PAPPAYAPPLY = "/pay/pappayapply"
# 代扣退款接口
REFUND = "/secapi/pay/refund"


def random_digits_num(st,num):
    res = []
    for i in range(num):
        print(i)
        res.append(random.choice(st))
    return ''.join(res)


class WechatAppPay:

    def __init__(self, appid=SHOPPING_APPID, mch_id=WX_MCH_ID, key=APP_KEY, plan_id=WX_PLAN_ID):
        # 公众账号ID
        self.appid = appid
        # 商户号
        self.mch_id = mch_id
        # 支付密钥
        self.key = key
        # 代扣模板ID
        self.plan_id = plan_id
        # 支付结果回调通知地址
        self.notify_url = DOMAIN_NAME + '/v2/callback/wechat'
        # 免密签约回调通知地址
        self.mm_notify_url = DOMAIN_NAME + '/v2/call_back'
        # 代扣扣款回调地址
        self.dk_notify_url = DOMAIN_NAME_BIZ + "/v2/dk_call_back"
        # 随机字符串
        self.nonce_str = None
        # 签名
        self.sign = None
        # 商品描述
        self.body = None
        # 商户订单号
        self.out_trade_no = None
        # 支付总金额
        self.total_fee = 0
        # 终端IP
        self.spbill_create_ip = None

        # 交易类型
        self.trade_type = None
        # 用户OPENID
        self.openid = None
        # 证书路径
        self.SSLCERT_PATH = None
        self.SSLKEY_PATH = None

    def unified_order(self, params):
        """
        下单方法
        params 下单参数
        :return:
        """
        self.body = params['body']
        self.out_trade_no = params['out_trade_no']
        self.total_fee = str(params['total_fee'])
        self.trade_type = params['trade_type']
        self.openid = params['openid']
        self.nonce_str = random_char(32)
        self.spbill_create_ip = request.remote_addr
        if len(self.body) == 1:
            goods = self.body[0]
        else:
            goods = self.body[0]+"等"
        # 参数
        param = {
            "appid": self.appid,
            "mch_id": self.mch_id,  # 商户号
            "nonce_str": self.nonce_str,  # 随机字符串
            "body": goods,  # 支付说明
            "out_trade_no": self.out_trade_no,  # 自己生成的订单号
            "total_fee": self.total_fee,
            "spbill_create_ip": self.spbill_create_ip,  # 发起统一下单的ip
            "notify_url": self.notify_url,
            "trade_type": self.trade_type,  # 小程序写JSAPI
            "openid": self.openid,
        }
        # 获取签名数据
        sign = self.make_sign(param)
        param["sign"] = sign  # 加入签名
        # 调用接口
        param = {'root': param}
        xml = xmltodict.unparse(param)
        url = API_URL_PREFIX + UNIFIEDORDER_URL
        result = self.post_xml_curl(xml, url)
        if 'result_code' in result.keys() and result['result_code'] and 'err_code' in result.keys() and result['err_code']:
            result['err_msg'] = self.error_code(result['err_code'])
        return result


    def make_signing(self):
        now_time = str(time.mktime(datetime.datetime.now().timetuple()))[:-2]
        # data = request.values
        data = request.data.decode()
        # print(data, type(data))
        contract_code = random_digits_num(string.digits, 32)

        # contract_display_account = data.get("openid")
        contract_display_account = json.loads(data)["openid"]
        print(contract_display_account)
        request_serial = now_time + ''.join(random.sample(string.digits,2))

        param = {
            "appid": self.appid,
            "contract_code": contract_code,
            "contract_display_account": contract_display_account,
            "mch_id": self.mch_id,
            "notify_url": self.mm_notify_url,
            "plan_id": self.plan_id,
            "request_serial": request_serial,
            "timestamp": now_time,
        }

        sign = self.make_sign(param=param)
        param["request_serial"] = int(request_serial)
        param["sign"] = sign
        return param

    def pay_contract_inquiry(self, contract_id):
        import xmltodict, requests
        url = "https://api.mch.weixin.qq.com/papay/querycontract"
        param = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "version": "1.0",
            "contract_id": contract_id,
        }
        sign = self.make_sign(param)
        param["sign"] = sign
        param = {"xml": param}
        post_data = xmltodict.unparse(param)
        response = requests.post(url=url, data=post_data.encode("utf-8"), headers={'Content-Type': 'text/xml'})
        response.encoding = 'utf-8'
        result = xmltodict.parse(response.text)
        contract_state = result["xml"]["contract_state"]

        return json.dumps({"contract_state": contract_state})

    # 扣款接口
    def apply_for_deduction(self, contract_id, payment, out_trade_no, goods_names):
        url = self.API_URL_PREFIX + self.PAPPAYAPPLY
        # print(request.remote_addr)
        if len(goods_names) == 1:
            goods = str(goods_names[0])
        else:
            goods = str(goods_names[0]) + "等"
        param = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "nonce_str": random_char(32),
            "body": goods,
            "out_trade_no": out_trade_no,
            "total_fee": str(payment),
            "spbill_create_ip": "115.192.23.211",
            "notify_url": self.dk_notify_url,
            "trade_type": "PAP",
            "contract_id": str(contract_id)
        }
        sign = self.make_sign(param)
        param["sign"] = sign
        param["total_fee"] = payment
        post_data = xmltodict.unparse({"xml": param})
        response = requests.post(url, data=post_data.encode("utf-8"), headers={'Content-Type': 'text/xml'})
        res = response.text
        xml = xmltodict.parse(res)

        return json.dumps({"xml": xml["xml"]})

    def refund(self, out_trade, total_fee, refund_fee):
        url = self.API_URL_PREFIX + self.REFUND
        print(url)
        param = {
            "appid": self.appid,
            "mch_id": self.mch_id,
            "nonce_str": random_char(32),
            "out_trade_no": str(out_trade),
            "out_refund_no": random_char(64),
            "total_fee": str(total_fee),
            "refund_fee": str(refund_fee),
        }
        print(param)
        sign = self.make_sign(param)
        param["sign"] = sign
        param["total_fee"] = int(total_fee)
        param["refund_fee"] = int(refund_fee)
        print(type(param), param)
        post_data = xmltodict.unparse({"xml": param})
        print(post_data)
        path = "./app/cli/comm/cert/"
        cert = (path + 'apiclient_cert.pem', path + 'apiclient_key.pem')
        response = requests.post(url, data=post_data.encode("utf-8"), cert=cert, headers={'Content-Type': 'text/xml'})

        return response

    def make_sign(self, param):
        """
        生成签名
        :param param:
        :return:
        """
        st = []

        ks = sorted(param.keys())
        # 参数排序
        for k in ks:
            st.append(k + '=' + str(param[k]) + '&')
        # 拼接商户KEY
        string_sign_temp = ''.join(st) + "key=" + self.key
        # md5加密
        hash_md5 = hashlib.md5(string_sign_temp.encode('utf-8'))
        sign = hash_md5.hexdigest().upper()
        return sign

    @staticmethod
    def post_xml_curl(xml, url):
        """
        发送xml请求
        :param url:
        :param xml:
        :param param:
        :return:
        """
        # dict 2 xml
        response = requests.post(url, data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'}, timeout=30.0)
        response.encoding = 'utf-8'
        # xml 2 dict
        if response:
            msg = response.text
            xmlmsg = xmltodict.parse(msg)
            print(xmlmsg)
            return xmlmsg['xml']
        else:
            return False

    def get_order_status(self, out_trade_no):
        url = self.API_URL_PREFIX + self.ORDERQUERY_URL
        # 参数
        param = {
            "appid": self.appid,
            "mch_id": self.mch_id,  # 商户号
            "nonce_str": random_char(32),  # 随机字符串
            "out_trade_no": out_trade_no,  # 自己生成的订单号
        }
        # 获取签名数据
        sign = self.make_sign(param)
        param["sign"] = sign  # 加入签名
        # 调用接口
        param = {'root': param}
        xml = xmltodict.unparse(param)
        result = self.post_xml_curl(xml, url)
        if 'result_code' in result.keys() and result['result_code'] and 'err_code' in result.keys() and result['err_code']:
            result['err_msg'] = self.error_code(result['err_code'])
        return result

    @staticmethod
    def error_code(code):
        errList = {
            'NOAUTH': '商户未开通此接口权限',
            'NOTENOUGH': '用户帐号余额不足',
            'ORDERNOTEXIST': '订单号不存在',
            'ORDERPAID': '商户订单已支付，无需重复操作',
            'ORDERCLOSED': '当前订单已关闭，无法支付',
            'SYSTEMERROR': '系统错误!系统超时',
            'APPID_NOT_EXIST': '参数中缺少APPID',
            'MCHID_NOT_EXIST': '参数中缺少MCHID',
            'APPID_MCHID_NOT_MATCH': 'appid和mch_id不匹配',
            'LACK_PARAMS': '缺少必要的请求参数',
            'OUT_TRADE_NO_USED': '同一笔交易不能多次提交',
            'SIGNERROR': '参数签名结果不正确',
            'XML_FORMAT_ERROR': 'XML格式错误',
            'REQUIRE_POST_METHOD': '未使用post传递参数 ',
            'POST_DATA_EMPTY': 'post数据不能为空',
            'NOT_UTF8': '未使用指定编码格式',
        }
        if code in errList.keys():
            return errList[code]


class OpenidUtils:
    def __init__(self, appid=None, secret=None):
        self.url = "https://api.weixin.qq.com/sns/jscode2session"
        self.appid = appid if appid else SHOPPING_APPID
        self.secret = secret if secret else SHOPPING_SECRET

    def get_openid(self, jscode=None):
        url = self.url + "?appid=" + self.appid + "&secret=" + self.secret + "&js_code=" + jscode + "&grant_type=authorization_code"
        print(url)
        result = Request.get(url)
        return result
