import numpy as np
import random

roadLen = 5
num_actions = ['left', 'right']

Q = np.zeros((roadLen, len(num_actions)))

alpha = 0.1
gamma = 0.9
epsilon = 0.1

for episode in range(1000):
    state = 0
    done = False

    print(f"Episode {episode+1}")
    print("Starting at state", state)
    print("Initial Q-table")
    print(Q)
    
    step = 0
    while not done:

        step += 1
        print(f"\nStep: {step}")
        print(f"Current state: {state}")

        if np.random.random() < epsilon:
            action = np.random.randint(0, len(num_actions))
            print(f"Random action chosen: {num_actions[action]}")
        else:
            action = np.argmax(Q[state]) 
            print(f"Greedy action chosen: {num_actions[action]}") 

        if state == 0:
            action = 1 
            print("Go right")
        elif state == roadLen-1:
            action = 0
            print("Go Right")

        next_state = state + (1 if action == 1 else -1 )
        reward = 1 if next_state == roadLen-1 else -0.1 
        print(f"Action taken: {num_actions[action]}")
        print(f"Moving to state: {next_state}")
        print(f"Reward received: {reward}") 

        old_q = Q[state, action]
        Q[state, action] = old_q + alpha * (reward + gamma * np.max(Q[next_state]) - old_q)
        print(f"Updated Q[{state},{action}] from {old_q:.2f} to {Q[state, action]:.2f}")
        print("Updated Q-table:")
        print(np.round(Q, 2))

        state = next_state
        if state == roadLen-1:
            done = True


print("\nTraining completed.")
print("Final Q-table:")
print(np.round(Q, 2))