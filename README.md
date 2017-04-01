# EzPyGame

`EzPyGame` aims to make the usage of [`pygame`](https://www.pygame.org/)
easier and more pythonic than before.  It implements easy scene management tools and an application class for initializing `pygame` and running scenes easily.


## Installation

    pip install ezpygame


## Quick start

Create scenes by subclassing `ezpygame.Scene` and overriding any of the following methods:

 - `draw(self, screen)`
 - `update(self, dt)`
 - `handle_event(self, event)`
 - `on_enter(self, previous_scene)`
 - `on_exit(self, next_scene)`

Now create an `ezpygame.Application` instance and start the execution from any scene:

```python
app = ezpygame.Application(
    title='My First EzPyGame Application!',
    resolution=(1280, 720),
    update_rate=60,
)
main_menu = MenuScene()
app.run(main_menu)
```

Scenes can be switched by using the `Application.change_scene(scene)` method:

```python
class Game(Scene):
    ...

    def on_enter(self, previous_scene):
        self.previous_scene = previous_scene

    def update(self, dt):
        self.player.move(dt)
        if self.player.died():
            self.application.change_scene(self.previous_scene)
```

## Reference documentation

With more in-depth guide and examples: https://ezpygame.readthedocs.io/
