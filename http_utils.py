import requests
import random
import time
import boto3
from bs4 import BeautifulSoup
from headers import get_header
from log import setup_logging

setup_logging()

from loguru import logger

s3 = boto3.client('s3')

# 隧道域名:端口号
tunnel = "161.123.152.115:6360"
username = "fgukdhnx"
password = "jo0h7cocz8pk"

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
            response = requests.get(url, headers=get_header(call_time), proxies=proxies, timeout=10)
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


def download_image_to_s3(url, bucket_name, s3_path):
    call_time = 1
    while True:
        logger.info(f"Downloading image from {url}, call_time: {call_time}")
        try:
            response = requests.get(url, headers=get_header(call_time), proxies=proxies, timeout=10)
            if response.status_code == 200:
                image_data = response.content
                s3.put_object(Bucket=bucket_name, Key=s3_path, Body=image_data)
                return
            elif response.status_code == 403:
                random_sleep()
                call_time += 1
        except Exception as e:
            logger.error(f"Downloading image from {url} failed, error: {e}")
            random_sleep()
            call_time += 1
