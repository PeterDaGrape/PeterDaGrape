numstudent = 3
numtest = 3
total = 0
for i in range(numtest):
	print('Please input the scores for test', (i + 1))
	testscore = 0
	for j in range(numstudent):
		print('Student', j + 1)
		score = int(input())
		testscore += score
		total += score
	print('The class average is:', testscore / numstudent)
print('The year average is: ', total / (numtest * numstudent))
