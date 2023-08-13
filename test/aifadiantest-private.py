import httpx
import hashlib
import time
import json
token=""
user_id="xxx"
ts=str(int(time.time()))
# ts="1688950858"
params='{"page":1}'
url = "https://afdian.net/api/creator/get-plans"

# text=token+"params"+params+"ts"+ts+"user_id"+user_id
text=token+"ts"+ts+"user_id"+user_id

hash_object = hashlib.md5()
# 更新对象中的字节串
hash_object.update(text.encode())

# 获取十六进制表示的哈希值
sign = hash_object.hexdigest()

print(sign)

request_params = {"user_id":user_id}

# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
plans = []
response = httpx.get(url, params=request_params)
list_data=json.loads(response.text)['data']['sale_list']
for i,data in enumerate(list_data, 1):
    plan_dict = {
        'id': i,
        '商品title': data['name'],
        '商品价格':data['price']
        # '商品_id': data['plan_id']
    }
    plans.append(plan_dict)
print(plans)
    

# https://afdian.net/api/creator/get-plans?album_id=&unlock_plan_ids=
