class Scene:
    """An individual scene in the application.

    Create a scene by subclassing and overriding any of the methods.
    The hosting :class:`application.Application` instance is accessible
    through the :attr:`application` property.

    Example usage with two scenes interacting:

    .. code-block:: python

        class Menu(Scene):

            def __init__(self):
                self.font = pygame.font.Font(...)

            def on_enter(self, previous_scene):
                self.application.title = 'Main Menu',
                self.application.update_rate = 30

            def draw(self, screen):
                pygame.draw.rect(...)
                text = self.font.render(...)
                screen.blit(text, ...)

            def handle_event(self, event):
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

            def on_enter(self, previous_scene):
                self.previous_scene = previous_scene
                self.application.title = 'The Game!',
                sefl.application.update_rate = 60

            def draw(self, screen):
                self.player.draw(screen)
                for enemy in self.enemies:
                    ...

            def update(self, dt):
                self.player.move(dt)
                ...
                if self.player.is_dead():
                    self.application.change_scene(self.previous_scene)
                elif self.player_won():
                    self.application.change_scene(...)

            def handle_event(self, event):
                ...  # Player movement etc.

    You can also use class variables to define custom application
    settings for when the scene is entered:

    .. code-block:: python

        class MyScene(Scene):
            title = 'My Awesome Scene'
            resolution = (640, 480)
            update_rate = 60

    Any of these can be left out (defaults to ``None``) to not override
    that particular setting. If you do override :meth:`on_enter`, you
    must call ``super().on_enter(previous_scene)`` in the subclass.

    These settings can further be overridden in individual instances:

    .. code-block:: python

        my_scene0 = MyScene()
        my_scene0.resolution = (1280, 720)
        my_scene1 = MyScene(title='My Second Awesome Scene')
    """
    title = None
    resolution = None
    update_rate = None

    def __init__(self, title=None, resolution=None, update_rate=None):
        """Initialize the scene.

        :attr:`application` is still ``None`` at this point. Application
        related initialization should be done in :meth:`on_enter`.
        """
        self._application = None
        if title is not None:
            self.title = title
        if resolution is not None:
            self.resolution = resolution
        if update_rate is not None:
            self.update_rate = update_rate

    @property
    def application(self):
        """The host application that's currently running the scene."""
        return self._application

    def draw(self, screen):
        """Override this with the scene drawing.

        :param pygame.Surface screen: screen to draw the scene on
        """

    def update(self, dt):
        """Override this with the scene update tick.

        :param int dt: time in milliseconds since the last update
        """

    def handle_event(self, event):
        """Override this to handle an event in the scene.

        All of :mod:`pygame`'s events are sent here, so filtering
        should be applied manually in the subclass.

        :param pygame.event.Event event: event to handle
        """

    def on_enter(self, previous_scene):
        """Override this to initialize upon scene entering.

        The :attr:`application` property is initialized at this point,
        so you are free to access it through ``self.application``.
        Stuff like changing resolution etc. should be done here.

        If you do override this method and want to use class variables
        to change the application's settings, you must call
        ``super().on_enter(previous_scene)`` in the subclass.

        :param Scene|None previous_scene: previous scene to run
        """
        for attr in ('title', 'resolution', 'update_rate'):
            value = getattr(self, attr)
            if value is not None:
                setattr(self.application, attr.lower(), value)

    def on_exit(self, next_scene):
        """Override this to deinitialize upon scene exiting.

        The :attr:`application` property is still initialized at this
        point. Feel free to do saving, settings reset, etc. here.

        :param Scene|None next_scene: next scene to run
        """
