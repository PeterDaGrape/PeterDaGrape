
def recursive2(list):
    
    if len(list) == 0:
        return 0
    else:
        return list[0] + recursive2(list[3:])
    

    


    

value = 0
data = [1, 2, 3, 4, 5]
sum = 0
#print(recursive(data, 0))
print(recursive2(data))