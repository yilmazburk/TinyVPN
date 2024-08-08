from flask import Flask
from routes import api_bp
from config import Config
from pymongo import MongoClient
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

mongo_client = MongoClient(app.config['MONGODB_URI'])
# db = mongo_client[app.config['vpn_db']]

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)