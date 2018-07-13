# CURL-TO-PY
## Transfer curl to python

### This program could transfer almost all curl command to python code.
Currently, you can only input your curl command in the console, later I will make it a website.

How to run: 
```
python /path/to/curl_to_py.py
```

#### Samples of curl to python:

> curl https://api.example.com/surprise -u banana:coconuts -d "sample data"

result:

```python
import requests

headers = {
	'Content-Type' : 'application/x-www-form-urlencoded',
}

fullurl = 'https://api.example.com/surprise'
data='sample data'
url = 'https://api.example.com/surprise'
requests.get(url = url, headers = headers, data = data, auth = {'banana':'coconuts'})
```

> curl -H ':method: GET' -H ':scheme: https' -H ':path: /mobile/v5/sale/property/view?app=i-ajk&cid=14&city_id=14&cv=11.11&entry=14&from=mobile&i=A5235DB5-0411-4DE9-B0C0-201806251624&id=1280061785&idfa=78E32BCA-3A99-42BE-9978-688F0661BAD1&invalid_type=0&is_auction=201&is_standard_house=0&m=iPhone&macid=0f607264fc6318a92b9e13c65db7cd3c&o=iOS&openudid=9cc27361cb287e199f067396a70b6ef654a4ae0b&opt_type=0&ostype2=ios11&pm=A01&qtime=20180625163918&refer=6&source_type=1&udid2=A5235DB5-0411-4DE9-B0C0-201806251624&uuid2=A5235DB5-0411-4DE9-B0C0-201806251624&uuid=A5235DB5-0411-4DE9-B0C0-201806251624&v=11.4' -H ':authority: api.anjuke.com' -H 'cookie: 58tj_uuid=909e0ef1-f30d-4bf6-a270-12e9d6f7de62; init_refer=; new_session=1; new_uv=1; aQQ_ajkguid=02BDF1D9-110D-87E5-1B80-0F53B9246E57; comm_device_info=app%3Di-ajk%3Bimei%3DA5235DB5-0411-4DE9-B0C0-201806251624%3Bmacid%3D0f607264fc6318a92b9e13c65db7cd3c%3Budid2%3DA5235DB5-0411-4DE9-B0C0-201806251624%3Bcv%3D11.11%3Btime%3D1529915591; ctid=14; lps="/bj/prop/vrview?pano_id=eyJwYW5vX2lkIjo5MTg5fQ==&prop_id=1281807561|"; sessid=2251BDCF-7435-5B6D-0405-D8E68FB4644F' -H 'accept: application/json' -H 'content-type: application/json' -H 'accept-language: zh-Hans-CN;q=1, en-CN;q=0.9' -H 'nsign: 1000883f9e04833dfb2b377d763f84ca0e39' -H 'key: d945dc04a511fcd7e6ee79d9bf4b9416' -H 'user-agent: Anjuke/11.11 (iPhone; iOS 11.4; Scale/3.00)' -H 'sig: 303563795882641e4d270b615963d16c' -H 'accept-encoding: br, gzip, deflate' 'https://api.anjuke.com/mobile/v5/sale/property/view?app=i-ajk&cid=14&city_id=14&cv=11.11&entry=14&from=mobile&i=A5235DB5-0411-4DE9-B0C0-201806251624&id=1280061785&idfa=78E32BCA-3A99-42BE-9978-688F0661BAD1&invalid_type=0&is_auction=201&is_standard_house=0&m=iPhone&macid=0f607264fc6318a92b9e13c65db7cd3c&o=iOS&openudid=9cc27361cb287e199f067396a70b6ef654a4ae0b&opt_type=0&ostype2=ios11&pm=A01&qtime=20180625163918&refer=6&source_type=1&udid2=A5235DB5-0411-4DE9-B0C0-201806251624&uuid2=A5235DB5-0411-4DE9-B0C0-201806251624&uuid=A5235DB5-0411-4DE9-B0C0-201806251624&v=11.4'

result:

```python
import requests

headers = {
	':path' : '/mobile/v5/sale/property/view?app=i-ajk&cid=14&city_id=14&cv=11.11&entry=14&from=mobile&i=A5235DB5-0411-4DE9-B0C0-201806251624&id=1280061785&idfa=78E32BCA-3A99-42BE-9978-688F0661BAD1&invalid_type=0&is_auction=201&is_standard_house=0&m=iPhone&macid=0f607264fc6318a92b9e13c65db7cd3c&o=iOS&openudid=9cc27361cb287e199f067396a70b6ef654a4ae0b&opt_type=0&ostype2=ios11&pm=A01&qtime=20180625163918&refer=6&source_type=1&udid2=A5235DB5-0411-4DE9-B0C0-201806251624&uuid2=A5235DB5-0411-4DE9-B0C0-201806251624&uuid=A5235DB5-0411-4DE9-B0C0-201806251624&v=11.4',
	'accept-language' : 'zh-Hans-CN;q=1, en-CN;q=0.9',
	':method' : 'GET',
	'nsign' : '1000883f9e04833dfb2b377d763f84ca0e39',
	'accept' : 'application/json',
	':authority' : 'api.anjuke.com',
	':scheme' : 'https',
	'cookie' : '58tj_uuid=909e0ef1-f30d-4bf6-a270-12e9d6f7de62; init_refer=; new_session=1; new_uv=1; aQQ_ajkguid=02BDF1D9-110D-87E5-1B80-0F53B9246E57; comm_device_info=app%3Di-ajk%3Bimei%3DA5235DB5-0411-4DE9-B0C0-201806251624%3Bmacid%3D0f607264fc6318a92b9e13c65db7cd3c%3Budid2%3DA5235DB5-0411-4DE9-B0C0-201806251624%3Bcv%3D11.11%3Btime%3D1529915591; ctid=14; lps="/bj/prop/vrview?pano_id=eyJwYW5vX2lkIjo5MTg5fQ==&prop_id=1281807561|"; sessid=2251BDCF-7435-5B6D-0405-D8E68FB4644F',
	'key' : 'd945dc04a511fcd7e6ee79d9bf4b9416',
	'sig' : '303563795882641e4d270b615963d16c',
	'user-agent' : 'Anjuke/11.11 (iPhone; iOS 11.4; Scale/3.00)',
	'content-type' : 'application/json',
	'accept-encoding' : 'br, gzip, deflate',
}

fullurl = 'https://api.anjuke.com/mobile/v5/sale/property/view?app=i-ajk&cid=14&city_id=14&cv=11.11&entry=14&from=mobile&i=A5235DB5-0411-4DE9-B0C0-201806251624&id=1280061785&idfa=78E32BCA-3A99-42BE-9978-688F0661BAD1&invalid_type=0&is_auction=201&is_standard_house=0&m=iPhone&macid=0f607264fc6318a92b9e13c65db7cd3c&o=iOS&openudid=9cc27361cb287e199f067396a70b6ef654a4ae0b&opt_type=0&ostype2=ios11&pm=A01&qtime=20180625163918&refer=6&source_type=1&udid2=A5235DB5-0411-4DE9-B0C0-201806251624&uuid2=A5235DB5-0411-4DE9-B0C0-201806251624&uuid=A5235DB5-0411-4DE9-B0C0-201806251624&v=11.4'

payload = {
	'invalid_type' : '0',
	'city_id' : '14',
	'qtime' : '20180625163918',
	'is_auction' : '201',
	'opt_type' : '0',
	'uuid2' : 'A5235DB5-0411-4DE9-B0C0-201806251624',
	'https://api.anjuke.com/mobile/v5/sale/property/view?app' : 'i-ajk',
	'id' : '1280061785',
	'from' : 'mobile',
	'uuid' : 'A5235DB5-0411-4DE9-B0C0-201806251624',
	'cv' : '11.11',
	'refer' : '6',
	'is_standard_house' : '0',
	'ostype2' : 'ios11',
	'source_type' : '1',
	'idfa' : '78E32BCA-3A99-42BE-9978-688F0661BAD1',
	'openudid' : '9cc27361cb287e199f067396a70b6ef654a4ae0b',
	'cid' : '14',
	'i' : 'A5235DB5-0411-4DE9-B0C0-201806251624',
	'm' : 'iPhone',
	'o' : 'iOS',
	'macid' : '0f607264fc6318a92b9e13c65db7cd3c',
	'udid2' : 'A5235DB5-0411-4DE9-B0C0-201806251624',
	'v' : '11.4',
	'entry' : '14',
	'pm' : 'A01',
}
url = 'https://api.anjuke.com/mobile/v5/sale/property/view?app=i-ajk'
requests.get(url = url, headers = headers, params = payload)
```

This program is inspired by  https://github.com/zhexuany/curl-to-py, but his program could not transfer some of my curl commands, so I decide to write a more functional curl to py program with python, that is why I write this program.
