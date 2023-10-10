'''
multiplier = int(input('Please enter the value you wish to multiply: '))
start = int(input('Please enter the starting value: '))
end = int(input('Please enter the end value:'))
for i in range(start, end):
	print(multiplier, 'x', i, '=', multiplier * i)
'''



pword = []
pword = [0] * 3
def getPword(attempt):
	valid = False
	while valid == False:
		if attempt == 1:
			pword[attempt] = str(input('Please enter a password: '))
		if attempt == 2:	
			pword[attempt] = str(input('Please enter password again: '))
		length = len(str(pword[attempt]))
		if length >= 6 and length <= 8:
			return(pword[attempt])
			print('Valid')
			valid = True
		else:
			print('The password should be between 6 and 8 characters.')
passwd1 = getPword(1)

while not passwd1 == getPword(2):
	print('Passwords do not match, try again.')
	continue
print('The password change has been successful.')

			

		
		


