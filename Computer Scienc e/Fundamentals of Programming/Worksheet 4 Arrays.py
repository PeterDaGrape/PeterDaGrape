'''
list = []
total = 0
for i in range(6):
	num = input('Please enter the number: ')
	list.append(num)
	total += num
for j in range(6):
	print(list[5-j])
	
print('The total is: ', total)
print('And the average is: ', total / 6)

'''

'''
names = ['James', 'Anthony', 'John', 'Jo', 'Max', 'Funminiyi']



search = str(input('Please enter the name to search: '))
try:
	index = names.index(search) + 1
except:
	index = -1

if not index == -1:
	print('The index of', search, 'is:', index)
else:
	print(search, 'could not be found.')
'''
Outlet1Sales = [10, 12, 15, 10]
Outlet2Sales = [5, 8, 3, 6]
Outlet3Sales = [10, 12, 15, 10]

total1 = 0
total2 = 0
total3 = 0

for i in range(len(Outlet1Sales)):
	total1 += Outlet1Sales[i]
	
for j in range(len(Outlet2Sales)):
	total2 += Outlet2Sales[j]
	
for k in range(len(Outlet3Sales)):
	total3 += Outlet3Sales[k]
	
print('Total for quarter 1 ', total1)
print('Total for quarter 2 ', total2)
print('Total for quarter 3 ', total3)


