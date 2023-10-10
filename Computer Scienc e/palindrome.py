word = 'kayak'
letters = []
for letter in(word):
    letters.append(letter)
palindrome = True
for i in range(len(word)-1, -1 ,-1):
    if word[i] != word[len(word)-1-i]:
        palindrome = False
if palindrome == False:
    print('not a palindrome')
else:
    print('Palindrome')
