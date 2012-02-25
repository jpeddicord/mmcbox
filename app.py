from mmc import app
from mmc import models
from mmc import views


# logging setup
if not app.debug:
    from logging import Formatter, StreamHandler, WARNING, DEBUG
    handler = StreamHandler()
    handler.setFormatter(Formatter('%(asctime)s %(levelname)-7s %(name)s - %(message)s'))
    app.logger.addHandler(handler)
    app.logger.setLevel(WARNING)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
