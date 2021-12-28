import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_height
from tiles import Tile, StaticTile, Crate, Coin, Palm, Clouds
from enemy import Enemy
from decoration import Sky, Water

class Level:
	def __init__(self, level_data, surface):
		# general setup
		self.display_surface = surface
		self.world_shift = 0

		# player
		player_layout = import_csv_layout(level_data['player'])
		self.player = pygame.sprite.GroupSingle()
		self.goal = pygame.sprite.GroupSingle()
		self.player_setup(player_layout)

		# terrain setup
		terrain_layout = import_csv_layout(level_data['terrain'])
		self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

		# grass setup
		grass_layout = import_csv_layout(level_data['grass'])
		self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

		# crates
		crate_layout = import_csv_layout(level_data['crates'])
		self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

		# coins
		coin_layout = import_csv_layout(level_data['coins'])
		self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

		# foreground palm  trees
		fg_palm_layout = import_csv_layout(level_data['fg palms'])
		self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'fg palms')

		# background palm trees
		bg_palm_layout = import_csv_layout(level_data['bg palms'])
		self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

		# enemy
		enemy_layout = import_csv_layout(level_data['enemies'])
		self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

		# contraints
		constraint_layout = import_csv_layout(level_data['constraints'])
		self.contstraint_sprites = self.create_tile_group(constraint_layout, 'constraint')

		# decoration
		self.sky = Sky(8)
		level_width = len(terrain_layout[0]) * tile_size
		self.water = Water(screen_height - 30, level_width)
		self.clouds = Clouds(400, level_width, 20)

	def create_tile_group(self, layout, type):
		sprite_group = pygame.sprite.Group()

		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				if val != '-1':
					x = col_index * tile_size
					y = row_index * tile_size

					if type == 'terrain':
						terrain_tile_list = import_cut_graphic('./graphics/terrain/terrain_tiles.png')
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'grass':
						grass_tile_list = import_cut_graphic('./graphics/decoration/grass/grass.png')
						tile_surface = grass_tile_list[int(val)]
						sprite = StaticTile(tile_size, x, y, tile_surface)

					if type == 'crates':
						sprite = Crate(tile_size, x, y)

					if type == 'coins':
						if val == '0':
							sprite = Coin(tile_size, x, y, './graphics/coins/gold')
						elif val == '1':
							sprite = Coin(tile_size, x, y, './graphics/coins/silver')

					if type == 'fg palms':
						if val == '0':
							sprite = Palm(tile_size, x, y, './graphics/terrain/palm_small', 38)
						elif val == '1':
							sprite = Palm(tile_size, x, y, './graphics/terrain/palm_large', 64)

					if type == 'bg palms':
						sprite = Palm(tile_size, x, y, './graphics/terrain/palm_bg')

					if type == 'enemies':
						sprite = Enemy(tile_size, x, y)

					if type == 'constraint':
						sprite = Tile(tile_size, x, y)

					sprite_group.add(sprite)

		
		return sprite_group

	def player_setup(self, layout):
		for row_index, row in enumerate(layout):
			for col_index, val in enumerate(row):
				x = col_index * tile_size
				y = row_index * tile_size
				if val == '0':
					print('player goes here')
				if val == '1':
					hat_surface = pygame.image.load('./graphics/character/hat.png').convert_alpha()
					sprite = StaticTile(tile_size, x, y, hat_surface)
					self.goal.add(sprite)


	def enemy_collision_reverse(self):
		for enemy in self.enemy_sprites.sprites():
			if pygame.sprite.spritecollide(enemy, self.contstraint_sprites, False):
				enemy.reverse()

	def run(self):
		# sky
		self.sky.draw(self.display_surface)
		self.clouds.draw(self.display_surface, self.world_shift)
		
		# background palms
		self.bg_palm_sprites.draw(self.display_surface)
		self.bg_palm_sprites.update(self.world_shift)

		# terrain
		self.terrain_sprites.draw(self.display_surface)
		self.terrain_sprites.update(self.world_shift)

		# crate
		self.crate_sprites.draw(self.display_surface)
		self.crate_sprites.update(self.world_shift)

		# enemies
		self.contstraint_sprites.update(self.world_shift)
		self.enemy_sprites.draw(self.display_surface)
		self.enemy_sprites.update(self.world_shift)
		self.enemy_collision_reverse()

		# grass
		self.grass_sprites.draw(self.display_surface)
		self.grass_sprites.update(self.world_shift)

		# coins
		self.coin_sprites.draw(self.display_surface)
		self.coin_sprites.update(self.world_shift)

		# foreground palms
		self.fg_palm_sprites.draw(self.display_surface)
		self.fg_palm_sprites.update(self.world_shift)

		# player sprites
		self.goal.draw(self.display_surface)
		self.goal.update(self.world_shift)

		# water
		self.water.draw(self.display_surface, self.world_shift)