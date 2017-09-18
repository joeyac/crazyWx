# -- coding: utf-8 --
import os
from wxpy import *
from time import sleep
from logzero import logger
bot1 = Bot(cache_path='wxpy1.pkl')
bot2 = Bot(cache_path='wxpy2.pkl')
bot1.auto_mark_as_read = True
bot2.auto_mark_as_read = True
rec1_dir = os.path.join(os.getcwd(), 'x1')
rec2_dir = os.path.join(os.getcwd(), 'x2')

x1 = bot1.search('小冰')[0]
x2 = bot2.search('小冰')[0]

@bot1.register(chats=x1)
def forward_bot1(msg):
	if msg.type == RECORDING:
		logger.info('bot1 save recording: %s', msg.file_name)
		msg.get_file(os.path.join(rec1_dir, msg.file_name))
		return

	logger.info('bot1 say: %s', msg.text)
	text = msg.text
	if (text.startswith('(') or text.startswith('（')) and (text.endswith(')') or text.endswith('）')):
		logger.warning('ignore %s', text)
		return
	logger.debug('sleep 3s.')
	sleep(3)
	x2.send(text)

@bot2.register(chats=x2)
def forward_bot1(msg):
	if msg.type == RECORDING:
		logger.info('bot2 save recording: %s', msg.file_name)
		msg.get_file(os.path.join(rec2_dir, msg.file_name))
		return

	logger.info('bot2 say: %s', msg.text)
	text = msg.text
	if (text.startswith('(') or text.startswith('（')) and (text.endswith(')') or text.endswith('）')):
		logger.warning('ignore %s', text)
		return
	logger.debug('sleep 3s.')
	sleep(3)
	x1.send(text)

if __name__ == '__main__':
	embed()


