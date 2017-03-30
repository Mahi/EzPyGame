# EzPyGame

## Introduction

`EzPyGame` aims to make the usage of [`pygame`](https://www.pygame.org/)
easier and more pythonic than before.  It implements easy scene management tools and an application class for initializing `pygame` and running scenes easily.


## Installation

    pip install ezpygame


## Usage

Create your scenes by subclassing `ezpygame.Scene` class and overriding the following methods (everything is optional, so override only the ones you actually need):

 - `draw(self, app, screen)`
 - `update(self, app, dt)`
 - `handle_event(self, app, event)`
 - `on_enter(self, app, previous_scene)`
 - `on_exit(self, app, next_scene)`

Now create an `ezpygame.Application` instance and start the program's execution from any scene instance you want:

    app = ezpygame.Application(update_rate=60)  # 60 fps!
    main_menu = MenuScene()
	app.run(main_menu)

Scenes can be switched by using the `Scene.change_scene(scene)` method.


## Example usage

    import ezpygame
	import pygame


	class Menu(ezpygame.Scene):

		def draw(self, app, screen):
			screen.blit(...)
			...

		def handle_event(self, app, event):
			if event.type == pygame.MOUSEDOWN and ...:
				self.change_scene(Game(...))

		def on_enter(self, app, previous_scene):
			app.update_settings(size=(640, 480))


	class Game(ezpygame.Scene):

		def __init__(self, bar, ...):
			super().__init__()
			self.foo = bar
			...

		def draw(self, app, screen):
			...

		def update(self, app, dt):
			self.player.move(dt)
			...

		def handle_event(self, app, event):
			...
			if self.player.died():
				self.change_scene(self.previous_scene)

		def on_enter(self, app, previous_scene):
			self.previous_scene = previous_scene
			app.update_settings(size=(1280, 720))


    app = ezpygame.Application('My Application', (640, 480), update_rate=30)
	menu = Menu()
	app.run(menu)
