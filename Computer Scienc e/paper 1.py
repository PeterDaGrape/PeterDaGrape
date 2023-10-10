# Skeleton Program for the end of Yr12 Summer Exam


def displayMenu():
   print("\n1. Add name")
   print("2. Display list")
   print("3. Display list alphabetically")
   print('4. Remove item')
   print("5. Quit")
  
   option = int(input("\nEnter your choice: "))
   while option not in range(1,5):
       option = int(input ("Invalid choice - please re-enter: "))
   return option




def addName(names):
    print("Enter the name to be added to the list")
    newName = input()
 
    index = (maxElements + 1)

    while not index in range(maxElements):
        print("Enter the position in the list to insert the name (1 -", maxElements,"): ")
        index = int(input())-1
        if index in range(maxElements):
            names[index] = newName
        else:
            print("invalid entry - must be between 1 and", maxElements)





def displayNames(names):
   for index in range(maxElements):
      if names[index]:
           print(index+1, names[index])


def displaySort(names):
    alpha = names[:]
    alpha.sort()
    index = 0
    for i in range(maxElements):
        if alpha[i]:
            index += 1
            print(index, alpha[i])
  


# main program
maxElements = int(input('Enter a maximum number of elements: '))

names = [""]*maxElements
choice = 0


while choice != 5:
    choice = displayMenu()
    if choice == 1:
        addName(names)
    elif choice == 2:
        displayNames(names)
    elif choice == 3:
        displaySort(names)
    elif choice == 4:
        remove = input('Please enter index OR exact name to remove: ')
        
        try:
            remove = int(remove)
            print('Removing index: ', remove)
            names[remove - 1] = ''
            
        except:
            remove = str(remove)
            removeIndex = names.index(remove)
            print('Removing item: ', remove, 'At index:', removeIndex+1)
            names[removeIndex] = ''

  




input("\nProgram terminating, press Enter to end ")
