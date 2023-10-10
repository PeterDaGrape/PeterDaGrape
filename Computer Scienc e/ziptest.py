list = [5, 2, 10, 57]

for number, i in zip(list, range(len(list))):
    list[i] = input()
    print(number, i)