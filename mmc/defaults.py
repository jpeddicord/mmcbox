# Copy this file to instance/application.cfg and edit it there.

# hostname; needed for sending emails with the correct URL
# if using a localhost development server, set to None
SERVER_NAME = 'mmcbox.com'

# set to your database location
SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'

# directory user sites are stored
SITES_DIR = '/tmp/mmcbox/sites'

# session secret key; set to some random string
SECRET_KEY = None

# default mail sender
DEFAULT_MAIL_SENDER = ''

# allowed upload types and sizes
ALLOWED_EXTENSIONS = ['html', 'htm', 'txt', 'js', 'css', 'jpg', 'jpeg', 'png', 'gif']
MAX_CONTENT_LENGTH = 2 * 1024 * 1024

# email addresses errors are sent to
ADMINS = []
