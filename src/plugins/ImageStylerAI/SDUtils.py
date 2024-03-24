from PIL import Image
import httpx
from io import BytesIO
import webuiapi
import base64
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
from typing import Tuple


class SDUtils:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = "7860"
        self.model = 'wd-v1-4-moat-tagger.v2'
        self.threshold = 0.35
        self.protocol = "http"

    async def download_img(self, img_url: str) -> Tuple[JpegImageFile, str]:
        """通过url下载图片,返回base64 str

        Parameters
        ----------
        img_url : str
            img链接

        Returns
        -------
        Tuple[JpegImageFile, str]
            base64格式图片和PIL图片组成的tuple
        """
        with httpx.Client() as client:
            response = client.get(img_url)
            if response.status_code != 200:
                print(f"下载失败，错误代码：{response.status_code}")
        pil_image = Image.open(BytesIO(response.content))
        image_base64 = base64.b64encode(response.content).decode('utf-8')
        return pil_image, image_base64

    async def img2tags(self, img_base64: str) -> str:
        """将图像转换为tag
        Parameters
        ----------
        img_base64 : str
            base64格式image

        Returns
        -------
        str
            tags,用作后面img2img的prompt
        """
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

    async def img2img(self, tags: str, img_pil: JpegImageFile) -> bytes:
        """通过tag和原始图像生成新图像

        Parameters
        ----------
        tags : str
            img2tag反推得到的tags
        img_pil : JpegImageFile
            原始PIL格式图像
        Returns
        -------
        bytes
            bytes图像
        """
        negative_prompt = (
            "nsfw,logo,text,badhandv4,EasyNegative,"
            "ng_deepnegative_v1_75t,rev2-badprompt,"
            "verybadimagenegative_v1.3,negative_hand-neg,"
            "mutated hands and fingers,poorly drawn face,"
            "extra limb,missing limb,disconnected limbs,"
            "malformed hands,ugly,strange fingers"
        )        
        api = webuiapi.WebUIApi(host=self.host, port=self.port)
        result = api.img2img(
            images=[img_pil], prompt=tags,negative_prompt=negative_prompt, seed="-1", cfg_scale=6.5, denoising_strength=0.6)
        # 获取pil图像
        print(type(img_pil))
        result_img = result.image
        # 将 PIL 图像对象转换为字节
        img_byte_array = BytesIO()
        result_img.save(img_byte_array, format='PNG')
        result_bytes = img_byte_array.getvalue()
        return result_bytes
