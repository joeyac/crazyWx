# -- coding: utf-8 --
import os
import json
from wxpy import *

from logzero import logger

from config import API_KEY
from config import DATA_PATH
from config import INFO_STRING, STATUS_FILE_PATH
from utils import hitokoto, notification, is_busy, music

AUTO_MODE = True
API_CALL_TIME = 0
STATUS = {}

bot = Bot(cache_path=True)

# 启用 puid 属性，并指定 puid 所需的映射数据保存/载入路径
bot.enable_puid('wxpy_puid.pkl')

# 自动消除手机端的新消息小红点提醒
bot.auto_mark_as_read = True

# 配置图灵机器人
tuLing = Tuling(api_key=API_KEY)

cur = None
self = bot.self
coach = ensure_one(bot.search('洪源老师'))
coach_group = [coach]
for group in bot.groups(update=True):
    if coach in group:
        coach_group.append(group)

logger.info('filter coach: %s', coach_group)


@bot.register()
def print_to_terminal(msg):
    sender = msg.member if msg.member else msg.sender

    notification(sender, msg.text)

    logger.info('%s say: %s', sender.name, msg.text)


@bot.register(chats=Friend, msg_types=TEXT)
def reply_friend(msg):
    name = msg.sender.name
    if len(name) > 15:
        name = name[:12] + '...'

    sender = msg.member if msg.member else msg.sender
    notification(sender, msg.text)
    logger.info('%s say: %s', name, msg.text)

    if not AUTO_MODE:
        return
    global API_CALL_TIME, STATUS

    if msg.sender.puid not in STATUS:
        logger.warning('add <%s:%s> to reminded friends list.', msg.sender.puid, msg.sender.name)
        STATUS[msg.sender.puid] = 0
        return INFO_STRING

    text = str(msg.text).lower().strip()

    if 'robot' in text:
        STATUS[msg.sender.puid] = 1
        ret = '徐少年的机器人为您服务！'

    elif 'exit' in text:
        STATUS[msg.sender.puid] = 0
        ret = '已退出自动回复模式！'

    elif STATUS[msg.sender.puid] == 0:
        # ret = '已收到您的留言！'
        ret = None

    else:
        if '一言' in text:
            ret = hitokoto()
        else:
            API_CALL_TIME += 1
            if API_CALL_TIME >= 750:
                logger.warning('api call time reach %s!', API_CALL_TIME)
            ret = tuLing.reply_text(msg)

    if ret:
        logger.info('robot say: %s', ret)
    return ret


@bot.register(chats=Group)
def reply_at_me(msg):
    sender = msg.member if msg.member else msg.sender
    notification(sender, msg.text)

    if not AUTO_MODE:
        return
    global coach_group, API_CALL_TIME
    if coach in msg.sender:
        logger.warning('coach at the group: %s and add it to list', msg.sender.name)
        coach_group.append(msg.sender)
        if msg.is_at:
            msg.reply('Roger.')
        return
    sender = msg.member if msg.member else msg.sender
    if at_me(msg):
        logger.warning('<@me msg> %s say: %s', sender.name, msg.text)
        msg.forward(bot.file_helper, suffix='<@me msg>')
        # text = str(msg.text).lower().strip()
        # if '一言' in text:
        #     return hitokoto()
        # else:
        #     API_CALL_TIME += 1
        #     if API_CALL_TIME >= 750:
        #         logger.warning('api call time reach %s!', API_CALL_TIME)
        #     tuLing.do_reply(msg)


@bot.register(chats=coach_group)
def reply_coach(msg):
    sender = msg.member if msg.member else msg.sender
    notification(sender, msg.text)

    logger.warning('%s say: %s', sender.name, msg.text)
    if not AUTO_MODE:
        return
    if msg.member == coach or msg.sender == coach:
        msg.forward(bot.file_helper, suffix='<coach msg>')
    if at_me(msg):
        msg.forward(bot.file_helper, suffix='<@me msg>')
        msg.reply('Roger.')


@bot.register(chats=None, msg_types=[PICTURE, RECORDING, ATTACHMENT, VIDEO])
def save_file(msg):
    logger.info('from who: %s(%s), msg: %s, filename: %s',
                msg.chat.name, msg.chat.puid,
                msg.text, msg.file_name)

    sender = msg.member if msg.member else msg.sender
    notification(sender, msg.type)

    if not AUTO_MODE:
        return

    file_name = msg.file_name
    if str(file_name).endswith('.png'):
        file_name = str(file_name)[:-3] + 'jpg'

    save_path = os.path.join(DATA_PATH, msg.chat.puid)
    if not os.path.isdir(save_path):
        os.mkdir(save_path)
    save_path = os.path.join(save_path, file_name)
    msg.get_file(save_path=save_path)

    if isinstance(msg.sender, User):
        if msg.sender.puid in STATUS:
            if STATUS['msg.sender.puid'] == 1:
                if msg.type == PICTURE:
                    return '已经收到您的图片～'
                elif msg.type == RECORDING:
                    return '已经收到您的语音～'
                elif msg.type == ATTACHMENT:
                    return '已经收到您的文件～'
                elif msg.type == VIDEO:
                    return '已经收到您的视频～'


@bot.register(chats=self, msg_types=TEXT, except_self=False)
def control(msg):
    global AUTO_MODE, API_CALL_TIME
    text = str(msg.text).lower()
    if text == 'on':
        AUTO_MODE = True
        logger.info('auto mode enabled.')
    elif text == 'off':
        AUTO_MODE = False
        logger.info('auto mode disabled.')
    elif text == '一言':
        return hitokoto()
    elif text == 'test':
        logger.info('test music.')
        music()
    else:
        API_CALL_TIME += 1
        if API_CALL_TIME >= 750:
            logger.warning('api call time reach %s!', API_CALL_TIME)
        tuLing.do_reply(msg)


def image(name):
    image_dir = os.path.join(os.getcwd(), 'image')
    return os.path.join(image_dir, name)


def at_me(msg):
    notify_list = ['@all', '@所有人', '@全体成员', '徐经纬']
    for item in notify_list:
        if item in msg.text:
            return True
    return msg.is_at


def re(text):
    global cur
    if not cur:
        logger.warning('You should set <cur> var first!')
        return
    logger.info('send %s to %s', text, cur.name)
    cur.send(text)


if __name__ == '__main__':
    logger.info('hello crazyWx')
    AUTO_MODE = is_busy()
    API_CALL_TIME = 0

    STATUS = {}
    if not os.path.exists(STATUS_FILE_PATH):
        json.dump(STATUS, open(STATUS_FILE_PATH, 'w'))
    else:
        STATUS = json.load(open(STATUS_FILE_PATH))

    try:
        # 进入 Python 命令行、让程序保持运行
        embed()

        # 或者仅仅堵塞线程
        # bot.join()
    finally:
        json.dump(STATUS, open(STATUS_FILE_PATH, 'w'))
        logger.info('thank you.')
