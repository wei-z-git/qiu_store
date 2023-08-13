import qrcode
from PIL import Image

# 定义要转换为二维码的字符串
data = "Hello, world!"

# 创建QRCode对象
qr = qrcode.QRCode(version=1, box_size=10, border=5)

# 将数据添加到QRCode对象中
qr.add_data(data)

# 编译QRCode对象以生成二维码图像
qr.make(fit=True)

# 获取QRCode图像
img = qr.make_image(fill_color="black", back_color="white")

# 定义要保存的图像文件名
filename = "qrcode.png"

# 将QRCode图像保存到文件中
img.save(filename)