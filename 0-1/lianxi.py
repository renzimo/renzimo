# list_1 = [ {
#     "code" : "00000000000",
#     "name" : "系统默认"
# }, {
#     "code" : "2MsVTqCIuYl",
#     "name" : "上海帆驰信息技术有限公司"
# }, {
#     "code" : "47A4j4fwJOG",
#     "name" : "小豆豆的企业"
# }, {
#     "code" : "5iDQXoF5eMj",
#     "name" : "woowow"
# }, {
#     "code" : "9j4AaGGf2UB",
#     "name" : "测试一下1"
# }, {
#     "code" : "9j4C8s1QsMN",
#     "name" : "测试一下1"
# }, {
#     "code" : "bZwAR7Hbm8h",
#     "name" : "string"
# }, {
#     "code" : "caec2e8ea6b",
#     "name" : "上海帆驰1"
# } ]
#
# dict_1 = list_1[1]["code"]
# print(dict_1)
headers = {
    "cookie": "_bl_uid=a9kpjnwUlOtc0k41sfsjv6bp07qb",
    "accept-language": "zh-CN,zh;q=0.9",
    "referer": "https://paas-os.mayitest.cn/user/login?redirect=https%3A%2F%2Fpaas-os.mayitest.cn%2Fuser%2Flogin",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "origin": "https://paas-os.mayitest.cn",
    "content-type": "application/json;charset=utf-8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "sec-ch-ua-mobile": "?0",
    "authorization": "Basic bWF5aWhyb3Btc3B1YmxpYzo5Yks0ekVFSUVJVDY4N3E4",
    "accept": "application/json",
    "authority": "paas-os.mayitest.cn"
}
headers["authorization"] = "qqqq"
print(headers)
