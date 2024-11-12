import requests
from bs4 import BeautifulSoup
from headers import headers
from loguru import logger
import random
import time

# 隧道域名:端口号
tunnel = "p440.kdlfps.com:18866"

# 用户名密码方式
username = "f2021834041"
password = "28c5qs2e"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}

proxies = None


def send(url, msg=""):
    call_time = 1
    while True:
        logger.info(f"request url:[{url}], call_time:<{call_time}>, msg: {msg}")
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            # 找到 title 标签
            title = soup.title.get_text()
            if title == 'Just a moment...':
                random_sleep()
                call_time += 1
                continue

            return soup
        except Exception as e:
            logger.error(f"request url:[{url}], call_time:<{call_time}> failed, error: {e}")
            random_sleep()
            call_time += 1


def random_sleep():
    time.sleep(random.randint(1, 3))
