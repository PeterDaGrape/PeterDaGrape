import numpy as np
import tensorflow as tf

xSize = 7
ySize = 6

gameCounter = 0

grid = np.full((ySize, xSize), 'x')
print(grid)
    

selection = np.full((xSize), 0)




            
def xInput(turn, x):
    for i in range(ySize):

        if grid[i, x] != 'x':
            grid[i - 1, x] = turn
            break
        if i == (ySize - 1):
            grid[i, x] = turn


def winCheck(turn):
   
    

    for i in range(ySize):
        
        for j in range(xSize-3):
            if grid[i, j] != turn:
                continue
            
            if all(grid[i,j:j+4] != grid[i,j]):
                
                return True
    
    # Check columns for 4 in a row
    for i in range(ySize-3):
        for j in range(xSize):
            if grid[i, j] != turn:
                continue
            if all(grid[i:i+4,j] == grid[i,j]):
                return True
    
    # Check diagonals (top left to bottom right) for 4 in a row
    for i in range(ySize-3):
        for j in range(xSize-3):
            if grid[i, j] != turn:
                continue
            if all([grid[i,j] == grid[i+1,j+1] == grid[i+2,j+2] == grid[i+3,j+3]]):
                return True
    
    # Check diagonals (top right to bottom left) for 4 in a row
    for i in range(ySize-3):
        for j in range(3,xSize):
            if grid[i, j] != turn:
                continue
            if all([grid[i,j] == grid[i+1,j+1] == grid[i+2,j+2] == grid[i+3,j+3]]):
                return True
    
    # No 4 in a row found
    return False



def playGame(xPos):
    
    if gameCounter % 2:
        turn = 'R'
    else:
        turn = 'B'

    xInput(turn, xPos)

    print(grid)
    if winCheck(turn) == True:
        if turn == 'r':
            print('Red Wins!')
        else:
            print('Blue Wins!')
        
    
    

    gameCounter += 1






# Define the input and output placeholders
input_array = tf.keras.Input(shape=(2,))
actions = tf.keras.Input(shape=(1,))

# Define the model variables
weights = tf.Variable(tf.random.normal([2, 7]))
bias = tf.Variable(tf.zeros([7]))

# Define the model prediction
def prediction(inputs):
    return tf.nn.softmax(tf.matmul(inputs, weights) + bias)

# Define the loss function
cross_entropy = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
loss = cross_entropy(actions, prediction(input_array))

# Define the optimizer
optimizer = tf.optimizers.SGD(0.01)

# Start a Tensorflow session

# Start a Tensorflow session
for i in range(1000):
    with tf.GradientTape() as tape:
        # Compute the loss
        input_data = grid
        action_data = [0,1,2,3,4,5,6,]
        l = loss(action_data, prediction(input_data))
    
    # Compute the gradients
    grads = tape.gradient(l, [weights, bias])
    
    # Apply the gradients to the variables
    optimizer.apply_gradients(zip(grads, [weights, bias]))

# Use the model to control the game
game_input = grid
action = tf.argmax(prediction(game_input), axis=1)
print(action)

# Evaluate the model's accuracy
accuracy = 1
optimizer.apply_gradients(zip(accuracy, [weights, bias]))



