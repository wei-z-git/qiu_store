import webuiapi
import base64
from PIL import Image
import io
# create API client
api = webuiapi.WebUIApi()

# create API client with custom host, port
api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)

# create API client with default sampler, steps.
#api = webuiapi.WebUIApi(sampler='Euler a', steps=20)\

image_path = 'D:/AI/images/1.jpg'
image = Image.open(image_path)


# you can also pass username, password to the WebUIApi constructor.
result2 = api.img2img(images=[image], prompt="cute cat", seed="-1", cfg_scale=6.5, denoising_strength=0.6)
x=result2.image
x.show()
# Display the image
# pil_image.show()