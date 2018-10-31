import os
import view
from models import User
from app import db

db.create_all()

for ide in os.listdir(path="./tmp"):
	if User.query.filter(User.user_id==ide):
		with open('tmp/' + ide, 'r') as file:
			view.add_user(ide, file.read())
	

