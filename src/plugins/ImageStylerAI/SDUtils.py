from typing import Dict
from PIL import Image
import httpx
import hashlib
import time
import json
import base64
from io import BytesIO


class SDUtils:
    def __init__(self):
        self.host = "http://127.0.0.1:7860"


    async def img2tags(self, img) -> list:
        api="/tagger/v1/interrogate"
        url=self.host+api
        image_path = 'D:/AI/images/1.jpg'
        model = 'wd-v1-4-moat-tagger.v2'
        threshold = 0.35
        image = Image.open(image_path)
        with open(image_path, 'rb') as file:
            image_data = file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
        data = {
            "image": base64_image,
            "model": model,
            "threshold": threshold
        }
        response = httpx.post(url, json=data)
        if response.status_code == 200: 
            json_data = response.json()
            caption_dict = list(json_data['caption']['tag'].keys())
            print(caption_dict)

        else:
            print('Error:', response.status_code)
            print('Response body:', response.text)
        
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
