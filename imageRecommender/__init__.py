from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from imageRecommender.config import developmentConfig, productionConfig
import os 
from dotenv import find_dotenv, load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
print(dotenv_path)
load_dotenv(dotenv_path)


db = SQLAlchemy()

def createApp():
    app = Flask(__name__)

    if os.environ['FLASK_ENV'] == "development":
        app.config.from_object(developmentConfig)
    else:
        app.config.from_object(productionConfig)

    db.init_app(app)

    from imageRecommender.main.routes import main
    from imageRecommender.commands.commands import cmd
    app.register_blueprint(main)
    app.register_blueprint(cmd)
    # app.register_blueprint(cmd, cli_group=None)

    return app