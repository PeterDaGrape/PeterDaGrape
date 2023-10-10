data = [2, 5, 4, 1, 3]
queue = []



for i in range(len(data)):
    queue.append(data[i])

print('The print jobs have been added for processing. ', queue)
queue.sort()

print('The queue has been sorted into priority', queue)

for i in range(len(queue)):
    printitem = queue[0]
    queue.pop(0)
    print('printjob', printitem, 'has been sent off for printing')
    if len(queue) == 0:
        print('Print queue is empty', queue)



