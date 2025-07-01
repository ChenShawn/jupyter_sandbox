import random
import requests
import base64
from PIL import Image
from io import BytesIO

code_1 = """
import matplotlib.pyplot as plt
x = [1,2,3]
y = [4,8,6]
print(f' [DEBUG] {x=}')

plt.plot(x, y)
plt.title('Debug Plot')
plt.show()
y
"""

code_2 = """
import numpy as np
x = np.array(x)
y = np.array(y)
z = x + y
print(' [DEBUG 123]')
plt.plot(x, z)
plt.title('Debug Plot 2')
plt.show()

print(' [DEBUG 234] {z=}')

plt.plot(x, -z)
plt.title('DEBUG PLOT 3')
plt.show()

print(' [DEBUG 345]')
"""

code_3 = """
import matplotlib.pyplot as plt
from PIL import Image

img = Image.open('highlighted_space.jpg').convert('RGB')
img_crop = img.crop((0, 0, 400, 600))  # Crop the image to a 100x100 square
plt.imshow(img_crop)
plt.axis('off')
plt.show()

img_crop2 = img.crop((400, 600, 800, 1200))  # Crop another part of the image
plt.imshow(img_crop2)
plt.axis('off')
plt.show()
"""

def base64_to_image(base64_string: str) -> Image.Image:
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image

test_sid = 'debug_jupyter_250701'
test_timeout = 5

# res1 = requests.post(
#     # 'http://10.39.10.230:12345/jupyter_sandbox',
#     'http://127.0.0.1:12345/jupyter_sandbox',
#     json={
#         "session_id": test_sid,
#         "code": code_1,
#         "timeout": test_timeout,
#     }
# ).json()

res2 = requests.post(
    # 'http://10.39.10.230:12345/jupyter_sandbox',
    'http://127.0.0.1:12345/jupyter_sandbox',
    json={
        "session_id": test_sid,
        "code": code_3,
        "timeout": test_timeout,
    }
).json()
print(f' [DEBUG #222] {res2.keys()=}')
print(f' [DEBUG #222] {res2["status"]=}')
print(f' [DEBUG #222] {res2["execution_time"]=}')
result_dict = res2['output']
# for k, v in result_dict.items():
#     print(f' [DEBUG #222] {k=}, {len(v)=}')

print(f' [stdout] {result_dict["stdout"]=}')
print(f' [stderr] {result_dict["stderr"]=}')
print(f' [images] {len(result_dict["images"])=}')

for idx, img in enumerate(result_dict['images']):
    img_pil = base64_to_image(img)
    img_pil.save(f'./debug_output/{test_sid}-{idx}.png', format='PNG')

print(' Done!!')

