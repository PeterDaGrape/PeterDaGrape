global list
list = [1, 2, 3, 4, 5]
global sum
sum = 0
'''
for i in range(len(list)):
    print(list[i])
    sum += list[i]
print(sum)
'''

print(len(list))
pointer = (-1)
value = 0
def recursive(arr):
    global sum
    global pointer
    global value
    print(arr)
    pointer += 1
    listlen = len(arr)
    if pointer != listlen:
        value = recursive(list[pointer])
    else:
        return value
    

    sum += value

    

print(recursive(list[]))




