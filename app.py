from mmc import app
from mmc import models
from mmc import views


# logging setup
if not app.debug:
    from logging import Formatter, StreamHandler, WARNING, DEBUG
    app.logger.setLevel(WARNING)

    # stdout handler
    file_handler = StreamHandler()
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)-7s %(name)s - %(message)s'))
    app.logger.addHandler(file_handler)

    # email handler
    if app.config.get('ADMINS', None):
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1', 'error@mmcbox.com', ADMINS, 'mmcbox error')
        mail_handler.setLevel(ERROR)
        mail_handler.setFormatter(Formatter('''
        Message type:       %(levelname)s
        Location:           %(pathname)s:%(lineno)d
        Module:             %(module)s
        Function:           %(funcName)s
        Time:               %(asctime)s

        Message:

        %(message)s'''))
        app.logger.addHandler(mail_handler)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
