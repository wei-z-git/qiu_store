from typing import Dict
import httpx
import hashlib
import time
import json
import qrcode
from io import BytesIO


class AifadianUtils:
    def __init__(self, token: str, user_id: str):
        self.token = token
        self.user_id = user_id
        self.ts = str(int(time.time()))
        self.host = "https://afdian.net/api"

    async def signing(self, params: str) -> str:
        '''
        计算Sign值
        '''
        text = self.token+"params"+params+"ts"+self.ts+"user_id"+self.user_id
        hash_object = hashlib.md5()
        # 更新对象中的字节串,获取十六进制表示的哈希值
        hash_object.update(text.encode())
        sign = hash_object.hexdigest()
        return sign

    async def search_order(self, out_trade_no) -> list:
        '''
        按订单号返回订单详情
        /query-order
        '''
        path = "/open/query-order"
        # 防止格式变为"{'out_trade_no':'xx'}",暂时没有好办法
        params = "{\"out_trade_no\": \"" + out_trade_no + "\"}"
        sign = await self.signing(str(params))
        request_params = {"params": params,
                          "user_id": self.user_id, "ts": self.ts, "sign": sign}
        response = httpx.get(self.host+path, params=request_params)
        plan_meta = json.loads(response.text)['data']['list']
        return plan_meta

    async def get_plans(self) -> list:
        '''
        按page返回plan列表
        '''
        path = "/creator/get-plans"
        request_params = {"user_id": self.user_id}
        response = httpx.get(self.host+path, params=request_params)
        list_data = json.loads(response.text)['data']['sale_list']
        plans = []
        for i, data in enumerate(list_data, 1):
            plan_dict = {
                'id': i,
                'name': data['name'],
                'price': data['price'],
                'desc': data['desc'],
                'plan_id': data['plan_id']
            }
            plans.append(plan_dict)
        return plans

    @staticmethod
    async def generate_QRcode(plan_id) -> bytes:
        '''
        根据plan_id返回QR code
        '''
        plan_text = "https://afdian.net/item/"+plan_id
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(plan_text)
        qr.make(fit=True)
        # 创建PIL图片对象
        img = qr.make_image(fill_color="black", back_color="white")
        # 将PIL图片对象转换为bytes对象
        img_byte_array = BytesIO()
        img.save(img_byte_array, format='PNG')
        qr_code_bytes = img_byte_array.getvalue()
        return qr_code_bytes

    async def get_formatting_plan_list(self) -> str:
        '''
        返回formating后的plan list
        '''
        plan_list = await self.get_plans()
        formatted_data = []
        for item in plan_list:
            formatted_data.append(
                f"编号: {item['id']} \n name: {item['name']} \n 描述：{item['desc']}\n 价格：{item['price']}\n plan_id: {item['plan_id']}")
        formating_plan_list = "\n\n".join(formatted_data)
        return formating_plan_list

    async def deliver_goods(self, out_trade_no: str, url: str) -> str:
        '''
        返回订单号对应商品
        '''
        # 校验订单号
        order_result = await self.search_order(out_trade_no)
        check_result = "CHECK_FAILED" if len(
            order_result) == 0 else "CHECK_PASS"
        if check_result == "CHECK_PASS":
            data = httpx.get(url).json()
            # 查找planid对应的内容
            for item in data:
                if item["plan_id"] == order_result[0]["plan_id"]:
                    goods = item
                    break
            formatted_data = []
            formatted_data.append(
                f"编号: {goods['id']} \n标题：{order_result[0]['plan_title']}\n"
                f"plan_id: {goods['plan_id']} \n订单price: {order_result[0]['show_amount']}\n"
                f"user_id: {order_result[0]['user_id']}\n 网盘链接（将。替换为.）:  {goods['goods_secrets_text']}  ")
            # 链接list
            goods = "".join(formatted_data) 
        else:
            goods = check_result
        return goods

    @staticmethod
    async def convert_message_url(msg: str) -> bytes:
        '''
        将消息中`.`替代为`。`,来规避不能发url的问题
        '''
        msg = msg.replace('.', '。')
        return msg
