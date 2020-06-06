# Info
This is an environment designed to be used for training machine learning agents on the game snake. 
![snake](https://media.giphy.com/media/S9ngZazht2WX9VkfMH/giphy.gif)

<br>

# How to use
When the environment is initialized the screen size (what you see) must be specified as well as the board size (obs space). If you would like to see how well the agent performs you can set a frame rate cap so you can actually view what is happening at a reasonable speed. 
```
snake_game = Snake(screen_size=800, board_size=20, max_fps=None) # Initialization
snake_game.max_fps = 12 # Modifies the frame rate
```
<br>

Collecting data from the environment works in a similar way to OpenAI's gym. Note that the state data is scaled and normalized so that no modifications are needed to feed it into the agent
```
action_space = snake_game.action_space
state = snake_game.reset() # Resets the environment and gets the starting state
state, reward, done = snake_game.step(action) # Makes step and returns the next state as well as the reward and whether or not the snake has died

snake_game.render()
```
<br>

You can also play the game yourself by feeding in your action to the step function instead of an agent's
```
action = snake_game.user_action()
```

<br>

# Installation
Just run the following code in your terminal or command line to install the package:
```
pip install git+https://github.com/mfiless/Snake-ML-Env/blob/master/snake.py
```
