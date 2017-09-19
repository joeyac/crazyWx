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


# 音量调到50%并打开网易云
def music():
    call(["amixer", "-D", "pulse", "sset", "Master", "on"])
    call(["amixer", "-D", "pulse", "sset", "Master", "50%"])
    call('netease-cloud-music')


# 使用Ubuntu 16.04 自带 notify-send
# 不过需要更新，原版有bug
# http://www.webupd8.org/2016/05/customize-notifyosd-notification.html
# 可以通过notify osd config来调整notify dialog参数
# 终端输入notify-send --help查看帮助
def notification(user, text=None):
    avatar_dir = os.path.join(os.getcwd(), 'avatar')
    if not os.path.isdir(avatar_dir):
        os.mkdir(avatar_dir)

    avatar = os.path.join(avatar_dir, user.puid + '.jpg')

    if not os.path.exists(avatar):
        user.get_avatar(avatar)

    if not os.path.exists(avatar):
        # https://wiki.ubuntu.com/NotificationDevelopmentGuidelines
        # part: How do I get these slick icons
        avatar = 'notification-message-im'

    name = user.name
    if len(name) > 10:
        name = name[:10] + '...'

    call(['notify-send', name, text, '-i', avatar, '-t', '3000', '-a', 'crazyWx'])


if __name__ == '__main__':
    print(hitokoto())
