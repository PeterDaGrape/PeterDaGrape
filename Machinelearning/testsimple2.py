import tensorflow as tf
import numpy as np
from collections import deque
import random

# Define the Q-value function
q_value = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation=None)
])
SOT = []
# Create the Q-value model
optimizer = tf.keras.optimizers.Adam(learning_rate=0.005)
rewardQueue = 0
# Define the epsilon-greedy policy
epsilon = 0.05
reward = 0
discount = 0.9
# Define the replay buffer
replay_buffer = deque(maxlen=10000)

# Loop over the episodes
for episode in range(100000):
    rewardQueue = 0
    # Generate a random state
    data = (np.arange(10))
    np.random.shuffle(data)

    #print(data)

    state = data
    done = False
    total_reward = 0
    step = 0
    randomAction = 0
    normalAction = 0
    while not done:
        done = False


        # Choose the action using the epsilon-greedy policy
        if np.random.uniform(0, 1) < epsilon:
            action = np.random.randint(0, 10)
            randomAction += 1
            Random = True
        else:
            q_values = q_value(np.expand_dims(state, axis=0))
            action = np.argmax(q_values)
            normalAction += 1
            Random = False
        
        # Take the action and observe the new state and reward
        next_state = np.random.randint(10, size=(10,))
        
        if step >= 200:
            #print('Never found value')
            done = True
    

        if action == np.argmax(data):
           # print('Found')
            reward = 5
            
            done = True
            
        else:
            #reward = int(data[action] / 2)
            reward = -1



        total_reward += reward
        
        # Add the experience to the replay buffer
        replay_buffer.append((state, action, reward, next_state, done))
        
        # Sample a batch of experiences from the replay buffer
        batch_size = 128
        if len(replay_buffer) >= batch_size:




            batch = random.sample(replay_buffer, batch_size)
            # Compute the target Q-values for the batch
            targets = []
            states = []
            for state, action, reward, next_state, done in batch:
                
                if done:
                    target = reward
                else:
                    next_q_values = q_value(np.expand_dims(next_state, axis=0))
                    max_q_value = np.max(next_q_values)
                    target = reward + discount * max_q_value
                target_q_values = (q_value(np.expand_dims(state, axis=0)))
                target_q_values = target_q_values.numpy()

                target_q_values[0][action] = target
                targets.append(target_q_values)
                states.append(state)

            # Update the Q-value function
            targets = np.vstack(targets)
            states = np.vstack(states)
            with tf.GradientTape() as tape:
                # Compute the loss and gradients
                loss = tf.reduce_mean(tf.square(q_value(states) - targets))
                gradients = tape.gradient(loss, q_value.trainable_variables)
            
            # Apply the gradients
            optimizer.apply_gradients(zip(gradients, q_value.trainable_variables))
            replay_buffer.clear()
        
        # Update the state
        state = next_state
        step += 1  
    # Print the total reward for the episode

    print("Episode {}: Attempts = {}".format(episode, step))
    SOT.append(step)
print(SOT)