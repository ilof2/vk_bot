from app import app, db
from models import User
from flask import request
from bot import Bot
from classes.keyboard import Keyboard
import keys, arguments
import random

bot = Bot(keys.TOKEN)

groups_spec_kbrd = Keyboard(arguments.specializace)

week_day_kbrd = Keyboard(arguments.DAYS_for_kbrd)

answers = {
	'help': 'Напишите полное название вашей группы (ПО711, Ро611) и затем день недели (вт, вторник либо 2)',

	'chgroup': 'Первые 2 бувы своей специальности:',

	'full_group': 'Полное название вашей группы:',

	'day': 'День недели для группы {}:',

	'errgroup' : 'Ошибка группы. Вы не ввели группу',
}

def number_of_week():
	from datetime import datetime
	week = datetime.now().isocalendar()[1]
	date = datetime.today().strftime("%d/%m/%Y")
	if week%2 == 0:
		return 'Сегодня, {}. Четная неделя\n'.format(date)
	return 'Сегодня, {}. Нечетная неделя\n'.format(date)

def find_day(message):
	message = str(message)
	for days in arguments.DAYS:
		for day in days:
			if message.lower() == day:
				return days[0]
	return None

def reader(user_group, day):
	with open('groups/{0}/{1}'.format(day, user_group), 'r') as file:
		return file.read()

def add_user(user_id, user_group):
	usr = User.query.filter(User.user_id == user_id).first()
	if not usr:
		user = User(user_id=user_id, user_group = user_group)
		db.session.add(user)
		db.session.commit()

def parsing(message, user_id):
	user_id = str(user_id)
	message = message.upper()
	if message.lower() == 'сменить группу' or message.lower()=='начать':
		User.query.filter(User.user_id == user_id).delete()
		db.session.commit()
		return {"keyboard": groups_spec_kbrd.get_body(), "message": answers['chgroup']}

	elif message.lower() == '/help' or message.lower() == '/помощь':
		return {"keyboard": groups_spec_kbrd.get_body(), "message": answers['help']}

	elif message in arguments.specializace:
		groups_num_kbrd = Keyboard(arguments.gnums[message])
		return {"keyboard": groups_num_kbrd.get_body(), "message": answers['full_group']}

	elif message in arguments.group_full:
		add_user(user_id, message)
		return {"keyboard": week_day_kbrd.get_body(), "message": answers['day'].format(message)}

	elif find_day(message):
		try:
			user_group = User.query.filter_by(user_id=user_id).first().user_group
			msg = number_of_week() + reader(find_day(message), user_group)
			return {"keyboard":week_day_kbrd.get_body(), "message": msg}
		except:
			return {"keyboard": groups_spec_kbrd.get_body(), "message": answers['errgroup']}

	else:
		return {"keyboard": groups_spec_kbrd.get_body(), "message": answers['help']}



@app.route('/bot', methods = ['POST', 'GET'])
def main():
	if request.method == 'POST':
		r = request.get_json()
		print(r)
		if not r:
			return 'ne ok'
		elif r['type'] == 'confirmation':
			return keys.CONFIRMATION_KEY

		elif r['type'] == 'message_new':
			params = {
				'user_id': r['object']['peer_id'],
				'message' : r['object']['text']
			}
			pars = parsing(params['message'], params['user_id'])
			print('message: ',params['message'])
			print('answer: ',pars['message'])
			bot.send_message(params['user_id'], pars['message'], kbrt = pars['keyboard'], random_id = random.randint(100000000, 999999999))
			return 'ok'
	else:
		return 'ne ok'


@app.route('/')
def index():
	return '<h1>hello</h1>'
