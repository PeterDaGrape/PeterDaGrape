'''
while True:
    list = []
    for i in range(2):
        list.append(input('Enter a number. '))
        if 'stop' in list:
            break
    try:
        for i in range(2):
            list[i] = int(list[i])
    except:
        print('Only use integer')
    try:
        print(list[0] / list[1])
    except:
        print('An error occurred, try again... ')
        continue



while True:
    list = []
    try:
        for i in range(2):
            list.append(int(input('Please enter number. ')))
        break
    except ValueError:
        print('Please only enter integers. ')
print(list[0]+list[1])
'''





fast, medium, slow = 0, 0, 0
while True:
    timeTaken = int(input('Enter time. '))
    if timeTaken == 0:
        break
    elif timeTaken < 30:
        fast += 1
    elif timeTaken < 60:
        medium += 1
    else:
        slow += 1
print(fast, medium, slow)
