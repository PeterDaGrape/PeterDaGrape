
numbers = [0 for i in range(3) ]

def compare(num1, num2):
	if numbers[num1] < numbers[num2]:
		print('Index', num1, 'is less than index', num2)
		
	else:
		print('Index', num1, 'is greater than index', num2)

for i in range(3):
	numbers[i] = input('Please enter a number: ')
	
compare(0, 1)
compare(1, 2)
compare(2, 0)

'''

def find_min(num1, num2):
	if num1 > num2:
		return num1
	elif num1 < num2:
		return num2
	else:
		return (0)
		
		
print(find_min(205, 200))
'''
