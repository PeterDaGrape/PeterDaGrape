data = [[27], 
			[19, 39], 
	[10, 24, 30, 51], 
[3, 12, 18, 26, 28, 34, 40, 58]]

def recursive(itemSought, thisNode):
		
    try:
       cNode = data[thisNode[0]][thisNode[1]]
       print('Current node is:', cNode)
    except:
        print('Stop')
        return False
    if cNode == itemSought:
        return True
    elif cNode < itemSought:
        print('Less than')
        nNode = [thisNode[0] + 1, 2 * thisNode[1] + 1]
        print('New node is:', nNode)
        return recursive(itemSought, nNode)
    elif cNode > itemSought:
        print('Greater than')
        nNode = [thisNode[0] + 1, 2 * thisNode[1]]
        print('New node is:', nNode)
        return recursive(itemSought, nNode)
    else:
        return False


found = recursive(40, [0, 0])


if found:
	print('Item Found!')
else:
	print("Item wasn't found'")

