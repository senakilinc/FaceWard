from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
bootstrap = Bootstrap(app)
moment = Moment(app)
#babel = Babel(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'mov', 'avi', 'wmv', 'flv', 'webm'}
app.config['UPLOAD_PATH'] = 'app/static/uploads'
app.config['STATISTICS_FOLDER'] = 'app/static/videos'


from app import routes, models, screenshot
