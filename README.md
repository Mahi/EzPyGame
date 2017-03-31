# EzPyGame

## Introduction

`EzPyGame` aims to make the usage of [`pygame`](https://www.pygame.org/)
easier and more pythonic than before.  It implements easy scene management tools and an application class for initializing `pygame` and running scenes easily.


## Installation

    pip install ezpygame


## Reference documentation

https://ezpygame.readthedocs.io/


## Quick start

Create scenes by subclassing `ezpygame.Scene` and overriding any of the following methods:

 - `draw(self, app, screen)`
 - `update(self, app, dt)`
 - `handle_event(self, app, event)`
 - `on_enter(self, app, previous_scene)`
 - `on_exit(self, app, next_scene)`

Now create an `ezpygame.Application` instance and start the execution from any scene:

    app = ezpygame.Application(
        title='My First EzPyGame Application!',
        size=(1280, 720),
        update_rate=60,
    )
    main_menu = MenuScene()
    app.run(main_menu)

Scenes can be switched by using the `Application.change_scene(scene)` method:

    class Game(Scene):
        ...

        def on_enter(self, app, previous_scene):
            self.previous_scene = previous_scene
        
        def update(self, app, dt):
            self.player.move(dt)
            if self.player.died():
                app.change_scene(self.previous_scene)
