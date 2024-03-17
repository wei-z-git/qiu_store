import httpx
import base64
from PIL import Image


url = 'http://127.0.0.1:7860/tagger/v1/interrogate'
image_path = 'D:/AI/images/1.jpg'
model = 'wd-v1-4-moat-tagger.v2'
threshold = 0.35

#确认照片为上传照片
image = Image.open(image_path)
# image.show()

# 将图片转换为Base64字符串
with open(image_path, 'rb') as file:
    image_data = file.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')

# 构建请求体的JSON数据
data = {
    "image": base64_image,
    "model": model,
    "threshold": threshold
}

# 发送POST请求
response = httpx.post(url, json=data)

# 检查响应状态码
if response.status_code == 200: 
    json_data = response.json()
    # 处理返回的JSON数据
    caption_dict = list(json_data['caption']['tag'].keys())
    print(caption_dict)

else:
    print('Error:', response.status_code)
    print('Response body:', response.text)