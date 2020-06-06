from snake import Snake

snake_game = Snake(screen_size=800, board_size=20, max_fps=12)

num_games = 3

for game in range(num_games):
	state = snake_game.reset()
	snake_game.render()

	while not snake_game.gameover:
		action = snake_game.user_action()
		state, reward, done = snake_game.step(action)
		snake_game.render()

snake_game.finish()