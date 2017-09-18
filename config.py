# -- coding: utf-8 --
import os
import datetime
import logging
import logzero

DEBUG = True

TRAINING_END = datetime.datetime(2017, 10, 29)

# iso weekday, where Monday is 1 and Sunday is 7.
WEEKLY_SPECIAL = 6

# daily busy time, list with [ [st_hour, st_minute, et_hour, et_minute], [...], ...]
DAILY_IN_BUSY = [
    {'st': [9, 0], 'et': [18, 30]},
    {'st': [19, 30], 'et': [22, 0]}
]
# means I am busy from 9.00 to 18.30 and 19.30 to 22.00 everyday expect Saturday before 2017.10.29

###########################

NOW = datetime.datetime.now()

TRAINING_END_STRING = TRAINING_END.strftime('%Y-%m-%d')

INFO_STRING = '非常抱歉，我在{end}之前有竞赛集训，可能无法及时回复您的消息。\n\n' \
              '您可以直接给我留言～\n\n' \
              '或者，你可以回复"robot"关键字，然后与我的机器人玩耍(回复"exit"退出)~\n\n' \
              'Tips: 关键字“一言”、“讲个故事”、“北京天气”等，请自行探索~\n\n' \
              'enjoy！'

INFO_STRING = INFO_STRING.format(end=TRAINING_END_STRING)

API_KEY = 'b2195ca4d67841ff8ca74ce1aada9860'

# None for no status, exist for 'reminded'
# REMINDED_FILE_PATH = os.path.join(os.getcwd(), 'reminded.json')
# None for no status, 0 for message mode, 1 for robot mode
STATUS_FILE_PATH = os.path.join(os.getcwd(), 'status.json')


# path where received image, file ... saved to
DATA_PATH = os.path.join(os.getcwd(), 'data')

if DEBUG:
    logzero.loglevel(logging.DEBUG)
else:
    logzero.loglevel(logging.WARNING)


fmt = '%(color)s[%(asctime)s <%(module)s:%(funcName)s>:%(lineno)d] [%(levelname)s]%(end_color)s - %(message)s'
formatter = logzero.LogFormatter(color=True, datefmt='%Y%m%d %H:%M:%S', fmt=fmt)
file_formatter = logzero.LogFormatter(color=False, datefmt='%Y%m%d %H:%M:%S', fmt=fmt)

logzero.formatter(formatter)

logzero.logfile(filename='crazyWx.log', formatter=file_formatter,
                maxBytes=1000000, backupCount=3)

# logzero.logfile(filename='warning.log', formatter=file_formatter,
#                 maxBytes=1000000, backupCount=3, loglevel=logging.WARNING)


logzero.logger.debug("crazyWx init")

if __name__ == '__main__':
    print(DATA_PATH)
    print(TRAINING_END_STRING)
