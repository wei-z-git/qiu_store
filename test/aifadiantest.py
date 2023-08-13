import httpx
import hashlib
import time
import json
token = "xxx"
user_id = "xxx"
ts = str(int(time.time()))
# ts="1688950858"
a="202307271446199849102542803"
params = "{\"out_trade_no\": \"" + a + "\"}"
# params = '{"out_trade_no":"202307271446199849102542803"}'
url = "https://afdian.net/api/open/query-order"
text = token+"params"+params+"ts"+ts+"user_id"+user_id
hash_object = hashlib.md5()
# 更新对象中的字节串
hash_object.update(text.encode())

# 获取十六进制表示的哈希值
sign = hash_object.hexdigest()

print(sign)

request_params = {"params": params, "user_id": user_id, "ts": ts, "sign": sign}
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

# response = httpx.get(url, params=request_params)
# plan_meta = json.loads(response.text)['data']['list']

# print(plan_meta)

response = httpx.get(url, params=request_params)
plan_meta = json.loads(response.text)['data']['list']
