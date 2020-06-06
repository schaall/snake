from snake import Snake

# Initializes environment with a 800x800 window on a 20x20 game of snake running at 12fps so that it is playable
snake_game = Snake(screen_size=800, board_size=20, max_fps=12, show_grid=True)

# Number of games you play before environment quits
num_games = 3

for game in range(num_games):

	# Resets environment at beginning of each game
	state = snake_game.reset()

	# Renders the first frame of the game
	snake_game.render()

	while not snake_game.gameover:
		# Gets your action
		action = snake_game.user_action()

		# Plays your action or continues moving straight if no action or an illegal action was made
		state, reward, done = snake_game.step(action)
		
		# Renders new state
		snake_game.render()

# Quits the environment after all games have finished
snake_game.finish()
