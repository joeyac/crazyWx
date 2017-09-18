# -- coding: utf-8 --
from time import sleep
from subprocess import Popen, call, PIPE
from config import *
import requests
import random


def hitokoto():
    choices = ['a', 'b', 'c', 'd']
    # 动画 漫画 游戏 小说
    url = 'https://sslapi.hitokoto.cn/?c=' + random.choice(choices)
    # logger.debug("hitokoto url %s", url)
    response = requests.get(url).json()
    ret = response['hitokoto']
    if 'from' in response:
        ret += '\n——' + response['from']
    return ret


def is_busy():
    if NOW > TRAINING_END or NOW.isoweekday() == WEEKLY_SPECIAL:
        return False
    for item in DAILY_IN_BUSY:
        st = NOW.replace(hour=item['st'][0], minute=item['st'][1])
        et = NOW.replace(hour=item['et'][0], minute=item['et'][1])
        if st < NOW < et:
            return True
    return False


def notification():
    call(["amixer", "-D", "pulse", "sset", "Master", "50%"], stdout=PIPE)
    call('netease-cloud-music')


if __name__ == '__main__':
    print(hitokoto())
