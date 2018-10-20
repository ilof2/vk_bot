import json

class Keyboard():

	def __init__(self, buttons):
		self.body = {"one_time": False,"buttons": [[self.get_btn('сменить группу', 'positive')]]}
		self.buttons = buttons

	def get_body(self):
		return json.dumps(self.body, indent=2, ensure_ascii = False)

	#spliting list for kbrd vk (should be less than 4 elements in line)
	def __parting_list(self):
		C = []
		for button in self.buttons:
			C.append(self.get_btn(button, 'primary'))

		half = len(C)//2
		return C[:half], C[half:]
		
	# constructor for btn
	def get_btn(self, text, color):
		btn = { 
        		"action": { 
          			"type": "text", 
          			"payload": "{\"button\": \"1\"}", 
       				"label": "" 
        			}, 
				"color": "primary" 
				}
		btn['action']['label'] = text
		btn['color'] = color
		return btn

	# creating table of btn
	def create_table(self):
		len_list = len(self.buttons)
		if self.buttons:
			if len_list == 1:
				self.body = {"one_time": False,"buttons": [[self.get_btn(self.buttons[0], 'primary')],[self.get_btn('сменить группу', 'positive')]]}
			else:
				A, B = self.__parting_list()
				self.body['buttons'].insert(0, B)
				self.body['buttons'].insert(0, A)
		else:
			pass