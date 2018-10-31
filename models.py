from app import db


class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, unique = True)
	user_group = db.Column(db.String(5))


	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)


	def __repr__(self):
		return '<user_id: {0}, user_group: {1}'.format(self.user_id, self.user_group)