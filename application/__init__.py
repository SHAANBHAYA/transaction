from flask import Flask
import builtins,os,logging
from flask_sqlalchemy import SQLAlchemy
from application import params
# Init the logger
formatter = logging.Formatter(
        '%(asctime)-2s %(processName)s %(threadName)s %(filename)s %(funcName)s() at %(lineno)d %(levelname)-8s %(message)s')
log = logging.getLogger(params.LOG_NAME)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
log.addHandler(streamHandler)
log.setLevel(logging.DEBUG)

log.debug("flask server init called.")
flask_app = Flask(__name__)
log.debug("flask app created.")

log.debug("DB init started")
flask_app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(params.DB_NAME)
db=SQLAlchemy(flask_app)

# Import routes and models to register with the flask_app
from application import models, params,routes
log.debug("flask db init done.")
# Creates the sqlite database and tables made in flask_models
db.create_all()
log.debug("flask db created.")
builtins.flask_app = flask_app
builtins.flask_db=db
log.info("Flask server init done.")