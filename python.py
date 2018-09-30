import csv
def reader(day):
	group = 'РО611'
	filename = 'days_{}/{}.csv'.format(group,day)
	with open(filename, 'r', newline ='') as file:
		table = csv.reader(file)
		for s in table:
			try:
				print(s[0],s[1], s[2], s[3])
			except:
				print(s[0], s[1], s[2])

reader('ср')