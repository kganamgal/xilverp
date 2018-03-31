import web
import oss2
import time
import datetime
import json
import base64
import hmac
from hashlib import sha1 as sha

accessKeyId = '6MKOqxGiGU4AUk44'
accessKeySecret = 'ufu7nS8kS59awNihtjSonMETLI0KLy'
host = 'http://post-test.oss-cn-hangzhou.aliyuncs.com';
expire_time = 30
upload_dir = 'user-dir/'

def get_iso_8601(expire):
    print expire
    gmt = datetime.datetime.fromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt

def get_token():
    now = int(time.time())
    expire_syncpoint  = now + expire_time
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with');
    array_item.append('$key');
    array_item.append(upload_dir);
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    #policy_encode = base64.encodestring(policy)
    policy_encode = base64.b64encode(policy)
    print policy_encode
    h = hmac.new(accessKeySecret, policy_encode, sha)
    sign_result = base64.encodestring(h.digest()).strip()

    token_dict = {}
    token_dict['accessid'] = accessKeyId
    token_dict['host'] = host
    token_dict['policy'] = policy_encode
    token_dict['signature'] = sign_result
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = upload_dir
    web.header("Access-Control-Allow-Methods","POST")
    web.header("Access-Control-Allow-Origin","*")
    #web.header('Content-Type', 'text/html; charset=UTF-8')
    result = json.dumps(token_dict)
    return result

urls = ('/(.*)', 'hello')
app = web.application(urls, globals())
class hello:
    def GET(self, name):
        if not name:
            token = get_token()
            print token
            return token

if __name__ == "__main__":
    app.run()
