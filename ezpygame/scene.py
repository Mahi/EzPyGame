class Scene:
    """An isolated scene which can be ran by an application.

    Create your own scene by subclassing and overriding any methods.
    The hosting :class:`.Application` instance is accessible
    through the :attr:`application` property.

    Example usage with two scenes interacting:

    .. code-block:: python

        class Menu(Scene):

            def __init__(self):
                self.font = pygame.font.Font(...)

            def on_enter(self, previous_scene):
                self.application.title = 'Main Menu'
                self.application.resolution = (640, 480)
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
            title = 'The Game!'
            resolution = (1280, 720)
            update_rate = 60

            def __init__(self, size):
                super().__init__()
                self.size = size
                self.player = ...
                ...

            def on_enter(self, previous_scene):
                super().on_enter(previous_scene)
                self.previous_scene = previous_scene

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

    The above two classes use different approaches for changing
    the application's settings when the scene is entered:

    1. Manually set them in :meth:`on_enter`, as seen in ``Menu``
    2. Use class variables, as I did with ``Game``

    When using class variables (2), you can leave out any setting
    (defaults to ``None``) to not override that particular setting.
    If you override :meth:`on_enter` in the subclass, you must call
    ``super().on_enter(previous_scene)`` to use the class variables.

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

        If you override this method and want to use class variables
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
