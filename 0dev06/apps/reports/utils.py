# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  @Time : 2021/3/11 21:50 
  @Auth : 可优
  @File : utils.py
  @IDE  : PyCharm
  @Motto: ABC(Always Be Coding)
  @Email: keyou100@qq.com
  @Company: 湖南省零檬信息技术有限公司
  @Copyright: 柠檬班
-------------------------------------------------
"""


def get_file_content(full_report_path, size=1024):
    with open(full_report_path) as file:
        while True:
            content = file.read(size)
            if not content:
                break
        yield content
