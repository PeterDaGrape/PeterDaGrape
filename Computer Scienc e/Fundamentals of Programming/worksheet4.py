'''
t = (56, 12, 33, 8, 3, 2, 98 )
product = 0

for i in range(0, len(t)):

	product += t[i]
	
print(product)

'''

'''
list = [None] * 5

for i in range(len(list)):
	list[i] = input('Please enter a number: ')
list.reverse()
print(list)
'''
'''
numbers = []

for i in range(8):
	add = int(input('Enter positive or negative number: '))
	if add > 0:
		numbers.append(add)
numbers.reverse()
print(numbers)
'''

numbers = []
indexes = []
for i in range(4):
	inp = input('enter a number: ')
	try:
		num = int(inp)
	except:
		num = float(inp)
		indexes.append(i)		
	numbers.append(inp)
print(indexes)
print(numbers)



'''
array = [[0 for i in range(6)] 0 for i in range(6)]

for r in range(6):
	for c in range(4):
		array[r][c] = 'x'

print(array)
'''
