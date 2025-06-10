import random
import requests

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
print(f' [DEBUG] {z=}')
plt.plot(x, z)
plt.title('Debug Plot 2')
plt.show()
z
"""

test_sid = 'test_jupyter'
test_timeout = 5
res1 = requests.post(
    # 'http://10.39.10.230:12345/jupyter_sandbox',
    'http://127.0.0.1:12345/jupyter_sandbox',
    json={
        "session_id": test_sid,
        "code": code_1,
        "timeout": test_timeout,
    }
).json()
print(f' [DEBUG #111] {res1.keys()=}')
print(f' [DEBUG #111] {res1["status"]=}')
print(f' [DEBUG #111] {res1["execution_time"]=}')
result_dict = res1['output']
for k, v in result_dict.items():
    print(f' [DEBUG #111] {k=}, {len(v)=}')

res2 = requests.post(
    # 'http://10.39.10.230:12345/jupyter_sandbox',
    'http://127.0.0.1:12345/jupyter_sandbox',
    json={
        "session_id": test_sid,
        "code": code_2,
        "timeout": test_timeout,
    }
).json()
print(f' [DEBUG #222] {res2.keys()=}')
print(f' [DEBUG #111] {res2["status"]=}')
print(f' [DEBUG #111] {res2["execution_time"]=}')
result_dict = res2['output']
for k, v in result_dict.items():
    print(f' [DEBUG #111] {k=}, {len(v)=}')
