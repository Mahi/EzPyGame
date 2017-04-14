import pygame


class Application:
    """The class for creating a :mod:`pygame` application.

    A simple wrapper around :mod:`pygame` for handling its
    initialization and running.  Also makes the scene
    management seamless together with the :class:`scene.Scene` class.

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
        """Initialize the application with initial settings.

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
        """The title to display in the application's window."""
        return pygame.display.get_caption()

    @title.setter
    def title(self, value):
        pygame.display.set_caption(value)

    @property
    def resolution(self):
        """The application's window's resolution."""
        return self._screen.get_size()

    @resolution.setter
    def resolution(self, value):
        self._screen = pygame.display.set_mode(value)

    @property
    def active_scene(self):
        """The currently active scene. Can be ``None``."""
        return self._scene

    def change_scene(self, scene):
        """Change the currently active scene.

        This will change the current scene and invoke
        :meth:`scene.Scene.on_exit` and :meth:`scene.Scene.on_enter`
        methods on the switching scenes. If ``None`` is provided,
        the application will end.

        The scene will change after the next update loop.

        :param scene.Scene|None scene: the scene to change into
        """
        if self.active_scene is not None:
            self.active_scene.on_exit(next_scene=scene)
            self.active_scene._application = None
        self._scene, old_scene = scene, self.active_scene
        if self.active_scene is not None:
            self.active_scene._application = self
            self.active_scene.on_enter(previous_scene=old_scene)

    def run(self, scene=None):
        """Execute the application.

        :param scene.Scene|None scene: scene to start the execution from
        """
        if scene is None:
            if self.active_scene is None:
                raise ValueError('No scene provided')
        else:
            self.change_scene(scene)

        clock = pygame.time.Clock()

        while self.active_scene is not None:

            for event in pygame.event.get():
                self.active_scene.handle_event(event)
                if event.type == pygame.QUIT:
                    self.change_scene(None)  # Trigger Scene.on_exit()
                    return

            dt = clock.tick(self.update_rate)
            self.active_scene.update(dt)

            self.active_scene.draw(self._screen)
            pygame.display.update()
