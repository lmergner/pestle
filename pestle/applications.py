import gunicorn.app.base


class GunicornWrapper(gunicorn.app.base.BaseApplication):
    """ Run a uWSGI app with gunicorn without using the cli client

            @cli.command()
            def run():
                logger.warning("Starting the server!")
                APIWrapper(api, DEFAULT_GUNICORN_ARGS).run()

        See the gunicorn docs for more information: https://docs.gunicorn.org/en/latest/custom.html#custom-application
    """
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
