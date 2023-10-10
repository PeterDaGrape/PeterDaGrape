
active = True
floorTrigger = [True, True]
if active == True:
    if floorTrigger[0]:
        print('Movement found on floor 1')
    if floorTrigger[1]:
        print('Movement found on floor 2')
    if not floorTrigger[0] and not floorTrigger[1]:
        print('No movement found')
else:
    print('System off')



'''








active = True
floorTrigger = [False, False]
if active == True:
    if floorTrigger[0] or floorTrigger[1]:
        print('Movement found!')
'''