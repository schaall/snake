# Info
This is an environment designed to be used for training reinforcement learning agents on the game snake. 

![snake](https://media.giphy.com/media/jSEgvTqbb9mqIF8dFE/giphy.gif)

<br>

# Installation
Just run the following code in your terminal or command line to install the toolkit:
```
pip install --upgrade git+https://github.com/schaall/snake.git
```

<br>

# How to use
When the environment is initialized the screen size (what is seen) must be specified as well as the board size (obs space). To see how well the agent performs a frame rate cap can be set so the environment runs at a reasonable speed. There is also the choice of showing a grid which spaces out the rectanges in the snake and makes it look nicer (same as in video above) but slightly hurts performance. 
```
snake_game = Snake(screen_size=800, board_size=20, max_fps=None, show_grid=True) # Initialization
snake_game.max_fps = 12 # Modifies the frame rate
```
<br>

Collecting data from the environment works in a similar way to OpenAI's gym. The observation is a representation of the screen where a 0 denotes an empty square, a 0.3 denotes a square with the tail of the snake, a 0.6 denotes a square with the head of the snake, and a 1 denotes a square with an apple. A reward is given every time the agent eats an apple and the agent is punished when it collides with its tail or a wall.
```
action_space = snake_game.action_space
state = snake_game.reset() # Resets the environment and gets the starting state
state, reward, done, info = snake_game.step(action) # Makes step and returns the next state as well as the reward and whether or not the snake has died

snake_game.render()
```
<br>

The game can also be played using user input as demonstrated below.
```
snake_game.reset()

done = False
while not done:
  action = snake_game.user_action()
  state, reward, done, info = snake_game.step(action)
  snake_game.render()
```
