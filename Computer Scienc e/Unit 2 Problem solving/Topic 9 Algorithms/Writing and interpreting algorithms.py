total = 0
number = [0] * 3
valid = False
for i in range(3):
	number[i] = int(input('Please enter 3 numbers: '))
	total += number[i]		
if total % 3 == 0:

	for i in range(3):
		if (number[i] - 1) in number:
			valid = False
			print('Invalid')
			break
			
		else:
			valid = True

else:
	print('invalid')
			

if valid == True:
	print('congrats')

