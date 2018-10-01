from flask import Flask, request
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from classes.keyboard import Keyboard
from bot import Bot
import arguments
import requests
import keys
import re
import json



app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)

token = keys.TOKEN
bot = Bot(token)

groups_spec_kbrd = Keyboard(arguments.specializace)
groups_spec_kbrd.create_table()
week_day_kbrd = Keyboard(arguments.DAYS)
week_day_kbrd.create_table()


class User(db.Model):

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
	
	def __repr__(self):
		return '<user_id:{}, group:{}>'.format(self.user_id, self.user_group)

	__tablename__ = 'user'
	user_id = db.Column('user_id',db.Integer, primary_key = True)
	user_group = db.Column('user_group', db.String(5))


def reader(day, user_id):
	usr = User.query.filter(User.user_id == user_id).first()
	group = usr.user_group
	filename = 'days_{}/{}'.format(group,day)
	with open(filename, 'r') as file:
		table = file.read()
		return table

def parsing(message, user_id):
	if message == 'перевыбрать группу':
		# while User.query.filter(User.user_id == user_id):
		try:
			User.query.filter(User.user_id == user_id).delete()
			return {"keyboard": groups_spec_kbrd.get_body(), "message": "Вы вернулись в начало, выберите специальность"}
		except:
			return {"keyboard": groups_spec_kbrd.get_body(), "message": "Вы вернулись в начало, выберите специальность"}

	elif message in arguments.specializace:
		groups_num_kbrd = Keyboard(arguments.gnums[message])
		groups_num_kbrd.create_table()
		return{"keyboard": groups_num_kbrd.get_body(), "message": "Выберите номер группы"}

	elif message in arguments.group_full:
		try:
			usr = User(user_id=user_id, user_group=message)
			db.session.add(usr)
			db.session.commit()
			return{"keyboard": week_day_kbrd.get_body(), "message": "Выберите день недели"}
		except:
			return {"keyboard": groups_spec_kbrd.get_body(), "message": "Что-то пошло не так, выберите специальность"}
		

	elif message in arguments.DAYS or User.query.filter(User.user_id == user_id):
		try:
			return{"keyboard":week_day_kbrd.get_body(), "message": reader(message, user_id)}
		except:
			return {"keyboard": groups_spec_kbrd.get_body(), "message": "Выберите специальность"}


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
			print(params['message'])
			print(pars['keyboard'])
			bot.send_message(params['user_id'], pars["message"], kbrt = pars["keyboard"])
			return 'ok'
	else:
		return 'ne ok'


@app.route('/')
def index():
	return '<h1>hello</h1>'






if __name__ == '__main__':
	app.run()