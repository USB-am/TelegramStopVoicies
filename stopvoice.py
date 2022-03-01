import colorama
colorama.init(autoreset=True)
from datetime import datetime
from colorama import Fore, Back
from telethon import TelegramClient, events
from telethon.tl.types import User

import config


import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
					level=logging.WARNING)

selfbot = TelegramClient('session_id', config.API_ID, config.API_HASH)
# selfbot.start(config.PHONE_NUMBER)


__all__ = ('connect', 'disconnect', 'log_list')


class Mail:
	def __init__(self, username, date, exceptions=False):
		self.username = username
		self.date = date
		self.exceptions = exceptions


log_list = [
	Mail('Usbam', '02.03.2022 00:11'),
	Mail('Usbam', '02.03.2022 00:11', AttributeError('Long error text.'))
]


def connect():
	selfbot.start(config.PHONE_NUMBER)
	selfbot.run_until_disconnected()


def disconnect():
	# selfbot.disconnected()
	selfbot.disconnect()


def get_attr(cls, attr_name: str):
	result = cls.__dict__.get(attr_name, '')
	if result is None:
		result = ''

	return result


def get_username(user: User) -> str:
	user_name = '{first_name} {last_name} {username}'.format(
		first_name=get_attr(user, 'first_name'),
		last_name=get_attr(user, 'last_name'),
		username=f'[{Fore.YELLOW}@{get_attr(user, "username")}{Fore.WHITE}]'
	).strip().replace('  ', ' ')

	return user_name


def log(user: User) -> None:
	username = get_username(user)
	date = datetime.now().strftime('%d.%m.%Y %H:%M')
	out = f'{Fore.CYAN}[{date}]{Fore.YELLOW} VOICE {Fore.WHITE}от {username}'
	print(out)


def is_valid_message(event) -> bool:
	id_more_0 = event.chat_id > 0
	not_have_whitelist = event.chat_id not in config.WHITE_LIST
	is_voice = event.message.voice

	if not is_voice:
		return False

	voice_attrs = get_attr(event.message.voice, 'attributes')
	duration_lass_1000 = voice_attrs[0].duration < 1000

	return all([id_more_0, not_have_whitelist, is_voice, duration_lass_1000])


@selfbot.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
	sender = await event.get_sender()
	username = get_username(sender)
	date = datetime.now().strftime('%d.%m.%Y %H:%M')
	print(username)
	log_list.append(Mail('Default: ' + username, date, False))
	print(log_list, end='\n\n')

	if (event.chat_id > 0) and (event.message.voice != None):
		log(sender)

	if is_valid_message(event):
		try:
			await event.respond(config.MESSAGE)
			await selfbot.delete_messages(event.chat_id, [event.id])
			log_list.append(Mail(username, date, False))
		except Excetion as exp:
			print(f'{Fore.RED}Ошибка обработки сообщения: {Fore.WHITE}{exp}')
			log_list.append(Mail(username, date, exp))