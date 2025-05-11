import numpy as np
from lemming_game import Game, MAZE_BANK

maze = MAZE_BANK['simple'] # alternately 'bottleneck' and 'open_trap'

game = Game(maze, max_episodes=8)

num_games = 10

present_state = game.reset()

for i in range(num_games):

    actions = game.sample_actions()

    rewards, next_state, terminated, truncated, info =  game.step(actions)

    done = terminated or truncated

    if not done:
        print(f'Game Step: {i}:')
        print(f'Episode Rewards: {rewards}')
        print(f'Info: {info}')
        game.render()

    if done:
        print("🎯 Game Over: ", "Terminated" if terminated else "Truncated")
        print(f"Final Reward: {rewards}")
