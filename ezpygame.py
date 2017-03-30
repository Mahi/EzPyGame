"""Easier and more pythonic usage of :module:`pygame`."""

import pygame


class Application:
    """A :module:`pygame` application.

    Simple wrapper around :module:`pygame` to make the initialization,
    deinitialization, and scene management seamless.
    """

    def __init__(self, title='EzPyGame App', size=(640, 480), update_rate=30):
        """Initialize the application with window settings.

        :param str title: title to display in the window's title bar
        :param tuple[int, int] size: size of the screen
        :param int update_rate: how many times per second to update
        """
        pygame.init()
        self._screen = pygame.display.set_mode(size)
        pygame.display.set_caption(title)
        self._update_rate = update_rate

    def update_settings(self, *, title=None, size=None, update_rate=None):
        """Update the application's settings.

        :param str title: title to display in the window's title bar
        :param tuple[int, int] size: size of the screen
        :param int update_rate: how many times per second to update
        """
        if title is not None:
            pygame.display.set_caption(title)
        if size is not None:
            self._screen = pygame.display.set_mode(size)
        if update_rate is not None:
            self._update_rate = update_rate

    @property
    def settings(self):
        """Get a dictionary of the application's settings."""
        return {
            'title': pygame.display.get_caption(),
            'size': self._screen.get_size(),
            'update_rate': self._update_rate,
        }

    def run(self, scene):
        """Run the application.

        :param Scene scene: initial scene to start the execution from
        """
        clock = pygame.time.Clock()

        done = False
        while not done:

            scene.draw(self, self._screen)
            pygame.display.update()

            for event in pygame.event.get():
                scene.handle_event(self, event)
                if event.type == pygame.QUIT:
                    done = True

            dt = clock.tick(self._update_rate)
            scene.update(self, dt)

            if scene.is_done():
                scene, old_scene = scene._next_scene, scene
                old_scene.on_exit(self, scene)
                if scene is None:
                    done = True
                else:
                    Scene.__init__(scene)
                    scene.on_enter(self, old_scene)

        pygame.quit()


class Scene:
    """A simple scene for an application.

    Create a scene by subclassing and overriding any needed methods:

        class MyScene(Scene):

            def draw(self, app, screen):
                ...

            def update(self, app, dt):
                ...

            def handle_event(self, app, event):
                ...

            def on_enter(self, app, previous_scene):
                ...

            def on_exit(self, app, next_scene):
                ...
    """

    # Default value for _next_scene so None can be used to stop
    __SENTINEL = object()

    def __init__(self):
        self._next_scene = Scene.__SENTINEL

    def change_scene(self, scene):
        """Change the scene to another one.

        Flags the scene as done (see :method:`is_done`) so that
        :func:`run` knows to change the scene (or exit upon ``None``).

        :param Scene scene: scene that wants focus, or ``None`` to quit
        """
        self._next_scene = scene

    def is_done(self):
        """Is the scene done executing?

        This will return ``True`` after :method:`change_scene` has been
        called, so that :func:`run` knows the scene wants to quit.
        """
        return self._next_scene is not Scene.__SENTINEL

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

        All of :module:`pygame`'s events are sent here, so filtering
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
