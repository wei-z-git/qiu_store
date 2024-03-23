from typing import Dict
from PIL import Image
import httpx
from io import BytesIO
import webuiapi
import base64
from PIL import Image


class SDUtils:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "7860"
        self.model = 'wd-v1-4-moat-tagger.v2'
        self.threshold = 0.35
        self.protocol = "http"

    async def img2tags(self, img_base64) -> str:
        api = "/tagger/v1/interrogate"
        url = f"{self.protocol}://{self.host}:{self.port}{api}"
        data = {
            "image": img_base64,
            "model": self.model,
            "threshold": self.threshold
        }
        # Get tags and serialize
        json_data = httpx.post(url, json=data).json()
        # 取出tags, 并拼接为str
        caption_dict = json_data['caption']['tag'].keys()
        caption_str = ', '.join(caption_dict)
        return caption_str

    async def img2img(self, tags, img_pil) -> bytes:
        api = webuiapi.WebUIApi(host=self.host, port=self.port)
        result = api.img2img(
            images=[img_pil], prompt=tags, seed="-1", cfg_scale=6.5, denoising_strength=0.6)
        result_img = result.image
        img_byte_array = BytesIO()
        result_img.save(img_byte_array, format='PNG')
        result_bytes = img_byte_array.getvalue()
        return result_bytes
