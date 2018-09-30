import requests



class Bot():
	def __init__(self, token):
		self.token = token


	def send_message(self, user, text, kbrt = None, random_id = 100000000):
		url = 'https://api.vk.com/method/messages.send'
		answer = {'user_id': user, 'message': text,'keyboard': kbrt, 'access_token':self.token, 'v':5.84}
		r = requests.post(url, params=answer)
		return r.json()

