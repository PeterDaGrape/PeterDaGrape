print('Please choose from the following: ')
print('1 - Economy Car')
print('2 - Saloon Car')
car = str(input('3 - Sports Car  '))
if car == str(1) or car == str(2) or car == str(3):
	print('Your choice is ', car)
	if input('Do you wish to proceed, to confirm what your choice is? y, n    ') == 'y':
		print('Have a nice day')
	else:
		print('Cancelled')
else:
	print('Invalid')
