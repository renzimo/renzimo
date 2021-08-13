# import json
# import requests
# from Common.my_logger import do_logger
#
#
# def send_requests(method, url, data=None, token=None):
#     """
#
#     :param method:
#     :param url:
#     :param data:字典形式的数据。
#     :param token:
#     :return:
#     """
#     do_logger.info("发起一次HTTP请求")
#     # 得到请求头
#     headers = __handle_header(token)
#     # 得到完整的url - 拼接url
#     url = url
#     # 请求数据的处理 - 如果是字符串，则转换成字典对象。
#     data = __pre_data(data)
#     # 将请求数据转换成字典对象。
#     do_logger.info("请求头为：{}".format(headers))
#     do_logger.info("请求方法为：{}".format(method))
#     do_logger.info("请求url为：{}".format(url))
#     do_logger.info("请求数据为：{}".format(data))
#     # 根据请求类型，调用请求方法
#     method = method.upper()  # 大写处理
#     if method == "GET":
#         res = requests.get(url, data, headers=headers)
#     else:
#         res = requests.post(url, json=data, headers=headers)
#     do_logger.info("响应状态码为：{}".format(res.status_code))
#     do_logger.info("响应数据为：{}".format(res.json()))
#     return res
#
#
# def __handle_header(token=None):
#     """
#     处理请求头。加上项目当中必带的请求头。如果有token，加上token。
#     :param token: token值
#     :return: 处理之后headers字典
#     """
#     headers = {
#         "cookie": "_bl_uid=a9kpjnwUlOtc0k41sfsjv6bp07qb",
#         "accept-language": "zh-CN,zh;q=0.9",
#         "referer": "https://paas-os.mayitest.cn/user/login?redirect=https%3A%2F%2Fpaas-os.mayitest.cn%2Fuser%2Flogin",
#         "sec-fetch-dest": "empty",
#         "sec-fetch-mode": "cors",
#         "sec-fetch-site": "same-origin",
#         "origin": "https://paas-os.mayitest.cn",
#         "content-type": "application/json;charset=utf-8",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
#         "sec-ch-ua-mobile": "?0",
#         "authorization": "Basic bWF5aWhyb3Btc3B1YmxpYzo5Yks0ekVFSUVJVDY4N3E4",
#         "accept": "application/json",
#         "authority": "paas-os.mayitest.cn"
#     }
#     if token:
#         headers["authorization"] = "bearer {}".format(token)
#     return headers
#
#
# # def __pre_url(url):
# #     """
# #     拼接接口的url地址。
# #     """
# #     base_url = conf.get("server", "base_url")
# #     if url.startswith("/"):
# #         return base_url + url
# #     else:
# #         return base_url + "/" + url
#
#
# def __pre_data(data):
#     """
#     如果data是字符串，则转换成字典对象。
#     """
#     if data is not None and isinstance(data, str):
#         # 如果有null，则替换为None
#         if data.find("null") != -1:
#             data = data.replace("null", "None")
#         # 使用eval转成字典.eval过程中，如果表达式有涉及计算，会自动计算。
#         data = eval(data)
#     return data
#
#
# if __name__ == '__main__':
#     login_url = "https://paas-os.mayitest.cn/opms/uaa/api/oauth/password-noCaptcha"
#     login_datas = {"username":"admin","password":"EddBlREhk25pmTHxXfQSFFB0jDE4/07QhdC7CBm77JEie+CZxctvkcevbhj9o+/SjU8KKrHLS/v/FsuJ1IiSPrIjYzF9zY6k7mQVn7pvsrFXWY1VKYiQ11i50MofbXxO8qAWFzXQNMH8UNTcxul+kUFiofv1nSzrnO50s7U803Y=","grant_type":"password"}
#     resp = send_requests("POST", login_url, login_datas)
#     access_token = resp.json()["access_token"]
#
#     recharge_url = "https://paas-os.mayitest.cn/opms/uaa/api/users/current"
#     recharge_data = {}
#     resp = send_requests("get", recharge_url, recharge_data, access_token)
#     print(resp.json())
