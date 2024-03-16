from typing import Dict
import httpx
import hashlib
import time
import json
import qrcode
from io import BytesIO


class SDUtils:
    def __init__(self, token: str, user_id: str):
        self.token = token
        self.user_id = user_id
        self.ts = str(int(time.time()))
        self.host = "https://afdian.net/api"

    async def img_to_tags(self, img) -> list:
        path = "/open/query-order"
        
        request_params = {"params": params,
                          "user_id": self.user_id, "ts": self.ts, "sign": sign}
        response = httpx.get(self.host+path, params=request_params)
        plan_meta = json.loads(response.text)['data']['list']
        return plan_meta

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
