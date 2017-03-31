"""Easier and more pythonic usage of :mod:`pygame`."""

import pygame


class Application:
    """The class for creating a :mod:`pygame` application.

    A simple wrapper around :mod:`pygame`, which initializes and quits
    :mod:`pygame` as the application starts/ends. Also makes the scene
    management seamless and fun together with :class:`Scene`.

    Example usage:

    .. code-block:: python

        class Menu(ezpygame.Scene):
            ...

        class Game(ezpygame.Scene):
            ...

        app = ezpygame.Application(
            title='My First EzPyGame Application',
            resolution=(1280, 720),
            update_rate=60,
        )
        main_menu = Menu()
        app.run(main_menu)
    """

    def __init__(self,
                 title='EzPyGame App',
                 resolution=(640, 480),
                 update_rate=30):
        """Initialize the application with window settings.

        :param str title: title to display in the window's title bar
        :param tuple[int,int] resolution: resolution of the game window
        :param int update_rate: how many times per second to update
        """
        pygame.init()
        self.update_rate = update_rate
        self._scene = None
        # Trigger property setters
        self.title = title
        self.resolution = resolution

    @property
    def title(self):
        """The title to display in the application's game window."""
        return pygame.display.get_caption()

    @title.setter
    def title(self, value):
        pygame.display.set_caption(value)

    @property
    def resolution(self):
        """The application's game window's resolution."""
        return self._screen.get_size()

    @resolution.setter
    def resolution(self, value):
        self._screen = pygame.display.set_mode(value)

    @property
    def active_scene(self):
        """The currently active scene."""
        return self._scene

    def change_scene(self, scene):
        """Change the currently active scene in the application.

        This will change the current scene and invoke
        :meth:`Scene.on_exit` and :meth:`Scene.on_enter`
        on the switching scenes (unless ``None``).

        The scene will change after the next update.

        :param Scene scene: the scene to change into
        """
        if self.active_scene is not None:
            self.active_scene.on_exit(self, next_scene=scene)
        self._scene, old_scene = scene, self.active_scene
        if self.active_scene is not None:
            self.active_scene.on_enter(self, previous_scene=old_scene)

    def run(self, scene=None):
        """Run the application.

        :param Scene scene: initial scene to start the execution from
        """
        if scene is None:
            if self.active_scene is None:
                raise ValueError('No scene provided')
        else:
            self.change_scene(scene)

        clock = pygame.time.Clock()

        while self.active_scene is not None:

            self.active_scene.draw(self, self._screen)
            pygame.display.update()

            for event in pygame.event.get():
                self.active_scene.handle_event(self, event)
                if event.type == pygame.QUIT:
                    self.change_scene(None)  # Trigger Scene.on_exit()
                    return

            dt = clock.tick(self._update_rate)
            self.active_scene.update(self, dt)


class Scene:
    """An individual scene in the application.

    Create a scene by subclassing and overriding any of the methods.

    Example usage with two scenes interacting:

    .. code-block:: python

        class Menu(Scene):

            def __init__(self):
                self.font = pygame.font.Font(...)

            def on_enter(self, app, previous_scene):
                app.update_settings(title='Main Menu', update_rate=30)

            def draw(self, app, screen):
                pygame.draw.rect(...)
                text = self.font.render(...)
                screen.blit(text, ...)

            def handle_event(self, app, event):
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        game_size = self._get_game_size(event.pos)
                        self.change_scene(Game(game_size))

            def _get_game_size(self, mouse_pos_upon_click):
                ...


        class Game(ezpygame.Scene):

            def __init__(self, size):
                super().__init__()
                self.size = size
                self.player = ...
                ...

            def on_enter(self, app, previous_scene):
                self.previous_scene = previous_scene
                app.update_settings(title='The Game!', update_rate=60)

            def draw(self, app, screen):
                self.player.draw(screen)
                for enemy in self.enemies:
                    ...

            def update(self, app, dt):
                self.player.move(dt)
                ...
                if self.player.is_dead():
                    app.change_scene(self.previous_scene)
                elif self.player_won():
                    app.change_scene(...)

            def handle_event(self, app, event):
                ...  # Player movement etc.
    """

    def draw(self, app, screen):
        """Draw the scene.

        :param Application app: application running the scene
        :param pygame.Surface screen: screen to draw the scene on
        """

    def update(self, app, dt):
        """Update the scene.

        :param Application app: application running the scene
        :param int dt: time in milliseconds since the last update
        """

    def handle_event(self, app, event):
        """Process an event.

        All of :mod:`pygame`'s events are sent here, so filtering
        should be applied manually in the subclass.

        :param Application app: application running the scene
        :param pygame.event.Event event: event to handle
        """

    def on_enter(self, app, previous_scene=None):
        """The scene is entered.

        :param Application app: application running the scene
        :param Scene previous_scene: previous scene to run, or ``None``
        """

    def on_exit(self, app, next_scene=None):
        """The scene is exited.

        :param Application app: application running the scene
        :param Scene next_scene: next scene to run, or ``None``
        """
