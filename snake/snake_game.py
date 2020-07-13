import pygame
from collections import deque
from sys import exit
import copy
import random
import time


class Snake:
	def __init__(self, screen_size, board_size, max_fps=None, show_grid=False):
		pygame.init()
		
		screen_size = round(screen_size/board_size)*board_size

		self.display_width = screen_size
		self.display_height = screen_size

		self.screen = pygame.display.set_mode((self.display_width, self.display_height))

		self.size = board_size
		self.snake_size =  screen_size/board_size
		self.snake_size2D = [self.snake_size] * 2
		self.starting_length = 3
		
		self.show_grid = show_grid

		self.action_space = 4

		self.up, self.left, self.down, self.right = 0, 1, 2, 3

		self.gray = (50, 50, 50)
		self.dark_green = (0, 170, 0)
		self.red = (170, 0, 0)
		self.white = (255, 255, 255)

		self.head_color = copy.copy(self.dark_green)
		self.body_color = copy.copy(self.dark_green)

		self.clock = pygame.time.Clock()
		self.max_fps = max_fps
		

	def reset(self):
		self.head_pos = [self.snake_size*int(self.size/4), self.snake_size*int(self.size/2)]
		self.length = copy.copy(self.starting_length)
		self.past_positions = deque([copy.copy(self.head_pos)], maxlen=self.length)

		self.gameover = False
		self.move_dir = self.right

		self.spawn_apple()
		
		self.user_input = False

		return self.create_pix_arr()


	def render(self):
		self.screen.fill(self.gray)

		# render snake
		color = self.head_color
		for pos in self.past_positions:
			pygame.draw.rect(self.screen, color, [pos, self.snake_size2D])
			color = self.body_color

		# render apple
		pygame.draw.rect(self.screen, self.red, [self.apple_pos, self.snake_size2D])
		
		# Renders grid if enabled
		line_width = round(100/self.size)
		if self.show_grid and line_width > 0:
			for type in range(2):
				for line in range(1, self.size):
					# Vertical lines
					if type == 0:
						start = [line*self.snake_size, 0]
						end = [start[0], self.display_height]
					else:
						start = [0, line*self.snake_size]
						end = [self.display_width, start[1]]
					pygame.draw.line(self.screen, self.gray, start, end, line_width)

		# Shows score at top of the screen
		text_size = 50
		text_pos = (self.display_width//2 - text_size//2, 15)
		font = pygame.font.SysFont('Comic Sans MS', text_size)
		text_surface = font.render(str(self.length-self.starting_length), True, self.white)
		self.screen.blit(text_surface, dest=text_pos)

		# Updates the display
		pygame.display.update()


	# Gets user key presses
	def user_action(self):
		start_time = time.time()
		action = self.move_dir
		self.user_input = True
		
		while time.time()-start_time < 1/self.max_fps:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						exit()
					elif event.key == pygame.K_ESCAPE:
						exit()

					if event.key == pygame.K_UP:
						action = self.up
					elif event.key == pygame.K_DOWN:
						action = self.down
					elif event.key == pygame.K_LEFT:
						action = self.left
					elif event.key == pygame.K_RIGHT:
						action = self.right

		return action


	def step(self, action):
		if action % 2 == self.move_dir % 2:
			action = self.move_dir
		else:
			self.move_dir = action

		if action == self.up:
			self.head_pos[1] -= self.snake_size
		elif action == self.down:
			self.head_pos[1] += self.snake_size
		elif action == self.left:
			self.head_pos[0] -= self.snake_size
		elif action == self.right:
			self.head_pos[0] += self.snake_size

		self.game_rules()

		# Returns the pixel_array, reward, and terminal state
		return self.create_pix_arr(), self.get_rew(), self.gameover, {"Head Position": self.head_pos, "Current Size": self.length-self.starting_length}
	
	
	def get_rew(self):
		if self.num_available_pos <= 0: # If board is full (win)
			rew = 10
		elif self.gameover: # Snake is dead
			rew = -1
		elif self.eaten: # Apple is eaten
			rew = self.length/(self.size**2) # value of apple increases and snake length gets longer
		else:
			rew = 0
			
		return rew


	# Creates a representation of the screen that has been shrunk down and normalized
	def create_pix_arr(self):
		pixel_array = [[] for column in range(self.size)]
		for i in range(self.size**2):
			pos = [(i%self.size)*self.snake_size, (i//self.size)*self.snake_size]

			if pos == self.head_pos:
				pixel_array[i%self.size].append(1)

			elif pos in self.past_positions:
				pixel_array[i%self.size].append(0.6)
			elif pos == self.apple_pos:
				pixel_array[i%self.size].append(0.3)
			else:
				pixel_array[i%self.size].append(0)

		return pixel_array


	def game_rules(self):
		# Ends if wall collision
		if not 0 <= self.head_pos[0] < self.display_width or not 0 <= self.head_pos[1] < self.display_height:
			self.gameover = True

		# Calculates if apple is eaten
		if self.head_pos == self.apple_pos:
			self.eaten = True
		else:
			self.eaten = False

		# Adds 1 to length of snake tail if apple is eaten
		if self.eaten:
			self.length += 1
			self.past_positions = deque(copy.copy(self.past_positions), maxlen=self.length)
			
		# Ends game if snake has collided with its tail
		if self.head_pos in list(self.past_positions)[:-1]:
			self.gameover = True

		# Adds head position to tail
		self.past_positions.append(copy.copy(self.head_pos))

		# Respawns the apple if it has been eaten
		if self.eaten:
			self.spawn_apple()

		if self.max_fps is not None:
			if not self.user_input:
				self.clock.tick(self.max_fps)
			else:
				self.user_input = False


	def spawn_apple(self):
		available_pos = []
		for i in range(self.size**2):
			pos = [(i%self.size)*self.snake_size, (i//self.size)*self.snake_size]
			if not pos in self.past_positions:
				available_pos.append(pos)
				
		self.num_available_pos = len(available_pos)
		
		if self.num_available_pos > 0:
			self.apple_pos = random.choice(available_pos)
		else:
			self.gameover = True

			
	def finish(self):
		pygame.quit()

