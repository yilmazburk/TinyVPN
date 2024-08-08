from flask import Flask
from routes import api_bp
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(api_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)