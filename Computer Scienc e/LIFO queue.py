queue = []
for i in range(5):
    queue.append(input('Enter guest name: '))
for i in range(len(queue)-1, -1, -1):
    print(queue[i])