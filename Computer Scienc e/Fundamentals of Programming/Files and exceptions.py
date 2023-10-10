def write(mode, name, write):
	with open (name, mode) as file_object:
		file_object.write(write)

def read(filename):
	with open(filename) as file_object:
		return file_object.read()


write('a', 'programming.txt', 'something\n')
write('a', 'programming.txt', 'else\n')
print(read('programming.txt'))
