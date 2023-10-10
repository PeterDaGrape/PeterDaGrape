# Define and set the global variable within a function
def set_global_variable():
    global my_variable
    my_variable = 10

# Modify the global variable within another function
def modify_global_variable():
    global my_variable
    my_variable += 5

# Call the functions
set_global_variable()
modify_global_variable()

# Access and print the modified global variable
print(my_variable)
